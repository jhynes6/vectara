---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/cisco-collaboration-vt-2017-and-cisco-prime-collaboration-provisioning-update/"
title: "Cisco Collaboration VT 2017 and Cisco Prime Collaboration Provisioning Update"
domain: "www.byteworks.com"
path: "/resources/blog/cisco-collaboration-vt-2017-and-cisco-prime-collaboration-provisioning-update/"
scraped_time: "2025-10-05T02:00:28.442271"
url_depth: 3
word_count: 1426
client_name: "byteworks"
---

# Cisco Collaboration VT 2017 and Cisco Prime Collaboration Provisioning Update

Byteworks recently attended the Cisco Collaboration VT 2017 in San Jose, California at the Cisco Headquarters and we came away extremely excited about CRS 12.X, Spark, SDN, and overall, the direction of Cisco Collaboration as a whole.  There’s a lot that we came away from seeing that we simply can’t talk about yet, but we are definitely excited for our legacy on-premise Cisco Collaboration customers and our Cloud customers.  Cisco is putting great effort into modernizing their portfolio and targeting up and coming competitors to remain the premier Unified Collaboration solution.

Over 600 people from Cisco Sales Engineering, PSS and Collaboration Executives joined more than 400 of Cisco’s top Collaboration Partners from all over the world for the 5 days of sessions and labs covering all things Cisco Collaboration.  The sessions were heavy on Cisco Spark, Video, and of course SDN/App-Dev.  The overall take-away is that Cisco is aware of Amazon, Microsoft, Zoom and so many others that have been coming after the front-runner with unrelenting determination, and they have a very sound strategy to remain the market leader and the premier provider of collaboration solutions for years to come.

It is clear, that despite the great strides made by competitors, no other Collaboration vendor can offer the complete and comprehensive suite of cloud and on-premise voice, messaging and video platforms that Cisco can.  Over the next several months, we will be blogging about, and bringing many of these new technologies to our customers, and we can’t wait as the new features coming out are going to up the ante big-time on ease of use and implementation of Cisco Collaboration products.

One such product that is being improved upon quite drastically, and for which we attended a special session on at Collaboration VT, is Prime Collaboration, specifically the provisioning application itself (Prime Collaboration Provisioning Manger or PCP).  For the purpose of this blog, we won’t cover the Assurance and Analytics apps, and focus solely on the Provisioning application.  PCP has had a love/hate relationship with most of us UC engineers who have worked with it.  We love the cost and we loved the “idea” of what it can do, but the actual implementation of what it can do has always been very challenging.

There are of course 3rd-party competitors that do a beautiful job at the task of provisioning, both the initial setup of sites and users, and the post-install day to day support and moves, adds, and changes.  Full disclosure however, not every client can afford these extra expensive tools, and for many environments, these tools are too big and complicated.  For the right environment, PCP does a great job, especially installs that have fewer than five sites overall.

The issue with PCP for a lot of us, is that it is very time-consuming to set up multiple domains and sites, and often when making what should be “routine” adjustments, many things would break.  The product has also had more than it’s share of bugs.  Also, beyond the initial site setups and user import, a lot of normal routine daily changes were complicated to do, or was not supported at all.  I’m happy to say that in Cisco’s defense, they have worked tirelessly on the product and recent updates to it are finally making it much more usable.  Whereas past versions of the product had so many issues it was un-usable in may environments, Cisco has worked very hard to address these issues and make it much more usable to a larger footprint of environments.  Versions 11.5 and 11.6 had a ton of improvements and now 12.1 has even more.  This is very encouraging for us Partners who have been determined to give smaller customers an affordable and easy provisioning system for their on-premise Cisco UC systems.

The most notable improvements for 12.1 include:

