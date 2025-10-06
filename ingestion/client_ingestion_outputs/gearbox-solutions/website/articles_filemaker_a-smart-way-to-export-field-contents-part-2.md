---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/filemaker/a-smart-way-to-export-field-contents-part-2"
title: "/articles/filemaker/a-smart-way-to-export-field-contents-part-2"
domain: "gearboxgo.com"
path: "/articles/filemaker/a-smart-way-to-export-field-contents-part-2"
scraped_time: "2025-10-05T01:40:11.725131"
url_depth: 3
word_count: 763
client_name: "gearbox-solutions"
---

A Smart Way to Export Field Contents - Part 2 - Gearbox Solutions

[

What we do

](/what-we-do)[

Software Kit

](/software-kit)[

Industries

](/industries)[

Case Studies

](/case-studies)[

Articles

](/articles)[

Client Portal

](https://portal.gearboxgo.com)

[

What we do

](/what-we-do)

[

Software Kit

](/software-kit)

[

Industries

](/industries)

[

Case Studies

](/case-studies)

[

Articles

](/articles)

Contact

## How can we help?

Ready to learn more about what Gearbox can do for you? Get in touch to schedule a free consultation.

Have a particular problem you’d like solved? Let Gearbox find the solution.

Submit

Or, feel free to call us at [770.765.6258](tel:7707656258)

# A Smart Way to Export Field Contents - Part 2

### **We love sometimes like Selector Connector**

Since the initial news of this new technique from [Todd Geist](https://twitter.com/toddgeist) and [Jason Young's](https://twitter.com/TeraPicoData) smashing session at DevCon this year, we've been incorporating it into most of our solutions.

If you haven't seen [Part 1](/articles/filemaker/a-smart-way-to-export-field-contents-part-1) discussing how we improved the ability to download files from container fields with one script, check it out.

Sometimes **"good enough" is never enough.** I thought we had moved on, but I was reminded that I had designed this particular large project to manage _all_ files (everything form creative briefs, spreadsheets, PDFs, lo-res comps, etc.) in one table **and** my colleague knew we were using [Selector Connector](http://www.seedcode.com/filemaker-selector-connector-basics/).

> Why don't we just leverage Selector Connector and pass the ID of the file record to SELECTOR and there's your target?

He was right... We avoided [premature optimization](https://en.wikiquote.org/wiki/Donald_Knuth) and then iterated as a team to come up with something that was simple to implement, simple to use, and then moved on. Below is the final script.

![](https://s3.us-east-1.amazonaws.com/assets.gearboxgo.com/sel-con.png)

#### What do you think?

\[saveFile ( id )\]
# . . . . . . . Gearbox Solutions
# . . . . . . . created on - 11.10.2015
# . . . . . . . created by - mhl
# . . . . . . . purpose - export contents of container to 'Downloads' folder
# . . . . . . . updates...
# . . . . . . . 11.11.2015 - mhl - rohit - write files to a global so we can export without hardcoding 'Export Field Contents'
# . . . . . . . 11.12.2015 - mhl - Marty suggested leveraging SelectorConnector
#  set vars
Set Variable \[ $vars ; Value: #Assign ( Get( ScriptParameter ) ) \]
#
# 11.12.2015 4:22pm - since all container fields/'files' are saved in a single "files" table, get the ID and use SelectorConnector
#
# SELECTOR
Set Field \[ SELECTOR::id\_FILE ; $id \]
Set Variable \[ $filename ; Value: GetContainerAttribute ( SEL.file::file ; "filename" ) \]
Set Variable \[ $filepath ; Value: Substitute(Get(DesktopPath);"Desktop";"Downloads") & $filename \]
# now export from ONE place!
Export Field Contents \[ SEL.file::file ; "$filepath" ; Automatically open \]
Exit Script \[ Result: 1 \]
#
# 11.11.2015 8:52pm - we're going to try a technique suggested by Rohit to use a global so we don't have to go through what is below...
#
# copy into global
Set Field \[ globals::FILE\_TEMP\_CONTAINER ; Evaluate ( $field ) \]
# now export from ONE place!
Export Field Contents \[ globals::FILE\_TEMP\_CONTAINER ; "$filepath" ; Automatically open \]
Exit Script \[ Result: 1 \]
# have to hard code field :(
If \[ $entity = "approvals" \]
Export Field Contents \[ SEL.approval\_versions::file ; "$filepath" ; Automatically open \]
Else If \[ $entity = "pro.files" \]
Export Field Contents \[ pro.files::file ; "$filepath" ; Automatically open \]
End If

## Let's Work Together

Ready to learn more about Gearbox? Get in touch to schedule a free consultation.

We'll talk about your projects and tell you how we can help.

Let's Go

## How can we help?

Ready to learn more about what Gearbox can do for you? Get in touch to schedule a free consultation.

Have a particular problem you’d like solved? Let Gearbox find the solution.

Submit

Or, feel free to call us at [770.765.6258](tel:7707656258)

Contact UsContact Us

## How can we help?

Ready to learn more about what Gearbox can do for you? Get in touch to schedule a free consultation.

Have a particular problem you’d like solved? Let Gearbox find the solution.

Submit

Or, feel free to call us at [770.765.6258](tel:7707656258)

Contact

[](https://www.youtube.com/@GearboxGo)[](https://www.linkedin.com/company/gearbox-solutions)

## How can we help?

Ready to learn more about what Gearbox can do for you? Get in touch to schedule a free consultation.

Have a particular problem you’d like solved? Let Gearbox find the solution.

Submit

Or, feel free to call us at [770.