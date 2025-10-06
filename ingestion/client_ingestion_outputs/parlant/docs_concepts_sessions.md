---
source: "website"
content_type: "other"
url: "https://parlant.io/docs/concepts/sessions"
title: "/docs/concepts/sessions"
domain: "parlant.io"
path: "/docs/concepts/sessions"
scraped_time: "2025-09-08T20:00:34.734207"
url_depth: 3
word_count: 2406
---

Sessions | Parlant

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
*   Sessions

On this page

# Sessions

## Sessions[​](#sessions-1 "Direct link to Sessions")

A session represents a continuous interaction between an [agent](/docs/concepts/entities/agents) and a [customer](/docs/concepts/entities/customers).

Sessions are the stage for your conversational model, allowing agents to engage with customers in a structured and persistent manner. They encapsulate all the interactions that occur between an agent and a customer, including messages, status updates, frontend events, and tool call results.

Agent Memory?

What some frameworks call "memory" is already built-in into sessions in Parlant. An agent is constantly aware of everything that has happened in the session, using this information to apply the right instructions and generate appropriate responses.

## A Modern Interaction Model[​](#a-modern-interaction-model "Direct link to A Modern Interaction Model")

Parlant views interaction sessions in a different manner than most Conversational AI frameworks.

In the past few decades, virtually all forms of conversational AI have assumed that an interaction occurs on a turn-by-turn basis, where a customer sends a message, and the agent responds to it.

Yet this is not how real conversations work. People often send each other multiple subsequent messages to communicate their thoughts. In addition, an agent may say something, put the customer on hold for a moment, and then return to the conversation with a follow-up message.

**Rigid Interaction Model**

**Modern Interaction Model**

Since this is how real conversations work, Parlant provides built-in support for it from the ground up.

Multi-Participant Sessions

A requested feature on Parlant's development roadmap, this will allow you to have multiple agents interact with the customer, or with each other. Another use case for this is transferring the customer to another AI agent.

## Configuring Session Storage[​](#configuring-session-storage "Direct link to Configuring Session Storage")

You can choose where you store sessions.

By default, Parlant does not persist sessions, meaning that they are stored in memory and will be lost when the server restarts. This is useful for testing and development purposes.

If you want to persist sessions, you can configure Parlant to use a database of your choice. For local persistence, we recommend using the integrated JSON file storage, as there's zero setup required. For production use, you can use MongoDB, which comes built-in, or another database.

### Persisting to Local Storage[​](#persisting-to-local-storage "Direct link to Persisting to Local Storage")

This will save sessions under `$PARLANT_HOME/sessions.json`.

import asyncioimport parlant.sdk as pasync def main():    async with p.Server(session_store="local") as server:        # ...asyncio.run(main())

### Persisting to MongoDB[​](#persisting-to-mongodb "Direct link to Persisting to MongoDB")

Just specify the connection string to your MongoDB database when starting the server:

import asyncioimport parlant.sdk as pasync def main():    async with p.Server(session_store="mongodb://path.to.your.host:27017") as server:        # ...asyncio.run(main())

![get-in-touch](/img/get-in-touch-button-icon.svg)We can help you ramp up

## Event Driven Communication[​](#event-driven-communication "Direct link to Event Driven Communication")

Think of a session in Parlant as a timeline of everything that's happened in a conversation.

Each moment in this timeline—whether it's someone speaking, a status update, or a tool call result—is captured as an event. These events line up one after another, each with its own position number (called its _offset_), starting from 0.

When a conversation unfolds, it creates a sequence of events. A customer might start the session by saying _"Hello"_—that's event 0. The system then notes that the agent has acknowledged the message and is preparing a response by outputting a status event—that's event 1. The agent's _"Hi there!"_ becomes event 2, and so on. Each event, whether it's a message being exchanged, the agent typing, or even an error occurring, takes its place in this ordered sequence.

Every event in this sequence carries important information: what type of event it is (like a message or a status update), what actually happened (the data), and when it occurred. This creates a complete record of the conversation that helps us understand exactly how things unfolded, making it easy to track and review the conversation's state when needed.

Each event is also associated with a **correlation ID**. This ID primarily helps to correlate between AI-generated messages and the engine triggers that produced them, including any generated tool events that may have informed them. This lets us easily fetch and understand the data that went into each generated message. For example, by having your frontend client inspect a message's correlated tool events, you can show relevant information in "footnotes" under the message.

## Interacting with an Agent[​](#interacting-with-an-agent "Direct link to Interacting with an Agent")

Once you have a Parlant server up and running, you can interact with its hosted agents through the [REST API](/docs/api/create-session).

You have three options:

