---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/capabilities/function_calling/"
title: "/capabilities/function_calling/"
domain: "docs.mistral.ai"
path: "/capabilities/function_calling/"
scraped_time: "2025-09-08T18:09:58.789306"
url_depth: 2
word_count: 1858
---

Function calling | Mistral AI

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
*   Function calling

On this page

# Function calling

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mistralai/cookbook/blob/main/mistral/function_calling/function_calling.ipynb)

Function calling allows Mistral models to connect to external tools. By integrating Mistral models with external tools such as user defined functions or APIs, users can easily build applications catering to specific use cases and practical problems. In this guide, for instance, we wrote two functions for tracking payment status and payment date. We can use these two tools to provide answers for payment-related queries.

### Available models[​](#available-models "Direct link to Available models")

Currently, function calling is available for the following models:

*   Mistral Large
*   Mistral Medium
*   Mistral Small
*   Devstral Small
*   Codestral
*   Ministral 8B
*   Ministral 3B
*   Pixtral 12B
*   Pixtral Large
*   Mistral Nemo

### Four steps[​](#four-steps "Direct link to Four steps")

At a glance, there are four steps with function calling:

*   User: specify tools and query
*   Model: Generate function arguments if applicable
*   User: Execute function to obtain tool results
*   Model: Generate final answer

![functioncalling1](/img/guides/functioncalling1.png)

In this guide, we will walk through a simple example to demonstrate how function calling works with Mistral models in these four steps.

Before we get started, let’s assume we have a dataframe consisting of payment transactions. When users ask questions about this dataframe, they can use certain tools to answer questions about this data. This is just an example to emulate an external database that the LLM cannot directly access.

*   python
*   typescript

import pandas as pd# Assuming we have the following datadata = {    'transaction_id': ['T1001', 'T1002', 'T1003', 'T1004', 'T1005'],    'customer_id': ['C001', 'C002', 'C003', 'C002', 'C001'],    'payment_amount': [125.50, 89.99, 120.00, 54.30, 210.20],    'payment_date': ['2021-10-05', '2021-10-06', '2021-10-07', '2021-10-05', '2021-10-08'],    'payment_status': ['Paid', 'Unpaid', 'Paid', 'Paid', 'Pending']}# Create DataFramedf = pd.DataFrame(data)

// Assuming we have the following dataconst data = {    transactionId: ['T1001', 'T1002', 'T1003', 'T1004', 'T1005'],    customerId: ['C001', 'C002', 'C003', 'C002', 'C001'],    paymentAmount: [125.50, 89.99, 120.00, 54.30, 210.20],    paymentDate: ['2021-10-05', '2021-10-06', '2021-10-07', '2021-10-05', '2021-10-08'],    paymentStatus: ['Paid', 'Unpaid', 'Paid', 'Paid', 'Pending']};// Convert data into an array of objects for easier manipulationconst transactions = data.transactionId.map((id, index) => ({    transactionId: id,    customerId: data.customerId[index],    paymentAmount: data.paymentAmount[index],    paymentDate: data.paymentDate[index],    paymentStatus: data.paymentStatus[index]}));

## Step 1. User: specify tools and query[​](#step-1-user-specify-tools-and-query "Direct link to Step 1. User: specify tools and query")

![functioncalling2](/img/guides/functioncalling2.png)

### Tools[​](#tools "Direct link to Tools")

Users can define all the necessary tools for their use cases.

*   In many cases, we might have multiple tools at our disposal. For example, let’s consider we have two functions as our two tools: `retrieve_payment_status` and `retrieve_payment_date` to retrieve payment status and payment date given transaction ID.

*   python
*   typescript

def retrieve_payment_status(df: data, transaction_id: str) -> str:    if transaction_id in df.transaction_id.values:         return json.dumps({'status': df[df.transaction_id == transaction_id].payment_status.item()})    return json.dumps({'error': 'transaction id not found.'})def retrieve_payment_date(df: data, transaction_id: str) -> str:    if transaction_id in df.transaction_id.values:         return json.dumps({'date': df[df.transaction_id == transaction_id].payment_date.item()})    return json.dumps({'error': 'transaction id not found.'})

function retrievePaymentStatus(transactions, transactionId) {    const transaction = transactions.find(t => t.transactionId === transactionId);    if (transaction) {        return JSON.stringify({ status: transaction.paymentStatus });    }    return JSON.stringify({ error: 'transaction id not found.' });}function retrievePaymentDate(transactions, transactionId) {    const transaction = transactions.find(t => t.transactionId === transactionId);    if (transaction) {        return JSON.stringify({ date: transaction.paymentDate });    }    return JSON.stringify({ error: 'transaction id not found.' });}

*   In order for Mistral models to understand the functions, we need to outline the function specifications with a JSON schema. Specifically, we need to describe the type, function name, function description, function parameters, and the required parameter for the function. Since we have two functions here, let’s list two function specifications in a list.

*   python
*   typescript

tools = [    {        "type": "function",        "function": {            "name": "retrieve_payment_status",            "description": "Get payment status of a transaction",            "parameters": {                "type": "object",                "properties": {                    "transaction_id": {                        "type": "string",                        "description": "The transaction id.",                    }                },                "required": ["transaction_id"],            },        },    },    {        "type": "function",        "function": {            "name": "retrieve_payment_date",            "description": "Get payment date of a transaction",            "parameters": {                "type": "object",                "properties": {                    "transaction_id": {                        "type": "string",                        "description": "The transaction id.",                    }                },                "required": ["transaction_id"],            },        },    }]

**Note**: You can specify multiple parameters for each function in the `properties` object. In the following example, we choose to merge the `retrieve_payment_status` and `retrieve_payment_date` into `retrieve_payment_info`:

tools = [    {        "type": "function",        "function": {            "name": "retrieve_payment_info",            "description": "Retrieves payment infos",            "parameters": {                "type": "object",                "properties": {                    "transaction_id": {                        "type": "string",                        "description": "The transaction id",                    },                    "info_type": {                        "type": "string",                        "description": "The info type ('status' or 'date')",                    }                },                "required": ["transaction_id", "info_type"],            },        },    }]

const tools = [    {        type: "function",        function: {            name: "retrievePaymentStatus",            description: "Get payment status of a transaction",            parameters: {                type: "object",                properties: {                    transactionId: {                        type: "string",                        description: "The transaction id.",                    }                },                required: ["transactionId"],            },        },    },    {        type: "function",        function: {            name: "retrievePaymentDate",            description: "Get payment date of a transaction",            parameters: {                type: "object",                properties: {                    transactionId: {                        type: "string",                        description: "The transaction id.",                    }                },                required: ["transactionId"],            },        },    }];

**Note**: You can specify multiple parameters for each function in the `properties` object. In the following example, we choose to merge the `retrieve_payment_status` and `retrieve_payment_date` into `retrieve_payment_info`:

const tools = [    {        type: "function",        function: {            name: "retrievePaymentInfo",            description: "Retrieves payment infos",            parameters: {                type: "object",                properties: {                    transactionId: {                        type: "string",                        description: "The transaction id",                    },                    infoType: {                        type: "string",                        description: "The info type ('status' or 'date')",                    }                },                required: ["transactionId", "infoType"],            },        },    }];

*   Then we organize the two functions into a dictionary where keys represent the function name, and values are the function with the `df` defined. This allows us to call each function based on its function name.

*   python
*   typescript

import functoolsnames_to_functions = {    'retrieve_payment_status': functools.partial(retrieve_payment_status, df=df),    'retrieve_payment_date': functools.partial(retrieve_payment_date, df=df)}

const namesToFunctions = {    'retrievePaymentStatus': (transactionId) => retrievePaymentStatus(transactions, transactionId),    'retrievePaymentDate': (transactionId) => retrievePaymentDate(transactions, transactionId)};

### User query[​](#user-query "Direct link to User query")

Suppose a user asks the following question: “What’s the status of my transaction?” A standalone LLM would not be able to answer this question, as it needs to query the business logic backend to access the necessary data. But what if we have an exact tool we can use to answer this question? We could potentially provide an answer!

*   python
*   typescript

messages = [{"role": "user", "content": "What's the status of my transaction T1001?"}]

const messages = [{"role": "user", "content": "What's the status of my transaction T1001?"}];

## Step 2. Model: Generate function arguments[​](#step-2-model-generate-function-arguments "Direct link to Step 2. Model: Generate function arguments")

![functioncalling3](/img/guides/functioncalling3.png)

How do Mistral models know about these functions and know which function to use? We provide both the user query and the tools specifications to Mistral models. The goal in this step is not for the Mistral model to run the function directly. It’s to 1) determine the appropriate function to use , 2) identify if there is any essential information missing for a function, and 3) generate necessary arguments for the chosen function.

### tool\_choice[​](#tool_choice "Direct link to tool_choice")

Users can use `tool_choice` to specify how tools are used:

*   "auto": default mode. Model decides if it uses the tool or not.
*   "any": forces tool use.
*   "none": prevents tool use.

### parallel\_tool\_calls[​](#parallel_tool_calls "Direct link to parallel_tool_calls")

Users can use `parallel_tool_calls` to specify whether parallel tool calling is allowed.

*   true: default mode. The model decides if it uses parallel tool calls or not.
*   false: forces the model to use single tool calling.

*   python
*   typescript

