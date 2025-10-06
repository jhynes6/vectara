---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/capabilities/finetuning/finetuning_overview/"
title: "/capabilities/finetuning/finetuning_overview/"
domain: "docs.mistral.ai"
path: "/capabilities/finetuning/finetuning_overview/"
scraped_time: "2025-09-08T18:09:40.854575"
url_depth: 3
word_count: 593
---

Fine-tuning Overview | Mistral AI

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

*   [Classifier Factory](/capabilities/finetuning/classifier_factory/)
*   [Text & Vision Fine-tuning](/capabilities/finetuning/text_vision_finetuning/)
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
*   Finetuning

On this page

# Fine-tuning Overview

warning

Every fine-tuning job comes with a minimum fee of $4, and there's a monthly storage fee of $2 for each model. For more detailed pricing information, please visit our [pricing page](https://mistral.ai/technology/#pricing).

## Fine-tuning Basics[​](#fine-tuning-basics "Direct link to Fine-tuning Basics")

### Fine-tuning vs. Prompting[​](#fine-tuning-vs-prompting "Direct link to Fine-tuning vs. Prompting")

When deciding whether to use prompt engineering or fine-tuning for an AI model, it can be difficult to determine which method is best. It's generally recommended to start with prompt engineering, as it's faster and less resource-intensive. To help you choose the right approach, here are the key benefits of prompting and fine-tuning:

*   **Benefits of Prompting**

*   A generic model can work out of the box (the task can be described in a zero shot fashion)
*   Does not require any fine-tuning data or training to work
*   Can easily be updated for new workflows and prototyping

Check out our [prompting guide](https://docs.mistral.ai/guides/prompting_capabilities/) to explore various capabilities of Mistral models.

*   **Benefits of Fine-tuning**

*   Works significantly better than prompting
*   Typically works better than a larger model (faster and cheaper because it doesn't require a very long prompt)
*   Provides a better alignment with the task of interest because it has been specifically trained on these tasks
*   Can be used to teach new facts and information to the model (such as advanced tools or complicated workflows)

### Common use cases[​](#common-use-cases "Direct link to Common use cases")

Fine-tuning has a wide range of use cases, some of which include:

*   Customizing the model to generate responses in a specific format and tone
*   Specializing the model for a specific topic or domain to improve its performance on domain-specific tasks
*   Improving the model through distillation from a stronger and more powerful model by training it to mimic the behavior of the larger model
*   Enhancing the model’s performance by mimicking the behavior of a model with a complex prompt, but without the need for the actual prompt, thereby saving tokens, and reducing associated costs
*   Reducing cost and latency by using a small yet efficient fine-tuned model

## Fine-tuning Services[​](#fine-tuning-services "Direct link to Fine-tuning Services")

*   [Text & Vision General Fine-tuning](/capabilities/finetuning/text_vision_finetuning/):
*   **SFT**: Supervised Fine-tuning, the most common fine-tuning method to teach the model knowledge and how to follow instructions.
*   [Classifier Factory](/capabilities/finetuning/classifier_factory/): A tool to finetune and create classifier specific models from a dataset of text.

[

Previous

Moderation

](/capabilities/guardrailing/)[

Next

Classifier Factory

](/capabilities/finetuning/classifier_factory/)

*   [Fine-tuning Basics](#fine-tuning-basics)
*   [Fine-tuning vs. Prompting](#fine-tuning-vs-prompting)
*   [Common use cases](#common-use-cases)
*   [Fine-tuning Services](#fine-tuning-services)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025