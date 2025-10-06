---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/reload-in-x-there-is-a-better-way/"
title: "/resources/blog/reload-in-x-there-is-a-better-way/"
domain: "www.byteworks.com"
path: "/resources/blog/reload-in-x-there-is-a-better-way/"
scraped_time: "2025-10-05T02:01:17.293242"
url_depth: 3
word_count: 1504
client_name: "byteworks"
---

Reload in X? There Is a Better Way | Byteworks | IT Solutions, Services, and Consulting

[![](data:image/svg+xml;nitro-empty-id=MTAzMjo0NTg=-1;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQ1IDE3NiIgd2lkdGg9IjI0NSIgaGVpZ2h0PSIxNzYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PC9zdmc+)](/)

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

# Reload in X? There Is a Better Way

[Brian Hartsfield](https://www.byteworks.com/resources/blog/author/bhartsfield/)

March 1, 2022

As network engineers, we have all been there when you make changes to a device remotely, something goes wrong and you get locked out. This results in either having to call someone on-site, or having to drive several hours to the site to fix the issue. While there is a commonly used workaround for this, we’ll take a deep dive into a better, lesser known, way that has actually been in iOS for a while.

## **The Old Way – Reload in X**

For many years, engineers have used “reload in x” to get around this problem. This method will reboot the router in x number of minutes if “reload cancel” isn’t entered. While this workaround may be shorter than a physical trip to your client’s office, it is a bit of a sledgehammer approach. You now have to reboot the whole device and are at the mercy of how long it takes for that device to do so—_which oh by the way on some platforms can be a while—_versus the x number approach.

## **The Better way – Revert Timers**

Cisco does have commands that will allow you to revert config changes and even replace the running config without having to do a reload on the router. These commands for rolling back configurations can be very useful especially when working remotely on a site or doing complex changes. Either way, if things don’t work out as planned, the ability to stop and return to your starting point can be very useful.

### Step 1 – Configure an Archive Directory

The first step to do this is to configure an archive directory where the saved config files will be stored. By default it will save up to 10 different versions and you can go back and look at them later if needed. In this example, archive will be prefixed to the file names. If you want these in a directory, you’ll need to add a trailing slash. With this, config files will be named “archive-<datetime>” and put in the root of the flash drive.

To setup an archive location, you’ll want to run something like the examples below:

**_Enter configuration commands, one per line. End with CNTL/Z._**
**_Router(config)#archive_**
**_Router(config-archive)#path flash:archive_**
**_Router(config-archive)#exit_**
_**Router(config)#exit**_

Let’s take a look at what this looks like and how it works. In this example, I have a router with the following configuration on it:

_**interface GigabitEthernet0/0**
**ip address 1.1.1.1 255.255.255.0**
_

### Step 2 – Set a Revert Timer

I want to change the IP to 2.2.2.2 but want it to revert back in 1 minute if something goes wrong. In this case, I am going to use “configure t revert timer x”.  (x can be 1-120 and is in minutes)

_**Router#conf t revert timer 1**_
_**Rollback Confirmed Change: Backing up current running config to flash:archive-Feb-15-15-56-38.517-1**_

_**Enter configuration commands, one per line. End with CNTL/Z.**_
_**Router(config)#Rollback Confirmed Change: Rollback will begin in one minute.**_
_**Enter “configure confirm” if you wish to keep what you’ve configured**_

_**\*Feb 15 15:56:41.528: %ARCHIVE\_DIFF-5-ROLLBK\_CNFMD\_CHG\_BACKUP: Backing up current running config to flash:archive-Feb-15-15-56-38.517-1**_
_**\*Feb 15 15:56:41.529: %ARCHIVE\_DIFF-5-ROLLBK\_CNFMD\_CHG\_START\_ABSTIMER: User: console(Priv: 15, View: 0): Scheduled to rollback to config flash:archive-Feb-15-15-56-38.517-1 in 1 minutes**_
_**\*Feb 15 15:56:41.573: %ARCHIVE\_DIFF-5-ROLLBK\_CNFMD\_CHG\_WARNING\_ABSTIMER: System will rollback to config flash:archive-Feb-15-15-56-38.517-1 in one minute. Enter “configure confirm” if you wish to keep what you’ve configured**_

_**Router(config)#int gig 0/0**_
_**Router(config-if)#ip address 2.2.2.2 255.255.255.0**_

**<after 1 minute>**

_**Rollback Confirmed Change: rolling to:flash:archive-Feb-15-15-56-38.517-1**_

_**\*Feb 15 15:57:41.535: %ARCHIVE\_DIFF-5-ROLLBK\_CNFMD\_CHG\_ROLLBACK\_START: Start rolling to: flash:archive-Feb-15-15-56-38.517-1**_
_**\*Feb 15 15:57:41.560: Rollback:Acquired Configuration lock.**_
_**!Pass 1**_
_**!List of Rollback Commands:**_
_**interface GigabitEthernet0/0**_
_**no ip address 2.2.2.2 255.255.255.0**_
_**interface GigabitEthernet0/0**_
_**ip address 1.1.1.1 255.255.255.0**_
_**end**_

_**Total number of passes: 1**_
_**Rollback Done**_

As you can see, we end up exactly back where we started. In the output given after the rollback, it runs 1 pass in this case, but depending on changes, could run multiple times to undo all the changes you may have made. In the event that the changes did work properly, and you wanted to keep them, and cancel the conversion, you run:

_**configure confirm**_

If you look in the output after running the “configure t revert timer x” command, it tells you exactly what you need to run. What’s more, if you made changes, but quickly realized that they were not working and wanted to revert back immediately, you run:

_**configure revert now**_

### Configuration Replacement (With Rollback)

Something else that can be very useful is the ability to replace the running config. Before big changes, we’ll always make a copy of the current running config so we can revert back if there are issues. _How_ you go back to the old config is super important, however. If you just do “copy old.conf running-config”, Cisco will do an APPEND and not a REPLACE and you may not get what you were looking for.

For example, you run:

_**interface GigabitEthernet0/0**_
_**ip address 2.2.2.2 255.255.255.0**_

_**ip route 0.0.0.0 0.0.0.0 2.2.2.3**_

and a file called old.conf of:

_**interface GigabitEthernet0/0**_
_**ip address 1.1.1.1 255.255.255.0**_

_**_ip route 0.0.0.0 0.0.0.0 1.1.1.2_
**_

running “copy old.conf running” results in the following:

_**Router#copy old.conf running-config**_
_**Destination filename \[running-config\]?**_
_**3005 bytes copied in 0.433 secs (6940 bytes/sec)**_

_**Router#sh run**_

_**interface GigabitEthernet0/0**_
_**ip address 1.1.1.1 255.255.255.0**_

_**ip route 0.0.0.0 0.0.0.0 2.2.2.3**_
_**ip route 0.0.0.0 0.0.0.0 1.1.1.2**_

The IP address changed, but because of the append, you now have two default routes which was not the desired outcome. Most network engineers will copy the old configuration file to startup and reboot, but here again we are having to wait on the entire router to reboot. Instead, you can do “configure replace” to replace what is there and apply the same rollback timer as mentioned above.

Let’s take a look at what this looks like and how it works.

_**Router#configure replace flash:old.conf list time 1**_
_**Rollback Confirmed Change: Backing up current running config to flash:archive-Feb-15-16-44-14.943-6**_

_**This will apply all necessary additions and deletions**_
_**to replace the current running configuration with the**_
_**contents of the specified configuration file, which is**_
_**assumed to be a complete configuration, not a partial**_
_**configuration. Enter Y if you are sure you want to proceed. ? \[no\]: yes**_
_**\*Feb 15 16:44:20.538: %ARCHIVE\_DIFF-5-ROLLBK\_CNFMD\_CHG\_BACKUP: Backing up current running config to flash:archive-Feb-15-16-44-14.943-6**_

_**\*Feb 15 16:44:22.430: Rollback: Acquired Configuration lock.**_
_**!Pass 1**_
_**!List of Rollback Commands:**_
_**no ip route 0.0.0.0 0.0.0.0 2.2.2.3**_
_**interface GigabitEthernet0/0**_
_**no ip address 2.2.2.2 255.255.255.0**_
_**interface GigabitEthernet0/0**_
_**ip address 1.1.1.1 255.255.255.0**_
_**ip route 0.0.0.0 0.0.0.0 1.1.1.2**_
_**end**_

_**Total number of passes: 1**_
_**Rollback Done**_

_**Router#Rollback Confirmed Change: Rollback will begin in one minute.**_
_**Enter “configure confirm” if you wish to keep what you’ve configured**_

_**\*Feb 15 16:44:30.187: %ARCHIVE\_DIFF-5-ROLLBK\_CNFMD\_CHG\_START\_ABSTIMER: User: console(Priv: 15, View: 0): Scheduled to rollback to config flash:archive-Feb-15-16-44-14.943-6 in 1 minutes**_
_**\*Feb 15 16:44:30.238: %ARCHIVE\_DIFF-5-ROLLBK\_CNFMD\_CHG\_WARNING\_ABSTIMER: System will rollback to config flash:archive-Feb-15-16-44-14.943-6 in one minute. Enter “configure confirm” if you wish to keep what you’ve configured**_
_**Router#**_

In this example, the “list” command is optional and gives the output of what specifically was changed. The “time x” is also optional but will configure the rollback. As mentioned previously, the same “configure revert now” and “configure commit” commands apply.  This configure replace feature can also be useful when making a lot of changes at once. The new configuration file can be staged on the device, and when it comes to the maintenance window time, you can run configure replace to make all the changes at once. If there are issues, you always have the optional rollback.

### Old Habits Don’t Have to Die Hard

Cisco has a decent collection of commands to allow rollback of configurations and to do a REPLACE instead of an APPEND operation on the running-config. Many seasoned engineers rely on the old way of “reload in x” and “copy old.conf startup-config” merely out of habit. The good thing about these newer commands is that they are fairly simple to implement, and in the long run, can save network engineers a great deal of time no longer having to wait on a reboot.

If you’d like to learn more about exciting, time-saving advancements like this, we’d love to share them. [Contact us today!](https://www.byteworks.com/contact/)

[

Previous Post

The All-New Webex Contact Center from Cisco – A Sneak Peek!

](https://www.byteworks.com/resources/blog/the-all-new-webex-contact-center-from-cisco-a-sneak-peek/ "The All-New Webex Contact Center from Cisco – A Sneak Peek!")[

Next Post

Meraki API Basics – Pulling Data from Meraki

](https://www.byteworks.com/resources/blog/meraki-api-basics-pulling-data-from-meraki/ "Meraki API Basics – Pulling Data from Meraki")

#### QUICK LINKS

[Case Studies](https://www.byteworks.com/resources/case-studies/)
[Privacy Policy](https://www.byteworks.com/privacy-policy/)

[](https://www.linkedin.com/company/byte-works-llc)

[](https://www.youtube.com/channel/UC0sglo13jgTeJvsoXqpyGCA)

[![](data:image/svg+xml;nitro-empty-id=MTEwNjoxODE3-1;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQ1IDE3NiIgd2lkdGg9IjI0NSIgaGVpZ2h0PSIxNzYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PC9zdmc+)](https://www.byteworks.com/)

#### ADDRESS

[2675 Breckinridge Blvd Suite 200
Duluth, GA 30096](https://maps.app.goo.gl/CgnvPBK2ABG9MFnY6)

#### CONT