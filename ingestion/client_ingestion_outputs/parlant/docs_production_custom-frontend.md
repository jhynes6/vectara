---
source: "website"
content_type: "other"
url: "https://parlant.io/docs/production/custom-frontend"
title: "/docs/production/custom-frontend"
domain: "parlant.io"
path: "/docs/production/custom-frontend"
scraped_time: "2025-09-08T19:59:08.112563"
url_depth: 3
word_count: 1839
---

Custom Frontend | Parlant

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
*   Custom Frontend

On this page

# Custom Frontend

## Using the Official React Widget[​](#using-the-official-react-widget "Direct link to Using the Official React Widget")

The fastest way to integrate Parlant into your React application is using our official [`parlant-chat-react`](https://github.com/emcie-co/parlant-chat-react) widget. This component provides a complete chat interface that connects directly to your Parlant agents.

### Installation and Basic Setup[​](#installation-and-basic-setup "Direct link to Installation and Basic Setup")

Install the widget via npm or yarn:

npm install parlant-chat-react# oryarn add parlant-chat-react

Then integrate it into your React application:

import React from 'react';import ParlantChatbox from 'parlant-chat-react';function App() {  return (    <div>      <h1>My Application</h1>      <ParlantChatbox        server="http://localhost:8800"  // Your Parlant server URL        agentId="your-agent-id"         // Your agent's ID      />    </div>  );}export default App;

### Configuration Options[​](#configuration-options "Direct link to Configuration Options")

The widget supports several configuration props:

<ParlantChatbox  // Required props  server="http://localhost:8800"  agentId="your-agent-id"  // Optional props  sessionId="existing-session-id"     // Continue existing session  customerId="customer-123"           // Associate with specific customer  float={true}                        // Display as floating popup  titleFn={(session) => `Chat ${session.id}`}  // Dynamic title generation/>

### Common Customizations[​](#common-customizations "Direct link to Common Customizations")

#### Styling with Custom Classes[​](#styling-with-custom-classes "Direct link to Styling with Custom Classes")

Customize the appearance using CSS class overrides:

<ParlantChatbox  server="http://localhost:8800"  agentId="your-agent-id"  classNames={{    chatboxWrapper: "my-chat-wrapper",    chatbox: "my-chatbox",    messagesArea: "my-messages",    agentMessage: "my-agent-bubble",    customerMessage: "my-customer-bubble",    textarea: "my-input-field",    popupButton: "my-popup-btn"  }}/>

#### Custom Component Replacement[​](#custom-component-replacement "Direct link to Custom Component Replacement")

Replace specific components with your own:

<ParlantChatbox  server="http://localhost:8800"  agentId="your-agent-id"  components={{    popupButton: ({ toggleChatOpen }) => (      <button        onClick={toggleChatOpen}        className="custom-chat-button"      >        💬 Chat with us      </button>    ),    agentMessage: ({ message }) => (      <div className="custom-agent-message">        <img src="/agent-avatar.png" alt="Agent" />        <p>{message.data.message}</p>      </div>    )  }}/>

#### Floating Chat Mode[​](#floating-chat-mode "Direct link to Floating Chat Mode")

Enable popup mode for a floating chat interface:

<ParlantChatbox  server="http://localhost:8800"  agentId="your-agent-id"  float={true}  popupButton={<ChatIcon size={24} color="white" />}/>

Reference Implementation

The parlant-chat-react widget is open source! You can [examine its implementation on GitHub](https://github.com/emcie-co/parlant-chat-react) as a reference for creating custom widgets in other UI frameworks like Vue, Angular, or vanilla JavaScript. The source code demonstrates best practices for session management, event handling, and UI state synchronization.

## Building a Custom Frontend[​](#building-a-custom-frontend "Direct link to Building a Custom Frontend")

If you need more control than the React widget provides, or you're using a different framework, you can build a custom frontend using Parlant's client APIs directly.

### Step 1: Initialize the Parlant Client[​](#step-1-initialize-the-parlant-client "Direct link to Step 1: Initialize the Parlant Client")

Start by setting up the Parlant client to communicate with your server:

*   TypeScript
*   JavaScript

import { ParlantClient } from 'parlant-client';class ParlantChat {  private client: ParlantClient;  private sessionId: string | null = null;  private lastOffset: number = 0;  constructor(serverUrl: string) {    this.client = new ParlantClient({      environment: serverUrl    });  }}

import { ParlantClient } from 'parlant-client';class ParlantChat {  constructor(serverUrl) {    this.client = new ParlantClient({      environment: serverUrl    });    this.sessionId = null;    this.lastOffset = 0;  }}

![get-in-touch](/img/get-in-touch-button-icon.svg)Need help with a custom frontend?

### Step 2: Create a Session[​](#step-2-create-a-session "Direct link to Step 2: Create a Session")

Initialize a conversation session with your agent:

*   TypeScript
*   JavaScript

async createSession(agentId: string, customerId?: string): Promise<string> {  try {    const session = await this.client.sessions.create({      agentId: agentId,      customerId: customerId,      title: `Chat Session ${new Date().toLocaleString()}`    });    this.sessionId = session.id;    console.log('Session created:', this.sessionId);    // Start monitoring for events    this.startEventMonitoring();    return this.sessionId;  } catch (error) {    console.error('Failed to create session:', error);    throw error;  }}

async createSession(agentId, customerId) {  try {    const session = await this.client.sessions.create({      agentId: agentId,      customerId: customerId,      title: `Chat Session ${new Date().toLocaleString()}`    });    this.sessionId = session.id;    console.log('Session created:', this.sessionId);    // Start monitoring for events    this.startEventMonitoring();    return this.sessionId;  } catch (error) {    console.error('Failed to create session:', error);    throw error;  }}

### Step 3: Send Customer Messages[​](#step-3-send-customer-messages "Direct link to Step 3: Send Customer Messages")

Handle user input and send messages to the agent:

*   TypeScript
*   JavaScript

async sendMessage(message: string): Promise<void> {  if (!this.sessionId) {    throw new Error('No active session');  }  try {    await this.client.sessions.createEvent(this.sessionId, {      kind: "message",      source: "customer",      message: message    });    // Message will appear in UI when it comes back from event monitoring    console.log('Message sent:', message);  } catch (error) {    console.error('Failed to send message:', error);    throw error;  }}

async sendMessage(message) {  if (!this.sessionId) {    throw new Error('No active session');  }  try {    await this.client.sessions.createEvent(this.sessionId, {      kind: "message",      source: "customer",      message: message    });    // Message will appear in UI when it comes back from event monitoring    console.log('Message sent:', message);  } catch (error) {    console.error('Failed to send message:', error);    throw error;  }}

### Step 4: Monitor Session Events[​](#step-4-monitor-session-events "Direct link to Step 4: Monitor Session Events")

Implement event monitoring to receive messages and updates:

*   TypeScript
*   JavaScript

private async startEventMonitoring(): Promise<void> {  if (!this.sessionId) return;  while (true) {    try {      // Poll for new events with long polling      const events = await this.client.sessions.listEvents(this.sessionId, {        minOffset: this.lastOffset,        waitForData: 30, // Wait up to 30 seconds for new events        kinds: ["message", "status"] // Only get message and status events      });      // Process each event      for (const event of events) {        await this.handleEvent(event);        this.lastOffset = Math.max(this.lastOffset, event.offset + 1);      }    } catch (error) {      console.error('Event monitoring error:', error);      // Wait before retrying      await new Promise(resolve => setTimeout(resolve, 5000));    }  }}private async handleEvent(event: any): Promise<void> {  if (event.kind === "message") {    this.displayMessage(event);  } else if (event.kind === "status") {    this.updateStatus(event.data.status);  }}

async startEventMonitoring() {  if (!this.sessionId) return;  while (true) {    try {      // Poll for new events with long polling      const events = await this.client.sessions.listEvents(this.sessionId, {        minOffset: this.lastOffset,        waitForData: 30, // Wait up to 30 seconds for new events        kinds: ["message", "status"] // Only get message and status events      });      // Process each event      for (const event of events) {        await this.handleEvent(event);        this.lastOffset = Math.max(this.lastOffset, event.offset + 1);      }    } catch (error) {      console.error('Event monitoring error:', error);      // Wait before retrying      await new Promise(resolve => setTimeout(resolve, 5000));    }  }}async handleEvent(event) {  if (event.kind === "message") {    this.displayMessage(event);  } else if (event.kind === "status") {    this.updateStatus(event.data.status);  }}

### Step 5: Display Messages in Your UI[​](#step-5-display-messages-in-your-ui "Direct link to Step 5: Display Messages in Your UI")

Implement UI updates based on events from Parlant:

*   TypeScript
*   JavaScript

private displayMessage(event: any): void {  const messageElement = document.createElement('div');  messageElement.className = `message ${event.source}`;  // Style based on message source  switch (event.source) {    case 'customer':      messageElement.classList.add('customer-message');      break;    case 'ai_agent':      messageElement.classList.add('agent-message');      break;    case 'human_agent':      messageElement.classList.add('human-agent-message');      const agentName = event.data.participant?.display_name || 'Agent';      messageElement.innerHTML = `        <div class="agent-info">${agentName}</div>        <div class="message-content">${event.data.message}</div>      `;      break;  }  // Add to chat container  const chatContainer = document.getElementById('chat-messages');  if (chatContainer) {    chatContainer.appendChild(messageElement);    chatContainer.scrollTop = chatContainer.scrollHeight;  }}private updateStatus(status: string): void {  const statusElement = document.getElementById('chat-status');  if (statusElement) {    switch (status) {      case 'processing':        statusElement.textContent = 'Agent is thinking...';        break;      case 'typing':        statusElement.textContent = 'Agent is typing...';        break;      case 'ready':        statusElement.textContent = '';        break;    }  }}

displayMessage(event) {  const messageElement = document.createElement('div');  messageElement.className = `message ${event.source}`;  // Style based on message source  switch (event.source) {    case 'customer':      messageElement.classList.add('customer-message');      messageElement.innerHTML = `<div class="message-content">${event.data.message}</div>`;      break;    case 'ai_agent':      messageElement.classList.add('agent-message');      messageElement.innerHTML = `<div class="message-content">${event.data.message}</div>`;      break;    case 'human_agent':      messageElement.classList.add('human-agent-message');      const agentName = event.data.participant?.display_name || 'Agent';      messageElement.innerHTML = `        <div class="agent-info">${agentName}</div>        <div class="message-content">${event.data.message}</div>      `;      break;  }  // Add to chat container  const chatContainer = document.getElementById('chat-messages');  if (chatContainer) {    chatContainer.appendChild(messageElement);    chatContainer.scrollTop = chatContainer.scrollHeight;  }}updateStatus(status) {  const statusElement = document.getElementById('chat-status');  if (statusElement) {    switch (status) {      case 'processing':        statusElement.textContent = 'Agent is thinking...';        break;      case 'typing':        statusElement.textContent = 'Agent is typing...';        break;      case 'ready':        statusElement.textContent = '';        break;    }  }}

### Step 6: Complete HTML Example[​](#step-6-complete-html-example "Direct link to Step 6: Complete HTML Example")

Here's a complete HTML page that demonstrates the custom implementation:

<!DOCTYPE html><html lang="en"><head>    <meta charset="UTF-8">    <meta name="viewport" content="width=device-width, initial-scale=1.0">    <title>Custom Parlant Chat</title>    <style>        .chat-container {            max-width: 500px;            margin: 50px auto;            border: 1px solid #ddd;            border-radius: 8px;            overflow: hidden;        }        .chat-header {            background: #007bff;            color: white;            padding: 15px;            text-align: center;        }        .chat-messages {            height: 400px;            padding: 15px;            overflow-y: auto;            background: #f8f9fa;        }        .message {            margin: 10px 0;            padding: 10px;            border-radius: 8px;            max-width: 80%;        }        .customer-message {            background: #007bff;            color: white;            margin-left: auto;            text-align: right;        }        .agent-message {            background: white;            border: 1px solid #ddd;        }        .human-agent-message {            background: #28a745;            color: white;        }        .chat-input {            display: flex;            padding: 15px;            background: white;        }        .chat-input input {            flex: 1;            padding: 10px;            border: 1px solid #ddd;            border-radius: 4px;            margin-right: 10px;        }        .chat-input button {            padding: 10px 20px;            background: #007bff;            color: white;            border: none;            border-radius: 4px;            cursor: pointer;        }        #chat-status {            font-style: italic;            color: #666;            padding: 5px 15px;        }    </style></head><body>    <div class="chat-container">        <div class="chat-header">            <h3>Customer Support Chat</h3>        </div>        <div id="chat-status"></div>        <div id="chat-messages" class="chat-messages"></div>        <div class="chat-input">            <input                type="text"                id="message-input"                placeholder="Type your message..."                onkeypress="handleKeyPress(event)"            />            <button onclick="sendMessage()">Send</button>        </div>    </div>    <script type="module">        import { ParlantClient } from 'https://unpkg.com/parlant-client@latest/dist/index.js';        // Initialize your custom chat        const chat = new ParlantChat('http://localhost:8800');        // Start chat session        chat.createSession('your-agent-id')            .then(sessionId => {                console.log('Chat ready!', sessionId);            })            .catch(error => {                console.error('Failed to start chat:', error);            });        // Make functions available globally        window.sendMessage = () => chat.sendUserMessage();        window.handleKeyPress = (event) => {            if (event.key === 'Enter') {                chat.sendUserMessage();            }        };    </script></body></html>

### Key Implementation Principles[​](#key-implementation-principles "Direct link to Key Implementation Principles")

1.  **Event-Driven Architecture**: The chat is driven by events from Parlant sessions, ensuring consistency with the server state.

2.  **Long Polling**: Use `waitForData` parameter in `listEvents()` for efficient real-time updates without constant polling.

3.  **State Synchronization**: Always display what comes from Parlant events rather than optimistically updating the UI.

4.  **Error Handling**: Implement robust error handling and retry logic for network issues.

5.  **Responsive Design**: Ensure your chat interface works well on both desktop and mobile devices.

![get-in-touch](/img/get-in-touch-button-icon.svg)Need help with a custom frontend?

This approach gives you complete control over the chat experience while leveraging Parlant's powerful agent capabilities. You can adapt this pattern to any frontend framework or vanilla JavaScript implementation.

[

Previous

API Hardening

](/docs/production/api-hardening)[

Next

Engine Extensions

](/docs/advanced/engine-extensions)

*   [Using the Official React Widget](#using-the-official-react-widget)
*   [Installation and Basic Setup](#installation-and-basic-setup)
*   [Configuration Options](#configuration-options)
*   [Common Customizations](#common-customizations)
*   [Building a Custom Frontend](#building-a-custom-frontend)
*   [Step 1: Initialize the Parlant Client](#step-1-initialize-the-parlant-client)
*   [Step 2: Create a Session](#step-2-create-a-session)
*   [Step 3: Send Customer Messages](#step-3-send-customer-messages)
*   [Step 4: Monitor Session Events](#step-4-monitor-session-events)
*   [Step 5: Display Messages in Your UI](#step-5-display-messages-in-your-ui)
*   [Step 6: Complete HTML Example](#step-6-complete-html-example)
*   [Key Implementation Principles](#key-implementation-principles)

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