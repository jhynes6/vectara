---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/web-application-development/nuxt-3-and-cloudflare-pages-failed-build-output-directory-contains-links-to-files-that-can-t-be-accessed"
title: "Nuxt 3 and CloudFlare Pages Deployment Issue"
domain: "gearboxgo.com"
path: "/articles/web-application-development/nuxt-3-and-cloudflare-pages-failed-build-output-directory-contains-links-to-files-that-can-t-be-accessed"
scraped_time: "2025-10-05T01:39:25.211731"
url_depth: 3
word_count: 225
client_name: "gearbox-solutions"
---

# Nuxt 3 and CloudFlare Pages - Failed: build output directory contains links to files that can't be accessed

![](/_ipx/_/https:/s3.us-east-1.amazonaws.com/assets.gearboxgo.com/nuxt-and-cloudflare-error.png)

We recently ran into a new issue with deploying our Nuxt 3 app on CloudFlare Pages. All of our builds, including previously successful builds, started getting a new error message:

> Failed: build output directory contains links to files that can't be accessed

The generate process would run successfully, but we'd get this error at the very end.

The cause of this appears to be an issue with a linked directory in the default Nuxt configuration in CloudFlare pages. If you follow the setup instructions for Nuxt or go with the default build configuration, CloudFlare will attempt to copy the `/dist` directory as the source of your static site.

The `/dist` folder is actually an alias of `/.output/public`, which is the true location of your statically generated content. For whatever reason, this alias is not created in the build process or CloudFlare Pages' deploy process can't handle the alias correctly.

The solution to this is to update your build configuration to use the `/.output/public` directory directly.

To change this, go to your Pages project, then to the settings tab. From there, go to Builds & deployments and update the "Build output directory option" to be `/.output/public`.

Re-run your deploy and you should be all set!