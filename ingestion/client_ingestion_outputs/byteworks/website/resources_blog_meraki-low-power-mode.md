---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/meraki-low-power-mode/"
title: "Meraki – Low Power Mode"
domain: "www.byteworks.com"
path: "/resources/blog/meraki-low-power-mode/"
scraped_time: "2025-10-05T02:00:08.860080"
url_depth: 3
word_count: 465
client_name: "byteworks"
---

# Meraki – “Low Power Mode”

As the Meraki product line gets more engrained into enterprise networks its going to touch Cisco switching that uses the proprietary CDP (Cisco Discovery Protocol) layer 2 broadcast identification protocol. CDP is very useful when trying to identify what device is plugged in where. CDP has an industry counterpart, called LLDP (Link Layer Discovery Protocol). These protocols basically do the same thing, only one is made for everyone and the other is specific to Cisco only. Meraki, having been acquired by Cisco back in 2012 is still integrating their software/hardware into the Cisco space so they still primarily use LLDP for their discovery protocol of choice.

Meraki uses LLDP to tell the connecting POE switch how much power it needs in order to operate. If the connecting switch does not talk LLDP, then it defaults to the original POE standard of 15.4 watts. Thats exactly what is happening when you plug a Meraki AP into a Cisco POE switch. Most Meraki AP’s require about 22.4 watts or so of power to operate. Since the wattage is above 15.4 watts, POE+ is required to take advantage of all of Meraki’s features. To get this to work, simply go into the Cisco switch, enable LLDP and add a few commands to the port, reboot the AP and you should be good to go!

First, check to see if the AP’s are in fact being provided with 15.4 watts. In the Meraki Dashboard you will see that the AP’s are in “Low Power” mode:

Now log into your switch and see if the switch is only granting 15.4 watts to the AP:

To enable LLDP globally on a switch running Cisco IOS:

```
Switch# configure terminal  
Switch(config)# lldp run  
Switch(config)# end
```

Now enable LLDP on the specific interfaces where the MR34 APs will be connected. Follow the example below for Cisco IOS devices, substituting “Interface #” with the actual interface in question:

```
Switch# conf t  
Switch(config)# interface (Interface #)  
Switch(config-if)# lldp transmit  
Switch(config-if)# lldp receive  
Switch(config-if)# end
```

To renegotiate power, either reboot the AP in the Meraki Dashboard, or shutdown and then re-enable the port on the Cisco switch:

```
Switch# configure terminal  
Switch(config)# interface (Interface #)  
Switch(config)# shut  
Switch(config)# no shut  
Switch(config)# end
```

At this point, the switch and AP should be able to negotiate up to the required power level. If this is still not occurring, make sure the switch port is allowing up to 30W of power for the connected device:

```
Switch# configure terminal  
Switch(config)# interface (Interface #)  
Switch(config-if)# power inline max 30000  
Switch(config-if)# end
```

Lets see if the switch is now providing the right power to the AP’s:

You’re done! Remember to save changes on your switch and enjoy your Meraki solution!