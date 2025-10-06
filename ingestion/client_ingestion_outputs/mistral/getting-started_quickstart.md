---
source: "website"
content_type: "blogs_resources"
url: "https://docs.mistral.ai/getting-started/quickstart/"
title: "/getting-started/quickstart/"
domain: "docs.mistral.ai"
path: "/getting-started/quickstart/"
scraped_time: "2025-09-08T18:10:19.995838"
url_depth: 2
word_count: 639
---

Quickstart | Mistral AI

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
*   Quickstart

On this page

# Quickstart

tip

Looking for La Plateforme? Head to [console.mistral.ai](https://console.mistral.ai/)

## Account setup[​](#account-setup "Direct link to Account setup")

*   To get started, create a Mistral account or sign in at [https://console.mistral.ai](https://console.mistral.ai).
*   Then, navigate to your "Organization" settings at [https://admin.mistral.ai](https://admin.mistral.ai).
*   To add your payment information and activate payments on your account, find the [billing](https://admin.mistral.ai/organization/billing) section under Administration.
*   You can now manage all your [Workspaces](https://admin.mistral.ai/organization/workspaces) and Organization via this page.
*   Return to [https://console.mistral.ai](https://console.mistral.ai) once everything is settled.
*   After that, go to the [API keys](https://console.mistral.ai/api-keys) page under your Workspace and create a new API key by clicking "Create new key". Make sure to copy the API key, save it securely, and do not share it with anyone.

## Getting started with Mistral AI API[​](#getting-started-with-mistral-ai-api "Direct link to Getting started with Mistral AI API")

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mistralai/cookbook/blob/main/quickstart.ipynb)

Mistral AI API provides a seamless way for developers to integrate Mistral's state-of-the-art models into their applications and production workflows with just a few lines of code. Our API is currently available through [La Plateforme](https://console.mistral.ai/). You need to activate payments on your account to enable your API keys. After a few moments, you will be able to use our `chat` endpoint:

*   python
*   typescript
*   curl

import osfrom mistralai import Mistralapi_key = os.environ["MISTRAL_API_KEY"]model = "mistral-large-latest"client = Mistral(api_key=api_key)chat_response = client.chat.complete(    model= model,    messages = [        {            "role": "user",            "content": "What is the best French cheese?",        },    ])print(chat_response.choices[0].message.content)

import { Mistral } from '@mistralai/mistralai';const apiKey = process.env.MISTRAL_API_KEY;const client = new Mistral({apiKey: apiKey});const chatResponse = await client.chat.complete({  model: 'mistral-large-latest',  messages: [{role: 'user', content: 'What is the best French cheese?'}],});console.log('Chat:', chatResponse.choices[0].message.content);

curl --location "https://api.mistral.ai/v1/chat/completions" \     --header 'Content-Type: application/json' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY" \     --data '{    "model": "mistral-large-latest",    "messages": [{"role": "user", "content": "Who is the most renowned French painter?"}]  }'

To generate text embeddings using Mistral AI's embeddings API, we can make a request to the API endpoint and specify the embedding model `mistral-embed`, along with providing a list of input texts. The API will then return the corresponding embeddings as numerical vectors, which can be used for further analysis or processing in NLP applications.

*   python
*   typescript
*   curl

import osfrom mistralai import Mistralapi_key = os.environ["MISTRAL_API_KEY"]model = "mistral-embed"client = Mistral(api_key=api_key)embeddings_response = client.embeddings.create(    model=model,    inputs=["Embed this sentence.", "As well as this one."])print(embeddings_response)

import { Mistral } from '@mistralai/mistralai';const apiKey = process.env.MISTRAL_API_KEY;const client = new Mistral({apiKey: apiKey});const embeddingsResponse = await client.embeddings.create({  model: 'mistral-embed',  inputs: ["Embed this sentence.", "As well as this one."],});console.log(embeddingsResponse);

curl --location "https://api.mistral.ai/v1/embeddings" \     --header 'Content-Type: application/json' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY" \     --data '{    "model": "mistral-embed",    "input": ["Embed this sentence.", "As well as this one."]  }'

For a full description of the models offered on the API, head on to the **[model documentation](/getting-started/models/models_overview/)**.

[

Previous

Introduction

](/)[

Next

Models Overview

](/getting-started/models/models_overview/)

*   [Account setup](#account-setup)
*   [Getting started with Mistral AI API](#getting-started-with-mistral-ai-api)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025 Mistra