import osfrom mistralai import Mistralapi_key = os.environ["MISTRAL_API_KEY"]model = "mistral-large-latest"client = Mistral(api_key=api_key)response = client.chat.complete(    model = model,    messages = messages,    tools = tools,    tool_choice = "any",    parallel_tool_calls = False,)response

We get the response including tool\_calls with the chosen function name `retrieve_payment_status` and the arguments for this function.

Output:

ChatCompletionResponse(id='7cbd8962041442459eb3636e1e3cbf10', object='chat.completion', model='mistral-large-latest', usage=Usage(prompt_tokens=94, completion_tokens=30, total_tokens=124), created=1721403550, choices=[Choices(index=0, finish_reason='tool_calls', message=AssistantMessage(content='', tool_calls=[ToolCall(function=FunctionCall(name='retrieve_payment_status', arguments='{"transaction_id": "T1001"}'), id='D681PevKs', type='function')], prefix=False, role='assistant'))])

import { Mistral } from '@mistralai/mistralai';const apiKey = process.env.MISTRAL_API_KEY;const model = "mistral-large-latest";const client = new Mistral({ apiKey: apiKey });let response = await client.chat.complete({    model: model,    messages: messages,    tools: tools,    toolChoice: "any",    parallelToolCalls: false,});

We get the response including toolCalls with the chosen function name `retrievePaymentStatus` and the arguments for this function.

Let’s add the response message to the `messages` list.

*   python
*   typescript

messages.append(response.choices[0].message)

messages.push(response.choices[0].message);

## Step 3. User: Execute function to obtain tool results[​](#step-3-user-execute-function-to-obtain-tool-results "Direct link to Step 3. User: Execute function to obtain tool results")

![functioncalling4](/img/guides/functioncalling4.png)

How do we execute the function? Currently, it is the user’s responsibility to execute these functions and the function execution lies on the user side. In the future, we may introduce some helpful functions that can be executed server-side.

Let’s extract some useful function information from model response including `function_name` and `function_params`. It’s clear here that our Mistral model has chosen to use the function `retrieve_payment_status` with the parameter `transaction_id` set to T1001.

*   python
*   typescript

import jsontool_call = response.choices[0].message.tool_calls[0]function_name = tool_call.function.namefunction_params = json.loads(tool_call.function.arguments)print("\nfunction_name: ", function_name, "\nfunction_params: ", function_params)

Output

function_name:  retrieve_payment_status function_params: {'transaction_id': 'T1001'}

const toolCall = response.choices[0].message.toolCalls[0];const functionName = toolCall.function.name;const functionParams = JSON.parse(toolCall.function.arguments);console.log("\nfunction_name: ", functionName, "\nfunction_params: ", functionParams);

Output

function_name:  retrievePaymentStatus function_params:  { transactionId: 'T1001' }

Now we can execute the function and we get the function output `'{"status": "Paid"}'`.

*   python
*   typescript

function_result = names_to_functions[function_name](**function_params)function_result

Output

'{"status": "Paid"}'

const functionResult = namesToFunctions[functionName](functionParams.transactionId);console.log(functionResult);

Output

{"status":"Paid"}

## Step 4. Model: Generate final answer[​](#step-4-model-generate-final-answer "Direct link to Step 4. Model: Generate final answer")

![functioncalling5](/img/guides/functioncalling5.png)

We can now provide the output from the tools to Mistral models, and in return, the Mistral model can produce a customised final response for the specific user.

*   python
*   typescript

messages.append({    "role":"tool",     "name":function_name,     "content":function_result,     "tool_call_id":tool_call.id})response = client.chat.complete(    model = model,     messages = messages)response.choices[0].message.content

Output:

The status of your transaction with ID T1001 is "Paid". Is there anything else I can assist you with?

messages.push({    role: "tool",    name: functionName,    content: functionResult,    toolCallId: toolCall.id});response = await client.chat.complete({    model: model,    messages: messages});console.log(response.choices[0].message.content);

Output:

The status of your transaction with ID T1001 is "Paid". Is there anything else I can assist you with?

[

Previous

Code Embeddings

](/capabilities/embeddings/code_embeddings/)[

Next

Citations and References

](/capabilities/citations/)

*   [Available models](#available-models)
*   [Four steps](#four-steps)
*   [Step 1. User: specify tools and query](#step-1-user-specify-tools-and-query)
*   [Tools](#tools)
*   [User query](#user-query)
*   [Step 2. Model: Generate function arguments](#step-2-model-generate-function-arguments)
*   [tool\_choice](#tool_choice)
*   [parallel\_tool\_calls](#parallel_tool_calls)
*   [Step 3. User: Execute function to obtain tool results](#step-3-user-execute-function-to-obtain-tool-results)
*   [Step 4. Model: Generate final answer](#step-4-model-generate-final-answer)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.co