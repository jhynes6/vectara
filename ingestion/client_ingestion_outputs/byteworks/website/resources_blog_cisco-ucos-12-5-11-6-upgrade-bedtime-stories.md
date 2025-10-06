---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/cisco-ucos-12-5-11-6-upgrade-bedtime-stories/"
title: "/resources/blog/cisco-ucos-12-5-11-6-upgrade-bedtime-stories/"
domain: "www.byteworks.com"
path: "/resources/blog/cisco-ucos-12-5-11-6-upgrade-bedtime-stories/"
scraped_time: "2025-10-05T02:00:36.521837"
url_depth: 3
word_count: 1397
client_name: "byteworks"
---

Cisco UCOS 12.5/11.6 Upgrade Bedtime Stories | Byteworks | IT Solutions, Services, and Consulting

[![](data:image/svg+xml;nitro-empty-id=MTAzMDo0NTg=-1;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQ1IDE3NiIgd2lkdGg9IjI0NSIgaGVpZ2h0PSIxNzYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PC9zdmc+)](/)

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

# Cisco UCOS 12.5/11.6 Upgrade Bedtime Stories

[Jeremiah Plaskett](https://www.byteworks.com/resources/blog/author/jplaskett/)

October 6, 2019

I’ve decided a blog detailing the upgrade experience in Cisco’s UCOS 12.5 UCCX 11.6 release would be a good enough read for a blog, as there are some some items to look out for. I recently completed an v10.5 to v12.5 upgrade in a large environment and it was completely successful (_flawless victory_ for the 90s Midway / Acclaim Entertainment fans..), but there were several things I learned. I won’t go into procedural detail about Cisco UCOS upgrades generally, as its beyond the scope of this blog, but I will share some upgrade basics and then some of the unique experiences in the 12.5 upgrade that are different from other version upgrades.

In this blog, I’ll be covering the upgrade experience **_from_** the following applications;

*   Cisco Unified Communications Manager v10.5
*   Cisco IM and Presence v10.5
*   Cisco Unity Connection v10.5
*   Cisco Unified Contact Center v10.6

## The Upgrade Basics

#### The Fail-Safe Plan

As a matter of good practice, **_ALWAYS_** have a complete and recent DRS backup set from each Cisco UC server application before attempting any upgrade. This is, ultimately, your only _officially_ and _completely_ supported fail-safe to recover from a total loss server failure. That said, if you have the option, allowance and ability; powering down each server and copying the entirety of the server’s VM files to a separate location will do just fine as well. However, DRS is the only way to backup with the server powered on, and be officially supported. Some UC ninjas have tried snapshots while the VM is powered on, but I’m not going to discuss or endorse that. Its generally a bad idea, it is not supported and if it isn’t done with precision, can cause way more problems than it was ever meant to solve.

#### The Expectation

Understand that an upgrade to version 12.5 is a _refresh_ _upgrade_ which is different than non refresh upgrades. The most substantial difference is that the server is powered down during the upgrade rather than being able to remain up while the upgrade is installed into the inactive partition. You must consider that while this won’t render a UC cluster of servers completely unusable, it will created degraded experiences and, UC applications without a cluster or HA server will be completely unusable during the upgrade.

Personally, I like to estimate a 2 hour maintenance window per UC server for a refresh upgrade. In the 12.5 upgrade I completed recently, there were 8 UC servers involved so I gave the client an 18 hour total expectation (I always add 2 extra outage hours to every actual outage estimate). Ultimately, I was able to get it done in just under 14 hours, and that is with a few road bumps encountered.

The client in my recent upgrade is a 24/7/365 medical facility, so finding the _perfect_ 18 hour window was very challenging; keep this in mind when crafting your business statement for the upgrade expectation. Know how the business operates and propose time frames that are likely to be the least impactful to the business.

Finally, have all the necessary upgrade files and images already staged in the environment before the upgrade. While 2 hours per server is a fair amount of time, it will mostly take that amount of time and doesn’t include a lot of spare time for downloading / uploading files.

## The 12.5 Upgrade Experience

UCOS 12.5 is based on CentOS Linux rather than the RedHat Linux so many of us are familiar with. The differences between the two that you’ll most likely encounter during the upgrade are in the way the two operating systems are installed through Cisco’s appliance image (ISO). Here is a list of items I noted during my upgrade that stood out to me.

#### General

*   During the refresh upgrade process when the server does the first reboot, there is a point where the CLI (assuming VMware Console) will be complete BSOD (Blue Screen of Death) for about 25 minutes and CPU/MEM stats on the VM will bottom out.
*   This is _normal_! The server will continue installing shortly after you start getting white knuckles and think the upgrade has somehow failed (about 25 minutes).
*   Next, the server reboots and right after the SELinux update it may start throwing error messages about missing files on the OS and will look scary. It will get past this in about 15 minutes and do a final reboot.
*   The upgrade should be applied via Direct Attachment / CD-DVD and initiated via VMware console CLI.
*   Make sure to power the server down and switch the VM OS type to Cent OS 4/5 64bit (after the upgrade is completed), in addition to any other VM changes needed in your upgrade scenario, as it does make a material difference to the VM’s performance.
*   Make sure the business has a Smart License Account setup _before_ the upgrade and consider converting the licenses _before_ the upgrade. You’ll still get the same 90 day grace period after the upgrade like the PLM model offered, it’s just easier to me if this is handled before the upgrade.
*   Take a screenshot of the PLM usage and inventory before upgrading! This is invaluable! If you have a standalone PLM, not as big of a deal as you hopefully can just leave it running should you need to reference it.
*   I’d suggest converting the PAK based licenses into the SLA (Smart License Account) 1-2 days before the upgrade. The real risk here is that if the business for some reasons scraps the upgrade altogether, their licenses might have been converted to version 12 and their servers didn’t upgrade, and this could potentially cause support/entitlement issues in the future.
*   This will take an act of Congress (GLO) to undo. So its best to wait as long as possible before converting the licenses. Some might even say wait till after the upgrade, but I like my exits as clean as possible with little to no post-effort / punch-list items.

#### Unity Connection Specifically

*   Any Unity Connection version being upgraded that is version 11.0 or lower requires the _ciscocm.cuc\_upgrade\_12\_0\_v1.2.k3.cop.sgn_ upgrade COP before a refresh upgrade can be applied to the server.
*   Unity Connection version 12.x uses a different image file (ISO) than Unified communications Manager, which is a departure from the last few major versions.

#### Unified Contact Center Express Specifically

*   Adjust the VM to the correct memory usage (Ex. in 11.6.2 the 100 agent size uses 10GB instead of 8GB) _BEFORE_ attempting the refresh upgrade.
*   If you don’t adjust the memory first, the server will tell you you’re using the wrong OVA template and won’t let you upgrade.
*   The VMware OS type remains RedHat 6 64Bit for UCCX 11.6.2
*   Apply the ES04 cumulative update after the refresh upgrade to version UCCX 11.6.2.
*   ES04 is applied to all UCCX servers
*   ES04 MUST be install via CLI (it restarts the Cisco tomcat service multiple times).
*   The ES04 update itself, takes about 40 minutes per server. Be sure to add that to the two hour per server estimate when calculating TEO (total expected outage).

In all, my upgrade experience to Cisco UCOS version 12.5 wasn’t that difficult and mostly inline with other UC refresh upgrades I’ve experienced, outside of the server installation behavioral differences.

If you are looking to upgrade your Cisco UC infrastructure to version 12.5 or have any questions, we’d love to talk to you about them. Please feel free to contact us!

[

Previous Post

Cisco Unity Connection – Split Brain

](https://www.byteworks.com/resources/blog/cisco-unity-connection-split-brain/ "Cisco Unity Connection – Split Brain")[

Next Post

Cisco Webex Enabled Conference Room

](https://www.byteworks.com/resources/blog/cisco-webex-enabled-conference-room/ "Cisco Webex Enabled Conference Room")

#### QUICK LINKS

[Case Studies](https://www.byteworks.com/resources/case-studies/)
[Privacy Policy](https://www.byteworks.com/privacy-policy/)

[](https://www.linkedin.com/company/byte-works-llc)

[](https://www.youtube.com/channel/UC0sglo13jgTeJvsoXqpyGCA)

[![](data:image/svg+xml;nitro-empty-id=MTE3NjoxODE3-1;base64,PHN2ZyB2aWV3Qm94PSIwIDAgMjQ1IDE3NiIgd2lkdGg9IjI0NSIgaGVpZ2h0PSIxNzYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PC9zdmc+)](https://www.byteworks.com/)

#### ADDRESS

[2675 Breckinridge Blvd Suite 200
Duluth, GA 30096](https://maps.app.goo.gl/CgnvPBK2ABG9MFnY6)

#### CONTACT