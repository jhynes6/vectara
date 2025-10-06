---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/agents/connectors/websearch/"
title: "/agents/connectors/websearch/"
domain: "docs.mistral.ai"
path: "/agents/connectors/websearch/"
scraped_time: "2025-09-08T18:09:53.772902"
url_depth: 3
word_count: 1286
---

Websearch | Mistral AI

[Skip to main content](#__docusaurus_skipToContent_fallback)

[

![Mistral AI Logo](/img/logo.svg)![Mistral AI Logo](/img/logo-dark.svg)

](https://mistral.ai/)[Le Chat](https://chat.mistral.ai/)[La Plateforme](https://console.mistral.ai/)[Docs](/)[Cookbooks (beta)](/cookbooks/)[API](/api/)

[GitHub](https://github.com/mistralai/)[Discord](https://discord.gg/mistralai)

*   Getting Started
*   [Introduction](/)
*   [Quickstart](/getting-started/quickstart/)
*   [Models](/getting-started/models/models_overview/)

*   [SDK Clients](/getting-started/clients/)
*   [Model customization](/getting-started/customization/)
*   [Developer examples](/getting-started/stories/)
*   [Changelog](/getting-started/changelog/)
*   [Glossary](/getting-started/glossary/)
*   Capabilities
*   [Text and Chat Completions](/capabilities/completion/)
*   [Vision](/capabilities/vision/)
*   [Audio & Transcription](/capabilities/audio/)
*   [Reasoning](/capabilities/reasoning/)
*   [Document AI](/capabilities/document_ai/document_ai_overview/)

*   [Coding](/capabilities/code_generation/)
*   [Embeddings](/capabilities/embeddings/overview/)

*   [Function calling](/capabilities/function_calling/)
*   [Citations and References](/capabilities/citations/)
*   [Structured Output](/capabilities/structured-output/structured_output_overview/)

*   [Moderation](/capabilities/guardrailing/)
*   [Finetuning](/capabilities/finetuning/finetuning_overview/)

*   [Batch Inference](/capabilities/batch/)
*   [Predicted outputs](/capabilities/predicted-outputs/)
*   Agents
*   [Agents Introduction](/agents/agents_introduction/)
*   [Agents & Conversations](/agents/agents_basics/)
*   [Connectors](/agents/connectors/connectors/)

*   [Websearch](/agents/connectors/websearch/)
*   [Code Interpreter](/agents/connectors/code_interpreter/)
*   [Image Generation](/agents/connectors/image_generation/)
*   [Document Library](/agents/connectors/document_library/)
*   [MCP](/agents/mcp/)
*   [Agents Function Calling](/agents/function_calling/)
*   [Agents Handoffs](/agents/handoffs/)
*   Deployment
*   [La Plateforme](/deployment/laplateforme/overview/)

*   [Cloud](/deployment/cloud/overview/)

*   [Self-deployment](/deployment/self-deployment/overview/)

*   Guides
*   [Prompting capabilities](/guides/prompting_capabilities/)
*   [Basic RAG](/guides/rag/)
*   [Prefix](/guides/prefix/)
*   [Tokenization](/guides/tokenization/)
*   [Sampling](/guides/sampling/)
*   [Fine-tuning](/guides/finetuning/)
*   [Evaluation](/guides/evaluation/)
*   [Observability](/guides/observability/)
*   [Other resources](/guides/resources/)
*   [How to contribute](/guides/contribute/overview/)

*   [](/)
*   [Connectors](/agents/connectors/connectors/)
*   Websearch

On this page

# Websearch

Websearch is the capability to browse the web in search of information, this tool does not only fix the limitations of models of not being up to date due to their training data, but also allows them to actually retrieve recent information or access specific websites.

![websearch_graph](/img/websearch_connector.png)

Our built-in [connector](/agents/connectors/connectors/) tool for websearch allows any of our models to access the web at any point to search websites and sources for relevant information to answer the given query, but also open provided URLs from the user.

There are two versions:

*   `web_search`: A simple web search tool that enables access to a search engine.
*   `web_search_premium`: A more complex web search tool that enables access to both a search engine and to news articles via integrated news provider verification.

## Create a Websearch Agent[​](#create-a-websearch-agent "Direct link to Create a Websearch Agent")

You can create an agent with access to websearch by providing it as one of the tools.
Note that you can still add more tools to the agent, the model is free to search the web or not on demand.

*   python
*   typescript
*   curl

websearch_agent = client.beta.agents.create(    model="mistral-medium-2505",    description="Agent able to search information over the web, such as news, weather, sport results...",    name="Websearch Agent",    instructions="You have the ability to perform web searches with `web_search` to find up-to-date information.",    tools=[{"type": "web_search"}],    completion_args={        "temperature": 0.3,        "top_p": 0.95,    })

const websearchAgent = await client.beta.agents.create({  model: "mistral-medium-latest",  name: "WebSearch Agent",  instructions: "Use your websearch abilities when answering requests you don't know.",  description: "Agent able to fetch new information on the web.",  tools: [{ type: "web_search" }],});

curl --location "https://api.mistral.ai/v1/agents" \     --header 'Content-Type: application/json' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY" \     --data '{     "model": "mistral-medium-2505",     "name": "Websearch Agent",     "description": "Agent able to search information over the web, such as news, weather, sport results...",     "instructions": "You have the ability to perform web searches with `web_search` to find up-to-date information.",     "tools": [       {         "type": "web_search"       }     ],     "completion_args": {       "temperature": 0.3,       "top_p": 0.95     }  }'

**Output**

{  "model": "mistral-medium-2505",  "name": "Websearch Agent",  "description": "Agent able to search information over the web, such as news, weather, sport results...",  "id": "ag_06835b734cc47dec8000b5f8f860b672",  "version": 0,  "created_at": "2025-05-27T12:59:32.803403Z",  "updated_at": "2025-05-27T12:59:32.803405Z",  "instructions": "You have the ability to perform web searches with `web_search` to find up-to-date information.",  "tools": [    {      "type": "web_search"    }  ],  "completion_args": {    "stop": null,    "presence_penalty": null,    "frequency_penalty": null,    "temperature": 0.3,    "top_p": 0.95,    "max_tokens": null,    "random_seed": null,    "prediction": null,    "response_format": null,    "tool_choice": "auto"  },  "handoffs": null,  "object": "agent"}

As for other agents, when creating one you will receive an agent id corresponding to the created agent that you can use to start a conversation.

## How it works[​](#how-it-works "Direct link to How it works")

Now that we have our websearch agent ready, we can at any point make use of it to ask it questions about recent events.

### Conversations with Websearch[​](#conversations-with-websearch "Direct link to Conversations with Websearch")

*   python
*   typescript
*   curl

response = client.beta.conversations.start(    agent_id=websearch_agent.id,    inputs="Who won the last European Football cup?")

let conversation = await client.beta.conversations.start({      agentId: agent.id,      inputs:"Who is Albert Einstein?",      //store:false});

curl --location "https://api.mistral.ai/v1/conversations" \     --header 'Content-Type: application/json' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY" \     --data '{     "inputs": "Who won the last European Football cup?",     "stream": false,     "agent_id": "<agent_id>"  }'

For explanation purposes, lets take a look at the output in a readable JSON format.

{  "conversation_id": "conv_06835b734f2776bb80008fa7a309bf5a",  "outputs": [    {      "type": "tool.execution",      "name": "web_search",      "object": "entry",      "created_at": "2025-05-27T12:59:33.171501Z",      "completed_at": "2025-05-27T12:59:34.828228Z",      "id": "tool_exec_06835b7352be74d38000b3523a0cce2e"    },    {      "type": "message.output",      "content": [        {          "type": "text",          "text": "The last winner of the European Football Cup was Spain, who won the UEFA Euro 2024 by defeating England 2-1 in the final"        },        {          "type": "tool_reference",          "tool": "web_search",          "title": "UEFA Euro Winners List from 1960 to today - MARCA in English",          "url": "https://www.marca.com/en/football/uefa-euro/winners.html",          "source": "brave"        },        {          "type": "tool_reference",          "tool": "web_search",          "title": "UEFA Euro winners: Know the champions - full list",          "url": "https://www.olympics.com/en/news/uefa-european-championships-euro-winners-list-champions",          "source": "brave"        },        {          "type": "tool_reference",          "tool": "web_search",          "title": "Full list of UEFA European Championship winners",          "url": "https://www.givemesport.com/football-european-championship-winners/",          "source": "brave"        },        {          "type": "text",          "text": "."        }      ],      "object": "entry",      "created_at": "2025-05-27T12:59:35.457474Z",      "completed_at": "2025-05-27T12:59:36.156233Z",      "id": "msg_06835b7377517a3680009b05207112ce",      "agent_id": "ag_06835b734cc47dec8000b5f8f860b672",      "model": "mistral-medium-2505",      "role": "assistant"    }  ],  "usage": {    "prompt_tokens": 188,    "completion_tokens": 55,    "total_tokens": 7355,    "connector_tokens": 7112,    "connectors": {      "web_search": 1    }  },  "object": "conversation.response"}

### Explanation of the Outputs[​](#explanation-of-the-outputs "Direct link to Explanation of the Outputs")

*   **`tool.execution`**: This entry corresponds to the execution of the web search tool. It includes metadata about the execution, such as:

*   `name`: The name of the tool, which in this case is `web_search`.
*   `object`: The type of object, which is `entry`.
*   `type`: The type of entry, which is `tool.execution`.
*   `created_at` and `completed_at`: Timestamps indicating when the tool execution started and finished.
*   `id`: A unique identifier for the tool execution.
*   **`message.output`**: This entry corresponds to the generated answer from our agent. It includes metadata about the message, such as:

*   `content`: The actual content of the message, which in this case is a list of chunks. These chunks correspond to the text chunks, the actual message response of the model, interleaved with reference chunks. These reference chunks are used for citations during Retrieval-Augmented Generation (RAG) related tool usages. In this case, it provides the source of the information it just answered with, which is extremely useful for web search. This allows for transparent feedback on where the model got its response from for each section and fact answered with. The `content` section includes:
*   `type`: The type of chunk, which can be `text` or `tool_reference`.
*   `text`: The actual text content of the message.
*   `tool`: The name of the tool used for the reference, which in this case is `web_search`.
*   `title`: The title of the reference source.
*   `url`: The URL of the reference source.
*   `source`: The source of the reference.
*   `object`: The type of object, which is `entry`.
*   `type`: The type of entry, which is `message.output`.
*   `created_at` and `completed_at`: Timestamps indicating when the message was created and completed.
*   `id`: A unique identifier for the message.
*   `agent_id`: A unique identifier for the agent that generated the message.
*   `model`: The model used to generate the message, which in this case is `mistral-medium-2505`.
*   `role`: The role of the message, which is `assistant`.

Another tool that pro-actively uses references is the document library beta connector, feel free to take a look [here](/agents/connectors/document_library/).
For more information regarding the use of citations, you can find more [here](/capabilities/citations/).

[

Previous

Connectors Overview

](/agents/connectors/connectors/)[

Next

Code Interpreter

](/agents/connectors/code_interpreter/)

*   [Create a Websearch Agent](#create-a-websearch-agent)
*   [How it works](#how-it-works)
*   [Conversations with Websearch](#conversations-with-websearch)
*   [Explanation of the Outputs](#explanation-of-the-outputs)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025 Mi