---
source: "website"
content_type: "other"
url: "https://docs.mistral.ai/api/"
title: "/api/"
domain: "docs.mistral.ai"
path: "/api/"
scraped_time: "2025-09-08T18:10:03.136691"
url_depth: 1
word_count: 12973
---

Mistral AI API | Mistral AI

[Skip to main content](#__docusaurus_skipToContent_fallback)

[

![Mistral AI Logo](/img/logo.svg)![Mistral AI Logo](/img/logo-dark.svg)

](https://mistral.ai/)[Le Chat](https://chat.mistral.ai/)[La Plateforme](https://console.mistral.ai/)[Docs](/)[Cookbooks (beta)](/cookbooks/)[API](/api/)

[GitHub](https://github.com/mistralai/)[Discord](https://discord.gg/mistralai)

*   Chat
*   postChat Completion
*   FIM
*   postFim Completion
*   Agents
*   postAgents Completion
*   Embeddings
*   postEmbeddings
*   Classifiers
*   postModerations
*   postChat Moderations
*   postClassifications
*   postChat Classifications
*   Files
*   postUpload File
*   getList Files
*   getRetrieve File
*   delDelete File
*   getDownload File
*   getGet Signed Url
*   Fine Tuning
*   getGet Fine Tuning Jobs
*   postCreate Fine Tuning Job
*   getGet Fine Tuning Job
*   postCancel Fine Tuning Job
*   postStart Fine Tuning Job
*   Models
*   getList Models
*   getRetrieve Model
*   delDelete Model
*   patchUpdate Fine Tuned Model
*   postArchive Fine Tuned Model
*   delUnarchive Fine Tuned Model
*   Batch
*   getGet Batch Jobs
*   postCreate Batch Job
*   getGet Batch Job
*   postCancel Batch Job
*   OCR API
*   postOCR
*   Transcriptions API
*   postCreate Transcription
*   postCreate streaming transcription (SSE)
*   (beta) Agents API
*   postCreate a agent that can be used within a conversation.
*   getList agent entities.
*   getRetrieve an agent entity.
*   patchUpdate an agent entity.
*   patchUpdate an agent version.
*   (beta) Conversations API
*   postCreate a conversation and append entries to it.
*   getList all created conversations.
*   getRetrieve a conversation information.
*   postAppend new entries to an existing conversation.
*   getRetrieve all entries in a conversation.
*   getRetrieve all messages in a conversation.
*   postRestart a conversation starting from a given entry.
*   postCreate a conversation and append entries to it.
*   postAppend new entries to an existing conversation.
*   postRestart a conversation starting from a given entry.
*   (beta) Libraries API - Main
*   getList all libraries you have access to.
*   postCreate a new Library.
*   getDetailed information about a specific Library.
*   delDelete a library and all of it's document.
*   putUpdate a library.
*   (beta) Libraries API - Documents
*   getList document in a given library.
*   postUpload a new document.
*   getRetrieve the metadata of a specific document.
*   putUpdate the metadata of a specific document.
*   delDelete a document.
*   getRetrieve the text content of a specific document.
*   getRetrieve the processing status of a specific document.
*   getRetrieve the signed URL of a specific document.
*   getRetrieve the signed URL of text extracted from a given document.
*   postReprocess a document.
*   (beta) Libraries API - Access
*   getList all of the access to this library.
*   putCreate or update an access level.
*   delDelete an access level.

# Mistral AI API (1.0.0)

Download OpenAPI specification:[Download](https://docs.mistral.ai/redocusaurus/plugin-redoc-0.yaml)

Our Chat Completion and Embeddings APIs specification. Create your account on [La Plateforme](https://console.mistral.ai) to get access and read the [docs](https://docs.mistral.ai) to learn how to use it.

## [](#tag/chat)Chat

Chat Completion API.

## [](#tag/chat/operation/chat_completion_v1_chat_completions_post)Chat Completion

##### Authorizations:

_ApiKey_

##### Request Body schema: application/json

required

model

required

string (Model)

ID of the model to use. You can use the [List Available Models](/api/#tag/models/operation/list_models_v1_models_get) API to see all of your available models, or see our [Model overview](/models) for model descriptions.

temperature

Temperature (number) or Temperature (null) (Temperature)

What sampling temperature to use, we recommend between 0.0 and 0.7. Higher values like 0.7 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both. The default value varies depending on the model you are targeting. Call the `/models` endpoint to retrieve the appropriate value.

top\_p

number (Top P) \[ 0 .. 1 \]

Default: 1

Nucleus sampling, where the model considers the results of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.

max\_tokens

Max Tokens (integer) or Max Tokens (null) (Max Tokens)

The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.

stream

boolean (Stream)

Default: false

Whether to stream back partial progress. If set, tokens will be sent as data-only server-side events as they become available, with the stream terminated by a data: \[DONE\] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

stop

Stop (string) or Array of Stop (strings) (Stop)

Stop generation if this token is detected. Or if one of these tokens is detected when providing an array

random\_seed

Random Seed (integer) or Random Seed (null) (Random Seed)

The seed to use for random sampling. If set, different calls will generate deterministic results.

messages

required

Array of any (Messages)

The prompt(s) to generate completions for, encoded as a list of dict with role and content.

response\_format

object (ResponseFormat)

tools

Array of Tools (objects) or Tools (null) (Tools)

tool\_choice

ToolChoice (object) or ToolChoiceEnum (string) (Tool Choice)

Default: "auto"

presence\_penalty

number (Presence Penalty) \[ -2 .. 2 \]

Default: 0

presence\_penalty determines how much the model penalizes the repetition of words or phrases. A higher presence penalty encourages the model to use a wider variety of words and phrases, making the output more diverse and creative.

frequency\_penalty

number (Frequency Penalty) \[ -2 .. 2 \]

Default: 0

frequency\_penalty penalizes the repetition of words based on their frequency in the generated text. A higher frequency penalty discourages the model from repeating words that have already appeared frequently in the output, promoting diversity and reducing repetition.

n

N (integer) or N (null) (N)

Number of completions to return for each request, input tokens are only billed once.

prediction

object (Prediction)

Default: {"type":"content","content":""}

Enable users to specify expected results, optimizing response times by leveraging known or predictable content. This approach is especially effective for updating text documents or code files with minimal changes, reducing latency while maintaining high-quality results.

parallel\_tool\_calls

boolean (Parallel Tool Calls)

Default: true

prompt\_mode

MistralPromptMode (string) or null

Allows toggling between the reasoning mode and no system prompt. When set to `reasoning` the system prompt for reasoning models will be used.

safe\_prompt

boolean

Default: false

Whether to inject a safety prompt before all conversations.

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/chat/completions

Production server

https://api.mistral.ai/v1/chat/completions

### Request samples

*   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  *   "model": "mistral-small-latest",      *   "temperature": 1.5,      *   "top_p": 1,      *   "max_tokens": 0,      *   "stream": false,      *   "stop": "string",      *   "random_seed": 0,      *   "messages": [          *   {                  *   "role": "user",                      *   "content": "Who is the best French painter? Answer in one short sentence."                               }                   ],      *   "response_format": {          *   "type": "text",              *   "json_schema": {                  *   "name": "string",                      *   "description": "string",                      *   "schema": { },                      *   "strict": false                               }                   },      *   "tools": [          *   {                  *   "type": "function",                      *   "function": {                          *   "name": "string",                              *   "description": "",                              *   "strict": false,                              *   "parameters": { }                                           }                               }                   ],      *   "tool_choice": "auto",      *   "presence_penalty": 0,      *   "frequency_penalty": 0,      *   "n": 1,      *   "prediction": {          *   "type": "content",              *   "content": ""                   },      *   "parallel_tool_calls": true,      *   "prompt_mode": "reasoning",      *   "safe_prompt": false       }`

### Response samples

*   200
*   422

Content type

application/jsontext/event-streamapplication/json

Copy

Expand all Collapse all

`{  *   "id": "cmpl-e5cc70bb28c444948073e77776eb30ef",      *   "object": "chat.completion",      *   "model": "mistral-small-latest",      *   "usage": {          *   "prompt_tokens": 0,              *   "completion_tokens": 0,              *   "total_tokens": 0,              *   "prompt_audio_seconds": 0                   },      *   "created": 1702256327,      *   "choices": [          *   {                  *   "index": 0,                      *   "message": {                          *   "content": "string",                              *   "tool_calls": [                                  *   {                                          *   "id": "null",                                              *   "type": "function",                                              *   "function": {                                                  *   "name": "string",                                                      *   "arguments": { }                                                                               },                                              *   "index": 0                                                                   }                                                       ],                              *   "prefix": false,                              *   "role": "assistant"                                           },                      *   "finish_reason": "stop"                               }                   ]       }`

## [](#tag/fim)FIM

Fill-in-the-middle API.

## [](#tag/fim/operation/fim_completion_v1_fim_completions_post)Fim Completion

FIM completion.

##### Authorizations:

_ApiKey_

##### Request Body schema: application/json

required

model

required

string (Model)

Default: "codestral-2405"

ID of the model to use. Only compatible for now with:

*   `codestral-2405`
*   `codestral-latest`

temperature

Temperature (number) or Temperature (null) (Temperature)

What sampling temperature to use, we recommend between 0.0 and 0.7. Higher values like 0.7 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or `top_p` but not both. The default value varies depending on the model you are targeting. Call the `/models` endpoint to retrieve the appropriate value.

top\_p

number (Top P) \[ 0 .. 1 \]

Default: 1

Nucleus sampling, where the model considers the results of the tokens with `top_p` probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or `temperature` but not both.

max\_tokens

Max Tokens (integer) or Max Tokens (null) (Max Tokens)

The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.

stream

boolean (Stream)

Default: false

Whether to stream back partial progress. If set, tokens will be sent as data-only server-side events as they become available, with the stream terminated by a data: \[DONE\] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

stop

Stop (string) or Array of Stop (strings) (Stop)

Stop generation if this token is detected. Or if one of these tokens is detected when providing an array

random\_seed

Random Seed (integer) or Random Seed (null) (Random Seed)

The seed to use for random sampling. If set, different calls will generate deterministic results.

prompt

required

string (Prompt)

The text/code to complete.

suffix

Suffix (string) or Suffix (null) (Suffix)

Default: ""

Optional text/code that adds more context for the model. When given a `prompt` and a `suffix` the model will fill what is between them. When `suffix` is not provided, the model will simply execute completion starting with `prompt`.

min\_tokens

Min Tokens (integer) or Min Tokens (null) (Min Tokens)

The minimum number of tokens to generate in the completion.

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/fim/completions

Production server

https://api.mistral.ai/v1/fim/completions

### Request samples

*   Payload

Content type

application/json

Copy

`{  *   "model": "codestral-2405",      *   "temperature": 1.5,      *   "top_p": 1,      *   "max_tokens": 0,      *   "stream": false,      *   "stop": "string",      *   "random_seed": 0,      *   "prompt": "def",      *   "suffix": "return a+b",      *   "min_tokens": 0       }`

### Response samples

*   200
*   422

Content type

application/jsontext/event-streamapplication/json

Copy

Expand all Collapse all

`{  *   "id": "cmpl-e5cc70bb28c444948073e77776eb30ef",      *   "object": "chat.completion",      *   "model": "codestral-latest",      *   "usage": {          *   "prompt_tokens": 0,              *   "completion_tokens": 0,              *   "total_tokens": 0,              *   "prompt_audio_seconds": 0                   },      *   "created": 1702256327,      *   "choices": [          *   {                  *   "index": 0,                      *   "message": {                          *   "content": "string",                              *   "tool_calls": [                                  *   {                                          *   "id": "null",                                              *   "type": "function",                                              *   "function": {                                                  *   "name": "string",                                                      *   "arguments": { }                                                                               },                                              *   "index": 0                                                                   }                                                       ],                              *   "prefix": false,                              *   "role": "assistant"                                           },                      *   "finish_reason": "stop"                               }                   ]       }`

## [](#tag/agents)Agents

Agents API.

## [](#tag/agents/operation/agents_completion_v1_agents_completions_post)Agents Completion

##### Authorizations:

_ApiKey_

##### Request Body schema: application/json

required

max\_tokens

Max Tokens (integer) or Max Tokens (null) (Max Tokens)

The maximum number of tokens to generate in the completion. The token count of your prompt plus `max_tokens` cannot exceed the model's context length.

stream

boolean (Stream)

Default: false

Whether to stream back partial progress. If set, tokens will be sent as data-only server-side events as they become available, with the stream terminated by a data: \[DONE\] message. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

stop

Stop (string) or Array of Stop (strings) (Stop)

Stop generation if this token is detected. Or if one of these tokens is detected when providing an array

random\_seed

Random Seed (integer) or Random Seed (null) (Random Seed)

The seed to use for random sampling. If set, different calls will generate deterministic results.

messages

required

Array of any (Messages)

The prompt(s) to generate completions for, encoded as a list of dict with role and content.

response\_format

object (ResponseFormat)

tools

Array of Tools (objects) or Tools (null) (Tools)

tool\_choice

ToolChoice (object) or ToolChoiceEnum (string) (Tool Choice)

Default: "auto"

presence\_penalty

number (Presence Penalty) \[ -2 .. 2 \]

Default: 0

presence\_penalty determines how much the model penalizes the repetition of words or phrases. A higher presence penalty encourages the model to use a wider variety of words and phrases, making the output more diverse and creative.

frequency\_penalty

number (Frequency Penalty) \[ -2 .. 2 \]

Default: 0

frequency\_penalty penalizes the repetition of words based on their frequency in the generated text. A higher frequency penalty discourages the model from repeating words that have already appeared frequently in the output, promoting diversity and reducing repetition.

n

N (integer) or N (null) (N)

Number of completions to return for each request, input tokens are only billed once.

prediction

object (Prediction)

Default: {"type":"content","content":""}

Enable users to specify expected results, optimizing response times by leveraging known or predictable content. This approach is especially effective for updating text documents or code files with minimal changes, reducing latency while maintaining high-quality results.

parallel\_tool\_calls

boolean (Parallel Tool Calls)

Default: true

prompt\_mode

MistralPromptMode (string) or null

Allows toggling between the reasoning mode and no system prompt. When set to `reasoning` the system prompt for reasoning models will be used.

agent\_id

required

string

The ID of the agent to use for this completion.

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/agents/completions

Production server

https://api.mistral.ai/v1/agents/completions

### Request samples

*   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  *   "max_tokens": 0,      *   "stream": false,      *   "stop": "string",      *   "random_seed": 0,      *   "messages": [          *   {                  *   "role": "user",                      *   "content": "Who is the best French painter? Answer in one short sentence."                               }                   ],      *   "response_format": {          *   "type": "text",              *   "json_schema": {                  *   "name": "string",                      *   "description": "string",                      *   "schema": { },                      *   "strict": false                               }                   },      *   "tools": [          *   {                  *   "type": "function",                      *   "function": {                          *   "name": "string",                              *   "description": "",                              *   "strict": false,                              *   "parameters": { }                                           }                               }                   ],      *   "tool_choice": "auto",      *   "presence_penalty": 0,      *   "frequency_penalty": 0,      *   "n": 1,      *   "prediction": {          *   "type": "content",              *   "content": ""                   },      *   "parallel_tool_calls": true,      *   "prompt_mode": "reasoning",      *   "agent_id": "string"       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "id": "cmpl-e5cc70bb28c444948073e77776eb30ef",      *   "object": "chat.completion",      *   "model": "mistral-small-latest",      *   "usage": {          *   "prompt_tokens": 0,              *   "completion_tokens": 0,              *   "total_tokens": 0,              *   "prompt_audio_seconds": 0                   },      *   "created": 1702256327,      *   "choices": [          *   {                  *   "index": 0,                      *   "message": {                          *   "content": "string",                              *   "tool_calls": [                                  *   {                                          *   "id": "null",                                              *   "type": "function",                                              *   "function": {                                                  *   "name": "string",                                                      *   "arguments": { }                                                                               },                                              *   "index": 0                                                                   }                                                       ],                              *   "prefix": false,                              *   "role": "assistant"                                           },                      *   "finish_reason": "stop"                               }                   ]       }`

## [](#tag/embeddings)Embeddings

Embeddings API.

## [](#tag/embeddings/operation/embeddings_v1_embeddings_post)Embeddings

Embeddings

##### Authorizations:

_ApiKey_

##### Request Body schema: application/json

required

model

required

string (Model)

ID of the model to use.

input

required

Input (string) or Array of Input (strings) (Input)

Text to embed.

output\_dimension

Output Dimension (integer) or Output Dimension (null) (Output Dimension)

The dimension of the output embeddings.

output\_dtype

string (EmbeddingDtype)

Default: "float"

Enum: "float" "int8" "uint8" "binary" "ubinary"

The data type of the output embeddings.

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/embeddings

Production server

https://api.mistral.ai/v1/embeddings

### Request samples

*   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  *   "model": "mistral-embed",      *   "input": [          *   "Embed this sentence.",              *   "As well as this one."                   ],      *   "output_dimension": 0,      *   "output_dtype": "float"       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "id": "cmpl-e5cc70bb28c444948073e77776eb30ef",      *   "object": "chat.completion",      *   "model": "mistral-small-latest",      *   "usage": {          *   "prompt_tokens": 0,              *   "completion_tokens": 0,              *   "total_tokens": 0,              *   "prompt_audio_seconds": 0                   },      *   "data": [          *   {                  *   "object": "embedding",                      *   "embedding": [                          *   0.1,                              *   0.2,                              *   0.3                                           ],                      *   "index": 0                               }                   ]       }`

## [](#tag/classifiers)Classifiers

Classifiers API.

## [](#tag/classifiers/operation/moderations_v1_moderations_post)Moderations

##### Authorizations:

_ApiKey_

##### Request Body schema: application/json

required

model

required

string (Model)

ID of the model to use.

input

required

Input (string) or Array of Input (strings) (Input)

Text to classify.

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/moderations

Production server

https://api.mistral.ai/v1/moderations

### Request samples

*   Payload

Content type

application/json

Copy

`{  *   "model": "string",      *   "input": "string"       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "id": "mod-e5cc70bb28c444948073e77776eb30ef",      *   "model": "string",      *   "results": [          *   {                  *   "categories": {                          *   "property1": true,                              *   "property2": true                                           },                      *   "category_scores": {                          *   "property1": 0,                              *   "property2": 0                                           }                               }                   ]       }`

## [](#tag/classifiers/operation/chat_moderations_v1_chat_moderations_post)Chat Moderations

##### Authorizations:

_ApiKey_

##### Request Body schema: application/json

required

input

required

Array of Input (any) or Array of Input (any) (Input)

Chat to classify

model

required

string (Model)

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/chat/moderations

Production server

https://api.mistral.ai/v1/chat/moderations

### Request samples

*   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  *   "input": [          *   {                  *   "content": "string",                      *   "role": "system"                               }                   ],      *   "model": "string"       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "id": "mod-e5cc70bb28c444948073e77776eb30ef",      *   "model": "string",      *   "results": [          *   {                  *   "categories": {                          *   "property1": true,                              *   "property2": true                                           },                      *   "category_scores": {                          *   "property1": 0,                              *   "property2": 0                                           }                               }                   ]       }`

## [](#tag/classifiers/operation/classifications_v1_classifications_post)Classifications

##### Authorizations:

_ApiKey_

##### Request Body schema: application/json

required

model

required

string (Model)

ID of the model to use.

input

required

Input (string) or Array of Input (strings) (Input)

Text to classify.

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/classifications

Production server

https://api.mistral.ai/v1/classifications

### Request samples

*   Payload

Content type

application/json

Copy

`{  *   "model": "string",      *   "input": "string"       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "id": "mod-e5cc70bb28c444948073e77776eb30ef",      *   "model": "string",      *   "results": [          *   {                  *   "property1": {                          *   "scores": {                                  *   "property1": 0,                                      *   "property2": 0                                                       }                                           },                      *   "property2": {                          *   "scores": {                                  *   "property1": 0,                                      *   "property2": 0                                                       }                                           }                               }                   ]       }`

## [](#tag/classifiers/operation/chat_classifications_v1_chat_classifications_post)Chat Classifications

##### Authorizations:

_ApiKey_

##### Request Body schema: application/json

required

model

required

string (Model)

input

required

InstructRequest (object) or Array of ChatClassificationRequestInputs (objects) (ChatClassificationRequestInputs)

Chat to classify

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/chat/classifications

Production server

https://api.mistral.ai/v1/chat/classifications

### Request samples

*   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  *   "model": "string",      *   "input": {          *   "messages": [                  *   {                          *   "content": "string",                              *   "role": "system"                                           }                               ]                   }       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "id": "mod-e5cc70bb28c444948073e77776eb30ef",      *   "model": "string",      *   "results": [          *   {                  *   "property1": {                          *   "scores": {                                  *   "property1": 0,                                      *   "property2": 0                                                       }                                           },                      *   "property2": {                          *   "scores": {                                  *   "property1": 0,                                      *   "property2": 0                                                       }                                           }                               }                   ]       }`

## [](#tag/files)Files

Files API

## [](#tag/files/operation/files_api_routes_upload_file)Upload File

Upload a file that can be used across various endpoints.

The size of individual files can be a maximum of 512 MB. The Fine-tuning API only supports .jsonl files.

Please contact us if you need to increase these storage limits.

##### Authorizations:

_ApiKey_

##### Request Body schema: multipart/form-data

required

purpose

string (FilePurpose)

Enum: "fine-tune" "batch" "ocr"

file

required

string <binary\> (File)

The File object (not file name) to be uploaded. To upload a file and specify a custom file name you should format your request as such:

file=@path/to/your/file.jsonl;filename=custom_name.jsonl

Otherwise, you can just keep the original file name:

file=@path/to/your/file.jsonl

### Responses

**200**

OK

post/v1/files

Production server

https://api.mistral.ai/v1/files

### Response samples

*   200

Content type

application/json

Copy

`{  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f09",      *   "object": "file",      *   "bytes": 13000,      *   "created_at": 1716963433,      *   "filename": "files_upload.jsonl",      *   "purpose": "fine-tune",      *   "sample_type": "pretrain",      *   "num_lines": 0,      *   "mimetype": "string",      *   "source": "upload",      *   "signature": "string"       }`

## [](#tag/files/operation/files_api_routes_list_files)List Files

Returns a list of files that belong to the user's organization.

##### Authorizations:

_ApiKey_

##### query Parameters

page

integer (Page)

Default: 0

page\_size

integer (Page Size)

Default: 100

sample\_type

Array of Sample Type (strings) or Sample Type (null) (Sample Type)

source

Array of Source (strings) or Source (null) (Source)

search

Search (string) or Search (null) (Search)

purpose

FilePurpose (string) or null

### Responses

**200**

OK

get/v1/files

Production server

https://api.mistral.ai/v1/files

### Response samples

*   200

Content type

application/json

Copy

Expand all Collapse all

`{  *   "data": [          *   {                  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f09",                      *   "object": "file",                      *   "bytes": 13000,                      *   "created_at": 1716963433,                      *   "filename": "files_upload.jsonl",                      *   "purpose": "fine-tune",                      *   "sample_type": "pretrain",                      *   "num_lines": 0,                      *   "mimetype": "string",                      *   "source": "upload",                      *   "signature": "string"                               }                   ],      *   "object": "string",      *   "total": 0       }`

## [](#tag/files/operation/files_api_routes_retrieve_file)Retrieve File

Returns information about a specific file.

##### Authorizations:

_ApiKey_

##### path Parameters

file\_id

required

string <uuid\> (File Id)

### Responses

**200**

OK

get/v1/files/{file\_id}

Production server

https://api.mistral.ai/v1/files/{file\_id}

### Response samples

*   200

Content type

application/json

Copy

`{  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f09",      *   "object": "file",      *   "bytes": 13000,      *   "created_at": 1716963433,      *   "filename": "files_upload.jsonl",      *   "purpose": "fine-tune",      *   "sample_type": "pretrain",      *   "num_lines": 0,      *   "mimetype": "string",      *   "source": "upload",      *   "signature": "string",      *   "deleted": true       }`

## [](#tag/files/operation/files_api_routes_delete_file)Delete File

Delete a file.

##### Authorizations:

_ApiKey_

##### path Parameters

file\_id

required

string <uuid\> (File Id)

### Responses

**200**

OK

delete/v1/files/{file\_id}

Production server

https://api.mistral.ai/v1/files/{file\_id}

### Response samples

*   200

Content type

application/json

Copy

`{  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f09",      *   "object": "file",      *   "deleted": false       }`

## [](#tag/files/operation/files_api_routes_download_file)Download File

Download a file

##### Authorizations:

_ApiKey_

##### path Parameters

file\_id

required

string <uuid\> (File Id)

### Responses

**200**

OK

get/v1/files/{file\_id}/content

Production server

https://api.mistral.ai/v1/files/{file\_id}/content

## [](#tag/files/operation/files_api_routes_get_signed_url)Get Signed Url

##### Authorizations:

_ApiKey_

##### path Parameters

file\_id

required

string <uuid\> (File Id)

##### query Parameters

expiry

integer (Expiry)

Default: 24

Number of hours before the url becomes invalid. Defaults to 24h

### Responses

**200**

OK

get/v1/files/{file\_id}/url

Production server

https://api.mistral.ai/v1/files/{file\_id}/url

### Response samples

*   200

Content type

application/json

Copy

`{  *   "url": "string"       }`

## [](#tag/fine-tuning)Fine Tuning

Fine-tuning API

## [](#tag/fine-tuning/operation/jobs_api_routes_fine_tuning_get_fine_tuning_jobs)Get Fine Tuning Jobs

Get a list of fine-tuning jobs for your organization and user.

##### Authorizations:

_ApiKey_

##### query Parameters

page

integer (Page)

Default: 0

The page number of the results to be returned.

page\_size

integer (Page Size)

Default: 100

The number of items to return per page.

model

Model (string) or Model (null) (Model)

The model name used for fine-tuning to filter on. When set, the other results are not displayed.

created\_after

Created After (string) or Created After (null) (Created After)

The date/time to filter on. When set, the results for previous creation times are not displayed.

created\_before

Created Before (string) or Created Before (null) (Created Before)

created\_by\_me

boolean (Created By Me)

Default: false

When set, only return results for jobs created by the API caller. Other results are not displayed.

status

Status (string) or Status (null) (Status)

The current job state to filter on. When set, the other results are not displayed.

wandb\_project

Wandb Project (string) or Wandb Project (null) (Wandb Project)

The Weights and Biases project to filter on. When set, the other results are not displayed.

wandb\_name

Wandb Name (string) or Wandb Name (null) (Wandb Name)

The Weight and Biases run name to filter on. When set, the other results are not displayed.

suffix

Suffix (string) or Suffix (null) (Suffix)

The model suffix to filter on. When set, the other results are not displayed.

### Responses

**200**

OK

get/v1/fine\_tuning/jobs

Production server

https://api.mistral.ai/v1/fine\_tuning/jobs

### Response samples

*   200

Content type

application/json

Copy

Expand all Collapse all

`{  *   "data": [ ],      *   "object": "list",      *   "total": 0       }`

## [](#tag/fine-tuning/operation/jobs_api_routes_fine_tuning_create_fine_tuning_job)Create Fine Tuning Job

Create a new fine-tuning job, it will be queued for processing.

##### Authorizations:

_ApiKey_

##### query Parameters

dry\_run

Dry Run (boolean) or Dry Run (null) (Dry Run)

*   If `true` the job is not spawned, instead the query returns a handful of useful metadata for the user to perform sanity checks (see `LegacyJobMetadataOut` response).
*   Otherwise, the job is started and the query returns the job ID along with some of the input parameters (see `JobOut` response).

##### Request Body schema: application/json

required

model

required

string (FineTuneableModel)

Enum: "ministral-3b-latest" "ministral-8b-latest" "open-mistral-7b" "open-mistral-nemo" "mistral-small-latest" "mistral-medium-latest" "mistral-large-latest" "pixtral-12b-latest" "codestral-latest"

The name of the model to fine-tune.

training\_files

Array of objects (Training Files)

Default: \[\]

validation\_files

Array of Validation Files (strings) or Validation Files (null) (Validation Files)

A list containing the IDs of uploaded files that contain validation data. If you provide these files, the data is used to generate validation metrics periodically during fine-tuning. These metrics can be viewed in `checkpoints` when getting the status of a running fine-tuning job. The same data should not be present in both train and validation files.

suffix

Suffix (string) or Suffix (null) (Suffix)

A string that will be added to your fine-tuning model name. For example, a suffix of "my-great-model" would produce a model name like `ft:open-mistral-7b:my-great-model:xxx...`

integrations

Array of Integrations (any) or Integrations (null) (Integrations)

A list of integrations to enable for your fine-tuning job.

auto\_start

boolean (Auto Start)

This field will be required in a future release.

invalid\_sample\_skip\_percentage

number (Invalid Sample Skip Percentage) \[ 0 .. 0.5 \]

Default: 0

job\_type

FineTuneableModelType (string) or null

hyperparameters

required

CompletionTrainingParametersIn (object) or ClassifierTrainingParametersIn (object) (Hyperparameters)

repositories

Array of Repositories (any) or Repositories (null) (Repositories)

classifier\_targets

Array of Classifier Targets (objects) or Classifier Targets (null) (Classifier Targets)

### Responses

**200**

OK

post/v1/fine\_tuning/jobs

Production server

https://api.mistral.ai/v1/fine\_tuning/jobs

### Request samples

*   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  *   "model": "ministral-3b-latest",      *   "training_files": [ ],      *   "validation_files": [          *   "497f6eca-6276-4993-bfeb-53cbbbba6f08"                   ],      *   "suffix": "string",      *   "integrations": [          *   {                  *   "type": "wandb",                      *   "project": "string",                      *   "name": "string",                      *   "api_key": "stringstringstringstringstringstringstri",                      *   "run_name": "string"                               }                   ],      *   "auto_start": true,      *   "invalid_sample_skip_percentage": 0,      *   "job_type": "completion",      *   "hyperparameters": {          *   "training_steps": 1,              *   "learning_rate": 0.0001,              *   "weight_decay": 0.1,              *   "warmup_fraction": 0.05,              *   "epochs": 0,              *   "seq_len": 100,              *   "fim_ratio": 0.9                   },      *   "repositories": [          *   {                  *   "type": "github",                      *   "name": "string",                      *   "owner": "string",                      *   "ref": "string",                      *   "weight": 1,                      *   "token": "string"                               }                   ],      *   "classifier_targets": [          *   {                  *   "name": "string",                      *   "labels": [                          *   "string"                                           ],                      *   "weight": 1,                      *   "loss_function": "single_class"                               }                   ]       }`

### Response samples

*   200

Content type

application/json

Example

ResponseLegacyJobMetadataOutResponse

Copy

Expand all Collapse all

`{  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",      *   "auto_start": true,      *   "model": "ministral-3b-latest",      *   "status": "QUEUED",      *   "created_at": 0,      *   "modified_at": 0,      *   "training_files": [          *   "497f6eca-6276-4993-bfeb-53cbbbba6f08"                   ],      *   "validation_files": [ ],      *   "object": "job",      *   "fine_tuned_model": "string",      *   "suffix": "string",      *   "integrations": [          *   {                  *   "type": "wandb",                      *   "project": "string",                      *   "name": "string",                      *   "run_name": "string",                      *   "url": "string"                               }                   ],      *   "trained_tokens": 0,      *   "metadata": {          *   "expected_duration_seconds": 0,              *   "cost": 0,              *   "cost_currency": "string",              *   "train_tokens_per_step": 0,              *   "train_tokens": 0,              *   "data_tokens": 0,              *   "estimated_start_time": 0                   },      *   "job_type": "completion",      *   "hyperparameters": {          *   "training_steps": 1,              *   "learning_rate": 0.0001,              *   "weight_decay": 0.1,              *   "warmup_fraction": 0.05,              *   "epochs": 0,              *   "seq_len": 100,              *   "fim_ratio": 0.9                   },      *   "repositories": [ ]       }`

## [](#tag/fine-tuning/operation/jobs_api_routes_fine_tuning_get_fine_tuning_job)Get Fine Tuning Job

Get a fine-tuned job details by its UUID.

##### Authorizations:

_ApiKey_

##### path Parameters

job\_id

required

string <uuid\> (Job Id)

The ID of the job to analyse.

### Responses

**200**

OK

get/v1/fine\_tuning/jobs/{job\_id}

Production server

https://api.mistral.ai/v1/fine\_tuning/jobs/{job\_id}

### Response samples

*   200

Content type

application/json

Example

classifiercompletionclassifier

Copy

Expand all Collapse all

`{  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",      *   "auto_start": true,      *   "model": "ministral-3b-latest",      *   "status": "QUEUED",      *   "created_at": 0,      *   "modified_at": 0,      *   "training_files": [          *   "497f6eca-6276-4993-bfeb-53cbbbba6f08"                   ],      *   "validation_files": [ ],      *   "object": "job",      *   "fine_tuned_model": "string",      *   "suffix": "string",      *   "integrations": [          *   {                  *   "type": "wandb",                      *   "project": "string",                      *   "name": "string",                      *   "run_name": "string",                      *   "url": "string"                               }                   ],      *   "trained_tokens": 0,      *   "metadata": {          *   "expected_duration_seconds": 0,              *   "cost": 0,              *   "cost_currency": "string",              *   "train_tokens_per_step": 0,              *   "train_tokens": 0,              *   "data_tokens": 0,              *   "estimated_start_time": 0                   },      *   "job_type": "classifier",      *   "hyperparameters": {          *   "training_steps": 1,              *   "learning_rate": 0.0001,              *   "weight_decay": 0.1,              *   "warmup_fraction": 0.05,              *   "epochs": 0,              *   "seq_len": 100                   },      *   "events": [ ],      *   "checkpoints": [ ],      *   "classifier_targets": [          *   {                  *   "name": "string",                      *   "labels": [                          *   "string"                                           ],                      *   "weight": 0,                      *   "loss_function": "single_class"                               }                   ]       }`

## [](#tag/fine-tuning/operation/jobs_api_routes_fine_tuning_cancel_fine_tuning_job)Cancel Fine Tuning Job

Request the cancellation of a fine tuning job.

##### Authorizations:

_ApiKey_

##### path Parameters

job\_id

required

string <uuid\> (Job Id)

The ID of the job to cancel.

### Responses

**200**

OK

post/v1/fine\_tuning/jobs/{job\_id}/cancel

Production server

https://api.mistral.ai/v1/fine\_tuning/jobs/{job\_id}/cancel

### Response samples

*   200

Content type

application/json

Example

classifiercompletionclassifier

Copy

Expand all Collapse all

`{  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",      *   "auto_start": true,      *   "model": "ministral-3b-latest",      *   "status": "QUEUED",      *   "created_at": 0,      *   "modified_at": 0,      *   "training_files": [          *   "497f6eca-6276-4993-bfeb-53cbbbba6f08"                   ],      *   "validation_files": [ ],      *   "object": "job",      *   "fine_tuned_model": "string",      *   "suffix": "string",      *   "integrations": [          *   {                  *   "type": "wandb",                      *   "project": "string",                      *   "name": "string",                      *   "run_name": "string",                      *   "url": "string"                               }                   ],      *   "trained_tokens": 0,      *   "metadata": {          *   "expected_duration_seconds": 0,              *   "cost": 0,              *   "cost_currency": "string",              *   "train_tokens_per_step": 0,              *   "train_tokens": 0,              *   "data_tokens": 0,              *   "estimated_start_time": 0                   },      *   "job_type": "classifier",      *   "hyperparameters": {          *   "training_steps": 1,              *   "learning_rate": 0.0001,              *   "weight_decay": 0.1,              *   "warmup_fraction": 0.05,              *   "epochs": 0,              *   "seq_len": 100                   },      *   "events": [ ],      *   "checkpoints": [ ],      *   "classifier_targets": [          *   {                  *   "name": "string",                      *   "labels": [                          *   "string"                                           ],                      *   "weight": 0,                      *   "loss_function": "single_class"                               }                   ]       }`

## [](#tag/fine-tuning/operation/jobs_api_routes_fine_tuning_start_fine_tuning_job)Start Fine Tuning Job

Request the start of a validated fine tuning job.

##### Authorizations:

_ApiKey_

##### path Parameters

job\_id

required

string <uuid\> (Job Id)

### Responses

**200**

OK

post/v1/fine\_tuning/jobs/{job\_id}/start

Production server

https://api.mistral.ai/v1/fine\_tuning/jobs/{job\_id}/start

### Response samples

*   200

Content type

application/json

Example

classifiercompletionclassifier

Copy

Expand all Collapse all

`{  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",      *   "auto_start": true,      *   "model": "ministral-3b-latest",      *   "status": "QUEUED",      *   "created_at": 0,      *   "modified_at": 0,      *   "training_files": [          *   "497f6eca-6276-4993-bfeb-53cbbbba6f08"                   ],      *   "validation_files": [ ],      *   "object": "job",      *   "fine_tuned_model": "string",      *   "suffix": "string",      *   "integrations": [          *   {                  *   "type": "wandb",                      *   "project": "string",                      *   "name": "string",                      *   "run_name": "string",                      *   "url": "string"                               }                   ],      *   "trained_tokens": 0,      *   "metadata": {          *   "expected_duration_seconds": 0,              *   "cost": 0,              *   "cost_currency": "string",              *   "train_tokens_per_step": 0,              *   "train_tokens": 0,              *   "data_tokens": 0,              *   "estimated_start_time": 0                   },      *   "job_type": "classifier",      *   "hyperparameters": {          *   "training_steps": 1,              *   "learning_rate": 0.0001,              *   "weight_decay": 0.1,              *   "warmup_fraction": 0.05,              *   "epochs": 0,              *   "seq_len": 100                   },      *   "events": [ ],      *   "checkpoints": [ ],      *   "classifier_targets": [          *   {                  *   "name": "string",                      *   "labels": [                          *   "string"                                           ],                      *   "weight": 0,                      *   "loss_function": "single_class"                               }                   ]       }`

## [](#tag/models)Models

Model Management API

## [](#tag/models/operation/list_models_v1_models_get)List Models

List all models available to the user.

##### Authorizations:

_ApiKey_

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/models

Production server

https://api.mistral.ai/v1/models

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "object": "list",      *   "data": [          *   {                  *   "id": "string",                      *   "object": "model",                      *   "created": 0,                      *   "owned_by": "mistralai",                      *   "capabilities": {                          *   "completion_chat": true,                              *   "completion_fim": false,                              *   "function_calling": true,                              *   "fine_tuning": false,                              *   "vision": false,                              *   "classification": false                                           },                      *   "name": "string",                      *   "description": "string",                      *   "max_context_length": 32768,                      *   "aliases": [ ],                      *   "deprecation": "2019-08-24T14:15:22Z",                      *   "deprecation_replacement_model": "string",                      *   "default_model_temperature": 0,                      *   "type": "base"                               }                   ]       }`

## [](#tag/models/operation/retrieve_model_v1_models__model_id__get)Retrieve Model

Retrieve information about a model.

##### Authorizations:

_ApiKey_

##### path Parameters

model\_id

required

string (Model Id)

Example: ft:open-mistral-7b:587a6b29:20240514:7e773925

The ID of the model to retrieve.

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/models/{model\_id}

Production server

https://api.mistral.ai/v1/models/{model\_id}

### Response samples

*   200
*   422

Content type

application/json

Example

basefine-tunedbase

Copy

Expand all Collapse all

`{  *   "id": "string",      *   "object": "model",      *   "created": 0,      *   "owned_by": "mistralai",      *   "capabilities": {          *   "completion_chat": true,              *   "completion_fim": false,              *   "function_calling": true,              *   "fine_tuning": false,              *   "vision": false,              *   "classification": false                   },      *   "name": "string",      *   "description": "string",      *   "max_context_length": 32768,      *   "aliases": [ ],      *   "deprecation": "2019-08-24T14:15:22Z",      *   "deprecation_replacement_model": "string",      *   "default_model_temperature": 0,      *   "type": "base"       }`

## [](#tag/models/operation/delete_model_v1_models__model_id__delete)Delete Model

Delete a fine-tuned model.

##### Authorizations:

_ApiKey_

##### path Parameters

model\_id

required

string (Model Id)

Example: ft:open-mistral-7b:587a6b29:20240514:7e773925

The ID of the model to delete.

### Responses

**200**

Successful Response

**422**

Validation Error

delete/v1/models/{model\_id}

Production server

https://api.mistral.ai/v1/models/{model\_id}

### Response samples

*   200
*   422

Content type

application/json

Copy

`{  *   "id": "ft:open-mistral-7b:587a6b29:20240514:7e773925",      *   "object": "model",      *   "deleted": true       }`

## [](#tag/models/operation/jobs_api_routes_fine_tuning_update_fine_tuned_model)Update Fine Tuned Model

Update a model name or description.

##### Authorizations:

_ApiKey_

##### path Parameters

model\_id

required

string (Model Id)

Example: ft:open-mistral-7b:587a6b29:20240514:7e773925

The ID of the model to update.

##### Request Body schema: application/json

required

name

Name (string) or Name (null) (Name)

description

Description (string) or Description (null) (Description)

### Responses

**200**

OK

patch/v1/fine\_tuning/models/{model\_id}

Production server

https://api.mistral.ai/v1/fine\_tuning/models/{model\_id}

### Request samples

*   Payload

Content type

application/json

Copy

`{  *   "name": "string",      *   "description": "string"       }`

### Response samples

*   200

Content type

application/json

Example

classifiercompletionclassifier

Copy

Expand all Collapse all

`{  *   "id": "string",      *   "object": "model",      *   "created": 0,      *   "owned_by": "string",      *   "workspace_id": "string",      *   "root": "string",      *   "root_version": "string",      *   "archived": true,      *   "name": "string",      *   "description": "string",      *   "capabilities": {          *   "completion_chat": true,              *   "completion_fim": false,              *   "function_calling": false,              *   "fine_tuning": false,              *   "classification": false                   },      *   "max_context_length": 32768,      *   "aliases": [ ],      *   "job": "4bbaedb0-902b-4b27-8218-8f40d3470a54",      *   "classifier_targets": [          *   {                  *   "name": "string",                      *   "labels": [                          *   "string"                                           ],                      *   "weight": 0,                      *   "loss_function": "single_class"                               }                   ],      *   "model_type": "classifier"       }`

## [](#tag/models/operation/jobs_api_routes_fine_tuning_archive_fine_tuned_model)Archive Fine Tuned Model

Archive a fine-tuned model.

##### Authorizations:

_ApiKey_

##### path Parameters

model\_id

required

string (Model Id)

Example: ft:open-mistral-7b:587a6b29:20240514:7e773925

The ID of the model to archive.

### Responses

**200**

OK

post/v1/fine\_tuning/models/{model\_id}/archive

Production server

https://api.mistral.ai/v1/fine\_tuning/models/{model\_id}/archive

### Response samples

*   200

Content type

application/json

Copy

`{  *   "id": "string",      *   "object": "model",      *   "archived": true       }`

## [](#tag/models/operation/jobs_api_routes_fine_tuning_unarchive_fine_tuned_model)Unarchive Fine Tuned Model

Un-archive a fine-tuned model.

##### Authorizations:

_ApiKey_

##### path Parameters

model\_id

required

string (Model Id)

Example: ft:open-mistral-7b:587a6b29:20240514:7e773925

The ID of the model to unarchive.

### Responses

**200**

OK

delete/v1/fine\_tuning/models/{model\_id}/archive

Production server

https://api.mistral.ai/v1/fine\_tuning/models/{model\_id}/archive

### Response samples

*   200

Content type

application/json

Copy

`{  *   "id": "string",      *   "object": "model",      *   "archived": false       }`

## [](#tag/batch)Batch

Batch API

## [](#tag/batch/operation/jobs_api_routes_batch_get_batch_jobs)Get Batch Jobs

Get a list of batch jobs for your organization and user.

##### Authorizations:

_ApiKey_

##### query Parameters

page

integer (Page)

Default: 0

page\_size

integer (Page Size)

Default: 100

model

Model (string) or Model (null) (Model)

agent\_id

Agent Id (string) or Agent Id (null) (Agent Id)

metadata

Metadata (object) or Metadata (null) (Metadata)

created\_after

Created After (string) or Created After (null) (Created After)

created\_by\_me

boolean (Created By Me)

Default: false

status

Array of Status (strings) or Status (null) (Status)

### Responses

**200**

OK

get/v1/batch/jobs

Production server

https://api.mistral.ai/v1/batch/jobs

### Response samples

*   200

Content type

application/json

Copy

Expand all Collapse all

`{  *   "data": [ ],      *   "object": "list",      *   "total": 0       }`

## [](#tag/batch/operation/jobs_api_routes_batch_create_batch_job)Create Batch Job

Create a new batch job, it will be queued for processing.

##### Authorizations:

_ApiKey_

##### Request Body schema: application/json

required

input\_files

required

Array of strings <uuid\> (Input Files) \[ items <uuid > \]

endpoint

required

string (ApiEndpoint)

Enum: "/v1/chat/completions" "/v1/embeddings" "/v1/fim/completions" "/v1/moderations" "/v1/chat/moderations"

model

Model (string) or Model (null) (Model)

agent\_id

Agent Id (string) or Agent Id (null) (Agent Id)

metadata

Metadata (object) or Metadata (null) (Metadata)

timeout\_hours

integer (Timeout Hours)

Default: 24

### Responses

**200**

OK

post/v1/batch/jobs

Production server

https://api.mistral.ai/v1/batch/jobs

### Request samples

*   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  *   "input_files": [          *   "497f6eca-6276-4993-bfeb-53cbbbba6f08"                   ],      *   "endpoint": "/v1/chat/completions",      *   "model": "string",      *   "agent_id": "string",      *   "metadata": {          *   "property1": "string",              *   "property2": "string"                   },      *   "timeout_hours": 24       }`

### Response samples

*   200

Content type

application/json

Copy

Expand all Collapse all

`{  *   "id": "string",      *   "object": "batch",      *   "input_files": [          *   "497f6eca-6276-4993-bfeb-53cbbbba6f08"                   ],      *   "metadata": { },      *   "endpoint": "string",      *   "model": "string",      *   "agent_id": "string",      *   "output_file": "c7c9cb17-f818-4ee3-85de-0d2f8954882c",      *   "error_file": "6b79e6a4-c3aa-4da1-8fb4-9e2520d26bfa",      *   "errors": [          *   {                  *   "message": "string",                      *   "count": 1                               }                   ],      *   "status": "QUEUED",      *   "created_at": 0,      *   "total_requests": 0,      *   "completed_requests": 0,      *   "succeeded_requests": 0,      *   "failed_requests": 0,      *   "started_at": 0,      *   "completed_at": 0       }`

## [](#tag/batch/operation/jobs_api_routes_batch_get_batch_job)Get Batch Job

Get a batch job details by its UUID.

##### Authorizations:

_ApiKey_

##### path Parameters

job\_id

required

string <uuid\> (Job Id)

### Responses

**200**

OK

get/v1/batch/jobs/{job\_id}

Production server

https://api.mistral.ai/v1/batch/jobs/{job\_id}

### Response samples

*   200

Content type

application/json

Copy

Expand all Collapse all

`{  *   "id": "string",      *   "object": "batch",      *   "input_files": [          *   "497f6eca-6276-4993-bfeb-53cbbbba6f08"                   ],      *   "metadata": { },      *   "endpoint": "string",      *   "model": "string",      *   "agent_id": "string",      *   "output_file": "c7c9cb17-f818-4ee3-85de-0d2f8954882c",      *   "error_file": "6b79e6a4-c3aa-4da1-8fb4-9e2520d26bfa",      *   "errors": [          *   {                  *   "message": "string",                      *   "count": 1                               }                   ],      *   "status": "QUEUED",      *   "created_at": 0,      *   "total_requests": 0,      *   "completed_requests": 0,      *   "succeeded_requests": 0,      *   "failed_requests": 0,      *   "started_at": 0,      *   "completed_at": 0       }`

## [](#tag/batch/operation/jobs_api_routes_batch_cancel_batch_job)Cancel Batch Job

Request the cancellation of a batch job.

##### Authorizations:

_ApiKey_

##### path Parameters

job\_id

required

string <uuid\> (Job Id)

### Responses

**200**

OK

post/v1/batch/jobs/{job\_id}/cancel

Production server

https://api.mistral.ai/v1/batch/jobs/{job\_id}/cancel

### Response samples

*   200

Content type

application/json

Copy

Expand all Collapse all

`{  *   "id": "string",      *   "object": "batch",      *   "input_files": [          *   "497f6eca-6276-4993-bfeb-53cbbbba6f08"                   ],      *   "metadata": { },      *   "endpoint": "string",      *   "model": "string",      *   "agent_id": "string",      *   "output_file": "c7c9cb17-f818-4ee3-85de-0d2f8954882c",      *   "error_file": "6b79e6a4-c3aa-4da1-8fb4-9e2520d26bfa",      *   "errors": [          *   {                  *   "message": "string",                      *   "count": 1                               }                   ],      *   "status": "QUEUED",      *   "created_at": 0,      *   "total_requests": 0,      *   "completed_requests": 0,      *   "succeeded_requests": 0,      *   "failed_requests": 0,      *   "started_at": 0,      *   "completed_at": 0       }`

## [](#tag/ocr)OCR API

OCR API

## [](#tag/ocr/operation/ocr_v1_ocr_post)OCR

##### Authorizations:

_ApiKey_

##### Request Body schema: application/json

required

model

required

Model (string) or Model (null) (Model)

id

string (Id)

document

required

FileChunk (object) or DocumentURLChunk (object) or ImageURLChunk (object) (Document)

Document to run OCR on

pages

Array of Pages (integers) or Pages (null) (Pages)

Specific pages user wants to process in various formats: single number, range, or list of both. Starts from 0

include\_image\_base64

Include Image Base64 (boolean) or Include Image Base64 (null) (Include Image Base64)

Include image URLs in response

image\_limit

Image Limit (integer) or Image Limit (null) (Image Limit)

Max images to extract

image\_min\_size

Image Min Size (integer) or Image Min Size (null) (Image Min Size)

Minimum height and width of image to extract

bbox\_annotation\_format

ResponseFormat (object) or null

Structured output class for extracting useful information from each extracted bounding box / image from document. Only json\_schema is valid for this field

document\_annotation\_format

ResponseFormat (object) or null

Structured output class for extracting useful information from the entire document. Only json\_schema is valid for this field

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/ocr

Production server

https://api.mistral.ai/v1/ocr

### Request samples

*   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  *   "model": "string",      *   "id": "string",      *   "document": {          *   "type": "file",              *   "file_id": "8a0cfb4f-ddc9-436d-91bb-75133c583767"                   },      *   "pages": [          *   0                   ],      *   "include_image_base64": true,      *   "image_limit": 0,      *   "image_min_size": 0,      *   "bbox_annotation_format": {          *   "type": "text",              *   "json_schema": {                  *   "name": "string",                      *   "description": "string",                      *   "schema": { },                      *   "strict": false                               }                   },      *   "document_annotation_format": {          *   "type": "text",              *   "json_schema": {                  *   "name": "string",                      *   "description": "string",                      *   "schema": { },                      *   "strict": false                               }                   }       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "pages": [          *   {                  *   "index": 0,                      *   "markdown": "string",                      *   "images": [                          *   {                                  *   "id": "string",                                      *   "top_left_x": 0,                                      *   "top_left_y": 0,                                      *   "bottom_right_x": 0,                                      *   "bottom_right_y": 0,                                      *   "image_base64": "string",                                      *   "image_annotation": "string"                                                       }                                           ],                      *   "dimensions": {                          *   "dpi": 0,                              *   "height": 0,                              *   "width": 0                                           }                               }                   ],      *   "model": "string",      *   "document_annotation": "string",      *   "usage_info": {          *   "pages_processed": 0,              *   "doc_size_bytes": 0                   }       }`

## [](#tag/audio.transcriptions)Transcriptions API

API for audio transcription.

## [](#tag/audio.transcriptions/operation/audio_api_v1_transcriptions_post)Create Transcription

##### Authorizations:

_ApiKey_

##### Request Body schema: multipart/form-data

required

model

required

string (Model)

file

File (string) or File (null) (File)

Default: null

file\_url

File Url (string) or File Url (null) (File Url)

Default: null

Url of a file to be transcribed

file\_id

File Id (string) or File Id (null) (File Id)

Default: null

ID of a file uploaded to /v1/files

language

Language (string) or Language (null) (Language)

Default: null

Language of the audio, e.g. 'en'. Providing the language can boost accuracy.

temperature

Temperature (number) or Temperature (null) (Temperature)

Default: null

stream

boolean (Stream)

Default: false

timestamp\_granularities

Array of strings (Timestamp Granularities)

Items Value: "segment"

Granularities of timestamps to include in the response.

### Responses

**200**

Successful Response

post/v1/audio/transcriptions

Production server

https://api.mistral.ai/v1/audio/transcriptions

### Response samples

*   200

Content type

application/json

Copy

Expand all Collapse all

`{  *   "model": "string",      *   "text": "string",      *   "language": "string",      *   "segments": [          *   {                  *   "text": "string",                      *   "start": 0,                      *   "end": 0,                      *   "type": "transcription_segment"                               }                   ],      *   "usage": {          *   "prompt_tokens": 0,              *   "completion_tokens": 0,              *   "total_tokens": 0,              *   "prompt_audio_seconds": 0                   }       }`

## [](#tag/audio.transcriptions/operation/audio_api_v1_transcriptions_post_stream)Create streaming transcription (SSE)

##### Authorizations:

_ApiKey_

##### Request Body schema: multipart/form-data

required

model

required

string (Model)

file

File (string) or File (null) (File)

Default: null

file\_url

File Url (string) or File Url (null) (File Url)

Default: null

Url of a file to be transcribed

file\_id

File Id (string) or File Id (null) (File Id)

Default: null

ID of a file uploaded to /v1/files

language

Language (string) or Language (null) (Language)

Default: null

Language of the audio, e.g. 'en'. Providing the language can boost accuracy.

temperature

Temperature (number) or Temperature (null) (Temperature)

Default: null

stream

boolean (Stream)

Default: true

Value: true

timestamp\_granularities

Array of strings (Timestamp Granularities)

Items Value: "segment"

Granularities of timestamps to include in the response.

### Responses

**200**

Stream of transcription events

post/v1/audio/transcriptions#stream

Production server

https://api.mistral.ai/v1/audio/transcriptions#stream

## [](#tag/beta.agents)(beta) Agents API

(beta) Agents API

## [](#tag/beta.agents/operation/agents_api_v1_agents_create)Create a agent that can be used within a conversation.

Create a new agent giving it instructions, tools, description. The agent is then available to be used as a regular assistant in a conversation or as part of an agent pool from which it can be used.

##### Authorizations:

_ApiKey_

##### Request Body schema: application/json

required

instructions

Instructions (string) or Instructions (null) (Instructions)

Instruction prompt the model will follow during the conversation.

tools

Array of any (Tools)

List of tools which are available to the model during the conversation.

completion\_args

object (CompletionArgs)

Completion arguments that will be used to generate assistant responses. Can be overridden at each message request.

model

required

string (Model)

name

required

string (Name)

description

Description (string) or Description (null) (Description)

handoffs

Array of Handoffs (strings) or Handoffs (null) (Handoffs)

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/agents

Production server

https://api.mistral.ai/v1/agents

### Request samples

*   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  *   "instructions": "string",      *   "tools": [          *   {                  *   "type": "function",                      *   "function": {                          *   "name": "string",                              *   "description": "",                              *   "strict": false,                              *   "parameters": { }                                           }                               }                   ],      *   "completion_args": {          *   "stop": "string",              *   "presence_penalty": -2,              *   "frequency_penalty": -2,              *   "temperature": 1,              *   "top_p": 1,              *   "max_tokens": 0,              *   "random_seed": 0,              *   "prediction": {                  *   "type": "content",                      *   "content": ""                               },              *   "response_format": {                  *   "type": "text",                      *   "json_schema": {                          *   "name": "string",                              *   "description": "string",                              *   "schema": { },                              *   "strict": false                                           }                               },              *   "tool_choice": "auto"                   },      *   "model": "string",      *   "name": "string",      *   "description": "string",      *   "handoffs": [          *   "string"                   ]       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "instructions": "string",      *   "tools": [          *   {                  *   "type": "function",                      *   "function": {                          *   "name": "string",                              *   "description": "",                              *   "strict": false,                              *   "parameters": { }                                           }                               }                   ],      *   "completion_args": {          *   "stop": "string",              *   "presence_penalty": -2,              *   "frequency_penalty": -2,              *   "temperature": 1,              *   "top_p": 1,              *   "max_tokens": 0,              *   "random_seed": 0,              *   "prediction": {                  *   "type": "content",                      *   "content": ""                               },              *   "response_format": {                  *   "type": "text",                      *   "json_schema": {                          *   "name": "string",                              *   "description": "string",                              *   "schema": { },                              *   "strict": false                                           }                               },              *   "tool_choice": "auto"                   },      *   "model": "string",      *   "name": "string",      *   "description": "string",      *   "handoffs": [          *   "string"                   ],      *   "object": "agent",      *   "id": "string",      *   "version": 0,      *   "created_at": "2019-08-24T14:15:22Z",      *   "updated_at": "2019-08-24T14:15:22Z"       }`

## [](#tag/beta.agents/operation/agents_api_v1_agents_list)List agent entities.

Retrieve a list of agent entities sorted by creation time.

##### Authorizations:

_ApiKey_

##### query Parameters

page

integer (Page)

Default: 0

page\_size

integer (Page Size)

Default: 20

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/agents

Production server

https://api.mistral.ai/v1/agents

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`[  *   {          *   "instructions": "string",              *   "tools": [                  *   {                          *   "type": "function",                              *   "function": {                                  *   "name": "string",                                      *   "description": "",                                      *   "strict": false,                                      *   "parameters": { }                                                       }                                           }                               ],              *   "completion_args": {                  *   "stop": "string",                      *   "presence_penalty": -2,                      *   "frequency_penalty": -2,                      *   "temperature": 1,                      *   "top_p": 1,                      *   "max_tokens": 0,                      *   "random_seed": 0,                      *   "prediction": {                          *   "type": "content",                              *   "content": ""                                           },                      *   "response_format": {                          *   "type": "text",                              *   "json_schema": {                                  *   "name": "string",                                      *   "description": "string",                                      *   "schema": { },                                      *   "strict": false                                                       }                                           },                      *   "tool_choice": "auto"                               },              *   "model": "string",              *   "name": "string",              *   "description": "string",              *   "handoffs": [                  *   "string"                               ],              *   "object": "agent",              *   "id": "string",              *   "version": 0,              *   "created_at": "2019-08-24T14:15:22Z",              *   "updated_at": "2019-08-24T14:15:22Z"                   }       ]`

## [](#tag/beta.agents/operation/agents_api_v1_agents_get)Retrieve an agent entity.

Given an agent retrieve an agent entity with its attributes.

##### Authorizations:

_ApiKey_

##### path Parameters

agent\_id

required

string (Agent Id)

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/agents/{agent\_id}

Production server

https://api.mistral.ai/v1/agents/{agent\_id}

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "instructions": "string",      *   "tools": [          *   {                  *   "type": "function",                      *   "function": {                          *   "name": "string",                              *   "description": "",                              *   "strict": false,                              *   "parameters": { }                                           }                               }                   ],      *   "completion_args": {          *   "stop": "string",              *   "presence_penalty": -2,              *   "frequency_penalty": -2,              *   "temperature": 1,              *   "top_p": 1,              *   "max_tokens": 0,              *   "random_seed": 0,              *   "prediction": {                  *   "type": "content",                      *   "content": ""                               },              *   "response_format": {                  *   "type": "text",                      *   "json_schema": {                          *   "name": "string",                              *   "description": "string",                              *   "schema": { },                              *   "strict": false                                           }                               },              *   "tool_choice": "auto"                   },      *   "model": "string",      *   "name": "string",      *   "description": "string",      *   "handoffs": [          *   "string"                   ],      *   "object": "agent",      *   "id": "string",      *   "version": 0,      *   "created_at": "2019-08-24T14:15:22Z",      *   "updated_at": "2019-08-24T14:15:22Z"       }`

## [](#tag/beta.agents/operation/agents_api_v1_agents_update)Update an agent entity.

Update an agent attributes and create a new version.

##### Authorizations:

_ApiKey_

##### path Parameters

agent\_id

required

string (Agent Id)

##### Request Body schema: application/json

required

instructions

Instructions (string) or Instructions (null) (Instructions)

Instruction prompt the model will follow during the conversation.

tools

Array of any (Tools)

List of tools which are available to the model during the conversation.

completion\_args

object (CompletionArgs)

Completion arguments that will be used to generate assistant responses. Can be overridden at each message request.

model

Model (string) or Model (null) (Model)

name

Name (string) or Name (null) (Name)

description

Description (string) or Description (null) (Description)

handoffs

Array of Handoffs (strings) or Handoffs (null) (Handoffs)

### Responses

**200**

Successful Response

**422**

Validation Error

patch/v1/agents/{agent\_id}

Production server

https://api.mistral.ai/v1/agents/{agent\_id}

### Request samples

*   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  *   "instructions": "string",      *   "tools": [          *   {                  *   "type": "function",                      *   "function": {                          *   "name": "string",                              *   "description": "",                              *   "strict": false,                              *   "parameters": { }                                           }                               }                   ],      *   "completion_args": {          *   "stop": "string",              *   "presence_penalty": -2,              *   "frequency_penalty": -2,              *   "temperature": 1,              *   "top_p": 1,              *   "max_tokens": 0,              *   "random_seed": 0,              *   "prediction": {                  *   "type": "content",                      *   "content": ""                               },              *   "response_format": {                  *   "type": "text",                      *   "json_schema": {                          *   "name": "string",                              *   "description": "string",                              *   "schema": { },                              *   "strict": false                                           }                               },              *   "tool_choice": "auto"                   },      *   "model": "string",      *   "name": "string",      *   "description": "string",      *   "handoffs": [          *   "string"                   ]       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "instructions": "string",      *   "tools": [          *   {                  *   "type": "function",                      *   "function": {                          *   "name": "string",                              *   "description": "",                              *   "strict": false,                              *   "parameters": { }                                           }                               }                   ],      *   "completion_args": {          *   "stop": "string",              *   "presence_penalty": -2,              *   "frequency_penalty": -2,              *   "temperature": 1,              *   "top_p": 1,              *   "max_tokens": 0,              *   "random_seed": 0,              *   "prediction": {                  *   "type": "content",                      *   "content": ""                               },              *   "response_format": {                  *   "type": "text",                      *   "json_schema": {                          *   "name": "string",                              *   "description": "string",                              *   "schema": { },                              *   "strict": false                                           }                               },              *   "tool_choice": "auto"                   },      *   "model": "string",      *   "name": "string",      *   "description": "string",      *   "handoffs": [          *   "string"                   ],      *   "object": "agent",      *   "id": "string",      *   "version": 0,      *   "created_at": "2019-08-24T14:15:22Z",      *   "updated_at": "2019-08-24T14:15:22Z"       }`

## [](#tag/beta.agents/operation/agents_api_v1_agents_update_version)Update an agent version.

Switch the version of an agent.

##### Authorizations:

_ApiKey_

##### path Parameters

agent\_id

required

string (Agent Id)

##### query Parameters

version

required

integer (Version)

### Responses

**200**

Successful Response

**422**

Validation Error

patch/v1/agents/{agent\_id}/version

Production server

https://api.mistral.ai/v1/agents/{agent\_id}/version

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "instructions": "string",      *   "tools": [          *   {                  *   "type": "function",                      *   "function": {                          *   "name": "string",                              *   "description": "",                              *   "strict": false,                              *   "parameters": { }                                           }                               }                   ],      *   "completion_args": {          *   "stop": "string",              *   "presence_penalty": -2,              *   "frequency_penalty": -2,              *   "temperature": 1,              *   "top_p": 1,              *   "max_tokens": 0,              *   "random_seed": 0,              *   "prediction": {                  *   "type": "content",                      *   "content": ""                               },              *   "response_format": {                  *   "type": "text",                      *   "json_schema": {                          *   "name": "string",                              *   "description": "string",                              *   "schema": { },                              *   "strict": false                                           }                               },              *   "tool_choice": "auto"                   },      *   "model": "string",      *   "name": "string",      *   "description": "string",      *   "handoffs": [          *   "string"                   ],      *   "object": "agent",      *   "id": "string",      *   "version": 0,      *   "created_at": "2019-08-24T14:15:22Z",      *   "updated_at": "2019-08-24T14:15:22Z"       }`

## [](#tag/beta.conversations)(beta) Conversations API

(beta) Conversations API

## [](#tag/beta.conversations/operation/agents_api_v1_conversations_start)Create a conversation and append entries to it.

Create a new conversation, using a base model or an agent and append entries. Completion and tool executions are run and the response is appended to the conversation.Use the returned conversation\_id to continue the conversation.

##### Authorizations:

_ApiKey_

##### Request Body schema: application/json

required

inputs

required

ConversationInputs (string) or (Array of InputEntries (MessageInputEntry (object) or MessageOutputEntry (object) or FunctionResultEntry (object) or FunctionCallEntry (object) or ToolExecutionEntry (object) or AgentHandoffEntry (object))) (ConversationInputs)

stream

Stream (boolean) or Stream (boolean) (Stream)

Default: false

Value: false

store

Store (boolean) or Store (null) (Store)

Default: null

handoff\_execution

Handoff Execution (string) or Handoff Execution (null) (Handoff Execution)

Default: null

instructions

Instructions (string) or Instructions (null) (Instructions)

Default: null

tools

Array of Tools (any) or Tools (null) (Tools)

Default: null

completion\_args

CompletionArgs (object) or null

Default: null

name

Name (string) or Name (null) (Name)

Default: null

description

Description (string) or Description (null) (Description)

Default: null

agent\_id

Agent Id (string) or Agent Id (null) (Agent Id)

Default: null

model

Model (string) or Model (null) (Model)

Default: null

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/conversations

Production server

https://api.mistral.ai/v1/conversations

### Request samples

*   Payload

Content type

application/json

Copy

`{  *   "inputs": "string",      *   "stream": false,      *   "store": null,      *   "handoff_execution": null,      *   "instructions": null,      *   "tools": null,      *   "completion_args": null,      *   "name": null,      *   "description": null,      *   "agent_id": null,      *   "model": null       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "object": "conversation.response",      *   "conversation_id": "string",      *   "outputs": [          *   {                  *   "object": "entry",                      *   "type": "message.output",                      *   "created_at": "2019-08-24T14:15:22Z",                      *   "completed_at": "2019-08-24T14:15:22Z",                      *   "id": "string",                      *   "agent_id": "string",                      *   "model": "string",                      *   "role": "assistant",                      *   "content": "string"                               }                   ],      *   "usage": {          *   "prompt_tokens": 0,              *   "completion_tokens": 0,              *   "total_tokens": 0,              *   "connector_tokens": null,              *   "connectors": null                   }       }`

## [](#tag/beta.conversations/operation/agents_api_v1_conversations_list)List all created conversations.

Retrieve a list of conversation entities sorted by creation time.

##### Authorizations:

_ApiKey_

##### query Parameters

page

integer (Page)

Default: 0

page\_size

integer (Page Size)

Default: 100

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/conversations

Production server

https://api.mistral.ai/v1/conversations

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`[  *   {          *   "instructions": "string",              *   "tools": [                  *   {                          *   "type": "function",                              *   "function": {                                  *   "name": "string",                                      *   "description": "",                                      *   "strict": false,                                      *   "parameters": { }                                                       }                                           }                               ],              *   "completion_args": {                  *   "stop": "string",                      *   "presence_penalty": -2,                      *   "frequency_penalty": -2,                      *   "temperature": 1,                      *   "top_p": 1,                      *   "max_tokens": 0,                      *   "random_seed": 0,                      *   "prediction": {                          *   "type": "content",                              *   "content": ""                                           },                      *   "response_format": {                          *   "type": "text",                              *   "json_schema": {                                  *   "name": "string",                                      *   "description": "string",                                      *   "schema": { },                                      *   "strict": false                                                       }                                           },                      *   "tool_choice": "auto"                               },              *   "name": "string",              *   "description": "string",              *   "object": "conversation",              *   "id": "string",              *   "created_at": "2019-08-24T14:15:22Z",              *   "updated_at": "2019-08-24T14:15:22Z",              *   "model": "string"                   }       ]`

## [](#tag/beta.conversations/operation/agents_api_v1_conversations_get)Retrieve a conversation information.

Given a conversation\_id retrieve a conversation entity with its attributes.

##### Authorizations:

_ApiKey_

##### path Parameters

conversation\_id

required

string (Conversation Id)

ID of the conversation from which we are fetching metadata.

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/conversations/{conversation\_id}

Production server

https://api.mistral.ai/v1/conversations/{conversation\_id}

### Response samples

*   200
*   422

Content type

application/json

Example

ModelConversationAgentConversationModelConversation

Copy

Expand all Collapse all

`{  *   "instructions": "string",      *   "tools": [          *   {                  *   "type": "function",                      *   "function": {                          *   "name": "string",                              *   "description": "",                              *   "strict": false,                              *   "parameters": { }                                           }                               }                   ],      *   "completion_args": {          *   "stop": "string",              *   "presence_penalty": -2,              *   "frequency_penalty": -2,              *   "temperature": 1,              *   "top_p": 1,              *   "max_tokens": 0,              *   "random_seed": 0,              *   "prediction": {                  *   "type": "content",                      *   "content": ""                               },              *   "response_format": {                  *   "type": "text",                      *   "json_schema": {                          *   "name": "string",                              *   "description": "string",                              *   "schema": { },                              *   "strict": false                                           }                               },              *   "tool_choice": "auto"                   },      *   "name": "string",      *   "description": "string",      *   "object": "conversation",      *   "id": "string",      *   "created_at": "2019-08-24T14:15:22Z",      *   "updated_at": "2019-08-24T14:15:22Z",      *   "model": "string"       }`

## [](#tag/beta.conversations/operation/agents_api_v1_conversations_append)Append new entries to an existing conversation.

Run completion on the history of the conversation and the user entries. Return the new created entries.

##### Authorizations:

_ApiKey_

##### path Parameters

conversation\_id

required

string (Conversation Id)

ID of the conversation to which we append entries.

##### Request Body schema: application/json

required

inputs

required

ConversationInputs (string) or (Array of InputEntries (MessageInputEntry (object) or MessageOutputEntry (object) or FunctionResultEntry (object) or FunctionCallEntry (object) or ToolExecutionEntry (object) or AgentHandoffEntry (object))) (ConversationInputs)

stream

boolean (Stream)

Default: false

Value: false

Whether to stream back partial progress. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

store

boolean (Store)

Default: true

Whether to store the results into our servers or not.

handoff\_execution

string (Handoff Execution)

Default: "server"

Enum: "client" "server"

completion\_args

object (CompletionArgs)

Completion arguments that will be used to generate assistant responses. Can be overridden at each message request.

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/conversations/{conversation\_id}

Production server

https://api.mistral.ai/v1/conversations/{conversation\_id}

### Request samples

*   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  *   "inputs": "string",      *   "stream": false,      *   "store": true,      *   "handoff_execution": "client",      *   "completion_args": {          *   "stop": "string",              *   "presence_penalty": -2,              *   "frequency_penalty": -2,              *   "temperature": 1,              *   "top_p": 1,              *   "max_tokens": 0,              *   "random_seed": 0,              *   "prediction": {                  *   "type": "content",                      *   "content": ""                               },              *   "response_format": {                  *   "type": "text",                      *   "json_schema": {                          *   "name": "string",                              *   "description": "string",                              *   "schema": { },                              *   "strict": false                                           }                               },              *   "tool_choice": "auto"                   }       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "object": "conversation.response",      *   "conversation_id": "string",      *   "outputs": [          *   {                  *   "object": "entry",                      *   "type": "message.output",                      *   "created_at": "2019-08-24T14:15:22Z",                      *   "completed_at": "2019-08-24T14:15:22Z",                      *   "id": "string",                      *   "agent_id": "string",                      *   "model": "string",                      *   "role": "assistant",                      *   "content": "string"                               }                   ],      *   "usage": {          *   "prompt_tokens": 0,              *   "completion_tokens": 0,              *   "total_tokens": 0,              *   "connector_tokens": null,              *   "connectors": null                   }       }`

