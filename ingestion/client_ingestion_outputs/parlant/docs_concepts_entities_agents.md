---
source: "website"
content_type: "other"
url: "https://parlant.io/docs/concepts/entities/agents"
title: "/docs/concepts/entities/agents"
domain: "parlant.io"
path: "/docs/concepts/entities/agents"
scraped_time: "2025-09-08T20:00:17.040776"
url_depth: 4
word_count: 1054
---

Agents | Parlant

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
*   Entities
*   Agents

On this page

# Agents

## Agents[​](#agents-1 "Direct link to Agents")

In Parlant, an agent is a customized AI personality that interacts with customers as a single, competent entity. It is essentially, "the one you talk to", as opposed to some frameworks where an agent is a specialized task function.

Agents form the basic umbrella of conversational customization—all behavioral configurations affect agent behavior.

import parlant.sdk as pasync with p.Server() as server:    hexon = await server.agents.create(        name="Hexon",        description="Technical support specialist"    )    # Continue to model the agent's behavior using guidelines, journeys, etc....

info

Note that a single Parlant server may host multiple agents, each with distinct roles and personalities.

Each agent can be uniquely configured with its own style, demeanor, and interaction patterns tailored to its target users. More importantly, different business units can own and maintain their specific agents. For example:

*   IT Department manages **Hexon**
*   Customer Success team oversees **Sprocket**
*   Sales/Marketing controls **Piston**

This agent-based design creates natural boundaries for separation of concerns within Parlant

### Crafting an Agent's Identity[​](#crafting-an-agents-identity "Direct link to Crafting an Agent's Identity")

Imagine you're creating a new employee who will become the voice of your service. Just as you'd carefully consider the personality and approach of a human hire, crafting an agent's identity ultimately requires thoughtful consideration of its core characteristics—and, like any good hire, you can grow and adapt it based on real-world feedback.

As an example, let's follow the possible evolution of **Hexon**, our technical support specialist. In its first iteration, we might simply define it as "a technical support agent who helps users solve technical problems professionally and efficiently." After observing some interactions, we might notice that it comes across as too mechanical, failing to build trust with users.

So we refine its identity:

> "A technical support specialist who combines deep technical knowledge with patient explanation. You take pride in making complex concepts accessible without oversimplifying them. While you're always professional, you communicate with a warm, approachable tone. You believe that every technical issue is an opportunity to help users better understand their tools. When users are frustrated, you remain calm and empathetic, acknowledging their challenges while focusing on solutions."

As we observe more interactions, we might further refine this general identity. Perhaps we notice users respond better when Hexon shows more personality, or maybe we find certain technical discussions need more gravitas. The identity can evolve with these insights.

The key is to start with an identity that gives the agent its basic orientation, but remain open to refinement based on real interactions. Watch how users respond to the agent's mannerisms. Gather feedback from stakeholders. Adjust the identity accordingly.

### A Single Agent or Multiple Agents?[​](#a-single-agent-or-multiple-agents "Direct link to A Single Agent or Multiple Agents?")

There's a frequent debate on whether to model user-facing agents as a single agent or multi-agent system. Parlant's position is a mix of both.

Generally speaking, managing complexity is easier when our solutions model the real world, because it makes us naturally have much more data with which to reason about design decisions, rather than trying to come up with something contrived. So instead of asking a very fundamental, "How should users interact with this agent?" we can instead ask something much more fruitful, like, "What would user expect based on their real-life experience?"

In practice, when we interact with human service representatives, there are certain expectations we've come to have from such experiences:

*   If we're talking to an agent, they have the full context of our conversation. They're coherent. They don't suddenly just forget or unexpectedly change their interpretation of the situation.
*   The agent we're talking to may not always be able to help us with everything. We may need to be transferred to another agent who specializes in some topic.
*   We expect to be notified of such transfers. If they happen suddently or without our awareness, we take that as a careless customer experience.

You can see how insights from familiar, real-world usage patterns help us arrive at informed design decisions. By modeling agent interactions on real-world patterns, we not only better understand what outcomes to strive for, but it turns out that managing our agents' configuration becomes easier to reason about, too.

This is why Parlant's formal recommendation is to model AI agents after how human agents work. In other words, if you can see it being a single personality in a real-life use case, that means it should be represented as a single AI agent in Parlant. Incidentally, Parlant's filtration of relevant elements of the agent's conversation model allow you to manage quite a lot of complexity in a single agent, so you don't need to adopt a multi-agent approach if that was your concern.

The Failures of Multi-Agent Systems

There's an interesting paper on the [failures of multi-agent systems](https://arxiv.org/abs/2503.13657#:~:text=We%20present%20MAST%20%28Multi-Agent%20System%20Failure%20Taxonomy%29%2C%20the,over%20200%20tasks%2C%20involving%20six%20expert%20human%20annotators), despite their promise of modularity and specialization. It highlights how multi-agent systems often struggle with coordination, communication, and consistency, leading to unexpected behaviors and failures. This aligns with Parlant's approach of using a single agent to maintain coherence and context in conversations.

![get-in-touch](/img/get-in-touch-button-icon.svg)Book a consultation

[

Previous

Sessions

](/docs/concepts/sessions)[

Next

Customers

](/docs/concepts/entities/customers)

*   [Agents](#agents-1)
*   [Crafting an Agent's Identity](#crafting-an-agents-identity)
*   [A Single Agent or Multiple Agents?](#a-single-agent-or-multiple-agents)

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

Source code available on [GitHub](https://github.com/emcie-