1.  Use the official React widget to quickly and easily integrate with the server
2.  Use the official client SDKs for Python or TypeScript to build a custom frontend application
3.  Use the [REST API](/docs/api/create-session) directly by making HTTP requests to the server in your language of choice

### Using the Official React Widget[​](#using-the-official-react-widget "Direct link to Using the Official React Widget")

If your frontend project is built with React, the fastest and easiest way to start is to use the official Parlant React widget to integrate with the server.

Here's a basic code example to get started:

import React from 'react';import ParlantChatbox from 'parlant-chat-react';function App() {  return (    <div>      <h1>My Application</h1>      <ParlantChatbox        server="PARLANT_SERVER_URL"        agentId="AGENT_ID"      />    </div>  );}export default App;

For more documentation and customization, see the **GitHub repo:** [https://github.com/emcie-co/parlant-chat-react](https://github.com/emcie-co/parlant-chat-react).

npm install parlant-chat-react

### Building a Custom Frontend[​](#building-a-custom-frontend "Direct link to Building a Custom Frontend")

If you're coding in Python or TypeScript, you can use the official, native client SDKs for a fully-typed experience.

**Python**

pip install parlant-client

**TypeScript**

npm install parlant-client

We'll now cover some basic use cases. The examples will be in Python, but the other SDKs have nearly identical APIs, so you can easily adapt them to your preferred language.

![get-in-touch](/img/get-in-touch-button-icon.svg)Reach out for help

#### Initializing the Client[​](#initializing-the-client "Direct link to Initializing the Client")

from parlant.client import AsyncParlantClient# Change localhost to your server's addressclient = AsyncParlantClient(base_url="http://localhost:8800")

Async Client?

The examples given here use the asynchronous client, which is the recommended way to interact with Parlant. This allows you to handle events in real-time without blocking your application. It's usually much better for production use.

However, if you prefer a synchronous client—for example, if you're just testing—you can use `ParlantClient` instead of `AsyncParlantClient`. The API remains the same, but you don't have to run within an async event loop.

#### Creating a Session[​](#creating-a-session "Direct link to Creating a Session")

await client.sessions.create(    agent_id=AGENT_ID,  # The ID of the agent to interact with    # Optional parameters    customer_id=CUSTOMER_ID,  # Optional: defaults to the guest customer's ID    title=SESSION_TITLE,  # Optional: session can be untitled)

#### Sending Customer Messages to an Agent[​](#sending-customer-messages-to-an-agent "Direct link to Sending Customer Messages to an Agent")

You can send messages to an agent by creating a new message event in the session. This is how you initiate a conversation or continue an existing one.

event = await client.sessions.create_event(    session_id=SESSION_ID,    kind="message",  # The event is of type 'message'    source="customer",  # The message is from the customer    message="Hello, I need help with my order.",)

#### Receiving Messages from an Agent[​](#receiving-messages-from-an-agent "Direct link to Receiving Messages from an Agent")

As stated before, unlike LLM APIs where you send a prompt and wait for a direct response, Parlant agents operate in their own timeline according to triggers, more like real conversation partners.

Much like a human service representative, they process information and decide when and how to respond based on their understanding of the context. This allows you to build much more flexible, ambient agentic experiences that can engage with customers proactively.

However, it also means we need to approach communication with them differently. Here's how you can do that:

new_events = await client.sessions.list_events(    session_id=SESSION_ID,    min_offset=EVENT_OFFSET,  # The offset of the last event you received (or created yourself)    wait_for_data=60,  # Wait for up to 60 seconds for new events, before timing out)

Normally, you'd have this polling in a loop. This way, you can keep checking for new events in the session, allowing you to receive messages from the agent asynchronously, whenever they arrive, due to whatever reason.

### Displaying Messages[​](#displaying-messages "Direct link to Displaying Messages")

Consult the message event's structure below to see how to display messages in your frontend application.

Here's a simple example:

agent_message = next((m for m in new_events if m.kind == "message" and m.source == "ai_agent"), None)if agent_message:    print(f"Agent: {agent_message.data['message']}")

### Events[​](#events "Direct link to Events")

If you decide to build a custom frontend, here's a quick overview of Parlant's event structure.

#### Event Types[​](#event-types "Direct link to Event Types")

Parlant defines several event types that you can work with:

1.  `"message"`: Represents a message sent by a participant in the conversation.
2.  `"status"`: Represents a status update from the AI agent, such as "thinking...", or "typing...".
3.  `"tool"`: Represents the result of a tool call made by the AI agent.
4.  `"custom"`: Represents a custom event defined by your application. This is useful for feeding custom state updates into your agent, e.g., making it aware of the customer's navigational state within your frontend application.

#### Event Offset[​](#event-offset "Direct link to Event Offset")

As said above, events are ordered by their offset, which is a number that indicates the order in which they occurred within the session. The first event in a session has an offset of 0, the second has an offset of 1, and so on.

This is useful because, when you list events, you can specify a minimum offset to only receive events that occurred after a certain point in time. This allows you to poll new events without having to re-fetch all previous ones.

#### Event Correlation ID[​](#event-correlation-id "Direct link to Event Correlation ID")

Each event has a correlation ID, which is a unique identifier that helps you track related events and their logs.

As one example, when an AI agent generates a message, it may also generate tool events that provide additional context or data used in that message. The correlation ID allows you to link these events together, making it easier to understand the flow of information as well as your agent's processing in the session.

#### Event Sources[​](#event-sources "Direct link to Event Sources")

Events in Parlant can originate from different sources. Here's a quick overview of the possible sources:

1.  `"customer"`: The event's data was created by the customer. Currently, this is always a message.
2.  `"customer_ui"`: The event was created by the customer's user interface, to feed relevant state into the agent.
3.  `"ai_agent"`: The event was generated by an AI agent, such as a message or a status update.
4.  `"human_agent"`: The event was manually created by a human, typically in a human-handoff scenario.
5.  `"human_agent_on_behalf_of_ai_agent"`: As above, the event was created by a human agent, but it appears to the customer as if it came from an AI agent. This can be useful for maintaining a consistent experience where you don't necessarily want to reveal the fact that a human agent got involved.
6.  `"system"`: The event was generated by the system, such as a tool-call result.

#### Message Event[​](#message-event "Direct link to Message Event")

A message event, as its name suggests, represents a message written by someone.

{    id: EVENT_ID,    kind: "message",    source: EVENT_SOURCE,    offset: N,    correlation_id: CORRELATION_ID,    data: {        message: MESSAGE,        participant={            id: PARTICIPANT_ID,            display_name: PARTICIPANT_DISPLAY_NAME        },        draft: OPTIONAL_DRAFT,  // Optional: if the message is a canned response    }}

#### Status Event[​](#status-event "Direct link to Status Event")

A status event represents an update on the status of the AI agent, and currently always has the source `"ai_agent"`.

Status events are great for displaying conversational updates during a chat with a customer. For example, you can have your frontend indicate when the agent is thinking or typing. There are 6 kinds of status events that you can make use of:

1.  `"acknowledged"`: The agent has acknowledged the customer's message and started working on a reply
2.  `"cancelled"`: The agent has cancelled its reply in the middle, normally because new data was added to the session
3.  `"processing"`: The agent is evaluating the session in preparation for generating an appropriate reply
4.  `"typing"`: The agent has finished evaluating the session and is currently generating a message
5.  `"ready"`: The agent is idle and ready to receive new events
6.  `"error"`: The agent encountered an error while trying to generate a reply

{    id: EVENT_ID,    kind: "status",    source: "ai_agent",    offset: N,    correlation_id: CORRELATION_ID,    data: {        status: STATUS_KIND,        data: OPTIONAL_DATA    }}

#### Tool Event[​](#tool-event "Direct link to Tool Event")

A tool event represents the result of a tool call made by the AI agent. It contains the result of the tool call, which can be used to inform the agent's next message.

The `result` object for each call comes directly from the [ToolResult](/docs/concepts/customization/tools#tool-result) object returned by tool calls.

{    id: EVENT_ID,    kind: "tool",    source: "system",    offset: N,    correlation_id: CORRELATION_ID,    data: {        tool_calls: [            {                tool_id: TOOL_ID,                arguments: {                    NAME: VALUE,                    ...                },                result: {                    data: TOOL_RESULT_DATA,  // The result of the tool call                    metadata: TOOL_RESULT_METADATA,  // Optional metadata about the tool result                    ... // Other available fields                }            },            ...        ]    }}

![get-in-touch](/img/get-in-touch-button-icon.svg)Reach out for help

[

Previous

Healthcare Agent Example

](/docs/quickstart/examples)[

Next

Agents

](/docs/concepts/entities/agents)

*   [Sessions](#sessions-1)
*   [A Modern Interaction Model](#a-modern-interaction-model)
*   [Configuring Session Storage](#configuring-session-storage)
*   [Persisting to Local Storage](#persisting-to-local-storage)
*   [Persisting to MongoDB](#persisting-to-mongodb)
*   [Event Driven Communication](#event-driven-communication)
*   [Interacting with an Agent](#interacting-with-an-agent)
*   [Using the Official React Widget](#using-the-official-react-widget)
*   [Building a Custom Frontend](#building-a-custom-frontend)
*   [Displaying Messages](#displaying-messages)
*   [Events](#events)

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

Source code a