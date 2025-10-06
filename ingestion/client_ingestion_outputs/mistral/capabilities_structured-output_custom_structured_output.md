---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/capabilities/structured-output/custom_structured_output/"
title: "/capabilities/structured-output/custom_structured_output/"
domain: "docs.mistral.ai"
path: "/capabilities/structured-output/custom_structured_output/"
scraped_time: "2025-09-08T18:10:33.701183"
url_depth: 3
word_count: 897
---

Custom Structured Output | Mistral AI

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
*   Custom Structured Output

On this page

# Custom Structured Outputs

Custom Structured Outputs allow you to ensure the model provides an answer in a very specific JSON format by supplying a clear JSON schema. This approach allows the model to consistently deliver responses with the correct typing and keywords.

*   python
*   typescript
*   curl

Here is an example of how to achieve this using the Mistral AI client and Pydantic:

### Define the Data Model[​](#define-the-data-model "Direct link to Define the Data Model")

First, define the structure of the output using a Pydantic model:

from pydantic import BaseModelclass Book(BaseModel):    name: str    authors: list[str]

### Start the completion[​](#start-the-completion "Direct link to Start the completion")

Next, use the Mistral AI python client to make a request and ensure the response adheres to the defined structure using `response_format` set to the corresponding pydantic model:

import osfrom mistralai import Mistralapi_key = os.environ["MISTRAL_API_KEY"]model = "ministral-8b-latest"client = Mistral(api_key=api_key)chat_response = client.chat.parse(    model=model,    messages=[        {            "role": "system",             "content": "Extract the books information."        },        {            "role": "user",             "content": "I recently read 'To Kill a Mockingbird' by Harper Lee."        },    ],    response_format=Book,    max_tokens=256,    temperature=0)

In this example, the `Book` class defines the structure of the output, ensuring that the model's response adheres to the specified format.

There are two types of possible outputs that are easily accessible via our SDK:

1.  The raw JSON output, accessed with `chat_response.choices[0].message.content`:

{  "authors": ["Harper Lee"],  "name": "To Kill a Mockingbird"}

2.  The parsed output, converted into a Pydantic object with `chat_response.choices[0].message.parsed`. In this case, it is a `Book` instance:

name='To Kill a Mockingbird' authors=['Harper Lee']

Here is an example of how to achieve this using the Mistral AI client and Zod:

### Define the Data Model[​](#define-the-data-model-1 "Direct link to Define the Data Model")

First, define the structure of the output using Zod:

import { z } from "zod";const Book = z.object({  name: z.string(),  authors: z.array(z.string()),});

### Start the completion[​](#start-the-completion-1 "Direct link to Start the completion")

Next, use the Mistral AI TypeScript client to make a request and ensure the response adheres to the defined structure using `responseFormat` set to the corresponding Zod schema:

import { Mistral } from "@mistralai/mistralai";const apiKey = process.env.MISTRAL_API_KEY;const client = new Mistral({apiKey: apiKey});const chatResponse = await client.chat.parse({  model: "ministral-8b-latest",  messages: [    {      role: "system",      content: "Extract the books information.",    },    {      role: "user",      content: "I recently read 'To Kill a Mockingbird' by Harper Lee.",    },  ],  responseFormat: Book,  maxTokens: 256,  temperature: 0,});

In this example, the `Book` schema defines the structure of the output, ensuring that the model's response adheres to the specified format.

There are two types of possible outputs that are easily accessible via our SDK:

1.  The raw JSON output, accessed with `chatResponse.choices[0].message.content`:

{  "authors": ["Harper Lee"],  "name": "To Kill a Mockingbird"}

2.  The parsed output, converted into a TypeScript object with `chatResponse.choices[0].message.parsed`. In this case, it is a `Book` object:

{ name: 'To Kill a Mockingbird', authors: [ 'Harper Lee' ] }

The request is structured to ensure that the response adheres to the specified custom JSON schema. The `schema` defines the structure of a Book object with name and authors properties.

curl --location "https://api.mistral.ai/v1/chat/completions" \     --header 'Content-Type: application/json' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY" \     --data '{    "model": "ministral-8b-latest",    "messages": [     {        "role": "system",        "content": "Extract the books information."      },     {        "role": "user",        "content": "I recently read To Kill a Mockingbird by Harper Lee."      }    ],    "response_format": {      "type": "json_schema",      "json_schema": {        "schema": {          "properties": {            "name": {              "title": "Name",              "type": "string"            },            "authors": {              "items": {                "type": "string"              },              "title": "Authors",              "type": "array"            }          },          "required": ["name", "authors"],          "title": "Book",          "type": "object",          "additionalProperties": false        },        "name": "book",        "strict": true      }    },    "max_tokens": 256,    "temperature": 0  }'

note

To better guide the model, the following is being always prepended by default to the System Prompt when using this method:

Your output should be an instance of a JSON object following this schema: {{ json_schema }}

However, it is recommended to add more explanations and iterate on your system prompt to better clarify the expected schema and behavior.

### FAQ[​](#faq "Direct link to FAQ")

**Q: Which models support custom Structured Outputs?**
**A:** All currently available models except for `codestral-mamba` are supported.

[

Previous

Structured Output

](/capabilities/structured-output/structured_output_overview/)[

Next

JSON mode

](/capabilities/structured-output/json_mode/)

*   [Define the Data Model](#define-the-data-model)
*   [Start the completion](#start-the-completion)
*   [Define the Data Model](#define-the-data-model-1)
*   [Start the completion](#start-the-completion-1)
*   [FAQ](#faq)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025