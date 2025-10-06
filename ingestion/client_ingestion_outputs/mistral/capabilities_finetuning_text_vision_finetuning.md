---
source: "website"
content_type: "services_products"
url: "https://docs.mistral.ai/capabilities/finetuning/text_vision_finetuning/"
title: "/capabilities/finetuning/text_vision_finetuning/"
domain: "docs.mistral.ai"
path: "/capabilities/finetuning/text_vision_finetuning/"
scraped_time: "2025-09-08T18:09:53.839772"
url_depth: 3
word_count: 2686
---

Text & Vision Fine-tuning | Mistral AI

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
*   [Finetuning](/capabilities/finetuning/finetuning_overview/)
*   Text & Vision Fine-tuning

On this page

# Text & Vision Fine-tuning

Fine-tuning allows you to tailor a pre-trained language model to your specific needs by training it on your dataset. This guide explains how to fine-tune text and vision models, from preparing your data to training, whether you aim to improve domain-specific understanding or adapt to a unique conversational style.

tip

For detailed end-to-end fine-tuning examples and FAQ, check out our [fine-tuning guide](/guides/finetuning/).

You can both finetune directly in [la plateforme](https://console.mistral.ai/build/finetuned-models) or via our API.

## Dataset Format[​](#dataset-format "Direct link to Dataset Format")

Data must be stored in JSON Lines (`.jsonl`) files, which allow storing multiple JSON objects, each on a new line.

SFT Datasets should follow an instruction-following format representing a user-assistant conversation. Each JSON data sample should either consist of only user and assistant messages or include function-calling logic.

### 1\. Default Instruct[​](#1-default-instruct "Direct link to 1. Default Instruct")

Conversational data between user and assistant, which can be one-turn or multi-turn.

#### Text only template[​](#text-only-template "Direct link to Text only template")

{    "messages": [        {            "role": "user",            "content": "User interaction n°1"        },        {            "role": "assistant",            "content": "Bot interaction n°1"        },        {            "role": "user",            "content": "User interaction n°2"        },        {            "role": "assistant",            "content": "Bot interaction n°2"        }    ]}

Note that the files must be in JSONL format, meaning every JSON object must be flattened into a single line, and each JSON object is on a new line.

**Raw `.jsonl` file example.**

{"messages": [{"role": "user","content": "..."},{"role": "assistant","content": "..."},...]}{"messages": [{"role": "user","content": "..."},{"role": "assistant","content": "..."},...]}{"messages": [{"role": "user","content": "..."},{"role": "assistant","content": "..."},...]}{"messages": [{"role": "user","content": "..."},{"role": "assistant","content": "..."},...]}...

*   Conversational data must be stored under the `"messages"` key as a list.
*   Each list item is a dictionary containing the `"content"` and `"role"` keys. `"role"` is a string: `"system"`, `"user"`, `"assistant"` or `"tool"`.
*   Loss computation is performed only on tokens corresponding to assistant messages (`"role" == "assistant"`).

While text-only fine-tuning covers multiple use cases, you can also fine-tune the vision capabilities of our models. This allows you to create models that can understand and generate responses based on both text and image inputs.

#### Vision template[​](#vision-template "Direct link to Vision template")

{    "messages": [        {            "role": "user",            "content": [                {                    "type":"image_url",                    "image_url":"User Image URL, usually in a base64 format." // "data:image/jpeg;base64,{image_base64}"                },                {                    "type":"text",                    "text":"User interaction n°1"                }            ]        },        {            "role": "assistant",            "content": "Bot interaction n°1"        },        {            "role": "user",            "content": [                {                    "type":"image_url",                    "image_url":"User Image URL, usually in a base64 format." // "data:image/jpeg;base64,{image_base64}"                },                {                    "type":"text",                    "text":"User interaction n°2"                }            ]        },        {            "role": "assistant",            "content": "Bot interaction n°2"        }    ]}

*   Content can be a list of dictionaries, each containing a `"type"` key and either `"text"` or `"image_url"` keys.

### 2\. Function-calling Instruct[​](#2-function-calling-instruct "Direct link to 2. Function-calling Instruct")

Conversational data with tool usage. Example:

{    "messages": [        {            "role": "system",            "content": "You are a helpful assistant with access to the following functions to help the user. You can use the functions if needed."        },        {            "role": "user",            "content": "Can you help me generate an anagram of the word 'listen'?"        },        {            "role": "assistant",            "tool_calls": [                {                    "id": "TX92Jm8Zi",                    "type": "function",                    "function": {                        "name": "generate_anagram",                        "arguments": "{\"word\": \"listen\"}"                    }                }            ]        },        {            "role": "tool",            "content": "{\"anagram\": \"silent\"}",            "tool_call_id": "TX92Jm8Zi"        },        {            "role": "assistant",            "content": "The anagram of the word 'listen' is 'silent'."        },        {            "role": "user",            "content": "That's amazing! Can you generate an anagram for the word 'race'?"        },        {            "role": "assistant",            "tool_calls": [                {                    "id": "3XhQnxLsT",                    "type": "function",                    "function": {                        "name": "generate_anagram",                        "arguments": "{\"word\": \"race\"}"                    }                }            ]        }    ],    "tools": [        {            "type": "function",            "function": {                "name": "generate_anagram",                "description": "Generate an anagram of a given word",                "parameters": {                    "type": "object",                    "properties": {                        "word": {                            "type": "string",                            "description": "The word to generate an anagram of"                        }                    },                    "required": ["word"]                }            }        }    ]}

*   Conversational data must be stored under the `"messages"` key as a list.
*   Each message is a dictionary containing the `"role"` and `"content"` or `"tool_calls"` keys. `"role"` should be one of `"system"`, `"user"`, `"assistant"` or `"tool"`.
*   Only messages of type `"assistant"` can have a `"tool_calls"` key, representing the assistant performing a call to an available tool.
*   An assistant message with a `"tool_calls"` key cannot have a `"content"` key and must be followed by a `"tool"` message, which in turn must be followed by another assistant message.
*   The `"tool_call_id"` of tool messages must match the `"id"` of at least one of the previous assistant messages.
*   Both `"id"` and `"tool_call_id"` are randomly generated strings of exactly 9 characters. We recommend generating these automatically in a data preparation script as done [here](https://github.com/mistralai/mistral-finetune/blob/208b25c0f7299bb78d06cea25b82adee03834319/utils/reformat_data_glaive.py#L74).
*   The `"tools"` key must include definitions of all tools used in the conversation.
*   Loss computation is performed only on tokens corresponding to assistant messages (`"role" == "assistant"`).

## Upload a file[​](#upload-a-file "Direct link to Upload a file")

Once you have the data file with the right format, you can upload the data file to the Mistral Client, making them available for use in fine-tuning jobs.

*   python
*   typescript
*   curl

from mistralai import Mistralimport osapi_key = os.environ["MISTRAL_API_KEY"]client = Mistral(api_key=api_key)training_data = client.files.upload(    file={        "file_name": "training_file.jsonl",        "content": open("training_file.jsonl", "rb"),    })validation_data = client.files.upload(    file={        "file_name": "validation_file.jsonl",        "content": open("validation_file.jsonl", "rb"),    })

import { Mistral } from '@mistralai/mistralai';import fs from 'fs';const apiKey = process.env.MISTRAL_API_KEY;const client = new Mistral({apiKey: apiKey});const training_file = fs.readFileSync('training_file.jsonl');const training_data = await client.files.upload({    file: {        fileName: "training_file.jsonl",        content: training_file,    }});const validation_file = fs.readFileSync('validation_file.jsonl');const validation_data = await client.files.upload({    file: {        fileName: "validation_file.jsonl",        content: validation_file,    }});

curl https://api.mistral.ai/v1/files \  -H "Authorization: Bearer $MISTRAL_API_KEY" \  -F purpose="fine-tune" \  -F file="@training_file.jsonl"curl https://api.mistral.ai/v1/files \  -H "Authorization: Bearer $MISTRAL_API_KEY" \  -F purpose="fine-tune" \  -F file="@validation_file.jsonl"

## Create a fine-tuning job[​](#create-a-fine-tuning-job "Direct link to Create a fine-tuning job")

The next step is to create a fine-tuning job.

*   model: the specific model you would like to fine-tune. The choices are:
*   Text Only:
*   `open-mistral-7b`
*   `mistral-small-latest`
*   `codestral-latest`
*   `open-mistral-nemo`
*   `mistral-large-latest`
*   `ministral-8b-latest`
*   `ministral-3b-latest`
*   Vision:
*   `pixtral-12b-latest`
*   training\_files: a collection of training file IDs, which can consist of a single file or multiple files
*   validation\_files: a collection of validation file IDs, which can consist of a single file or multiple files
*   hyperparameters: two adjustable hyperparameters, "training\_steps" and "learning\_rate", that users can modify.
*   auto\_start:
*   `auto_start=True`: Your job will be launched immediately after validation.
*   `auto_start=False` (default): You can manually start the training after validation by sending a POST request to `/fine_tuning/jobs/<uuid>/start`.
*   integrations: external integrations we support such as Weights and Biases for metrics tracking during training.

*   python
*   typescript
*   curl

# create a fine-tuning jobcreated_jobs = client.fine_tuning.jobs.create(    model="open-mistral-7b",    training_files=[{"file_id": training_data.id, "weight": 1}],    validation_files=[validation_data.id],    hyperparameters={        "training_steps": 10,        "learning_rate":0.0001    },    auto_start=False,#   integrations=[#       {#           "project": "finetuning",#           "api_key": "WANDB_KEY",#       }#   ])

After creating a fine-tuning job, you can check the job status using `client.fine_tuning.jobs.get(job_id = created_jobs.id)`.

const createdJob = await client.fineTuning.jobs.create({    model: 'open-mistral-7b',    trainingFiles: [{fileId: training_data.id, weight: 1}],    validationFiles: [validation_data.id],    hyperparameters: {      trainingSteps: 10,      learningRate: 0.0001,    },    autoStart:false,//  integrations=[//      {//          project: "finetuning",//          apiKey: "WANDB_KEY",//      }//  ]});

After creating a fine-tuning job, you can check the job status using `client.fineTuning.jobs.get({ jobId: createdJob.id })`.

curl https://api.mistral.ai/v1/fine_tuning/jobs \--header "Authorization: Bearer $MISTRAL_API_KEY" \--header 'Content-Type: application/json' \--header 'Accept: application/json' \--data '{  "model": "open-mistral-7b",  "training_files": [    "<uuid>"  ],  "validation_files": [    "<uuid>"  ],  "hyperparameters": {    "training_steps": 10,    "learning_rate": 0.0001  },  "auto_start": false}'

After creating a fine-tuning job, you can check the job status using:

curl https://api.mistral.ai/v1/fine_tuning/jobs/<jobid> \--header "Authorization: Bearer $MISTRAL_API_KEY"

Initially, the job status will be `"QUEUED"`. After a brief period, the status will update to `"VALIDATED"`. At this point, you can proceed to start the fine-tuning job:

*   python
*   typescript
*   curl

# start a fine-tuning jobclient.fine_tuning.jobs.start(job_id = created_jobs.id)created_jobs

await client.fineTuning.jobs.start({jobId: createdJob.id})

curl -X POST https://api.mistral.ai/v1/fine_tuning/jobs/<jobid>/start \--header "Authorization: Bearer $MISTRAL_API_KEY"

## List/retrieve/cancel jobs[​](#listretrievecancel-jobs "Direct link to List/retrieve/cancel jobs")

You can also list jobs, retrieve a job, or cancel a job.

You can filter and view a list of jobs using various parameters such as `page`, `page_size`, `model`, `created_after`, `created_by_me`, `status`, `wandb_project`, `wandb_name`, and `suffix`. Check out our [API specs](https://docs.mistral.ai/api/#tag/fine-tuning) for details.

*   python
*   typescript
*   curl

# List jobsjobs = client.fine_tuning.jobs.list()print(jobs)# Retrieve a jobsretrieved_jobs = client.fine_tuning.jobs.get(job_id = created_jobs.id)print(retrieved_jobs)# Cancel a jobscanceled_jobs = client.fine_tuning.jobs.cancel(job_id = created_jobs.id)print(canceled_jobs)

// List jobsconst jobs = await client.fineTuning.jobs.list();// Retrieve a jobconst retrievedJob = await client.fineTuning.jobs.get({ jobId: createdJob.id })// Cancel a jobconst canceledJob = await client.fineTuning.jobs.cancel({  jobId: createdJob.id,});

# List jobscurl https://api.mistral.ai/v1/fine_tuning/jobs \--header "Authorization: Bearer $MISTRAL_API_KEY"# Retrieve a jobcurl https://api.mistral.ai/v1/fine_tuning/jobs/<jobid> \--header "Authorization: Bearer $MISTRAL_API_KEY"# Cancel a jobcurl -X POST https://api.mistral.ai/v1/fine_tuning/jobs/<jobid>/cancel \--header "Authorization: Bearer $MISTRAL_API_KEY"

## Use a fine-tuned model[​](#use-a-fine-tuned-model "Direct link to Use a fine-tuned model")

When a fine-tuned job is finished, you will be able to see the fine-tuned model name via `retrieved_jobs.fine_tuned_model`. Then you can use our `chat` endpoint to chat with the fine-tuned model:

*   python
*   typescript
*   curl

chat_response = client.chat.complete(    model=retrieved_job.fine_tuned_model,    messages = [{"role":'user', "content":'What is the best French cheese?'}])

const chatResponse = await client.chat.complete({  model: retrievedJob.fine_tuned_model,  messages: [{role: 'user', content: 'What is the best French cheese?'}],});

curl "https://api.mistral.ai/v1/chat/completions" \     --header 'Content-Type: application/json' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY" \     --data '{    "model": "ft:open-mistral-7b:daf5e488:20240430:c1bed559",    "messages": [{"role": "user", "content": "Who is the most renowned French painter?"}]  }'

## Delete a fine-tuned model[​](#delete-a-fine-tuned-model "Direct link to Delete a fine-tuned model")

*   python
*   typescript
*   curl

client.models.delete(model_id=retrieved_job.fine_tuned_model)

await client.models.delete({modelId:retrieved_job.fine_tuned_model})

curl --location --request DELETE 'https://api.mistral.ai/v1/models/ft:open-mistral-7b:XXX:20240531:XXX' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY"

## FAQ[​](#faq "Direct link to FAQ")

### How to validate data format?[​](#how-to-validate-data-format "Direct link to How to validate data format?")

*   Mistral API: We currently validate each file when you upload the dataset.

*   `mistral-finetune`: You can run the [data validation script](https://github.com/mistralai/mistral-finetune/blob/main/utils/validate_data.py) to validate the data and run the [reformat data script](https://github.com/mistralai/mistral-finetune/blob/main/utils/reformat_data.py) to reformat the data to the right format:

# download the reformat scriptwget https://raw.githubusercontent.com/mistralai/mistral-finetune/main/utils/reformat_data.py# download the validation scriptwget https://raw.githubusercontent.com/mistralai/mistral-finetune/main/utils/validate_data.py# reformat datapython reformat_data.py data.jsonl# validate datapython validate_data.py data.jsonl

However, it's important to note that these scripts might not detect all problematic cases. Therefore, you may need to manually validate and correct any unique edge cases in your data.

### What's the size limit of the training data?[​](#whats-the-size-limit-of-the-training-data "Direct link to What's the size limit of the training data?")

While the size limit for an individual training data file is 512MB, there's no limitation on the number of files you can upload. You can upload multiple files and reference them when creating the job.

### What's the size limit of the validation data?[​](#whats-the-size-limit-of-the-validation-data "Direct link to What's the size limit of the validation data?")

The size limit for the validation data is 1MB. As a rule of thumb:

`validation_set_max_size = min(1MB, 5% of training data)`

### What happens if I try to create a job that already exists?[​](#what-happens-if-i-try-to-create-a-job-that-already-exists "Direct link to What happens if I try to create a job that already exists?")

At job creation, you will receive a `409 Conflict` error in case a similar job is already running / validated / queued. This mechanism helps avoid inadvertently creating duplicate jobs, saving resources and preventing redundancy.

### What if I upload an already existing file?[​](#what-if-i-upload-an-already-existing-file "Direct link to What if I upload an already existing file?")

If a file is uploaded and matches an existing file in both content and name, the pre-existing file is returned instead of creating a new one.

### How many epochs are in the training process?[​](#how-many-epochs-are-in-the-training-process "Direct link to How many epochs are in the training process?")

A general rule of thumb is: Num epochs = max\_steps / file\_of\_training\_jsonls\_in\_MB. For instance, if your training file is 100MB and you set max\_steps=1000, the training process will roughly perform 10 epochs.

### Where can I find information on cost/ ETA / number of tokens / number of passes over each files?[​](#where-can-i-find-information-on-cost-eta--number-of-tokens--number-of-passes-over-each-files "Direct link to Where can I find information on cost/ ETA / number of tokens / number of passes over each files?")

Mistral API: When you create a fine-tuning job, you should automatically see these info with the default `auto_start=False` argument.

Note that the `dry_run=True` argument will be removed in September.

`mistral-finetune`: You can use the following script to find out: [https://github.com/mistralai/mistral-finetune/blob/main/utils/validate\_data.py](https://github.com/mistralai/mistral-finetune/blob/main/utils/validate_data.py). This script accepts a .yaml training file as input and returns the number of tokens the model is being trained on.

### How to estimate cost of a fine-tuning job?[​](#how-to-estimate-cost-of-a-fine-tuning-job "Direct link to How to estimate cost of a fine-tuning job?")

For Mistral API, you can use the `auto_start=False` argument as mentioned in the previous question.

### What is the recommended learning rate?[​](#what-is-the-recommended-learning-rate "Direct link to What is the recommended learning rate?")

For LoRA fine-tuning, we recommend 1e-4 (default) or 1e-5.

Note that the learning rate we define is the peak learning rate, instead of a flat learning rate. The learning rate follows a linear warmup and cosine decay schedule. During the warmup phase, the learning rate is linearly increased from a small initial value to a larger value over a certain number of training steps. After the warmup phase, the learning rate is decayed using a cosine function.

### Is the fine-tuning API compatible with OpenAI data format?[​](#is-the-fine-tuning-api-compatible-with-openai-data-format "Direct link to Is the fine-tuning API compatible with OpenAI data format?")

Yes, we support OpenAI format.

### What if my file size is larger than 500MB and I get the error message `413 Request Entity Too Large`?[​](#what-if-my-file-size-is-larger-than-500mb-and-i-get-the-error-message-413-request-entity-too-large "Direct link to what-if-my-file-size-is-larger-than-500mb-and-i-get-the-error-message-413-request-entity-too-large")

You can split your data file into chunks. Here is an example:

Details

import jsonfrom datasets import load_dataset# get data from hugging faceds = load_dataset("HuggingFaceH4/ultrachat_200k",split="train_gen")# save data into .jsonl. This file is about 1.3GBwith open('train.jsonl', 'w') as f:    for line in ds:        json.dump(line, f)        f.write('\n')# reformat data !wget https://raw.githubusercontent.com/mistralai/mistral-finetune/main/utils/reformat_data.py!python reformat_data.py train.jsonl# Split file into three chunks input_file = "train.jsonl"output_files = ["train_1.jsonl", "train_2.jsonl", "train_3.jsonl"]# open the output filesoutput_file_objects = [open(file, "w") for file in output_files]# counter for output filescounter = 0with open(input_file, "r") as f_in:    # read the input file line by line    for line in f_in:        # parse the line as JSON        data = json.loads(line)        # write the data to the current output file        output_file_objects[counter].write(json.dumps(data) + "\n")        # increment the counter        counter = (counter + 1) % 3# close the output filesfor file in output_file_objects:    file.close()# now you should see three jsonl files under 500MB

[

Previous

Classifier Factory

](/capabilities/finetuning/classifier_factory/)[

Next

Batch Inference

](/capabilities/batch/)

*   [Dataset Format](#dataset-format)
*   [1\. Default Instruct](#1-default-instruct)
*   [2\. Function-calling Instruct](#2-function-calling-instruct)
*   [Upload a file](#upload-a-file)
*   [Create a fine-tuning job](#create-a-fine-tuning-job)
*   [List/retrieve/cancel jobs](#listretrievecancel-jobs)
*   [Use a fine-tuned model](#use-a-fine-tuned-model)
*   [Delete a fine-tuned model](#delete-a-fine-tuned-model)
*   [FAQ](#faq)
*   [How to validate data format?](#how-to-validate-data-format)
*   [What's the size limit of the training data?](#whats-the-size-limit-of-the-training-data)
*   [What's the size limit of the validation data?](#whats-the-size-limit-of-the-validation-data)
*   [What happens if I try to create a job that already exists?](#what-happens-if-i-try-to-create-a-job-that-already-exists)
*   [What if I upload an already existing file?](#what-if-i-upload-an-already-existing-file)
*   [How many epochs are in the training process?](#how-many-epochs-are-in-the-training-process)
*   [Where can I find information on cost/ ETA / number of tokens / number of passes over each files?](#where-can-i-find-information-on-cost-eta--number-of-tokens--number-of-passes-over-each-files)
*   [How to estimate cost of a fine-tuning job?](#how-to-estimate-cost-of-a-fine-tuning-job)
*   [What is the recommended learning rate?](#what-is-the-recommended-learning-rate)
*   [Is the fine-tuning API compatible with OpenAI data format?](#is-the-fine-tuning-api-compatible-with-openai-data-format)
*   [What if my file size is larger than 500MB and I get the error message `413 Request Entity Too Large`?](#what-if-my-file-size-is-larger-than-500mb-and-i-get-the-error-message-413-request-entity-too-large)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https:/