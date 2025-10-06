---
source: "website"
content_type: "blogs_resources"
url: "https://parlant.io/docs/engine-internals/conversation-api"
title: "/docs/engine-internals/conversation-api"
domain: "parlant.io"
path: "/docs/engine-internals/conversation-api"
scraped_time: "2025-09-08T20:00:33.426841"
url_depth: 3
word_count: 881
---

Conversation API | Parlant

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
*   Conversation API

On this page

# Conversation API

## Conversation API[​](#conversation-api-1 "Direct link to Conversation API")

### Motivation[​](#motivation "Direct link to Motivation")

The first thing that's important to understand about the design of the Human/AI interface in Parlant is that it's meant to facilitate conversations that aren't only natural in _content_, but also in their _flow_.

Most traditional chatbot systems (and most LLM interfaces) rely on a request-reply mechanism based on a single last message.

However, these days we know that a natural text interface must allow for a few things that are unsupported by that traditional model:

1.  A human often expresses themselves in more than a single message event, before they're fully ready for a reply from the other party.
2.  Information regarding their intent needs to be captured from not only their last N messages, but from the conversation as a whole.

Moreover, the agent may need to respond not just when triggered by a human message; for example, when it needs to follow-up with the user to ensure their message was received, to try another engagement tactic, or to buy time before replying with further information, e.g., _"Let me check that and get back to you in a minute."_

## Solution[​](#solution "Direct link to Solution")

Parlant's API and engine is meant to work in an asynchronous fashion with respect to the interaction session. In simple terms, this means that both the human customer and the AI agent are free to add events (messages) to the session at any point in time, and in any number—just like in a real IM conversation between two people.

### Sending Messages[​](#sending-messages "Direct link to Sending Messages")

The diagram above shows the API flows for initiating changes to a session.

1.  **Customer Message:** This request adds a new message to a session on behalf of the customer, and triggers the AI agent to respond asynchronously. This means that the _Created Event_ does not in fact contain the agent's reply—that will come in time—but rather the ID (and other details) of the created and persisted customer event.
2.  **AI Agent Message:** This request directly activates the full reaction engine. The agent will match and activate the relevant guidelines and tools, and produce a reply. The _Created Event_ here, however, is not the agent's message, since that may take some time. Instead, it returns a _status event_ containing the same _Correlation ID_ as the eventual agent's message event. It's important to note here that, in most frontend clients, this created event is usually ignored, and is provided mainly for diagnostic purposes.
3.  **Human Agent Message:** Sometimes it makes sense for a human (perhaps a developer) to manually add messages on behalf of the AI agent. This request allows you to do that. The _Created Event_ here is the created and persisted manually-written agent message.

### Receiving Messages[​](#receiving-messages "Direct link to Receiving Messages")

Since messages are sent asyncrhonously, and potentially simultaneously, receiving them must be done in asynchronous fashion as well. In essence, we are to always wait for new messages, which may arrive at any time, from any party.

Parlant implements this functionality with a long-polling, timeout-restricted API endpoint for listing new events. This is what it does behind the scenes:

When it receives a request for new messages, that request generally has 2 important components: 1) The session ID; and 2) The minimum event offset to return. Normally, when making a request to this endpoint, the frontend client is expected to pass the session ID at hand, and _1 + the offset of its last-known event_. This will make this endpoint return only when _new_ messages arrive. It's normal to run this long-polling request in a loop, timing-out every 60 seconds or so and renewing the request while the session is open on the UI. It's this loop that continuously keeps your UI updated with the latest messages, regardless of when they arrive or what caused them to arrive.

In summary, Parlant implements a flexible conversational API that supports natural, modern Human/AI interactions.

[

Previous

Engine Overview

](/docs/engine-internals/overview)[

Next

Create Agent

](/docs/api/create-agent)

*   [Conversation API](#conversation-api-1)
*   [Motivation](#motivation)
*   [Solution](#solution)
*   [Sending Messages](#sending-messages)
*   [Receiving Messages](#receiving-messages)

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