*   **Root Access Disabled** – This is a pretty big change, because in older versions things would often break that required you to get into the Root Access of the system.  Typically, if you were at this point, it meant TAC became involved.  The issue was, this is a pretty big security vulnerability.  This has now been disabled.  You can now login as a troubleshooting user for a secured, time based, and limited access to the PCP functionalities.
*   **Eliminate Distributed Server Model** From PCP 12.1 onwards, the need for distributed server model (two different servers for installing a very large scale setup) has been eliminated. Both the PCP application and database can be installed on the same server to support up to 150 K endpoints. Also, there are only 3 ova types available for installation to support a range of endpoint count from 3000 to 150 K.
*   **Troubleshooting Account and Troubleshooting UI –** You, as a user with full access, can:
    *   Create a troubleshooting account (**Administration > Logging and ShowTech**) from Cisco Prime Collaboration Provisioning to debug and monitor issues.
    *   Use a troubleshooting user interface to debug and monitor the Cisco Prime Collaboration Provisioning server.
    *   Monitor the system activities such as memory usage and disk usage of the Cisco Prime Collaboration Provisioning server without root access.
    *   Use the troubleshooting user interface even when the Prime Collaboration Provisioning database or JBoss is down.
*   **Phone Button Template in Service Templates –** You can now do the following:
    *   Provision endpoints through the service templates using the Cisco Prime Collaboration Provisioning user interface and batch.
    *   Preselect a phone button template when you create a service template for an endpoint.
    *   Choose the phone button template through the endpoint service templates for automatic service provisioning and quick service provisioning.
    *   Select the **Phone Button Template** (**Provisioning Attributes > Endpoint Information**) when adding a service template through the **Provisioning Setup** menu in the Cisco Prime Collaboration Provisioning user interface.
    *   If model specific template is not set as default, and Universal Phone template is the default template, then the Universal template should get applied. If model specific template is set as default, then the selected phone button template is applied during quick service provisioning.
*   **Provisioning of Directory URIs –**  
    *   You can provision Directory URIs through the Line service template.
    *   You can add up to five Directory URIs.
    *   The template text field includes keyword support for Directory URI auto-creation along with partition.
    *   Supports a new keyword **DIRECTORYURI** in the service template. While creating a line template, if this keyword is used for a Directory URI, it will be replaced with the value set at user level.
    *   Template can include the Directory URI synchronized from LDAP.
*   **Enable Attendant Console Standard through Batch –** 
    *   You can enable Attendant Console Standard through batch provisioning from Cisco Unified CM 10.0 and later versions. To enable, you must perform the following on the Cisco Unified CM:
        *   Create a new Access Control Group
        *   Assign Roles to Access Control Group
        *   Assign Application User
        *   Assign End User Account for Presence
    *   You can create, update, and delete the Access Control Group service through batch provisioning from Cisco Unified CM 10.0 and later versions.
    *   Supports add, change, and cancel operations through the batch provisioning.
    *   Supports the following attributes:
        *   Name
        *   End user(s) to group
        *   App user(s) to group
        *   Role(s)
*   **Provisioning of Cisco Expressway Devices –** This is one we’ve definitely been waiting for!
    *   Support for Cisco Expressway Edge 8.9 and Cisco Expressway Core 8.9 from Cisco Prime Collaboration Provisioning user interface and batch.
    *   Provision the Cisco Expressway devices and Cisco Unified CM for Mobile and Remote Access and B2B Video Calling.
*   **Batch Provisioning of Auto Attendant**
    *   You can enable the Auto Attendant feature through batch with all the supported attributes from Cisco Unified CM 10.0 and later versions.  
        Supports add, change, and cancel operations through the batch provisioning.
    *   The following attributes are supported for the CTI Route Point object:
        *   Voice Mail Profile
        *   Call Forward and Call Pickup Settings—Forward All
        *   Maximum Number of Calls
        *   Busy Trigger

There are actually many more new and improved features for 12.1, these are simply the most notable at this time.  The latest documentation roadmap for 12.z can be found [here](https://www.cisco.com/c/en/us/td/docs/net_mgmt/prime/collaboration/12-1/documentation/overview/cpco_b_cisco-prime-collaboration-provisioning-documentation-overview-12-1.html).  We will be attending the Prime Collaboration Breakout session at Cisco Live, and will provide further updates after this.  Don’t forget, if you’re a Byteworks’ client and you’re going to Cisco Live 2017 (June 25-29 2017), let us know, we’d love to see you there!