---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/agents/agents_introduction/"
title: "/agents/agents_introduction/"
domain: "docs.mistral.ai"
path: "/agents/agents_introduction/"
scraped_time: "2025-09-08T18:10:09.077652"
url_depth: 2
word_count: 550
---

Agents Introduction | Mistral AI

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
*   Agents Introduction

On this page

# Agents Introduction

## What are AI agents?[​](#what-are-ai-agents "Direct link to What are AI agents?")

![agent_introduction](/img/agent_overview.png)

AI agents are autonomous systems powered by large language models (LLMs) that, given high-level instructions, can plan, use tools, carry out processing steps, and take actions to achieve specific goals. These agents leverage advanced natural language processing capabilities to understand and execute complex tasks efficiently and can even collaborate with each other to achieve more sophisticated outcomes.

Our Agents and Conversations API allows developers to build such agents, leveraging multiple features such as:

*   Multiple mutlimodal models available, **text and vision models**.
*   **Persistent state** across conversations.
*   Ability to have conversations with **base models**, **a single agent**, and **multiple agents**.
*   Built-in connector tools for **code execution**, **web search**, **image generation** and **document library** out of the box.
*   **Handoff capability** to use different agents as part of a workflow, allowing agents to call other agents.
*   Features supported via our chat completions endpoint are also supported, such as:
*   **Structured Outputs**
*   **Document Understanding**
*   **Tool Usage**
*   **Citations**

## More Information[​](#more-information "Direct link to More Information")

*   [Agents & Conversations](/agents/agents_basics/): Basic explanations and code snippets around our Agents and Conversations API.
*   [Connectors](/agents/connectors/connectors/): Make your tools accessible directly to any Agents.
*   [Websearch](/agents/connectors/websearch/): In-depth explanation of our web search built-in connector tool.
*   [Code Interpreter](/agents/connectors/code_interpreter/): In-depth explanation of our code interpreter for code execution built-in connector tool.
*   [Image Generation](/agents/connectors/image_generation/): In-depth explanation of our image generation built-in connector tool.
*   [Document Library (Beta)](/agents/connectors/document_library/): A RAG built-in connector enabling Agents to access a library of documents.
*   [MCP](/agents/mcp/): How to use [MCP](/capabilities/function_calling/) (Model Context Protocol) servers with Agents.
*   [Function Calling](/agents/function_calling/): How to use [Function calling](/capabilities/function_calling/) with Agents.
*   [Handoffs](/agents/handoffs/): Relay tasks and use other agents as tools in agentic workflows.

## Cookbooks[​](#cookbooks "Direct link to Cookbooks")

For more information and guides on how to use our Agents, we have the following cookbooks:

*   [Github Agent](https://github.com/mistralai/cookbook/tree/main/mistral/agents/agents_api/github_agent)
*   [Linear Tickets](https://github.com/mistralai/cookbook/tree/main/mistral/agents/agents_api/prd_linear_ticket)
*   [Financial Analyst](https://github.com/mistralai/cookbook/tree/main/mistral/agents/agents_api/financial_analyst)
*   [Travel Assistant](https://github.com/mistralai/cookbook/tree/main/mistral/agents/agents_api/travel_assistant)
*   [Food Diet Companion](https://github.com/mistralai/cookbook/tree/main/mistral/agents/agents_api/food_diet_companion)

## FAQ[​](#faq "Direct link to FAQ")

*   **Which models are supported?**

Currently, only `mistral-medium-latest` and `mistral-large-latest` are supported, but we will soon enable it for more models.

[

Previous

Predicted outputs

](/capabilities/predicted-outputs/)[

Next

Agents & Conversations

](/agents/agents_basics/)

*   [What are AI agents?](#what-are-ai-agents)
*   [More Information](#more-information)
*   [Cookbooks](#cookbooks)
*   [FAQ](#faq)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025 Mi