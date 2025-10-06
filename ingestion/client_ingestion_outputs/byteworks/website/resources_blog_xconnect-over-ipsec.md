---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/xconnect-over-ipsec/"
title: "XConnect over IPSEC"
domain: "www.byteworks.com"
path: "/resources/blog/xconnect-over-ipsec/"
scraped_time: "2025-10-05T02:01:37.102619"
url_depth: 3
word_count: 364
client_name: "byteworks"
---

# XConnect over IPSEC

XConnect, or L2TPv3 is a great way to extend a layer 2 broadcast network over a WAN connection to another site. It works great when you need to do things like MDNS or AirPlay, or anything else that requires a broadcast style protocol to function.

With corporations and other entities, its apparent that encryption is a very important tool to ensure that communication over the open internet is secure to protect that confidential and proprietary information. L2TPv3 or Xconnect doesn’t help secure the traffic. So a solution needs to be addressed to encrypt the traffic. By simply creating a AES 256 bit encrypted VTI tunnel between the two endpoints and then executing an xconnect inside the tunnel this solves both requirements by only adding an additional 18 bytes of overhead per packet.

Here is an example configuration:

**Both Sites:**

```
l2tp-class xconnect-l2tp  
authentication  
password x0nn3ctvt1

pseudowire-class xconnect-pw  
encapsulation l2tpv3  
protocol l2tpv3 xconnect-l2tp  
ip local interface Tunnel1

crypto isakmp policy 10  
encr aes 256  
hash sha512  
authentication pre-share

crypto ipsec transform-set TSVTI esp-aes 256  
mode transport

crypto ipsec profile VTI  
set transform-set TSVTI
```

**Site 1:**

```
crypto isakmp key x0nn3ctvt! address 2.2.2.2 255.255.255.255

interface Tunnel1  
description Site 1 to Site 2 – VTI Tunnel  
ip address 10.100.101.1 255.255.255.252  
tunnel source 1.1.1.1  
tunnel mode ipsec ipv4  
tunnel destination 2.2.2.2  
tunnel protection ipsec profile VTI

interface FastEthernet0/1  
description // Data Interface (via xconnect to Site 2)  
no cdp enable  
xconnect 10.100.101.2 60 encapsulation l2tpv3 pw-class xconnect-pw
```

**Site 2:**

```
crypto isakmp key x0nn3ctvt! address 1.1.1.1 255.255.255.255

interface Tunnel1  
description Site 2 to Site 1 – VTI Tunnel  
ip address 10.100.101.2 255.255.255.252  
tunnel source 2.2.2.2  
tunnel mode ipsec ipv4  
tunnel destination 1.1.1.1  
tunnel protection ipsec profile VTI

interface FastEthernet0/1  
description // Data Interface (via xconnect to Site 1)  
no cdp enable  
xconnect 10.100.101.1 60 encapsulation l2tpv3 pw-class xconnect-pw
```

To make sure you are good to go, make sure your VTI tunnel shows UP/UP and your xconnect session(s) show UP/UP.

```
“sh int t1” – for VTI tunnel stats  
“sh cry isa sa” – ISAKMP Status  
“sh ipsec sa” – IPSEC Status  
“sh xconnect all” – xconnect status
```

Reference:  
https://www.cisco.com/c/en/us/td/docs/ios/12_0s/feature/guide/l2tpv325.html#wp1039063  
https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/WAN_and_MAN/IPSec_Over.html#wp1000115