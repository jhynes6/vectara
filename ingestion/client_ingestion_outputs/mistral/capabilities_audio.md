---
source: "website"
content_type: "services_products"
url: "https://docs.mistral.ai/capabilities/audio/"
title: "/capabilities/audio/"
domain: "docs.mistral.ai"
path: "/capabilities/audio/"
scraped_time: "2025-09-08T18:10:12.427848"
url_depth: 2
word_count: 4714
---

Audio & Transcription | Mistral AI

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
*   Audio & Transcription

On this page

# Audio & Transcription

Audio input capabilities enable models to chat and understand audio directly, this can be used for both chat use cases via audio or for optimal transcription purposes.

![audio_graph](/img/audio.png)

### Models with Audio Capabilities[​](#models-with-audio-capabilities "Direct link to Models with Audio Capabilities")

Audio capable models:

*   **Voxtral Small** (`voxtral-small-latest`) with audio input for [chat](#chat-with-audio) use cases.
*   **Voxtral Mini** (`voxtral-mini-latest`) with audio input for [chat](#chat-with-audio) use cases
*   And **Voxtral Mini Transcribe** (`voxtral-mini-latest` via `audio/transcriptions`), with an efficient [transcription](#transcription) only service.

## Chat with Audio[​](#chat-with-audio "Direct link to Chat with Audio")

Our Voxtral models are capable of being used for chat use cases with our chat completions endpoint.

### Passing an Audio File[​](#passing-an-audio-file "Direct link to Passing an Audio File")

To pass a local audio file, you can encode it in base64 and pass it as a string.

*   python
*   typescript
*   curl

import base64from mistralai import Mistral# Retrieve the API key from environment variablesapi_key = os.environ["MISTRAL_API_KEY"]# Specify modelmodel = "voxtral-mini-latest"# Initialize the Mistral clientclient = Mistral(api_key=api_key)# Encode the audio file in base64with open("examples/files/bcn_weather.mp3", "rb") as f:    content = f.read()audio_base64 = base64.b64encode(content).decode('utf-8')# Get the chat responsechat_response = client.chat.complete(    model=model,    messages=[{        "role": "user",        "content": [            {                "type": "input_audio",                "input_audio": audio_base64,            },            {                "type": "text",                "text": "What's in this file?"            },        ]    }],)# Print the content of the responseprint(chat_response.choices[0].message.content)

import { Mistral } from "@mistralai/mistralai";import fs from "fs";// Retrieve the API key from environment variablesconst apiKey = process.env["MISTRAL_API_KEY"];// Initialize the Mistral clientconst client = new Mistral({ apiKey: apiKey });// Encode the audio file in base64const audio_file = fs.readFileSync('local_audio.mp3');const audio_base64 = audio_file.toString('base64');// Get the chat responseconst chatResponse = await client.chat.complete({  model: "voxtral-mini-latest",  messages: [    {      role: "user",      content: [        {          type: "input_audio",          input_audio: audio_base64,        },        {          type: "text",          text: "What's in this file?",        },      ],    },  ],});// Print the content of the responseconsole.log(chatResponse.choices[0].message.content);

curl --location https://api.mistral.ai/v1/chat/completions \  --header "Authorization: Bearer $MISTRAL_API_KEY" \  --header "Content-Type: application/json" \  --data '{    "model": "voxtral-mini-latest",    "messages": [      {        "role": "user",        "content": [          {            "type": "input_audio",            "input_audio": "<audio_base64>",          },          {            "type": "text",            "text": "What'\''s in this file?"          }        ]      }    ]  }'

### Passing an Audio URL[​](#passing-an-audio-url "Direct link to Passing an Audio URL")

You can also provide an url of a file.

*   python
*   typescript
*   curl

import osfrom mistralai import Mistral# Retrieve the API key from environment variablesapi_key = os.environ["MISTRAL_API_KEY"]# Specify modelmodel = "voxtral-mini-latest"# Initialize the Mistral clientclient = Mistral(api_key=api_key)# Define the messages for the chatmessages = [    {        "role": "user",        "content": [            {                "type": "input_audio",                "input_audio": "https://download.samplelib.com/mp3/sample-15s.mp3",            },            {                "type": "text",                "text": "What's in this file?"            }        ]    }]# Get the chat responsechat_response = client.chat.complete(    model=model,    messages=messages)# Print the content of the responseprint(chat_response.choices[0].message.content)

import { Mistral } from "@mistralai/mistralai";// Retrieve the API key from environment variablesconst apiKey = process.env["MISTRAL_API_KEY"];// Initialize the Mistral clientconst client = new Mistral({ apiKey: apiKey });// Get the chat responseconst chatResponse = await client.chat.complete({  model: "voxtral-mini-latest",  messages: [    {      role: "user",      content: [        {          type: "input_audio",          input_audio: "https://download.samplelib.com/mp3/sample-15s.mp3",        },        {          type: "text",          text: "What's in this file?",        },      ],    },  ],});// Print the content of the responseconsole.log("JSON:", chatResponse.choices[0].message.content);

curl --location https://api.mistral.ai/v1/chat/completions \  --header "Authorization: Bearer $MISTRAL_API_KEY" \  --header "Content-Type: application/json" \  --data '{    "model": "voxtral-mini-2507",    "messages": [      {        "role": "user",        "content": [          {            "type": "input_audio",            "input_audio": "https://download.samplelib.com/mp3/sample-15s.mp3"          },          {            "type": "text",            "text": "What'\''s in this file?"          }        ]      }    ]  }'

### Passing an Uploaded Audio File[​](#passing-an-uploaded-audio-file "Direct link to Passing an Uploaded Audio File")

Alternatively, you can upload a local file to our cloud and then use a signed URL for the task.

*   python
*   typescript
*   curl

import osfrom mistralai import Mistral# Retrieve the API key from environment variablesapi_key = os.environ["MISTRAL_API_KEY"]# Specify modelmodel = "voxtral-mini-latest"# Initialize the Mistral clientclient = Mistral(api_key=api_key)# If local audio, upload and retrieve the signed urlwith open("music.mp3", "rb") as f:    uploaded_audio = client.files.upload(      file={          "content": f,          "file_name": f.name      },      purpose="audio"    )signed_url = client.files.get_signed_url(file_id=uploaded_audio.id)# Define the messages for the chatmessages = [    {        "role": "user",        "content": [            {                "type": "input_audio",                "input_audio": signed_url.url,            },            {                "type": "text",                "text": "What's in this file?"            }        ]    }]# Get the chat responsechat_response = client.chat.complete(    model=model,    messages=messages)# Print the content of the responseprint(chat_response.choices[0].message.content)

import { Mistral } from "@mistralai/mistralai";import fs from "fs";const apiKey = process.env["MISTRAL_API_KEY"];const client = new Mistral({ apiKey: apiKey });// If local document, upload and retrieve the signed urlconst audio_file = fs.readFileSync('local_audio.mp3');const uploaded_audio = await client.files.upload({  file: audio_file,  purpose: "audio",});const signedUrl = await client.files.getSignedUrl({    fileId: uploaded_audio.id,});// Get the chat responseconst chatResponse = await client.chat.complete({  model: "voxtral-mini-latest",  messages: [    {      role: "user",      content: [        {          type: "input_audio",          input_audio: signedUrl.url,        },        {          type: "text",          text: "What's in this file?",        },      ],    },  ],});// Print the content of the responseconsole.log(chatResponse.choices[0].message.content);

**Upload the Audio File**

curl --location https://api.mistral.ai/v1/files \  --header "Authorization: Bearer $MISTRAL_API_KEY" \  --form purpose="audio" \  --form file="@local_audio.mp3"

**Get the Signed URL**

curl --location "https://api.mistral.ai/v1/files/$id/url?expiry=24" \    --header "Accept: application/json" \    --header "Authorization: Bearer $MISTRAL_API_KEY"

**Send Completion Request**

curl --location https://api.mistral.ai/v1/chat/completions \  --header "Authorization: Bearer $MISTRAL_API_KEY" \  --header "Content-Type: application/json" \  --data '{    "model": "voxtral-mini-2507",    "messages": [      {        "role": "user",        "content": [          {            "type": "input_audio",            "input_audio": "<signed_url>"          },          {            "type": "text",            "text": "What'\''s in this file?"          }        ]      }    ]  }'

**Samples**

*   Chat
*   Music
*   Compare Speakers

**User**

Your browser does not support the audio element.

**Assistant**

Sure, here is the transcription of what you said:
"Today on July 15th, 2025, Mistral AI is announcing the new Voxtral models."
And here is the Python code to generate the first n digits of the Fibonacci sequence:

def fibonacci(n):if n <= 0:    return []elif n == 1:    return [0]elif n == 2:    return [0, 1]fib_sequence = [0, 1]for i in range(2, n):    next_value = fib_sequence[-1] + fib_sequence[-2]    fib_sequence.append(next_value)return fib_sequence# Example usage:n = 10  # Change this value to get the first n digits of the Fibonacci sequenceprint(fibonacci(n))

This code defines a function `fibonacci` that takes an integer `n` and returns a list containing the first `n` digits of the Fibonacci sequence. You can change the value of `n` to get the desired number of Fibonacci digits.

**User**

Your browser does not support the audio element.

What's in this file?

**Assistant**

The audio file contains music.

**User**

Your browser does not support the audio element.

Your browser does not support the audio element.

Which speaker do you prefer between the two? Why? How are they different from each other?

**Assistant**

The speaker who delivers the farewell address is more engaging and inspiring.
They express gratitude and optimism, emphasizing the importance of self-government and citizenship.
They also share personal experiences and observations, making the speech more relatable and heartfelt.
In contrast, the second speaker provides factual information about the weather in Barcelona, which is less engaging and lacks the emotional depth of the first speaker's address.

## Transcription[​](#transcription "Direct link to Transcription")

Transcription provides an optimized endpoint for transcription purposes and currently supports `voxtral-mini-latest`, which runs **Voxtral Mini Transcribe**.

**Parameters**
We provide different settings and parameters for transcription, such as:

*   `timestamp_granularities`: This allows you to set timestamps to track not only "what" was said but also "when". You can find more about timestamps [here](#transcription-with-timestamps).
*   `language`: Our transcription service also works as a language detection service. However, you can manually set the language of the transcription for better accuracy if the language of the audio is already known.

### Passing an Audio File[​](#passing-an-audio-file-1 "Direct link to Passing an Audio File")

Among the different methods to pass the audio, you can directly provide a path to a file to upload and transcribe it as follows:

*   python
*   typescript
*   curl

import osfrom mistralai import Mistral# Retrieve the API key from environment variablesapi_key = os.environ["MISTRAL_API_KEY"]# Specify modelmodel = "voxtral-mini-latest"# Initialize the Mistral clientclient = Mistral(api_key=api_key)# Get the transcriptionwith open("/path/to/file/audio.mp3", "rb") as f:    transcription_response = client.audio.transcriptions.complete(        model=model,        file={            "content": f,            "file_name": "audio.mp3",        },        ## language="en"    )# Print the content of the responseprint(transcription_response)

import { Mistral } from "@mistralai/mistralai";import fs from "fs";// Retrieve the API key from environment variablesconst apiKey = process.env["MISTRAL_API_KEY"];// Initialize the Mistral clientconst client = new Mistral({ apiKey: apiKey });// Get the transcriptionconst audio_file = fs.readFileSync('/path/to/file/audio.mp3');const transcriptionResponse = await client.audio.transcriptions.complete({  model: "voxtral-mini-latest",  file: {    fileName: "audio.mp3",    content: audio_file,  },  // language: "en"});// Log the content of the responseconsole.log(transcriptionResponse);

curl --location 'https://api.mistral.ai/v1/audio/transcriptions' \  --header "x-api-key: $MISTRAL_API_KEY" \  --form 'file=@"/path/to/file/audio.mp3"' \  --form 'model="voxtral-mini-2507"'

**With Language defined**

curl --location 'https://api.mistral.ai/v1/audio/transcriptions' \  --header "x-api-key: $MISTRAL_API_KEY" \  --form 'file=@"/path/to/file/audio.mp3"' \  --form 'model="voxtral-mini-2507"' \  --form 'language="en"'

### Passing an Audio URL[​](#passing-an-audio-url-1 "Direct link to Passing an Audio URL")

Similarly, you can provide an url of an audio file.

*   python
*   typescript
*   curl

import osfrom mistralai import Mistral# Retrieve the API key from environment variablesapi_key = os.environ["MISTRAL_API_KEY"]# Specify modelmodel = "voxtral-mini-latest"# Initialize the Mistral clientclient = Mistral(api_key=api_key)# Get the transcriptiontranscription_response = client.audio.transcriptions.complete(    model=model,    file_url="https://docs.mistral.ai/audio/obama.mp3",    ## language="en")# Print the content of the responseprint(transcription_response)

import { Mistral } from "@mistralai/mistralai";// Retrieve the API key from environment variablesconst apiKey = process.env["MISTRAL_API_KEY"];// Initialize the Mistral clientconst client = new Mistral({ apiKey: apiKey });// Get the transcriptionconst transcriptionResponse = await client.audio.transcriptions.complete({  model: "voxtral-mini-latest",  fileUrl: "https://docs.mistral.ai/audio/obama.mp3",  // language: "en"});// Log the content of the responseconsole.log(transcriptionResponse);

curl --location 'https://api.mistral.ai/v1/audio/transcriptions' \  --header "x-api-key: $MISTRAL_API_KEY" \  --form 'file_url="https://docs.mistral.ai/audio/obama.mp3"' \  --form 'model="voxtral-mini-2507"'

**With Language defined**

curl --location 'https://api.mistral.ai/v1/audio/transcriptions' \  --header "x-api-key: $MISTRAL_API_KEY" \  --form 'file_url="https://docs.mistral.ai/audio/obama.mp3"' \  --form 'model="voxtral-mini-2507"' \  --form 'language="en"'

### Passing an Uploaded Audio File[​](#passing-an-uploaded-audio-file-1 "Direct link to Passing an Uploaded Audio File")

Alternatively, you can first upload the file to our cloud service and then pass the signed URL instead.

*   python
*   typescript
*   curl

import osfrom mistralai import Mistral# Retrieve the API key from environment variablesapi_key = os.environ["MISTRAL_API_KEY"]# Specify modelmodel = "voxtral-mini-latest"# Initialize the Mistral clientclient = Mistral(api_key=api_key)# If local audio, upload and retrieve the signed urlwith open("local_audio.mp3", "rb") as f:    uploaded_audio = client.files.upload(        file={            "content": f,            "file_name": "local_audio.mp3",            },        purpose="audio"    )signed_url = client.files.get_signed_url(file_id=uploaded_audio.id)# Get the transcriptiontranscription_response = client.audio.transcriptions.complete(    model=model,    file_url=signed_url.url,    ## language="en")# Print the content of the responseprint(transcription_response)

import { Mistral } from "@mistralai/mistralai";import fs from "fs";// Retrieve the API key from environment variablesconst apiKey = process.env["MISTRAL_API_KEY"];// Initialize the Mistral clientconst client = new Mistral({ apiKey: apiKey });// If local document, upload and retrieve the signed urlconst uploaded_pdf = await client.files.upload({    file: {        fileName: "local_audio.mp3",        content: fs.readFileSync("local_audio.mp3"),        },    purpose: "audio",});const signedUrl = await client.files.getSignedUrl({    fileId: uploaded_pdf.id,});// Get the transcriptionconst transcriptionResponse = await client.audio.transcriptions.complete({    model: "voxtral-mini-latest",    fileUrl: signedUrl.url,    // language: "en"});// Log the content of the responseconsole.log(transcriptionResponse);

**Upload the Audio File**

curl --location https://api.mistral.ai/v1/files \  --header "Authorization: Bearer $MISTRAL_API_KEY" \  --form purpose="audio" \  --form file="@local_audio.mp3"

**Get the Signed URL**

curl --location "https://api.mistral.ai/v1/files/$id/url?expiry=24" \    --header "Accept: application/json" \    --header "Authorization: Bearer $MISTRAL_API_KEY"

**Send Transcription Request**

curl --location 'https://api.mistral.ai/v1/audio/transcriptions' \    --header "x-api-key: $MISTRAL_API_KEY" \    --form 'file_url="<signed_url>"' \    --form 'model="voxtral-mini-2507"'

**Send Transcription Request with Language defined**

curl --location 'https://api.mistral.ai/v1/audio/transcriptions' \    --header "x-api-key: $MISTRAL_API_KEY" \    --form 'file_url="<signed_url>"' \    --form 'model="voxtral-mini-2507"' \    --form 'language="en"'

**JSON Output**

{  "model":"voxtral-mini-2507",  "text":"This week, I traveled to Chicago to deliver my final farewell address to the nation, following in the tradition of presidents before me. It was an opportunity to say thank you. Whether we've seen eye to eye or rarely agreed at all, my conversations with you, the American people, in living rooms, in schools, at farms and on factory floors, at diners and on distant military outposts, All these conversations are what have kept me honest, kept me inspired, and kept me going. Every day, I learned from you. You made me a better President, and you made me a better man. Over the course of these eight years, I've seen the goodness, the resilience, and the hope of the American people. I've seen neighbors looking out for each other as we rescued our economy from the worst crisis of our lifetimes. I've hugged cancer survivors who finally know the security of affordable health care. I've seen communities like Joplin rebuild from disaster, and cities like Boston show the world that no terrorist will ever break the American spirit. I've seen the hopeful faces of young graduates and our newest military officers. I've mourned with grieving families searching for answers. And I found grace in a Charleston church. I've seen our scientists help a paralyzed man regain his sense of touch, and our wounded warriors walk again. I've seen our doctors and volunteers rebuild after earthquakes and stop pandemics in their tracks. I've learned from students who are building robots and curing diseases, and who will change the world in ways we can't even imagine. I've seen the youngest of children remind us of our obligations to care for our refugees. to work in peace, and above all, to look out for each other. That's what's possible when we come together in the slow, hard, sometimes frustrating, but always vital work of self-government. But we can't take our democracy for granted. All of us, regardless of party, should throw ourselves into the work of citizenship. Not just when there is an election. Not just when our own narrow interest is at stake. But over the full span of a lifetime. If you're tired of arguing with strangers on the Internet, try to talk with one in real life. If something needs fixing, lace up your shoes and do some organizing. If you're disappointed by your elected officials, then grab a clipboard, get some signatures, and run for office yourself. Our success depends on our participation, regardless of which way the pendulum of power swings. It falls on each of us to be guardians of our democracy. to embrace the joyous task we've been given to continually try to improve this great nation of ours. Because for all our outward differences, we all share the same proud title – citizen. It has been the honor of my life to serve you as President. Eight years later, I am even more optimistic about our country's promise. And I look forward to working along your side as a citizen for all my days that remain. Thanks, everybody. God bless you. And God bless the United States of America.",  "language":"en",  "segments":[],  "usage":{    "prompt_audio_seconds":203,    "prompt_tokens":4,    "total_tokens":3264,    "completion_tokens":635  }}

**Samples**

*   Obama

**Audio**

Your browser does not support the audio element.

**Transcription**
This week, I traveled to Chicago to deliver my final farewell address to the nation, following in the tradition of presidents before me. It was an opportunity to say thank you. Whether we've seen eye to eye or rarely agreed at all, my conversations with you, the American people, in living rooms, in schools, at farms and on factory floors, at diners and on distant military outposts, All these conversations are what have kept me honest, kept me inspired, and kept me going. Every day, I learned from you. You made me a better President, and you made me a better man. Over the course of these eight years, I've seen the goodness, the resilience, and the hope of the American people. I've seen neighbors looking out for each other as we rescued our economy from the worst crisis of our lifetimes. I've hugged cancer survivors who finally know the security of affordable health care. I've seen communities like Joplin rebuild from disaster, and cities like Boston show the world that no terrorist will ever break the American spirit. I've seen the hopeful faces of young graduates and our newest military officers. I've mourned with grieving families searching for answers. And I found grace in a Charleston church. I've seen our scientists help a paralyzed man regain his sense of touch, and our wounded warriors walk again. I've seen our doctors and volunteers rebuild after earthquakes and stop pandemics in their tracks. I've learned from students who are building robots and curing diseases, and who will change the world in ways we can't even imagine. I've seen the youngest of children remind us of our obligations to care for our refugees. to work in peace, and above all, to look out for each other. That's what's possible when we come together in the slow, hard, sometimes frustrating, but always vital work of self-government. But we can't take our democracy for granted. All of us, regardless of party, should throw ourselves into the work of citizenship. Not just when there is an election. Not just when our own narrow interest is at stake. But over the full span of a lifetime. If you're tired of arguing with strangers on the Internet, try to talk with one in real life. If something needs fixing, lace up your shoes and do some organizing. If you're disappointed by your elected officials, then grab a clipboard, get some signatures, and run for office yourself. Our success depends on our participation, regardless of which way the pendulum of power swings. It falls on each of us to be guardians of our democracy. to embrace the joyous task we've been given to continually try to improve this great nation of ours. Because for all our outward differences, we all share the same proud title – citizen. It has been the honor of my life to serve you as President. Eight years later, I am even more optimistic about our country's promise. And I look forward to working along your side as a citizen for all my days that remain. Thanks, everybody. God bless you. And God bless the United States of America.

**Language** English

## Transcription with Timestamps[​](#transcription-with-timestamps "Direct link to Transcription with Timestamps")

You can request timestamps for the transcription by passing the `timestamp_granularities` parameter, currently supporting `segment`.
It will return the start and end time of each segment in the audio file.

*   python
*   typescript
*   curl

import osfrom mistralai import Mistral# Retrieve the API key from environment variablesapi_key = os.environ["MISTRAL_API_KEY"]# Specify modelmodel = "voxtral-mini-latest"# Initialize the Mistral clientclient = Mistral(api_key=api_key)# Transcribe the audio with timestampstranscription_response = client.audio.transcriptions.complete(    model=model,    file_url="https://docs.mistral.ai/audio/obama.mp3",    timestamp_granularities=["segment"])# Print the contentsprint(transcription_response)

import { Mistral } from "@mistralai/mistralai";// Retrieve the API key from environment variablesconst apiKey = process.env["MISTRAL_API_KEY"];// Initialize the Mistral clientconst client = new Mistral({ apiKey: apiKey });// Transcribe the audio with timestampsconst transcriptionResponse = await client.audio.transcriptions.complete({  model: "voxtral-mini-latest",  fileUrl: "https://docs.mistral.ai/audio/obama.mp3",  timestamp_granularities: ["segment"]});// Log the contentsconsole.log(transcriptionResponse);

curl --location 'https://api.mistral.ai/v1/audio/transcriptions' \--header "x-api-key: $MISTRAL_API_KEY" \--form 'file_url="https://docs.mistral.ai/audio/obama.mp3"' \--form 'model="voxtral-mini-latest"' \--form 'timestamp_granularities="segment"'

**JSON Output**

{  "model": "voxtral-mini-2507",  "text": "This week, I traveled to Chicago to deliver my final farewell address to the nation, following in the tradition of presidents before me. It was an opportunity to say thank you. Whether we've seen eye to eye or rarely agreed at all, my conversations with you, the American people, in living rooms, in schools, at farms and on factory floors, at diners and on distant military outposts. All these conversations are what have kept me honest, kept me inspired, and kept me going. Every day, I learned from you. You made me a better President, and you made me a better man. Over the course of these eight years, I've seen the goodness, the resilience, and the hope of the American people. I've seen neighbors looking out for each other as we rescued our economy from the worst crisis of our lifetimes. I've hugged cancer survivors who finally know the security of affordable health care. I've seen communities like Joplin rebuild from disaster, and cities like Boston show the world that no terrorist will ever break the American spirit. I've seen the hopeful faces of young graduates and our newest military officers. I've mourned with grieving families searching for answers. And I found grace in a Charleston church. I've seen our scientists help a paralyzed man regain his sense of touch and our wounded warriors walk again. I've seen our doctors and volunteers rebuild after earthquakes and stop pandemics in their tracks. I've learned from students who are building robots and curing diseases and who will change the world in ways we can't even imagine. I've seen the youngest of children remind us of our obligations to care for our refugees. to work in peace, and above all, to look out for each other. That's what's possible when we come together in the slow, hard, sometimes frustrating, but always vital work of self-government. But we can't take our democracy for granted. All of us, regardless of party, should throw ourselves into the work of citizenship. Not just when there's an election. Not just when our own narrow interest is at stake. But over the full span of a lifetime. If you're tired of arguing with strangers on the Internet, try to talk with one in real life. If something needs fixing, lace up your shoes and do some organizing. If you're disappointed by your elected officials, then grab a clipboard, get some signatures, and run for office yourself. Our success depends on our participation, regardless of which way the pendulum of power swings. It falls on each of us to be guardians of our democracy. to embrace the joyous task we've been given to continually try to improve this great nation of ours. Because for all our outward differences, we all share the same proud title, citizen. It has been the honor of my life to serve you as president. Eight years later, I am even more optimistic about our country's promise, and I look forward to working along your side as a citizen for all my days that remain. Thanks, everybody. God bless you, and God bless the United States of America.",  "language": null,  "segments": [    {      "text": "This week, I traveled to Chicago to deliver my final farewell address to the nation, following",      "start": 0.8,      "end": 6.2    },    {      "text": "in the tradition of presidents before me.",      "start": 6.2,      "end": 9.0    },    {      "text": "It was an opportunity to say thank you.",      "start": 9.0,      "end": 11.8    },    {      "text": "Whether we've seen eye to eye or rarely agreed at all, my conversations with you, the American",      "start": 11.8,      "end": 17.6    },    {      "text": "people, in living rooms, in schools, at farms and on factory floors, at diners and on distant",      "start": 17.6,      "end": 24.9    },    {      "text": "military outposts.",      "start": 24.9,      "end": 26.6    },    {      "text": "All these conversations are what have kept me honest, kept me inspired, and kept me going.",      "start": 26.6,      "end": 32.8    },    {      "text": "Every day, I learned from you.",      "start": 32.8,      "end": 35.4    },    {      "text": "You made me a better President, and you made me a better man.",      "start": 35.4,      "end": 39.3    },    {      "text": "Over the course of these eight years, I've seen the goodness, the resilience, and the hope of the American people.",      "start": 39.3,      "end": 46.1    },    {      "text": "I've seen neighbors looking out for each other as we rescued our economy from the worst crisis of our lifetimes.",      "start": 46.1,      "end": 51.3    },    {      "text": "I've hugged cancer survivors who finally know the security of affordable health care.",      "start": 52.2,      "end": 56.5    },    {      "text": "I've seen communities like Joplin rebuild from disaster, and cities like Boston show the world that no terrorist will ever break the American spirit.",      "start": 57.1,      "end": 65.7    },    {      "text": "I've seen the hopeful faces of young graduates and our newest military officers.",      "start": 66.5,      "end": 71.1    },    {      "text": "I've mourned with grieving families searching for answers.",      "start": 71.7,      "end": 74.4    },    {      "text": "And I found grace in a Charleston church.",      "start": 75.2,      "end": 77.7    },    {      "text": "I've seen our scientists help a paralyzed man regain his sense of touch and our wounded warriors walk again.",      "start": 78.5,      "end": 85.2    },    {      "text": "I've seen our doctors and volunteers rebuild after earthquakes and stop pandemics in their tracks.",      "start": 85.9,      "end": 91.9    },    {      "text": "I've learned from students who are building robots and curing diseases and who will change the world in ways we can't even imagine.",      "start": 92.6,      "end": 99.2    },    {      "text": "I've seen the youngest of children remind us of our obligations to care for our refugees.",      "start": 100.1,      "end": 105.8    },    {      "text": "to work in peace, and above all, to look out for each other.",      "start": 106.6,      "end": 111.6    },    {      "text": "That's what's possible when we come together in the slow, hard, sometimes frustrating, but always vital work of self-government.",      "start": 111.6,      "end": 120.3    },    {      "text": "But we can't take our democracy for granted.",      "start": 120.3,      "end": 123.4    },    {      "text": "All of us, regardless of party, should throw ourselves into the work of citizenship.",      "start": 123.4,      "end": 129.2    },    {      "text": "Not just when there's an election.",      "start": 129.2,      "end": 131.2    },    {      "text": "Not just when our own narrow interest is at stake.",      "start": 131.2,      "end": 134.7    },    {      "text": "But over the full span of a lifetime.",      "start": 134.7,      "end": 138.1    },    {      "text": "If you're tired of arguing with strangers on the Internet,",      "start": 138.1,      "end": 141.4    },    {      "text": "try to talk with one in real life.",      "start": 141.4,      "end": 144.0    },    {      "text": "If something needs fixing,",      "start": 144.0,      "end": 146.0    },    {      "text": "lace up your shoes and do some organizing.",      "start": 146.0,      "end": 149.3    },    {      "text": "If you're disappointed by your elected officials, then grab a clipboard, get some signatures, and run for office yourself.",      "start": 149.3,      "end": 156.8    },    {      "text": "Our success depends on our participation, regardless of which way the pendulum of power swings.",      "start": 156.8,      "end": 165.3    },    {      "text": "It falls on each of us to be guardians of our democracy.",      "start": 165.3,      "end": 168.5    },    {      "text": "to embrace the joyous task we've been given to continually try to improve this great nation of ours.",      "start": 168.5,      "end": 174.6    },    {      "text": "Because for all our outward differences, we all share the same proud title, citizen.",      "start": 175.4,      "end": 181.7    },    {      "text": "It has been the honor of my life to serve you as president.",      "start": 182.7,      "end": 186.0    },    {      "text": "Eight years later, I am even more optimistic about our country's promise,",      "start": 186.9,      "end": 190.3    },    {      "text": "and I look forward to working along your side as a citizen for all my days that remain.",      "start": 190.3,      "end": 197.3    },    {      "text": "Thanks, everybody. God bless you, and God bless the United States of America.",      "start": 198.5,      "end": 203.4    }  ],  "usage": {    "prompt_audio_seconds": 203,    "prompt_tokens": 4,    "total_tokens": 3945,    "completion_tokens": 1316  }}

## FAQ[​](#faq "Direct link to FAQ")

*   **What's the maximum audio length?**

The maximum length will depend on the endpoint used, currently the limits are as follows:

*   ≈20 minutes for [Chat with Audio](#chat-with-audio) for both models.
*   ≈15 minutes for [Transcription](#transcription), longer transcriptions will be available soon.

tip

Here are some tips if you need to handle longer audio files:

*   **Divide the audio into smaller segments:** Transcribe each segment individually. However, be aware that this might lead to a loss of context, difficulties in splitting the audio at natural pauses (such as mid-sentence), and the need to combine the transcriptions afterward.
*   **Increase the playback speed:** Send the file at a faster pace by speeding up the audio. Keep in mind that this can reduce audio quality and require adjusting the transcription timestamps to align with the original audio file.

[

Previous

Vision

](/capabilities/vision/)[

Next

Reasoning

](/capabilities/reasoning/)

*   [Models with Audio Capabilities](#models-with-audio-capabilities)
*   [Chat with Audio](#chat-with-audio)
*   [Passing an Audio File](#passing-an-audio-file)
*   [Passing an Audio URL](#passing-an-audio-url)
*   [Passing an Uploaded Audio File](#passing-an-uploaded-audio-file)
*   [Transcription](#transcription)
*   [Passing an Audio File](#passing-an-audio-file-1)
*   [Passing an Audio URL](#passing-an-audio-url-1)
*   [Passing an Uploaded Audio File](#passing-an-uploaded-audio-file-1)
*   [Transcription with Timestamps](#transcription-with-timestamps)
*   [FAQ](#faq)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)