---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/filemaker/cargowise-filemaker-integration"
title: "CargoWise + FileMaker Integration"
domain: "gearboxgo.com"
path: "/articles/filemaker/cargowise-filemaker-integration"
scraped_time: "2025-10-05T01:40:16.745947"
url_depth: 3
word_count: 616
client_name: "gearbox-solutions"
---

# CargoWise + FileMaker Integration

We have a client in the Logistics space with a focus on moving fine art all over the world. Let's say you have a $7 million (or $70 million) Monet you would like to loan to the Petit Palais in Paris for 6 months for an exhibition... How would you get it there and how do you make sure you get it back? This company does that...

### The Problem

They began as a small boutique over 30 years ago when most things in that industry were paper-based. In recent years in order to stay competitive and leverage industry best-practices, they moved most of their business back-end to a platform called CargoWise. By some estimates, 70% of the worlds shipments each year are managed on this supply chain platform. To give you an idea of how big they are, UPS is a client. From customs, compliance and airway bills to customer management and finance, it's their system of record. When they asked Gearbox to rebuild their in-house systems for client management, estimating, and forecasting, it was clear that if we could not integrate with CargoWise, it was a non-starter for all involved. Just another example of how important integrations are to pretty much any business these days.

Working with their existing integration partners, we designed a process that not only met their needs, but brought about a major efficiency by not forcing managers and coordinators to log into multiple systems to do their jobs.

### The Example

In their old system, there was an "import/export" style integration that included XML files and FTP servers. It worked, but it was brittle and the process failed sometimes on a daily basis. When it was working, they only had 1 shot of a successful transaction. After that, it was "login to CargoWise".

If it "worked", then they were able to log into CargoWise to complete the necessary shipment data required for something to actually travel. Limited financial information and no contents/crate information could be sent to CargoWise.

### The Solution

Not only can the coordinators now click a button to create new shipments in CargoWise, but they get back the all-important shipment reference number that ties all airway bills, customs documentation, power of attorney, consignee and foreign agents together as well as the actual crates - the objects being shipped.

They can choose to send billing information to populate finance and crate contents for customs if they like. And they can do this as many times as necessary.

Since we're integrating with a custom API in this case, we can parse and display detailed information to the users about every single transaction so that if there was a problem, they can begin troubleshooting themselves on the spot.

### The Landmines

1. Integrating directly with CargoWise can be a daunting feat. We recommend working with CargoWise certified partners to save time and headache. For example, the raw data from a single shipment can be upwards of 5 thousands lines of complex XML. Once it gets to what our app deals with, we are dealing with around 200 lines of JSON with a RESTful API. Pushing and pulling data can be as simple as leveraging the latest versions of the Claris FileMaker platform.

2. Another consideration is that there is currently no such thing as truly synchronous communication with CargoWise. It is asynchronous, therefore you must consider building your integration for listening to API calls from another system. You must set up your own endpoints to allow data to flow both ways.

Sometimes everything we deliver, we design and develop. This is an example of how Gearbox can work with other partners to truly add value.