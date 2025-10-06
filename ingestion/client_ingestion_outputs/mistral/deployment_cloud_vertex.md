---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/deployment/cloud/vertex/"
title: "/deployment/cloud/vertex/"
domain: "docs.mistral.ai"
path: "/deployment/cloud/vertex/"
scraped_time: "2025-09-08T18:10:16.725118"
url_depth: 3
word_count: 884
---

Vertex AI | Mistral AI

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
*   Vertex AI

On this page

# Vertex AI

## Introduction[​](#introduction "Direct link to Introduction")

Mistral AI's open and commercial models can be deployed on the Google Cloud Vertex AI platform as fully managed endpoints. Mistral models on Vertex AI are serverless services so you don't have to manage any infrastructure.

As of today, the following models are available:

*   Mistral Large (24.11, 24.07)
*   Codestral (24.05)
*   Mistral Nemo

For more details, visit the [models](/getting-started/models/models_overview/) page.

## Getting started[​](#getting-started "Direct link to Getting started")

The following sections outline the steps to deploy and query a Mistral model on the Vertex AI platform.

### Requesting access to the model[​](#requesting-access-to-the-model "Direct link to Requesting access to the model")

The following items are required:

*   Access to a Google Cloud Project with the Vertex AI API enabled
*   Relevant IAM permissions to be able to enable the model and query endpoints through the following roles:
*   [Vertex AI User IAM role](https://cloud.google.com/vertex-ai/docs/general/access-control#aiplatform.user).
*   Consumer Procurement Entitlement Manager role

To enable the model of your choice, navigate to its card in the [Vertex Model Garden catalog](https://cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models), then click on "Enable".

### Querying the model (chat completion)[​](#querying-the-model-chat-completion "Direct link to Querying the model (chat completion)")

Available models expose a REST API that you can query using Mistral's SDKs or plain HTTP calls.

To run the examples below:

*   Install the `gcloud` CLI to authenticate against the Google Cloud APIs, please refer to [this page](https://cloud.google.com/docs/authentication/provide-credentials-adc#google-idp) for more details.
*   Set the following environment variables:
*   `GOOGLE_CLOUD_REGION`: The target cloud region.
*   `GOOGLE_CLOUD_PROJECT_ID`: The name of your project.
*   `VERTEX_MODEL_NAME`: The name of the model to query (e.g. `mistral-large`).
*   `VERTEX_MODEL_VERSION`: The version of the model to query (e.g. `2407`).

*   cURL
*   Python
*   TypeScript

base_url="https://$GOOGLE_CLOUD_REGION-aiplatform.googleapis.com/v1/projects/$GOOGLE_CLOUD_PROJECT_ID/locations/$GOOGLE_CLOUD_REGION/publishers/mistralai/models"model_version="$VERTEX_MODEL_NAME@$VERTEX_MODEL_VERSION"url="$base_url/$model_version:rawPredict"curl --location $url\  --header "Content-Type: application/json" \  --header "Authorization: Bearer $(gcloud auth print-access-token)" \  --data '{      "model": "'"$VERTEX_MODEL_NAME"'",      "temperature": 0,      "messages": [        {"role": "user", "content": "Who is the best French painter? Answer in one short sentence."}      ],      "stream": false    }'

This code requires a virtual environment with the following packages:

*   `mistralai[gcp]>=1.0.0`

import osfrom mistralai_gcp import MistralGoogleCloudregion = os.environ.get("GOOGLE_CLOUD_REGION")project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_NAME")model_name = os.environ.get("VERTEX_MODEL_NAME")model_version = os.environ.get("VERTEX_MODEL_VERSION")client = MistralGoogleCloud(region=region, project_id=project_id)resp = client.chat.complete(    model = f"{model_name}-{model_version}",    messages=[        {            "role": "user",            "content": "Who is the best French painter? Answer in one short sentence.",        }    ],)print(resp.choices[0].message.content)

This code requires the following package:

*   `@mistralai/mistralai-gcp` (version >= `1.0.0`)

import { MistralGoogleCloud } from "@mistralai/mistralai-gcp";const client = new MistralGoogleCloud({    region: process.env.GOOGLE_CLOUD_REGION || "",    projectId: process.env.GOOGLE_CLOUD_PROJECT_ID || "",});const modelName = process.env.VERTEX_MODEL_NAME|| "";const modelVersion = process.env.VERTEX_MODEL_VERSION || "";async function chatCompletion(user_msg: string) {    const resp = await client.chat.complete({        model: modelName + "-" + modelVersion,        messages: [            {                content: user_msg,                role: "user",            },        ],    });    if (resp.choices && resp.choices.length > 0) {        console.log(resp.choices[0]);    }}chatCompletion("Who is the best French painter? Answer in one short sentence.");

### Querying the model (FIM completion)[​](#querying-the-model-fim-completion "Direct link to Querying the model (FIM completion)")

Codestral can be queried using an additional completion mode called fill-in-the-middle (FIM). For more information, see the [code generation section](/capabilities/code_generation/).

*   cURL
*   Python
*   TypeScript

VERTEX_MODEL_NAME=codestralVERTEX_MODEL_VERSION=2405base_url="https://$GOOGLE_CLOUD_REGION-aiplatform.googleapis.com/v1/projects/$GOOGLE_CLOUD_PROJECT_ID/locations/$GOOGLE_CLOUD_REGION/publishers/mistralai/models"model_version="$VERTEX_MODEL_NAME@$VERTEX_MODEL_VERSION"url="$base_url/$model_version:rawPredict"curl --location $url\  --header "Content-Type: application/json" \  --header "Authorization: Bearer $(gcloud auth print-access-token)" \  --data '{      "model":"'"$VERTEX_MODEL_NAME"'",      "prompt": "def count_words_in_file(file_path: str) -> int:",      "suffix": "return n_words",      "stream": false    }'

import osfrom mistralai_gcp import MistralGoogleCloudregion = os.environ.get("GOOGLE_CLOUD_REGION")project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_NAME")model_name = "codestral"model_version = "2405"client = MistralGoogleCloud(region=region, project_id=project_id)resp = client.fim.complete(    model = f"{model_name}-{model_version}",    prompt="def count_words_in_file(file_path: str) -> int:",    suffix="return n_words")print(resp.choices[0].message.content)

import { MistralGoogleCloud } from "@mistralai/mistralai-gcp";const client = new MistralGoogleCloud({    region: process.env.GOOGLE_CLOUD_REGION || "",    projectId: process.env.GOOGLE_CLOUD_PROJECT_ID || "",});const modelName = "codestral";const modelVersion = "2405";async function fimCompletion(prompt: string, suffix: string) {    const resp = await client.fim.complete({        model: modelName + "-" + modelVersion,        prompt: prompt,        suffix: suffix    });    if (resp.choices && resp.choices.length > 0) {        console.log(resp.choices[0]);    }}fimCompletion("def count_words_in_file(file_path: str) -> int:",              "return n_words");

## Going further[​](#going-further "Direct link to Going further")

For more information and examples, you can check:

*   The Google Cloud [Partner Models](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/mistral) documentation page.
*   The Vertex Model Cards for [Mistral Large](https://console.cloud.google.com/vertex-ai/publishers/mistralai/model-garden/mistral-large), [Mistral-NeMo](https://console.cloud.google.com/vertex-ai/publishers/mistralai/model-garden/mistral-nemo) and [Codestral](https://console.cloud.google.com/vertex-ai/publishers/mistralai/model-garden/codestral).
*   The [Getting Started Colab Notebook](https://colab.research.google.com/github/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/official/generative_ai/mistralai_intro.ipynb) for Mistral models on Vertex, along with the [source file on GitHub](https://github.com/GoogleCloudPlatform/vertex-ai-samples/tree/main/notebooks/official/generative_ai/mistralai_intro.ipynb).

[

Previous

AWS Bedrock

](/deployment/cloud/aws/)[

Next

Snowflake Cortex

](/deployment/cloud/sfcortex/)

*   [Introduction](#introduction)
*   [Getting started](#getting-started)
*   [Requesting access to the model](#requesting-access-to-the-model)
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