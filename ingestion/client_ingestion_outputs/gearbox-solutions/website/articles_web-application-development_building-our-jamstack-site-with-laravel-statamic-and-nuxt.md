---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/web-application-development/building-our-jamstack-site-with-laravel-statamic-and-nuxt"
title: "Building our Jamstack site with Laravel, Statamic, and Nuxt SSG"
domain: "gearboxgo.com"
path: "/articles/web-application-development/building-our-jamstack-site-with-laravel-statamic-and-nuxt"
scraped_time: "2025-10-05T01:39:52.299827"
url_depth: 3
word_count: 1806
client_name: "gearbox-solutions"
---

# Building our Jamstack site with Laravel, Statamic, and Nuxt SSG

We’ve recently launched a new version of the Gearbox site, and the tech stack behind this is pretty fun! We’ve built our site using Jamstack methodologies to be able to deliver the highest performance for our visitors.

### What is Jamstack?

Jamstack isn’t a framework or piece of software, but is instead a concept for how to build a site or web application. The idea behind Jamstack is that you separate the presentation of your site or content from data processing or business logic behind it. In the case of a website and blog like ours, this means separating our CMS used for writing our content and the generation and presentation of the site.

The “Jam” in Jamstack stands for Javascript, APIs, and Markup. In a Jamstack site you use these tools to build out the functionality of the presentation layer of your application (ie: the HTML content delivered to your users).

A core concept of Jamstack is pre-rendering of pages and content for faster, easier distribution to visitors. Instead of hitting your application server for every request, and generating the same page over and over again, such as a home page or a blog post, you pre-render your content as static HTML. This works great for content that doesn’t change very often, such as a blog post.

Even for things that initially seem like you’d need to hit a database for, like a list of blog posts with pagination; The content of page 1 is always the same, as well as page 2, page 3, etc. Why not pre-render the HTML for those pages? The most recent 10 posts are always going to be the most recent 10 until you write a new post and the content is going to be exactly the same every time! When the time comes and you do write a new post and the content changes you re-generate your HTML to reflect your updated content and re-deploy to your hosting.

What about searching and returning search results? That’s where the APIs part comes in. It’s still fine to use client-side Javascript to hit an API endpoint to get specific data, such as a CMS to query for relevant blog posts or products matching specific filter criteria. For the stuff that’s the same for everyone, you pre-render. For things that change based on specific user actions, hit an API and get your data from there.

The data you retrieve is still less than you might expect. For a blog search you only need to return the search results from your API, with a post name, cover image, and summary. When you link to the actual blog content you’re back to a pre-rendered HTML page which was generated ahead of time.

This concept of rebuilding and redeploying is quite different from what you’d get with a platform like Wordpress or Magento for eCommerce. With those platforms you would update your content, which would save in a database, and then run server-side code on each request to retrieve the latest content from the database. You need a database and application server involved to handle every request. With Jamstack you’re going to be redeploying your static HTML every time you have a content change. With frequent updates this might mean many deployments in a single day.

This means having the right stack and a good deployment pipeline is really important.

### Our tech stack

We selected two key platforms for building our Jamstack site. We needed a CMS for writing our content, and a front-end for displaying it.

### The CMS