## [](#tag/beta.conversations/operation/agents_api_v1_conversations_history)Retrieve all entries in a conversation.

Given a conversation\_id retrieve all the entries belonging to that conversation. The entries are sorted in the order they were appended, those can be messages, connectors or function\_call.

##### Authorizations:

_ApiKey_

##### path Parameters

conversation\_id

required

string (Conversation Id)

ID of the conversation from which we are fetching entries.

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/conversations/{conversation\_id}/history

Production server

https://api.mistral.ai/v1/conversations/{conversation\_id}/history

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "object": "conversation.history",      *   "conversation_id": "string",      *   "entries": [          *   {                  *   "object": "entry",                      *   "type": "message.input",                      *   "created_at": "2019-08-24T14:15:22Z",                      *   "completed_at": "2019-08-24T14:15:22Z",                      *   "id": "string",                      *   "role": "assistant",                      *   "content": "string",                      *   "prefix": false                               }                   ]       }`

## [](#tag/beta.conversations/operation/agents_api_v1_conversations_messages)Retrieve all messages in a conversation.

Given a conversation\_id retrieve all the messages belonging to that conversation. This is similar to retrieving all entries except we filter the messages only.

##### Authorizations:

_ApiKey_

##### path Parameters

conversation\_id

required

string (Conversation Id)

ID of the conversation from which we are fetching messages.

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/conversations/{conversation\_id}/messages

Production server

https://api.mistral.ai/v1/conversations/{conversation\_id}/messages

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "object": "conversation.messages",      *   "conversation_id": "string",      *   "messages": [          *   {                  *   "object": "entry",                      *   "type": "message.input",                      *   "created_at": "2019-08-24T14:15:22Z",                      *   "completed_at": "2019-08-24T14:15:22Z",                      *   "id": "string",                      *   "role": "assistant",                      *   "content": "string",                      *   "prefix": false                               }                   ]       }`

