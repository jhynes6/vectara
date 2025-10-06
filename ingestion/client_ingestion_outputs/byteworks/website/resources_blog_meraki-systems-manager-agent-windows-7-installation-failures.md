---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/meraki-systems-manager-agent-windows-7-installation-failures/"
title: "Meraki Systems Manager Agent – Windows 7 Installation Failures"
domain: "www.byteworks.com"
path: "/resources/blog/meraki-systems-manager-agent-windows-7-installation-failures/"
scraped_time: "2025-10-05T02:00:26.493955"
url_depth: 3
word_count: 680
client_name: "byteworks"
---

# Meraki Systems Manager Agent – Windows 7 Installation Failures

In some cases it appears that when attempting to install the Meraki Systems Manager Agent (MerakiPCCAgent.msi) in Windows people have experienced the following error:

> **There is a problem with this Windows Installer package. A program run as part of the setup did not finish as expected. Contact your support personnel or package vendor.**

Just before this error is observed, there is a brief period that some text is flashed up on a command-line window but quickly vanishes before it can be read (which as usual is quite helpful). The line people seem to normally catch is the following:

> **main(): cannot use Windows temp; use GetTempPath Agent registration.**

With the help of a screen recorder the complete text in one particular instance has been captured and provided below:

Looking at this output more closely provides an important clue about the issue. The path for the script file is incomplete. In fact, the user profile path in this instance should be “C:\Users\Rob Patmore”. It became clear at this point that the issue was the script not taking into consideration any profile folder name with a space in it. Anyone who has created a Windows username with a space in it will result in this scenario. After removing the space and updating the user profile path to be “C:\Users\Rob” the installation was able to complete successfully without any further issues.

While the solution is clear, the steps to get there may not be. The simpler option would be to create a whole new user profile on the computer, but for those that want to salvage the existing profile this can also be done. For awareness, this may be impacting to some applications that don’t utilize the %USERPROFILE% variable in all cases and instead have the path directly assigned. This doesn’t appear to be an issue with most applications, but it is something to be aware of and would have to be addressed for each of those cases individually. Microsoft Outlook 2013 has been observed to handle it properly except for the path to the cache file when using cached Exchange mode and will result in building a new local cache of the email at the old path. Microsoft has a KB article [https://support.microsoft.com/kb/2752583](https://support.microsoft.com/kb/2752583) which addresses the options for changing it.

Below are the outlined steps necessary in order to change the profile folder path. It is strongly advised to only proceed if comfortable with making changes to the Windows Registry.

1. It will be necessary to use a different account with administrator access in order to complete these steps. If a second account is not yet available, one can be created following the steps below. If there is already a separate administrator account available, proceed to step 2.
    * Open Control Panel
    * Select User Accounts from the list
    * Select “Manage another account” to view/manage the list of local accounts active on the computer.
    * Select Create a new account
    * Enter an account name of your choosing then be sure to change the option from Standard User to Administrator before clicking Create Account. You will be returned to the previous window and the account created will be shown and set as an Administrator
2. Log off the computer then log back on with the other administrator account. It is important that you log off of the account you are changing and not just switching users.
3. Open Windows Explorer and proceed to the path C:\Users. Rename the existing profile folder to a new name without spaces.
4. Open the Windows Registry Editor.

Navigate in the Windows Registry to HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList. Within the ProfileList folder, there are multiple sub folders. Check each of them until you identify the one with a key ProfileImagePath that matches the old user profile path. An example of what you should expect to see is provided below.

Double-click on that key to edit and update the value to the new path after the folder rename. Click OK.

Reboot the machine and the install should complete.