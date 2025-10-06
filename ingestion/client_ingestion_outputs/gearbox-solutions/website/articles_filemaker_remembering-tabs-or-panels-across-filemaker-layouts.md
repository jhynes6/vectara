---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/filemaker/remembering-tabs-or-panels-across-filemaker-layouts"
title: "/articles/filemaker/remembering-tabs-or-panels-across-filemaker-layouts"
domain: "gearboxgo.com"
path: "/articles/filemaker/remembering-tabs-or-panels-across-filemaker-layouts"
scraped_time: "2025-10-05T01:40:03.979312"
url_depth: 3
word_count: 775
client_name: "gearbox-solutions"
---

Remembering tabs or panels across FileMaker layouts - Gearbox Solutions

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

# Remembering tabs or panels across FileMaker layouts

In a recent discussion with another FileMaker developer, we were singing the praises of the popular [Browser Navigation module](http://www.modularfilemaker.org/module/browser-navigation/) from Paul Jansen. We've been using it for a few years now and I see it more all the time. It's also used in Geist Interactive's open framework, [Karbon (Github)](https://github.com/karbonfm/karbonfm).

### **How do we remember what tab the user was on when we come back?**

That was a challenge we needed to meet head-on as many users find it frustrating to jump some place else in the app to look at other information, only to come back to the original layout and loose their focus because when they left, they were on **Team** tab and now they're on the **Summary** tab.

![](https://s3.us-east-1.amazonaws.com/assets.gearboxgo.com/ui-tabs.png)

### The Solution

Here's what we do... we have a modular script we call

> _gotoPanel ( entity ; object ; nav )_

First off, we don't use FileMaker's native tabs. There were limitations on styling them as well as some constraints that required work-arounds. Overall, while they serve a purpose, we have incorporated [button bars](https://fmhelp.filemaker.com/help/17/fmp/en/index.html#page/FMP_Help%2Fdefining-changing-button-bar.html%23) and [slide controls](https://fmhelp.filemaker.com/help/17/fmp/en/index.html#page/FMP_Help%2Fadding-slide-control.html), which we find more flexible.

Assuming a layout is based on an _entity_, we set a global specific for that entity and check for its existence and go to that object when we land back on our original layout.

This technique requires an **onLayoutEnter** script trigger.

Step 1 - Name your button bar object. We'll call this **company**.tabs (company being our entity).

Step 2 - Name your individual buttons in the button bar:

*   company\_tab.1

*   company\_tab.2

*   company\_tab.3

*   ...

Step 3 - Name your panels in your slide control:

*   company\_panel.1

*   company\_panel.2

*   company\_panel.3

*   ...

When the user clicks a button bar, we run our script, passing parameters:

Let (\[
n = 1 ;
entity = "company"
\] ;
JSONSetElement ( "{}";
\[ "entity" ; entity ; JSONString \] ;
\[ "object" ; entity & "\_panel." & n ; JSONString \] ;
\[ "nav" ; entity & ".tabs" ; JSONString \]
)
)

This is broken out with local variables in the Let statement so that we can use this across our solution, only chancing the "n" and "entity" when we need to.

The script itself is straight forward. We simply assign a global as follows:

"TAB." & $entity ; $object = $$TAB.company = company\_panel.1

### Completion

When we do return to our original layout, we run our script trigger **onLayoutEnter ( entity )**. The layout passes the correct entity (in this case "company").

\# we're always getting our parameters... JSON
Set Variable \[ $! ; Value: JSONCreateVarsFromKeys ( Get ( ScriptParameter ) ; "" ) \]
#
If \[ not IsEmpty ( Evaluate ( "$$TAB." & $entity ) ) \]
Perform Script \[ Specified: From list ; "gotoPanel ( object { ; focus ; refresh\_object } )" ; Parameter: JSONSetElement ( "{}"; \["entity"; $entity ; JSONString\] ; \["object"; Evaluate ( "$$TAB." & $entity ) ; JSONString\] ; \["nav"; $entity & ".tabs" ; JSONString\] ) \]
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

Or, feel free to call us at [770.7