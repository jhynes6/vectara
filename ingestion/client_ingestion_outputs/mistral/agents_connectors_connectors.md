---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/agents/connectors/connectors/"
title: "/agents/connectors/connectors/"
domain: "docs.mistral.ai"
path: "/agents/connectors/connectors/"
scraped_time: "2025-09-08T18:10:29.059137"
url_depth: 3
word_count: 412
---

Connectors Overview | Mistral AI

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
*   Connectors

On this page

# Connectors Overview

Connectors are tools that Agents can call at any given point. They are deployed and ready for the agents to leverage to answer questions on demand.

![connectors_graph](/img/connectors_graph.png)

They are also available for users to use them directly via Conversations without the Agent creation step!

## General Usage[​](#general-usage "Direct link to General Usage")

*   python
*   typescript
*   curl

You can either create an Agent with the desired tools:

agent = client.beta.agents.create(    model="<model>",    name="<name_of_the_agent>",    description="<description>",    instructions="<instructions_or_system_prompt>",    tools=[<list_of_tools>])

Or call our conversations API directly:

response = client.beta.conversations.start(    model="<model>",    inputs=[<messages_or_question>],    tools=[<list_of_tools>],    # store=False)

You can either create an Agent with the desired tools:

agent = client.beta.agents.create({    model:"<model>",    name:"<name_of_the_agent>",    description:"<description>",    instructions:"<instructions_or_system_prompt>",    tools:[<list_of_tools>]});

Or call our conversations API directly:

response = client.beta.conversations.start({    model:"<model>",    inputs:[<messages_or_question>],    tools:[<list_of_tools>],    // store:False});

You can either create an Agent with the desired tools:

curl --location "https://api.mistral.ai/v1/agents" \     --header 'Content-Type: application/json' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY" \     --data '{     "model": "<model>",     "name": "<name_of_the_agent>",     "description": "<description>",     "instructions": "<instructions_or_system_prompt>",     "tools": [<list_of_tools>]  }'

Or call our conversations API directly:

curl --location "https://api.mistral.ai/v1/conversations" \     --header 'Content-Type: application/json' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY" \     --data '{     "model": "<model>",     "inputs": [<messages_or_question>],     "tools": [<list_of_tools>]  }'

Currently, our API has 4 built-in Connector tools, here you can find how to use them in details:

*   [Websearch](/agents/connectors/websearch/)
*   [Code Interpreter](/agents/connectors/code_interpreter/)
*   [Image Generation](/agents/connectors/image_generation/)
*   [Document Library](/agents/connectors/document_library/)

[

Previous

Agents & Conversations

](/agents/agents_basics/)[

Next

Websearch

](/agents/connectors/websearch/)

*   [General Usage](#general-usage)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025 Mistral