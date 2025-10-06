---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/cisco-unity-connection-split-brain/"
title: "Cisco Unity Connection – Split Brain"
domain: "www.byteworks.com"
path: "/resources/blog/cisco-unity-connection-split-brain/"
scraped_time: "2025-10-05T02:03:30.602169"
url_depth: 3
word_count: 668
client_name: "byteworks"
---

# Cisco Unity Connection – Split Brain

The _Spint Brain Recovery_ condition in Unity Connections is an odd state to find your Unity Connections cluster in, for sure. One thing is certain though, ‘_something_‘ happened, and this is the result of whatever that ‘_something_‘ was or is.

When this condition happens, what you’ll notice (either from logs or by watching the cluster node status) is that the Primary and HA servers will take turns being the cluster’s primary node every few minutes. This is because both cluster nodes have somehow ended up with slightly different database versions and the Server Redundancy Manager service cannot determine exactly which server should be primary. The cluster will try to resolve this issue on it’s own, but often times cannot.

The good news (maybe not _so_ good) is that in several cases, the cluster will continue to function and answer calls during a _split brain_. Where I have seen the _split brain_ condition cause service outage to users is with integrations that do not have sufficient SCCP/SIP ports on both cluster nodes.

What causes this can be a number of things; often it is the result of the two nodes losing network communication between themselves and/or service failure. The resolution to this condition is fairly simple, although, you’d be best served to figure out why it happened in the first place, lest you repeat it again.

Since Unity Connection is running the same core operating system as Unified Communications Manager, you can run the same diagnostic health check in Unity Connections that you would run in Unified Communications Manager; from the CLI of the Unity Connection servers issue the command _utils diagnose test_. You’ll want to resolve any issues discovered in the results of this diagnostic test before resolving the _split brain_ issue.

Assuming you have a healthy Unity Connections cluster and/or resolved the issue that caused the _split brain_ you’ll want to move on to resolution.

*   Power off / shut down the _true_ HA node (the node that is not supposed to be the true primary).
*   In the _Cisco Unity Connection Administration_ section click on _Cluster_ under _System Settings_ in the left-side vertical navigation menu and verify that both nodes are entered in correctly (albeit IP address, hostname or FQDN).
*   In the _Cisco Unity Connection Serviceability_ section of the Primary server click on _Service Management_ under the _Tools_ menu and verify that the _Coversation Manager,_ _Connection Message Transfer Agent_ and the _Connection Notifer_ services are started.
*   Restart the Unity Connections Cluster primary server. From the CLI, issue the command “_utils system restart_” and press “_Y_” to the proceeding prompt.
*   Once the rebooted primary server is back up, wait till you can access the GUI web page of the server before proceeding (in other words, wait till the Cisco Tomcat Service is operational). **Don’t Worry**, it can take a Unity Connection server upto 20 minutes or more to be fully active.
*   From the Unified Communications Server (or other type of call control server), place a call into voicemail (all you really need is something that will signal the IVR to answer) and then hang-up and wait 5 minutes before proceeding to the last step.
*   Power on the HA node (that should still be shutdown) and wait till you can access the GUI web page of the server before proceeding (in other words, wait till the Cisco Tomcat Service is operational). **Don’t Worry**, it can take a Unity Connection server upto 20 minutes or more to be fully active.
*   Verify that the _split brain_ status has been removed for the node status on the _Cluster Management_ page under _Cisco Unity Connection Serviceability_ (or issue _show cuc cluster status_ from the CLI of the cluster’s primary server).
*   Run _utils diagnose test_ on the Unity Connection servers one last time, to verify everything is still healthy and operational.
*   The cluster should be back to normal status now and the _split brain_ condition no longer shown.