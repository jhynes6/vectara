---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/calling-party-number-cpn-based-call-routing-using-cisco-unified-communications-manager-8-x-and-sip-gateway-protocol/"
title: "ANI-Based Call Routing in Cisco Unified Communications Manager using SIP"
domain: "www.byteworks.com"
path: "/resources/blog/calling-party-number-cpn-based-call-routing-using-cisco-unified-communications-manager-8-x-and-sip-gateway-protocol/"
scraped_time: "2025-10-05T02:02:01.955150"
url_depth: 3
word_count: 1471
client_name: "byteworks"
---

# ANI-Based Call Routing in Cisco Unified Communications Manager using SIP

Some clients will request that their IP telephony system have the capability to block inbound calls into their organization, or to route these calls to a specific destination, solely based on the “Caller-ID” being sent by the caller.  For example, if the Caller-ID or ANI (Automatic Number Identification) is that of a specific customer, then they may want to direct that call from that customer’s home number to a dedicated support representative, IVR, or Voice Message System.  Another scenario is maybe the caller is malicious, or keeps prank calling, so you may choose to simply reject the call, or send it to a specific pre-recorded message.

A client may also want to block marketing calls, recruitment calls, or any other call that is generally unwanted.  We’ve seen many blog postings covering the steps to do this, however you have to read many different ones to properly implement and understand this configuration end-to-end, and more specifically, how to implement this when you are using SIP for your interior gateway protocol.  This blog focuses on all of the needed steps, and specifically the extra steps required when configuring this when using SIP as your primary gateway protocol versus MGCP or H323.

In older versions of Cisco IP Telephony Systems, call-blocking based on ANI was typically accomplished by using Translation-Profiles on Cisco IOS Voice Gateways, or ISR’s or CUBE (Cisco Unified Border Element).

**Voice Translation Rule:**  
voice translation-rule 99  
rule 1 reject /^800.*/  
rule 2 reject /4049769999/  
rule 3 reject /7709769999/

**Voice Translation Profile:**  
voice translation-profile blacklist  
translate calling 99

**POTS Dial-Peer:**  
dial-peer voice 99 pots  
description Ingress From PSTN  
incoming called-number 678353….  
 call-block translation-profile incoming blacklist  
call-block disconnect-cause incoming call-reject  
direct-inward-dial  
port 0/0/1:23  
forward-digits 10

Here we have dial-peer 99 handling inbound calls from the PSTN and it is configured to check the call setup and match it against the configured translation-profile.

Translation rule 99 defines several patterns that should be rejected. Namely, any number that begins 800, calls from 4049769999, and calls from 7709769999.

This method is only applicable to SIP and H.323 configurations. It does not work with MGCP. Also, please note that there is a limit of 15 rules in a translation-rule set.

In Cisco Communications Manager 8.0 and above, Cisco added the “Route next Hop by Calling Party Number”, which is part of the [“hotline” feature](https://www.cisco.com/en/US/docs/voice_ip_comm/cucm/admin/8_0_1/ccmfeat/fshotline.pdf).

This “Route Next Hop by Calling Party Number” feature is a check box that now exists on translation profiles. The new parameter is used to instruct the CUCM to route the call using the configured calling search space, based on the Calling ANI, instead of the traditional method of routing based on the dialed DNIS. It can be used to ‘blacklist’ calls based on what number they are calling from. The following diagram is a run-through of how it works:

In the Previous diagram, the following occurs:

1. The call comes from the PSTN and hits the Cisco Voice Gateway (ISR/Router/CUBE).  
2. The router processes the call and relays the call to the CUCM cluster.  
3. The router is configured as a gateway or trunk in CUCM, using MGCP, SIP or H323 protocol. This gateway/trunk is assigned a inbound Calling Search Space of “PSTN-GW-IN-CSS”.  
4. The call uses this Calling Search Space to determine the Partitions to which it will try to send the call. The Partition assigned to the “PSTN-GW-IN-CSS” is the “PSTN-IN-PT” partition.

5. A Translation Pattern is configured using the “PSTN-IN-PT” and the pattern is “!” (Which catches any numeric value, and another translation pattern with a “<null>” (blank) pattern is configured which matches calls that are sent with no calling ANI. These 2 translation patterns have the checkbox checked for “Route Next Hop by Calling Party Number”. This then catches the calling ANI and uses it, combined with the CSS assigned at the Translation Profile to determine the partitions that are available to the call for the next leg of the call.

6. These translation patterns will then route the call to the next hop by using the CSS assigned, which is “PSTN-Screen-CSS”. Now the “PSTN-Screen-CSS” will also have identical translation patterns within their primary partition, just like the “PSTN-GW-IN-CSS” does, which will allow all ‘non-blocked’ ANI’s to ring in successfully. These patterns will look identical, except for the fact that “Route Next Hop by Calling Party Number” check box will not be selected. Here is the “Screening” CSS:

And then here are the identical patterns that allow all calls through:

These two patterns are designed to catch calls from the PSTN that use ANY numeric caller-id, which is what the “1” will catch… And then calls from the PSTN that may not have an ANI at all, which is what the second “NULL” (blank) translation pattern is for. The CSS these patterns point to would of course be the CSS that has access to all internal extensions, in this example, the “Phones-CSS”:

Now, the next step is to simply create the translation patterns for the ANI’s that you want to block. Now that all of the previous configuration is completed, adding future numbers for blacklisting or routing based on ANI becomes a simple step of creating a translation pattern in the “PSTN-Screen-PT” partition, and to block or route accordingly. The following illustrations show what these would look like for this sample configuration:

If you needed to make sure that calls from a specific number always route to a specific extension/hunt group/employee/auto attendant this becomes an easy task right through the translation pattern:

Now, if you have set up your gateway as MGCP or H323, your config should be pretty much golden at this point. With SIP however, an anonymous caller, or in other words, a caller who has an “unlisted”, “restricted” or “blocked” caller-id when calling inbound to your system would fail. The reason for this is that with SIP, the “From” header will contain either “anonymous” or “unavailable”, and since Cisco Unified Communications Manager’s digit analysis engine is not designed to match on non-numeric strings, the call would simply fail. There are profiles you could apply to replace the header fields with an actual “dummy” number is similar, but these get complicated and can quickly become an administrative burden. After opening a case with Cisco TAC on this issue, they pointed me to this script, written by a Cisco employee, but not technically supported by TAC. I can tell you, that I have tested this extensively and gotten it to work with no issues in multiple production environments. To create, you navigate within Cisco Unified Communications Manager to Device -> Device Settings -> SIP Normalization Script. Once there you can paste the following “LUA” script into the “Content” section:

To keep it simple, all you have to do do is change the ANI in the “ReplacementNumber” sections marked above to the one you desire (can be an unused, dummy number to just allow calls through).  
Here is the complete actual script, a lot of which is of course customizable to your environment/needs.

```lua
M={}

trace.disable()  

function M.inbound_INVITE(msg)  

   local replacementNumber = scriptParameters.getValue("6785559999")

   if replacementNumber == nil
   then
      replacementNumber = "sip\:6785559999"
   else
      replacementNumber = "sip\:" .. replacementNumber
   end
   trace.format("Replacement Number: %s", replacementNumber)

   local fields = { "From" , "Remote-Party-ID" }
   local numberOfFields = #fields 
   trace.format("Fields/Count: %s, %s, %s", fields[1], fields[2], numberOfFields)

   local x = 1
   while  x <= numberOfFields do 

      local header = msg:getHeader(fields[x])
      if header == nil
      then
         trace.format("Field %s not found", fields[x])
      else
         trace.format("Field %s: %s", fields[x], header)

         if string.find(string.lower(header), "sip\:anonymous")  
         then
            trace.format("Found string anonymous in %s", fields[x])
            trace.format("Header: %s %s", fields[x], string.lower(header))

           local newHeader = string.gsub(string.lower(header), "sip\:anonymous", replacementNumber) 
           trace.format("New %s Field: %s", fields[x], newHeader)

           msg:modifyHeader(fields[x], newHeader)    
         elseif string.find(string.lower(header), "sip\:unavailable")
         then
            trace.format("Found string unavailable in %s", fields[x])
            trace.format("Header: %s %s", fields[x], string.lower(header))

           local newHeader = string.gsub(string.lower(header), "sip\:unavailable", replacementNumber) 
           trace.format("New %s Field: %s", fields[x], newHeader)

           msg:modifyHeader(fields[x], newHeader)    
         else
            trace.format("Field %s number valid.  No change made.", fields[x])
         end
      end
      x = x+1
   end
end
return M
```

After creating and saving the SIP Normalization Script, you next need to apply it to the SIP Trunk from the PSTN within Cisco Unified Communications Manager. This section is on the SIP Trunk Device Configuration Page:

After the script is applied, all anonymous calls will now pass through. You can now easily route calls from anonymous callers by using another translation profile to catch the ANI you identified in the script, in this example “6785559999” using the methods previously described. You can block these globally, or allow them all through, or route them to a specific desired extension.

The end result of this configuration will give the administrator an easy to use, centralized, ability to administrate system-wide whitelist/blacklist based on calling ANI in their IP Telephony environment through Cisco Communications Manager while still using SIP protocol as your interior gateway protocol.