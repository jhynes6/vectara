---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/layer-2-extensibility-options-for-business-networks/"
title: "Layer 2 Extensibility options for Business networks"
domain: "www.byteworks.com"
path: "/resources/blog/layer-2-extensibility-options-for-business-networks/"
scraped_time: "2025-10-05T02:00:35.803231"
url_depth: 3
word_count: 842
client_name: "byteworks"
---

# Layer 2 Extensibility options for Business networks

There have been many advancements in networking technology to allow the extension of Business Networks between multiple locations, allowing customers and employees at Satellite or Home offices to access the same resources as if they were plugged in at Corporate headquarters. These range from a simple “dial-up” Virtual Private Network (VPN) connection, to private circuits such as T1 and Fiber.

Most of these connections have always operated at Layer 3 (L3) of the OSI network model, which basically simulates a connection via Router. In recent years, however, there has been a growing requirement to extend links at Layer 2, which allows broadcast traffic such as Bonjour to be forwarded between sites. Depending on your inter-site connection medium, different technologies are utilized.

## Virtual Private LAN Service (VPLS)

For those that are familiar with Multi-Protocol Label Switching (MPLS) networks, you will know that MPLS links technically operate in-between layers 2 and 3 (MPLS label headers are placed between layer 2 and layer 3 headers), however their operation more resembles a Layer 3 link in practice. This type of link works well for standard data transfer, however it falls short for broadcast-based protocols and services.

If an extension of a Layer 2 circuit or VLAN, many providers offer an MPLS-like system called Virtual Private LAN Services, or VPLS. They allow for a one-to-one (bridge) or one-to-many (switch) layer 2 link between sites. This way, broadcasts can be forwarded over WAN links.

These links can be configured as a single vlan, or as a trunk, to forward multiple vlans (similar to Q-in-Q), allowing you to bridge all of your corporate VLANs between sites, and even to home-office users, if needed. Since VPLS links are maintained in the provider cloud, no additional configuration is required on customer equipment.

## Cisco Xconnect

VPLS circuits can be costly, due to the high-bandwidth used in layer 2 broadcasts. Cisco has developed a protocol that may be suitable or a lower-cost scenario, called Xconnect. Xconnect allows for a one-to-one Layer 2 bridge over a static L2TP tunnel. Like VPLS, these tunnels can forward a single VLAN, or a trunk of multiple VLANS. Unlike VPLS, however, there is no one-to-many solution, and each connection requires the use of a hardware port for the encapsulation process. In the event multiple xconnect sessions are needed, such as a hub-and-spoke topology, one physical port is needed for each xconnect session.

Since Xconnect sessions do not reply on a provider, the configuration of each circuit is done on the corporate routers at each location, and each router needs to be operating an xconnect-compatible IOS. There are several configuration options available depending on specific needs of the link.

### Configuration

As stated previously, Xconnect session needs two physical interfaces to create a successful bridge link; A layer 2 inside interface that is connected to the vlan or trunk from a switch, and a layer 3 outside interface used to create the L2TP connection. In some instances, such as a router with an NME module, the backside virtual interface can be used in lieu of a physical interface for the xconnect inside.

In order to create the xconnect session, a pseudo-wire instance needs to be configured. Optionally, an l2tp policy class can be created to globally-define l2tp settings.

```plaintext
! Layer 2 Tunneling Protocol configuration
!
l2tp-class _[l2tp-class-name]_
authentication
password 0 _[l2tp-authentication-password]_
!! Pseudo-wire configuration
!
pseudowire-class _[pseudowire-class-name]_
encapsulation l2tpv3
protocol l2tpv3 _[l2tp-class-name]_ ! Optional
ip local interface _[physical-outside-interface-name]_
```

Once these options are configured, you can configure the xconnect session on the inside interface. This is typically done on the interface facing your layer 2 switch or network module, and the interface needs to be operating in Layer 2, or switchport mode.

Below is a standard configuration on a single layer 2 interface (or layer 3 interface connected to an access port).

```plaintext
! Xconnect session
!
interface _[layer2-internal-interface]_ description ** Single VLAN on physical interface
xconnect _[ip-address] [session-id]_ encapsulation l2tpv3 pw-class _[class-name]_  
```

Xconnect can also be configured on subinterfaces, in order to allow for individual vlans in a trunk to be bridged. If xconnect is configured on a physical interface, that interface, nor any sub interface of it, can have layer 3 configuration such as IP addresses applied.

In order to bridge a trunk, the xconnect configuration must be configured on a trunked interface that does not act as the layer 3 endpoint (no IP addresses), or a single xconnect session must be created on each xconnect subinterface.

```plaintext
! Xconnect session
!
interface _[layer2-internal-interface]_ description ** Single VLAN on subinterface
encapsulation dot1q _[vlan-id]_
xconnect _[ip-address] [session-id]_ encapsulation l2tpv3 pw-class _[class-name]_  
```

Xconnect sessions must utilize the same interface type on each end (primary interface vs subinterface), otherwise IOS will record a “Payload type mismatch” error. Other information useful for troubleshooting Xconnect sessions may be found in the following debug commands. Please note that the availability of some of these commands may vary based on IOS version.

```
debug xconnect error
debug xconnect event [detail]
```