---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/cisco-collaboration-endpoint-8-2-on-dx/"
title: "Cisco Collaboration Endpoint 8.2 on DX"
domain: "www.byteworks.com"
path: "/resources/blog/cisco-collaboration-endpoint-8-2-on-dx/"
scraped_time: "2025-10-05T02:00:24.083678"
url_depth: 3
word_count: 974
client_name: "byteworks"
---

# Cisco Collaboration Endpoint 8.2 on DX

The much-anticipated Cisco Collaboration Endpoint 8.2.1 software for DX 80 and DX 70 devices is now available (as of 7/8), and after a couple of consistent weeks of testing, we wanted to write up some quick feedback. Quick recap: The Cisco TelePresence DX line until now, used Android-based software that has been, to say the least, a bit unstable. The primary issues our customers have reported include random reboots, phone call freezes, freezing during screen-share, and all sorts of video and display issues when connected as an extra monitor. The Android-based software is cool, and robust with all that it can do, yet when compared to the “tc” line of code used on Cisco’s other video codecs (SX, EX, MX, etc) and now the new CE code on the newer devices, it was noticeably less stable and an overall different user experience. This made it quite difficult at times during TelePresence system roll-outs, and the confusion it could cause end-users due to different user interfaces and experiences. Now, to Cisco’s credit, they have done a lot to try and address this on the Android based code, releasing updates frequently and allowing the phones to run in a “basic” mode which locked down a lot of extra features and did help a lot. That being said, it was way past time that the same code and features be consistent across all Cisco TelePresence Endpoints.

Let’s start with what you lose when you switch from the Android DX software to the new CE software:

* Wireless Network (Wifi)
* Bluetooth Headset
* 3rd Party App Installation
* Keyboard Control, Keyboard and Mouse Redirect
* Voicemail, Extension Mobility, Transferring of calls, Call Forwarding and Shared Lines

Now, again, this is not a list of features you gain, these are what you lose! No call transferring? No BT Headsets? No Shared lines or Call forwarding or Extension Mobility? We could understand some of these, but a lot of these seem like pretty basic features. Oh well, surely updates will be forthcoming, so let us now focus on the positives: The platform is very stable. While it does not do a lot, what it does it performs very well doing, and without the reboots, and freezes, and all the random crazy behavior. The UI is consistent with what you now see on the other CE compatible endpoints, and it is quick and responsive. Here is what you can do:

* Make and receive HD voice and HD video calls
* Dial into other Video Codecs and bridges
* Seamless PC Integration
* Use and Monitor and easily share content in meetings
* Conference in participants (requires UC system bridging resources)
* Place calls on hold

A couple of issues that we have run into: There is a constant warning on the screen stating: “Security risk System passphrase not set”. Normally, this is an easy fix, we would simply login via web to the IP address of the codec itself and add a password, except when we try this since we changed from Android DX code to the CE code, we cannot get to the codec via the web. Pretty big issue actually, if you want to run this device in prime time. As a workaround, we even tried to set the “admin” password on the device configuration page in CUCM, but this has no effect. Admittedly, so far testing has been remotely through a Meraki Z1, but we have never had this issue before, and we can get to the web page of other IP phones and codecs connected through the same remote network. More testing will be coming, but as of right now, we have been unable to successfully reach the web login for the DX80 codec running CE 8.2.1, we either reach a completely empty web page, or sometimes it returns this error: “Internal Error: Missing Template ERR_CONNECT_FAIL”. The next item we noticed is that Proximity would not work. We assumed, incorrectly, that this feature was included on the DX series, but it is not included. The release notes confirm this.

The process of converting from the Android DX software to the CE software was a bit complex. The process goes like this:

1. Make sure Android based DX device is registered to CUCM, and running at least Android version 10.2.5.207, if not, the firmware must first be upgraded to this version
2. Install these two cop files on all nodes in CUCM cluster:
    1. Latest Device Pack that matches your environment’s version of CUCM, in our test environment it was: cmterm-devicepack11.0.1.22049-2.cop.sgn
    2. cmterm-synergy-ce8_2_1_no_defaults.cop.sgn
3. Restart TFTP services
4. Change “Phone Load Name” field on the “Device Configuration” page of the DX device you want to convert, to the phone load name for CE, for example: “sipdx80.ce821.rel.loads”. Click save and apply the config.
5. The device will upgrade for the first time to CE software, it takes about 15-20 minutes. It will reboot twice. DO NOT tap “Get Started” on the _Welcome Screen_ when the software is installed. See next steps first.
6. Delete the original “Cisco DX 80” or “Cisco DX 70” Device Type in CUCM, and add them as a new “Cisco TelePresence DX80 or Cisco TelePresence DX70” Device Type.
7. Now you can go back to the DX Screen and press “Get Started” on the _Welcome Screen._
8. If using DHCP with Option 150 still, the device will find CUCM and you simply press “Activate”.

To reverse the process and go back to the Android code, you must install the COP file to do so from Cisco.com, and reverse the process by changing the phone load name on the new device, letting it change version, and then when on start screen you delete it and re-add in CUCM as a “Cisco DX 80” or 70 device type.