## [](#tag/beta.conversations/operation/agents_api_v1_conversations_restart)Restart a conversation starting from a given entry.

Given a conversation\_id and an id, recreate a conversation from this point and run completion. A new conversation is returned with the new entries returned.

##### Authorizations:

_ApiKey_

##### path Parameters

conversation\_id

required

string (Conversation Id)

ID of the original conversation which is being restarted.

##### Request Body schema: application/json

required

inputs

required

ConversationInputs (string) or (Array of InputEntries (MessageInputEntry (object) or MessageOutputEntry (object) or FunctionResultEntry (object) or FunctionCallEntry (object) or ToolExecutionEntry (object) or AgentHandoffEntry (object))) (ConversationInputs)

stream

boolean (Stream)

Default: false

Value: false

Whether to stream back partial progress. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

store

boolean (Store)

Default: true

Whether to store the results into our servers or not.

handoff\_execution

string (Handoff Execution)

Default: "server"

Enum: "client" "server"

completion\_args

object (CompletionArgs)

Completion arguments that will be used to generate assistant responses. Can be overridden at each message request.

from\_entry\_id

required

string (From Entry Id)

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/conversations/{conversation\_id}/restart

Production server

https://api.mistral.ai/v1/conversations/{conversation\_id}/restart

### Request samples

