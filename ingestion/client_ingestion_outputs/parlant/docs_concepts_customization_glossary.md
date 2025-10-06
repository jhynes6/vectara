---
source: "website"
content_type: "other"
url: "https://parlant.io/docs/concepts/customization/glossary"
title: "/docs/concepts/customization/glossary"
domain: "parlant.io"
path: "/docs/concepts/customization/glossary"
scraped_time: "2025-09-08T19:59:50.986006"
url_depth: 4
word_count: 962
---

Glossary | Parlant

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
*   Glossary

On this page

# Glossary

## Glossary[​](#glossary-1 "Direct link to Glossary")

The glossary is a fundamental part of shaping your agent's understanding of its domain. It's like your agent's professional dictionary: a set of terms specific to your business or service context.

### When to Use the Glossary[​](#when-to-use-the-glossary "Direct link to When to Use the Glossary")

When you create an agent to handle specific tasks, it often needs to understand the unique vocabulary of your domain. For example, if your agent helps guests book rooms at the Boogie Nights hotel, it needs to know what "Boogie Nights" means in your context—in this case, that it's not just a movie title, but your hotel's name.

#### Creating Glossary Terms[​](#creating-glossary-terms "Direct link to Creating Glossary Terms")

Here's how to create a new glossary term:

await agent.create_term(    name=TERM,    description=DESCRIPTION,    synonyms=[SYNONYM_1, SYNONYM_2, ...],)

### Structure of Terms[​](#structure-of-terms "Direct link to Structure of Terms")

Each glossary entry consists of three components:

> *   **Term:** The word or phrase being defined
> *   **Description:** What this term means in your specific context
> *   **Synonyms:** Alternative ways users might refer to this term

For example:

await agent.create_term(    name="Boogie Nights",    description="Our luxury beachfront hotel located in Miami",    synonyms=["BN Hotel", "The Boogie", "Boogie Hotel"],)

### How Agents Use the Glossary[​](#how-agents-use-the-glossary "Direct link to How Agents Use the Glossary")

The glossary serves two crucial purposes in agent interactions.

First, it helps your agent understand customers better when they interact with it. When a guest says _"I'd like to stay at The Boogie,"_ the agent knows they're referring to your hotel.

Second, it helps the agent interpret your guidelines correctly. Consider the following configuration:

await agent.create_guideline(    condition="the user asks about Ocean View rooms",    action="explain the Sunrise Package benefits",)await agent.create_term(    name="Ocean View",    description="Our premium rooms on floors 15-20 facing the Atlantic",    synonyms=["seaside rooms", "beach view"],)await agent.create_term(    name="Sunrise Package",    description="Complimentary breakfast and early check-in for Ocean View bookings",    synonyms=["morning special", "sunrise special"],)

Here, both the condition as well as the action depend on the agent understanding what these terms mean.

If the Customer comes in and asks,

> **Customer:** I heard you have some rooms with a view to the Atlantic. What are those?

The agent can understand, based on the glossary term, that the condition _"the user asks about Ocean View rooms"_ is met, and it can then respond with the action _"explain the Sunrise Package benefits"_.

![get-in-touch](/img/get-in-touch-button-icon.svg)Questions? Reach out!

## Glossary vs Guidelines vs Agent Description[​](#glossary-vs-guidelines-vs-agent-description "Direct link to Glossary vs Guidelines vs Agent Description")

Each component serves a distinct purpose in shaping your agent's behavior:

1.  The Glossary teaches your agent "what things are". For example, _"A Club Member is a guest who has stayed with us more than 5 times."_ You can have as many terms as you want.
2.  Guidelines teach your agent "how to act in situations". For example, _"When speaking with Club Members, acknowledge their loyalty status."_ You can have as many guidelines as you want.
3.  Agent Description provides overall context and personality. For example, _"You are a helpful hotel booking assistant for Boogie Nights."_ The agent's description is static and limited.

Think of it this way: the glossary builds your agent's vocabulary, guidelines shape its behavior, and the agent description sets its overall context, role, personality and tone.

## Glossary vs Tools[​](#glossary-vs-tools "Direct link to Glossary vs Tools")

While both glossary terms and tools help your agent understand your domain, they serve fundamentally different purposes. The glossary provides static knowledge, while tools enable dynamic data access.

Consider a hotel booking scenario:

**Glossary Term:**

> *   **Term:** Club Member
> *   **Description:** A guest who has stayed with us more than 5 times
> *   **Synonyms:** loyal guest, regular guest

**Tool:** `check_member_status(user_id) # Returns current stay count and benefits`

The glossary term provides a consistent definition of what a Club Member is, while the tool can check a specific user's actual status in your database. Similarly:

**Glossary Term:**

> *   **Term:** Ocean View Room
> *   **Description:** Premium rooms on floors 15-20 facing the Atlantic
> *   **Synonyms:** seaside room, beach view

**Tool:** `check_room_availability(room_type, dates) # Returns current availability and rates`

The glossary helps your agent understand what an Ocean View Room is, while the tool provides real-time information about specific rooms' availability and pricing.

This separation between static knowledge (glossary) and dynamic data access (tools) helps create clear, maintainable agent implementations that can handle both general inquiries and specific, data-driven interactions.

![get-in-touch](/img/get-in-touch-button-icon.svg)Reach out for assistance

[

Previous

Retrievers

](/docs/concepts/customization/retrievers)[

Next

Variables

](/docs/concepts/customization/variables)

*   [Glossary](#glossary-1)
*   [When to Use the Glossary](#when-to-use-the-glossary)
*   [Structure of Terms](#structure-of-terms)
*   [How Agents Use the Glossary](#how-agents-use-the-glossary)
*   [Glossary vs Guidelines vs Agent Description](#glossary-vs-guidelines-vs-agent-description)
*   [Glossary vs Tools](#glossary-vs-tools)

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

Source code available on [GitHub](https://github.com/