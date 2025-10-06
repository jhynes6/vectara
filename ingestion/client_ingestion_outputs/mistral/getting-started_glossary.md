---
source: "website"
content_type: "blogs_resources"
url: "https://docs.mistral.ai/getting-started/glossary/"
title: "/getting-started/glossary/"
domain: "docs.mistral.ai"
path: "/getting-started/glossary/"
scraped_time: "2025-09-08T18:10:28.077731"
url_depth: 2
word_count: 1177
---

Glossary | Mistral AI

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
*   Glossary

On this page

# Glossary

## LLM[​](#llm "Direct link to LLM")

LLMs (Large Language Models), such as the Mistral AI models, are AI models trained on extensive text data to predict the next word in a sentence. They are capable of understanding and generating text in a way that's similar to how humans communicate. They can answer questions, draft documents, summarize texts, extract information, translate languages, write code, and more.

## Text generation[​](#text-generation "Direct link to Text generation")

Text generation in large language models is the process of producing coherent and contextually relevant text based on a given input prompt. These models, such as Mistral AI, are trained on vast amounts of text data to predict the next word in a sentence, given the previous words as context. This capability enables them to generate text that is similar to human communication and can be used for various applications, including answering questions, drafting documents, summarizing texts, translating languages, and coding.

## Tokens[​](#tokens "Direct link to Tokens")

Tokens serve as the smallest individual units that a language model processes, typically representing common sequences of characters such as words or subwords. In order for a language model to comprehend text, it must be converted into numerical representations. This is accomplished by encoding the text into a series of tokens, where each token is assigned a unique numerical index. The process of converting text into tokens is known as tokenization. One widely used tokenization algorithm is Byte-Pair Encoding (BPE), which initially treats each byte in a text as a separate token. BPE then iteratively adds new tokens to the vocabulary for the most frequent pair of tokens in the corpus, replacing occurrences of the pair with the new token, until no more replacements can be made. This results in a compact and efficient representation of the text for processing by the language model.

## Mixture of Experts[​](#mixture-of-experts "Direct link to Mixture of Experts")

Mixture of Experts (MoE) is the underlying architecture of Mixtral 8x7b and Mixtral 8x22b. It is a neural network architecture that incorporates expert layers within the Transformer block, allowing models to be pretrained with much less compute while maintaining the same quality as dense models. This is achieved by replacing dense feed-forward network (FFN) layers with sparse MoE layers, which contain multiple "experts" (FFNs). A gate network or router determines which input tokens are sent to which expert for computation. MoE offers benefits such as efficient pretraining and faster inference, but also presents challenges like overfitting during fine-tuning and high memory requirements. Nevertheless, MoE is a valuable method for achieving improved model quality at lower computing costs by dynamically assigning input tokens to specialized experts for processing.

## RAG[​](#rag "Direct link to RAG")

Retrieval-augmented generation (RAG) is an AI framework that synergizes the capabilities of LLMs and information retrieval systems. There are two main steps in RAG: 1) retrieval: retrieve relevant information from a knowledge base with text embeddings stored in a vector store; 2) generation: insert the relevant information to the prompt for the LLM to generate information. RAG is useful to answer questions or generate content leveraging external knowledge including up-to-date information and domain-specific information. RAG allows the model to access and utilize information beyond its training data, reducing hallucination and improving factual accuracy. Check out our [Basic RAG](/guides/rag/) guide for details.

## Fine-tuning[​](#fine-tuning "Direct link to Fine-tuning")

Fine-tuning is a process used in large language models to adapt a pre-trained model to a specific task or domain. It involves continuing the training process on a smaller, task-specific dataset and adjusting the model's parameters to optimize its performance on the new dataset. This enables the model to learn task-specific language patterns and improve its performance on the target task. Fine-tuning can be beneficial for adapting the model to a particular format or tone, domain-specific tasks, and improving performance through distillation from a larger model. This approach can achieve state-of-the-art performance with fewer data and computational resources compared to training a model from scratch.

## Function calling[​](#function-calling "Direct link to Function calling")

Function calling allows Mistral models to connect to external tools and call external functions or APIs to perform tasks beyond the model's capabilities. This allows the model to access and leverage external tools and resources to improve its performance and provide more accurate responses. Function calling can be used for tasks such as retrieving real-time data, performing calculations, accessing databases, and interacting with other systems or services. It improves the model's accuracy, efficiency, and versatility. Check out our [Function Calling](/capabilities/function_calling/) guide to learn more.

## Embeddings[​](#embeddings "Direct link to Embeddings")

Embeddings are vectorial representations of text that capture the semantic meaning of paragraphs through their position in a high dimensional vector space. These vectors capture the semantic meaning and context of the text, allowing the model to understand and generate language more effectively. Mistral AI Embeddings API offers cutting-edge, state-of-the-art embeddings for text, which can be used for many NLP tasks. Check out our [Embeddings](/capabilities/embeddings/overview/) guide to learn more.

## Temperature[​](#temperature "Direct link to Temperature")

Temperature is a fundamental sampling parameter in LLMs that controls the randomness and diversity of the generated outputs. Lower Temperature values result in more deterministic and accurate responses, while higher values introduce more creativity and randomness. This parameter affects the softmax function, which normalizes logits into a probability distribution. Higher Temperatures flatten the distribution, making less likely tokens more probable, while lower Temperatures sharpen the distribution, favoring the most likely tokens. Adjusting the Temperature allows for tailoring the model's behavior to suit different applications, such as requiring high accuracy for tasks like mathematics or classification, or enhancing creativity for tasks like brainstorming or writing novels. Balancing creativity and coherence is crucial, as increasing Temperature can also introduce inaccuracies. Some models, such as `pixtral-12b`, `ministral-3b-2410`, `ministral-8b-2410` and `open-mistral-nemo` have a factor of 0.43 on temperature when used via our services, to align better with how it impacts other models and unify model behaviour.

[

Previous

Changelog

](/getting-started/changelog/)[

Next

Text and Chat Completions

](/capabilities/completion/)

*   [LLM](#llm)
*   [Text generation](#text-generation)
*   [Tokens](#tokens)
*   [Mixture of Experts](#mixture-of-experts)
*   [RAG](#rag)
*   [Fine-tuning](#fine-tuning)
*   [Function calling](#function-calling)
*   [Embeddings](#embeddings)
*   [Temperature](#temperature)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright