---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/filemaker/a-simple-filemaker-while-example"
title: "A Simple FileMaker While() Example"
domain: "gearboxgo.com"
path: "/articles/filemaker/a-simple-filemaker-while-example"
scraped_time: "2025-10-05T01:40:24.920416"
url_depth: 3
word_count: 579
client_name: "gearbox-solutions"
---

# A Simple FileMaker While() Example

### **Thanks for the While()**

FileMaker 18 has provided a new function that can transform what we can do within the calculation engine. There are several articles that explain the function such as these from [Geist Interactive](https://www.geistinteractive.com/2019/06/10/filemaker-18-exploring-all-the-while/), [AppWorks](https://app.works/while-loops/), [Skeleton Key](https://skeletonkey.com/filemaker-18-the-while-function-looping-in-calculations/), and more.

### **Not Hello World**

I get the `Hello World` thing when people explain simple concepts in an attempt for readers to understand how a language or function or method works, but I often find myself needing just a bit more... perhaps a **real-world** example.

### **Button Bars as Navigation**

At Gearbox, we often use button bars for a tab navigation along with slide controls. They work great; total control/customization, modular... I love it. But how do we control state (i.e. which segment is active)? FileMaker gave us a door to the calc engine when it comes to specifying the Active State. If this wasn't available, we'd have to come up with yet another _hack_. We discuss how we track tabs and panels [here](https://craft.gearboxgo.com/admin/entries/insights/%7Bentry:418:url%7D#entry:418:url).

### **The Obstacle is the Way**

OK. Here's how I used to programmatically determine which segment needed to be "Active". In case you're not familiar, the way this works is that you must _name_ each button bar segment object.

```plaintext
Let ( [ 
entity = "shipment" 
] ;
Case ( 
 GetLayoutObjectAttribute ( entity & "\_panel.2"; "isFrontPanel" ) ;
 entity & "\_tab.2" ;
 GetLayoutObjectAttribute ( entity & "\_panel.3"; "isFrontPanel" ) ;
 entity & "\_tab.3" ;
 GetLayoutObjectAttribute ( entity & "\_panel.4"; "isFrontPanel" ) ;
 entity & "\_tab.4" ;
 GetLayoutObjectAttribute ( entity & "\_panel.5"; "isFrontPanel" ) ;
 entity & "\_tab.5" ;
 GetLayoutObjectAttribute ( entity & "\_panel.6"; "isFrontPanel" ) ;
 entity & "\_tab.6" ;
 GetLayoutObjectAttribute ( entity & "\_panel.7"; "isFrontPanel" ) ;
 entity & "\_tab.7" ; 
 GetLayoutObjectAttribute ( entity & "\_panel.8"; "isFrontPanel" ) ; 
 entity & "\_tab.8" ; 
 GetLayoutObjectAttribute ( entity & "\_panel.9"; "isFrontPanel" ) ; 
 entity & "\_tab.9" ; 
 GetLayoutObjectAttribute ( entity & "\_panel.10"; "isFrontPanel" ) ; 
 entity & "\_tab.10" ; 
 // default
 entity & "\_tab.1" 
) 
)
```

It took me a bit of time to figure out what I was doing and make some mistakes along the way. Part of the reason was that I was trying to write a While() statement based on the examples I had seen. What worked for me was going back to the [original documentation](https://fmhelp.filemaker.com/help/18/fmp/en/#page/FMP_Help%2Fwhile.html%23ww1286452). The key for me was

> `condition` _- a Boolean evaluated before each loop iteration. While True, the loop repeats. When False, the loop stops._

This is where I ended up and I'm so glad I'll never have to type out all those numbers and lines again!

```plaintext
While ( 
 [ 
 entity = "shipment";
 i = 1;
 result = ""
 ] ; 
 // condition/magic
 GetLayoutObjectAttribute ( entity & "\_panel." & i ; "isFrontPanel" );
 [ 
 result = entity & "\_tab." & i;
 i = i + 1
 ] ;
 
 result 
)
```

### **Extra Credit**

We also track which tab is active so that when they navigate away from the layout, we bring them back to the correct spot. So we set that variable like so:

```plaintext
// initTab may result is 1 - 10
initTab = Right ( GetAsNumber ( JSONGetElement ( $TAB.json ; entity ) ) ; 1 );
 
// if we have an initial tab, great, otherwise load the first tab (i = 1)
result = If ( IsEmpty ( initTab ) ; entity & "\_tab." & i ; entity & "\_tab." & initTab )
```