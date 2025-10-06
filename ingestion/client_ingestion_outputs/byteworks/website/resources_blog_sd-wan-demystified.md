---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/sd-wan-demystified/"
title: "SD-WAN Demystified"
domain: "www.byteworks.com"
path: "/resources/blog/sd-wan-demystified/"
scraped_time: "2025-10-05T02:01:16.744352"
url_depth: 3
word_count: 1569
client_name: "byteworks"
---

# SD-WAN Demystified

#### **What is SD-WAN**

In essence, a software defined wide area network, or SD-WAN, involves two or more transports (WAN links) with a software controller to continually monitor the health of the available transports to make real-time and dynamic decisions as to which path certain classes of traffic will take. SD-WAN technologies began emerging around 2014 but did not reach “mass adoption” status until 2019.

Technically, a SD-WAN solution doesn’t require more than one WAN transport, but its usefulness is quite limited if there are not multiple paths for the software controller to choose from. In rare cases where a single transport is used, that’s generally because the site is not considered as important yet it participates within the SD-WAN “cloud” (overlay) for the purposes of simplified and standardized administration. But even if using a single primary transport for such a site, it is generally very cost effective to add a 4G/LTE cellular data transport as a backup link for basic connectivity should the primary circuit go down.

Traditionally, organizations with multiple locations would interconnect the local area networks in each location into a wide area network using technologies such as MPLS, VPLS, private lines, IPSec VPN tunnels across public internet links and – if you go far enough back in time – Frame Relay or ATM. MPLS eventually pulled ahead as the prominent private WAN solution because it allowed carriers to offer end-to-end quality of service (QoS) guarantees to accommodate the rapid emergence of IP-based voice and video technologies. MPLS is, however, expensive.

Using IPSec tunnels across public internet links is a much cheaper alternative to MPLS simply because the price-per-megabit of an internet circuit is substantially less than that of MPLS – and that’s logical because internet service is “best effort” and the carrier does not have to build a network as robust as one that guarantees bandwidth and QoS as does MPLS. This means, though, that using the public internet – where the traffic may transit multiple peering points (often choke points for traffic) across multiple autonomous systems (carrier backbones) – is giving up any control of how that traffic is treated along the way, which is less than ideal for real-time voice and video traffic. Traditional IPSec tunnels are also notoriously difficult to administer at scale as they require configuring tunnels between the hub and each spoke site, at a minimum or, double the number of tunnels for adding a redundant hub or, for full mesh: Tn = (N(N – 1))/2 – which means 45 tunnels (!!!) for just 10 sites. Later solutions such as Cisco’s DMVPN did help this scalability issue dramatically by combining the technologies mGRE, IPSec, and NHRP, however this still involved sending traffic across the tunnel and hoping for the best.

#### **Enter SD-WAN**

While there are as many SD-WAN products out there as there are brands of shampoo, many of them offer at least a core set of common capabilities, with more unique capabilities and management interfaces being the differentiators for evaluation. In general, a good SD-WAN solution will support a wide variety of underlying transports (MPLS, broadband internet, DIA, LTE, etc.) and then continually probe those paths for reliability (packet loss, latency, jitter, utilization), automatically establishing and tearing down tunnels in either a full mesh or forced hub-and-spoke topology, and enforcing defined policies for how certain classes of traffic are handled.

The ability to define and enforce traffic policies is perhaps the most important aspect of SD-WAN for migrating away from a traditional WAN. Simply put, each organization has certain types of traffic which are more important to it operating successfully and efficiently than other types of traffic. This is commonly voice and video for organizations where IP telephony and conferencing are in use, but it could also include applications such as intranet sites, access to file servers, ERP software, Citrix desktops, etc. Whatever those applications are, the organization can generally determine which ones are more important than the others, which are generally all more important than miscellaneous internet traffic, and then define policies that translate those organizational requirements into actual traffic policies. The SD-WAN solution then has the job of monitoring and managing resources to ensure that it makes the best use of its underlying transports in order to fulfil those policy definitions.

