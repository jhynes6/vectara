---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/the-long-treacherous-journey-to-the-collaboration-edge/"
title: "/resources/blog/the-long-treacherous-journey-to-the-collaboration-edge/"
domain: "www.byteworks.com"
path: "/resources/blog/the-long-treacherous-journey-to-the-collaboration-edge/"
scraped_time: "2025-10-05T02:03:28.506803"
url_depth: 3
word_count: 2982
client_name: "byteworks"
---

The long, treacherous journey to the Collaboration Edge! | Byteworks | IT Solutions, Services, and Consulting

[![](data:image/svg+xml;nitro-empty-id=MTAyNjo0NTg=-1;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQ1IDE3NiIgd2lkdGg9IjI0NSIgaGVpZ2h0PSIxNzYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PC9zdmc+)](/)

[

](#)

*   [Markets](https://www.byteworks.com/markets/)
*   [IT Solutions](https://www.byteworks.com/solutions/)
*   [Security](https://www.byteworks.com/solutions/security/)
*   [Infrastructure](https://www.byteworks.com/solutions/infrastructure/)
*   [Collaboration](https://www.byteworks.com/solutions/collaboration/)
*   [Cloud](https://www.byteworks.com/solutions/cloud/)
*   [Services](https://www.byteworks.com/services/)
*   [Managed Services](https://www.byteworks.com/services/managed-services/)
*   [Lifecycle Management](https://www.byteworks.com/services/lifecycle-management/)
*   [Technology Consulting](https://www.byteworks.com/technology-consulting/)
*   Resources
*   [Bits and Bytes by Byteworks](https://www.byteworks.com/bits-and-bytes-podcast/)
*   [Blog](https://www.byteworks.com/resources/blog/)
*   [Case Studies](https://www.byteworks.com/resources/case-studies/)
*   [eBooks](https://www.byteworks.com/resources/ebooks/)
*   [Events](https://www.byteworks.com/resources/events/)
*   [Cisco Technology Experience Portal](https://www.byteworks.com/cisco-technology-experience-portal/)
*   [About Us](https://www.byteworks.com/about-us/)
*   [Contact](https://www.byteworks.com/contact/)
*   [Remote Support](https://byteworks.screenconnect.com)
*   [Client Login](https://byteworks.myportallogin.com)

# The long, treacherous journey to the Collaboration Edge!

[Jeremiah Plaskett](https://www.byteworks.com/resources/blog/author/jplaskett/)

June 1, 2014

Cisco’s Collaboration Edge is one of the highly touted new capabilities of Unified Collaboration 10.X Framework.  Deploying it however, has not necessarily been an easy or painless endeavor.  This process drew blood.  To be fair, the inherent nature of how this all works is itself complex, there is no “easy button” for this.   Let’s start with the basics, before we delve into the more complex.

For those of you who may not even know what I’m talking about, a quick product overview:  Cisco Jabber is a PC, Mac, and mobile device software (iOS, Android), application that allows the user the ability to send instant messaging , and to see presence statuses (available, in a meeting, away, etc.) of their co-workers and friends.  In addition to instant messaging, you can use the software to either physically control your desk phone for calling, or you can use it as a “soft phone” and make your laptop or mobile device become your office phone while away.

The idea behind the product is great, but the real limitation has always been that unless you are physically at the office, local to the Cisco Call Control, IM and Voicemail servers, or you are connected via a VPN method of some kind, the actual usability of the product becomes greatly limited.  The Unified Collaboration market has long been hobbled by poor interoperability between products, particularly with IM and Presence.  For the ever-growing number of users on the go, mobile workers, telecommuters, etc., this solution has a huge gap in reliability.  Cisco has previously tried to address this via VPN solutions like AnyConnect, and On-Demand launching of this, but that has not worked out so great at all.  The feature simply rarely ever works as designed, is klugey, and often takes several manual attempts to get everything synched and properly working.

The new Cisco Expressway product tackles this challenge head on.  What Cisco did is leverage their existing Cisco VCS products, and by licensing them for Expressway they change product feature sets and provide Mobile and Remote device access to the UC system.  Cisco Expressway or Collaboration Edge is another name for VCS-Expressway.  It is the exact same software, it simply changes names depending on how it is licensed.  VCS-C becomes Expressway C, and VCS-E becomes Expressway-E.  The solution consists of 2 servers (you can also make HA pairs), which can be virtual and reside in the same UCS systems as with the rest of the UC Servers.  Expressway-E stands for “Edge”, and this server sits in the DMZ or on the outside (public internet) and then you have the Expressway-C for “Core” or “Control” and this server sits on the same server subnet as your voice UC systems (CUCM, CUC, etc.).

Cisco markets this solution as a VPN-less Enterprise Access and B2B Collaboration Edge Deployment.   Instead of using a VPN tunnel, VPN-less clients establish a secure and encrypted signaling path to the edge traversal platform (Cisco Expressway-E) (CUBE also supports this, but for voice only, not IM&P and VM).  VPN-less clients register with Unified CM within the enterprise (by using the secure traversal between the Expressway-E and the Expressway-C), and the secure channel to the edge traversal platform allows the client to establish an encrypted media path over the internet for calls to other enterprise devices. Inside the enterprise, signaling is typically unencrypted, whereas media can optionally remain encrypted.

Collaboration Edge VPN-Less Access with Cisco Expressway:

Unlike VPN clients, VPN-less clients provide enterprise access to Unified Communications applications only; business applications within the enterprise (such as corporate email and internal websites) are not accessible, and connections to the internet are made directly from the device rather than through the enterprise.  In addition to providing enterprise access for remote and/ or mobile employees, Cisco Expressway can also be deployed for business-to-business (B2B) communications.

So, now that the product overview and benefits are out of the way, let’s talk about the fun of deploying it:

Part 1: The Part Numbers:

Cisco Expressway Series virtual application software is available at no additional charge to customers who have a license and valid support contract for Cisco Unified Communications Manager 9.1.2 or later.  For those of you who have recently purchased this, you are most likely all set, because those part #’s and PAKs will have come with your order.  For those of you who have upgraded to 9, 10 etc., from previous versions of CUCM, your original order did not come with these PAKs, so you need to place a “Zero-Dollar” order for several part numbers.  The following illustration shows these part numbers:

Now of course I figured this out only after opening TAC case # 1 for this process. TAC pointed me to my Cisco account team.  Thankfully, we have a great Cisco team and they quickly provided me with the correct part numbers which we ordered.

Next I received 3 PAKs from Cisco from the ordering of the 14 line items above.  This brought about TAC case # 2 for this process.  There were 2 PAKs labeled EXP-E and one labeled EXP, so I made the wrong assumption to apply the EXP one to the C device, and the EXP-E ones to the E device, in the end I messed up the licensing for both.  In my defense, I had no real documentation or instructions for this process that I could find, so I was totally winging it at this point.  TAC helped me however by getting me through to the Tandberg folks.  They could never tell me the correct process I should have followed either, apparently the product is right in the middle of being transferred from legacy Tandberg support to TAC, and also from a licensing perspective as well, so this was a very gray-area still.  In the end it was former Tandberg licensing folks (now Cisco employees of course) who applied the correct option keys I needed within the devices to get them both properly licensed.  I have a feeling that the next time I deploy this product the actual licensing part may require another TAC case.

Whew, now that the licenses are on these, I sailed the rest of the way right?  Not so much.  The problem with trying to be the first is the path has not really been cleared of all the debris yet.  That was definitely the case in regards to deploying Collaboration Edge.  In retrospect, a major handicap was my inexperience with the VCS product.  If you have used this product previously, I think you are in a much better position to understand all of the requirements of deploying Collaboration Edge.  Being a rookie to the product, I scraped my elbows and knees more than once.  My second big handicap was that at the point I started to deploy the product, they had not even finished writing the “Mobile and Remote Access via Cisco Expressway Deployment Guide” yet.  I started using one document, and it actually referenced other documents that had not yet been publicly released by Cisco yet.  I had another document that was literally a rough-draft still, and left huge parts out.

Without boring everyone with all the mundane details here, let’s talk about the highlights.  My 3rd TAC case in this process started after I had configured everything per the documentation that I had, I felt like everything should work, but on my Jabber client I could never get Call Control to establish through the traversal zone.  My endpoint would not register to the CUCM, it seemed like no matter what we tried.  I disabled TLS completely, and it would not work.  Voicemail connected with no problem, so I really felt that the issue had to be firewall and/or how my Expressway was configured.  I had tested all of my certificates like crazy, and I felt good about them.

At the end of several back and forths with TAC, the issue I was having was that I started my config reading one document, abandoned it, and then continued with another document, and I got parts of my configurations messed up.  Also, I should have been following two documents all along, instead of trying to only rely on the “Mobile and Remote Access” document, I should have also followed the “Expressway Basic Configuration Deployment Guide” first.  As a result, I had my config as far as how my “E” device was configured was messed up.  I had my E device sitting in my DMZ, but I did not have NAT correctly configured on the device, or on my firewall.

The thing about the Expressway-E device, is that you have multiple deployment models.   You can just do it the “easy” way and physically assign it two LAN Interfaces.  On one LAN Interface it would get a public IP address, and on the second Interface it would be assigned a private IP address in the same VLAN as the UC voice servers.  This is less secure, because it takes the firewall completely out of the picture basically.  Any outside requests to the Expressway Edge would come into the physical public address of the device and it would then have a private address to use for communications to other UC systems.  While arguably less secure (because technically there is security inherent to the Expressway-E in this method, even though the regular corporate firewall is bypassed) this certainly keeps the configuration a lot simpler.

Another way to deploy, is two-legged with the external interface in the DMZ network, and the internal interface on the same subnet as your UC servers.  This allows for a little more control, but slightly more complex configuration.

And then you can also deploy “on a stick” in your DMZ.  In this method, you completely control what goes in/out of the IP through your firewall.  This deployment method is typical in enterprise environments, and can technically be considered more secure.  You assign the Expressway device an external IP in your DMZ range, and you NAT from your public IP to the DMZ IP.  This method seems easier at first because you only have to worry about 1 VLAN getting to the virtual machine, however the configuration is more complex from a firewall standpoint.  This is the method of deployment we chose at Byteworks.

After all the confusion here are the primary tips I would impart to others going down this road:

*   Place on DMZ if you have a requirement to.  The configuration is a lot easier two-legged on the public internet, however do consider all security requirements.
*   If you don’t see option for a second NIC, or options for NAT, you are missing the Advanced Networking License.
*   Remember to use the inside IP of the “E” device for internal DNS records.
*   You’ll need to configure NAT on your firewall from a public IP address outside your network to the DMZ address of Expressway-E, or do 1:1 public to your DMZ if you’ve deployed it with a public address.
*   HTTP Whitelisting:  Make sure to add your Unity Connection, and any other servers that Jabber needs access to.   Unity Connection requires it for Visual Voicemail to work.
*   Don’t forget to open all the ports that MRA requires on the firewall.
*   Trunk your DMZ to your ESXi hosts.

Now, after going through this process, if I had to do it all again, this is the process I would follow and the documents/links I would reference:

*   Obtain licensing (order part numbers in illustration above).
*   Deploy Virtual Machines:  Follow this guide: [https://www.cisco.com/c/dam/en/us/td/docs/voice\_ip\_comm/expressway/install\_guide/Cisco-Expressway-Virtual-Machine-Install-Guide-X8-1.pdf](https://www.cisco.com/c/dam/en/us/td/docs/voice_ip_comm/expressway/install_guide/Cisco-Expressway-Virtual-Machine-Install-Guide-X8-1.pdf "Cisco Expressway on Virtual Machine Installation Guide")
*   To keep things simple, deploy two-legged with public/inside IP address.  If you can’t do this for whatever reason, make sure to have a good understanding of firewalls or know someone 🙂 .
*   Activate License PAKs and Option Keys (I don’t really have a step-by-step for this process, because I had to open a TAC case to get mine properly licensed and applied, I am hoping it goes smoother next time as the product matures)
*   Configure the firewall (If placed in DMZ): Refer to this guide: [https://www.cisco.com/c/dam/en/us/td/docs/voice\_ip\_comm/expressway/config\_guide/X8-1/Cisco-Expressway-IP-Port-Usage-for-Firewall-Traversal-Deployment\_Guide-X8-1.pdf](https://www.cisco.com/c/dam/en/us/td/docs/voice_ip_comm/expressway/config_guide/X8-1/Cisco-Expressway-IP-Port-Usage-for-Firewall-Traversal-Deployment_Guide-X8-1.pdf "Cisco Expressway IP Port Usage for Firewall Traversal")
*   Follow this guide to prepare Expressways for basic configuration: [https://www.cisco.com/c/dam/en/us/td/docs/voice\_ip\_comm/expressway/config\_guide/X8-1/Cisco-Expressway-Basic-Configuration-Deployment-Guide-X8-1.pdf](https://www.cisco.com/c/dam/en/us/td/docs/voice_ip_comm/expressway/config_guide/X8-1/Cisco-Expressway-Basic-Configuration-Deployment-Guide-X8-1.pdf "Cisco Expressway Basic Configuration Deployment Guide")
*   Prepare and create all needed certs following this guide: [https://www.cisco.com/c/dam/en/us/td/docs/voice\_ip\_comm/expressway/config\_guide/X8-1/Cisco-Expressway-Certificate-Creation-and-Use-Deployment-Guide-X8-1.pdf](https://www.cisco.com/c/dam/en/us/td/docs/voice_ip_comm/expressway/config_guide/X8-1/Cisco-Expressway-Certificate-Creation-and-Use-Deployment-Guide-X8-1.pdf "Cisco Expressway Certificate Creation and Use")
*   To complete the setup of MRA follow this guide: [https://www.cisco.com/c/dam/en/us/td/docs/voice\_ip\_comm/expressway/config\_guide/X8-1/Mobile-Remote-Access-via-Expressway-Deployment-Guide-X8-1-1.pdf](https://www.cisco.com/c/dam/en/us/td/docs/voice_ip_comm/expressway/config_guide/X8-1/Mobile-Remote-Access-via-Expressway-Deployment-Guide-X8-1-1.pdf "Unified Communications Mobile and Remote Access via Cisco Expressway Deployment Guide")

Additional Helpful Tips:

*   To support Expressway, you must be running CUCM 9.1(2)SU1 or later.  Byteworks tested with Cisco Expressway X8.1.1, CUCM 9.1(2)SU1, CUC 9.1.1.10000-32, Cisco Jabber for Windows 9.7.0 Build 18474, Cisco Jabber for Mac Version 10.0.0 (160788i) (beta), Cisco Jabber for iPhone Version 9.6.1, and Cisco Jabber for Android 9.6.1.
*   This blog was very helpful to me for my deployment, particularly when it came to the certificate process:  [https://ciscocollab.wordpress.com/2014/01/29/deploying-collaboration-edge/](https://ciscocollab.wordpress.com/2014/01/29/deploying-collaboration-edge/ "DEPLOYING CISCO COLLABORATION EDGE")
*   You can customize the login banner, and personally we think the login UI looks awesome with our logo!:
*   I sometimes ran into deskphone mode phone connectivity issues on the Jabber for Mac application.  This occurred to me admittedly on a beta version 10.x of the client, so I did not really expect perfection.  For obvious reasons, Cisco Expressway does not support deskphone mode, it supports softphone mode.  So of course I need to launch VPN when I am remote, but still want to control my physical desk phone.  In my case, I have a Cisco 9971 IP Phone setup at my home office using the VPN Phone Proxy Feature (that could be a whole separate blog).  So in essence, I am remote from my corporate LAN, but local to my physical desk phone.  The issue would occur when I would switch from being on public internet and in softphone mode, I would login to VPN and want to switch to deskphone mode.  Often, I could not get it to register to deskphone mode unless I would kill the VPN, the Jabber application, then restart the network adapter, then relaunch VPN, then deskphone mode would register.  Crazy, I know.  I also experienced different behaviors with deskphone mode after setting up Expressway depending on what type of VPN I tested with.  I had the most success using SSL (AnyConnect), but I also tested with IPSec, both split-tunneled and non split.  Of course, I would expect some different behaviors, but in all cases the Jabber for Windows client adjusted on the fly with no issues.  I only experienced these issues on the Jabber for Mac application, and I did not test with the supported, 9.6.1 version, I was using a 10.0 beta, so I am not too concerned about these, especially with a work-around.  I only point these issues out in the event anyone else runs into them.  I’ll continue to test and provide further updates as new versions are made available.
*   We also tested this with the “Hybrid” deployment consisting of on-premise CUCM and CUC, but we use hosted IM & P through WebEx Messenger.  We had no issues with this setup.

Epilogue:

Now that we have it completely setup and working, how does it work?  Very well actually.  We’ve tested on iPhones and on Android Galaxy S4 on 2 different carriers, and we have seen above average to good performance on 4G LTE networks.  On Windows the application itself is much more dependable at this point than it is on Mac, while the iPhone version seems more stable than the Android version at this point.  We also tested with the iPad Jabber app and had great success on that as well.  Video works very well on wireless, not so great on LTE, but is adequate if you have a strong signal in most cases.  The end result is that we are very happy with the mobility of the app now.  Previously, even though we had Jabber for IPhone and Android setup it was never highly used as a dependable application because even with the “On-Demand” feature of the AnyConnect, where it was supposed to transition from the corporate LAN to external wifi/LTE and auto-launch the VPN, this simply never worked very well.  It almost always required user-intervention.  Also, the PC/Mac based versions were not reliable as well, particularly for mobile employees who spend a lot of time on-site with our various customers.  In a lot of cases, there would be restrictions to launching VPN, so relying on a VPN/Jabber combination was simply not practical in a lot of cases.  Now, with Expressway, those worries are gone and provided you have a reliable internet connection, you have access to the full functionality and power of collaboration with Jabber in almost all scenarios.  Those of us who have been using this product for a while now, are all sighing with relief and whispering “finally!”  Cisco heard us all and despite the bumps in rolling the product out, it works to address all of our concerns and is a very nice solution!

[

Previous Post

Install NVIDIA Drivers and CUDA Toolkit on Kali 1.0.6

](https://www.byteworks.com/resources/blog/install-nvidia-drivers-and-cuda-toolkit-on-kali-1-0-6/ "Install NVIDIA Drivers and CUDA Toolkit on Kali 1.0.6")[

Next Post

Layer 2 Extensibility options for Business networks

](https://www.byteworks.com/resources/blog/layer-2-extensibility-options-for-business-networks/ "Layer 2 Extensibility options for Business networks")

#### QUICK LINKS

[Case Studies](https://www.byteworks.com/resources/case-studies/)
[Privacy Policy](https://www.byteworks.com/privacy-policy/)

[](https://www.linkedin.com/company/byte-works-llc)

[](https://www.youtube.com/channel/UC0sglo13jgTeJvsoXqpyGCA)

[![](data:image/svg+xml;nitro-empty-id=MTA5ODoxODE3-1;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQ1IDE3NiIgd2lkdGg9IjI0NSIgaGVpZ2h0PSIxNzYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PC9zdmc+)](https://www.byteworks.com/)

#### ADDRESS

[2675 Breckinridge Blvd Suite 200
Du