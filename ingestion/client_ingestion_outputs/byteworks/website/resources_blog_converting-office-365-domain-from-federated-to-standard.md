---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/converting-office-365-domain-from-federated-to-standard/"
title: "Converting Office 365 Domain from Federated (SSO) to Standard"
domain: "www.byteworks.com"
path: "/resources/blog/converting-office-365-domain-from-federated-to-standard/"
scraped_time: "2025-10-05T02:02:22.875830"
url_depth: 3
word_count: 1173
client_name: "byteworks"
---

# Converting Office 365 Domain from Federated (SSO) to Standard

Being a person who has had a long love/hate relationship with Microsoft products, I have to say that I have been very pleased with what Microsoft has done with the Office 365 suite – particularly with Exchange Online and SharePoint Online, the hosted versions of their popular messaging and collaboration products.

What has not been great, however, is the implementation of Active Directory Federation Services with the Office 365 infrastructure when attempting to use Single Sign-On (SSO) to transparently authenticate local AD domain users to Office 365 services. I recently had a scenario where a domain that was using Directory Sync and SSO (Federation) needed to be converted back to a Standard domain. In theory, Single Sign-On is a great capability that provides convenient transparent access to Office 365 services for users on your internal Active Directory domain. In practice, I don’t believe Microsoft truly has a handle on how to make this service reliable as of yet. After many support cases, several being escalated very high within the Office 365 server support team and still being told “We know ADFS is broken right now, so please wait two weeks and try again”, it was clear that SSO just wasn’t ready for primetime. But removing SSO can be perilous too, as minimizing the impact to the users is critical. Nobody wants have to reset and distribute new passwords to dozens or hundreds of users. Below is an account of the steps I performed to make this happen nearly transparently to the users.

First, to define two concepts: Directory Sync and Single Sign-On:

Directory Sync is an application developed by Microsoft to be installed on a local domain-member server (Windows 2008 R2 or better, x64). It is designed to pull user account attributes from the local Active Directory domain and synchronize them to the Office 365 account. This includes user information such as phone number, address, job title, and so on. In more recent versions, this also includes the option to synchronize user passwords. With full Directory Sync integration, a local domain user would be able to access their Office 365 services by going to the appropriate location (i.e., https://office365.microsoft.com) and entering their organizational domain username and password when prompted.

Single Sign-On can be added to work in conjunction with Directory Sync to provide transparent user authentication for users accessing their company’s Office 365 services while logged in as a domain user on a domain-member PC. Essentially this works by configuring the Active Directory Federation Services infrastructure locally within the domain, and then logins to an Office 365 service redirect the user to their own organization’s SSO proxy server, where the credentials are passed transparently through Kerberos, and then the SSO proxy server redirects the user back to the requested Office 365 service page, complete with an authentication token showing that the user has successfully authenticated. For more information on ADFS, refer to the following link: [https://technet.microsoft.com/en-us/windowsserver/dd448613.aspx](https://technet.microsoft.com/en-us/windowsserver/dd448613.aspx). SSO does not synchronize any of the directory information, and therefore would often be used in conjunction with Directory Sync. Note that when using SSO, the user password that may be synchronized via the Directory Sync application is completely irrelevant, as all password entry/verification is performed entirely on the internal ADFS proxy server.

With those two concepts defined, we can go through the following process to disabled Federation/SSO, if you so desire.

I highly recommend that you perform the steps using an administrator account local to Office 365 (an account whose status is “In Cloud” and set as a Global Administrator under Users and Groups within the Office 365 control panel), in order to avoid any problems accessing the environment during the conversion.

1. Open the Windows Azure Active Directory Module for PowerShell and perform the normal connection process as shown below. If you do not have the Windows Azure module, you can download it from here: https://technet.microsoft.com/en-us/library/jj151815.aspx#bkmk_installmodule. Although, if you do not have the Windows Azure module, it’s unlikely you would have been able to set up federation/SSO in the first place.

   ```powershell
   $cred = Get-Credential  
   Connect-MSOLService -Credential $cred
   ```

2. Configure the domain authentication type to be ‘Managed’

   ```powershell
   Set-MsolDomainAuthentication -Authentication Managed -DomainName
   ```

3. Convert the Windows Azure users from Federated to Standard. When you do this, all of the passwords for the users within Windows Azure will be reset (within 365, not within your local AD domain). This is unavoidable. Again, in our scenario, the domain is using Directory Sync anyway and we will soon replace these temporary passwords with those contained within Active Directory.

   ```powershell
   Get-MsolUser | Convert-MsolFederatedUser
   ```

   At this point, the user passwords are all reset, and the output shows the temporary password for each user.

4. Next, we need Directory Sync to push out all local AD user passwords to Windows Azure. The behavior of Office 365 is that, with Directory Sync, user passwords can then be changed directly on the Office 365 control panel (or through the Set-MsolUserPassword PowerShell cmdlet) and that password will then remain separate from the user’s AD password until such time as they change their password within AD, at which point the change will be captured and synchronized up to Windows Azure. A full password synchronization is required to overwrite the temporary passwords created above with the current user passwords within AD.

   The ability to perform a full password synchronization is a feature that requires Directory Sync version 6438.03 or newer. You can check the version by opening regedit and looking at the following key:

   ```plaintext
   HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft\Online Directory Sync\DisplayVersion
   ```

   It will say something to the effect of 1.0.xxxx.xx (as of the time of this post), where xxxx.xx must be at least 6438.03. If you do not have the minimum required version, you can download Directory Sync from the Office 365 control panel, under Users and Groups.

   Open a PowerShell session and run the following commands:

   ```powershell
   cd C:\Program Files\Windows Azure Active Directory Sync\  
   .\DirSyncConfigShell.psc1  
   Set-FullPasswordSync
   ```

   This will enable a full password synchronization when the services are restarted.

   Open Services  
   Restart “Forefront Identity Manager Synchronization Service”  
   It also restarts “Windows Azure Active Directory Sync Service”

5. Verify the full password synchronization by opening Event Viewer and looking in the Application Event Log.

   Look for a source of “Directory Synchronization” with an Event ID of 656. The details of the event will list the users for which password sync is starting.

   After a minute or two, you should see Event ID 657 that shows the status (success or failure) of the password synchronization for each user.

At this point, your Active Directory users should be able to successfully log into their Office 365 services using their AD credentials, and any future user password changes should also automatically synchronize over to Windows Azure. In case you’re wondering (as I was initially, based on experience with other sync tools), Director Sync does NOT require a user to first change their password before it can be captured and synchronized. Directory Sync pulls passwords “at rest” from AD.