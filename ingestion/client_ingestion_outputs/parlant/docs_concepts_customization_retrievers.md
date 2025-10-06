---
source: "website"
content_type: "other"
url: "https://parlant.io/docs/concepts/customization/retrievers"
title: "/docs/concepts/customization/retrievers"
domain: "parlant.io"
path: "/docs/concepts/customization/retrievers"
scraped_time: "2025-09-08T19:59:24.271211"
url_depth: 4
word_count: 906
---

Retrievers | Parlant

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
*   Retrievers

On this page

# Retrievers

## Retrievers[​](#retrievers-1 "Direct link to Retrievers")

For pragmatic reasons, Parlant distinguishes between two modes of data access; namely, tools and **retrievers**.

When developing customer-facing agents, there are practically two different use cases for fetching data:

1.  **Tools**: Fetching data from specific services in response to specific events, such as user requests.
2.  **Retrievers**: Fetching contextual information to ground, orientate, and align the agent's knowledge with respect to the current state of the conversation. This is traditionally referred to as RAG (Retrieval-Augmented Generation).

A rule of thumb is to use **retrievers** for data that you would typically expect the agent "to know"—compared to tools, which are used for data that the agent needs to "load" or "do something with".

**Use cases for retrievers include:**

*   Fetching answers to common questions
*   Fetching relevant documents or information based on the current conversation context
*   Fetching user-specific data to personalize the agent's responses (see also [Variables](/docs/concepts/customization/variables))

The Response Latency Trade-Off

Because retrievers are only used to ground the agent's knowledge within the current conversation's context, they can typically be executed in parallel with the agent's other tasks (such as guideline matching, tool calling, etc.).

Hence, using retrievers allows you to ground your agent's response without the added latency of guideline matching or tool calls.

## Creating a Retriever[​](#creating-a-retriever "Direct link to Creating a Retriever")

A retriever is a function that takes a `p.RetrieverContext` and returns a `p.RetrieverResult`. The `p.RetrieverContext` contains the current conversation context, and the `p.RetrieverResult` contains the data that the retriever has fetched.

async def my_retriever(context: p.RetrieverContext) -> p.RetrieverResult:  ...

#### Simple RAG Example[​](#simple-rag-example "Direct link to Simple RAG Example")

Here's a simple example of a retriever that fetches documents from a DB based on the customer's last message:

async def answer_retriever(context: p.RetrieverContext) -> p.RetrieverResult:    # Get the last message from the conversation    if last_message := context.interaction.last_customer_message:        # Use an embedder to convert the message into a vector        message_vector = my_embedder.embed(last_message.content)        # Fetch documents from the database based on the message vector        documents = await fetch_documents_from_db(message_vector)        return p.RetrieverResult(documents)    return p.RetrieverResult(None)

Alternatively, you could use an LLM to generate a query based on the entire interaction history:

async def answer_retriever(context: p.RetrieverContext) -> p.RetrieverResult:    if context.interaction.messages:        # Join all messages in the conversation to create a neat context        conversation_text = "\n".join(str(msg) for msg in context.interaction.messages)        # Use an LLM to extract a user query from the conversation        if query := await my_llm.extract_user_query_from_conversation(conversation_text):          # Use an embedder to convert the query into a vector          message_vector = my_embedder.embed(query)          # Fetch documents from the database based on the query vector          documents = await fetch_documents_from_db(message_vector)          return p.RetrieverResult(documents)    return p.RetrieverResult(None)

![get-in-touch](/img/get-in-touch-button-icon.svg)Questions? Reach out!

#### Attaching a Retriever[​](#attaching-a-retriever "Direct link to Attaching a Retriever")

To actually get an agent to use your retriever, you need to attach it in the following manner:

await agent.attach_retriever(my_retriever)

You can also specify the retriever's ID, which is useful for debugging and logging purposes:

await agent.attach_retriever(my_retriever, id="my_retriever")

## Retriever Result Lifespan[​](#retriever-result-lifespan "Direct link to Retriever Result Lifespan")

The lifespan of retriever results is limited to the current response; in other words, it does not persist throughout the conversation. This also helps you keep the conversation context clean and focused, while also reducing average input tokens, throughout the conversation.

## Retriever Context[​](#retriever-context "Direct link to Retriever Context")

Using the retriever context, you can access a number of useful properties that can help you build more sophisticated retrievers:

*   `server`: The server that is currently processing the retriever request, which can be useful for accessing server-specific resources or configurations.
*   `container`: The dependency-injection container that is currently being used, which allows you to access services and resources registered in the container.
*   `logger`: The logger that is currently being used, which can be useful for logging debug information or errors during the retriever's execution.
*   `correlation_id`: A unique identifier for the agent's current response, which can be used for tracking and debugging purposes.
*   `interaction`: The current interaction, which contains the conversation history and other relevant information.
*   `agent`: The agent that is currently processing the interaction.
*   `customer`: The customer that is currently interacting with the agent.
*   `variables`: The variables that are currently set for the interaction.

![get-in-touch](/img/get-in-touch-button-icon.svg)Reach out for assistance

[

Previous

Tools

](/docs/concepts/customization/tools)[

Next

Glossary

](/docs/concepts/customization/glossary)

*   [Retrievers](#retrievers-1)
*   [Creating a Retriever](#creating-a-retriever)
*   [Retriever Result Lifespan](#retriever-result-lifespan)
*   [Retriever Context](#retriever-context)

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

Source code available on [GitHub](https://github.com/em