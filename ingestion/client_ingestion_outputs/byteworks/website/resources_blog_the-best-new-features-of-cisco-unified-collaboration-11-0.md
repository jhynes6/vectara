---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/the-best-new-features-of-cisco-unified-collaboration-11-0/"
title: "The Best New Features of Cisco Unified Collaboration 11.0"
domain: "www.byteworks.com"
path: "/resources/blog/the-best-new-features-of-cisco-unified-collaboration-11-0/"
scraped_time: "2025-10-05T02:03:44.278944"
url_depth: 3
word_count: 1931
client_name: "byteworks"
---

# The Best New Features of Cisco Unified Collaboration 11.0

Cisco recently released version 11.0(1) of their IP Telephony applications, specifically Communications Manager (formerly CallManager, CUCM), IM and Presence (CIMP), and Unity Connection (CUC). While we would normally stay away from a “dot zero” release, and encourage waiting till .5, we have been testing 11.0 and have found some very useful new features and enhancements that will have some companies wanting to take the plunge and go ahead and upgrade. We’ve compiled these here and while some may not be worth upgrading right now for, some are definitely cool and worth the consideration.

The actual list of all the new enhancements are quite long, and we will go over several here, but only the ones we really find useful, some not so much, but others definitely cool. For the full lists of new and changed features, check out the Cisco release notes for the referenced applications.

Let’s start with some new **Information Assurance** features. When end users (with either local or LDAP credentials) and administrators log in to web applications for Cisco Unified Communications Manager or IM and Presence Service, the main application window displays the last successful and unsuccessful login details. This is good information to be able to see for Admins. this is true for all of the various administration pages of the CUCM and IM and P application pages. For the Platform admin pages, (OS Admin and DRS), only Administrators logging in can see the last login details.

A long overdue improvement within CUCM and CIMP Release 11.0 are the support of **Enterprise Groups**. Cisco Jabber users can search for groups in Microsoft Active Directory and add them to their contact lists. If a group that is already added to the contact list is updated, the contact list is automatically updated, per the LDAP Directory Sync schedule as configured.

Currently, the Enterprise Groups feature is supported only on the Microsoft Active Directory server. It is not supported on Active Directory Lightweight Directory Services (AD LDS) and other corporate directories.

The **Conference Now** feature allows both external and internal callers to join a conference by dialing a Conference Now **IVR** (another new feature enhancement to CUCM) Directory Number, which is a centralized conference assistant number. This is a big enhancement over MeetMe, and is also a long overdue feature for CUCM. An IVR application guides the caller to join the conference by playing announcements. A conference is established using a Meeting Number, which is the same as the Self-Service User ID. The meeting number is configured by the administrator in the end user’s window. The Self-Service User ID is usually same as the user’s primary extension number. The host (End User) provides the Meeting Number, Time slot, and Attendees Access Code to all the participants. The host requires a PIN to join the conference, but the participants do not require it. If a participant dials into the meeting before the host, the participant hears Music on Hold (MOH). After the host enters both Meeting Number and PIN correctly, a conference bridge is allocated based on the MRGL (Media Resource Group List) of the host. Participants who join before the start of the meeting are redirected to the same conference bridge. The host can set the Attendees Access Code for a secure conference call. There are some limitations for Conference Now, that we should point out such as the inability for the host to mute participants, the inability to see a conference participant list, and the lack of support for Video on Hold, however this is still a nice conference bridge alternative to expensive services and will meet the needs of plenty of businesses.

There is a new **Emergency Call Handler** which helps you to manage emergency calls in your telephony network while following local ordinances and regulations. In the past, one could only get these abilities from a full deployment of Cisco Emergency Responder (CER), so this is a major enhancement to CUCM that saves money. It is not as robust as CER, but it definitely will meet the needs of a lot of businesses. When an emergency call is made the following is required:

* The emergency call must be routed to the local Public-Safety Answering Point (PSAP) based on the location of the caller.
* The caller’s location information must be displayed at the emergency operator terminal. The location information can be obtained from an Automatic Location Information (ALI) database.

This is now all handled within configuration parameters and setup objects within CUCM, and is simple to configure and maintain.

Another new feature is **LDAPv3-compliant** directories with Cisco Unified Communications Manager and Cisco Unity Connection.

New support for the **Opus codec** is an interactive speech and audio codec that is, specially designed to handle a wide range of interactive audio applications such as VoIP, video conferencing, in-game chat, and live distributed music performance.

**Security Enhancements**

CUCM 11.0 now supports **Online Certificate Status Protocol (OCSP)**, which allows a device to obtain real-time information about the status of a certificate. Examples of certificate status are Good, Revoked, and Unknown. CUCM uses OCSP for validating third-party certificates that are uploaded into the Cisco Unified Communications Manager trust store. CUCM requires an OCSP Responder URL to connect to the OCSP responder server over HTTP. It sends an HTTP request to the responder to validate a certificate.

