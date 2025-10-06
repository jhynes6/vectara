---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/deployment/cloud/outscale/"
title: "/deployment/cloud/outscale/"
domain: "docs.mistral.ai"
path: "/deployment/cloud/outscale/"
scraped_time: "2025-09-08T18:10:01.828649"
url_depth: 3
word_count: 717
---

Outscale | Mistral AI

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
*   Outscale

On this page

# Outscale

## Introduction[​](#introduction "Direct link to Introduction")

Mistral AI models are available on the Outscale platform as managed deployments. Through the Outscale marketplace, you can subscribe to a Mistral service that will, on your behalf, provision a virtual machine and a GPU then deploy the model on it.

As of today, the following models are available:

*   Mistral Small (24.09)
*   Codestral (24.05)
*   Ministral 8B (24.10)

For more details, visit the [models](/getting-started/models/models_overview/) page.

## Getting started[​](#getting-started "Direct link to Getting started")

The following sections outline the steps to query a Mistral model on the Outscale platform.

### Deploying the model[​](#deploying-the-model "Direct link to Deploying the model")

Follow the steps described in the [Outscale documentation](https://docs.outscale.com/en/userguide/Subscribing-To-a-Mistral-Service-and-Deploying-it.html) to deploy a service with the model of your choice.

### Querying the model (chat completion)[​](#querying-the-model-chat-completion "Direct link to Querying the model (chat completion)")

Deployed models expose a REST API that you can query using Mistral's SDK or plain HTTP calls. To run the examples below you will need to set the following environment variables:

*   `OUTSCALE_SERVER_URL`: the URL of the VM hosting your Mistral model
*   `OUTSCALE_MODEL_NAME`: the name of the model to query (e.g. `small-2409`, `codestral-2405`)

*   cURL
*   Python
*   TypeScript

echo $OUTSCALE_SERVER_URL/v1/chat/completionsecho $OUTSCALE_MODEL_NAMEcurl --location $OUTSCALE_SRV_URL/v1/chat/completions \  --header "Content-Type: application/json" \  --header "Accept: application/json" \  --data '{      "model": "'"$OUTSCALE_MODEL_NAME"'",      "temperature": 0,      "messages": [        {"role": "user", "content": "Who is the best French painter? Answer in one short sentence."}      ],      "stream": false    }'

import osfrom mistralai import Mistralclient = Mistral(server_url=os.environ["OUTSCALE_SERVER_URL"])resp = client.chat.complete(    model=os.environ["OUTSCALE_MODEL_NAME"],    messages=[        {            "role": "user",            "content": "Who is the best French painter? Answer in one short sentence.",        }    ],    temperature=0)print(resp.choices[0].message.content)

import { Mistral } from "@mistralai/mistralai";const client = new Mistral({    serverURL: process.env.OUTSCALE_SERVER_URL || ""});const modelName = process.env.OUTSCALE_MODEL_NAME|| "";async function chatCompletion(user_msg: string) {    const resp = await client.chat.complete({        model: modelName,        messages: [            {                content: user_msg,                role: "user",            },        ],    });    if (resp.choices && resp.choices.length > 0) {        console.log(resp.choices[0]);    }}chatCompletion("Who is the best French painter? Answer in one short sentence.");

### Querying the model (FIM completion)[​](#querying-the-model-fim-completion "Direct link to Querying the model (FIM completion)")

Codestral can be queried using an additional completion mode called fill-in-the-middle (FIM). For more information, see the [code generation section](/capabilities/code_generation/).

*   cURL
*   Python
*   TypeScript

curl --location $OUTSCALE_SERVER_URL/v1/fim/completions \   --header "Content-Type: application/json" \   --header "Accept: application/json" \   --data '{       "model": "'"$OUTSCALE_MODEL_NAME"'",       "prompt": "def count_words_in_file(file_path: str) -> int:",       "suffix": "return n_words",       "stream": false     }'

import os from mistralai import Mistral client = Mistral(server_url=os.environ["OUTSCALE_SERVER_URL"]) resp = client.fim.complete(     model = os.environ["OUTSCALE_MODEL_NAME"],     prompt="def count_words_in_file(file_path: str) -> int:",     suffix="return n_words" ) print(resp.choices[0].message.content)

import { Mistral} from "@mistralai/mistralai"; const client = new Mistral({     serverURL: process.env.OUTSCALE_SERVER_URL || "" }); const modelName = "codestral-2405"; async function fimCompletion(prompt: string, suffix: string) {     const resp = await client.fim.complete({         model: modelName,         prompt: prompt,         suffix: suffix     });     if (resp.choices && resp.choices.length > 0) {         console.log(resp.choices[0]);     } } fimCompletion("def count_words_in_file(file_path: str) -> int:",               "return n_words");

## Going further[​](#going-further "Direct link to Going further")

For more information and examples, you can check:

*   The [Outscale documentation](https://docs.outscale.com/en/userguide/Subscribing-To-a-Mistral-Service-and-Deploying-it.html) explaining how to subscribe to a Mistral service and deploy it.

[

Previous

IBM watsonx.ai

](/deployment/cloud/ibm-watsonx/)[

Next

Self-deployment

](/deployment/self-deployment/overview/)

*   [Introduction](#introduction)
*   [Getting started](#getting-started)
*   [Deploying the model](#deploying-the-model)
*   [Querying the model (chat completion)](#querying-the-model-chat-completion)
*   [Querying the model (FIM completion)](#querying-the-model-fim-completion)
*   [Going further](#going-further)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 202