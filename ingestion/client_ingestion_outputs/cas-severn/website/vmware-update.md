---
source: "website"
content_type: "blogs_resources"
url: "https://cassevern.com/vmware-update/"
title: "VMware / Broadcom—Significant Update Affecting All VMware Clients"
domain: "cassevern.com"
path: "/vmware-update/"
scraped_time: "2025-09-07T07:07:27.876599"
url_depth: 1
word_count: 1057
client_name: "cas-severn"
---

by Mark Belluz | Dec 21, 2023

Categories: cloud security, Cybersecurity Solutions, data protection, network security, News

Every week since the Broadcom acquisition of VMware there has been considerable news, like:

* Week 1 – RIFs and resizing of workforce in Week 1
* Week 2 – Move from Outlook/Zoom VMware-based emails and collaboration to Google, in only a couple days (mad respect)
* Last week – Announcement by Hock Tan on last week’s earnings call that Horizon/EUC and Carbon Black are up for sale

This week is no different – however, this announcement affects EVERY SINGLE VMware client. Total respect for the velocity at which this acquisition and integration are happening. Hock Tan is a legend and absolutely getting it done, ripping off the bandaid, making hard decisions, and implementing with velocity. So what’s up this week?

**TL/DR: going forward there are only two products available from VMware for enterprise-level VMware deployments**, which are provided at fantastic prices vs. the previous a la carte model, with significant benefits to all clients but also massive impacts to data center architectures (most notably Storage, but also Networks). Winners here will be customers, Broadcom, Nutanix, Azure, and AWS.

**SO WHAT HAPPENED?**

If you’re a typical client of CAS, you run vSphere Enterprise Plus. It’s the industry standard in enterprise virtualization. Last Monday I learned that this product no longer exists as a standalone SKU. However, it wasn’t until this week that I fully realized the implications as I started to analyze actual customer renewal scenarios.

So first things first – two major changes: vSphere is now no longer a standalone product. You either buy vSphere Foundation (which includes the products below) or the full software-defined data center, VMware Cloud Foundation (VCF). It’s now available as a CORE-based SUBSCRIPTION only (vs. the socket/processor-based perpetual model).

**VMware Cloud Foundation**
- vSphere (includes TKG, vCenter)
- vSAN (1 TiB / core)
- NSX Networking / HCX / AON
- Aria Suite Enterprise
- SDDC Manager
- Select Support and SRE

**vSphere Foundation**
- vSphere (includes TKG, vCenter)
- vSAN (100 GiB / core)
- Aria Suite Standard

Let me preface the rest of my analysis by saying I believe everything I’m sharing is public and was received via channel updates and by working on in-flight customer transactions. We are a 20+ year VAR of their products with extensive knowledge of their license models. We love VMware, use it every day, and I am trying to provide unbiased advice and analysis here. CAVEAT – the situation is evolving, and I have incomplete info as new details are coming out by the day. I’ve done my best to make informed assumptions. Feel free to correct me or provide your opinions on the subject.

**SO WHAT DOES THIS MEAN?**

I’ve dealt with two types of customers – naked vSphere ENT+/vCenter shops and vSphere ENT+/vCenter plus other product (i.e., VSAN, NSX, vRealize/Aria) shops. If you fall outside these, where vSphere Standard or Essentials is where you run your business – those still exist, you’re fine, everything is fine.

**I am one of the 99% of the enterprise IT market, and run vSphere Enterprise Plus. DO I HAVE A CHOICE?**

Not to my knowledge. The old SKUs are no longer available effective in a few weeks, including from OEMs such as Dell, HPE, or Lenovo.

I think clients have 3 immediate choices when their renewal comes due:
1. Buy vSphere Foundation or VMware Cloud Foundation subscriptions;
2. Downgrade to vSphere Standard, eliminating the H/A capabilities that are table stakes in the enterprise; or
3. Migrate hypervisors or to the Cloud.

Option 1 is where I’m doing a ton of analysis right now, more info below. Option 2 is not viable for most of my clients.

Option 3 – TL/DR on that: On-prem, there are only two enterprise-class alternatives in my opinion – Nutanix’s Acropolis HyperVisor (AHV) and Microsoft’s Hyper-V. For cloud, 99% of our clients will go either AWS or Azure. We have done countless migrations between these options (on-prem between hypervisors, and to/from cloud) and as a result, we’re Nutanix’s 2023 SLED Partner of the Year, an Azure Gold Partner, and an AWS Select Partner.

**THE MORE LIKELY OUTCOME – PROCEEDING WITH A RENEWAL UNDER THE NEW MODEL.**

While we are happy to advise you on migration plans, since most clients need to pull the trigger on their renewal in the next 1-12 months, I personally believe 90%+ of our clients will proceed with a purchase under this new model. Broadcom’s prices for the amount of software you are getting are truly fantastic and lock you into a new 3-year Broadcom agreement ensuring no increase in pricing in the near term.

Proceeding with the new license model can either:
1. Buy you time to fully embrace the new VMware and its associated technologies, including software-defined storage and networking; or
2. Buy you time to create a comprehensive migration plan so in 3 years you have moved to your new destination.

Keep in mind – **vSAN is included in EVERY RENEWAL.** Getting ahead of this can save you on any planned storage investments over the next 12-24 months. As everyone who has analyzed a storage Bill of Materials knows, the most expensive part of a storage purchase is the storage software (it’s been that way for 10+ years), not the hardware. You’re now getting some portion of that as a vSphere ENT+ client, no matter what.

**IS THAT GOOD NEWS? IS THERE OTHER GOOD NEWS? YES. YOU MAY SAVE A TON OF MONEY.**

So… I am 50-60% done with our first actual client analysis, for a vSphere ENT+ client that also runs NSX, Aria/vRealize, and some other VMware products, and it looks like _the new Broadcom model is GOING TO SAVE THEM A TON OF MONEY._ Like – a MASSIVE AMOUNT. Back of the napkin, I’m estimating 20-30% less for their VMware ELA, for 2X the software. This software can then reduce their storage costs substantially. Total Estimated ROI: $200K on VMware, plus $500K-$1M in additional storage and value-oriented savings over the next 3 years…

Want the details and more analysis? We are analyzing 5 actual client scenarios now. Assuming I don’t get barred from posting more on this subject, stay tuned, and I will be doing subsequent articles and LinkedIn posts on each customer we analyze.