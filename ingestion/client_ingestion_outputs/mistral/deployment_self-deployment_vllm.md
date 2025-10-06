---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/deployment/self-deployment/vllm/"
title: "/deployment/self-deployment/vllm/"
domain: "docs.mistral.ai"
path: "/deployment/self-deployment/vllm/"
scraped_time: "2025-09-08T18:09:41.698911"
url_depth: 3
word_count: 1299
---

vLLM | Mistral AI

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
*   vLLM

On this page

# vLLM

[vLLM](https://github.com/vllm-project/vllm) is an open-source LLM inference and serving engine. It is particularly appropriate as a target platform for self-deploying Mistral models on-premise.

## Pre-requisites[​](#pre-requisites "Direct link to Pre-requisites")

*   The hardware requirements for vLLM are listed on its [installation documentation page](https://docs.vllm.ai/en/latest/getting_started/installation.html).
*   By default, vLLM sources the model weights from Hugging Face. To access Mistral model repositories you need to be authenticated on Hugging Face, so an access token `HF_TOKEN` with the `READ` permission will be required. You should also make sure that you have accepted the conditions of access on each model card page.
*   If you already have the model artifacts on your infrastructure you can use them directly by pointing vLLM to their local path instead of a Hugging Face model ID. In this scenario you will be able to skip all Hugging Face related setup steps.

## Getting started[​](#getting-started "Direct link to Getting started")

The following sections will guide you through the process of deploying and querying Mistral models on vLLM.

### Installing vLLM[​](#installing-vllm "Direct link to Installing vLLM")

*   Create a Python virtual environment and install the `vllm` package (version `>=0.6.1.post1` to ensure maximum compatibility with all Mistral models).

*   Authenticate on the HuggingFace Hub using your access token `$HF_TOKEN` :

huggingface-cli login --token $HF_TOKEN

### Offline mode inference[​](#offline-mode-inference "Direct link to Offline mode inference")

When using vLLM in _offline mode_ the model is loaded and used for one-off batch inference workloads.

*   Text input (Mistral NeMo)
*   Text input (Mistral Small)
*   Image + text input (Pixtral-12B)

from vllm import LLMfrom vllm.sampling_params import SamplingParamsmodel_name = "mistralai/Mistral-NeMo-Instruct-2407"sampling_params = SamplingParams(max_tokens=8192)llm = LLM(    model=model_name,    tokenizer_mode="mistral",    load_format="mistral",    config_format="mistral",)messages = [    {        "role": "user",        "content": "Who is the best French painter. Answer with detailed explanations.",    }]res = llm.chat(messages=messages, sampling_params=sampling_params)print(res[0].outputs[0].text)

from vllm import LLMfrom vllm.sampling_params import SamplingParamsmodel_name = "mistralai/Mistral-Small-Instruct-2409"sampling_params = SamplingParams(max_tokens=8192)llm = LLM(    model=model_name,    tokenizer_mode="mistral",    load_format="mistral",    config_format="mistral",)messages = [    {        "role": "user",        "content": "Who is the best French painter. Answer with detailed explanations.",    }]res = llm.chat(messages=messages, sampling_params=sampling_params)print(res[0].outputs[0].text)

Suppose you want to caption the following images:

[![](/img/laptop.png)](https://picsum.photos/id/1/512/512)[![](/img/countryside.png)](https://picsum.photos/id/11/512/512)[![](/img/vintage_car.png)](https://picsum.photos/id/111/512/512)

You can do so by running the following code:

from vllm import LLMfrom vllm.sampling_params import SamplingParamsmodel_name = "mistralai/Pixtral-12B-2409"max_img_per_msg = 3sampling_params = SamplingParams(max_tokens=8192)llm = LLM(    model=model_name,    tokenizer_mode="mistral",    load_format="mistral",    config_format="mistral",    limit_mm_per_prompt={"image": max_img_per_msg},)urls = [f"https://picsum.photos/id/{id}/512/512" for id in ["1", "11", "111"]]messages = [    {        "role": "user",        "content": [            {"type": "text", "text": "Describe this image"},            ] + [{"type": "image_url", "image_url": {"url": f"{u}"}} for u in urls],    },]res = llm.chat(messages=messages, sampling_params=sampling_params)print(res[0].outputs[0].text)

### Server mode inference[​](#server-mode-inference "Direct link to Server mode inference")

In _server mode_, vLLM spawns an HTTP server that continuously waits for clients to connect and send requests concurrently. The server exposes a REST API that implements the OpenAI protocol, allowing you to directly reuse existing code relying on the OpenAI API.

*   Text input (Mistral NeMo)
*   Text input (Mistral Small)
*   Image + text input (Pixtral-12B)

Start the inference server to deploy your model, e.g. for Mistral NeMo:

vllm serve mistralai/Mistral-Nemo-Instruct-2407 \  --tokenizer_mode mistral \  --config_format mistral \  --load_format mistral

You can now run inference requests with text input:

*   cURL
*   Python

curl --location 'http://localhost:8000/v1/chat/completions' \    --header 'Content-Type: application/json' \    --header 'Authorization: Bearer token' \    --data '{        "model": "mistralai/Mistral-Nemo-Instruct-2407",        "messages": [          {            "role": "user",            "content": "Who is the best French painter? Answer in one short sentence."          }        ]      }'

import httpxurl = 'http://localhost:8000/v1/chat/completions'headers = {    'Content-Type': 'application/json',    'Authorization': 'Bearer token'}data = {    "model": "mistralai/Mistral-Nemo-Instruct-2407",    "messages": [        {            "role": "user",            "content": "Who is the best French painter? Answer in one short sentence."        }    ]}response = httpx.post(url, headers=headers, json=data)print(response.json())

Start the inference server to deploy your model, e.g. for Mistral Small:

vllm serve mistralai/Mistral-Small-Instruct-2409 \  --tokenizer_mode mistral \  --config_format mistral \  --load_format mistral

You can now run inference requests with text input:

*   cURL
*   Python

curl --location 'http://localhost:8000/v1/chat/completions' \    --header 'Content-Type: application/json' \    --header 'Authorization: Bearer token' \    --data '{        "model": "mistralai/Mistral-Small-Instruct-2409",        "messages": [          {            "role": "user",            "content": "Who is the best French painter? Answer in one short sentence."          }        ]      }'

import httpxurl = 'http://localhost:8000/v1/chat/completions'headers = {    'Content-Type': 'application/json',    'Authorization': 'Bearer token'}data = {    "model": "mistralai/Mistral-Small-Instruct-2409",    "messages": [        {            "role": "user",            "content": "Who is the best French painter? Answer in one short sentence."        }    ]}response = httpx.post(url, headers=headers, json=data)print(response.json())

Start the inference server to deploy your model, e.g. for Pixtral-12B:

vllm serve mistralai/Pixtral-12B-2409 \    --tokenizer_mode mistral \    --config_format mistral \    --load_format mistral

info

*   The default number of image inputs per prompt is set to 1. To increase it, set the `--limit_mm_per_prompt` option (e.g. `--limit_mm_per_prompt 'image=4'`).

*   If you encounter memory issues, set the `--max_model_len` option to reduce the memory requirements of vLLM (e.g. `--max_model_len 16384`). More troubleshooting details can be found in the [vLLM documentation](https://qwen.readthedocs.io/en/latest/deployment/vllm.html#troubleshooting).

You can now run inference requests with images and text inputs. Suppose you want to caption the following image:

[![](/img/doggo.png)](https://picsum.photos/id/237/512/512)

You can prompt the model and retrieve its response like so:

*   cURL
*   Python

curl --location 'http://localhost:8000/v1/chat/completions' \--header 'Content-Type: application/json' \--header 'Authorization: Bearer token' \--data '{    "model": "mistralai/Pixtral-12B-2409",    "messages": [      {        "role": "user",        "content": [            {"type" : "text", "text": "Describe this image in a short sentence."},            {"type": "image_url", "image_url": {"url": "https://picsum.photos/id/237/200/300"}}        ]      }    ]  }'

import httpx  url = "http://localhost:8000/v1/chat/completions"  headers = {"Content-Type": "application/json", "Authorization": "Bearer token"}  data = {      "model": "mistralai/Pixtral-12B-2409",      "messages": [          {              "role": "user",              "content": [                  {"type": "text", "text": "Describe this image in a short sentence."},                  {                      "type": "image_url",                      "image_url": {"url": "https://picsum.photos/id/237/200/300"},                  },              ],          }      ],  }  response = httpx.post(url, headers=headers, json=data)  print(response.json())

## Deploying with Docker[​](#deploying-with-docker "Direct link to Deploying with Docker")

If you are looking to deploy vLLM as a containerized inference server you can leverage the project's official Docker image (see more details in the [vLLM Docker documentation](https://docs.vllm.ai/en/latest/serving/deploying_with_docker.html)).

*   Set the HuggingFace access token environment variable in your shell:

export HF_TOKEN=your-access-token

*   Run the Docker command to start the container:

*   Mistral NeMo
*   Mistral Small
*   Pixtral-12B

docker run --runtime nvidia --gpus all \    -v ~/.cache/huggingface:/root/.cache/huggingface \    --env "HUGGING_FACE_HUB_TOKEN=${HF_TOKEN}" \    -p 8000:8000 \    --ipc=host \    vllm/vllm-openai:latest \    --model mistralai/Mistral-NeMo-Instruct-2407 \    --tokenizer_mode mistral \    --load_format mistral \    --config_format mistral

docker run --runtime nvidia --gpus all \    -v ~/.cache/huggingface:/root/.cache/huggingface \    --env "HUGGING_FACE_HUB_TOKEN=${HF_TOKEN}" \    -p 8000:8000 \    --ipc=host \    vllm/vllm-openai:latest \    --model mistralai/Mistral-Small-Instruct-2409 \    --tokenizer_mode mistral \    --load_format mistral \    --config_format mistral

docker run --runtime nvidia --gpus all \    -v ~/.cache/huggingface:/root/.cache/huggingface \    --env "HUGGING_FACE_HUB_TOKEN=${HF_TOKEN}" \    -p 8000:8000 \    --ipc=host \    vllm/vllm-openai:latest \    --model mistralai/Pixtral-12B-2409 \    --tokenizer_mode mistral \    --load_format mistral \    --config_format mistral

Once the container is up and running you will be able to run inference on your model using the same code as in a standalone deployment.

[

Previous

Self-deployment

](/deployment/self-deployment/overview/)[

Next

TensorRT

](/deployment/self-deployment/trt/)

*   [Pre-requisites](#pre-requisites)
*   [Getting started](#getting-started)
*   [Installing vLLM](#installing-vllm)
*   [Offline mode inference](#offline-mode-inference)
*   [Server mode inference](#server-mode-inference)
*   [Deploying with Docker](#deploying-with-docker)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 202