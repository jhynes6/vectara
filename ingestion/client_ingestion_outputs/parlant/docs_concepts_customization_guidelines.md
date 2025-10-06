---
source: "website"
content_type: "blogs_resources"
url: "https://parlant.io/docs/concepts/customization/guidelines"
title: "/docs/concepts/customization/guidelines"
domain: "parlant.io"
path: "/docs/concepts/customization/guidelines"
scraped_time: "2025-09-08T19:59:29.479852"
url_depth: 4
word_count: 1848
---

Guidelines | Parlant

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
*   Components
*   Behavior Modeling
*   Guidelines

On this page

# Guidelines

## Guidelines[​](#guidelines-1 "Direct link to Guidelines")

Guidelines are a powerful customization feature. While they're quite simple in principle, there is a lot to say about them.

### What Are Guidelines?[​](#what-are-guidelines "Direct link to What Are Guidelines?")

Guidelines are the primary way to nudge the behavior of [agents](/docs/concepts/entities/agents) in Parlant in a contextual and targeted manner.

They allow us to instruct how an agent should respond in specific situations, overriding its default behavior, thus ensuring that its behavior aligns with our expectations and business needs.

Guidelines allow us to shape an [agent](/docs/concepts/entities/agents)'s behavior in two key scenarios:

1.  When certain out-of-the-box responses don't meet our expectations
2.  When we simply want to ensure consistent behavior across all interactions

Guidelines vs. Journeys

Journeys are the ideal way to provide a structured, step-by-step interaction flow, while guidelines are more about providing contextual nudges to the agent's behavior. Use journeys for complex interactions that require multiple steps, and guidelines for simpler, context-specific adjustments—as well as for simple, general tool-calling triggers that aren't necessarily within any particular journey.

#### Example[​](#example "Direct link to Example")

Suppose we have an agent that helps customers order products. By default, the agent's behavior might look like this:

> **User:** I'd like to order a new laptop.
>
> **Agent:** Sure, what are your preferences? (e.g., budget, operating system, screen size, use cases?)

But say we want to make our agent more personable by first having it ask simply whether they want Mac or Windows. We can add a guideline to ensure that this happens consistently, like so:

await agent.create_guideline(    condition="The customer wants to buy a laptop",    action="First, determine whether they prefer Mac or Windows")

Resulting in a conversation like this:

> **User:** I'd like to order a new laptop.
>
> **Agent:** Sounds good. Would you prefer Mac or Windows?

Careful What You Wish For

Instructing an LLM is very similar to instructing a human, except that by default it has absolutely zero context of who is instructing it and the context in which the instruction is given. For this reason, when we provide guidelines, we must strive to be as clear and articulate as possible, so that the agent can follow them without ambiguity. More about this later in this page.

### The Structure of Guidelines[​](#the-structure-of-guidelines "Direct link to The Structure of Guidelines")

In Parlant, each guideline is composed of two parts: the **condition** and the **action**.

1.  The **action** part describes what the guideline should accomplish. For example, "Offer a discount."
2.  The **condition** is the part the specifies _when the action should take place_. For example, "It is a holiday".

await agent.create_guideline(    condition="It is a holiday",    action="Offer a discount on the order")

When speaking informally about guidelines, we often describe them in _when/then_ form: When <CONDITION>, Then <ACTION>, or in this case, When it is a holiday, Then offer a discount.

Guideline Tracking

Once the action is accomplished in a session, Parlant will deactivate the guideline—unless it has reason to believe the action should re-apply due to a contextual shift (e.g., in the example above, if the customer starts another order).

### Using Tools[​](#using-tools "Direct link to Using Tools")

One of the foremost issues with most LLMs is their bias toward false-positives. Put simply, they are always looking to please, so they will tend to answer positively to most questions.

This becomes a huge problem when we want to ensure that an agent only performs certain actions when it has the right context or information.

For this reasons, Parlant allows us to associate [tools](/docs/concepts/customization/tools) (essentially, functions) with guidelines, such that the agent would only consider calling a tool when a guideline's requisite condition is met within the interaction's current context.

Just as importantly, it also allows you to specify contextual information on _how_ and _why_ you want a particular tool to be called when certain circumstances hold. Here's an example:

@p.toolasync def find_products_in_stock(context: p.ToolContext, query: str) -> p.ToolResult:  ...await agent.create_guideline(    condition="The customer asks about the newest laptops",    action="First recommend the latest Mac laptops",    # The guideline's action will ensure the following tool is    # called with the right query (e.g., "Latest Mac laptops")    tools=[find_products_in_stock],)

## How Guidelines Work[​](#how-guidelines-work "Direct link to How Guidelines Work")

To understand how guidelines work, we need to look briefly at Parlant's response processing pipeline.

When an agent receives a message, it goes through a response processing pipeline that involves several steps to ensure the response is aligned with the guidelines and expectations.

As the figure above suggests, guidelines are evaluated and matched _before_ the agent composes its response.

Keep in Mind

This means that the agent needs to be able to evaluate and apply instructions and tool calls based on the interaction's context _before_ generating the response. In other words, guidelines such as "Do X immediately after you've done Y" may not work as you expect.

![get-in-touch](/img/get-in-touch-button-icon.svg)Questions? Reach out!

### How Parlant Uses Guidelines[​](#how-parlant-uses-guidelines "Direct link to How Parlant Uses Guidelines")

LLMs are a magnificent creation, built on the principle of [statistical attention](https://arxiv.org/abs/1706.03762) in text; yet, their attention span is painfully finite. When it comes to following instructions, they need help.

Behind the scenes, Parlant ensures that agent responses are aligned with expectations by dynamically managing the LLM's context to only include the relevant guidelines at each point.

Before each response, Parlant only loads the guidelines that are relevant to the conversation's current state. This dynamic management keeps the LLM's "cognitive load" minimal, maximizing its attention and, consequently, the alignment of each response with expected behavior.

info

Another important ability that Parlant employs to ensure alignment is supervising the agent's outputs before they reach the [customer](/docs/concepts/entities/customers), to ensure to the utmost degree that guidelines were correctly adhered to. To achieve this, NLP researchers working on Parlant have devised an innovative prompting technique called **Attentive Reasoning Queries (ARQs)**. You're welcome to explore the research paper on [arxiv.org, Attentive Reasoning Queries: A Systematic Method for Optimizing Instruction-Following in Large Language Models](https://arxiv.org/abs/2503.03669#:~:text=We%20present%20Attentive%20Reasoning%20Queries%20%28ARQs%29%2C%20a%20novel,in%20Large%20Language%20Models%20through%20domain-specialized%20reasoning%20blueprints.)

### Managing Guidelines[​](#managing-guidelines "Direct link to Managing Guidelines")

Parlant is built to make guideline management as simple as possible.

Often, guidelines are added when business experts request behavioral changes in the agent. Developers can use Parlant to make those changes, iterating quickly and reliably, at the pace of the business experts they're working with.

Here's a practical example. When Sales requests: "The agent should first ask about the customer's needs and pain points before discussing our solution," implementing this feedback takes just a minute by adding the following:

await agent.create_guideline(  condition="The customer has yet to specify their current pain points",  action="Seek to understand their pain points before talking about our solution")

Once added, Parlant takes care of the rest, automatically ensuring this new guideline is followed consistently across all relevant conversations, without degrading your agent's conformance to other guidelines.

### Formulating Guidelines[​](#formulating-guidelines "Direct link to Formulating Guidelines")

Think of an LLM as a highly knowledgeable stranger who's just walked into your business. They might have years of general experience, but they don't know your specific context, preferences, or way of doing things. Yet, this stranger is eager to help and will always try to—even when uncertain.

This is where guidelines come in. They're your way of channeling this endless enthusiasm and broad knowledge into focused, appropriate responses.

But specifying effective guidelines is a bit of an art—just like it is with people.

#### The Art of Guidance[​](#the-art-of-guidance "Direct link to The Art of Guidance")

Consider a customer service scenario. As a very naive example, we might be tempted to have:

DON'T

> *   **Condition:** Customer is unhappy
> *   **Action:** Make them feel better

While well-intentioned, this is an example of a guideline that is just too vague. The LLM might interpret this in countless ways, from offering discounts it can't actually provide to making jokes that might be inappropriate for your brand. Instead, consider:

DO

> *   **Condition:** Customer expresses dissatisfaction with our service
> *   **Action:** Acknowledge their frustration specifically, express sincere empathy, and ask for details about their experience so we can address it properly.

Notice how this guideline is both specific and bounded.

DON'T

> *   **Condition:** Customer asks about products
> *   **Action:** Recommend something they might like

DO

> *   **Condition:** Customer asks for product recommendations without specifying preferences
> *   **Action:** Ask about their specific needs, previous experience with similar products, and any particular features they're looking for before making recommendations

#### Finding the Right Balance[​](#finding-the-right-balance "Direct link to Finding the Right Balance")

In principle, we're looking for guidelines that are "just right"—neither over nor under specified. Consider these iterations for a technical support agent:

DON'T

Too vague:

> *   **Condition:** Customer has a technical problem
> *   **Action:** Help them fix it

DON'T

Too rigid:

> *   **Condition:** Customer reports an error message
> *   **Action:** First ask for their operating system version, then their browser version, then their last system update date

DO

Just right:

> *   **Condition:** Customer reports difficulty accessing our platform
> *   **Action:** Express understanding of their situation, ask for key details about their setup (OS and browser), and check if they've tried some concrete troubleshooting steps

Remember, LLMs will usually take your guidance quite literally. If you tell your agent to "always suggest premium features," it might do so even when talking to a customer who's complaining about pricing. Always try to consider the broader context and potential edge cases when formulating your guidelines. It'll pay off in less changes and trouleshooting down the line.

**If in doubt, prefer to err on the side of vagueness.** The goal of Agentic Behavior Modeling isn't to script out every possible interaction but to provide clear, contextual guidance that shapes the LLM's natural generalization abilities into reliable, appropriate responses for your specific use case.

[

Previous

Journeys

](/docs/concepts/customization/journeys)[

Next

Relationships

](/docs/concepts/customization/relationships)

*   [Guidelines](#guidelines-1)
*   [What Are Guidelines?](#what-are-guidelines)
*   [The Structure of Guidelines](#the-structure-of-guidelines)
*   [Using Tools](#using-tools)
*   [How Guidelines Work](#how-guidelines-work)
*   [How Parlant Uses Guidelines](#how-parlant-uses-guidelines)
*   [Managing Guidelines](#managing-guidelines)
*   [Formulating Guidelines](#formulating-guidelines)

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

Source code available on [GitHub](htt