---
source: "website"
content_type: "services_products"
url: "https://docs.mistral.ai/capabilities/batch/"
title: "/capabilities/batch/"
domain: "docs.mistral.ai"
path: "/capabilities/batch/"
scraped_time: "2025-09-08T18:09:55.178143"
url_depth: 2
word_count: 1711
---

Batch Inference | Mistral AI

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
*   Batch Inference

On this page

# Batch Inference

## Prepare and upload your batch[​](#prepare-and-upload-your-batch "Direct link to Prepare and upload your batch")

A batch is composed of a list of API requests. The structure of an individual request includes:

*   A unique `custom_id` for identifying each request and referencing results after completion
*   A `body` object with message information

Here's an example of how to structure a batch request:

{"custom_id": "0", "body": {"max_tokens": 100, "messages": [{"role": "user", "content": "What is the best French cheese?"}]}}{"custom_id": "1", "body": {"max_tokens": 100, "messages": [{"role": "user", "content": "What is the best French wine?"}]}}

Save your batch into a .jsonl file. Once saved, you can upload your batch input file to ensure it is correctly referenced when initiating batch processes:

*   python
*   typescript
*   curl

from mistralai import Mistralimport osapi_key = os.environ["MISTRAL_API_KEY"]client = Mistral(api_key=api_key)batch_data = client.files.upload(    file={        "file_name": "test.jsonl",        "content": open("test.jsonl", "rb")    },    purpose = "batch")

import { Mistral } from '@mistralai/mistralai';import fs from 'fs';const apiKey = process.env.MISTRAL_API_KEY;const client = new Mistral({apiKey: apiKey});const batchFile = fs.readFileSync('batch_input_file.jsonl');const batchData = await client.files.upload({    file: {        fileName: "batch_input_file.jsonl",        content: batchFile,    },    purpose: "batch"});

curl https://api.mistral.ai/v1/files \  -H "Authorization: Bearer $MISTRAL_API_KEY" \  -F purpose="batch" \  -F file="@batch_input_file.jsonl"

## Create a new batch job[​](#create-a-new-batch-job "Direct link to Create a new batch job")

Create a new batch job, it will be queued for processing.

*   `input_files`: a list of the batch input file IDs.
*   `model`: you can only use one model (e.g., `codestral-latest`) per batch. However, you can run multiple batches on the same files with different models if you want to compare outputs.
*   `endpoint`: we currently support `/v1/embeddings`, `/v1/chat/completions`, `/v1/fim/completions`, `/v1/moderations`, `/v1/chat/moderations`.
*   `metadata`: optional custom metadata for the batch.

*   python
*   typescript
*   curl

created_job = client.batch.jobs.create(    input_files=[batch_data.id],    model="mistral-small-latest",    endpoint="/v1/chat/completions",    metadata={"job_type": "testing"})

import { Mistral } from '@mistralai/mistralai';const apiKey = process.env.MISTRAL_API_KEY;const client = new Mistral({apiKey: apiKey});const createdJob = await client.batch.jobs.create({    inputFiles: [batchData.id],    model: "mistral-small-latest",    endpoint: "/v1/chat/completions",    metadata: {jobType: "testing"}});

curl --location "https://api.mistral.ai/v1/batch/jobs" \--header "Authorization: Bearer $MISTRAL_API_KEY" \--header "Content-Type: application/json" \--header "Accept: application/json" \--data '{    "model": "mistral-small-latest",    "input_files": [        "<uuid>"    ],    "endpoint": "/v1/chat/completions",    "metadata": {        "job_type": "testing"    }}'

## Get a batch job details[​](#get-a-batch-job-details "Direct link to Get a batch job details")

*   python
*   typescript
*   curl

retrieved_job = client.batch.jobs.get(job_id=created_job.id)

const retrievedJob = await client.batch.jobs.get({ jobId: createdJob.id});

curl https://api.mistral.ai/v1/batch/jobs/<jobid> \--header "Authorization: Bearer $MISTRAL_API_KEY"

## Get batch job results[​](#get-batch-job-results "Direct link to Get batch job results")

*   python
*   typescript
*   curl

output_file_stream = client.files.download(file_id=retrieved_job.output_file)# Write and save the filewith open('batch_results.jsonl', 'wb') as f:    f.write(output_file_stream.read())

import fs from 'fs';const outputFileStream = await client.files.download({ fileId: retrievedJob.outputFile });// Write the stream to a fileconst writeStream = fs.createWriteStream('batch_results.jsonl');outputFileStream.pipeTo(new WritableStream({    write(chunk) {      writeStream.write(chunk);    },    close() {      writeStream.end();    }}));

curl 'https://api.mistral.ai/v1/files/<uuid>/content' \--header "Authorization: Bearer $MISTRAL_API_KEY" \