*   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  *   "inputs": "string",      *   "stream": false,      *   "store": true,      *   "handoff_execution": "client",      *   "completion_args": {          *   "stop": "string",              *   "presence_penalty": -2,              *   "frequency_penalty": -2,              *   "temperature": 1,              *   "top_p": 1,              *   "max_tokens": 0,              *   "random_seed": 0,              *   "prediction": {                  *   "type": "content",                      *   "content": ""                               },              *   "response_format": {                  *   "type": "text",                      *   "json_schema": {                          *   "name": "string",                              *   "description": "string",                              *   "schema": { },                              *   "strict": false                                           }                               },              *   "tool_choice": "auto"                   },      *   "from_entry_id": "string"       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "object": "conversation.response",      *   "conversation_id": "string",      *   "outputs": [          *   {                  *   "object": "entry",                      *   "type": "message.output",                      *   "created_at": "2019-08-24T14:15:22Z",                      *   "completed_at": "2019-08-24T14:15:22Z",                      *   "id": "string",                      *   "agent_id": "string",                      *   "model": "string",                      *   "role": "assistant",                      *   "content": "string"                               }                   ],      *   "usage": {          *   "prompt_tokens": 0,              *   "completion_tokens": 0,              *   "total_tokens": 0,              *   "connector_tokens": null,              *   "connectors": null                   }       }`

## [](#tag/beta.conversations/operation/agents_api_v1_conversations_start_stream)Create a conversation and append entries to it.

Create a new conversation, using a base model or an agent and append entries. Completion and tool executions are run and the response is appended to the conversation.Use the returned conversation\_id to continue the conversation.

##### Authorizations:

_ApiKey_

##### Request Body schema: application/json

required

inputs

required

ConversationInputs (string) or (Array of InputEntries (MessageInputEntry (object) or MessageOutputEntry (object) or FunctionResultEntry (object) or FunctionCallEntry (object) or ToolExecutionEntry (object) or AgentHandoffEntry (object))) (ConversationInputs)

stream

Stream (boolean) or Stream (boolean) (Stream)

Default: true

Value: true

store

Store (boolean) or Store (null) (Store)

Default: null

handoff\_execution

Handoff Execution (string) or Handoff Execution (null) (Handoff Execution)

Default: null

instructions

Instructions (string) or Instructions (null) (Instructions)

Default: null

tools

Array of Tools (any) or Tools (null) (Tools)

Default: null

completion\_args

CompletionArgs (object) or null

Default: null

name

Name (string) or Name (null) (Name)

Default: null

description

Description (string) or Description (null) (Description)

Default: null

agent\_id

Agent Id (string) or Agent Id (null) (Agent Id)

Default: null

model

Model (string) or Model (null) (Model)

Default: null

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/conversations#stream

Production server

https://api.mistral.ai/v1/conversations#stream

### Request samples

*   Payload

Content type

application/json

Copy

`{  *   "inputs": "string",      *   "stream": true,      *   "store": null,      *   "handoff_execution": null,      *   "instructions": null,      *   "tools": null,      *   "completion_args": null,      *   "name": null,      *   "description": null,      *   "agent_id": null,      *   "model": null       }`

### Response samples

*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "detail": [          *   {                  *   "loc": [                          *   "string"                                           ],                      *   "msg": "string",                      *   "type": "string"                               }                   ]       }`

