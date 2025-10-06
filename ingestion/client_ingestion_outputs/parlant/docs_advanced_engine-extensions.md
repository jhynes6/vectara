---
source: "website"
content_type: "other"
url: "https://parlant.io/docs/advanced/engine-extensions"
title: "/docs/advanced/engine-extensions"
domain: "parlant.io"
path: "/docs/advanced/engine-extensions"
scraped_time: "2025-09-08T19:59:03.464077"
url_depth: 3
word_count: 1255
---

Engine Extensions | Parlant

[Skip to main content](#__docusaurus_skipToContent_fallback)

[Introducing Parlant 3.0](/blog/parlant-3-0-release)

— our most significant overhaul.

Dismiss

[

![Parlant's logo](/logo/logo-full.png)![Parlant's logo](/logo/logo-full.png)

](/)

Docs

[Install](/docs/quickstart/installation)[Learn](/docs/quickstart/motivation)[Blog](/blog)[About](/docs/about)[Need Help?](/contact)

![](/img/icons/search.svg)

![](/img/icons/search.svg)Search

![](/img/icons/menu.svg)

[![](/img/icons/x.svg)](https://x.com/EmcieCo)[![](/img/icons/discord.svg)](https://discord.gg/duxWqxKk6J)

[![github](/img/icons/github.svg)**Star**](https://github.com/emcie-co/parlant)[**\--**](https://github.com/emcie-co/parlant)

* * *

* * *

[

![Parlant's logo](/logo/logo-full.png)![Parlant's logo](/logo/logo-full.png)

](/)

*   [Install](/docs/quickstart/installation)
*   [Learn](/docs/quickstart/motivation)
*   [Blog](/blog)
*   [About](/docs/about)
*   [Need Help?](/contact)

* * *

[![](/img/icons/x.svg)](https://x.com/EmcieCo)[![](/img/icons/discord.svg)](https://discord.gg/duxWqxKk6J)

*   [Quick Start](/docs/quickstart/installation)

*   [Installation](/docs/quickstart/installation)
*   [Motivation](/docs/quickstart/motivation)
*   [Healthcare Agent Example](/docs/quickstart/examples)
*   [Components](/docs/concepts/sessions)

*   [Sessions](/docs/concepts/sessions)
*   [Entities](/docs/concepts/entities/agents)

*   [Agents](/docs/concepts/entities/agents)
*   [Customers](/docs/concepts/entities/customers)
*   [Behavior Modeling](/docs/concepts/customization/journeys)

*   [Journeys](/docs/concepts/customization/journeys)
*   [Guidelines](/docs/concepts/customization/guidelines)
*   [Relationships](/docs/concepts/customization/relationships)
*   [Tools](/docs/concepts/customization/tools)
*   [Retrievers](/docs/concepts/customization/retrievers)
*   [Glossary](/docs/concepts/customization/glossary)
*   [Variables](/docs/concepts/customization/variables)
*   [Canned Responses](/docs/concepts/customization/canned-responses)
*   [Production](/docs/category/production)

*   [Agentic Design Methodology](/docs/production/agentic-design)
*   [User-Input Moderation](/docs/production/input-moderation)
*   [Human Handoff](/docs/production/human-handoff)
*   [API Hardening](/docs/production/api-hardening)
*   [Custom Frontend](/docs/production/custom-frontend)
*   [Advanced Topics](/docs/advanced/engine-extensions)

*   [Engine Extensions](/docs/advanced/engine-extensions)
*   [Custom NLP Models](/docs/advanced/custom-llms)
*   [Enforcement & Explainability](/docs/advanced/explainability)
*   [Contributing to Parlant](/docs/advanced/contributing)
*   [Engine Internals](/docs/engine-internals/overview)

*   [REST API Reference](/docs/api/create-agent)

*   [About Parlant](/docs/about)

*   [](/)
*   Advanced Topics
*   Engine Extensions

On this page

# Engine Extensions

## Engine Extensions[​](#engine-extensions-1 "Direct link to Engine Extensions")

Working with an external framework and adapting it to your needs isn’t always simple, especially when you need it to behave in ways its original design didn’t anticipate. Modifying the framework’s source code is a treacherous path—not just because it requires deeper expertise, but also because it leads to divergences between your locally-modified version and upstream updates.

So how do you get a pre-built framework to work differently? The idea is to be able to run a system or software that includes your code customizations without breaking its fundamental assumptions.

The [Open/Closed Principle](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle) states that software should be open for extension, but closed for modification, such that it can allow its behavior to be extended without modifying its source code. Parlant is carefully designed to abide by this principle, allowing you to achieve extreme extensibility by hooking into its structure.

With extensions, you are free to build exactly what you need without waiting for updates or modifying core engine components. This is a good time to remind you that you can join our [Discord](https://discord.gg/duxWqxKk6J) community to ask questions.

![get-in-touch](/img/get-in-touch-button-icon.svg)Reach out for assistance

## Engine Hooks[​](#engine-hooks "Direct link to Engine Hooks")

Every time an agent needs to respond to a customer, the engine goes through a series of steps to generate the response. You can hook into these steps to modify the behavior of the engine. This is easily done by registering hook functions.

While there are many hooks you can utilize, here's a simple example that:

1.  Overrides the entire engine's response generation process if we detect that the customer only greeted the agent.
2.  Inspects the agent's message for compliance breaches (using a custom checker) before sending it to the customer.

import asynciofrom typing import Anyimport parlant.sdk as pasync def intercept_message_generation_with_greeting(    ctx: p.LoadedContext, payload: Any, exc: Exception | None) -> p.EngineHookResult:    if await is_only_greeting(ctx.interaction.last_customer_message):        await ctx.session_event_emitter.emit_message_event(            correlation_id=ctx.correlator.correlation_id,            data="Hello! How can I help you today?",        )        return p.EngineHookResult.BAIL  # Intercept the rest of the process    else:        return p.EngineHookResult.CALL_NEXT  # Continue with the normal processasync def check_message_compliance(    ctx: p.LoadedContext, payload: Any, exc: Exception | None) -> p.EngineHookResult:    generated_message = payload    if not await is_compliant(generated_message):        ctx.logger.warning(f"Prevented sending a non-compliant message: '{generated_message}'.")        return p.EngineHookResult.BAIL  # Do not send this message    return p.EngineHookResult.CALL_NEXT  # Continue with the normal processasync def configure_hooks(hooks: p.EngineHooks) -> p.EngineHooks:    hooks.on_acknowledged.append(intercept_message_generation_with_greeting)    hooks.on_message_generated.append(check_message_compliance)    return hooksasync def main():    async with p.Server(        configure_hooks=configure_hooks,    ) as server:        # Your logic here        ...

![get-in-touch](/img/get-in-touch-button-icon.svg)Get help with hooks

## Dependency Injection[​](#dependency-injection "Direct link to Dependency Injection")

In order to extend the engine without modifying its source code, Parlant uses a [dependency injection](https://en.wikipedia.org/wiki/Dependency_injection) system. This allows you to inject your own implementations of various components or even the processing engine itself (say, if you wanted to optimize the entire pipeline for particular use cases).

For simplicity, we'll take a look at some basic extension mechanics, as well as common use cases for extension.

However, if you need help with something that isn't covered here, please reach out to us on [Discord](https://discord.gg/duxWqxKk6J), [GitHub Discussions](https://github.com/emcie-co/parlant/discussions), or simply using the [Contact Page](https://parlant.io/contact) and we'll get back to you.

### Working with the Container[​](#working-with-the-container "Direct link to Working with the Container")

Let's see how to work with Parlant's dependency injection container. The container is a central place where all components are registered, and you can use it to retrieve or register your own components.

There are two things you might want to do with respect to the container:

1.  **Register your own components**: You can add your own implementations of various components to the container, making them available for injection throughout the application.
2.  **Adjust the behavior of existing components**: You can retrieve instances of components from the container, allowing you to use them in your own code.

#### Registering Components[​](#registering-components "Direct link to Registering Components")

Registering components lets you override nearly every aspect of how Parlant works. You can access the container during its registration phase by passing a `configure_container` hook to the server.

This hook accepts a baseline state of the container, and returns a modified version of it before the server starts.

import asyncioimport parlant.sdk as pasync def configure_container(container: p.Container) -> p.Container:    # Register your own components here    # ...    return containerasync def main():    async with p.Server(        configure_container=configure_container,    ) as server:        # Your logic here        ...

#### Adjusting Existing Components[​](#adjusting-existing-components "Direct link to Adjusting Existing Components")

If you want to adjust the behavior of built-in components, you can retrieve them from the container and modify their behavior. This is useful for debugging or extending existing functionality without replacing the entire component.

This hook is called `initialize_container`, and it allows you to modify components within the container after all of the classes have been registered and determined—but before the server actually starts to use them.

This hook accepts the final state of the container, and returns `None`, as the container is only provided for _accessing_ registered components.

import asyncioimport parlant.sdk as pasync def initialize_container(container: p.Container) -> None:    # Register your own components here    # ...    return containerasync def main():    async with p.Server(        configure_container=configure_container,    ) as server:        # Your logic here        ...

![get-in-touch](/img/get-in-touch-button-icon.svg)Need help? Reach out!

## Open for Extension[​](#open-for-extension "Direct link to Open for Extension")

If you read or debug Parlant code, you'll come across many different types of components within the engine. Using the configuration and initialization hooks, you now know how to access them and extend, modify, or completely override their implementations as needed.

#### Common Use Cases for Extensions[​](#common-use-cases-for-extensions "Direct link to Common Use Cases for Extensions")

1.  Overriding the no-match behavior of canned responses. This is actually documented here: [Canned Responses](/docs/concepts/customization/canned-responses#no-match-responses).
2.  Wrapping any engine component to add logging, monitoring, or other cross-cutting concerns.
3.  Overriding the way particular guidelines are evaluated. For example, if they are simple and you have enough data, you can evaluate them with custom-trained BERT models instead of going through an LLM.
4.  Overriding the entire message generation component, allowing you to leverage Parlant's guideline matching and tool execution, but using your message generation logic.

But there's much more you can do. The engine is designed to be flexible and extensible, so you can adapt it to your specific needs without modifying the core codebase.

![get-in-touch](/img/get-in-touch-button-icon.svg)Help me ramp up

[

Previous

Custom Frontend

](/docs/production/custom-frontend)[

Next

Custom NLP Models

](/docs/advanced/custom-llms)

*   [Engine Extensions](#engine-extensions-1)
*   [Engine Hooks](#engine-hooks)
*   [Dependency Injection](#dependency-injection)
*   [Working with the Container](#working-with-the-container)
*   [Open for Extension](#open-for-extension)

![Parlant's logo](/logo/logo-full-white.svg)![Parlant's logo](/logo/logo-full-white.svg)

[![GitHub](/img/icons/github-rounded.svg)](https://github.com/emcie-co/parlant)[![Discord](/img/icons/discord-rounded.svg)](https://discord.gg/duxWqxKk6J)[![X](/img/icons/x-rounded.svg)](https://x.com/EmcieCo)[![LinkedIn](/img/icons/linkedin-rounded.svg)](https://linkedin.com/company/emcie/posts/?feedView=all)[![YouTube](/img/icons/youtube-rounded.svg)](https://www.youtube.com/channel/UCmUiKJfCnLage9RhywiiUTw)

2025 parlant

[

Privacy Policy

](/privacy-policy)

Community

*   [GitHub](https://github.com/emcie-co/parlant)
*   [Discord](https://discord.gg/duxWqxKk6J)
*   [X (Twitter)](https://x.com/EmcieCo)

a

Copyright 2025 [Emcie](https://emcie.co).

Licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).

Source code available on [GitHub](https://g