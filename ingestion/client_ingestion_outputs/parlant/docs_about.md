---
source: "website"
content_type: "about"
url: "https://parlant.io/docs/about"
title: "/docs/about"
domain: "parlant.io"
path: "/docs/about"
scraped_time: "2025-09-08T20:00:05.802099"
url_depth: 2
word_count: 1191
---

About Parlant | Parlant

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
*   About Parlant

On this page

# About Parlant

## About Parlant[​](#about-parlant-1 "Direct link to About Parlant")

Parlant is built and maintained by a team of software engineers from Microsoft, EverC, Check Point and Dynamic Yield, NLP researchers from the Weizmann Institute of Science, and several contributors from Fortune 500 companies.

We built Parlant to deliver better results from customer-facing AI agents to our clients. Now we're sharing it with the community to help us evolve it together, as we firmly believe in the open, [guided approach to AI agents](https://www.nfx.com/post/guided-ai-agents-turbocharge-smb).

We've licensed Parlant under the [Apache 2](https://www.apache.org/licenses/LICENSE-2.0) open-source license. We don't believe in the long-term viability of the [open-core business model](https://thenewstack.io/rip-open-core-long-live-open-source/) and have no intention of monetizing Parlant itself or making it a freemium product.

With that said, alongside maintaining Parlant, we'll probably release some complementary tools for it down the line. Stay tuned, or [get in touch](mailto:partners@emcie.co)!

### Why Parlant[​](#why-parlant "Direct link to Why Parlant")

Despite the fact that, today, building demo-grade conversational AI agents with LLMs is both simple and accessible to many developers, the challenges of production-grade service agents remain as real as they've ever been.

Since GPT 4's release in March, 2023, we've watched many GenAI teams (including ourselves) sailing through the early stages of agent development—that is, before it meets actual users.

The real challenge emerges after deployment. Once our functioning GenAI agent meets actual users, our backlog quickly fills up with requests to improve how the agent communicates in a variety of situations: _"Here it should say this; there it should follow that principle."_

From a product perspective, [crafting the right conversational experience](https://www.conversationdesigninstitute.com/blog/5-best-conversation-design-strategies-to-get-the-most-out-of-your-chatbot-or-voice-assistant) is something that takes time. While an efficient feedback cycle is essential for delivering high-quality features and improvements in a timely and reliable manner, this basic capability is notably absent from today's LLM frameworks—which is why we built Parlant.

note

Our research into [Conversation Design](https://www.conversationdesigninstitute.com/communications/what-is-conversation-design) revealed that even subtle language adjustments—for example, in how the agent greets customers—can dramatically boost engagement. In one case, a simple rephrasing led to nearly 10% higher engagement for an agent that serves thousands of daily customers.

### The Intrinsic Need for Guidance[​](#the-intrinsic-need-for-guidance "Direct link to The Intrinsic Need for Guidance")

With an eye to the future of GenAI, some view "correct" AI behavior as a purely algorithmic problem—something that can ultimately be automated without human input.

Parlant's philosophy challenges this assumption at its core.

Machine-learning algorithms (including LLMs) are based on data labeled by [people—specific people with specific opinions](https://the-decoder.com/former-openai-researcher-explains-what-ask-the-ai-really-means/) (or vendor-specific labeling guidelines). So regardless of the algorithm, it is always based on some people's input, which may or may not align with others.

On that note, before behavior can be automated, it must first be defined and agreed upon by stakeholders. But how often do we achieve complete agreement with colleagues—or even with our past selves—on every detail? "Correct" behavior is inherently a moving target, constantly evolving for both individuals and organizations.

This leads to an important realization: even if we created a "perfect" agent, project stakeholders would still want to customize its behavior according to their own vision of correctness, regardless of any allegedly objective standard. This is why customization isn't just a feature—it's fundamental to Parlant's approach.

### Parlant vs. Prompt Engineering[​](#parlant-vs-prompt-engineering "Direct link to Parlant vs. Prompt Engineering")

In typical prompt-engineered situations—whether graph-based or otherwise—adjusting specific behaviors becomes increasingly challenging as prompts grow more numerous and complex. [This creates troubling realities for GenAI teams](https://dl.acm.org/doi/fullHtml/10.1145/3563657.3596138?t): one, changing prompts might break existing, tested behaviors; and two, there's little assurance that new behavioral prescriptions will be consistently followed at scale.

**With Parlant, the feedback cycle is reduced to an instant.** When behavioral changes are needed, you can quickly and reliably modify the elements that shape the conversational experience—guidelines, glossaries, context variables, and API usage instructions—and the generation engine immediately applies these changes, ensuring consistent behavior across all interactions.

Better yet, since these behavioral changes are stored in code, they can be easily versioned and tracked using Git.

## Design Philosophy[​](#design-philosophy "Direct link to Design Philosophy")

The landscape of Large Language Models shows clear patterns in its evolution—patterns that directly influence how we should build agent frameworks. Let's look at the data.

The trends are clear: response latency and token costs are dropping significantly across providers. OpenAI's GPT-4 Turbo offers 3x faster response times than its predecessor at 1/3 the cost, and GPT-4o followed suit with its $2.50/1M input tokens and 300ms response latency. Together AI and Anthropic are following similar trajectories, with deployment optimizations and more efficient architectures driving down both latency and cost.

![LLM Prices](/img/llm-prices.png)

More promisingly, custom LLM hardware is on the rise from multiple vendors, [touting 25x improvement on today's best performing APIs](https://www.forbes.com/sites/karlfreund/2024/11/18/cerebras-now-the-fastest-llm-inference-processor--its-not-even-close/).

Yet when we look at accuracy metrics, the story changes. Even recent models with architectural improvements show relatively [marginal gains in key metrics like reasoning and instruction following](https://www.nasdaq.com/articles/ai-progress-stalls-openai-google-and-anthropic-hit-roadblocks#:~:text=Despite%20years%20of%20rapid%20advancements%20in%20artificial%20intelligence,efforts%20to%20develop%20more%20sophisticated%20models%2C%20reports%20Bloomberg.), and, in many cases, in our tests and experience, they actually show degradation. So, while some capabilities expand and improve, fundamental challenges persist, where making sense of complexity remains a significant roadblock.

### Parlant's Response[​](#parlants-response "Direct link to Parlant's Response")

In view of these trends, Parlant is designed to improve and maximize control and alignment on the software level—qualitative but crucial concerns that are largely neglected today—even with today's LLMs. It does so by focusing on three specific, important concerns:

1.  **Strong alignment infrastructure:** clarifying the intended results and feeding instructions to the models only when such instructions are determined relevant, and, finally, enforcing them with specialized prompting techniques.

2.  **Explainable results:** adding visibility to the relevance scoring mechanism with regard to instructions, as well as a human-readable rationale, which helps to troubleshoot and improve alignment issues.

3.  **Human-centric design:** designing the API to facilitate a real-world development and maintenance process, accounting for the nature of software teams, the different roles they contain and how people interact within them to create polished projects while meeting deadlines.

[

Previous

Update Variable

](/docs/api/update-variable)

*   [About Parlant](#about-parlant-1)
*   [Why Parlant](#why-parlant)
*   [The Intrinsic Need for Guidance](#the-intrinsic-need-for-guidance)
*   [Parlant vs. Prompt Engineering](#parlant-vs-prompt-engineering)
*   [Design Philosophy](#design-philosophy)
*   [Parlant's Response](#parlants-response)

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

Source code available on