## List batch jobs[​](#list-batch-jobs "Direct link to List batch jobs")

You can view a list of your batch jobs and filter them by various criteria, including:

*   Status: `QUEUED`, `RUNNING`, `SUCCESS`, `FAILED`, `TIMEOUT_EXCEEDED`, `CANCELLATION_REQUESTED` and `CANCELLED`
*   Metadata: custom metadata key and value for the batch

*   python
*   typescript
*   curl

list_job = client.batch.jobs.list(    status="RUNNING",    metadata={"job_type": "testing"})

const listJob = await client.batch.jobs.list({    status: "RUNNING",    metadata: {        jobType: "testing"    }});

curl 'https://api.mistral.ai/v1/batch/jobs?status=RUNNING&job_type=testing'\--header 'x-api-key: $MISTRAL_API_KEY'

## Request the cancellation of a batch job[​](#request-the-cancellation-of-a-batch-job "Direct link to Request the cancellation of a batch job")

*   python
*   typescript
*   curl

canceled_job = client.batch.jobs.cancel(job_id=created_job.id)

const canceledJob = await mistral.batch.jobs.cancel({  jobId: createdJob.id,});

curl -X POST https://api.mistral.ai/v1/batch/jobs/<jobid>/cancel \--header "Authorization: Bearer $MISTRAL_API_KEY"

## An end-to-end example[​](#an-end-to-end-example "Direct link to An end-to-end example")

**Example**

import argparseimport jsonimport osimport randomimport timefrom io import BytesIOimport httpxfrom mistralai import File, Mistraldef create_client():    """    Create a Mistral client using the API key from environment variables.    Returns:        Mistral: An instance of the Mistral client.    """    return Mistral(api_key=os.environ["MISTRAL_API_KEY"])def generate_random_string(start, end):    """    Generate a random string of variable length.    Args:        start (int): Minimum length of the string.        end (int): Maximum length of the string.    Returns:        str: A randomly generated string.    """    length = random.randrange(start, end)    return ' '.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=length))def print_stats(batch_job):    """    Print the statistics of the batch job.    Args:        batch_job: The batch job object containing job statistics.    """    print(f"Total requests: {batch_job.total_requests}")    print(f"Failed requests: {batch_job.failed_requests}")    print(f"Successful requests: {batch_job.succeeded_requests}")    print(        f"Percent done: {round((batch_job.succeeded_requests + batch_job.failed_requests) / batch_job.total_requests, 4) * 100}")def create_input_file(client, num_samples):    """    Create an input file for the batch job.    Args:        client (Mistral): The Mistral client instance.        num_samples (int): Number of samples to generate.    Returns:        File: The uploaded input file object.    """    buffer = BytesIO()    for idx in range(num_samples):        request = {            "custom_id": str(idx),            "body": {                "max_tokens": random.randint(10, 1000),                "messages": [{"role": "user", "content": generate_random_string(100, 5000)}]            }        }        buffer.write(json.dumps(request).encode("utf-8"))        buffer.write("\n".encode("utf-8"))    return client.files.upload(file=File(file_name="file.jsonl", content=buffer.getvalue()), purpose="batch")def run_batch_job(client, input_file, model):    """    Run a batch job using the provided input file and model.    Args:        client (Mistral): The Mistral client instance.        input_file (File): The input file object.        model (str): The model to use for the batch job.    Returns:        BatchJob: The completed batch job object.    """    batch_job = client.batch.jobs.create(        input_files=[input_file.id],        model=model,        endpoint="/v1/chat/completions",        metadata={"job_type": "testing"}    )    while batch_job.status in ["QUEUED", "RUNNING"]:        batch_job = client.batch.jobs.get(job_id=batch_job.id)        print_stats(batch_job)        time.sleep(1)    print(f"Batch job {batch_job.id} completed with status: {batch_job.status}")    return batch_jobdef download_file(client, file_id, output_path):    """    Download a file from the Mistral server.    Args:        client (Mistral): The Mistral client instance.        file_id (str): The ID of the file to download.        output_path (str): The path where the file will be saved.    """    if file_id is not None:        print(f"Downloading file to {output_path}")        output_file = client.files.download(file_id=file_id)        with open(output_path, "w") as f:            for chunk in output_file.stream:                f.write(chunk.decode("utf-8"))        print(f"Downloaded file to {output_path}")def main(num_samples, success_path, error_path, model):    """    Main function to run the batch job.    Args:        num_samples (int): Number of samples to process.        success_path (str): Path to save successful outputs.        error_path (str): Path to save error outputs.        model (str): Model name to use.    """    client = create_client()    input_file = create_input_file(client, num_samples)    print(f"Created input file {input_file}")    batch_job = run_batch_job(client, input_file, model)    print(f"Job duration: {batch_job.completed_at - batch_job.created_at} seconds")    download_file(client, batch_job.error_file, error_path)    download_file(client, batch_job.output_file, success_path)if __name__ == "__main__":    parser = argparse.ArgumentParser(description="Run Mistral AI batch job")    parser.add_argument("--num_samples", type=int, default=100, help="Number of samples to process")    parser.add_argument("--success_path", type=str, default="output.jsonl", help="Path to save successful outputs")    parser.add_argument("--error_path", type=str, default="error.jsonl", help="Path to save error outputs")    parser.add_argument("--model", type=str, default="codestral-latest", help="Model name to use")    args = parser.parse_args()    main(args.num_samples, args.success_path, args.error_path, args.model)

## FAQ[​](#faq "Direct link to FAQ")

### Is the batch API available for all models?[​](#is-the-batch-api-available-for-all-models "Direct link to Is the batch API available for all models?")

Yes, batch API is available for all models including user fine-tuned models.

### Does the batch API affect pricing?[​](#does-the-batch-api-affect-pricing "Direct link to Does the batch API affect pricing?")

We offer a 50% discount on batch API. Learn more about our [pricing](https://mistral.ai/pricing#api-pricing).

### Does the batch API affect rate limits?[​](#does-the-batch-api-affect-rate-limits "Direct link to Does the batch API affect rate limits?")

No

### What's the max number of requests in a batch?[​](#whats-the-max-number-of-requests-in-a-batch "Direct link to What's the max number of requests in a batch?")

Currently, there is a maximum limit of 1 million pending requests per workspace. This means you cannot submit a job with more than 1 million requests. Additionally, you cannot submit two jobs with 600,000 requests each at the same time. You would need to wait until the first job has processed at least 200,000 requests, reducing its pending count to 400,000. At that point, the new job with 600,000 requests would fit within the limit.

### What's the max number of batch jobs one can create?[​](#whats-the-max-number-of-batch-jobs-one-can-create "Direct link to What's the max number of batch jobs one can create?")

Currently, there is no maximum limit.

### How long does the batch API take to process?[​](#how-long-does-the-batch-api-take-to-process "Direct link to How long does the batch API take to process?")

Processing speeds may be adjusted based on current demand and the volume of your request. Your batch results will only be accessible once the entire batch processing is complete.

Users can set `timeout_hours` when creating a job, which specifies the number of hours after which the job should expire. It defaults to 24 hours and should be lower than 7 days. A batch will expire if processing does not complete within the specified timeout.

### Can I view batch results from my workspace?[​](#can-i-view-batch-results-from-my-workspace "Direct link to Can I view batch results from my workspace?")

Yes, batches are specific to a workspace. You can see all batches and their results that were created within the workspace associated with your API key.

### Will batch results ever expire?[​](#will-batch-results-ever-expire "Direct link to Will batch results ever expire?")

No, the results do not expire at this time.

### Can batches exceed the spend limit?[​](#can-batches-exceed-the-spend-limit "Direct link to Can batches exceed the spend limit?")

Yes, due to high throughput and concurrent processing, batches may slightly exceed your workspace's configured spend limit.

[

Previous

Text & Vision Fine-tuning

](/capabilities/finetuning/text_vision_finetuning/)[

Next

Predicted outputs

](/capabilities/predicted-outputs/)

*   [Prepare and upload your batch](#prepare-and-upload-your-batch)
*   [Create a new batch job](#create-a-new-batch-job)
*   [Get a batch job details](#get-a-batch-job-details)
*   [Get batch job results](#get-batch-job-results)
*   [List batch jobs](#list-batch-jobs)
*   [Request the cancellation of a batch job](#request-the-cancellation-of-a-batch-job)
*   [An end-to-end example](#an-end-to-end-example)
*   [FAQ](#faq)
*   [Is the batch API available for all models?](#is-the-batch-api-available-for-all-models)
*   [Does the batch API affect pricing?](#does-the-batch-api-affect-pricing)
*   [Does the batch API affect rate limits?](#does-the-batch-api-affect-rate-limits)
*   [What's the max number of requests in a batch?](#whats-the-max-number-of-requests-in-a-batch)
*   [What's the max number of batch jobs one can create?](#whats-the-max-number-of-batch-jobs-one-can-create)
*   [How long does the batch API take to process?](#how-long-does-the-batch-api-take-to-process)
*   [Can I view batch results from my workspace?](#can-i-view-batch-results-from-my-workspace)
*   [Will batch results ever expire?](#will-batch-results-ever-expire)
*   [Can batches exceed the spend limit?](#can-batches-exceed-the-spend-limit)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistra