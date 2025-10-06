---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/filemaker/transactions-mvc-party-model-in-filemaker"
title: "Transactions, MVC, and Party Model in FileMaker"
domain: "gearboxgo.com"
path: "/articles/filemaker/transactions-mvc-party-model-in-filemaker"
scraped_time: "2025-10-05T01:39:29.827074"
url_depth: 3
word_count: 526
client_name: "gearbox-solutions"
---

# Transactions + MVC + Party Model in FileMaker.

We've been busy working on one of the largest solutions we've ever developed here at Gearbox.

Thank goodness for this [platform](https://www.filemaker.com/workplace-innovation/) and the [community](https://community.filemaker.com/) around it. We're still learning new techniques all the time. Over the past several months, a large new project forced us to challenge ourselves and ask ourselves some serious questions... Were we able to pull this off? Did we have the right resources? Did we have best approaches for modular scripting, managing and modeling data, etc?

The answers led us to not only bring our best game, but also adopt all kinds of techniques we had not used much in the past. **By far** the largest impact on the progress and success so far has been implementing the Party Model, using MVC, and leveraging what we have learned from Karbon - mostly around [transactions](https://en.wikipedia.org/wiki/Database_transaction).

### Transactions

If you want to know how we're taking our best work to the next level, learn the value of transactions in [this article](https://www.geistinteractive.com/filemaker-transactions/), most widely evangelized by [Todd Geist](https://twitter.com/toddgeist). There are other resources out there, but it's a great place to start.

A stellar example of this is found in the Geist Interactive's open source application framework, [Karbon](https://github.com/karbonfm/karbonfm). While we did not build our solution with this framework, we leveraged much of the transactions functionality that has made development and testing **so much better**.

### MVC

Karbon certainly promotes the idea of MVC within the FileMaker platform and while we have used similar approaches before, this project led us to fully commit to this pattern.

Another source of inspiration and insight for MVC is from the highly respected team at [The Proof Group](https://proofgroup.com/). While their recent talk was focused on the Party Model, there is much to glean from their MVC architecture. Ernest and Corn are... smart.

### Party Model

[Len Silverston](http://www.universaldatamodels.com/).

He gets his own paragraph. Know what he knows and you'll be set.

I confess I think I heard of him years ago and paid little attention. Then after hearing Corn Walker reference him, I looked him up again. Now I own all three volumes of [The Data Model Resource Book](http://www.universaldatamodels.com/Publications/Books.aspx). It's not necessary to read every page of every one of these books, but it helped immensely when trying to understand and implement the party model within FileMaker. For example, knowing the difference between a _declarative_ role and a _contextual_ role can be really helpful.

There is not only one way to implement this data model, but the more I understood the various approaches, the better I was able to implement the **right** model for a particular solution.

Karbon implements the Party Model, as do many other FileMaker solutions. If you want a high level overview, I highly recommend the [DIGFM session](https://www.youtube.com/watch?v=6JCEqsP7VQQ) by Ernest Koe and Corn Walker.

Another source of education and inspiration is a presentation by [Dave Graham](https://twitter.com/bittailor) of Geist Interactive. If you're interested, watch [Data Modeling That Scales](https://www.youtube.com/watch?v=kfiP8TQ1Jtg).

### Evidence

We're hoping the screenshots can in some small way convey how far we've come. We are grateful for what we have learned from Geist, Proof, and so many others every day.