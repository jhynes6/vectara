---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/deployment/cloud/ibm-watsonx/"
title: "/deployment/cloud/ibm-watsonx/"
domain: "docs.mistral.ai"
path: "/deployment/cloud/ibm-watsonx/"
scraped_time: "2025-09-08T18:10:08.439981"
url_depth: 3
word_count: 659
---

IBM watsonx.ai | Mistral AI

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

*   [Azure AI](/deployment/cloud/azure/)
*   [AWS Bedrock](/deployment/cloud/aws/)
*   [Vertex AI](/deployment/cloud/vertex/)
*   [Snowflake Cortex](/deployment/cloud/sfcortex/)
*   [IBM watsonx.ai](/deployment/cloud/ibm-watsonx/)
*   [Outscale](/deployment/cloud/outscale/)
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
*   [Cloud](/deployment/cloud/overview/)
*   IBM watsonx.ai

On this page

# IBM watsonx.ai

## Introduction[​](#introduction "Direct link to Introduction")

Mistral AI's Large model is available on the IBM watsonx.ai platform as a fully managed solution, as well as an on-premise deployment.

## Getting started[​](#getting-started "Direct link to Getting started")

The following solutions outline the steps to query Mistral Large on the SaaS version of IBM watsonx.ai.

### Pre-requisites[​](#pre-requisites "Direct link to Pre-requisites")

The following items are required:

*   An IBM watsonx project (`IBM_CLOUD_PROJECT_ID`)
*   A Service ID with an access policy enabling the use of the Watson Lachine Learning service.

To enable access to the API, you must make sure that:

*   Your Service ID has been added to the project as `EDITOR`,
*   You have generated an API key (`IBM_CLOUD_API_KEY`) for your Service ID.

### Querying the model (chat completion)[​](#querying-the-model-chat-completion "Direct link to Querying the model (chat completion)")

You can query Mistral Large using either IBM's SDK or plain HTTP calls.

warning

The examples below leverage the `mistral-common` Python package to properly format the user messages with special tokens. It is **strongly recommended to avoid passing raw strings and handle special tokens manually**: this might result in silent tokenization errors that would highly degrade the quality of the model output.

*   Python

You will need to run your code from a virtual environment with the following packages:

*   `httpx` (tested with `0.27.2`)
*   `ibm-watsonx-ai` (tested with `1.1.11`)
*   `mistral-common` (tested with `1.4.4`)

In the following snippet, your API key will be used to generate an IAM token, then the call to the model is performed using this token for authentication.

from ibm_watsonx_ai import Credentialsfrom ibm_watsonx_ai.foundation_models import ModelInferencefrom ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParamsfrom mistral_common.tokens.tokenizers.mistral import MistralTokenizerfrom mistral_common.protocol.instruct.request import ChatCompletionRequestfrom mistral_common.protocol.instruct.messages import UserMessageimport osimport httpxIBM_CLOUD_REGIONS = {        "dallas": "us-south",        "london": "eu-gb",        "frankfurt": "eu-de",        "tokyo": "jp-tok"        }IBM_CLOUD_PROJECT_ID = "xxx-xxx-xxx" # Replace with your project iddef get_iam_token(api_key: str) -> str:    """    Return an IAM access token generated from an API key.    """    headers = {"Content-Type": "application/x-www-form-urlencoded"}    data = f"apikey={api_key}&grant_type=urn:ibm:params:oauth:grant-type:apikey"    resp = httpx.post(        url="https://iam.cloud.ibm.com/identity/token",        headers=headers,        data=data,    )    token = resp.json().get("access_token")    return tokendef format_user_message(raw_user_msg: str) -> str:    """    Return a formatted prompt using the official Mistral tokenizer.    """    tokenizer = MistralTokenizer.v3()  # Use v3 for Mistral Large    tokenized = tokenizer.encode_chat_completion(        ChatCompletionRequest(            messages=[UserMessage(content=raw_user_msg)], model="mistral-large"        )    )    return tokenized.textregion = "frankfurt" # Define the region of your choice hereapi_key = os.environ["IBM_API_KEY"]access_token = get_iam_token(api_key=api_key)credentials = Credentials(url=f"https://{IBM_CLOUD_REGIONS[region]}.ml.cloud.ibm.com",                          token=access_token)params = {GenParams.MAX_NEW_TOKENS: 256, GenParams.TEMPERATURE: 0.0}model_inference = ModelInference(    project_id=IBM_CLOUD_PROJECT_ID,    model_id="mistralai/mistral-large",    params=params,    credentials=credentials,)user_msg_content = "Who is the best French painter? Answer in one short sentence."resp = model_inference.generate_text(prompt=format_user_message(user_msg_content))print(resp)

## Going further[​](#going-further "Direct link to Going further")

For more information and examples, you can check:

*   The [IBM watsonx.ai Python SDK documentation](https://ibm.github.io/watsonx-ai-python-sdk/index.html)
*   This [IBM Developer tutorial](https://developer.ibm.com/tutorials/awb-using-mistral-ai-llms-in-watsonx-ai-flows-engine/) on how to use Mistral Large with IBM watsonx.ai flows engine.

[

Previous

Snowflake Cortex

](/deployment/cloud/sfcortex/)[

Next

Outscale

](/deployment/cloud/outscale/)

*   [Introduction](#introduction)
*   [Getting started](#getting-started)
*   [Pre-requisites](#pre-requisites)
*   [Querying the model (chat completion)](#querying-the-model-chat-completion)
*   [Going further](#going-further)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025