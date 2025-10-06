---
source: "website"
content_type: "blogs_resources"
url: "https://parlant.io/docs/quickstart/installation"
title: "/docs/quickstart/installation"
domain: "parlant.io"
path: "/docs/quickstart/installation"
scraped_time: "2025-09-08T19:59:58.668206"
url_depth: 3
word_count: 1055
---

Installation | Parlant

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
*   Quick Start
*   Installation

On this page

# Installation

![Parlant Logo](/logo/logo-full.svg)

## Getting Started with Parlant[​](#getting-started-with-parlant "Direct link to Getting Started with Parlant")

**Parlant** is an open-source **Agentic Behavior Modeling Engine** for LLM agents, built to help developers quickly create customer-engaging, business-aligned conversational agents with control, clarity, and confidence.

It gives you all the structure you need to build customer-facing agents that behave exactly as your business requires:

*   **[Journeys](/docs/concepts/customization/journeys)**: Define clear customer journeys and how your agent should respond at each step.

*   **[Behavioral Guidelines](/docs/concepts/customization/guidelines)**: Easily craft agent behavior; Parlant will match the relevant elements contextually.

*   **[Tool Use](/docs/concepts/customization/tools)**: Attach external APIs, data fetchers, or backend services to specific interaction events.

*   **[Domain Adaptation](/docs/concepts/customization/glossary)**: Teach your agent domain-specific terminology and craft personalized responses.

*   **[Canned Responses](/docs/concepts/customization/canned-responses)**: Use response templates to eliminate hallucinations and guarantee style consistency.

*   **[Explainability](/docs/advanced/explainability)**: Understand why and when each guideline was matched and followed.

## Installation[​](#installation-1 "Direct link to Installation")

Parlant is available on both [GitHub](https://github.com/emcie-co/parlant) and [PyPI](https://pypi.org/project/parlant/) and works on multiple platforms (Windows, Mac, and Linux).

Please note that [Python 3.10](https://www.python.org/downloads/release/python-3105/) and up is required for Parlant to run properly.

pip install parlant

Development Branch

If you're feeling adventurous and want to try out new features, you can also install the latest development version directly from GitHub.

pip install git+https://github.com/emcie-co/parlant@develop

## Creating Your First Agent[​](#creating-your-first-agent "Direct link to Creating Your First Agent")

Once installed, you can use the following code to spin up an initial, sample agent. You'll flesh out its behavior later.

# main.pyimport asyncioimport parlant.sdk as pasync def main():  async with p.Server() as server:    agent = await server.create_agent(        name="Otto Carmen",        description="You work at a car dealership",    )asyncio.run(main())

ASYNC/AWAIT?

You'll notice Parlant follows the asynchronous programming paradigm with `async` and `await`. This is a powerful feature of Python that lets you to write code that can handle many tasks at once, allowing your agent to handle more concurrent requests in production.

If you're new to async programming, check out the [official Python documentation](https://docs.python.org/3/library/asyncio.html) for a quick introduction.

Parlant uses OpenAI as the default NLP provider, so you need to ensure you have `OPENAI_API_KEY` set in your environment.

Then, run the program!

export OPENAI_API_KEY="<YOUR_API_KEY>"python main.py

Using Other LLM Providers

Parlant supports multiple LLM providers by default, accessible via the `p.NLPServices` class. You can also add your own provider by implementing the `p.NLPService` interface, which you can learn how to do in the [Custom NLP Models](/docs/advanced/custom-llms) section.

To use one of the built-in-providers, you can specify it when creating the server. For example:

async with p.Server(nlp_service=p.NLPServices.cerebras) as server:  ...

Note that you may need to install an additional "extra" package for some providers. For example, to use the Cerebras NLP service:

pip install parlant[cerebras]

Having said that, Parlant is observed to work best with [OpenAI](https://openai.com) and [Anthropic](https://www.anthropic.com) models, as these models are highly consistent in generating high-quality completions with valid JSON schemas—so we recommend using one of those if you're just starting out.

## Testing Your Agent[​](#testing-your-agent "Direct link to Testing Your Agent")

To test your installation, head over to [http://localhost:8800](http://localhost:8800) and start a new session with the agent.

![Post installation demo](/img/post-installation-demo.gif)

## Creating Your First Guideline[​](#creating-your-first-guideline "Direct link to Creating Your First Guideline")

Guidelines are the core of Parlant's behavior model. They allow you to define how your agent should respond to specific user inputs or conditions. Parlant cleverly manages guideline context for you, so you can add as many guidelines as you need without worrying about context overload or other scale issues.

# main.pyimport asyncioimport parlant.sdk as pasync def main():  async with p.Server() as server:    agent = await server.create_agent(        name="Otto Carmen",        description="You work at a car dealership",    )    ##############################    ##    Add the following:    ##    ##############################    await agent.create_guideline(        # This is when the guideline will be triggered        condition="the customer greets you",        # This is what the guideline instructs the agent to do        action="offer a refreshing drink",    )asyncio.run(main())

Now re-run the program:

python main.py

Refresh [http://localhost:8800](http://localhost:8800), start a new session, and greet the agent. You should expect to be offered a drink!

## Using the Official React Widget[​](#using-the-official-react-widget "Direct link to Using the Official React Widget")

If your frontend project is built with React, the fastest and easiest way to start is to use the official Parlant React widget to integrate with the server.

Here's a basic code example to get started:

import React from 'react';import ParlantChatbox from 'parlant-chat-react';function App() {  return (    <div>      <h1>My Application</h1>      <ParlantChatbox        server="PARLANT_SERVER_URL"        agentId="AGENT_ID"      />    </div>  );}export default App;

For more documentation and customization, see the **GitHub repo:** [https://github.com/emcie-co/parlant-chat-react](https://github.com/emcie-co/parlant-chat-react).

npm install parlant-chat-react

## Installing Client SDK(s)[​](#installing-client-sdks "Direct link to Installing Client SDK(s)")

To create a custom frontend app that interacts with the Parlant server, we recommend installing our native client SDKs. We currently support Python and TypeScript (also works with JavaScript).

#### Python[​](#python "Direct link to Python")

pip install parlant-client

#### TypeScript/JavaScript[​](#typescriptjavascript "Direct link to TypeScript/JavaScript")

npm install parlant-client

tip

You can review our tutorial on integrating a custom frontend here: [Custom Frontend Integration](/docs/production/custom-frontend).

For other languages—they are coming soon! Meanwhile you can use the [REST API](/docs/api/create-agent) directly.

![get-in-touch](/img/get-in-touch-button-icon.svg)Get a guided demo!

[

Next

Motivation

](/docs/quickstart/motivation)

*   [Getting Started with Parlant](#getting-started-with-parlant)
*   [Installation](#installation-1)
*   [Creating Your First Agent](#creating-your-first-agent)
*   [Testing Your Agent](#testing-your-agent)
*   [Creating Your First Guideline](#creating-your-first-guideline)
*   [Using the Official React Widget](#using-the-official-react-widget)
*   [Installing Client SDK(s)](#installing-client-sdks)

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

Source code available on [GitHub](https://githu