## [](#tag/beta.conversations/operation/agents_api_v1_conversations_append_stream)Append new entries to an existing conversation.

Run completion on the history of the conversation and the user entries. Return the new created entries.

##### Authorizations:

_ApiKey_

##### path Parameters

conversation\_id

required

string (Conversation Id)

ID of the conversation to which we append entries.

##### Request Body schema: application/json

required

inputs

required

ConversationInputs (string) or (Array of InputEntries (MessageInputEntry (object) or MessageOutputEntry (object) or FunctionResultEntry (object) or FunctionCallEntry (object) or ToolExecutionEntry (object) or AgentHandoffEntry (object))) (ConversationInputs)

stream

boolean (Stream)

Default: true

Value: true

Whether to stream back partial progress. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

store

boolean (Store)

Default: true

Whether to store the results into our servers or not.

handoff\_execution

string (Handoff Execution)

Default: "server"

Enum: "client" "server"

completion\_args

object (CompletionArgs)

Completion arguments that will be used to generate assistant responses. Can be overridden at each message request.

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/conversations/{conversation\_id}#stream

Production server

https://api.mistral.ai/v1/conversations/{conversation\_id}#stream

### Request samples

*   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  *   "inputs": "string",      *   "stream": true,      *   "store": true,      *   "handoff_execution": "client",      *   "completion_args": {          *   "stop": "string",              *   "presence_penalty": -2,              *   "frequency_penalty": -2,              *   "temperature": 1,              *   "top_p": 1,              *   "max_tokens": 0,              *   "random_seed": 0,              *   "prediction": {                  *   "type": "content",                      *   "content": ""                               },              *   "response_format": {                  *   "type": "text",                      *   "json_schema": {                          *   "name": "string",                              *   "description": "string",                              *   "schema": { },                              *   "strict": false                                           }                               },              *   "tool_choice": "auto"                   }       }`

### Response samples

*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "detail": [          *   {                  *   "loc": [                          *   "string"                                           ],                      *   "msg": "string",                      *   "type": "string"                               }                   ]       }`

