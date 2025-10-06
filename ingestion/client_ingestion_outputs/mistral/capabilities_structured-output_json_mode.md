---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/capabilities/structured-output/json_mode/"
title: "/capabilities/structured-output/json_mode/"
domain: "docs.mistral.ai"
path: "/capabilities/structured-output/json_mode/"
scraped_time: "2025-09-08T18:10:05.432801"
url_depth: 3
word_count: 381
---

JSON mode | Mistral AI

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

*   [Custom Structured Output](/capabilities/structured-output/custom_structured_output/)
*   [JSON mode](/capabilities/structured-output/json_mode/)
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
*   [Structured Output](/capabilities/structured-output/structured_output_overview/)
*   JSON mode

# JSON mode

Users have the option to set `response_format` to `{"type": "json_object"}` to enable JSON mode. Currently, JSON mode is available for all of our models through API.

*   python
*   typescript
*   curl

import osfrom mistralai import Mistralapi_key = os.environ["MISTRAL_API_KEY"]model = "mistral-large-latest"client = Mistral(api_key=api_key)messages = [    {        "role": "user",        "content": "What is the best French meal? Return the name and the ingredients in short JSON object.",    }]chat_response = client.chat.complete(      model = model,      messages = messages,      response_format = {          "type": "json_object",      })print(chat_response.choices[0].message.content)

Example output:

{"name": "Coq au Vin", "ingredients": ["chicken", "red wine", "bacon", "mushrooms", "onions", "garlic", "chicken broth", "thyme", "bay leaf", "flour", "butter", "olive oil", "salt", "pepper"]}

import { Mistral } from "mistralai";const apiKey = process.env.MISTRAL_API_KEY;const mistral = new Mistral({apiKey: apiKey});const chatResponse = await mistral.chat.complete({    model: "mistral-large-latest",    messages: [{role: 'user', content: 'What is the best French meal? Return the name and the ingredients in JSON format.'}],    responseFormat: {type: 'json_object'},    });console.log('JSON:', chatResponse.choices[0].message.content)

curl --location "https://api.mistral.ai/v1/chat/completions" \     --header 'Content-Type: application/json' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY" \     --data '{    "model": "mistral-large-latest",    "messages": [     {        "role": "user",        "content": "What is the best French cheese? Return the product and produce location in JSON format"      }    ],    "response_format": {"type": "json_object"}  }'

[

Previous

Custom Structured Output

](/capabilities/structured-output/custom_structured_output/)[

Next

Moderation

](/capabilities/guardrailing/)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025 Mistral AI