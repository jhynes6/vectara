---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/allow-or-block-anonymous-calls-into-cisco-communications-manager-lua-script-update/"
title: "Allow or Block Anonymous Calls Into Cisco Communications Manager LUA Script Update"
domain: "www.byteworks.com"
path: "/resources/blog/allow-or-block-anonymous-calls-into-cisco-communications-manager-lua-script-update/"
scraped_time: "2025-10-05T02:01:43.441050"
url_depth: 3
word_count: 688
client_name: "byteworks"
---

# Allow or Block Anonymous Calls Into Cisco Communications Manager LUA Script Update

This is a follow-up of sorts to a previous blog I posted on how to route calls into your Cisco Call Manager based on the calling ANI, or in layman’s terms, the caller-id of the ingress call.  So, for example, if you wanted to route all calls from a specific customer, to a specific employee or Call Handler etc., this would give you that ability.  I had previously posted a script that would still allow you to block specific calls, while still having the flexibility to allow or block “Anonymous” or restricted calls.  In CUCM 8.5 and previous, digit analysis did not handle non-numeric dial strings.  Due to this, when routing based on ANI, and the ANI was “anonymous” or “unavailable”, Call Manager would not accept the call.  The original script basically replaced this with a specific string of digits that you would choose.  This new updated script however, removes the unroutable string completely, allowing Call Manager to route or block based on a <NULL> route pattern in the <Filter_List> partition.  The biggest benefit to the new script in my opinion is that the display on the phone for allowed anonymous calls in most cases will be “private”.  Most folks expect that a call from an unknown caller to show as private, so this bahavior is more in line with normal expectations.  A few notes about the script:

*   The script is a proof of concept script and should be tested prior to deployment into a production environment.
*   The Script is not officially supported by Cisco TAC, Cisco Systems, or any of its affiliates (TAC will assist on a best-effort basis).
*   This script is entirely authored and supported by Dan Keller at Cisco Systems, and I thank and appreciate all his efforts supporting this feature and script.
*   If the script does not behave as expected:
    *   Change the “trace.disable()” to “trace.enable()”.
    *   Reset the SIP Trunk.
    *   Place a couple of calls into the trunk to demonstrate the issue.
    *   When configuring this script, set the “LUA Instruction Threshold” to 1500.
    *   Collect a detailed SDI trace file.
    *   Email the trace file, current SIP trunk script (if changes were made), and a description of the issue that includes the date, time, calling/called numbers and the result to Dan Keller for review to dakeller@cisco.com.

## Updated Script:

```lua
M={}

--change to trace.enable() to have trace output in SDI
trace.disable() 

function M.inbound_INVITE(msg) --capture inbound INVITE messages
 --set the string to replace the anonymous, unavailable or restricted strings in the INVITE message
 replacementNumber = "sip\:" 
 trace.format("Replacement Number: %s", replacementNumber)

 --Set the header values to inspect for anonymous caller
 local fields = { "From" , "Remote-Party-ID" , "P-Preferred-Identity", "P-Asserted-Identity" }
 local numberOfFields = #fields 
 trace.format("Fields/Count: %s, %s, %s, %s, %s", fields[1], fields[2], fields[3], fields[4], numberOfFields)
 
 --loop though the header fields to inspect and replace any instance of 'anonymous' with the specified replacement number
 local x = 1
 while x <= numberOfFields do 

 --get the field from the header
 local header = msg:getHeader(fields[x])
 if header == nil
 then
 trace.format("Field %s not found", fields[x])
 else
 trace.format("Field %s: %s", fields[x], header)

 --does the from contain anonymous
 if string.find(string.lower(header), "sip\:anonymous") 
 then
 trace.format("Found string anonymous in %s", fields[x])
 trace.format("Header: %s %s", fields[x], string.lower(header))

 --replace the word anonymous with the user defined replacement number
 local newHeader = string.gsub(string.lower(header), "sip\:anonymous", replacementNumber) 
 trace.format("New %s Field: %s", fields[x], newHeader)

 --modify the From field
 msg:modifyHeader(fields[x], newHeader) 
 else if string.find(string.lower(header), "sip\:unavailable")
 then
 trace.format("Found string unavailable in %s", fields[x])
 trace.format("Header: %s %s", fields[x], string.lower(header))

 --replace the word unavailable with the user defined replacement numbe
 local newHeader = string.gsub(string.lower(header), "sip\:unavailable", replacementNumber) 
 trace.format("New %s Field: %s", fields[x], newHeader)

 --modify the From field
 msg:modifyHeader(fields[x], newHeader) 
 
 else if string.find(string.lower(header), "sip\:restricted")
 then
 trace.format("Found string unavailable in %s", fields[x])
 trace.format("Header: %s %s", fields[x], string.lower(header))

 --replace the word unavailable with the user defined replacement number
 local newHeader = string.gsub(string.lower(header), "sip\:restricted", replacementNumber) 
 trace.format("New %s Field: %s", fields[x], newHeader)

 --modify the From field
 msg:modifyHeader(fields[x], newHeader) 
 
 else
 trace.format("Field %s number valid. No change made.", fields[x])
 end
 end
 end
 end
 x = x+1
 end
end
return M
```