## [](#tag/beta.conversations/operation/agents_api_v1_conversations_restart_stream)Restart a conversation starting from a given entry.

Given a conversation\_id and an id, recreate a conversation from this point and run completion. A new conversation is returned with the new entries returned.

##### Authorizations:

_ApiKey_

##### path Parameters

conversation\_id

required

string (Conversation Id)

ID of the original conversation which is being restarted.

##### Request Body schema: application/json

required

inputs

required

ConversationInputs (string) or (Array of InputEntries (MessageInputEntry (object) or MessageOutputEntry (object) or FunctionResultEntry (object) or FunctionCallEntry (object) or ToolExecutionEntry (object) or AgentHandoffEntry (object))) (ConversationInputs)

stream

boolean (Stream)

Default: true

Value: true

Whether to stream back partial progress. Otherwise, the server will hold the request open until the timeout or until completion, with the response containing the full result as JSON.

store

boolean (Store)

Default: true

Whether to store the results into our servers or not.

handoff\_execution

string (Handoff Execution)

Default: "server"

Enum: "client" "server"

completion\_args

object (CompletionArgs)

Completion arguments that will be used to generate assistant responses. Can be overridden at each message request.

from\_entry\_id

required

string (From Entry Id)

### Responses

**200**

Successful Response

**422**

