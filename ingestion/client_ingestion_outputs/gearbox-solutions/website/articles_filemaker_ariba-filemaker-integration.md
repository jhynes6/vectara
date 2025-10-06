---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/filemaker/ariba-filemaker-integration"
title: "Ariba + FileMaker Integration"
domain: "gearboxgo.com"
path: "/articles/filemaker/ariba-filemaker-integration"
scraped_time: "2025-10-05T01:39:54.642617"
url_depth: 3
word_count: 1171
client_name: "gearbox-solutions"
---

# Ariba + FileMaker Integration

In this video, Gearbox and Marty Thomasson of Gearbox talk about the experience they had integrating SAP Ariba with a custom workgroup solution. As you'll hear, the client had some real world constraints that prevented a direct API integration. Gearbox worked with the client to execute an effective work around that got the job done without blowing the budget or missing the deadline. Like all work arounds, there were a few drawbacks. Stay tuned to hear more about that.

Michael (00:27):  
Hey Marty, thanks for chatting with me today.

Marty (00:31):  
No problem, Michael.

Michael (00:33):  
I wanted to talk to you about some of the integration work that we've done over the years specifically about SAP Ariba. But before we get started, have we done any integrations with finance or accounting software besides Ariba.

Marty (00:51)  
Yes, we've had a number of projects with accounting and process management systems at larger companies, as well as accounting systems like QuickBooks or QuickBooks Online at smaller companies. Our smaller midsize companies that are using QuickBooks, I'm seeing a lot of them shift over to QuickBooks Online.

Michael (01:21):  
Okay. So you had already done a pretty complex integration with this particular client before they moved to Ariba. Can you speak a little about that legacy system and how it compares to what you ended up doing when they switched to Ariba?

Marty (01:39)  
Sure. They had an internal system that they had built that managed all their POS invoices and payments and integrated with a number of other systems internally. We built a custom solution for a particular department that allowed them to track things a little more granularly and do a better job of forecasting for their needs. At the time we had a lot of support from that department and their internal IT group, and there was budget and time available. So we were able to integrate directly with that system which is your best case scenario. If there is an API or a way to do direct integration and you have the support, well, that's the way to go. And so we had a robust, tightly integrated set of systems in that case.

Michael (02:47):  
What were some of the benefits of integrating with their Ariba system rather than just simply leaving it to them, logging in Ariba only.

Marty (03:00)  
So when they switched to Ariba, that was one of the decisions they had to make corporate wide. The switch brought a central single process for managing all of their POs and invoices and payments. However, we weren't going to have the time and budget available from their IT group to do a direct integration to SAPs Ariba API. So they had to make a decision, do they want to stop using this custom system and stop leveraging the benefits that it gave them, or keep using it and rekey the data which was going to take a lot of time and be error prone. So at first that seemed like their only options, but we just dug a little deeper and decided, well, we can't get direct API access, but there has gotta be another way to do it. So we went with built-in reporting options. And so now the users just run a report on a weekly basis export that data and then we import it into our system.

Michael (04:28):  
I like that that digging deeper. It sounds like digging deeper is something that happens on a lot of projects.

Marty (04:36):  
Yeah. It's about every one.

Michael (04:39):  
So how have you managed any changes or updates to their Ariba environment? Since, since they've gone live with the system?

Marty (04:49):  
There really haven't been too many changes on the Ariba side, you know, it's following standard accounting processes. So the reports that we get are the same every time. So we really haven't had to change how we do the integration. We have made changes since it's a small custom system, we can still be nimble and make changes to meet the particular department's needs, but the integration really hasn't changed.

Michael (05:23):  
Were there any landmines as you were having to deal with the Ariba system importing all that data from those reports?

Marty (05:36):  
Yeah. You know, if we were dealing directly with the API we would have had better internal unique identifiers for records, for example. And by pulling it from reports, we didn't get that. So in some cases, some of the data, we don't a unique identifier and we had to sort of craft one from multiple data points. So that's one example.

Marty (06:02):  
We had to map out all the different scenarios. You need to do this with any integration, but we definitely had to map out all the different scenarios. When new data comes in, how do we treat it? And in this case, we don't get a lot of options for which data when they pull the report, there's some data included that we don't want.

Marty (06:35):  
So we have to identify that data and parse it out and leave it behind. But we had to map out all the different scenarios of when records, when that date is created, when it's updated on either side, how are we going to handle that change?

Michael (06:53):  
So it sounds like someone in the current custom application, they might click a button, but a lot goes on behind the scenes to massage that data and to get it right before it actually gets pulled into the custom system.

Marty (07:09):  
Yeah, absolutely. We're stepping through a lot of different checks to validate data and make sure that we don't have any issues. We don't want to end up with duplicate records in our system. We've got to manage versioning of the data that we get from SAP, from Ariba.

Michael (07:27):  
I mean, what could ever go wrong with duplicate records?

Marty (07:32):  
I mean, the more data, the better, right. (laughs)

Michael (07:34):  
So wrapping up on a scale from one to 10, how would you rate the complexity of this particular Ariba integration that you did?

Marty (07:45):  
I would say getting the data out of Ariba and just importing it, that was pretty straightforward, fairly easy. Probably took less time than if we were working with the API. But on the backend, after we get the data, there's a lot of work we have to do that we might not have needed if we had direct API access. So I'd give it a solid six.

Michael (08:14):  
Alright, fair enough. Well, this was helpful for me to get an idea of what Gearbox did and I appreciate you walking me through this.

Marty (08:26):  
Appreciate it.

Narrator (08:30):  
If you have software integration needs, please visit gearbox, go.com and click the blue button to schedule a call. That URL again is gearbox. go.com. Thanks for watching.