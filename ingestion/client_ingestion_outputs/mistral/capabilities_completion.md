---
source: "website"
content_type: "services_products"
url: "https://docs.mistral.ai/capabilities/completion/"
title: "/capabilities/completion/"
domain: "docs.mistral.ai"
path: "/capabilities/completion/"
scraped_time: "2025-09-08T18:09:44.432939"
url_depth: 2
word_count: 1112
---

Text and Chat Completions | Mistral AI

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
*   Text and Chat Completions

On this page

# Text and Chat Completions

The Mistral models allows you to chat with a model that has been fine-tuned to follow instructions and respond to natural language prompts. A prompt is the input that you provide to the Mistral model. It can come in various forms, such as asking a question, giving an instruction, or providing a few examples of the task you want the model to perform. Based on the prompt, the Mistral model generates a text output as a response.

The [chat completion API](https://docs.mistral.ai/api/#tag/chat) accepts a list of chat messages as input and generates a response. This response is in the form of a new chat message with the role "assistant" as output, the "content" of each response can either be a `string` or a `list` of chunks with different kinds of chunk types for different features. Visit our [API spec](https://docs.mistral.ai/api) for more details.

*   python
*   typescript
*   curl

**No streaming**

import osfrom mistralai import Mistralapi_key = os.environ["MISTRAL_API_KEY"]model = "mistral-large-latest"client = Mistral(api_key=api_key)chat_response = client.chat.complete(    model = model,    messages = [        {            "role": "user",            "content": "What is the best French cheese?",        },    ])print(chat_response.choices[0].message.content)

**With streaming**

import osfrom mistralai import Mistralapi_key = os.environ["MISTRAL_API_KEY"]model = "mistral-large-latest"client = Mistral(api_key=api_key)stream_response = client.chat.stream(    model = model,    messages = [        {            "role": "user",            "content": "What is the best French cheese?",        },    ])for chunk in stream_response:    print(chunk.data.choices[0].delta.content)

**With async and without streaming**

import asyncioimport osfrom mistralai import Mistralfrom mistralai.models import UserMessageasync def main():    api_key = os.environ["MISTRAL_API_KEY"]    model = "mistral-large-latest"    client = Mistral(api_key=api_key)    chat_response = await client.chat.complete_async(        model=model,        messages=[UserMessage(content="What is the best French cheese?")],    )    print(chat_response.choices[0].message.content)if __name__ == "__main__":    asyncio.run(main())

**With async and with streaming**

import asyncioimport osfrom mistralai import Mistralasync def main():    api_key = os.environ["MISTRAL_API_KEY"]    model = "mistral-large-latest"    client = Mistral(api_key=api_key)    response = await client.chat.stream_async(        model=model,        messages=[             {                  "role": "user",                  "content": "Who is the best French painter? Answer in JSON.",              },        ],    )    async for chunk in response:        if chunk.data.choices[0].delta.content is not None:            print(chunk.data.choices[0].delta.content, end="")if __name__ == "__main__":    asyncio.run(main())

**No streaming**

import { Mistral } from '@mistralai/mistralai';import * as dotenv from 'dotenv';dotenv.config();const apiKey = process.env.MISTRAL_API_KEY;const client = new Mistral({apiKey: apiKey});async function main() {    const chatResponse = await client.chat.complete({        model: "mistral-large-latest",        messages: [{role: 'user', content: 'What is the best French cheese?'}]    });    console.log('Chat:', chatResponse.choices?.[0]?.message?.content);}main();

**With streaming**

import { Mistral } from "@mistralai/mistralai";import * as dotenv from 'dotenv';dotenv.config();const apiKey = process.env["MISTRAL_API_KEY"];const client = new Mistral({ apiKey: apiKey });async function main() {    const result = await client.chat.stream({        model: "mistral-large-latest",        messages: [{ role: "user", content: "What is the best French cheese?" }],    });    for await (const chunk of result) {        const streamText = chunk.data.choices[0].delta.content;        if (typeof streamText === "string") {            process.stdout.write(streamText);        }    }}main()

curl --location "https://api.mistral.ai/v1/chat/completions" \     --header 'Content-Type: application/json' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY" \     --data '{    "model": "mistral-large-latest",    "messages": [     {        "role": "user",        "content": "What is the best French cheese?"      }    ]  }'

## Chat messages[​](#chat-messages "Direct link to Chat messages")

Chat messages (`messages`) are a collection of prompts or messages, with each message having a specific role assigned to it, such as "system," "user," "assistant," or "tool."

*   A _system message_ is an _optional_ message that sets the behavior and context for an AI assistant in a conversation, such as modifying its personality or providing specific instructions. A system message can include task instructions, personality traits, contextual information, creativity constraints, and other relevant guidelines to help the AI better understand and respond to the user's input. See the [API reference](/api/) for explanations on how to set up a custom system prompt.
*   A _user message_ is a message sent from the perspective of the human in a conversation with an AI assistant. It typically provides a request, question, or comment that the AI assistant should respond to. User prompts allow the human to initiate and guide the conversation, and they can be used to request information, ask for help, provide feedback, or engage in other types of interaction with the AI.
*   An _assistant message_ is a message sent by the AI assistant back to the user. It is usually meant to reply to a previous user message by following its instructions, but you can also find it at the beginning of a conversation, for example to greet the user.
*   A _tool message_ only appears in the context of _function calling_, it is used at the final response formulation step when the model has to format the tool call's output for the user. To learn more about function calling, see the [guide](/capabilities/function_calling/).

When to use `user` prompt vs. `system` message then `user` message?

*   You can either combine your `system` message and `user` message into a single `user` message or separate them into two distinct messages.
*   We recommend you experiment with both ways to determine which one works better for your specific use case.

## Other useful features[​](#other-useful-features "Direct link to Other useful features")

*   The `prefix` flag enables prepending content to the assistant's response content. When used in a message, it allows the addition of an assistant's message at the end of the list, which will be prepended to the assistant's response. For more details on how it works see [prefix](/guides/prefix/).

*   The `safe_prompt` flag is used to force chat completion to be moderated against sensitive content (see [Guardrailing](/capabilities/guardrailing/)).

*   A `stop` sequence allows forcing the model to stop generating after one or more chosen tokens or strings.

**Stop Sequence Example**

curl --location "https://api.mistral.ai/v1/chat/completions" \    --header 'Content-Type: application/json' \    --header 'Accept: application/json' \    --header "Authorization: Bearer $MISTRAL_API_KEY" \    --data '{    "model": "mistral-large-latest",    "messages": [    {        "role": "user",        "content": "What is the capital of France?"      }    ],    "stop": ["Paris"]  }'

[

Previous

Glossary

](/getting-started/glossary/)[

Next

Vision

](/capabilities/vision/)

*   [Chat messages](#chat-messages)
*   [Other useful features](#other-useful-features)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025 Mistra