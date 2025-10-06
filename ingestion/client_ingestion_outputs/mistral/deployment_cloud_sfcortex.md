---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/deployment/cloud/sfcortex/"
title: "/deployment/cloud/sfcortex/"
domain: "docs.mistral.ai"
path: "/deployment/cloud/sfcortex/"
scraped_time: "2025-09-08T18:10:11.780799"
url_depth: 3
word_count: 545
---

Snowflake Cortex | Mistral AI

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
*   Snowflake Cortex

On this page

# Snowflake Cortex

## Introduction[​](#introduction "Direct link to Introduction")

Mistral AI's open and commercial models can be leveraged from the Snowflake Cortex platform as fully managed endpoints. Mistral models on Snowflake Cortex are serverless services so you don't have to manage any infrastructure.

As of today, the following models are available:

*   Mistral Large
*   Mistral 7B

For more details, visit the [models](/getting-started/models/models_overview/) page.

## Getting started[​](#getting-started "Direct link to Getting started")

The following sections outline the steps to query the latest version of Mistral Large on the Snowflake Cortex platform.

### Getting access to the model[​](#getting-access-to-the-model "Direct link to Getting access to the model")

The following items are required:

*   The associated Snowflake account must be in a compatible region (see the [region list](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#availability) in the Snowflake documentation).
*   The principal that is calling the model must have the `CORTEX_USER` database role.

### Querying the model (chat completion)[​](#querying-the-model-chat-completion "Direct link to Querying the model (chat completion)")

The model can be called either directly in SQL or in Python using Snowpark ML. It is exposed via the [`COMPLETE` _LLM function_](https://docs.snowflake.com/en/sql-reference/functions/complete-snowflake-cortex).

*   SQL
*   Python

SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large2', 'Who is the best French painter? Answer in one short sentence.');

Execute this code either from a hosted Snowflake notebook or from your local machine.

For local execution you need to:

*   Create a virtual environment with the following package:
*   `snowflake-ml-python` (tested with version `1.6.1`)
*   Ensure that you have a [configuration file](https://docs.snowflake.com/en/user-guide/snowsql-config) with the proper credentials on your system. The example below assumes that you have a named connection called `mistral` that is configured appropriately.

from snowflake.snowpark import Sessionfrom snowflake.ml.utils import connection_paramsfrom snowflake.cortex import Complete# Start session (local execution only)params = connection_params.SnowflakeLoginOptions(connection_name="mistral")session = Session.builder.configs(params).create()# Query the modelprompt = "Who is the best French painter? Answer in one short sentence."completion = Complete(model="mistral-large2", prompt=prompt)print(completion)

## Going further[​](#going-further "Direct link to Going further")

For more information and examples, you can check the Snowflake documentation for:

*   [LLM functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions)
*   The API of the `COMPLETE` function in [SQL](https://docs.snowflake.com/en/sql-reference/functions/complete-snowflake-cortex) and [Python](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/model/snowflake.cortex.Complete).

[

Previous

Vertex AI

](/deployment/cloud/vertex/)[

Next

IBM watsonx.ai

](/deployment/cloud/ibm-watsonx/)

*   [Introduction](#introduction)
*   [Getting started](#getting-started)
*   [Getting access to the model](#getting-access-to-the-model)
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