---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/deployment/self-deployment/cloudflare/"
title: "/deployment/self-deployment/cloudflare/"
domain: "docs.mistral.ai"
path: "/deployment/self-deployment/cloudflare/"
scraped_time: "2025-09-08T18:10:20.988091"
url_depth: 3
word_count: 459
---

Deploy with Cloudflare Workers AI | Mistral AI

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
*   Deploy with Cloudflare Workers AI

On this page

# Deploy with Cloudflare Workers AI

[Cloudflare](https://www.cloudflare.com/en-gb/) is a web performance and security company that provides content delivery network (CDN), DDoS protection, Internet security, and distributed domain name server services. Cloudflare launched Workers AI, which allows developers to run LLMs models powered by serverless GPUs on Cloudflare’s global network.

To learn more about Mistral models on Workers AI you can read the dedicated [Cloudflare documentation page](https://developers.cloudflare.com/workers-ai/models/mistral-7b-instruct-v0.1/).

## Set-up[​](#set-up "Direct link to Set-up")

To set-up Workers AI on Cloudflare, you need to create an account on the [Cloudflare dashboard](https://dash.cloudflare.com/), get your account ID, and generate a token with Workers AI permissions. You can then send a completion request:

*   curl
*   typescript
*   python

curl https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/mistral/mistral-7b-instruct-v0.1 \  -X POST \  -H "Authorization: Bearer {API_TOKEN}" \  -d '{ "messages": [{ "role": "user", "content": "[INST] 2 + 2 ? [/INST]" }]}'

async function run(model, prompt) {  const messages = [    { role: "user", content: prompt },  ];  const response = await fetch(    `https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/${model}`,    {      headers: { Authorization: "Bearer {API_TOKEN}" },      method: "POST",      body: JSON.stringify({ messages }),    }  );  const result = await response.json();  return result;}run("@cf/mistral/mistral-7b-instruct-v0.1", "[INST] 2 + 2 ? [/INST]").then(  (response) => {    console.log(JSON.stringify(response));  });

import requestsAPI_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/"headers = {"Authorization": "Bearer {API_TOKEN}"}def run(model, prompt):  input = {    "messages": [      { "role": "user", "content": prompt }    ]  }  response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)  return response.json()output = run("@cf/mistral/mistral-7b-instruct-v0.1", "[INST] 2 + 2 = ? [/INST]")print(output)

Here is the output you should receive

{'result': {'response': '2 + 2 = 4.'}, 'success': True, 'errors': [], 'messages': []}

[

Previous

Deploy with Cerebrium

](/deployment/self-deployment/cerebrium/)[

Next

Text Generation Inference

](/deployment/self-deployment/tgi/)

*   [Set-up](#set-up)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025 Mistra