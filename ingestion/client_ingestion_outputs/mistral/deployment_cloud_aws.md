---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/deployment/cloud/aws/"
title: "/deployment/cloud/aws/"
domain: "docs.mistral.ai"
path: "/deployment/cloud/aws/"
scraped_time: "2025-09-08T18:10:08.568577"
url_depth: 3
word_count: 640
---

AWS Bedrock | Mistral AI

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
*   AWS Bedrock

On this page

# AWS Bedrock

## Introduction[​](#introduction "Direct link to Introduction")

Mistral AI's open and commercial models can be deployed on the AWS Bedrock cloud platform as fully managed endpoints. AWS Bedrock is a serverless service so you don't have to manage any infrastructure.

As of today, the following models are available:

*   Mistral Large (24.07, 24.02)
*   Mistral Small (24.02)
*   Mixtral 8x7B
*   Mistral 7B

For more details, visit the [models](/getting-started/models/models_overview/) page.

## Getting started[​](#getting-started "Direct link to Getting started")

The following sections outline the steps to deploy and query a Mistral model on the AWS Bedrock platform.

The following items are required:

*   Access to an **AWS account** within a region that supports the AWS Bedrock service and offers access to your model of choice: see [the AWS documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) for model availability per region.
*   An AWS **IAM principal** (user, role) with sufficient permissions, see [the AWS documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html) for more details.
*   A local **code environment** set up with the relevant AWS SDK components, namely:
*   the AWS CLI: see [the AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) for the installation procedure.
*   the `boto3` Python library: see the [AWS documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) for the installation procedure.

### Requesting access to the model[​](#requesting-access-to-the-model "Direct link to Requesting access to the model")

Follow the instructions on [the AWS documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) to unlock access to the Mistral model of your choice.

### Querying the model[​](#querying-the-model "Direct link to Querying the model")

AWS Bedrock models are accessible through the Converse API.

Before running the examples below, make sure to sure to :

*   Properly configure the authentication credentials for your development environment. [The AWS documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) provides an in-depth explanation on the required steps.
*   Create a Python virtual environment with the `boto3` package (version >= `1.34.131`).
*   Set the following environment variables:
*   `AWS_REGION`: The region where the model is deployed (e.g. `us-west-2`),
*   `AWS_BEDROCK_MODEL_ID`: The model ID (e.g. `mistral.mistral-large-2407-v1:0`).

*   Python
*   AWS CLI

import boto3import osregion = os.environ.get("AWS_REGION")model_id = os.environ.get("AWS_BEDROCK_MODEL_ID")bedrock_client = boto3.client(service_name='bedrock-runtime', region_name=region)user_msg = "Who is the best French painter? Answer in one short sentence."messages = [{"role": "user", "content": [{"text": user_msg}]}]temperature = 0.0max_tokens = 1024params = {"modelId": model_id,          "messages": messages,          "inferenceConfig": {"temperature": temperature,                              "maxTokens": max_tokens}}resp = bedrock_client.converse(**params)print(resp["output"]["message"]["content"][0]["text"])

aws bedrock-runtime converse \ --region $AWS_REGION \ --model-id $AWS_BEDROCK_MODEL_ID \ --messages '[{"role": "user", "content": [{"text": "Who is the best French painter? Answer in one short sentence."}]}]'

## Going further[​](#going-further "Direct link to Going further")

For more details and examples, refer to the following resources:

*   [AWS GitHub repository with multiple examples and use-cases leveraging Mistral models](https://github.com/aws-samples/mistral-on-aws).
*   [AWS documentation on the Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html).
*   [AWS documentation on inference requests for Mistral models](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-mistral.html#model-parameters-mistral-request-response).

[

Previous

Azure AI

](/deployment/cloud/azure/)[

Next

Vertex AI

](/deployment/cloud/vertex/)

*   [Introduction](#introduction)
*   [Getting started](#getting-started)
*   [Requesting access to the model](#requesting-access-to-the-model)
*   [Querying the model](#querying-the-model)
*   [Going further](#going-further)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025