For our CMS we selected [Statamic](https://statamic.com/), which is built on [Laravel](https://laravel.com/). Statamic has a powerful and customizable editing interface, allowing us to configure our editing experience. It’s fairly priced for our use case, has lots of built-in features, and good community support.

By default, Statamic is a flat-file CMS and doesn’t require a database (though databases are well-supported). For a smaller site like ours a flat-file content storage system works very well. We don’t have thousands and thousands of pages which would require a database to manage, and as an added bonus the flat-file system means that we can track all of our content through version control.

Because it’s built on top of Laravel, Statamic runs on a platform we’re already very familiar with. We can use our regular application development concepts when extending the CMS or building our own unique features. We don’t have to learn a new CMS-specific way of doing things just to have access to a CMS we enjoy. Laravel is a secure, performant, powerful, and widely adopted framework with first-party and community features we love to use, making our lives as developers a breeze.

In our case, we used Statamic as a headless CMS with a separate front-end for displaying our CMS content.

### The front-end

[Vue](https://vuejs.org/) is our preferred front-end framework. Vue’s component, scripting, and templating engines work great with [Tailwind CSS](https://tailwindcss.com/) and make creating layouts a breeze. Unfortunately, the default behavior for a Vue app is to send a mostly-empty HTML page and then fill the content in with JavaScript. This is absolutely terrible for the purposes of SEO, as it means that search engines don’t really see any content on your page.

Luckily, [Nuxt](https://nuxt.com/) provides a great solution for this problem. Nuxt is a Node framework for building sites and applications using Javascript and Vue. Nuxt allows you to build your site using Vue, but will then do server-side rendering of your Vue components into full, regular HTML. When an API request is made, the content is fetched server-side. The Vue components are processed, and then the final HTML of the rendered Vue components is generated. The fully-rendered HTML is sent to the visitor’s browser before Vue kicks in, hydrates on top of the HTML, and makes your page work like regular Vue components for the purposes of interactivity. You get the benefits of server-side rendered content for SEO with a page that is fully rendered without any JavaScript, while maintaining the interactivity you love from a JavaScript framework.

It gets better, though. In addition to traditional server-rendered content where the server answers each query and generates a page, Nuxt also allows you to generate static HTML content for your whole site with its [static site generation feature](https://nuxt.com/docs/getting-started/deployment#static-hosting). It will generate your routes, follow the links it finds, and statically generate all of the pages it can find links for. For a marketing and blog site like this one, this means that all of the main pages and articles are discovered and rendered as static HTML. The generate process creates a single folder with all of our content in it. We can then take this generated folder of directories and HTML files and put them up on any hosting without needing to run a PHP or Node server at all.

### The deployment pipeline

Once we have generated our nice little folder of HTML content we’re ready to put it up for the world to see! We could FTP it up to some shared hosting server, but that’s not a particularly efficient way of deploying or distributing content.

Instead, we use [Cloudflare Pages](https://pages.cloudflare.com/) to host our content. Cloudflare Pages is static content hosting on Cloudflare’s CDN and specifically supports Nuxt static site generation. We point Cloudflare Pages at our GitHub repository, it downloads our code, runs the generate process, and then serves our content on Cloudflare’s massive global CDN. This means that our HTML, JavaScript, CSS, and static images are all served from locations close to our visitors, resulting in faster load times. Because it’s all static HTML, the time-to-first-byte is virtually instantaneous, the CDN’s high bandwidth and distribution delivers the content quickly, our users get fast-loading pages, and the search engine crawlers are pleased with all the content being there from the start.

A one-time build-and-deploy isn’t good enough, though. Since it’s all static HTML content with no data connection we need to rebuild our site whenever we have content changes in our CMS. We could log into the Pages admin console and trigger a rebuild whenever we want, but that’s time consuming and easy to forget. A much better option is to hook into Statamic’s save process and send a message to Cloudflare Pages’s [Deploy Hooks feature](https://developers.cloudflare.com/pages/platform/deploy-hooks/) to trigger our new build whenever we have content updates.

Statamic expects that you’re going to want to trigger custom actions when making changes to content, and so provides [event listeners](https://statamic.dev/extending/events) for doing this. We can listen for the “[EntrySaved](https://statamic.dev/extending/events#entrysaved)” event to run some code when an entry like a blog post is successfully saved. We can then use this event to send a message to the Cloudflare Pages deploy hook to let it know there is new content available and it needs to generate new HTML. Through this method we can work in our CMS like normal without having to think about the static build-and-deploy process and our content changes automatically go live just a few minutes later.

### Conclusion

Working with Statamic and Nuxt and deploying our site using Jamstack concepts provides benefits to us as developers as well as benefits to our site’s visitors.

For us as developers, we get the opportunity to build a site and customize a CMS using tools we’re very experienced with through our day-to-day work building complex web applications. Laravel provides the [Blade templating engine](https://laravel.com/docs/9.x/blade) and has [Inertia support with Vue](https://inertiajs.com/), but Blade instead of Vue means swapping back-and-forth between different templating syntaxes and our front-end developers jumping between PHP and JavaScript. Inertia is great for full-stack, monolithic applications, but is designed for client-side rendering (though there is server-side-rendering support). Even still, using either Blade or Inertia + Vue + SSR means hitting a server for every request and not taking full advantage of a CDN like Cloudflare.

Statamic does have a [static site generator package](https://github.com/statamic/ssg) available, but that still puts us back to PHP and Blade or Statamic’s own Antlers templating, which is another new templating syntax to learn the nuances of.

With the Statamic + Nuxt + SSG + Cloudflare Pages combo we get easy development and nice, automated deployment. There’s no application server running to serve our front-end content, and so this helps limit our available windows for security vulnerabilities. Cloudflare Pages helps distribute our content and provides protection from DDOS attacks as well.

Our visitors benefit from this stack as well. All of the content pages are pre-rendered as HTML. Even a visitor with JavaScript disabled will be able to see the full content of our site. Pages, images, and CSS are on a CDN and get served quickly. This means both a good user experience as well as high scores from search engine crawlers, which take site performance into consideration for ranking.