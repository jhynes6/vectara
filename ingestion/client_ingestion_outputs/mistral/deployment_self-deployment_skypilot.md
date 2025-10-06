---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/deployment/self-deployment/skypilot/"
title: "/deployment/self-deployment/skypilot/"
domain: "docs.mistral.ai"
path: "/deployment/self-deployment/skypilot/"
scraped_time: "2025-09-08T18:10:11.935856"
url_depth: 3
word_count: 536
---

Deploy with SkyPilot | Mistral AI

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
*   Deploy with SkyPilot

On this page

# Deploy with SkyPilot

[SkyPilot](https://skypilot.readthedocs.io/en/latest/) is a framework for running LLMs, AI, and batch jobs on any cloud, offering maximum cost savings, highest GPU availability, and managed execution.

We provide an example SkyPilot config that deploys our models.

## SkyPilot Configuration[​](#skypilot-configuration "Direct link to SkyPilot Configuration")

After [installing SkyPilot](https://skypilot.readthedocs.io/en/latest/getting-started/installation.html), you need to create a configuration file that tells SkyPilot how and where to deploy your inference server, using our pre-built docker container:

*   Mistral-7B
*   Mixtral-8X7B
*   Mixtral-8X22B

resources:   cloud: ${CLOUD_PROVIDER}  accelerators: A10G:1  ports:     - 8000run: |  docker run --gpus all -p 8000:8000 ghcr.io/mistralai/mistral-src/vllm:latest \                   --host 0.0.0.0 \                   --model mistralai/Mistral-7B-Instruct-v0.2 \                   --tensor-parallel-size 1

resources:   cloud: ${CLOUD_PROVIDER}  accelerators: A100-80GB:2  ports:     - 8000run: |  docker run --gpus all -p 8000:8000 ghcr.io/mistralai/mistral-src/vllm:latest \                   --host 0.0.0.0 \                   --model mistralai/Mixtral-8x7B-Instruct-v0.1 \                   --tensor-parallel-size 2

resources:   cloud: ${CLOUD_PROVIDER}  accelerators: A100-80GB:4  ports:     - 8000run: |  docker run --gpus all -p 8000:8000 ghcr.io/mistralai/mistral-src/vllm:latest \                   --host 0.0.0.0 \                   --model mistralai/Mixtral-8x22B-Instruct-v0.1 \                   --tensor-parallel-size 4

Once these environment variables are set, you can use `sky launch` to launch the inference server with the appropriate model name, for example with `mistral-7b`:

sky launch -c mistral-7b mistral-7b-v0.1.yaml --region us-east-1

caution

When deployed that way, the model will be accessible to the whole world. You **must** secure it, either by exposing it exclusively on your private network (change the `--host` Docker option for that), by adding a load-balancer with an authentication mechanism in front of it, or by configuring your instance networking properly.

### Test it out![​](#test-it-out "Direct link to Test it out!")

To easily retrieve the IP address of the deployed `mistral-7b` cluster you can use:

sky status --ip mistral-7b

You can then use curl to send a completion request:

IP=$(sky status --ip cluster-name)curl http://$IP:8000/v1/completions \  -H "Content-Type: application/json" \  -d '{      "model": "mistralai/Mistral-7B-v0.1",      "prompt": "My favourite condiment is",      "max_tokens": 25  }'

## Usage Quotas[​](#usage-quotas "Direct link to Usage Quotas")

Many cloud providers require you to explicitly request access to powerful GPU instances. Read [SkyPilot's guide](https://skypilot.readthedocs.io/en/latest/cloud-setup/quota.html) on how to do this.

[

Previous

TensorRT

](/deployment/self-deployment/trt/)[

Next

Deploy with Cerebrium

](/deployment/self-deployment/cerebrium/)

*   [SkyPilot Configuration](#skypilot-configuration)
*   [Test it out!](#test-it-out)
*   [Usage Quotas](#usage-quotas)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025 Mist