Validation Error

post/v1/conversations/{conversation\_id}/restart#stream

Production server

https://api.mistral.ai/v1/conversations/{conversation\_id}/restart#stream

### Request samples

*   Payload

Content type

application/json

Copy

Expand all Collapse all

`{  *   "inputs": "string",      *   "stream": true,      *   "store": true,      *   "handoff_execution": "client",      *   "completion_args": {          *   "stop": "string",              *   "presence_penalty": -2,              *   "frequency_penalty": -2,              *   "temperature": 1,              *   "top_p": 1,              *   "max_tokens": 0,              *   "random_seed": 0,              *   "prediction": {                  *   "type": "content",                      *   "content": ""                               },              *   "response_format": {                  *   "type": "text",                      *   "json_schema": {                          *   "name": "string",                              *   "description": "string",                              *   "schema": { },                              *   "strict": false                                           }                               },              *   "tool_choice": "auto"                   },      *   "from_entry_id": "string"       }`

### Response samples

*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "detail": [          *   {                  *   "loc": [                          *   "string"                                           ],                      *   "msg": "string",                      *   "type": "string"                               }                   ]       }`

## [](#tag/beta.libraries)(beta) Libraries API - Main

(beta) Libraries API to create and manage libraries - index your documents to enhance agent capabilities.

## [](#tag/beta.libraries/operation/libraries_list_v1)List all libraries you have access to.

List all libraries that you have created or have been shared with you.

##### Authorizations:

_ApiKey_

### Responses

**200**

Successful Response

get/v1/libraries

Production server

https://api.mistral.ai/v1/libraries

### Response samples

*   200

Content type

application/json

Copy

Expand all Collapse all

`{  *   "data": [          *   {                  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",                      *   "name": "string",                      *   "created_at": "2019-08-24T14:15:22Z",                      *   "updated_at": "2019-08-24T14:15:22Z",                      *   "owner_id": "8826ee2e-7933-4665-aef2-2393f84a0d05",                      *   "owner_type": "string",                      *   "total_size": 0,                      *   "nb_documents": 0,                      *   "chunk_size": 0,                      *   "emoji": "string",                      *   "description": "string",                      *   "generated_name": "string",                      *   "generated_description": "string",                      *   "explicit_user_members_count": 0,                      *   "explicit_workspace_members_count": 0,                      *   "org_sharing_role": "string"                               }                   ]       }`

## [](#tag/beta.libraries/operation/libraries_create_v1)Create a new Library.

Create a new Library, you will be marked as the owner and only you will have the possibility to share it with others. When first created this will only be accessible by you.

##### Authorizations:

_ApiKey_

##### Request Body schema: application/json

required

name

required

string (Name)

description

Description (string) or Description (null) (Description)

chunk\_size

Chunk Size (integer) or Chunk Size (null) (Chunk Size)

### Responses

**201**

Successful Response

**422**

Validation Error

post/v1/libraries

Production server

https://api.mistral.ai/v1/libraries

### Request samples

*   Payload

Content type

application/json

Copy

`{  *   "name": "string",      *   "description": "string",      *   "chunk_size": 0       }`

### Response samples

*   201
*   422

Content type

application/json

Copy

`{  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",      *   "name": "string",      *   "created_at": "2019-08-24T14:15:22Z",      *   "updated_at": "2019-08-24T14:15:22Z",      *   "owner_id": "8826ee2e-7933-4665-aef2-2393f84a0d05",      *   "owner_type": "string",      *   "total_size": 0,      *   "nb_documents": 0,      *   "chunk_size": 0,      *   "emoji": "string",      *   "description": "string",      *   "generated_name": "string",      *   "generated_description": "string",      *   "explicit_user_members_count": 0,      *   "explicit_workspace_members_count": 0,      *   "org_sharing_role": "string"       }`

## [](#tag/beta.libraries/operation/libraries_get_v1)Detailed information about a specific Library.

Given a library id, details information about that Library.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/libraries/{library\_id}

Production server

https://api.mistral.ai/v1/libraries/{library\_id}

### Response samples

*   200
*   422

Content type

application/json

Copy

`{  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",      *   "name": "string",      *   "created_at": "2019-08-24T14:15:22Z",      *   "updated_at": "2019-08-24T14:15:22Z",      *   "owner_id": "8826ee2e-7933-4665-aef2-2393f84a0d05",      *   "owner_type": "string",      *   "total_size": 0,      *   "nb_documents": 0,      *   "chunk_size": 0,      *   "emoji": "string",      *   "description": "string",      *   "generated_name": "string",      *   "generated_description": "string",      *   "explicit_user_members_count": 0,      *   "explicit_workspace_members_count": 0,      *   "org_sharing_role": "string"       }`

## [](#tag/beta.libraries/operation/libraries_delete_v1)Delete a library and all of it's document.

Given a library id, deletes it together with all documents that have been uploaded to that library.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

### Responses

**200**

Successful Response

**422**

Validation Error

delete/v1/libraries/{library\_id}

Production server

https://api.mistral.ai/v1/libraries/{library\_id}

### Response samples

*   200
*   422

Content type

application/json

Copy

`{  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",      *   "name": "string",      *   "created_at": "2019-08-24T14:15:22Z",      *   "updated_at": "2019-08-24T14:15:22Z",      *   "owner_id": "8826ee2e-7933-4665-aef2-2393f84a0d05",      *   "owner_type": "string",      *   "total_size": 0,      *   "nb_documents": 0,      *   "chunk_size": 0,      *   "emoji": "string",      *   "description": "string",      *   "generated_name": "string",      *   "generated_description": "string",      *   "explicit_user_members_count": 0,      *   "explicit_workspace_members_count": 0,      *   "org_sharing_role": "string"       }`

## [](#tag/beta.libraries/operation/libraries_update_v1)Update a library.

Given a library id, you can update the name and description.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

##### Request Body schema: application/json

required

name

Name (string) or Name (null) (Name)

description

Description (string) or Description (null) (Description)

### Responses

**200**

Successful Response

**422**

Validation Error

put/v1/libraries/{library\_id}

Production server

https://api.mistral.ai/v1/libraries/{library\_id}

### Request samples

*   Payload

Content type

application/json

Copy

`{  *   "name": "string",      *   "description": "string"       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

`{  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",      *   "name": "string",      *   "created_at": "2019-08-24T14:15:22Z",      *   "updated_at": "2019-08-24T14:15:22Z",      *   "owner_id": "8826ee2e-7933-4665-aef2-2393f84a0d05",      *   "owner_type": "string",      *   "total_size": 0,      *   "nb_documents": 0,      *   "chunk_size": 0,      *   "emoji": "string",      *   "description": "string",      *   "generated_name": "string",      *   "generated_description": "string",      *   "explicit_user_members_count": 0,      *   "explicit_workspace_members_count": 0,      *   "org_sharing_role": "string"       }`

## [](#tag/beta.libraries.documents)(beta) Libraries API - Documents

(beta) Libraries API - manage documents in a library.

## [](#tag/beta.libraries.documents/operation/libraries_documents_list_v1)List document in a given library.

Given a library, lists the document that have been uploaded to that library.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

##### query Parameters

search

Search (string) or Search (null) (Search)

page\_size

integer (Page Size)

Default: 100

page

integer (Page)

Default: 0

sort\_by

string (Sort By)

Default: "created\_at"

sort\_order

string (Sort Order)

Default: "desc"

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/libraries/{library\_id}/documents

Production server

https://api.mistral.ai/v1/libraries/{library\_id}/documents

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "pagination": {          *   "total_items": 0,              *   "total_pages": 0,              *   "current_page": 0,              *   "page_size": 0,              *   "has_more": true                   },      *   "data": [          *   {                  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",                      *   "library_id": "21f784c9-c915-48d4-a805-f15b3e01b084",                      *   "hash": "string",                      *   "mime_type": "string",                      *   "extension": "string",                      *   "size": 0,                      *   "name": "string",                      *   "summary": "string",                      *   "created_at": "2019-08-24T14:15:22Z",                      *   "last_processed_at": "2019-08-24T14:15:22Z",                      *   "number_of_pages": 0,                      *   "processing_status": "string",                      *   "uploaded_by_id": "890d2c95-7e66-4f6f-803c-a2ce12e35ae3",                      *   "uploaded_by_type": "string",                      *   "tokens_processing_main_content": 0,                      *   "tokens_processing_summary": 0,                      *   "tokens_processing_total": 0                               }                   ]       }`

## [](#tag/beta.libraries.documents/operation/libraries_documents_upload_v1)Upload a new document.

Given a library, upload a new document to that library. It is queued for processing, it status will change it has been processed. The processing has to be completed in order be discoverable for the library search

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

##### Request Body schema: multipart/form-data

required

file

required

string <binary\> (File)

The File object (not file name) to be uploaded. To upload a file and specify a custom file name you should format your request as such:

file=@path/to/your/file.jsonl;filename=custom_name.jsonl

Otherwise, you can just keep the original file name:

file=@path/to/your/file.jsonl

### Responses

**200**

A document with the same hash was found in this library. Returns the existing document.

**201**

Upload successful, returns the created document information's.

**422**

Validation Error

post/v1/libraries/{library\_id}/documents

Production server

https://api.mistral.ai/v1/libraries/{library\_id}/documents

### Response samples

*   200
*   201
*   422

Content type

application/json

Copy

`{  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",      *   "library_id": "21f784c9-c915-48d4-a805-f15b3e01b084",      *   "hash": "string",      *   "mime_type": "string",      *   "extension": "string",      *   "size": 0,      *   "name": "string",      *   "summary": "string",      *   "created_at": "2019-08-24T14:15:22Z",      *   "last_processed_at": "2019-08-24T14:15:22Z",      *   "number_of_pages": 0,      *   "processing_status": "string",      *   "uploaded_by_id": "890d2c95-7e66-4f6f-803c-a2ce12e35ae3",      *   "uploaded_by_type": "string",      *   "tokens_processing_main_content": 0,      *   "tokens_processing_summary": 0,      *   "tokens_processing_total": 0       }`

## [](#tag/beta.libraries.documents/operation/libraries_documents_get_v1)Retrieve the metadata of a specific document.

Given a library and a document in this library, you can retrieve the metadata of that document.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

document\_id

required

string <uuid\> (Document Id)

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/libraries/{library\_id}/documents/{document\_id}

Production server

https://api.mistral.ai/v1/libraries/{library\_id}/documents/{document\_id}

### Response samples

*   200
*   422

Content type

application/json

Copy

`{  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",      *   "library_id": "21f784c9-c915-48d4-a805-f15b3e01b084",      *   "hash": "string",      *   "mime_type": "string",      *   "extension": "string",      *   "size": 0,      *   "name": "string",      *   "summary": "string",      *   "created_at": "2019-08-24T14:15:22Z",      *   "last_processed_at": "2019-08-24T14:15:22Z",      *   "number_of_pages": 0,      *   "processing_status": "string",      *   "uploaded_by_id": "890d2c95-7e66-4f6f-803c-a2ce12e35ae3",      *   "uploaded_by_type": "string",      *   "tokens_processing_main_content": 0,      *   "tokens_processing_summary": 0,      *   "tokens_processing_total": 0       }`

## [](#tag/beta.libraries.documents/operation/libraries_documents_update_v1)Update the metadata of a specific document.

Given a library and a document in that library, update the name of that document.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

document\_id

required

string <uuid\> (Document Id)

##### Request Body schema: application/json

required

name

Name (string) or Name (null) (Name)

Any of

NameName

string (Name)

### Responses

**200**

Successful Response

**422**

Validation Error

put/v1/libraries/{library\_id}/documents/{document\_id}

Production server

https://api.mistral.ai/v1/libraries/{library\_id}/documents/{document\_id}

### Request samples

*   Payload

Content type

application/json

Copy

`{  *   "name": "string"       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

`{  *   "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",      *   "library_id": "21f784c9-c915-48d4-a805-f15b3e01b084",      *   "hash": "string",      *   "mime_type": "string",      *   "extension": "string",      *   "size": 0,      *   "name": "string",      *   "summary": "string",      *   "created_at": "2019-08-24T14:15:22Z",      *   "last_processed_at": "2019-08-24T14:15:22Z",      *   "number_of_pages": 0,      *   "processing_status": "string",      *   "uploaded_by_id": "890d2c95-7e66-4f6f-803c-a2ce12e35ae3",      *   "uploaded_by_type": "string",      *   "tokens_processing_main_content": 0,      *   "tokens_processing_summary": 0,      *   "tokens_processing_total": 0       }`

## [](#tag/beta.libraries.documents/operation/libraries_documents_delete_v1)Delete a document.

Given a library and a document in that library, delete that document. The document will be deleted from the library and the search index.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

document\_id

required

string <uuid\> (Document Id)

### Responses

**204**

Successful Response

**422**

Validation Error

delete/v1/libraries/{library\_id}/documents/{document\_id}

Production server

https://api.mistral.ai/v1/libraries/{library\_id}/documents/{document\_id}

### Response samples

*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "detail": [          *   {                  *   "loc": [                          *   "string"                                           ],                      *   "msg": "string",                      *   "type": "string"                               }                   ]       }`

## [](#tag/beta.libraries.documents/operation/libraries_documents_get_text_content_v1)Retrieve the text content of a specific document.

Given a library and a document in that library, you can retrieve the text content of that document if it exists. For documents like pdf, docx and pptx the text content results from our processing using Mistral OCR.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

document\_id

required

string <uuid\> (Document Id)

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/libraries/{library\_id}/documents/{document\_id}/text\_content

Production server

https://api.mistral.ai/v1/libraries/{library\_id}/documents/{document\_id}/text\_content

### Response samples

*   200
*   422

Content type

application/json

Copy

`{  *   "text": "string"       }`

## [](#tag/beta.libraries.documents/operation/libraries_documents_get_status_v1)Retrieve the processing status of a specific document.

Given a library and a document in that library, retrieve the processing status of that document.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

document\_id

required

string <uuid\> (Document Id)

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/libraries/{library\_id}/documents/{document\_id}/status

Production server

https://api.mistral.ai/v1/libraries/{library\_id}/documents/{document\_id}/status

### Response samples

*   200
*   422

Content type

application/json

Copy

`{  *   "document_id": "b792e8ae-2cb4-4209-85b9-32be4c2fcdd6",      *   "processing_status": "string"       }`

## [](#tag/beta.libraries.documents/operation/libraries_documents_get_signed_url_v1)Retrieve the signed URL of a specific document.

Given a library and a document in that library, retrieve the signed URL of a specific document.The url will expire after 30 minutes and can be accessed by anyone with the link.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

document\_id

required

string <uuid\> (Document Id)

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/libraries/{library\_id}/documents/{document\_id}/signed-url

Production server

https://api.mistral.ai/v1/libraries/{library\_id}/documents/{document\_id}/signed-url

### Response samples

*   200
*   422

Content type

application/json

Copy

`"string"`

## [](#tag/beta.libraries.documents/operation/libraries_documents_get_extracted_text_signed_url_v1)Retrieve the signed URL of text extracted from a given document.

Given a library and a document in that library, retrieve the signed URL of text extracted. For documents that are sent to the OCR this returns the result of the OCR queries.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

document\_id

required

string <uuid\> (Document Id)

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/libraries/{library\_id}/documents/{document\_id}/extracted-text-signed-url

Production server

https://api.mistral.ai/v1/libraries/{library\_id}/documents/{document\_id}/extracted-text-signed-url

### Response samples

*   200
*   422

Content type

application/json

Copy

`"string"`

## [](#tag/beta.libraries.documents/operation/libraries_documents_reprocess_v1)Reprocess a document.

Given a library and a document in that library, reprocess that document, it will be billed again.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

document\_id

required

string <uuid\> (Document Id)

### Responses

**204**

Successful Response

**422**

Validation Error

post/v1/libraries/{library\_id}/documents/{document\_id}/reprocess

Production server

https://api.mistral.ai/v1/libraries/{library\_id}/documents/{document\_id}/reprocess

### Response samples

*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "detail": [          *   {                  *   "loc": [                          *   "string"                                           ],                      *   "msg": "string",                      *   "type": "string"                               }                   ]       }`

## [](#tag/beta.libraries.accesses)(beta) Libraries API - Access

(beta) Libraries API - manage access to a library.

## [](#tag/beta.libraries.accesses/operation/libraries_share_list_v1)List all of the access to this library.

Given a library, list all of the Entity that have access and to what level.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

### Responses

**200**

Successful Response

**422**

Validation Error

get/v1/libraries/{library\_id}/share

Production server

https://api.mistral.ai/v1/libraries/{library\_id}/share

### Response samples

*   200
*   422

Content type

application/json

Copy

Expand all Collapse all

`{  *   "data": [          *   {                  *   "library_id": "21f784c9-c915-48d4-a805-f15b3e01b084",                      *   "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",                      *   "org_id": "a40f5d1f-d889-42e9-94ea-b9b33585fc6b",                      *   "role": "string",                      *   "share_with_type": "string",                      *   "share_with_uuid": "eefaa7a1-01a4-4caf-bd17-b410bd83c9fd"                               }                   ]       }`

## [](#tag/beta.libraries.accesses/operation/libraries_share_create_v1)Create or update an access level.

Given a library id, you can create or update the access level of an entity. You have to be owner of the library to share a library. An owner cannot change their own role. A library cannot be shared outside of the organization.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

##### Request Body schema: application/json

required

org\_id

required

string <uuid\> (Org Id)

level

required

string (ShareEnum)

Enum: "Viewer" "Editor"

share\_with\_uuid

required

string <uuid\>

The id of the entity (user, workspace or organization) to share with

share\_with\_type

required

string (EntityType)

Enum: "User" "Workspace" "Org"

The type of entity, used to share a library.

### Responses

**200**

Successful Response

**422**

Validation Error

put/v1/libraries/{library\_id}/share

Production server

https://api.mistral.ai/v1/libraries/{library\_id}/share

### Request samples

*   Payload

Content type

application/json

Copy

`{  *   "org_id": "a40f5d1f-d889-42e9-94ea-b9b33585fc6b",      *   "level": "Viewer",      *   "share_with_uuid": "eefaa7a1-01a4-4caf-bd17-b410bd83c9fd",      *   "share_with_type": "User"       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

`{  *   "library_id": "21f784c9-c915-48d4-a805-f15b3e01b084",      *   "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",      *   "org_id": "a40f5d1f-d889-42e9-94ea-b9b33585fc6b",      *   "role": "string",      *   "share_with_type": "string",      *   "share_with_uuid": "eefaa7a1-01a4-4caf-bd17-b410bd83c9fd"       }`

## [](#tag/beta.libraries.accesses/operation/libraries_share_delete_v1)Delete an access level.

Given a library id, you can delete the access level of an entity. An owner cannot delete it's own access. You have to be the owner of the library to delete an acces other than yours.

##### Authorizations:

_ApiKey_

##### path Parameters

library\_id

required

string <uuid\> (Library Id)

##### Request Body schema: application/json

required

org\_id

required

string <uuid\> (Org Id)

share\_with\_uuid

required

string <uuid\>

The id of the entity (user, workspace or organization) to share with

share\_with\_type

required

string (EntityType)

Enum: "User" "Workspace" "Org"

The type of entity, used to share a library.

### Responses

**200**

Successful Response

**422**

Validation Error

delete/v1/libraries/{library\_id}/share

Production server

https://api.mistral.ai/v1/libraries/{library\_id}/share

### Request samples

*   Payload

Content type

application/json

Copy

`{  *   "org_id": "a40f5d1f-d889-42e9-94ea-b9b33585fc6b",      *   "share_with_uuid": "eefaa7a1-01a4-4caf-bd17-b410bd83c9fd",      *   "share_with_type": "User"       }`

### Response samples

*   200
*   422

Content type

application/json

Copy

`{  *   "library_id": "21f784c9-c915-48d4-a805-f15b3e01b084",      *   "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",      *   "org_id": "a40f5d1f-d889-42e9-94ea-b9b33585fc6b",      *   "role": "string",      *   "share_with_type": "string",      *   "share_with_uuid": "eefaa7a1-01a4-4caf-bd17-b410bd83c9fd"       }`

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025 Mistral AI