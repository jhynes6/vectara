---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/getting-started/clients/"
title: "/getting-started/clients/"
domain: "docs.mistral.ai"
path: "/getting-started/clients/"
scraped_time: "2025-09-08T18:10:28.097912"
url_depth: 2
word_count: 462
---

SDK Clients | Mistral AI

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
*   SDK Clients

On this page

# SDK Clients

We provide client codes in both Python and Typescript.

## Python[​](#python "Direct link to Python")

You can install our [Python Client](https://github.com/mistralai/client-python) by running:

pip install mistralai

Once installed, you can run the chat completion:

import osfrom mistralai import Mistralapi_key = os.environ["MISTRAL_API_KEY"]model = "mistral-large-latest"client = Mistral(api_key=api_key)chat_response = client.chat.complete(    model = model,    messages = [        {            "role": "user",            "content": "What is the best French cheese?",        },    ])print(chat_response.choices[0].message.content)

See more examples [here](https://github.com/mistralai/client-python/tree/main/examples).

## Typescript[​](#typescript "Direct link to Typescript")

You can install our [Typescript Client](https://github.com/mistralai/client-ts) in your project using:

npm install @mistralai/mistralai

Once installed, you can run the chat completion:

import { Mistral } from '@mistralai/mistralai';const apiKey = process.env.MISTRAL_API_KEY || 'your_api_key';const client = new Mistral({apiKey: apiKey});const chatResponse = await client.chat.complete({  model: 'mistral-tiny',  messages: [{role: 'user', content: 'What is the best French cheese?'}],});console.log('Chat:', chatResponse.choices[0].message.content);

See more examples [here](https://github.com/mistralai/client-js/tree/main/examples).

## Third-party clients[​](#third-party-clients "Direct link to Third-party clients")

Here are some clients built by the community for various other languages:

This section lists third-party clients in other languages provided by the community. Please note that these clients are not actively maintained or supported by Mistral AI. We recommend reaching out to the respective maintainers for any assistance or inquiries.

### CLI[​](#cli "Direct link to CLI")

[icebaker/nano-bots](https://github.com/icebaker/ruby-nano-bots)

### Dart[​](#dart "Direct link to Dart")

[nomtek/mistralai\_client\_dart](https://github.com/nomtek/mistralai_client_dart)

### Elixir[​](#elixir "Direct link to Elixir")

[axonzeta/mistral\_elixir](https://github.com/axonzeta/mistral_elixir)

### Go[​](#go "Direct link to Go")

[Gage-Technologies](https://github.com/Gage-Technologies/mistral-go)

### Java[​](#java "Direct link to Java")

[langchain4j](https://github.com/langchain4j/langchain4j) [Spring AI](https://github.com/spring-projects/spring-ai)

### JavaScript / TypeScript[​](#javascript--typescript "Direct link to JavaScript / TypeScript")

### PHP[​](#php "Direct link to PHP")

[HelgeSverre/mistral](https://github.com/HelgeSverre/mistral) [partITech/php-mistral](https://github.com/partITech/php-mistral)

### Ruby[​](#ruby "Direct link to Ruby")

[gbaptista/mistral-ai](https://github.com/gbaptista/mistral-ai) [wilsonsilva/mistral](https://github.com/wilsonsilva/mistral)

### Rust[​](#rust "Direct link to Rust")

[ivangabriele/mistralai-client-rs](https://github.com/ivangabriele/mistralai-client-rs)

[

Previous

Model weights

](/getting-started/models/weights/)[

Next

Model customization

](/getting-started/customization/)

*   [Python](#python)
*   [Typescript](#typescript)
*   [Third-party clients](#third-party-clients)
*   [CLI](#cli)
*   [Dart](#dart)
*   [Elixir](#elixir)
*   [Go](#go)
*   [Java](#java)
*   [JavaScript / TypeScript](#javascript--typescript)
*   [PHP](#php)
*   [Ruby](#ruby)
*   [Rust](#rust)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copy