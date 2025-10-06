---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/why-globalized-e-164-dial-plans-for-your-cisco-uc-environment/"
title: "Globalized E.164 Dial Plans for Cisco UC Environment"
domain: "www.byteworks.com"
path: "/resources/blog/why-globalized-e-164-dial-plans-for-your-cisco-uc-environment/"
scraped_time: "2025-10-05T02:02:34.047274"
url_depth: 3
word_count: 1154
client_name: "byteworks"
---

# Why Globalized E.164 Dial Plans for your Cisco UC Environment?

Talking to a client recently, the discussion around proper dial plan design came up, as it often does of course. There is we believe, a misconception that a “Globalized” dial plan design is something only larger enterprises with numerous locations, specifically, international ones should actually deploy. For smaller clients, particularly in the SMB space, abbreviated, traditional dial plans are still very popular and viewed as easier to manage and deploy. By “Globalized” dial plans, we are referring to “E.164” specification.

**E.164** is an ITU-T recommendation, titled _The international public telecommunication numbering plan_, that defines a numbering plan for the worldwide public switched telephone network (PSTN).

To simplify it, let’s say you have a DID (Direct Inward Dialed) phone number of 770-555-1234. The E.164 format of this number is +17705551234 (1 is the Country Code for the US). If we were in the United Kingdom, and your local number is “01632-960493”, the “Globalized” or E.164 version would be +441632960493, because the country code for UK is 44. The format is always the “+” character followed by the country code and the rest of the country-specific format, omitting any local dialing rules or digits.

In the US, we may live in an area where local calls are still 7 digits, although that is getting more and more rare. In this area though we may have to add 1 plus an area code to our dialing rules depending on how far away we are calling to. One of the designed advantages of dialing with a “globalized” format is so you have confidence that the format of the number will work regardless of where the call is placed from.

Of course when we use phones at home, or even our cell phones, we typically dial based on the dialing rules for the area in which we live. If I live in Atlanta, and I’m calling a local friend, I dial the 10 digits. If I’m calling New York, I add a 1. If I’m calling London, I change it up and have to dial 011 plus the country code, etc. It’s the magic of the equipment of the phone companies, that “translate” the numbers based on where we are calling from, to where we are calling to, and “converts” it into the “Globalized” numbering plan under the hood, so to speak. After all, most phones don’t have the “+” character to add to your dialing as a prefix.

Now, in the work place, what’s traditionally been setup is an “on-net” extension based dial plan design. Some employee phones will just have an “internal” extension that is 4 digits long. Other employees dial those 4 digits to call each other. If employees are calling between sites, often they call a site number, followed by the internal extension, depending on how large the company is. If a customer is calling, they may call a main line, or a direct outside number that rings into the appropriate internal extension.

In the better designs, the outside number will often match the internal extension, either fully or partially. For example, maybe the PSTN DID is 770-555-1234, and the internal extension is 1234. If I want to reach this employee as a customer, I dial the outside PSTN DID number, if I am a fellow employee, I simply dial “1234”. If I’m the employee though, and I want to call outside the company, I typically dial an external access code, (9 in most places), followed by the normal “localized” dialing rule for the area from which I’m placing the call. These are just a few examples.

To get back to the point here, for our clients supporting these systems, and our engineers who support these systems, regardless of the size of your company, we at Byteworks recommend an E.164 “Globalized” dial plan design, as it simply helps with so much from an administrative and usability standpoint. You no longer need to be a huge enterprise with numerous sites to realize these benefits either.

Whether you are supporting a phone system with 30 users, or 30,000 users, this clean design approach makes the upkeep and administration of not just the dial plan design, but the system as a whole, much better. And if you do have a cloud based system, using an E.164 dial plan design is also recommended. Although this blog focuses on the benefits for on-premise Cisco systems, we recommend this design for any IP Telephony system, regardless of manufacturer or hosting status.

So, using our previous example scenario client, the employee who’s extension was “1234” in the phone system, with a “globalized” approach, we would change the “extension” to be “+17705551234”. This would be the employee’s “full extension” that would be programmed. In a Cisco Unified Communications Manager (CUCM/BE6K/BE7K) environment, this is the “Directory Number” configuration.

The entire routing in the system would all be configured to route based on E.164 patterns. The “Calling” and “Called” numbers would be translated to this format (if not sent from the PSTN in that format already) on ingress, and then all routing within the Cisco UC systems, from Call Manager, Unity Connection Voicemail, Unified Contact Center Express, Emergency Responder, whatever the voice application, the routing internally would all be based off of this format.

All egress calling to other systems and to the PSTN, would also be sent in this format. Please note that this does not mean other employees still can’t use “abbreviated” dialing to reach their fellow employees. E.164 can be implemented, and still allow traditional “shortened” on-net dialing, i.e. dialing only 4 digits to reach colleagues. Any “localized” dialing rules and formats for caller-id, etc., could still be met while deploying an E.164 design.

This approach, immediately decreases the amount of ANI (Calling Number) and DNIS (Dialed Number) manipulation, thus the complexity of both the transfer and troubleshooting of all call flows in and out of the systems. When combined with SIP PSTN services that send and receive in this format, it provides further enhancements and failover capabilities in addition to the following:

* +E.164 directory numbers are unique by definition.
* +E.164 directory numbers enable one dialing habit (+E.164) directly without requiring any further dial plan configuration.
* +E.164 directory numbers simplify the implementation of forced on-net routing.
* Configuration of Automated Alternate Routing (AAR) is greatly simplified. There is no need to provision multiple AAR groups and AAR PSTN prefixes because the target on-net destination can be used directly as an alternate PSTN address; it is a +E.164 number.
* Correct caller ID is automatically achieved for all call flows (direct, forwarded, on-net, and off-net).
* Ingress and Egress failover are more easily achieved, and advanced features more easily enabled, once compliant.

If you’d like to learn more about this and how our Byteworks Collaboration Engineers can help support and maintain your IP Telephony environment, please email us: solutions@byteworks.com