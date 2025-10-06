---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/deployment/cloud/azure/"
title: "/deployment/cloud/azure/"
domain: "docs.mistral.ai"
path: "/deployment/cloud/azure/"
scraped_time: "2025-09-08T18:10:20.960046"
url_depth: 3
word_count: 660
---

Azure AI | Mistral AI

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

*   [Azure AI](/deployment/cloud/azure/)
*   [AWS Bedrock](/deployment/cloud/aws/)
*   [Vertex AI](/deployment/cloud/vertex/)
*   [Snowflake Cortex](/deployment/cloud/sfcortex/)
*   [IBM watsonx.ai](/deployment/cloud/ibm-watsonx/)
*   [Outscale](/deployment/cloud/outscale/)
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
*   [Cloud](/deployment/cloud/overview/)
*   Azure AI

On this page

# Azure AI

## Introduction[​](#introduction "Direct link to Introduction")

Mistral AI's open and commercial models can be deployed on the Microsoft Azure AI cloud platform in two ways:

*   _Pay-as-you-go managed services_: Using Model-as-a-Service (MaaS) serverless API deployments billed on endpoint usage. No GPU capacity quota is required for deployment.

*   _Real-time endpoints_: With quota-based billing tied to the underlying GPU infrastructure you choose to deploy.

This page focuses on the MaaS offering, where the following models are available:

*   Mistral Large (24.11, 24.07)
*   Mistral Medium (25.05)
*   Mistral Small (25.03)
*   Mistral Document AI (25.05)
*   Mistral OCR (25.05)
*   Ministral 3B (24.10)
*   Mistral Nemo

For more details, visit the [models](/getting-started/models/models_overview/) page.

## Getting started[​](#getting-started "Direct link to Getting started")

The following sections outline the steps to deploy and query a Mistral model on the Azure AI MaaS platform.

### Deploying the model[​](#deploying-the-model "Direct link to Deploying the model")

Follow the instructions on the [Azure documentation](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-mistral?tabs=mistral-large#create-a-new-deployment) to create a new deployment for the model of your choice. Once deployed, take note of its corresponding URL and secret key.

### Querying the model[​](#querying-the-model "Direct link to Querying the model")

Deployed endpoints expose a REST API that you can query using Mistral's SDKs or plain HTTP calls.

To run the examples below, set the following environment variables:

*   `AZUREAI_ENDPOINT`: Your endpoint URL, should be of the form `https://your-endpoint.inference.ai.azure.com/v1/chat/completions`.
*   `AZUREAI_API_KEY`: Your secret key.

*   cURL
*   Python
*   TypeScript

curl --location $AZUREAI_ENDPOINT/v1/chat/completions \    --header  "Content-Type: application/json" \    --header "Authorization: Bearer $AZURE_API_KEY" \    --data '{  "model": "azureai",  "messages": [    {      "role": "user",      "content": "Who is the best French painter? Answer in one short sentence."    }  ]}'

This code requires a virtual environment with the following packages:

*   `mistralai-azure>=1.0.0`

from mistralai_azure import MistralAzureimport osendpoint = os.environ.get("AZUREAI_ENDPOINT", "")api_key = os.environ.get("AZUREAI_API_KEY", "")client = MistralAzure(azure_endpoint=endpoint,                 azure_api_key=api_key)resp = client.chat.complete(messages=[    {        "role": "user",        "content": "Who is the best French painter? Answer in one short sentence."    },], model="azureai")if resp:    print(resp)

This code requires the following package:

*   `@mistralai/mistralai-azure` (version >= `1.0.0`)

import { MistralAzure } from "@mistralai/mistralai-azure";const client = new MistralAzure({    endpoint: process.env.AZUREAI_ENDPOINT || "",    apiKey: process.env.AZUREAI_API_KEY || ""});async function chat_completion(user_msg: string) {    const resp = await client.chat.complete({        model: "azureai",        messages: [            {                content: user_msg,                role: "user",            },        ],    });    if (resp.choices && resp.choices.length > 0) {        console.log(resp.choices[0]);    }}chat_completion("Who is the best French painter? Answer in one short sentence.");

## Going further[​](#going-further "Direct link to Going further")

For more details and examples, refer to the following resources:

*   [Release blog post for Mistral Document AI](https://techcommunity.microsoft.com/blog/aiplatformblog/deepening-our-partnership-with-mistral-ai-on-azure-ai-foundry/4434656)
*   [Release blog post for Mistral Large 2 and Mistral NeMo](https://techcommunity.microsoft.com/t5/ai-machine-learning-blog/ai-innovation-continues-introducing-mistral-large-2-and-mistral/ba-p/4200181).
*   [Azure documentation for MaaS deployment of Mistral models](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-mistral).
*   [Azure ML examples GitHub repository](https://github.com/Azure/azureml-examples/tree/main/sdk/python/foundation-models/mistral) with several Mistral-based samples.
*   [Azure AI Foundry GitHub repository](https://github.com/azure-ai-foundry/foundry-samples/tree/main/samples/mistral)

[

Previous

Cloud

](/deployment/cloud/overview/)[

Next

AWS Bedrock

](/deployment/cloud/aws/)

*   [Introduction](#introduction)
*   [Getting started](#getting-started)
*   [Deploying the model](#deploying-the-model)
*   [Querying the model](#querying-the-model)
*   [Going further](#going-further)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025