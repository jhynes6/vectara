---
source: "website"
content_type: "blogs_resources"
url: "https://gearboxgo.com/articles/web-application-development/setting-up-sentry-with-nuxt-3"
title: "Setting up Sentry with Nuxt 3"
domain: "gearboxgo.com"
path: "/articles/web-application-development/setting-up-sentry-with-nuxt-3"
scraped_time: "2025-10-05T01:40:33.870637"
url_depth: 3
word_count: 966
client_name: "gearbox-solutions"
---

# Setting up Sentry with Nuxt 3

![Sentry with Nuxt 3](/_ipx/_/https:/s3.us-east-1.amazonaws.com/assets.gearboxgo.com/articles/nuxt-and-sentry.png)

### Introduction

Integrating Sentry with Nuxt 3 is a straightforward process which can be completed in only a few minutes. In this guide, we'll provide templates and instructions for setting up Sentry in your Nuxt 3 app. This configuration will work for both a regular Nuxt server deployment as well as static site generation (SSG).

### The setup process

#### 1. Create a project in Sentry

Before beginning the steps below you'll need to have your project set up in Sentry and your DSN configuration available. [Create a new project](https://gearbox.sentry.io/projects/new/) in Sentry and record your DSN, which Sentry will generate.

#### 2. Add the Sentry Vue package to your app

Sentry provides a package for error capture with Vue apps. We'll need to install this package using our package manager.

```
npm install @sentry/vue
```

#### 3. Run the Sourcemap Wizard

When Sentry captures errors it will be from your transpiled, minified code. This is better than nothing, but can be difficult to read and identify where the error occurred. To resolve this problem, we need to make sure that Sentry has the sourcemaps for our code available to match up when an error occurs.

Sentry provides a sourcemap wizard which will help to set this up in our project. It has a configuration for Vite, but not for Nuxt. We'll make some modifications to what the wizard does to make the configuration work for Nuxt.

Run the wizard by running:

```
npx @sentry/wizard@latest -i sourcemaps
```

Follow the instructions on the screen, going through the authentication and project selection. Be sure to select Vite as the bundler that you will be using. It will also ask if you have access to a Vite config file to make changes. You should answer "yes" to this question, though we don't actually have a vite file to work with.

The wizard will add a `vite.config.js` file for you. This file is not used by Nuxt, and instead we put the Vite configuration options in our `nuxt.config.ts` file. Delete the `vite.config.js` file which the wizard created automatically. We'll be adding the required configuration to our Nuxt config in the next step.

#### 4. Update Nuxt configuration

We'll want to be able to adjust the sampling and tracing which gets sent to the Sentry service using .env values. To make these values available though the app we'll need to add properties to the Nuxt config. We also need to update the Vite configuration through our Nuxt config to support sending sourcemaps to Sentry.

Add the properties in the example below to your `nuxt.config.ts` file.

```typescript
import { defineNuxtConfig } from "nuxt/config";
import { sentryVitePlugin } from "@sentry/vite-plugin";

// https://nuxt.com/docs/api/nuxt-config
export default defineNuxtConfig({
    runtimeConfig: {
        public: {
            // Config within public will be also exposed to the client
            SENTRY_DSN_PUBLIC: process.env.SENTRY_DSN_PUBLIC,
            SENTRY_TRACES_SAMPLE_RATE: parseFloat(process.env.SENTRY_TRACES_SAMPLE_RATE ?? '0'),
            SENTRY_REPLAY_SAMPLE_RATE: parseFloat(process.env.SENTRY_REPLAY_SAMPLE_RATE ?? '0'),
            SENTRY_ERROR_REPLAY_SAMPLE_RATE: parseFloat(process.env.SENTRY_ERROR_REPLAY_SAMPLE_RATE ?? '0'),
        },
    },
    sourcemap: true,
    vite: {
        plugins: [
            // Put the Sentry vite plugin after all other plugins
            sentryVitePlugin({
                authToken: process.env.SENTRY_AUTH_TOKEN,
                org: "gearbox",
                project: "abc-website-frontend",
            }),
        ],
    },
});
```

#### 5. Update .env

Next, update your `.env` file with the Sentry configuration values you want to use. This is an example configuration, but you can set the rates to whatever you wish for your environment. You'll probably want to remove or comment out the DSN value in your development environment to stop error reporting while you're doing development, but it will be important to have in your production environment.

```
SENTRY_TRACES_SAMPLE_RATE=.1
SENTRY_REPLAY_SAMPLE_RATE=0
SENTRY_ERROR_REPLAY_SAMPLE_RATE=1
SENTRY_DSN_PUBLIC=xxxxxxxxxxxxx
SENTRY_AUTH_TOKEN=xxxxxxxxxxxxx
```

#### 6. Create the Sentry plugin

Finally, create a new file in the plugins folder, which will be what configures the integration with Sentry throughout your Nuxt app. Copy and paste the code block below into a new `sentry.ts` file in your `/plugins` folder. This will create the new Sentry plugin, which Nuxt will auto-detect and load into your app.

```typescript
import * as Sentry from "@sentry/vue";

async function lazyLoadSentryIntegrations() {
    // don't load on server
    if (!process.client) return;

    const { Replay } = await import("@sentry/vue");
    Sentry.addIntegration(new Replay({
        maskAllText: false,
        blockAllMedia: false,
    }));
}

function getSentryIntegrations() {
    // don't load on server
    if (!process.client) return [];

    const router = useRouter();
    const browserTracing = new Sentry.BrowserTracing({
        routingInstrumentation: Sentry.vueRouterInstrumentation(router),
    });

    return [browserTracing];
}

export default defineNuxtPlugin({
    name: 'sentry',
    parallel: true,
    async setup(nuxtApp) {
        const vueApp = nuxtApp.vueApp;

        const config = useRuntimeConfig();

        Sentry.init({
            app: vueApp,
            dsn: config.public.SENTRY_DSN_PUBLIC ?? null,
            integrations: getSentryIntegrations(),

            // Set tracesSampleRate to 1.0 to capture 100%
            // of transactions for performance monitoring.
            // We recommend adjusting this value in production
            tracesSampleRate: config.public.SENTRY_TRACES_SAMPLE_RATE as number,

            // Set `tracePropagationTargets` to control for which URLs distributed tracing should be enabled
            // tracePropagationTargets: ["localhost", /^https:\/\/yourserver\.io\/api/],

            // This sets the sample rate. You may want this to be 100% while
            // in development and sample at a lower rate in production
            replaysSessionSampleRate: config.public.SENTRY_REPLAY_SAMPLE_RATE as number,

            // If the entire session is not sampled, use the below sample rate to sample
            // sessions when an error occurs.
            replaysOnErrorSampleRate: config.public.SENTRY_ERROR_REPLAY_SAMPLE_RATE as number,
        });

        // Lazy-load the replay integration to reduce bundle size
        lazyLoadSentryIntegrations();
    }
});
```

#### 7. Complete!

That should do it! Your Sentry integration should be all set and ready to go. Sourcemaps will be uploaded to Sentry automatically when `nuxi generate` or `nuxi build` are run.

This configuration uses lazy-loading to separate out the initialization of the Sentry Replay service. It's a fairly large package, so lazy-loading it helps keep the bundle size down and improves app initialization times. You can modify the `lazyLoadSentryIntegrations` function to configure other integrations which you would like to have lazy-loaded.

### Contact us to help with your project

At Gearbox, we love building great web apps with Vue and Nuxt. [Contact us](https://gearboxgo.com/#contact-form) if you'd like help with a project!