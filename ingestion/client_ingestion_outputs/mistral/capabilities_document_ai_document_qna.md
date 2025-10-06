---
source: "website"
content_type: "services_products"
url: "https://docs.mistral.ai/capabilities/document_ai/document_qna/"
title: "/capabilities/document_ai/document_qna/"
domain: "docs.mistral.ai"
path: "/capabilities/document_ai/document_qna/"
scraped_time: "2025-09-08T18:09:54.606351"
url_depth: 3
word_count: 758
---

Document QnA | Mistral AI

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

*   [Basic OCR](/capabilities/document_ai/basic_ocr/)
*   [Annotations](/capabilities/document_ai/annotations/)
*   [Document QnA](/capabilities/document_ai/document_qna/)
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
*   [Document AI](/capabilities/document_ai/document_ai_overview/)
*   Document QnA

On this page

# Document AI QnA

The Document QnA capability combines OCR with large language model capabilities to enable natural language interaction with document content. This allows you to extract information and insights from documents by asking questions in natural language.

**The workflow consists of two main steps:**

![Document QnA Graph](/img/document_qna.png)

1.  Document Processing: OCR extracts text, structure, and formatting, creating a machine-readable version of the document.

2.  Language Model Understanding: The extracted document content is analyzed by a large language model. You can ask questions or request information in natural language. The model understands context and relationships within the document and can provide relevant answers based on the document content.

**Key capabilities:**

*   Question answering about specific document content
*   Information extraction and summarization
*   Document analysis and insights
*   Multi-document queries and comparisons
*   Context-aware responses that consider the full document

**Common use cases:**

*   Analyzing research papers and technical documents
*   Extracting information from business documents
*   Processing legal documents and contracts
*   Building document Q&A applications
*   Automating document-based workflows

The examples below show how to interact with a PDF document using natural language:

*   python
*   typescript
*   curl

import osfrom mistralai import Mistral# Retrieve the API key from environment variablesapi_key = os.environ["MISTRAL_API_KEY"]# Specify modelmodel = "mistral-small-latest"# Initialize the Mistral clientclient = Mistral(api_key=api_key)# If local document, upload and retrieve the signed url# uploaded_pdf = client.files.upload(#     file={#         "file_name": "uploaded_file.pdf",#         "content": open("uploaded_file.pdf", "rb"),#     },#     purpose="ocr"# )# signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)# Define the messages for the chatmessages = [    {        "role": "user",        "content": [            {                "type": "text",                "text": "what is the last sentence in the document"            },            {                "type": "document_url",                "document_url": "https://arxiv.org/pdf/1805.04770"                # "document_url": signed_url.url            }        ]    }]# Get the chat responsechat_response = client.chat.complete(    model=model,    messages=messages)# Print the content of the responseprint(chat_response.choices[0].message.content)# Output: # The last sentence in the document is:\n\n\"Zaremba, W., Sutskever, I., and Vinyals, O. Recurrent neural network regularization. arXiv:1409.2329, 2014.

import { Mistral } from "@mistralai/mistralai";// import fs from 'fs';// Retrieve the API key from environment variablesconst apiKey = process.env["MISTRAL_API_KEY"];const client = new Mistral({  apiKey: apiKey,});// If local document, upload and retrieve the signed url// const uploaded_file = fs.readFileSync('uploaded_file.pdf');// const uploaded_pdf = await client.files.upload({//     file: {//         fileName: "uploaded_file.pdf",//         content: uploaded_file,//     },//     purpose: "ocr"// });// const signedUrl = await client.files.getSignedUrl({//     fileId: uploaded_pdf.id,// });const chatResponse = await client.chat.complete({  model: "mistral-small-latest",  messages: [    {      role: "user",      content: [        {          type: "text",          text: "what is the last sentence in the document",        },        {          type: "document_url",          documentUrl: "https://arxiv.org/pdf/1805.04770",          // documentUrl: signedUrl.url        },      ],    },  ],});console.log("JSON:", chatResponse.choices[0].message.content);

**Upload the Image File**

curl https://api.mistral.ai/v1/files \  -H "Authorization: Bearer $MISTRAL_API_KEY" \  -F purpose="ocr" \  -F file="@uploaded_file.pdf"

**Get the Signed URL**

curl -X GET "https://api.mistral.ai/v1/files/$id/url?expiry=24" \     -H "Accept: application/json" \     -H "Authorization: Bearer $MISTRAL_API_KEY"

**Chat Completion**

curl https://api.mistral.ai/v1/chat/completions \  -H "Content-Type: application/json" \  -H "Authorization: Bearer ${MISTRAL_API_KEY}" \  -d '{    "model": "mistral-small-latest",    "messages": [      {        "role": "user",        "content": [          {            "type": "text",            "text": "what is the last sentence in the document"          },          {            "type": "document_url",            "document_url": "<url>"          }        ]      }    ],    "document_image_limit": 8,    "document_page_limit": 64  }'

## Cookbooks[​](#cookbooks "Direct link to Cookbooks")

For more information on how to make use of Document QnA, we have the following [Document QnA Cookbook](https://colab.research.google.com/github/mistralai/cookbook/blob/main/mistral/ocr/document_understanding.ipynb) with a simple example.

## FAQ[​](#faq "Direct link to FAQ")

**Q: Are there any limits regarding the Document QnA API?**
A: Yes, there are certain limitations for the Document QnA API. Uploaded document files must not exceed 50 MB in size and should be no longer than 1,000 pages.

[

Previous

Annotations

](/capabilities/document_ai/annotations/)[

Next

Coding

](/capabilities/code_generation/)

*   [Cookbooks](#cookbooks)
*   [FAQ](#faq)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/MistralAI)
*   [GitHub](https://github.com/mistralai)

Copyright © 2025 Mistra