For example, a SD-WAN environment with an MPLS transport and a broadband internet transport would likely prefer the MPLS path for sending voice and video because of the inherent reliability and QoS controls while sending file server traffic across a tunnel over the broadband internet path because it likely has much greater bandwidth since it’s cheaper per megabit. However, because the SD-WAN controller is continually monitoring both paths, should the MPLS path become degraded it may temporarily move that voice/video traffic over to the broadband internet path (while also potentially constraining file transfer traffic to give priority to the voice/video traffic) until the MPLS path has returned to stability. Conversely, should the broadband internet path be degraded the controller may swing non-business-critical traffic over to the MPLS path, but given a much lower priority than other business-critical traffic on that link.

It’s becoming increasingly common for a SD-WAN solution to displace MPLS entirely because 1) commercial internet connectivity continues to become more reliable and, 2) having available multiple diverse broadband or DIA circuits helps “play the odds” that, while a path may be degraded from time to time, the probability that multiple paths are degraded simultaneously is much lower. Therefore if the locations have available, for example, fiber internet and broadband coax (cable) internet – each from different carriers – you could expect a high degree of reliability for connectivity given that those paths share very little in common in terms of physical media, service type, and carrier infrastructure.

#### **Do I still need MPLS?**

Maybe. As mentioned above, some organizations prefer to “play the odds” by incorporating multiple diverse public internet carriers where available. At the same time, the public internet is still no substitute for the absolute end-to-end traffic controls of MPLS. At a minimum, organizations that identify that they still prefer the guarantees of MPLS are often able to still save costs by reducing their MPLS circuit bandwidth to bare minimum levels and incorporating fast and relatively cheap internet to provide substantially greater bandwidth across the WAN during normal operations.

The math is simple. If you have two diverse internet transports and each has, for example, 98% reliability, when you multiply the probability of an outage (2%) of a circuit with the probability of an outage (2%) of the other, the probability of having both paths unavailable simultaneously (short of a cataclysmic event like a natural disaster) is 0.04%. The more diverse transports you add (i.e., LTE) the lower this probability becomes, and most common SD-WAN solutions will support three or more transports.

#### **Not all SD-WAN solutions are created the same.**

Alright, so you start researching which SD-WAN solution is right and quickly determine there are perhaps hundreds of options. Here are some pointers to begin to think about narrowing the field:

*   **Does the solution meet the organization’s requirements?** First and foremost, determine if the SD-WAN offering meets the needs of the organization. Have stakeholders discuss what is important and create a list of requirements. Use the scorecard method to weight the requirements and compare against the evaluated offerings.

*   **Is the solution organically built or was it “bolted on” to an existing solution?** While a “bolted on” SD-WAN function to a solution isn’t necessarily a deal breaker, this often results in a clunky implementation as the capability had to work within the codebase and constraints of the repurposed platform.

*   **Does the manufacturer have staying power?** With so many SD-WAN offerings on the market you can be confident that most will not survive and will simply go out of business or be acquired and absorbed into another company’s solution. You do not want to be left holding the bag with a hardware/software solution that will no longer be around in a few years.

*   **What is the complexity of administration?** Some solutions will deliberately simplify the administrative interface which therefore limits overall configurability and customization. If the organization requires fine-tuned policies and functionality then a simplified solution probably does not have the flexibility that is required. Conversely, if the needs of the organization are simple and there is not a solid skillset within the IT staff, having this simplicity and these constraints may be desirable.

*   **What are the upfront and recurring costs?** Is the solution sold as hardware plus licensing plus maintenance? Purely monthly recurring costs? If bandwidth for an underlying transport is upgraded will it require new hardware?

#### **What do you recommend?**

At Byteworks, we pride ourselves on not making recommendations in a vacuum. It is critical to understand factors such as business requirements, the existing WAN, applications, bandwidth, budgets, administrative requirements, etc., prior to suggesting any particular solution. The advantage that we have is that we get to work with a wide variety of SD-WAN solutions on any given day and therefore know, in a practical manner, what works well, what does not, and the benefits one platform may have over another in a particular environment. Feel free to reach out to us if you would like assistance understanding these differences and determining what would work best with your set of requirements.