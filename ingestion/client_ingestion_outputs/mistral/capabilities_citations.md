---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/capabilities/citations/"
title: "/capabilities/citations/"
domain: "docs.mistral.ai"
path: "/capabilities/citations/"
scraped_time: "2025-09-08T18:10:11.763172"
url_depth: 2
word_count: 1015
---

Citations and References | Mistral AI

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
*   Citations and References

On this page

# Citations and References

Citations enable models to ground their responses and provide references, making them a powerful feature for Retrieval-Augmented Generation (RAG) and agentic applications. This feature allows the model to provide the source of the information extracted from a document or chunk of data from a tool call.

Our models have been deeply trained to ground on documents and provide sources, with a built-in feature to extract references and citations.

## Code Example[​](#code-example "Direct link to Code Example")

To provide documents to the model, you can include the sources as a function call response.
Below is an example of references, in this case from Wikipedia, using tool calls.

**References Example**

{  "0": {    "url": "https://en.wikipedia.org/wiki/2024_Nobel_Peace_Prize",    "title": "2024 Nobel Peace Prize",    "snippets": [      [        "The 2024 Nobel Peace Prize, an international peace prize established according to Alfred Nobel's will, was awarded to Nihon Hidankyo (the Japan Confederation of A- and H-Bomb Sufferers Organizations), for their activism against nuclear weapons, assisted by victim/survivors (known as Hibakusha) of the atomic bombings of Hiroshima and Nagasaki in 1945.",        "They will receive the prize at a ceremony on 10 December 2024 at Oslo, Norway."      ]    ],    "description": null,    "date": "2024-11-26T17:39:55.057454",    "source": "wikipedia"  },  "1": {    "url": "https://en.wikipedia.org/wiki/Climate_Change",    "title": "Climate Change",    "snippets": [      [        "Present-day climate change includes both global warming—the ongoing increase in global average temperature—and its wider effects on Earth’s climate system. Climate change in a broader sense also includes previous long-term changes to Earth's climate. The current rise in global temperatures is driven by human activities, especially fossil fuel burning since the Industrial Revolution. Fossil fuel use, deforestation, and some agricultural and industrial practices release greenhouse gases. These gases absorb some of the heat that the Earth radiates after it warms from sunlight, warming the lower atmosphere. Carbon dioxide, the primary gas driving global warming, has increased in concentration by about 50% since the pre-industrial era to levels not seen for millions of years."      ]    ],    "description": null,    "date": "2024-11-26T17:39:55.057454",    "source": "wikipedia"  },  "2": {    "url": "https://en.wikipedia.org/wiki/Artificial_Intelligence",    "title": "Artificial Intelligence",    "snippets": [      [        "Artificial intelligence (AI) refers to the capability of computational systems to perform tasks typically associated with human intelligence, such as learning, reasoning, problem-solving, perception, and decision-making. It is a field of research in computer science that develops and studies methods and software that enable machines to perceive their environment and use learning and intelligence to take actions that maximize their chances of achieving defined goals. Such machines may be called AIs."      ]    ],    "description": null,    "date": "2024-11-26T17:39:55.057454",    "source": "wikipedia"  }}

### Initialize Client[​](#initialize-client "Direct link to Initialize Client")

import osfrom mistralai import Mistral, ToolMessageimport jsonapi_key = os.environ["MISTRAL_API_KEY"]model = "mistral-large-latest"client = Mistral(api_key=api_key)

### Define the Tool[​](#define-the-tool "Direct link to Define the Tool")

In this case, we will create a `get_information` tool that will return the references mentioned previously.

get_information_tool = {    "type": "function",    "function": {        "name": "get_information",        "description": "Get information from external source.",        "parameters": {}    },}def get_information():    return json.dumps(references)

### Set Up Chat History[​](#set-up-chat-history "Direct link to Set Up Chat History")

chat_history = [    {        "role": "system",        "content": "Answer the user by providing references to the source of the information."    },    {        "role": "user",        "content": "Who won the Nobel Prize in 2024?"    }]

### Make the Initial Chat Request[​](#make-the-initial-chat-request "Direct link to Make the Initial Chat Request")

chat_response = client.chat.complete(    model=model,    messages=chat_history,    tools=[get_information_tool],)if hasattr(chat_response.choices[0].message, 'tool_calls'):    tool_call = chat_response.choices[0].message.tool_calls[0]    chat_history.append(chat_response.choices[0].message)    print(tool_call)else:    print("No tool call found in the response")

Output:

function=FunctionCall(name='get_information', arguments='{}') id='F4HiRgdZp' type=None index=0

### Handle Tool Call and Append Result[​](#handle-tool-call-and-append-result "Direct link to Handle Tool Call and Append Result")

result = get_information()tool_call_result = ToolMessage(    content=result,    tool_call_id=tool_call.id,    name=tool_call.function.name,)# Append the tool call message to the chat_historychat_history.append(tool_call_result)

### Make the Final Chat Request[​](#make-the-final-chat-request "Direct link to Make the Final Chat Request")

chat_response = client.chat.complete(    model=model,    messages=chat_history,    tools=[get_information_tool],)print(chat_response.choices[0].message.content)

Output:

[TextChunk(text='The Nobel Peace Prize for 2024 was awarded to the Japan Confederation of A- and H-Bomb Sufferers Organizations (Nihon Hidankyo) for their activism against nuclear weapons, including efforts by survivors of the atomic bombings of Hiroshima and Nagasaki', type='text'), ReferenceChunk(reference_ids=[0], type='reference'), TextChunk(text='.', type='text')]

### Extract and Print References[​](#extract-and-print-references "Direct link to Extract and Print References")

from mistralai.models import TextChunk, ReferenceChunkrefs_used = []# Print the main response and save each referencefor chunk in chat_response.choices[0].message.content:    if isinstance(chunk, TextChunk):        print(chunk.text, end="")    elif isinstance(chunk, ReferenceChunk):        refs_used += chunk.reference_ids# Print references onlyif refs_used:    print("\n\nSources:")    for i, ref in enumerate(set(refs_used), 1):        reference = json.loads(result)[str(ref)]        print(f"\n{i}. {reference['title']}: {reference['url']}")

Output:

The Nobel Peace Prize for 2024 was awarded to the Japan Confederation of A- and H-Bomb Sufferers Organizations (Nihon Hidankyo) for their activism against nuclear weapons, including efforts by survivors of the atomic bombings of Hiroshima and Nagasaki.Sources:1. 2024 Nobel Peace Prize: https://en.wikipedia.org/wiki/2024_Nobel_Peace_Prize

# Full Cookbook

You can find a comprehensive cookbook exploring Citations and References leveraging RAG with Wikipedia [here](https://colab.research.google.com/github/mistralai/cookbook/blob/main/mistral/rag/mistral-reference-rag.ipynb).
This template will help get started with web search and document grounding with citations.

[

Previous

Function calling

](/capabilities/function_calling/)[

Next

Structured Output

](/capabilities/structured-output/structured_output_overview/)

*   [Code Example](#code-example)
*   [Initialize Client](#initialize-client)
*   [Define the Tool](#define-the-tool)
*   [Set Up Chat History](#set-up-chat-history)
*   [Make the Initial Chat Request](#make-the-initial-chat-request)
*   [Handle Tool Call and Append Result](#handle-tool-call-and-append-result)
*   [Make the Final Chat Request](#make-the-final-chat-request)
*   [Extract and Print References](#extract-and-print-references)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyri