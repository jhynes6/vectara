---
source: "website"
content_type: "blogs_resources"
url: "https://parlant.io/docs/engine-internals/overview"
title: "/docs/engine-internals/overview"
domain: "parlant.io"
path: "/docs/engine-internals/overview"
scraped_time: "2025-09-08T19:58:51.430155"
url_depth: 3
word_count: 1307
---

Engine Overview | Parlant

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

*   [Engine Overview](/docs/engine-internals/overview)
*   [Conversation API](/docs/engine-internals/conversation-api)
*   [REST API Reference](/docs/api/create-agent)

*   [About Parlant](/docs/about)

*   [](/)
*   Engine Internals
*   Engine Overview

On this page

# Engine Overview

## Engine Overview[​](#engine-overview-1 "Direct link to Engine Overview")

In Parlant, the **Engine** is the part that's responsible for agent responses from end to end, where most of Parlant's logic and algorithms reside.

The engine is comprised of several key components, each one dedicated to a particular mission. As we will see, each of these missions assists in creating a well-guided response. At the same time, each of them is also quite complex in its own right.

While this article won't go into each specific component in detail, it will explain them briefly—just enough to understand how they function together to produce consistent responses.

## Main Components[​](#main-components "Direct link to Main Components")

There are currently 4 components to the engine:

1.  **Glossary Store**: Where domain-specific terms are stored
2.  **Guideline Matcher**: Filters matching guidelines for each response
3.  **Tool Caller**: Executes matched tool calls
4.  **Message Composer**: Tailors a suitable response message

Generally speaking, the Engine—normally activated by the API—utilizes all of these components when generating a response.

Each of these components acts as one part of the whole process of agent response. They are each designed to have a single responsibility in the process, and be independently optimizable, so that when something goes wrong we know exactly which part of the process to turn to and optimize.

Let's briefly consider each of them in its own right.

### Glossary Store[​](#glossary-store "Direct link to Glossary Store")

This component allows us to store and retrieve relevant terms and definitions that are specific to our business domain.

These terms, or more correctly, the most relevant among them at each particular point in the conversation, are loaded into the execution context and made available to each of the other components. This not only allows the agent to respond in a way that's grounded to your domain's terminology, but also allows you to _define guidelines that themselves speak your terminology._

In other words, the fetched glossary terms are imbued into all of the other components, to help them in accomplishing their task more accurately.

### Guideline Matcher[​](#guideline-matcher "Direct link to Guideline Matcher")

Before we explain this component, we first need to understand the motivation for its existence.

As you probably already know, behavior in Parlant is controlled primarily using guidelines, where each guideline is comprised of a _condition_ and an _action_. The condition is the part that specifies when the action should be followed.

Parlant takes advantage of this condition/action model to help the _Tool Caller_ and the _Message Composer_ stay focused, by only providing them with guidelines that are actually relevant for their current task. For example, if we have a guideline with the condition `the customer has just greeted you`, we do not need to account for the action of this guideline if we're already well into the conversation at this point—in which case it can just be ignored.

By avoiding such unneeded instructions, Parlant's engine improves the LLM's focus and accuracy and reduces the complexity to be handled by its supervision mechanism. It also lowers the cost and latency of the LLM's completions by eliminating unneeded tokens.

The Guideline Matcher is what accomplishes this reduction in complexity. It matches the appropriate guidelines that need to be activated in the processing of the agent's next response.

### Tool Caller[​](#tool-caller "Direct link to Tool Caller")

Instead of using a vendor-provided tool-calling API, Parlant implements its own tool-calling mechanism.

There are four important reasons for this:

1.  To support as many vendors as possible, including the ability to test other vendors and switch between them while maintaining the exact same user configuration.
2.  To support **guided tool calling,** i.e. calling a tool in the context of a specific set of guidelines which explain not just the "what" and "how" of calling the tool, but also the "why" and "when".
3.  To support multiple preparation iterations when working on a response; for example, where the first iteration matches relevant guidelines and runs tools and then, based on the output of the first iteration's tool calls, match a potentially different or wider set of guidelines, which may come with their own tool calls, and so forth. This allows you to specify guidelines freely and naturally, where their conditions can be met not just based on the conversation itself but also on data coming dynamically from tools. For more info on this, please refer to the [Optimization page](https://www.parlant.io/docs/advanced/optimization) on Parlant's docs site.
4.  To enable opportunistic processing optimizations by leveraging the additional guidance-related information Parlant has about tools.

The ToolCaller receives a list of tools—all of the tools that are associated with the currently-matched guidelines—decides which need to be called and how, and runs them, returning the results to the engine.

### Message Composer[​](#message-composer "Direct link to Message Composer")

Finally we come to the component that actually generates the response message (to be exact, it generates zero or more messages, as the case demands).

Essentially, everything up until the Message Composer's turn is considered a _preparation_ for the response—though this preparation may have already produced actions in the real world via tool calls. However, the customer doesn't know about it yet, because the agent still hasn't communicated anything about it (unless the tools themselves emitted messages).

The Message Composer is perhaps the most important component, where every other component basically aims to help it generate the most appropriate message possible.

It receives the relevant glossary terms, the matched guidelines for this particular state of the conversation, the tools that were just called (as well as interesting reasons why relevant or useful tools could not be called), and the entire interaction history. Its job is to further evaluate the matched guidelines in-context, prioritize what the customer needs to hear first in the very next message, and ensure that the guidelines are adhered to as reliably as possible, while at the same time continuing the conversation with the customer as naturally as possible.

## Response Lifecycle[​](#response-lifecycle "Direct link to Response Lifecycle")

Now that we have a basic understanding of what each engine component does, let's look at the lifecycle of a single response. This diagram is somewhat simplistic in terms of the actual architecture, but it does capture the essence of what's happening.

The response cycle is designed to allow us to [hook into it](/docs/advanced/engine-extensions) at various stages and control it with our own business logic (code), potentially replacing one of the components with our own implementation: say a fine-tuned SLM or an additional filter based on a BERT classifier.

[

Previous

Contributing to Parlant

](/docs/advanced/contributing)[

Next

Conversation API

](/docs/engine-internals/conversation-api)

*   [Engine Overview](#engine-overview-1)
*   [Main Components](#main-components)
*   [Glossary Store](#glossary-store)
*   [Guideline Matcher](#guideline-matcher)
*   [Tool Caller](#tool-caller)
*   [Message Composer](#message-composer)
*   [Response Lifecycle](#response-lifecycle)

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

Source code available on [GitHub](https:/