---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/deployment/self-deployment/cerebrium/"
title: "/deployment/self-deployment/cerebrium/"
domain: "docs.mistral.ai"
path: "/deployment/self-deployment/cerebrium/"
scraped_time: "2025-09-08T18:10:20.508335"
url_depth: 3
word_count: 804
---

Deploy with Cerebrium | Mistral AI

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

*   [vLLM](/deployment/self-deployment/vllm/)
*   [TensorRT](/deployment/self-deployment/trt/)
*   [Deploy with SkyPilot](/deployment/self-deployment/skypilot/)
*   [Deploy with Cerebrium](/deployment/self-deployment/cerebrium/)
*   [Deploy with Cloudflare Workers AI](/deployment/self-deployment/cloudflare/)
*   [Text Generation Inference](/deployment/self-deployment/tgi/)
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
*   [Self-deployment](/deployment/self-deployment/overview/)
*   Deploy with Cerebrium

On this page

# Deploy with Cerebrium

[Cerebrium](https://www.cerebrium.ai/) is a serverless AI infrastructure platform that makes it easier for companies to build and deploy AI based applications. They offer Serverless GPU's with low cold start times with over 12 varieties of GPU chips that auto scale and you only pay for the compute you use.

## Setup Cerebrium[​](#setup-cerebrium "Direct link to Setup Cerebrium")

First, we install Cerebrium and login to get authenticated.

pip install cerebriumcerebrium login

Then let us create our first project

cerebrium init mistral-vllm

## Setup Environment and Hardware[​](#setup-environment-and-hardware "Direct link to Setup Environment and Hardware")

You set up your environment and hardware in the **cerebrium.toml** file that was created using the init function above. Here we are using a Ampere A10 GPU etc. You can read more [here](https://docs.cerebrium.ai/cerebrium/environments/custom-images)

[cerebrium.deployment]name = "mistral-vllm"python_version = "3.11"docker_base_image_url = "debian:bookworm-slim"include = "[./*, main.py, cerebrium.toml]"exclude = "[.*]"[cerebrium.hardware]cpu = 2memory = 14.0compute = "AMPERE_A10"gpu_count = 1provider = "aws"region = "us-east-1"[cerebrium.dependencies.pip]sentencepiece = "latest"torch = ">=2.0.0"vllm = "latest"transformers = ">=4.35.0"accelerate = "latest"xformers = "latest"

## Setup inference[​](#setup-inference "Direct link to Setup inference")

Running code in Cerebrium is like writing normal python with no special syntax. In your **main.py** specify the following:

from vllm import LLM, SamplingParamsfrom huggingface_hub import loginfrom cerebrium import get_secret# Your huggingface token (HF_AUTH_TOKEN) should be stored in your project secrets on your Cerebrium dashboardlogin(token=get_secret("HF_AUTH_TOKEN"))# Initialize the modelllm = LLM(model="mistralai/Mistral-7B-Instruct-v0.3", dtype="bfloat16", max_model_len=20000, gpu_memory_utilization=0.9)

We need to add our Hugging Face token to our [Cerebrium Secrets](https://docs.cerebrium.ai/cerebrium/environments/using-secrets) since using the Mistral model requires authentication. Please make sure the Huggingface token you added, has **WRITE** permissions. On first deploy, it will download the model and store it on disk therefore for subsequent calls it will load the model from disk.

Add the following to your main.py:

def run(prompt: str, temperature: float = 0.8, top_p: float = 0.75, top_k: int = 40, max_tokens: int = 256, frequency_penalty: int = 1):      sampling_params = SamplingParams(        temperature=temperature,        top_p=top_p,        top_k=top_k,        max_tokens=max_tokens,        frequency_penalty=frequency_penalty    )    outputs = llm.generate([item.prompt], sampling_params)    generated_text = []    for output in outputs:        generated_text.append(output.outputs[0].text)    return {"result": generated_text}

Every function in Cerebrium is callable through and API endpoint. Code at the top most layer (ie: not in a function) is instantiated only when the container is spun up the first time so for subsequent calls, it will simply run the code defined in the function you call.

Our final main.py should look like this:

from vllm import LLM, SamplingParamsfrom huggingface_hub import loginfrom cerebrium import get_secret# Your huggingface token (HF_AUTH_TOKEN) should be stored in your project secrets on your Cerebrium dashboardlogin(token=get_secret("HF_AUTH_TOKEN"))# Initialize the modelllm = LLM(model="mistralai/Mistral-7B-Instruct-v0.3", dtype="bfloat16", max_model_len=20000, gpu_memory_utilization=0.9)def run(prompt: str, temperature: float = 0.8, top_p: float = 0.75, top_k: int = 40, max_tokens: int = 256, frequency_penalty: int = 1):      sampling_params = SamplingParams(        temperature=temperature,        top_p=top_p,        top_k=top_k,        max_tokens=max_tokens,        frequency_penalty=frequency_penalty    )    outputs = llm.generate([item.prompt], sampling_params)    generated_text = []    for output in outputs:        generated_text.append(output.outputs[0].text)    return {"result": generated_text}

## Run on the cloud[​](#run-on-the-cloud "Direct link to Run on the cloud")

cerebrium deploy

You will see your application deploy, install pip packages and download the model. Once completed it will output a CURL request you can use to call your endpoint. Just remember to end the url with the function you would like to call - in this case /run.

curl --location --request POST 'https://api.cortex.cerebrium.ai/v4/p-<YOUR PROJECT ID>/mistral-vllm/run' \--header 'Authorization: Bearer <YOUR TOKEN HERE>' \--header 'Content-Type: application/json' \--data-raw '{    "prompt: "What is the capital city of France?"}'

You should then get a message looking like this:

{  "run_id": "nZL6mD8q66u4lHTXcqmPCc6pxxFwn95IfqQvEix0gHaOH4gkHUdz1w==",  "message": "Finished inference request with run_id: `nZL6mD8q66u4lHTXcqmPCc6pxxFwn95IfqQvEix0gHaOH4gkHUdz1w==`",  "result": {    "result": ["\nA: Paris"]  },  "status_code": 200,  "run_time_ms": 151.24988555908203}

[

Previous

Deploy with SkyPilot

](/deployment/self-deployment/skypilot/)[

Next

Deploy with Cloudflare Workers AI

](/deployment/self-deployment/cloudflare/)

*   [Setup Cerebrium](#setup-cerebrium)
*   [Setup Environment and Hardware](#setup-environment-and-hardware)
*   [Setup inference](#setup-inference)
*   [Run on the cloud](#run-on-the-cloud)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025 M