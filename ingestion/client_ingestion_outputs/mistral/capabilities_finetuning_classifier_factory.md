---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/capabilities/finetuning/classifier_factory/"
title: "/capabilities/finetuning/classifier_factory/"
domain: "docs.mistral.ai"
path: "/capabilities/finetuning/classifier_factory/"
scraped_time: "2025-09-08T18:09:58.841394"
url_depth: 3
word_count: 1780
---

Classifier Factory | Mistral AI

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
*   Classifier Factory

On this page

# Classifier Factory

In various domains and enterprises, classification models play a crucial role in enhancing efficiency, improving user experience, and ensuring compliance. These models serve diverse purposes, including but not limited to:

*   **Moderation**: Classification models are essential for moderating services and classifying unwanted content. For instance, our [moderation service](/capabilities/guardrailing/#moderation-api) helps in identifying and filtering inappropriate or harmful content in real-time, ensuring a safe and respectful environment for users.
*   **Intent Detection**: These models help in understanding user intent and behavior. By analyzing user interactions, they can predict the user's next actions or needs, enabling personalized recommendations and improved customer support.
*   **Sentiment Analysis**: Emotion and sentiment detection models analyze text data to determine the emotional tone behind words. This is particularly useful in social media monitoring, customer feedback analysis, and market research, where understanding public sentiment can drive strategic decisions.
*   **Data Clustering**: Classification models can group similar data points together, aiding in data organization and pattern recognition. This is beneficial in market segmentation, where businesses can identify distinct customer groups for targeted marketing campaigns.
*   **Fraud Detection**: In the financial sector, classification models help in identifying fraudulent transactions by analyzing patterns and anomalies in transaction data. This ensures the security and integrity of financial systems.
*   **Spam Filtering**: Email services use classification models to filter out spam emails, ensuring that users receive only relevant and safe communications.
*   **Recommendation Systems**: Classification models power recommendation engines by categorizing user preferences and suggesting relevant products, movies, or content based on past behavior and preferences.

By leveraging classification models, organizations can make data-driven decisions, improve operational efficiency, and deliver better products and services to their customers.

For this reason, we designed a friendly and easy way to make your own classifiers. Leveraging our small but highly efficient models and training methods, the Classifier Factory is both available directly in [la plateforme](https://console.mistral.ai/build/finetuned-models) and our API.

## Dataset Format[​](#dataset-format "Direct link to Dataset Format")

Data must be stored in JSON Lines (`.jsonl`) files, which allow storing multiple JSON objects, each on a new line.

We provide two endpoints:

*   `v1/classifications`: To classify raw text.
*   `v1/chat/classifications`: To classify chats and multi-turn interactions.

There are 2 main kinds of classification models:

*   Single Target
*   Multi-Target

### 1\. Single Target[​](#1-single-target "Direct link to 1. Single Target")

For single label classification, data must have the label name and the value for that corresponding label. Example:

*   v1/classifications
*   v1/chat/classifications

{    "text": "I love this product!",    "labels": {        "sentiment": "positive" // positive/neutral/negative    }}

For multiple labels, you can provide a list.

{    "text": "I love this product!",    "labels": {        "sentiment": ["positive","neutral"]    }}

{    "messages": [{"role": "user", "content": "I love this product!"}],    "labels": {        "sentiment": "positive" // positive/neutral/negative    }}

For multiple labels, you can provide a list.

{    "messages": [{"role": "user", "content": "I love this product!"}],    "labels": {        "sentiment": ["positive","neutral"]    }}

When using the result model, you will be able to retrieve the scores for the corresponding label and value.

Note that the files must be in JSONL format, meaning every JSON object must be flattened into a single line, and each JSON object is on a new line.

**Raw `.jsonl` file example.**

{"text": "I love this product!", "labels": {"sentiment": "positive"}}{"text": "The game was amazing.", "labels": {"sentiment": "positive"}}{"text": "The new policy is controversial.", "labels": {"sentiment": "neutral"}}{"text": "I don't like the new design.", "labels": {"sentiment": "negative"}}{"text": "The team won the championship.", "labels": {"sentiment": "positive"}}{"text": "The economy is in a bad shape.", "labels": {"sentiment": "negative"}}...

*   Label data must be a dictionary with the label name as the key and the label value as the value.

### 2\. Multi-Target[​](#2-multi-target "Direct link to 2. Multi-Target")

You can also have multiple targets and not only a single one. This is useful if you want to classify different aspects of the same content independently. Example:

*   v1/classifications
*   v1/chat/classifications

{    "text": "I love this product!",    "labels": {        "sentiment": "positive", // positive/neutral/negative        "is-english": "yes" // yes/no, boolean    }}

{    "messages": [{"role": "user", "content": "I love this product!"}],    "labels": {        "sentiment": "positive", // positive/neutral/negative        "is-english": "yes" // yes/no, boolean    }}

*   Each target is independent of each other, meaning the scores for each label will also be independent.

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

*   model: the specific model you would like to fine-tune. The choice is `ministral-3b-latest`.
*   training\_files: a collection of training file IDs, which can consist of a single file or multiple files.
*   validation\_files: a collection of validation file IDs, which can consist of a single file or multiple files.
*   hyperparameters: two adjustable hyperparameters, "training\_steps" and "learning\_rate", that users can modify.
*   auto\_start:
*   `auto_start=True`: Your job will be launched immediately after validation.
*   `auto_start=False` (default): You can manually start the training after validation by sending a POST request to `/fine_tuning/jobs/<uuid>/start`.
*   integrations: external integrations we support such as Weights and Biases for metrics tracking during training.

*   python
*   typescript
*   curl

# create a fine-tuning jobcreated_jobs = client.fine_tuning.jobs.create(    model="ministral-3b-latest",    job_type="classifier",    training_files=[{"file_id": training_data.id, "weight": 1}],    validation_files=[validation_data.id],    hyperparameters={        "training_steps": 10,        "learning_rate":0.0001    },    auto_start=False,#   integrations=[#       {#           "project": "finetuning",#           "api_key": "WANDB_KEY",#       }#   ])

After creating a fine-tuning job, you can check the job status using `client.fine_tuning.jobs.get(job_id = created_jobs.id)`.

const createdJob = await client.fineTuning.jobs.create({    model: 'ministral-3b-latest',    jobType: 'classifier',    trainingFiles: [{fileId: training_data.id, weight: 1}],    validationFiles: [validation_data.id],    hyperparameters: {      trainingSteps: 10,      learningRate: 0.0001,    },    autoStart:false,//  integrations:[//      {//          project: "finetuning",//          apiKey: "WANDB_KEY",//      }//  ],});

After creating a fine-tuning job, you can check the job status using `client.fineTuning.jobs.get({ jobId: createdJob.id })`.

curl https://api.mistral.ai/v1/fine_tuning/jobs \--header "Authorization: Bearer $MISTRAL_API_KEY" \--header 'Content-Type: application/json' \--header 'Accept: application/json' \--data '{  "model": "ministral-3b-latest",  "job_type": "classifier",  "training_files": [    "<uuid>"  ],  "validation_files": [    "<uuid>"  ],  "hyperparameters": {    "training_steps": 10,    "learning_rate": 0.0001  },  "auto_start": false}'

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

When a fine-tuned job is finished, you will be able to see the fine-tuned model name via `retrieved_jobs.fine_tuned_model`.

*   python
*   typescript
*   curl

classifier_response = client.classifiers.classify(    model=retrieved_job.fine_tuned_model,    inputs=["It's nice", "It's terrible", "Why not"],)

Use `classify_chat` to classify chats and multiturn interactions.

const classifierResponse = await client.classifiers.classify({    model: retrievedJob.fine_tuned_model,    inputs: ["It's nice", "It's terrible", "Why not"],})

Use `classifyChat` to classify chats and multiturn interactions.

curl "https://api.mistral.ai/v1/classifications" \     --header 'Content-Type: application/json' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY" \     --data '{    "model": "ft:classifier:ministral-3b-latest:XXX:20250401:XXX",    "input": ["It's nice", "It's terrible", "Why not"]  }'

## Delete a fine-tuned model[​](#delete-a-fine-tuned-model "Direct link to Delete a fine-tuned model")

*   python
*   typescript
*   curl

client.models.delete(model_id=retrieved_job.fine_tuned_model)

await client.models.delete({modelId:retrieved_job.fine_tuned_model})

curl --location --request DELETE 'https://api.mistral.ai/v1/models/ft:classifier:ministral-3b-latest:XXX:20250401:XXX' \     --header 'Accept: application/json' \     --header "Authorization: Bearer $MISTRAL_API_KEY"

## Cookbooks[​](#cookbooks "Direct link to Cookbooks")

Explore our guides and [cookbooks](https://github.com/mistralai/cookbook) leveraging the Classifier Factory:

*   [Intent Classification](https://colab.research.google.com/github/mistralai/cookbook/blob/main/mistral/classifier_factory/intent_classification.ipynb): Creating a single-target, single-label, intent classification model to predict user actions and improve customer interactions.
*   [Moderation Classifier](https://colab.research.google.com/github/mistralai/cookbook/blob/main/mistral/classifier_factory/moderation_classifier.ipynb): Build a single-target, multi-label, simple moderation model to label public comments.
*   [Product Classification](https://colab.research.google.com/github/mistralai/cookbook/blob/main/mistral/classifier_factory/product_classification.ipynb): Create a multi-target, single-label and multi-label, food classification model to categorize dishes and their country of origin and compare to classic LLM solutions, enhancing recipe recommendations and dietary planning.

## FAQ[​](#faq "Direct link to FAQ")

**Q: Which models can we fine-tune to create our own classifiers?** **A:** Currently, the classifier factory supports `ministral-3b`.

**Q: Where can I find the pricing?** **A:** You can find it on our [pricing page](https://mistral.ai/pricing#api-pricing) in the "fine-tunable models" section of our API Pricing.

[

Previous

Fine-tuning Overview

](/capabilities/finetuning/finetuning_overview/)[

Next

Text & Vision Fine-tuning

](/capabilities/finetuning/text_vision_finetuning/)

*   [Dataset Format](#dataset-format)
*   [1\. Single Target](#1-single-target)
*   [2\. Multi-Target](#2-multi-target)
*   [Upload a file](#upload-a-file)
*   [Create a fine-tuning job](#create-a-fine-tuning-job)
*   [List/retrieve/cancel jobs](#listretrievecancel-jobs)
*   [Use a fine-tuned model](#use-a-fine-tuned-model)
*   [Delete a fine-tuned model](#delete-a-fine-tuned-model)
*   [Cookbooks](#cookbooks)
*   [FAQ](#faq)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyrigh