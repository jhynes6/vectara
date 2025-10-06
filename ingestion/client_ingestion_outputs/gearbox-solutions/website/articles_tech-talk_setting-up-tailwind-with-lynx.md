---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/tech-talk/setting-up-tailwind-with-lynx"
title: "Setting up Tailwind with Lynx"
domain: "gearboxgo.com"
path: "/articles/tech-talk/setting-up-tailwind-with-lynx"
scraped_time: "2025-10-05T01:40:18.914861"
url_depth: 3
word_count: 418
client_name: "gearbox-solutions"
---

# Setting up Tailwind with Lynx

![Lynx](https://s3.us-east-1.amazonaws.com/assets.gearboxgo.com/lynx-tailwind.png)

[Lynx](https://lynxjs.org/) is a new web-stack-to-native mobile development platform by ByteDance, and with a little configuration can work very well with Tailwind. Let's get Tailwind set up with Lynx so we can use one of our favorite web dev tools for mobile development.

An easy way to get started is by following the Lynx Quick Start guide. This will get a basic UI up and running for you, and then we can add Tailwind to this configuration. We'll use the Quick Start demo app as a starting point for the instructions in this article, but you should be able to do similar configurations in any Lynx app.

### Install Tailwind

Lynx currently works best with Tailwind 3. Lynx interprets CSS for the purposes of rendering a UI, and not all CSS rules are supported. There are some Tailwind presets we'll be using to make sure it's compatible. These presets work for Tailwind 3, so that's what we'll be installing.

Install Tailwind 3, along with its additional dependencies, and run the tailwind init

```
pnpm install -D tailwindcss@3 postcss postcss-loader autoprefixer

npx tailwindcss init -p
```

### Add the Lynx Tailwind presets

You'll also need to install the Tailwind presets from the Lynx team, which will help make sure that the Tailwind rules are compatible.

```
pnpm install -D @lynx-js/tailwind-preset
```

Some people have had a better experience using the canary version of the tailwind preset. You can install this instead with `pnpm install -D @lynx-js/tailwind-preset-canary` or [check npmjs.com for the latest version](https://www.npmjs.com/package/@lynx-js/tailwind-preset-canary).

Add the Lynx Tailwind preset and configure your content directory in `tailwind.config.js`

```javascript
const lynxPreset = require('@lynx-js/tailwind-preset');

/** @type {import('tailwindcss').Config} */

export default {
  presets: [lynxPreset], // Use the preset
  content: ['./src/**/*.{html,js,ts,jsx,tsx}'],
};
```

### Add the Tailwind CSS directives

Add the Tailwind directives at the top of `src/App.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  background-color: #000;
  --color-text: #fff;
}
```

### Done

And that's it! We're ready to start using Tailwind in our Lynx project. This should work well for most of the Tailwind classes you'll want to use, and should appear instantly with the Lynx hot-reloading.

You should now be able to make Tailwind class changes in your layout files, like App.tsx, and see the changes appear immediately in the simulator.

Host your app with `pnpm run dev`, launch your device simulator, open the Lynx Explorer app, and open your layout. Add some Tailwind classes to `App.tsx` and save the files to see the changes.