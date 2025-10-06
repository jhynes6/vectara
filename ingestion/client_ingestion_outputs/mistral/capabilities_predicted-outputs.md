---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/capabilities/predicted-outputs/"
title: "/capabilities/predicted-outputs/"
domain: "docs.mistral.ai"
path: "/capabilities/predicted-outputs/"
scraped_time: "2025-09-08T18:10:23.986391"
url_depth: 2
word_count: 717
---

Predicted outputs | Mistral AI

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
*   Predicted outputs

On this page

# Predicted outputs

Predicted Outputs optimizes response time by leveraging known or predictable content. This approach minimizes latency while maintaining high output quality. In tasks such as editing large texts, modifying code, or generating template-based responses, significant portions of the output are often predetermined. By predefining these expected parts with Predicted Outputs, models can allocate more computational resources to the unpredictable elements, improving overall efficiency.

## Example: Code modification[​](#example-code-modification "Direct link to Example: Code modification")

Predicted Outputs shine in scenarios where you need to regenerate text documents or code files with minor modifications. The key parameter introduced is the `prediction` parameter, which enables users to define predicted outputs. For example, imagine you want your model to update the model used in a fine-tuning job. You can include the code snippet you'd like to modify as both the user prompt and the predicted output.

*   python
*   typescript
*   curl

import osfrom mistralai import Mistralapi_key = os.environ["MISTRAL_API_KEY"]model = "mistral-large-latest"client = Mistral(api_key=api_key)code = """created_jobs = client.fine_tuning.jobs.create(    model="open-mistral-7b",     training_files=[{"file_id": ultrachat_chunk_train.id, "weight": 1}],    validation_files=[ultrachat_chunk_eval.id],     hyperparameters={        "training_steps": 10,        "learning_rate":0.0001    },    auto_start=False)"""prompt = "Change the model name from open-mistral-7b to open-mistral-nemo. Respond only with code, no explanation, no formatting."chat_response = client.chat.complete(    model= model,    messages = [        {            "role": "user",            "content": prompt,        },        {            "role": "user",            "content": code        },    ],    prediction = {        "type": "content",        "content": code    })print(chat_response.choices[0].message.content)

import { Mistral } from '@mistralai/mistralai';const apiKey = process.env.MISTRAL_API_KEY;const client = new Mistral({apiKey: apiKey});const code = `created_jobs = client.fine_tuning.jobs.create(    model="open-mistral-7b",     training_files=[{"file_id": ultrachat_chunk_train.id, "weight": 1}],    validation_files=[ultrachat_chunk_eval.id],     hyperparameters={        "training_steps": 10,        "learning_rate":0.0001    },    auto_start=False)`.trim();const prompt = `Change the model name from open-mistral-7b to open-mistral-nemo. Respond only with code, no explanation, no formatting.`;const chatResponse = await client.chat.complete({    model: "mistral-large-latest",    messages: [        {            role: 'user',             content: prompt        },        {            role: "user",            content: code        },    ],    prediction: {        type: "content",        content: code     },});console.log('Chat:', chatResponse.choices[0].message.content);

curl --location "https://api.mistral.ai/v1/chat/completions" \     --header 'Content-Type: application/json' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY" \     --data '{    "model": "mistral-large-latest",    "messages": [        {"role": "user", "content": "Change the model name from open-mistral-7b to open-mistral-nemo. Respond only with code, no explanation, no formatting."},        {"role": "user", "content": "$CODE"}    ],    "prediction": {        "type": "content",        "content": "$CODE"    }  }'

## FAQ[​](#faq "Direct link to FAQ")

### Which model supports predicted outputs?[​](#which-model-supports-predicted-outputs "Direct link to Which model supports predicted outputs?")

As of now, `codestral-2501` and `mistral-large-2411` support predicted outputs.

### How does predicted outputs affect pricing?[​](#how-does-predicted-outputs-affect-pricing "Direct link to How does predicted outputs affect pricing?")

Currently, predicted outputs do not impact pricing.

### Which parameters are not supported when using Predicted Outputs?[​](#which-parameters-are-not-supported-when-using-predicted-outputs "Direct link to Which parameters are not supported when using Predicted Outputs?")

`n` (number of completions to return for each request) is not supported when using predicted outputs.

### Does the Position of Certain Sentences or Words in the Prediction Matter?[​](#does-the-position-of-certain-sentences-or-words-in-the-prediction-matter "Direct link to Does the Position of Certain Sentences or Words in the Prediction Matter?")

No, the placement of sentences or words in your prediction does not affect its effectiveness. Predictions can appear anywhere within the generated response and still help reduce the API's output latency.

[

Previous

Batch Inference

](/capabilities/batch/)[

Next

Agents Introduction

](/agents/agents_introduction/)

*   [Example: Code modification](#example-code-modification)
*   [FAQ](#faq)
*   [Which model supports predicted outputs?](#which-model-supports-predicted-outputs)
*   [How does predicted outputs affect pricing?](#how-does-predicted-outputs-affect-pricing)
*   [Which parameters are not supported when using Predicted Outputs?](#which-parameters-are-not-supported-when-using-predicted-outputs)
*   [Does the Position of Certain Sentences or Words in the Prediction Matter?](#does-the-position-of-certain-sentences-or-words-in-the-prediction-matter)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 202