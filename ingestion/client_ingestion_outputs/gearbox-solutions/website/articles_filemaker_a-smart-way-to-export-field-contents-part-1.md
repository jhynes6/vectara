---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/filemaker/a-smart-way-to-export-field-contents-part-1"
title: "A Smart Way to Export Field Contents - Part 1"
domain: "gearboxgo.com"
path: "/articles/filemaker/a-smart-way-to-export-field-contents-part-1"
scraped_time: "2025-10-05T01:39:26.330822"
url_depth: 3
word_count: 461
client_name: "gearbox-solutions"
---

# A Smart Way to Export Field Contents - Part 1

A little collaboration is always a good thing (and it's nice to work with smart people)...

### The Problem

As a FileMaker developer (citizen or otherwise), have you ever had a need to export from multiple container fields within a system? We wanted to be able to export files from disparate container fields directly to the "Downloads" folder of the user.

A member of our team initially wrote a nice script to get the path and export the contents. One issue we have is that we have container fields used throughout the solution, so since there is no "Export Field Contents By Name", we have to explicitly point to the target field, which makes things... not elegant.

### The Solution

We decided to pass the field as a parameter so we could evaluate and get the proper attributes (see below), but we were unable to leverage that bit of goodness to export the file itself.

Then someone else suggested setting a global with the contents and exporting from there. Brilliant, but we weren't even sure it would work. **It did.**

Now we can pass the field name in the script and reuse this script across the entire solution. Yea!

**UPDATE** - Check out the follow-up post, using [Selector Connector](/articles/filemaker/a-smart-way-to-export-field-contents-part-2).

```plaintext
[saveFile ( field ; entity )]
```

# . . . . . . . Gearbox Solutions
# . . . . . . . created on - 11.10.2015
# . . . . . . . created by - mt
# . . . . . . . purpose - export contents of container to 'Downloads' folder
# . . . . . . . updates...
# . . . . . . . 11.12.2015 - mhl - write files to a global so we can export without hardcoding 'Export Field Contents'
#  set vars
Set Variable [ $vars ; Value: #Assign ( Get( ScriptParameter ) ) ] 
# now the remainder
Set Variable [ $filename ; Value: GetContainerAttribute(Evaluate($field) ; "filename") ] 
Set Variable [ $filepath ; Value: Substitute(Get(DesktopPath);"Desktop";"Downloads") & $filename ] 
#  
# we're going to try a technique suggested by rr to use a global so we don't have to go through what is below...
#  
# copy into global
Set Field [ globals::FILE_TEMP_CONTAINER ; Evaluate ( $field ) ] 
# now export from ONE place!
Export Field Contents [ globals::FILE_TEMP_CONTAINER ; "$filepath" ; Automatically open ] 
Exit Script [ Result: 1 ] 
# have to hard code field :(
If [ $entity = "approvals" ] 
    Export Field Contents [ SEL.approval_versions::file ; "$filepath" ; Automatically open ] 
Else If [ $entity = "pro.files" ] 
    Export Field Contents [ pro.files::file ; "$filepath" ; Automatically open ] 
End If