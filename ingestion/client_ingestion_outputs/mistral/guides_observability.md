---
source: "website"
content_type: "blogs_resources"
url: "https://docs.mistral.ai/guides/observability/"
title: "/guides/observability/"
domain: "docs.mistral.ai"
path: "/guides/observability/"
scraped_time: "2025-09-08T18:10:27.917722"
url_depth: 2
word_count: 2128
---

Observability | Mistral AI

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
*   Observability

On this page

# Observability

## Why observability?[​](#why-observability "Direct link to Why observability?")

Observability is essential for Large Language Model (LLM) systems across prototyping, testing, and production for several reasons:

*   **Visibility**: Observability provides detailed insights into the internal states of LLM applications, allowing developers to understand system behavior. This visibility is crucial for identifying and diagnosing issues and debugging.
*   **Production requirement**: Implementing observability in production environments address critical requirements including monitoring, scalability, security and compliance.
*   **Reproducibility**: Observability enables developers to observe and reproduce LLM system behavior.
*   **Continuous improvement**: The insights gained from observability data can be used to drive continuous improvement initiatives.

## What components do we observe?[​](#what-components-do-we-observe "Direct link to What components do we observe?")

The short answer is: anything and everything!

An LLM (Large Language Model) application can include one or more LLM calls. Understanding both the details at the individual API call level and the sequence of these calls at the application level is crucial:

1.  **Individual LLM call level**: at the individual LLM API call level, an LLM receives an input prompt and generates an output. Therefore, we can monitor and observe three key components: input prompt, model, and output.

2.  **Application level**: At the application level, it’s important to observe the pattern, logistics and sequence of LLM calls. This sequence determines the flow of information and the order in which LLMs are called and which tasks are executed.

## Individual level: what components can we observe?[​](#individual-level-what-components-can-we-observe "Direct link to Individual level: what components can we observe?")

For effective observability, we need to monitor and record detailed information for each version of each component involved in the interaction with the LLM. Here's a breakdown of what to observe and some expected modules in an observability tool:

### Input prompt[​](#input-prompt "Direct link to Input prompt")

*   **Prompt template**
*   The standardized format or structure used to generate the input prompt, including any placeholders or variables within the template.
*   Observability tools often provide a registry of prompt templates that the community or an organization can use and share.
*   **Examples**
*   Few-shot in-context learning is often effective in prompt engineering. Specific examples or sample inputs can be used to guide the model's response used.
*   **Retrieve context**
*   In a Retrieval-Augmented Generation (RAG) system, relevant context is retrieved from external sources or databases to provide information for the LLM, making the results more reliable.
*   **Memory**
*   Historical data or previous interactions stored in memory.
*   How this memory is used to influence the current prompt, such as summarizing past memory, retrieving relevant memory, or using the most recent memory.
*   **Tools**
*   Any tools or utilities used to preprocess or enhance the input prompt.
*   Tools are becoming increasingly important in LLM applications, serving as the bridge to real-life applications.
*   Specific configurations or settings applied by these tools and their impact.

### Model[​](#model "Direct link to Model")

*   **Models specs**
*   The specific version or identifier of the model being used.
*   Configuration settings, hyperparameters, and any customizations applied to the model.

### Output[​](#output "Direct link to Output")

*   **Formatting**
*   The structure and format of the output generated by the model.

## Application level: what workflow patterns can we observe?[​](#application-level-what-workflow-patterns-can-we-observe "Direct link to Application level: what workflow patterns can we observe?")

An LLM system often composed of more than just one LLM. At the application level, there are specific workflow patterns that require specific observability in each step of the workflow. Here is some example workflows:

*   **RAG**
*   A RAG system includes the document retrieval step in addition to the generation step from an LLM. Additional observability is needed to track and monitor the external document/dataset and the retrieval step.
*   **LLM as part of a system**
*   An LLM system could involve multiple LLMs chained together, [flow engineering](https://x.com/karpathy/status/1748043513156272416) with various iterations, or a complicated multi-agent system, for example to create a simulated world. The input and output of each step need to be observed to understand the overall system behavior, identify bottlenecks, and ensure the system's reliability and performance.
*   **Fine-tuning**
*   Fine-tuning is a distinct workflow that might be part of a larger workflow or a prerequisite step of another workflow. It involves preparing a fine-tuning dataset, uploading data, creating a fine-tuning job, and using a fine-tuned model. Each of these steps, especially the fine-tuning training job, could benefit from observability to track fine-tuning datasets, monitor progress, identify issues, and ensure the quality of the fine-tuned model.

## What metrics do we observe?[​](#what-metrics-do-we-observe "Direct link to What metrics do we observe?")

At each step of the LLM system workflow, we can observe the following and set overall Service Level Objectives (SLOs), alerts, and monitoring:

### Token and cost[​](#token-and-cost "Direct link to Token and cost")

*   Track the number of tokens processed and the associated costs.

### Traces and latency[​](#traces-and-latency "Direct link to Traces and latency")

*   Trace the system workflow to observe and monitor the sequence of operations.
*   Measure and monitor latency to identify performance bottlenecks and ensure timely responses.

### Anomalies and errors[​](#anomalies-and-errors "Direct link to Anomalies and errors")

*   Identify issues within the system promptly.
*   Build datasets for testing
*   Understand patterns and use cases from thumbs down cases for example
*   Monitor error rates and negative feedback over time.

### Quality[​](#quality "Direct link to Quality")

In an observability tool, we should be able to monitor key performance indicators through the evaluation, feedback, and annotation:

*   **Evaluation**
*   Metrics and criteria used to evaluate the quality and relevance of the output.
*   Observability tools often provide comprehensive evaluation toolkits for creating evaluation datasets, annotating, evaluating, and comparing model results.
*   **Feedback**
*   User feedback on the output, including ratings, comments, and suggestions.
*   Any automated feedback mechanisms or systems in place to collect and analyze user feedback.
*   **Annotation**
*   Manual or automated annotations added to the output for further analysis and potentially added to the evaluation or fine-tuning dataset.

## Integrations[​](#integrations "Direct link to Integrations")

Mistral integrates with several observability tools to help you monitor and ensure more reliable and high-performing LLM applications.

### Integration with LangSmith[​](#integration-with-langsmith "Direct link to Integration with LangSmith")

LangSmith provides observability throughout the LLM application development lifecycle.

![drawing](/img/guides/obs_langchain0.png)

**Pros:**

*   LangSmith is compatible with both the LangChain ecosystem and external systems.
*   Deployment option coming soon.
*   It offers a broad range of observable areas, serving as an all-in-one platform.

**Mistral integration Example:**

*   All of the [langchain notebooks](https://github.com/mistralai/cookbook/tree/main/third_party/langchain) in the Mistral cookbook include LangSmith integration.

Here is an example tracking traces, input, output, documents, tokens, and status when we run the [corrective RAG example](https://github.com/mistralai/cookbook/blob/main/third_party/langchain/corrective_rag_mistral.ipynb) from the Mistral cookbook.

![drawing](/img/guides/obs_langchain.png)

### Integration with 🪢 Langfuse[​](#integration-with--langfuse "Direct link to Integration with 🪢 Langfuse")

[Langfuse](https://langfuse.com) ([GitHub](https://github.com/langfuse/langfuse)) is an open-source platform for LLM engineering. It provides tracing and monitoring capabilities for AI applications, helping developers debug, analyze, and optimize their products. Langfuse integrates with various tools and frameworks via native integrations, OpenTelemetry, and SDKs.

![drawing](/img/guides/obs_langfuse.png)

**Pros:**

*   Most used open-source LLMOps platform ([blog post](https://langfuse.com/blog/2024-11-most-used-oss-llmops))
*   Model and framework agnostic
*   Built for production
*   Incrementally adoptable, start with one feature and expand to the full platform over time
*   API-first, all features are available via API for custom integrations
*   Optionally, Langfuse can be easily self-hosted

**Mistral integration example:**

*   [Step-by-step guide](https://langfuse.com/docs/integrations/mistral-sdk) on tracing Mistral models with Langfuse.
*   [Cookbook](https://langfuse.com/guides/cookbook/integration_llama_index_posthog_mistral) on building a RAG application with Mistral and LlamaIndex and trace the steps with Langfuse.

![drawing](/img/guides/obs_langfuse2.png)

_[Public example trace in Langfuse](https://cloud.langfuse.com/project/cloramnkj0002jz088vzn1ja4/traces/a3360c6f-24ad-455c-aae7-eb9d5c6f5dac?observation=767f8ac1-0c7d-412f-8fd8-2642acb267c6&display=preview)_

### Integration with Arize Phoenix[​](#integration-with-arize-phoenix "Direct link to Integration with Arize Phoenix")

Phoenix is an open-source observability library designed for experimentation, evaluation, and troubleshooting. It is designed to support agents, RAG pipelines, and other LLM applications.

**Pros:**

*   Open-source ([Github](https://github.com/Arize-ai/phoenix)), and built on OpenTelemetry
*   Can be [self-hosted](https://docs.arize.com/phoenix/setup/environments#container), accessed via [cloud](https://docs.arize.com/phoenix/hosted-phoenix), or run directly in a [notebook](https://docs.arize.com/phoenix/setup/environments#notebooks)
*   Provides a [Mistral integration](https://docs.arize.com/phoenix/tracing/integrations-tracing/mistralai) to automatically trace Client.chat and Agent.chat calls
*   Strong analytical platform, with a copilot agent to help debug your application

**Mistral integration Example:** Here is an [example notebook](https://github.com/mistralai/cookbook/blob/main/third_party/Phoenix/arize_phoenix_tracing.ipynb) that shows how to trace Mistral chat.complete and tool calls in Phoenix.

![drawing](/img/guides/obs_phoenix1.png)

### Integration with Weights and Biases[​](#integration-with-weights-and-biases "Direct link to Integration with Weights and Biases")

Weights & Biases is an end-to-end AI developer platform for ML and LLM workflows used for both fine-tuning and LLM application building. Use W&B Weave to evaluate, monitor, and iterate on GenAI applications, and W&B Models as a system of record to train, fine-tune, and manage AI models.

![drawing](/img/guides/obs_wandb.png)

**Pros:**

*   Platform for both LLM app development and fine-tuning
*   Integrated with [Mistral API](https://weave-docs.wandb.ai/guides/integrations/mistral/)
*   Get started by adding one line: `weave.init('my-project')`
*   Automatically tracks inputs, output, context, errors, evaluation metrics & traces
*   Integrated with [Mistral fine-tuning service](/guides/finetuning/#integration-with-weights-and-biases)
*   Track training metrics while fine-tuning
*   Compare training experiments

**Mistral integration Example:**

To get you started you can check our recent webinar "Fine-tuning an LLM judge to reduce hallucination" and the [cookbook](https://github.com/mistralai/cookbook/tree/main/third_party/wandb).

### Integration with PromptLayer[​](#integration-with-promptlayer "Direct link to Integration with PromptLayer")

PromptLayer is a platform for prompt management, collaboration, monitoring, and evaluation. Good for hackers and production teams alike.

**Pros:**

*   No-code CMS for prompt management and versioning
*   Native support for Mistral
*   Prompts are model agnostic by default
*   Simple prompt tracking and observability

**Mistral integration:**

### Integration with AgentOps[​](#integration-with-agentops "Direct link to Integration with AgentOps")

AgentOps is an open-source observability and DevTool platform for AI Agents. It helps developers build, evaluate, and monitor AI agents.

**Pros:**

*   Open-source
*   Designed for observing agents
*   Allow for time travel
*   Integrates with CrewAI, AutoGen, & LangChain

**Mistral integration Example:**

[https://github.com/mistralai/cookbook/blob/main/third\_party/CAMEL\_AI/camel\_roleplaying\_scraper.ipynb](https://github.com/mistralai/cookbook/blob/main/third_party/CAMEL_AI/camel_roleplaying_scraper.ipynb)

![drawing](/img/guides/obs_agentops.png)

### Integration with phospho[​](#integration-with-phospho "Direct link to Integration with phospho")

[phospho](https://phospho.ai/) is a text analytics platform that makes it easy to get answers, take decisions and reduce churn by data mining user messages.

![drawing](/img/guides/obs_phospho.png)

**Pros:**

*   Open-source ([github](https://github.com/phospho-app)) platform
*   No code clustering and analytics
*   Customizable dashboards
*   Many integrations with other observability frameworks, languages, APIs…

**Mistral integration example:**

*   Check out the [phospho notebooks](https://github.com/mistralai/cookbook/tree/main/third_party/phospho) in the Mistral cookbook.

![drawing](/img/guides/obs_phospho2.png)

### Integration with MLflow[​](#integration-with-mlflow "Direct link to Integration with MLflow")

MLflow is a unified, end-to-end, open source MLOps platform for both traditional ML and GenAI applications, providing comprehensive tracing capabilities to monitor and analyze the execution of GenAI applications.

**Pros:**

*   Open-source ([Github](https://github.com/mlflow/mlflow))
*   Add Mistral integration with one line: `mlflow.mistral.autolog()` and get full tracing of chat and embedding calls.
*   Can be [run locally or self-hosted](https://mlflow.org/docs/latest/getting-started/intro-quickstart/index.html), or used via one of the available [Managed MLflow services](https://mlflow.org/docs/latest/introduction/index.html#running-mlflow-anywhere)
*   Provides complete model evaluation, versioning, and deployment capabilities, in addition to tracing and experiment tracking.

**Mistral integration Example:** Here is an [example notebook](https://github.com/mistralai/cookbook/blob/main/third_party/MLflow/mistral-mlflow-tracing.ipynb).

![drawing](/img/guides/obs_mlflow.png)

### Integration with Maxim[​](#integration-with-maxim "Direct link to Integration with Maxim")

Maxim AI provides comprehensive observability for your Mistral based AI applications. With Maxim's one-line integration, you can easily trace and analyse LLM calls, metrics, and more.

**Pros:**

*   Performance Analytics: Track latency, tokens consumed, and costs
*   Advanced Visualisation: Understand agent trajectories through intuitive dashboards

**Mistral integration Example:**

*   Learn how to integrate Maxim observability with the Mistral SDK in just one line of code - [Colab Notebook](https://github.com/mistralai/cookbook/blob/main/third_party/Maxim/cookbook_maxim_mistral_integration.ipynb)

Maxim Documentation to use Mistral as an LLM Provider and Maxim as Logger - [Docs Link](https://www.getmaxim.ai/docs/sdk/python/integrations/mistral/mistral)

![Gif](https://raw.githubusercontent.com/akmadan/platform-docs-public/docs/observability-maxim-provider/static/img/guides/maxim_traces.gif)

[

Previous

Evaluation

](/guides/evaluation/)[

Next

Other resources

](/guides/resources/)

*   [Why observability?](#why-observability)
*   [What components do we observe?](#what-components-do-we-observe)
*   [Individual level: what components can we observe?](#individual-level-what-components-can-we-observe)
*   [Input prompt](#input-prompt)
*   [Model](#model)
*   [Output](#output)
*   [Application level: what workflow patterns can we observe?](#application-level-what-workflow-patterns-can-we-observe)
*   [What metrics do we observe?](#what-metrics-do-we-observe)
*   [Token and cost](#token-and-cost)
*   [Traces and latency](#traces-and-latency)
*   [Anomalies and errors](#anomalies-and-errors)
*   [Quality](#quality)
*   [Integrations](#integrations)
*   [Integration with LangSmith](#integration-with-langsmith)
*   [Integration with 🪢 Langfuse](#integration-with--langfuse)
*   [Integration with Arize Phoenix](#integration-with-arize-phoenix)
*   [Integration with Weights and Biases](#integration-with-weights-and-biases)
*   [Integration with PromptLayer](#integration-with-promptlayer)
*   [Integration with AgentOps](#integration-with-agentops)
*   [Integration with phospho](#integration-with-phospho)
*   [Integration with MLflow](#integration-with-mlflow)
*   [Integration with Maxim](#integration-with-maxim)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](htt