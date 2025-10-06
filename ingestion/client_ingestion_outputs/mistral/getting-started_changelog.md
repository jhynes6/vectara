---
source: "website"
content_type: "blogs_resources"
url: "https://docs.mistral.ai/getting-started/changelog/"
title: "/getting-started/changelog/"
domain: "docs.mistral.ai"
path: "/getting-started/changelog/"
scraped_time: "2025-09-08T18:09:54.842627"
url_depth: 2
word_count: 1249
---

Changelog | Mistral AI

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
*   Changelog

# Changelog

August 27, 2025

*   Added a new parameter `p` to the chunks streamed back by the Completion API.
*   Implemented for security to prevent token-length side-channel attacks, as reported by Microsoft researchers.
*   Note that this change may break applications relying on strict parsing of the chunks. Applications using the official SDK are unaffected, but users relying on the `mistral-common` package may need to update to `1.8.4` or higher.

August 12, 2025

*   We released Mistral Medium 3.1 (`mistral-medium-2508`).

July 30, 2025

*   We released Codestral 2508 (`codestral-2508`).

July 24, 2025

*   We released Magistral Medium 1.1 (`magistral-medium-2507`) and Magistral Small 1.1 (`magistral-small-2507`).
*   We released a Document Library API to manage libraries.
*   SDK support for Audio and Transcription available.

July 15, 2025

*   We released our first Audio models for chat and a Transcription API:
*   Voxtral Small (`voxtral-small-2507`) available for chat use cases
*   Voxtral Mini (`voxtral-mini-2507`) available for chat use cases
*   Voxtral Mini Transcribe (`voxtral-mini-2507` via `audio/transcriptions`) optimized for transcription

July 10, 2025

*   We released Devstral Small 1.1 (`devstral-small-2507`) and Devstral Medium (`devstral-medium-2507`).

June 23, 2025

*   Mistral Small 3.2 API available (`mistral-small-2506`).

June 20, 2025

*   We released Mistral Small 3.2.

June 10, 2025

*   We released Magistral Medium (`magistral-medium-2506`) and Magistral Small (`magistral-small-2506`).

May 28, 2025

*   We released Codestral Embed (`codestral-embed`).

May 27, 2025

*   We released the new [Agents API](/agents/agents_introduction/).

May 22, 2025

*   We released Mistral OCR 2505 (`mistral-ocr-2505`) and [annotations](/capabilities/document_ai/annotations/).

May 21, 2025

*   We released Devstral Small (`devstral-small-2505`).

May 7, 2025

*   We released Mistral Medium 3 (`mistral-medium-2505`).

April 16, 2025

*   We released the [Classifier Factory](/capabilities/finetuning/classifier_factory/).

March 17, 2025

*   We released Mistral Small 3.1 (`mistral-small-2503`).

March 6, 2025

*   We released Mistral OCR (`mistral-ocr-2503`) and [document understanding](/capabilities/document_ai/basic_ocr/).

February 17, 2025

*   We released Mistral Saba (`mistral-saba-2502`).

January 30, 2025

*   We released Mistral Small 3 (`mistral-small-2501`).

January 28, 2025

*   We released custom [structured outputs](/capabilities/structured-output/custom_structured_output/) for all models.

January 13, 2025

*   We released Codestral 2501 (`codestral-2501`).

November 18, 2024

*   We released Mistral Large 2.1 (`mistral-large-2411`) and Pixtral Large (`pixtral-large-2411`).
*   [Le Chat](https://chat.mistral.ai/):
*   Web search with citations
*   Canvas for ideation, in-line editing, and export
*   State of the art document and image understanding, powered by the new multimodal Pixtral Large
*   Image generation, powered by Black Forest Labs Flux Pro
*   Fully integrated offering, from models to outputs
*   Faster responses powered by speculative editing

November 6, 2024

*   We released moderation API and batch API.
*   We introduced three new parameters:
*   `presence_penalty`: penalizes the repetition of words or phrases
*   `frequency_penalty`: penalizes the repetition of words based on their frequency in the generated text
*   `n`: number of completions to return for each request, input tokens are only billed once.

November 6, 2024

*   We downscaled the temperature parameter of `pixtral-12b`, `ministral-3b-2410`, and `ministral-8b-2410` by a multiplier of 0.43 to improve consistency, quality, and unify model behavior.

October 9, 2024

*   We released Ministral 3B (`ministral-3b-2410`) and Ministral 8B (`ministral-8b-2410`).

September 17, 2024

*   We released Pixtral (`pixtral-12b-2409`) and Mistral Small v24.09 (`mistral-small-2409`).
*   We reduced price on our flagship model, Mistral Large 2.
*   We introduced a free API tier on La Plateforme.

September 13, 2024

*   In le Chat, we added a mitigation against an obfuscated prompt method that could lead to data exfiltration, reported by researchers [Xiaohan Fu](https://xhfu.me/) and Earlence Fernandes. The attack required users to willingfully copy and paste adversarial prompts and provide personal data to the model. No user was impacted and no data was exfiltrated.

July 29, 2024

*   We released version 1.0 of our Python and JS SDKs with major upgrades and syntax changes. Check out our [migration guide](https://github.com/mistralai/client-python/blob/main/MIGRATION.md) for details.
*   We released Agents API. See details [here](/agents/agents_introduction/).

July 24, 2024

*   We released Mistral Large 2 (`mistral-large-2407`).
*   We added fine-tuning support for Codestral, Mistral Nemo and Mistral Large. Now the model choices for fine-tuning are `open-mistral-7b` (v0.3), `mistral-small-latest` (`mistral-small-2402`), `codestral-latest` (`codestral-2405`), `open-mistral-nemo` and , `mistral-large-latest` (`mistral-large-2407`)

July 18, 2024

*   We released Mistral Nemo (`open-mistral-nemo`).

July 16, 2024

*   We released Codestral Mamba (`open-codestral-mamba`) and Mathstral.

Jun 5, 2024

*   We released fine-tuning API. Check out the [capability docs](/capabilities/finetuning/finetuning_overview/) and [guides](/guides/finetuning/).

May 29, 2024

*   New model available: `codestral-latest` (aka `codestral-2405`). Check out the code generation [docs](/capabilities/code_generation/).

May 23, 2024

*   Function calling: `tool_call_id` is now mandatory in chat messages with the `tool` role.

Apr. 17, 2024

*   New model available: `open-mixtral-8x22b` (aka `open-mixtral-8x22b-2404`). Check the release [blog](https://mistral.ai/news/mixtral-8x22b/) for details.
*   For function calling, `tool_call_id` must not be null for `open-mixtral-8x22b`.
*   We released three versions of tokenizers for commercial and open-weight models: check the related [guide](/guides/tokenization/) and [repo](https://github.com/mistralai/mistral-common) for more details.

Mar. 28, 2024

*   JSON mode now available for all models on La Plateforme.

Feb. 26, 2024

*   API endpoints: We renamed 3 API endpoints and added 2 model endpoints.

*   `open-mistral-7b` (aka `mistral-tiny-2312`): renamed from `mistral-tiny`. The endpoint `mistral-tiny` will be deprecated in three months.
*   `open-mixtral-8x7B` (aka `mistral-small-2312`): renamed from `mistral-small`. The endpoint `mistral-small` will be deprecated in three months.
*   `mistral-small-latest` (aka `mistral-small-2402`): new model.
*   `mistral-medium-latest` (aka `mistral-medium-2312`): old model. The previous `mistral-medium` has been dated and tagged as `mistral-medium-2312`. The endpoint `mistral-medium` will be deprecated in three months.
*   `mistral-large-latest` (aka `mistral-large-2402`): our new flagship model with leading performance.
*   New API capabilities:

*   [Function calling](/capabilities/function_calling/): available for Mistral Small and Mistral Large.
*   [JSON mode](/capabilities/structured-output/json_mode/): available for Mistral Small and Mistral Large
*   [La Plateforme](https://console.mistral.ai/):

*   We added multiple currency support to the payment system, including the option to pay in US dollars.
*   We introduced enterprise platform features including admin management, which allows users to manage individuals from your organization.
*   [Le Chat](https://chat.mistral.ai/):

*   We introduced the brand new chat interface Le Chat to easily interact with Mistral models.
*   You can currently interact with three models: Mistral Large, Mistral Next, and Mistral Small.

Jan. 11, 2024

*   We have enhanced the API's strictness. Previously the API would silently ignores unsupported parameters in the requests, but it now strictly enforces the validity of all parameters. If you have unsupported parameters in your request, you will see the error message "Extra inputs are not permitted".
*   A previous version of the [guardrailing documentation](/capabilities/guardrailing/) incorrectly referred to the API parameter as `safe_mode` instead of `safe_prompt`. We corrected this in the documentation.

Jan. 16, 2024

*   We added token usage information in streaming requests. You can find it in the last chunk returned.

[

Previous

Developer examples

](/getting-started/stories/)[

Next

Glossary

](/getting-started/glossary/)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025 Mistral AI