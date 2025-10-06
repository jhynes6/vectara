---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/web-application-development/primevue-with-tailwind-40"
title: "Configuring PrimeVue to work with Tailwind 4.0"
domain: "gearboxgo.com"
path: "/articles/web-application-development/primevue-with-tailwind-40"
scraped_time: "2025-10-05T01:40:15.359134"
url_depth: 3
word_count: 459
client_name: "gearbox-solutions"
---

# Configuring PrimeVue to work with Tailwind 4.0

## Introduction

Tailwind 4 is now available, and there are a lot of new features.

PrimeVue has some tricks for integrating with Tailwind, and you need to make some updates to your PrimeVue and CSS configurations to get it to work with Tailwind 4.

## Upgrading Tailwind

First, follow the general [Tailwind 4 upgrade guide](https://tailwindcss.com/docs/upgrade-guide). This will get you most of the way. We recommend using their upgrade utility to fix some of the classes in your components which may need to be modified due to the class changes between Tailwind 3 and Tailwind 4. The `@tailwindcss/vite` plugin is also great to install.

Once you've gone through the guide you should have a modified `app.css` (or equivalent for your project) and your `tailwind.config.js` will have been removed. You'll now need to modify your `app.css` file and your `app.ts` to get your layers in the right order and have your classes apply correctly.

## Upgrading our PrimeVue configuration

### `app.css`

Remove the custom layer configurations and add the `tailwindcss` import and `tailwindcss-primeui` plugin

Old:

```css
@layer tailwind-base, primevue, tailwind-utilities;

@layer tailwind-base {
    @tailwind base;
}

@layer tailwind-utilities {
    @tailwind components;
    @tailwind utilities;
}
```

New:

```css
@import "tailwindcss";
@plugin "tailwindcss-primeui";
```

Next, change the `cssLayer.order` property in your theme configuration

### `app.ts`

Old:

```javascript
const app = createApp({ render: () => h(App, props) })
    .use(PrimeVue, {
        theme: {
            preset: customTheme,
            options: {
                cssLayer: {
                    name: "primevue",
                    order: "tailwind-base, primevue, tailwind-utilities",
                },
                darkModeSelector: ".dark",
            },
        },
    })
```

New:

```javascript
const app = createApp({ render: () => h(App, props) })
    .use(PrimeVue, {
        theme: {
            preset: customTheme,
            options: {
                cssLayer: {
                    name: "primevue",
                    order: "theme, base, primevue",
                },
                darkModeSelector: ".dark",
            },
        },
    })
```

## What do these changes actually do?

In the Tailwind 3 implementation we had some css layers which organized the PrimeVue css between the Tailwind layers. In the browser, it looks like this:

0: tailwind-base  
1: primevue  
2: tailwind-utilities

The `tailwind-base` layer contained the `@tailwind base` css from tailwind. The `tailwind-utilities` layer contained `@tailwind components` and `@tailwind utilities`. Tailwind 4 provides similar layers for us already. Our changes layer the PrimeVue CSS back in the same spot.

In the new Tailwind 4 with our updated configuration, our css layers now look like this:

0: base  
1: primevue  
2: theme  
3: components  
4: utilities

The new layer structure drops the primevue layer right in the middle of the Tailwind layers, exactly where we want it!

## Conclusion

This should get your PrimeVue CSS properly integrated with Tailwind 4! We hope that these instructions get you up and running quickly. Please contact us using the form at the bottom of this page if you'd like assistance with any of your PrimeVue projects.