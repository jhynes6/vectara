---
source: "website"
content_type: "blogs_resources"
url: "https://parlant.io/docs/advanced/explainability"
title: "/docs/advanced/explainability"
domain: "parlant.io"
path: "/docs/advanced/explainability"
scraped_time: "2025-09-08T20:00:11.442496"
url_depth: 3
word_count: 744
---

Enforcement & Explainability | Parlant

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
*   Enforcement & Explainability

On this page

# Enforcement & Explainability

## Enforcement & Explainability[​](#enforcement--explainability-1 "Direct link to Enforcement & Explainability")

Let's dive into how Parlant enforces the conversation model consistently and provides visibility into your agent's situational understanding and decision-making process.

In this section, you'll learn:

1.  How _Attentive Reasoning Queries (ARQs)_ enforce the conversation model
2.  How to use ARQ artifacts to troubleshoot and improve behavior

### Understanding Runtime Enforcement[​](#understanding-runtime-enforcement "Direct link to Understanding Runtime Enforcement")

During message generation, Parlant ensures guidelines are followed consistently in real-time conversations through our [Attentive Reasoning Queries](https://arxiv.org/abs/2503.03669#:~:text=We%20present%20Attentive%20Reasoning%20Queries%20%28ARQs%29%2C%20a%20novel,in%20Large%20Language%20Models%20through%20domain-specialized%20reasoning%20blueprints.) prompting method. Rather than simply adding guidelines to prompts and hoping for the best, Parlant employes explicit techniques to maximize the LLM's ability and likelihood to adhere to your guidelines.

Attentive Reasoning Queries (ARQs) are essentially structured reasoning blueprints built into prompts that guide LLMs through specific thinking patterns when making decisions or solving problems. Rather than hoping an AI agent naturally considers all important factors, ARQs explicitly outline reasoning steps for different domains—like having specialized mental checklists to go through.

What makes ARQs effective for behavioral enforcement is that they force attention on critical considerations that might otherwise be overlooked. The model must work through predetermined reasoning stages (like context assessment, solution exploration, critique, and decision formation), ensuring it consistently evaluates important constraints before taking action.

![ARQs](https://arxiv.org/html/2503.03669v1/x1.png)

**Figure:** Illustration of ARQs (taken from the [research paper](https://arxiv.org/abs/2503.03669#:~:text=We%20present%20Attentive%20Reasoning%20Queries%20%28ARQs%29%2C%20a%20novel,in%20Large%20Language%20Models%20through%20domain-specialized%20reasoning%20blueprints.))

Besides increasing accuracy and conformance to instructions, this process creates, as a byproduct, transparent, auditable reasoning paths that help maintain alignment with desired behaviors.

ARQs are flexible enough to adapt to different contexts and risk levels, with reasoning blueprints that can be tailored to specific domains or regulatory requirements. While there's some computational overhead to this more deliberate thinking process, carefully designed ARQs can beat Chain-of-Thought reasoning in both accuracy and latency.

Parlant uses different sets of ARQs for each of its components (e.g., guideline matching, tool-calling, or message composition), and dynamically specializes the ARQs to the specific entity it's evaluating, whether it's a particular guideline, tool, or conversational context.

Here's an illustrated example from the `GuidelineMatcher`'s logs:

{  "guideline_id": "fl00LGUyZX",  "condition": "the customer wants to return an item",  "condition_application_rationale": "The customer explicitly stated that they need to return a sweater that doesn't fit, indicating a desire to return an item.",  "condition_applies": true,  "action": "get the order number and item name and them help them return it",  "action_application_rationale": [    {      "action_segment": "Get the order number and item name",      "rationale": "I've yet to get the order number and item name from the customer."    },    {      "action_segment": "Help them return it",      "rationale": "I've yet to offer to help the customer in returning the item."    }  ],  "applies_score": 9}

### Explaining and Troubleshooting Agent Behavior[​](#explaining-and-troubleshooting-agent-behavior "Direct link to Explaining and Troubleshooting Agent Behavior")

Message generation in Parlant goes through quite a lot of quality assurance. As mentioned above, ARQs produce artifacts that can help explain how the agent interpreted circumstances and instructions.

When you run into issues, you can inspect these artifacts to better understand why the agent responded the way it did, and whether it correctly interpreted your intentions.

Over time, this feedback loop helps you build more precise and effective sets of guidelines.

![Explainability in Parlant](/img/explainability.gif)

[

Previous

Custom NLP Models

](/docs/advanced/custom-llms)[

Next

Contributing to Parlant

](/docs/advanced/contributing)

*   [Enforcement & Explainability](#enforcement--explainability-1)
*   [Understanding Runtime Enforcement](#understanding-runtime-enforcement)
*   [Explaining and Troubleshooting Agent Behavior](#explaining-and-troubleshooting-agent-behavior)

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

Source code available on [GitHub](https://github.com/emcie-co