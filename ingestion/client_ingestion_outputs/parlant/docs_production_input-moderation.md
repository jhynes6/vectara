---
source: "website"
content_type: "blogs_resources"
url: "https://parlant.io/docs/production/input-moderation"
title: "/docs/production/input-moderation"
domain: "parlant.io"
path: "/docs/production/input-moderation"
scraped_time: "2025-09-08T19:59:26.216768"
url_depth: 3
word_count: 751
---

User-Input Moderation | Parlant

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
*   [Production](/docs/category/production)
*   User-Input Moderation

On this page

# User-Input Moderation

## User-Input Moderation[​](#user-input-moderation-1 "Direct link to User-Input Moderation")

Adding content filtering to your AI agents helps achieve a more professional level of customer interactions. Here's why it matters.

### Understanding the Challenges[​](#understanding-the-challenges "Direct link to Understanding the Challenges")

AI agents, being based on LLMs, are statistical pattern matchers that can be influenced by the nature of inputs they receive. Think of them like customer service representatives who benefit from clear boundaries about what conversations they should and shouldn't engage in.

#### Sensitive Topics[​](#sensitive-topics "Direct link to Sensitive Topics")

Some topics, like mental health or illicit activities, require professional human handling. While your agent might technically handle these topics, in practical use cases it's often better for it to avoid such conversations, or even redirect them to appropriate human resources.

#### Protection from Harassment[​](#protection-from-harassment "Direct link to Protection from Harassment")

Customer interactions should remain professional, but some users might attempt to harass or abuse the agent (or others). This isn't just about maintaining decorum: LLMs (like humans) can in some cases be influenced by aggressive or inappropriate language, potentially affecting their responses.

To address such cases, Parlant integrates with moderation APIs, such as [OpenAI's Omni Moderation](https://openai.com/index/upgrading-the-moderation-api-with-our-new-multimodal-moderation-model/), to filter such interactions before they reach your agent.

### Enabling Input Moderation[​](#enabling-input-moderation "Direct link to Enabling Input Moderation")

To enable moderation, all you need to do is set a query parameter when creating events.

*   Python
*   TypeScript

from parlant.client import ParlantClientclient = ParlantClient(base_url=SERVER_ADDRESS)client.sessions.create_event(    SESSION_ID,    kind="message",    source="customer",    message=MESSAGE,    moderation="auto",)

import { ParlantClient } from 'parlant-client';const client = new ParlantClient({ environment: SERVER_ADDRESS });await client.sessions.createEvent(SESSION_ID, {     kind: "message",     source: "customer",     message: MESSAGE,     moderation: "auto",});

When customers send inappropriate messages, Parlant ensures that their content is not even visible to the agent; rather, all the agent sees is that a customer sent a message which has been "censored" for a some specific reason (e.g. harrassment, illicit behavior, etc.).

This integrates well with guidelines. For example, you may install a guideline such as:

> *   **Condition:** the customer's last message is censored
> *   **Action:** inform them that you can't help them with this query, and suggest they contact human support

From a UX perspective, this approach is superior to just "erroring out" when encountering such messages. Instead of seeing an error, the customer gets a polite and informative response. Better yet, the response can be controlled with guidelines and tools just as in any other situation.

## Jailbreak Protection[​](#jailbreak-protection "Direct link to Jailbreak Protection")

While your agent's guidelines aren't strictly security measures (as that's handled more robustly by backend permissions), maintaining presentable behavior is important even when some users might try to trick the agent into revealing its instructions or acting outside its intended boundaries.

Parlant's moderation system supports a special `paranoid` mode, which integrates with [Lakera Guard](https://www.lakera.ai/lakera-guard) (from the creators of the [Gandalf Challenge](https://gandalf.lakera.ai/baseline)) to prevent such manipulation attempts.

*   Python
*   TypeScript

from parlant.client import ParlantClientclient = ParlantClient(base_url=SERVER_ADDRESS)client.sessions.create_event(    SESSION_ID,    kind="message",    source="customer",    message=MESSAGE,    moderation="paranoid",)

import { ParlantClient } from 'parlant-client';const client = new ParlantClient({ environment: SERVER_ADDRESS });await client.sessions.createEvent(SESSION_ID, {     kind: "message",     source: "customer",     message: MESSAGE,     moderation: "paranoid",});

Note that to activate `paranoid` mode, you need to get an API key from Lakera and assign it to the environment variable `LAKERA_API_KEY` before starting the server.

[

Previous

Agentic Design Methodology

](/docs/production/agentic-design)[

Next

Human Handoff

](/docs/production/human-handoff)

*   [User-Input Moderation](#user-input-moderation-1)
*   [Understanding the Challenges](#understanding-the-challenges)
*   [Enabling Input Moderation](#enabling-input-moderation)
*   [Jailbreak Protection](#jailbreak-protection)

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

Source code available on [GitHub](https://github.com/emci