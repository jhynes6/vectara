---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/deployment/self-deployment/tgi/"
title: "/deployment/self-deployment/tgi/"
domain: "docs.mistral.ai"
path: "/deployment/self-deployment/tgi/"
scraped_time: "2025-09-08T18:10:31.558404"
url_depth: 3
word_count: 652
---

Text Generation Inference | Mistral AI

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

*   [vLLM](/deployment/self-deployment/vllm/)
*   [TensorRT](/deployment/self-deployment/trt/)
*   [Deploy with SkyPilot](/deployment/self-deployment/skypilot/)
*   [Deploy with Cerebrium](/deployment/self-deployment/cerebrium/)
*   [Deploy with Cloudflare Workers AI](/deployment/self-deployment/cloudflare/)
*   [Text Generation Inference](/deployment/self-deployment/tgi/)
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
*   [Self-deployment](/deployment/self-deployment/overview/)
*   Text Generation Inference

On this page

# Text Generation Inference

Text Generation Inference (TGI) is a toolkit for deploying and serving Large Language Models (LLMs). TGI enables high-performance text generation for the most popular open-access LLMs. Among other features, it has quantization, tensor parallelism, token streaming, continuous batching, flash attention, guidance, and more.

The easiest way of getting started with TGI is using the official Docker container.

## Deploying[​](#deploying "Direct link to Deploying")

*   Mistral-7B
*   Mixtral-8X7B
*   Mixtral-8X22B

model=mistralai/Mistral-7B-Instruct-v0.3

model=mistralai/Mixtral-8x22B-Instruct-v0.1

model=mistralai/Mixtral-8x22B-Instruct-v0.1

volume=$PWD/data # share a volume with the Docker container to avoid downloading weights every rundocker run --gpus all --shm-size 1g -p 8080:80 -v $volume:/data  \    -e HUGGING_FACE_HUB_TOKEN=$HUGGING_FACE_HUB_TOKEN \    ghcr.io/huggingface/text-generation-inference:2.0.3 \    --model-id $model

This will spawn a TGI instance exposing an OpenAI-like API, as documented in the [API section](/api/).

Make sure to set the `HUGGING_FACE_HUB_TOKEN` environment variable to your [Hugging Face user access token](https://huggingface.co/docs/hub/security-tokens). To use Mistral models, you must first visit the corresponding model page and fill out the small form. You then automatically get access to the model.

If the model does not fit in your GPU, you can also use quantization methods (AWQ, GPTQ, etc.). You can find all TGI launch options at [their documentation](https://huggingface.co/docs/text-generation-inference/en/basic_tutorials/launcher).

## Using the API[​](#using-the-api "Direct link to Using the API")

### With chat-compatible endpoint[​](#with-chat-compatible-endpoint "Direct link to With chat-compatible endpoint")

TGI supports the [Messages API](https://huggingface.co/docs/text-generation-inference/en/messages_api) which is compatible with Mistral and OpenAI Chat Completion API.

*   Using MistralClient
*   Using OpenAI Client
*   Using cURL

from mistralai.client import MistralClientfrom mistralai.models.chat_completion import ChatMessage# init the client but point it to TGIclient = MistralClient(api_key="-", endpoint="http://127.0.0.1:8080")chat_response = client.chat(    model="-",    messages=[      ChatMessage(role="user", content="What is the best French cheese?")    ])print(chat_response.choices[0].message.content)

from openai import OpenAI# init the client but point it to TGIclient = OpenAI(api_key="-", base_url="http://127.0.0.1:8080/v1")chat_response = client.chat.completions.create(    model="-",    messages=[      {"role": "user", "content": "What is deep learning?"}    ])print(chat_response)

curl http://127.0.0.1:8080/v1/chat/completions \    -X POST \    -d '{  "model": "tgi",  "messages": [    {      "role": "user",      "content": "What is deep learning?"    }  ]}' \    -H 'Content-Type: application/json'

### Using a generate endpoint[​](#using-a-generate-endpoint "Direct link to Using a generate endpoint")

If you want more control over what you send to the server, you can use the `generate` endpoint. In this case, you're responsible of formatting the prompt with the correct template and stop tokens.

*   Using Python
*   Using JavaScript
*   Using cURL

# Make sure to install the huggingface_hub package beforefrom huggingface_hub import InferenceClientclient = InferenceClient(model="http://127.0.0.1:8080")client.text_generation(prompt="What is Deep Learning?")

async function query() {    const response = await fetch(        'http://127.0.0.1:8080/generate',        {            method: 'POST',            headers: { 'Content-Type': 'application/json'},            body: JSON.stringify({                'inputs': 'What is Deep Learning?'            })        }    );}query().then((response) => {    console.log(JSON.stringify(response));});

curl 127.0.0.1:8080/generate \-X POST \-d '{"inputs":"What is Deep Learning?","parameters":{"max_new_tokens":20}}' \-H 'Content-Type: application/json'

[

Previous

Deploy with Cloudflare Workers AI

](/deployment/self-deployment/cloudflare/)[

Next

Prompting capabilities

](/guides/prompting_capabilities/)

*   [Deploying](#deploying)
*   [Using the API](#using-the-api)
*   [With chat-compatible endpoint](#with-chat-compatible-endpoint)
*   [Using a generate endpoint](#using-a-generate-endpoint)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025 Mi