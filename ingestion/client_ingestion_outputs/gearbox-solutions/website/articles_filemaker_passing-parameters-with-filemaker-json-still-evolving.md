---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/filemaker/passing-parameters-with-filemaker-json-still-evolving"
title: "/articles/filemaker/passing-parameters-with-filemaker-json-still-evolving"
domain: "gearboxgo.com"
path: "/articles/filemaker/passing-parameters-with-filemaker-json-still-evolving"
scraped_time: "2025-10-05T01:39:36.803897"
url_depth: 3
word_count: 1061
client_name: "gearbox-solutions"
---

Passing Parameters with FileMaker + JSON - Still Evolving - Gearbox Solutions

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

# Passing Parameters with FileMaker + JSON - Still Evolving

### In the beginning...

I was among the masses that took Geoff Coffey's lead and started using custom functions to [pass multiple parameters](http://sixfriedrice.com/wp/passing-multiple-parameters-to-scripts-advanced/) over a decade ago. As time passed, the next thing that stuck was the now legendary [#Parameters](http://www.modularfilemaker.org/module/parameters/) set of functions - a gift from [Jeremy Bante](https://twitter.com/jbante) several years ago.

With the advent of FileMaker 16, we got native JSON. As lovely as it was (and is), My brain felt a slight step backward as I lost a bit of control and efficiency as I decided to force myself to use JSON everywhere I could. I even [presented on this topic](https://twitter.com/dotfmp/status/1004999121588105216) in June at @dotmfp in Berlin.

Passing JSON back to a script without anything fancy means you need to declare your variables one at a time - which has been argued is a good thing - verbose, easy to follow, know what to expect. But after years of using a prototype for my FileMaker scripts like this below, I wanted to stick with doing it all at once.

getBidSheet ( id {; card })

### Sometimes if you procrastinate, you are rewarded

I started to tinker with a custom function but never completed it. Then one cold day in January (I'm sure it was cold in Chicago at least), Mislav Kos of Soliant shared a shiny new [custom function to parse JSON](http://www.soliantconsulting.com/blog/automatically-create-variables-json-filemaker) that was just what I was looking for (well, almost).

I didn't hesitate using this everywhere (and got to get rid of stuff like this:)

<del>Set Variable \[ $parameters ; Value: Get ( ScriptParameter ) \]
# now do this
Set Variable \[ $id ; Value: JSONGetElement ( $parameters ; "id" ) \]
Set Variable \[ $card ; Value: JSONGetElement ( $parameters ; "card" ) \]</del>

Set Variable \[ $! ; Value: JSONCreateVarsFromKeys ( Get ( ScriptParameter ) ; "" ) \]

### What about setting multiple key-value pairs?

I came up with a script I've been using for years to set as many key-value pairs as I wanted using the #Parameters function. Consider this script...

setFields ( field\[\] ; value\[\] {; flush ; object ; portal ; layout } )

and this to pass...

\# ( "field\[0\]" ; GetFieldName ( SELECTOR::ID\_RESPONSE ) ) &
\# ( "value\[0\]" ; responses::id ) &
\# ( "field\[1\]" ; GetFieldName ( SELECTOR::ID\_PATIENT ) ) &
\# ( "value\[1\]" ; respPatients::id )

the stuff that does the work...

\# do we have multiple fields here?
If \[ PatternCount ( Get ( ScriptParameter ) ; "\[" ) \]
Set Variable \[ $n ; Value: 0 \]
Loop
Exit Loop If \[ IsEmpty ( $field\[$n + 1\] ) \]
Set Variable \[ $n ; Value: $n + 1 \]
Set Field By Name \[ $field\[$n\] ; $value\[$n\] \]
End Loop
Else
Set Field By Name \[ $field ; $value \]
End If
Commit Records/Requests \[ Skip data entry validation ; With dialog: Off \]

I can only speak for myself, but what I wanted now was something that allowed me to do what the above script does, but with using JSON. It didn't take long if you have a bit of JSON structure knowledge. I finally settled on this. I get to leverage JSON, leverage my **go-to** custom function for parsing JSON, and all is right with the world.

The script:

setFieldsJSON ( array ( field ; value {; object ; portal ; layout } )

The parameters:

JSONSetElement ( "{}";
\[ "pairs\[0\].field" ; GetFieldName ( FIND::id\_VENDORS ) ; JSONString \] ;
\[ "pairs\[0\].value" ; FIND.companies::id ; JSONString \] ;
\[ "pairs\[1\].field" ; GetFieldName ( FIND::id\_PRODUCTS ) ; JSONString \] ;
\[ "pairs\[1\].value" ; FIND.companies::id ; JSONString \] ;
\[ "object" ; "portal.vendors" ; JSONString \]
)

The script bit that does the heavy lifting:

\# do we have multiple fields here?
Set Variable \[ $count ; Value: ValueCount ( JSONListKeys ( $pairs ; "" ) ) \]
Set Variable \[ $i ; Value: 0 \]
Loop
Set Variable \[ $field ; Value: JSONGetElement ( $pairs ; "\[" & $i & "\].field" ) \]
Set Variable \[ $value ; Value: JSONGetElement ( $pairs ; "\[" & $i & "\].value" ) \]
Set Field By Name \[ $field ; $value \]
Set Variable \[ $i ; Value: $i + 1 \]
Exit Loop If \[ $i > ( $count - 1 ) \]
End Loop
Commit Records/Requests \[ Skip data entry validation ; With dialog: Off \]

### **We're done**

This stuff helps our team be more efficient and this stuff is very portable. We have this running in several projects right now and it's a breath of fresh air knowing we have this and so many wonderful tools from the FileMaker community at our disposal.

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

Or, feel free to call us at [770.765.6