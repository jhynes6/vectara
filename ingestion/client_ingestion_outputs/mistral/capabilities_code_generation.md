---
source: "website"
content_type: "services_products"
url: "https://docs.mistral.ai/capabilities/code_generation/"
title: "/capabilities/code_generation/"
domain: "docs.mistral.ai"
path: "/capabilities/code_generation/"
scraped_time: "2025-09-08T18:10:15.502236"
url_depth: 2
word_count: 2393
---

Coding | Mistral AI

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
*   Coding

On this page

# Coding

LLMs are powerfull tools for text generation, and they also show great performance in code generation for multiple tasks, both for code completion, code generation and agentic tool use for semi-automated software development.

We provide 2 major families of llms for coding:

*   **Codestral**: Specifically trained for Code Generation and FIM.
*   **Devstral**: Specifically trained for Agentic Tool Use for Software Development.

Note that we also provide **Codestral Embed**, for semantic search and embedding code databases, repositories, and powering coding assistants with state-of-the-art retrieval. Learn more about it [here](https://docs.mistral.ai/capabilities/embeddings/code_embeddings).

## Endpoints & Models[​](#endpoints--models "Direct link to Endpoints & Models")

We provide 2 main endpoints:

*   `https://api.mistral.ai/v1/fim/completions`: [Fill-in-the-middle](#fim), for code completion and code generation; supporting `codestral-latest`.
*   `https://api.mistral.ai/v1/chat/completions`: [Instruction following](#instruct-following), for coding and agentic tool use; supporting `codestral-latest`, `devstral-small-latest` and `devstral-medium-latest`.

## FIM[​](#fim "Direct link to FIM")

With this feature, users can define the starting point of the code using a `prompt`, and the ending point of the code using an optional `suffix` and an optional `stop`. The FIM model will then generate the code that fits in between, making it ideal for tasks that require a specific piece of code to be generated.

tip

We also provide the `min_tokens` and `max_tokens` sampling parameters, which are particularly useful for code generation as it allows you to set the minimum and maximum number of tokens that should be produced. This is especially useful when FIM models decide to produce no tokens at all, or are overly verbose, allowing developers to enforce completions within a specific range if they are needed.

### Codestral[​](#codestral "Direct link to Codestral")

Codestral is a cutting-edge generative model that has been specifically designed and optimized for code generation tasks, including fill-in-the-middle and code completion. Codestral was trained on 80+ programming languages, enabling it to perform well on both common and less common languages.

important

We currently offer two domains for Codestral endpoints, both providing FIM and instruct routes:

Domain

Features

codestral.mistral.ai

\- Monthly subscription based, currently free to use
\- Requires a new key for which a phone number is needed

api.mistral.ai

\- Allows you to use your existing API key and you can pay to use Codestral
\- Ideal for business use

Wondering which endpoint to use?

*   If you're a user, wanting to query Codestral as part of an IDE plugin, codestral.mistral.ai is recommended.
*   If you're building a plugin, or anything that exposes these endpoints directly to the user, and expect them to bring their own API keys, you should also target codestral.mistral.ai
*   For all other use cases, api.mistral.ai will be better suited

_This guide uses api.mistral.ai for demonstration._

Below we present three examples:

#### Example 1: Fill in the middle[​](#example-1-fill-in-the-middle "Direct link to Example 1: Fill in the middle")

Originally, these models are designed to complete code in-between 2 points: a prefix (here called `prompt`) and a `suffix`, generating the code in-between.

*   python
*   curl

import osfrom mistralai import Mistralapi_key = os.environ["MISTRAL_API_KEY"]client = Mistral(api_key=api_key)model = "codestral-latest"prompt = "def fibonacci(n: int):"suffix = "n = int(input('Enter a number: '))\nprint(fibonacci(n))"response = client.fim.complete(    model=model,    prompt=prompt,    suffix=suffix,    temperature=0,    # min_tokens=1, # Uncomment to enforce completions to at least 1 token)print(    f"""{prompt}{response.choices[0].message.content}{suffix}""")

curl --location 'https://api.mistral.ai/v1/fim/completions' \--header 'Content-Type: application/json' \--header 'Accept: application/json' \--header "Authorization: Bearer $MISTRAL_API_KEY" \--data '{    "model": "codestral-latest",    "prompt": "def f(",    "suffix": "return a + b",    "max_tokens": 64,    "temperature": 0}'

#### Example 2: Completion[​](#example-2-completion "Direct link to Example 2: Completion")

However, you can also use the model for pure code completion, by only providing a `prompt` and no `suffix`.

*   python
*   curl

import osfrom mistralai import Mistralapi_key = os.environ["MISTRAL_API_KEY"]client = Mistral(api_key=api_key)model = "codestral-latest"prompt = "def is_odd(n): \n return n % 2 == 1 \ndef test_is_odd():"response = client.fim.complete(model=model, prompt=prompt, temperature=0)print(    f"""{prompt}{response.choices[0].message.content}""")

curl --location 'https://api.mistral.ai/v1/fim/completions' \--header 'Content-Type: application/json' \--header 'Accept: application/json' \--header "Authorization: Bearer $MISTRAL_API_KEY" \--data '{    "model": "codestral-latest",    "prompt": "def is_odd(n): \n return n % 2 == 1 \n def test_is_odd():",     "suffix": "",    "max_tokens": 64,    "temperature": 0}'

#### Example 3: Stop tokens[​](#example-3-stop-tokens "Direct link to Example 3: Stop tokens")

You can also use stop tokens to control the generation of the model when it generates specific strings.

tip

We recommend adding stop tokens for IDE autocomplete integrations to prevent the model from being too verbose.

*   python
*   curl

import osfrom mistralai import Mistralapi_key = os.environ["MISTRAL_API_KEY"]client = Mistral(api_key=api_key)model = "codestral-latest"prompt = "def is_odd(n): \n return n % 2 == 1 \ndef test_is_odd():"suffix = "n = int(input('Enter a number: '))\nprint(fibonacci(n))"response = client.fim.complete(    model=model, prompt=prompt, suffix=suffix, temperature=0, stop=["\n\n"])print(    f"""{prompt}{response.choices[0].message.content}""")

curl --location 'https://api.mistral.ai/v1/fim/completions' \--header 'Content-Type: application/json' \--header 'Accept: application/json' \--header "Authorization: Bearer $MISTRAL_API_KEY" \--data '{    "model": "codestral-latest",    "prompt": "def is_odd(n): \n return n % 2 == 1 \n def test_is_odd():",     "suffix": "test_is_odd()",    "stop": ["\n\n"],    "max_tokens": 64,    "temperature": 0}'

## Instruct Following[​](#instruct-following "Direct link to Instruct Following")

We also provide the instruct chat endpoint of Codestral with the same model `codestral-latest`.
The only difference is the endpoint used; so you can leverage powerfull code completion with instruct and chat use cases.

However we also provide `devstral-small-latest` and `devstral-medium-latest` for agentic tool use for software development, this family of models is specifically trained to navigate code bases and leverage tool usage for diverse tasks.

### Codestral[​](#codestral-1 "Direct link to Codestral")

Here is an example of how to use the instruct endpoint of Codestral, it's perfect for specific **code generation** of specific snippets or **code completion** while **following instructions**; so you can better guide generation and exchange with a powerfull coding model.

*   python
*   curl

import osfrom mistralai import Mistralapi_key = os.environ["MISTRAL_API_KEY"]client = Mistral(api_key=api_key)model = "codestral-latest"message = [{"role": "user", "content": "Write a function for fibonacci"}]chat_response = client.chat.complete(    model = model,    messages = message)

curl --location "https://api.mistral.ai/v1/chat/completions" \     --header 'Content-Type: application/json' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY" \     --data '{    "model": "codestral-latest",    "messages": [{"role": "user", "content": "Write a function for fibonacci"}]  }'

### Devstral[​](#devstral "Direct link to Devstral")

While Codestral is designed for code generation and FIM, Devstral is a cutting-edge generative model that has been specifically designed and optimized for **agentic tool use for software development**, it can leverage function calling to navigate code bases and call the right tools to perform specific tasks for semi-automated software development.

*   python
*   curl

import osfrom mistralai import Mistralapi_key = os.environ["MISTRAL_API_KEY"]client = Mistral(api_key=api_key)model = "devstral-medium-latest"message = [{"role": "user", "content": "Create a new file called test.py and write a function for fibonacci"}]tools = [    {        "type": "function",        "function": {            "name": "create_file",            "description": "Create a new file with the given name and content",            "parameters": {                "type": "object",                "properties": {                    "filename": {                        "type": "string",                        "description": "The name of the file to create",                    },                    "content": {                        "type": "string",                        "description": "The content to write to the file",                    },                },                "required": ["filename", "content"],            },        },    }]chat_response = client.chat.complete(    model = model,    messages = message,    tools = tools)

curl --location "https://api.mistral.ai/v1/chat/completions" \     --header 'Content-Type: application/json' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY" \     --data '{    "model": "devstral-medium-latest",    "messages": [{"role": "user", "content": "Create a new file called test.py and write a function for fibonacci"}],    "tools": [        {            "type": "function",            "function": {                "name": "create_file",                "description": "Create a new file with the given name and content",                "parameters": {                    "type": "object",                    "properties": {                        "filename": {                            "type": "string",                            "description": "The name of the file to create"                        },                        "content": {                            "type": "string",                            "description": "The content to write to the file"                        }                    },                    "required": ["filename", "content"]                }            }        }    ]  }'

## Integrations[​](#integrations "Direct link to Integrations")

### Codestral Integrations[​](#codestral-integrations "Direct link to Codestral Integrations")

**Integration with continue.dev**

Continue.dev supports both Codestral base for code generation and Codestral Instruct for chat.

#### How to set up Codestral with Continue[​](#how-to-set-up-codestral-with-continue "Direct link to How to set up Codestral with Continue")

**Here is a step-by-step guide on how to set up Codestral with Continue using the Mistral AI API:**

1.  Install the Continue VS Code or JetBrains extension following the instructions [here](https://docs.continue.dev/quickstart). Please make sure you install Continue version >v0.8.33.

2.  Automatic set up:

*   Click on the Continue extension iron on the left menu. Select `Mistral API` as a provider, select `Codestral` as a model.
*   Click "Get API Key" to get Codestral API key.
*   Click "Add model", which will automatically populate the config.json.

![drawing](/img/guides/codestral1.png)

2.  (alternative) Manually edit config.json

*   Click on the gear icon in the bottom right corner of the Continue window to open `~/.continue/config.json` (MacOS) / `%userprofile%\.continue\config.json` (Windows)
*   Log in and request a Codestral API key on Mistral AI's La Plateforme [here](https://console.mistral.ai/codestral)
*   To use Codestral as your model for both `autocomplete` and `chat`, replace `[API_KEY]` with your Mistral API key below and add it to your `config.json` file:

~/.continue/config.json

{  "models": [    {      "title": "Codestral",      "provider": "mistral",      "model": "codestral-latest",      "apiKey": "[API_KEY]"    }  ],  "tabAutocompleteModel": {    "title": "Codestral",    "provider": "mistral",    "model": "codestral-latest",    "apiKey": "[API_KEY]"  }}

If you run into any issues or have any questions, please join our Discord and post in `#help` channel [here](https://discord.gg/EfJEfdFnDQ)

**Integration with Tabnine**

Tabnine supports Codestral Instruct for chat.

#### How to set up Codestral with Tabnine[​](#how-to-set-up-codestral-with-tabnine "Direct link to How to set up Codestral with Tabnine")

##### What is Tabnine Chat?[​](#what-is-tabnine-chat "Direct link to What is Tabnine Chat?")

Tabnine Chat is a code-centric chat application that runs in the IDE and allows developers to interact with Tabnine’s AI models in a flexible, free-form way, using natural language. Tabnine Chat also supports dedicated quick actions that use predefined prompts optimized for specific use cases.

##### Getting started[​](#getting-started "Direct link to Getting started")

To start using Tabnine Chat, first [launch](https://docs.tabnine.com/main/getting-started/getting-the-most-from-tabnine-chat/launch) it in your IDE (VSCode, JetBrains, or Eclipse). Then, learn how to [interact](https://docs.tabnine.com/main/getting-started/getting-the-most-from-tabnine-chat/interact) with Tabnine Chat, for example, how to ask questions or give instructions. Once you receive your response, you can [read, review, and apply](https://docs.tabnine.com/main/getting-started/getting-the-most-from-tabnine-chat/consume) it within your code.

##### Selecting Codestral as Tabnine Chat App model[​](#selecting-codestral-as-tabnine-chat-app-model "Direct link to Selecting Codestral as Tabnine Chat App model")

In the Tabnine Chat App, use the [model selector](https://docs.tabnine.com/main/getting-started/getting-the-most-from-tabnine-chat/switching-between-chat-ai-models) to choose _Codestral_.

**Integration with LangChain**

LangChain provides support for Codestral Instruct. Here is how you can use it in LangChain:

# make sure to install `langchain` and `langchain-mistralai` in your Python environmentimport osfrom langchain_mistralai import ChatMistralAIfrom langchain_core.prompts import ChatPromptTemplate api_key = os.environ["MISTRAL_API_KEY"]mistral_model = "codestral-latest"llm = ChatMistralAI(model=mistral_model, temperature=0, api_key=api_key)llm.invoke([("user", "Write a function for fibonacci")])

For a more complex use case of self-corrective code generation using the instruct Codestral tool use, check out this [notebook](https://github.com/mistralai/cookbook/blob/main/third_party/langchain/langgraph_code_assistant_mistral.ipynb) and this video:

**Integration with LlamaIndex**

LlamaIndex provides support for Codestral Instruct and Fill In Middle (FIM) endpoints. Here is how you can use it in LlamaIndex:

# make sure to install `llama-index` and `llama-index-llms-mistralai` in your Python enviornmentimport osfrom llama_index.core.llms import ChatMessagefrom llama_index.llms.mistralai import MistralAIapi_key =  os.environ["MISTRAL_API_KEY"]mistral_model = "codestral-latest"messages = [    ChatMessage(role="user", content="Write a function for fibonacci"),]MistralAI(api_key=api_key, model=mistral_model).chat(messages)

Check out more details on using Instruct and Fill In Middle(FIM) with LlamaIndex in this [notebook](https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/cookbooks/codestral.ipynb).

**Integration with Jupyter AI**

Jupyter AI seamlessly integrates Codestral into JupyterLab, offering users a streamlined and enhanced AI-assisted coding experience within the Jupyter ecosystem. This integration boosts productivity and optimizes users' overall interaction with Jupyter.

To get started using Codestral and Jupyter AI in JupyterLab, first install needed packages in your Python environment:

pip install jupyterlab langchain-mistralai jupyter-ai pandas matplotlib

Then launch Jupyter Lab:

jupyter lab

Afterwards, you can select Codestral as your model of choice, input your Mistral API key, and start coding with Codestral!

**Integration with JupyterLite**

JupyterLite is a project that aims to bring the JupyterLab environment to the web browser, allowing users to run Jupyter directly in their browser without the need for a local installation.

You can try Codestral with JupyterLite in your browser: [![lite-badge](https://jupyterlite.rtfd.io/en/latest/_static/badge.svg)](https://jupyterlite.github.io/ai/lab/index.html) **Integration with Tabby**

Tabby is an open-source AI coding assistant. You can use Codestral for both code completion and chat via Tabby.

To use Codestral in Tabby, configure your model configuration in `~/.tabby/config.toml` as follows.

[model.completion.http]kind = "mistral/completion"api_endpoint = "https://api.mistral.ai"api_key = "secret-api-key"

You can check out [Tabby's documentation](https://tabby.tabbyml.com/docs/administration/model/#mistral--codestral) to learn more.

**Integration with E2B**

E2B provides open-source secure sandboxes for AI-generated code execution. With E2B, it is easy for developers to add code interpreting capabilities to AI apps using Codestral.

In the following examples, the AI agent performs a data analysis task on an uploaded CSV file, executes the AI-generated code by Codestral in the sandboxed environment by E2B, and returns a chart, saving it as a PNG file.

Python implementation ([cookbook](https://github.com/mistralai/cookbook/tree/main/third_party/E2B_Code_Interpreting/codestral-code-interpreter-python)):

JS implementation ([cookbook](https://github.com/mistralai/cookbook/tree/main/third_party/E2B_Code_Interpreting/codestral-code-interpreter-js)):

### Devstral Integrations[​](#devstral-integrations "Direct link to Devstral Integrations")

**Integration with Open Hands**

OpenHands is an open-source scaffolding tool designed for building AI agents focused on software development. It offers a comprehensive framework for creating and managing these agents that can modify code, run commands, browse the web, call APIs, and even copy code snippets from StackOverflow.

After creating a Mistral AI account, you can use the following commands to start the OpenHands Docker container:

export MISTRAL_API_KEY=<MY_KEY>mkdir -p ~/.openhands && echo '{"language":"en","agent":"CodeActAgent","max_iterations":null,"security_analyzer":null,"confirmation_mode":false,"llm_model":"mistral/devstral-small-2507","llm_api_key":"'$MISTRAL_API_KEY'","remote_runtime_resource_factor":null,"github_token":null,"enable_default_condenser":true}' > ~/.openhands-state/settings.jsondocker pull docker.all-hands.dev/all-hands-ai/runtime:0.48-nikolaikdocker run -it --rm --pull=always \    -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:0.48-nikolaik \    -e LOG_ALL_EVENTS=true \    -v /var/run/docker.sock:/var/run/docker.sock \    -v ~/.openhands:/.openhands \    -p 3000:3000 \    --add-host host.docker.internal:host-gateway \    --name openhands-app \    docker.all-hands.dev/all-hands-ai/openhands:0.48

For more information visit the [OpenHands github repo](https://github.com/All-Hands-AI/OpenHands) and their [documentation](https://docs.all-hands.dev/usage/llms/local-llms).

**Integration with Cline**

Cline is an autonomous coding agent operating right in your IDE, capable of creating/editing files, executing commands, using the browser, and more with your permission every step of the way.

For more information visit the [Cline github repo](https://github.com/cline/cline).

[

Previous

Document QnA

](/capabilities/document_ai/document_qna/)[

Next

Embeddings Overview

](/capabilities/embeddings/overview/)

*   [Endpoints & Models](#endpoints--models)
*   [FIM](#fim)
*   [Codestral](#codestral)
*   [Instruct Following](#instruct-following)
*   [Codestral](#codestral-1)
*   [Devstral](#devstral)
*   [Integrations](#integrations)
*   [Codestral Integrations](#codestral-integrations)
*   [Devstral Integrations](#devstral-integrations)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mist