CUCM 11.0 now supports **Elliptic Curve Digital Signature Algorithm (ECDSA) certificates**. These certificates are stronger than the RSA-based certificates and are required for products that have Common Criteria (CC) certifications. The US government Commercial Solutions for Classified Systems (CSfC) program requires the CC certification and so, it is included in CUCM 11.0. The ECDSA certificates are available along with the existing RSA certificates in the following areas—Certificate Manager, SIP, Certificate Authority Proxy Function (CAPF), Transport Layer Security (TLS) Tracing, Entropy, HTTP, and computer telephony integration (CTI) Manager.

With CUCM 11.0 onwards, you can **enable or disable TLS tracing for services**. Currently, Tomcat is the only supported service. Use the CLI commands to view the reasons of connection failure of TLS connections to Cisco Unified Communications Manager.

To have strong encryption, a robust source of entropy is required. Entropy is a measure of randomness of data and helps in determining the minimum threshold for common criteria requirements. Data conversion techniques, such as cryptography and encryption, rely on a good source of entropy for their effectiveness. If a strong encryption algorithm, such as ECDSA, uses a weak source of entropy, the encryption can be easily broken. In CUCM 11.0, the **entropy source for Cisco Unified Communications Manager is improved**. Entropy Monitoring Daemon is a built-in feature that does not require configuration. However, you can turn it off through the Cisco Unified Communications Manager CLI.

For secure configuration download, Cisco Unified Communications Manager Release 11.0 is enhanced to **support HTTPS** in addition to the HTTP and TFTP interfaces that were used in the earlier releases. Both client and server use mutual authentication, if required. Clients that are enrolled with ECDSA LSCs and Encrypted TFTP configurations are required to present their LSC. The HTTPS interface uses both the CallManager and the CallManager-ECDSA certificates as the server certificates.

For Release 11.0(1) of CUCM, the following **Quality of Service (QoS) updates** were made:

• **Quality of Service (QoS) with APIC-EM Controller**. As of Release 11.0(1), you can now assign an APIC-EM Controller to dynamically manage network traffic and set the priority for specific media packet types in order to relieve congested networks and ensure QoS.

• **Custom QoS Settings for Users**. DSCP configuration has been enhanced for Release 11.0(1). In previous releases, DSCP settings for the users in your network were configured using service parameters, and the same settings were applied to all users in the network. With Release 11.0(1), you can now customize DSCP settings within a SIP Profile and then associate that SIP profile to a device. You can also configure separate port ranges for the audio and video streams in order to dedicate ports to one media type and simplify network bandwidth management.

• **Call Admission Control Enhancement** for Audio Portion of Video Calls, In Release 11.0(1), the Call Admission Control (CAC) feature has been enhanced for video calls. For video calls, CAC can now be configured to split the bandwidth deductions for the audio stream and the video stream into separate pools. If this feature is configured, the bandwidth that is required for the IP/UDP network overhead is also deducted from the audio pool.

**Cisco Unity Connection 11.0(1)**

**Summary Notification** feature allows the end user to receive summary notifications of your voice messages in email. An administrator has the option of customizing the notifications templates using the number of options provided. For example, specifying the number of message count to be provided in summary, customizing the subject of the email, setting up the time stamp. The settings for the summary notification can be done from Cisco Personal Communications Assistant as well as Cisco Unity Connection Administration.

**Missed call Alert feature** allows the end user to receive the missed call alerts on email. This is a feature that had been in Lync, so to see it added to CUC is a nice touch. The user has the option of either getting the missed call with summary notifications or receiving only the missed call alerts.

**Next Generation Security over SIP interface** provides high confidentiality, integrity, and message authentication through cryptographic algorithms. Next Generation Encryption is more secure as it restricts SIP interface to use Suite B ciphers based on TLS 1.2, SHA-2 and AES256 protocols. In addition to ciphers, Next Generation Encryption also includes third party certificates that must be uploaded on both Unity Connection and Cisco Unified CM. During the communication between Unity Connection and Cisco Unified CM, both ciphers and third party certificates are verified at both the ends. For environments that have stringent security requirements, this is critical.

The **System Restore Tool** is a new tool introduced in Unity Connection that allows the administrator to take either manual backup or schedule backup at specified intervals of time. The tool creates restore points that the administrator can use to restore data. For example, if the database is corrupted, the data can be restored using restore points.

With CUC 11.0(1), **video greetings** are now supported with call handlers also. This requires Cisco MediaSense server. Allowing businesses the ability to greet business partners and customers with a Video Call Handler is a differentiator. Combining this type of technology with Jabber Guest for example, opens up a whole new avenue for customer and business partner interactions.

You can now configure the **subject line format** for the notifications sent through emails. You can customize the subject line format for Message Notification, Missed Call Notification, and Schedule Summary notifications.

Last, but not least, Cisco Unity Connection now has the same **license violation behavior** as CUCM. In the past, when a license violation occurred on CUC, the system became inoperable, and would not take any new calls. Now, like CUCM, the system will maintain operation, it will simply not allow any further provisioning to occur. This is vital, because licensing issues happen, and you should not be put in a situation where your system is down as a result.

In summary, there are indeed a lot of new enhancements and features with 11.0. Whether you decide these are worth it in your environment is up to you. As always, if you need help with a Cisco UC upgrade, reach out to Byteworks for the technical expertise to do it right the first time.