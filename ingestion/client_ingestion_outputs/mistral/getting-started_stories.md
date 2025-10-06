---
source: "website"
content_type: "blogs_resources"
url: "https://docs.mistral.ai/getting-started/stories/"
title: "/getting-started/stories/"
domain: "docs.mistral.ai"
path: "/getting-started/stories/"
scraped_time: "2025-09-08T18:10:24.575689"
url_depth: 2
word_count: 4214
---

Developer examples | Mistral AI

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
*   Developer examples

On this page

# Developer examples

## Model customization[​](#model-customization "Direct link to Model customization")

The following are developer examples from the startup community using our fine-tuning API. Check out our [fine-tuning doc](/capabilities/finetuning/finetuning_overview/) to learn the benefits of fine-tuning and how to use our fine-tuning API.

**RAG for internet retrieval**

# Phospho: RAG for internet retrieval

The video showcases the behavior of Tak. When a user inputs a query, Tak will use the LLM knowledge, a tool to search the web and a tool to fetch the news to generate the most relevant answer to the user query. Its behavior depends on the type of query by the user.

## Description[​](#description "Direct link to Description")

[Tak is a B2C internet search app](https://tak.phospho.ai/) powered by Mistral Large and other models with RAG and Function Calling.

In order to provide the most relevant answer to the user query, several function calls are performed to categorize the request (see diagram below). As the multiple agents are chained, ensuring consistently formatted outputs is crucial.

![Performance Metrics](/assets/images/tak_architecture_diagram-67dec15ab9bea191e3ef12d5214f6870.png)

## Company Description[​](#company-description "Direct link to Company Description")

At phospho, we developed the Tak chatbot as an experimental playground to test new phospho features and showcase the power of phospho analytics. A great thing is that you can use the data logged to phospho to finetune LLM models. We are [phospho](https://phospho.ai/), an open-source text analytics platform for LLM apps. Companies of all sizes use phospho to understand what users do with their LLM app and how well the app performs at the product level.

## Data[​](#data "Direct link to Data")

We used a dataset of user queries in Tak and the corresponding GPT-4-turbo function calls, collected and filtered through the phospho platform. We then divided the dataset into a _train_ set (70%), an _evaluation_ set (15%) and a test set (15%).

To determine the optimal training duration, we followed the rule of thumb that each token should be seen three times (in our case, 150 training steps, which is approximately 10 minutes).

For the learning rate, we used the suggested learning rate of 6e-5.

## Eval[​](#eval "Direct link to Eval")

To evaluate our fine-tuned model, we run inference of the test set of our dataset, then use binary classification metrics (Accuracy, Recall, F1 score). We test whether we were able to align the behavior of Mistral 7b to the classification behavior of OpenAI GPT-4-turbo, while maintaining the expected structured output. Indeed, we removed the function calling.

![Performance Metrics](/assets/images/performance_metrics-69f392d077eb121350b1895cfcf6d1a8.png)

Fine-tuning made Mistral 7B match the reference model, **increasing the F1 score from 20% to 78%**. Without fine-tuning, Mistral 7B achieved 87% accuracy and 20% recall on our classification task. With the fine-tuned model, we achieved 96% accuracy and 90% recall.

As we fine-tuned the model to only answer with `news_related` or `not_news_related`, we do not need to use function calling anymore. This led to a **34% decrease in the number of tokens used** excluding the user query, which further decreases costs.

## Conclusion[​](#conclusion "Direct link to Conclusion")

In conclusion, by combining phospho data collection and labeling with Mistral's fine-tuning services, we significantly enhanced our ability to deliver precise and relevant answers to user queries while decreasing cost. We have successfully aligned the behavior of Mistral 7B with GPT-4-turbo. This fine-tuning process not only ensures consistent output formatting but also reduces operational costs by minimizing token usage.

If you also want to improve your RAG agent, we encourage you to try fine tuning with Mistral using the data collected and labeled with phospho. This can lead to significant improvement on your user experience.

**RAG for medical domain**

# AmiRA (A miRNA Research Assistant)

## Company Information[​](#company-information "Direct link to Company Information")

[Myo](https://myo.fit) is building multimodal AI for brain health. Right now, we're exploring the relationship between microRNAs and various neurological conditions, including how these biomarkers can be utilized for early detection and monitoring of these diseases. AmiRA is an internal tool powered by Mistral's commercial and open-source models to help understand the functions of certain miRNA in sample results and their accompanying target genes.

## Description[​](#description "Direct link to Description")

This project demonstrates the fine tuning of mistral models and their use in a RAG system for:

1.  Disease association/prediction provided a given miRNA molecule
2.  Greater scientific accuracy and relevance when determining the function of miRNA molecules.

This project serves mainly as a proof-of-concept, showing that LLMs and agents can help us explore biomarkers and their relationships to health outcomes with proper engineering.

## Data and Training[​](#data-and-training "Direct link to Data and Training")

Titles and abstracts from 9839 PubMed were crawled. Three questions for each paper were then generated using the `mistral-large-latest` function calling API and traditional prompting. An example prompt is below:

def generate_questions(molecule, title, abstract): prompt = f"""     Based on the following molecule, title, and abstract, generate scientific questions to be     put in a function. Here is the information:\n\n     Molecule: {molecule}\nTitle: {title}\nAbstract: {abstract}     Ask your questions in a way that does not mention the abstract or the title of the work.     Treat information from the title/abstract as new/general knowledge, and   ask questions framed off of that.   """ response = MISTRAL_CLIENT.chat(     model=MISTRAL_MODEL,     messages=[ChatMessage(role="user", content=prompt)],     tools=tools,     tool_choice="any" ) return response

After questions were generated, answers for each question were then generated using mistral-large latest. An example prompt is below:

def generate_answer(molecule, title, abstract, question):     prompt = f"""         Based on the following molecule, title, and abstract, and question, generate an answer:         Molecule: {molecule}\nTitle: {title}\nAbstract: {abstract}\nQuestion: {question}\nAnswer:         Answer the question given only context information and not prior knowledge.         Answer in a way that does not mention the abstract or the title of the work.         Treat the provided information as general knowledge, and answer the questions         framed off of that.       """     response = MISTRAL_CLIENT.chat(         model=MISTRAL_MODEL,         messages=[ChatMessage(role="user", content=prompt)],     )     return response.choices[0].message.content.strip()

With multithreading on 2 CPU cores, question and answer generating took ~2.5 hours. Out of the original 9839 rows, 9414 made it past the data processing due to various errors.

This leaves us with ~28000 question/answer pairs to feed into the model for tuning. An example Q/A pair is below:

{"messages": [{"role": "user", "content": "What is the role of hsa-miR-335-5p in the development of type 2 diabetes mellitus (T2DM) and which genes does it potentially regulate?"}, {"role": "assistant", "content": "The role of hsa-miR-335-5p in the development of type 2 diabetes mellitus (T2DM) is that it potentially regulates the expression of various candidate genes. These genes include procollagen C-endopeptidase enhancer 2, connective tissue growth factor, family with sequence similarity 105, member A, protein phosphatase 1 regulatory inhibitor subunit 1A, and C-C motif chemokine receptor 4. The specific mechanisms through which hsa-miR-335-5p regulates these genes and contributes to the development of T2DM are not detailed in the provided information. However, it is suggested that understanding these regulatory networks could potentially be useful for the molecular diagnosis and targeted therapy of T2DM."}]}

## "RAG" Pipeline[​](#rag-pipeline "Direct link to \"RAG\" Pipeline")

A simple table lookup (Pandas Dataframe) was used to surface relevant information about each miRNA present in query strings, and whole abstracts were fed into the model. N of results was never more than 12, and the context window limit was never reached.

![](/assets/images/rag-c8437b8e5a8aa997d26e680ce0c07f2c.png)

Embeddings for each paper and title abstract were prepopulated and stored in the dataframe, and cosine similarity was used to surface the top-_**k**_ most relevant papers before feeding into the model. The number of results fed into the model varied depending on the number of entries present for each molecule. (ie. if there is only 1 entry, k will equal 1. If there are 30 entries, get the best 12 via cosine similarity.)

The model also has the option to take the raw query and perform lookups in the dataframe to gather more information or context at it's own discretion.

## Benchmarking and results[​](#benchmarking-and-results "Direct link to Benchmarking and results")

For disease association and prediction, 150 random questions from a miRNA disease association [benchmarking paper published in 2019](https://pubmed.ncbi.nlm.nih.gov/31594544/) were sampled. This dataset was completely separate from any training data used or any PubMed papers crawled to create the training data.

The fine-tuned model outperformed both `mistral-small-latest` and `mistral-large-latest` in question answering, without explicitly seeing any data affiliated to the benchmark. Values below are the averages across 3 attempts.

![](/assets/images/test-0d79db91165a73445cad786c057601f2.png)

One of the benefits of fine-tuning is that you can achieve better performnance with smaller, and therefore faster, models. Below is the average latency for each API call for the same three runs above.

![](/assets/images/latency-3b8aa2e4d6420e3921c6e5d076c4681f.png)

## Example responses[​](#example-responses "Direct link to Example responses")

The purpose of the finetuning model is not to be a test taker, but to provide better context for RAG systems, so it's natural to want to evaluate the actual outputs of the model in use. Below are two examples of the fine-tuned model's output compared to similar outputs `mistral-large-latest` and `mistral-small-latest`. In situations where the model was forced to "guess" the answer to a question, it gave correct context from it's own knowledge, based off of information it gathered from papers included in its training.

mistral-finetune

mistral-small-latest

Letter: D: gastrointestinal neoplasms -- This is based on the information provided in the context that hsa-miR-106a-5p is identified as one of the key miRNAs associated with the regulation of hub genes in SARS-CoV-2 infections. However, a direct association with gastrointestinal neoplasms is not explicitly mentioned. The option D: gastrointestinal neoplasms is chosen as hsa-miR-106a has been previously reported in literature to be associated with various types of cancers, including colorectal cancer, which falls under gastrointestinal neoplasms. [Pubmed paper related to this response](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10451182/#:~:text=2.1.%20Colorectal%20Cancer,metastases%20%5B12%5D.)

vascular disease -- Letter: A, B, C, or D not mentioned in the context, so I can't definitively answer. However, hsa-let-7e has been associated with various diseases including some types of cancer, but the context provided doesn't specify its association with any of the listed diseases.

mistral-finetune

mistral-large-latest

Letter: D: hypertension (This is an educated guess as the context does not explicitly mention hsa-mir-146b being associated with any of the provided diseases. However, hsa-mir-146b has been studied in relation to hypertension in the literature.) [Pubmed paper related to this response](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6941490/#:~:text=Increased%20miR%2D146b%2D5p%20abundance%20has%20been%20reported%20in%20clinical%20studies%20of%20renal%20pathology%20and%20experimental%20disease%20models%3B%20including%20hypertension%2C%20AKI%2C%20renal%20fibrosis%2C%20and%20CKD.)

I'm sorry for any confusion, but the provided context does not contain any specific information linking hsa-mir-23b to a particular disease. Therefore, I'm unable to provide a precise answer based on the given options. If I were to make an educated guess without additional information, it would not be reliable or accurate. I recommend further research or consultation with a medical professional or a relevant database for the most accurate information.

**Financial advisor conversational assistant**

# Cleo: Financial assistant

## Company Description[​](#company-description "Direct link to Company Description")

Cleo is an AI fintech, building a financial assistant that helps its users navigate the complexity of their financial life.

## Data[​](#data "Direct link to Data")

Using an internal dataset consisting of user requests and Cleo responses crafted by Cleo's Content Design team.

## Eval[​](#eval "Direct link to Eval")

Human evaluation by the Content Design team.

The objective was simple: A translator from dry, factual, generated language to the playful Tone of Voice of Cleo. For that, we fine-tuned Mistral using La Plateforme on company data that have been crafted and evaluated by the Content Design team. The goal was to lift the writing style that is characteristic of Cleo and its brand.
For example a typical message to our users could be:

"Your Cleo Plus subscription payment didn't go through, so no cash advance for now, Nikos."

However, using the fine-tuned model, we can get more playful responses:

curl -s -XPOST 'https://api.mistral.ai/v1/chat/completions' \  -H "Authorization: Bearer $MISTRAL_API_KEY" \  -H 'Content-Type: application/json' \  -d '{  "model": "ft:open-mistral-7b:...",  "messages": [    {      "role": "user",      "content": "Your Cleo Plus subscription payment didn't go through, so no cash advance for now, Nikos."    }  ],  "temperature": 0.0,  "top_p": 1,  "max_tokens": 512,  "stream": false,   "safe_prompt": false,  "random_seed": 42}'

{  "id": "d43ba5cf228a43ff9bf27ed8fb403292",  "object": "chat.completion",  "created": 1717417588,  "model": "ft:open-mistral-7b:...",  "choices": [    {      "index": 0,      "message": {        "role": "assistant",        "content": "Oh darling Nikos, it seems your Cleo Plus payment has taken a little vacay, so no jingle in the pocket for a cash advance at the moment, love. Don't you worry, just give it a little nudge and we'll get you sorted in no time! 💃🏼💸",        "tool_calls": null      },      "finish_reason": "stop",      "logprobs": null    }  ]}

We get a response more characteristic of Cleo’s brand.

"Oh darling Nikos, it seems your Cleo Plus payment has taken a little vacay, so no jingle in the pocket for a cash advance at the moment, love. Don't you worry, just give it a little nudge and we'll get you sorted in no time! 💃🏼💸"

Getting a response that corresponds more to our brand.

**Legal copilot**

# Jimini AI: Legal copilot

_Video 1: Integration of the Mistral fine-tuned models into our product [Jimini Analyzer](https://jimini.ai/)._

The video begins by showcasing the integration of the fine-tuned model on [BSARD](https://arxiv.org/pdf/2108.11792) into our legal document analysis tool. In contrast to the base model, the fine-tuned version **accurately lists the relevant legal articles** in Markdown format, providing a clear and concise overview of the applicable laws.

The remainder of the video highlights the integration of the fine-tuned template on [Multi EURLEX](https://arxiv.org/pdf/2109.00904) into our legal translation tool, resulting in more precise translations of complex legal terminology, such as "_Gerichtsgesetzbuch_'' for "_Code judiciaire_". This enhancement ensures that our translations **accurately reflect the intended legal meaning, ultimately providing greater value to our clients**.

## Description[​](#description "Direct link to Description")

As we are building a legal copilot, fine-tuning a model presents several interests for us :

*   _**It can teach the model to generate responses in a specific format and tone.**_

To ensure that our legal copilot outputs reliable, well-sourced and professionally formatted legal answers, we've fine-tuned the `mistral-small` model, focusing on **improving response structure and sourcing**.

For this first use-case, demonstrated on the [_BSARD_](https://arxiv.org/pdf/2108.11792) dataset, we employ **distillation** from the smarter `mistral-large` model. This approach **reduces costs**, saves tokens (no need for a complex prompt anymore) and **decreases latency** by using a small, efficient and fine-tuned model.

*   _**It can also be used to specialize the model for a specific topic or domain to improve its performance on domain-specific tasks, such as the legal translation.**_

Our **strong European roots** and commitment to our European clients drive us to excel in French-German legal translation. By harnessing the strong multilingual abilities of `mistral-small` and fine-tuning it further specifically for legal terms on the [Multi EURLEX](https://arxiv.org/pdf/2109.00904) dataset, we significantly improved the translation of legal terminology.

## Company description[​](#company-description "Direct link to Company description")

At [Jimini AI](https://jimini.ai/), we are dedicated to creating a **cutting-edge legal copilot**, designed to assist legal professionals in automating their most tedious and time-consuming tasks, such as the legal research or the translation of legal documents. Gaining access to [Mistral AI](https://mistral.ai/)'s fine-tuning API presented us with an ideal opportunity to focus on two of our key use-cases.

## BSARD[​](#bsard "Direct link to BSARD")

### Data[​](#data "Direct link to Data")

We used the [Belgian Statutory Article Retrieval Dataset (BSARD)](https://aclanthology.org/2022.acl-long.468/), a comprehensive French dataset for examining legal information retrieval, to fine-tune `mistral-small-latest` and improve the legal accuracy and quality of its answers. It encompasses over 22,600 statutory articles derived from Belgian law along with approximately 1,100 legal inquiries.

We created a synthetic _Question Answering_ (QA) dataset by utilizing the `mistral-large-latest` model to generate ground truth answers based on expertly crafted guidelines, which were meticulously developed **in collaboration with legal professionals**. We then divided the dataset into a _train_ set (80%) and an _evaluation_ set (20%).

To determine the optimal training duration, we followed the rule of thumb that each token should be seen three times (in our case, 220 training steps, which is approximately 30 minutes).

To tune the `learning_rate`, we opted to measure third-party and more generic capabilities than legal criteria to ensure that the model does not regress due to catastrophic forgetting. To this end, we evaluated the model's performance using the [faithfulness](https://docs.ragas.io/en/stable/concepts/metrics/faithfulness.html) and [relevancy](https://docs.ragas.io/en/stable/references/metrics.html#ragas.metrics.AnswerRelevancy) metrics from [RAGAS](https://arxiv.org/abs/2309.15217) on a proprietary _generalist_ dataset.

![RAGAS evaluation on BSARD](/assets/images/results_bsard-90697f350dcaeae8a85ed00359546a3e.png) _Figure 1: RAGAS based evaluation of Faithfulness and Answer relevancy of the `mistral-small-latest` and `mistral-small-fine-tuned` models for different learning rates and different number of steps._

​​We have therefore selected a `learning_rate` of `1e-6`, for which we observe a slight improvement compared to `mistral-small-latest`, as well as a balance between the two criteria. Thus, there does not appear to be any regression of the model's general capabilities.

In addition to this initial sanity check, we used the very useful integration of the Mistral AI fine-tuning endpoint’s with [Weights & Biases](https://wandb.ai/site) to monitor our trainings, and we have notably measured the evolution of the model's `perplexity`, which seems to effectively converge under this training regime (where each token is seen 3 times).

![BSARD training curves](/assets/images/bsard_curves-e7094624b19115973d3a05445d535fb3.png) _Figure 2: Perplexity and eval loss during the fine-tuning on BSARD monitored in _Weights & Biases_._

### Eval[​](#eval "Direct link to Eval")

To evaluate the effectiveness of our fine-tuning process, we employed the _LLM-as-a-Judge_ methodology. Specifically, we drew inspiration from the additive scale approach developed by [Yuan et al](https://arxiv.org/abs/2401.10020). and recently utilized for the [FineWeb-Edu dataset constitution](https://huggingface.co/spaces/HuggingFaceFW/blogpost-fineweb-v1). We then adapted the methodology by transforming it into a preference score system, denoted in the following by `legal_quality` :

Given the following two answers, compare them based on the following criteria:- Explicit, accurate citation of the relevant legal article(s), such as "d'après l'article 123 du Code Civil". Implicit (such as "d'après l'extrait fourni") or general references (such as "d'après le Code Civil") are not accepted.- Clear, logical argumentation of each stated element, including the precise identifier of the corresponding legal article.- Well-structured answer with Markdown formatting, clear writing, and no ambiguities. Source references are required.---For each criterion, assign a point to the answer that best satisfies the criterion. If both answers are equal, assign 1 point to both. Be strict; if no answer perfectly meets a criterion, do not award a point. Briefly justify your total score in up to 100 words. Conclude with the score of each answer as an integer between 0 and 3.Return the information in JSON format following this schema:{    "justification": "string",    "score_answer_1": int,    "score_answer_2": int}Question :{question}Answer 1:{answer_1}Answer 2:{answer_2}JSON:

These criteria were meticulously established and fine-tuned based on the feedback of multiple legal experts.

We conducted a rigorous evaluation of several candidate `Judge LLMs`, including `gpt-3.5-turbo`, `mixtral`, and `mistral-large`. The results of our analysis revealed that `mistral-large` demonstrated the highest correlation with the experts' preferences, and was therefore selected as the `Judge LLM`.

### Results[​](#results "Direct link to Results")

![BSARD evaluation on legal quality](/assets/images/legal_quality-f4dfdc7e2bad6a1f9d766102099533b0.png) _Figure 3: LLM-as-a-judge evaluation of `mistral-small-latest` and `mistral-small-finetuned` based on the legal quality of their answers._

We observe a significant improvement, with a score increase from 1.42 to 1.73, representing a **20% enhancement!**

This progress is also noticeable in practical applications. The example demonstrated in the video serves as evidence of this improvement: _(For the non-French readers, we have translated the original French answers into English)_

**Question :**

What are the risks if I stop paying my consumer credit?

**`mistral-small-finetuned` answer:**

If you stop paying your consumer credit, you face several consequences:1. Payment deadline and suspension of proceedings: The judge may grant moderate payment deadlines and suspend proceedings (Art. 1244, Civil Code).2. Payment facilities: You can request payment facilities from the justice of the peace, but only after the creditor has refused to grant these facilities. This procedure is governed by articles 1337bis to 1337octies of the Judicial Code.3. Forfeiture of the term or resolutory condition: If you do not comply with the payment terms and the contract provides for it, the creditor may declare the forfeiture of the term or the resolutory condition. However, the conditions of forfeiture of the term or resolutory condition are strictly regulated by article VII.105 of the Economic Law Code. For example, a forfeiture of the term or resolutory condition clause can only be applied if you are in default of payment of at least two term amounts or a sum equivalent to 20% of the total amount due.4. Penalties and late interest: In case of late payment, the creditor may claim the outstanding and unpaid capital, the outstanding and unpaid amount of the total cost of credit for the consumer, the amount of the agreed late interest calculated on the outstanding and unpaid capital, and the agreed fees for reminder letters and formal notices (Art. VII.106, Economic Law Code).5. Repossession of the financed asset: If the financed asset is subject to a retention of title clause or a promise of pledge with an irrevocable mandate, the creditor may repossess the asset if you do not meet your payment obligations. However, if you have already paid 40% or more of the cash price of the asset, it cannot be repossessed except by court decision or a written agreement concluded after formal notice by registered mail (Art. VII.108, Economic Law Code).

**`mistral-small-latest` answer:**

If you continue to not pay, this may lead to the termination of the contract or the forfeiture of the term. In this case, the creditor can claim the remaining balance, the total cost of credit for the consumer, and penalties or compensation within certain limits. Finally, if the situation persists, the creditor may initiate recovery procedures, which may include wage garnishment or seizure of your bank account. Your financial situation could then deteriorate significantly.

The answer from `mistral-small-finetuned` is clear and well-structured, supported by precise legal references, whereas the response from `mistral-small-latest` is not.

## Multi EURLEX[​](#multi-eurlex "Direct link to Multi EURLEX")

### Data[​](#data-1 "Direct link to Data")

To enhance our legal translation tool, we have also fine-tuned `mistral-small-latest` on legal documents. For this purpose, we selected a subset of the [Multi EURLEX](https://arxiv.org/pdf/2109.00904) dataset, which consists of 35,000 European legal documents in French translated into German.

![Multi EURLEX training curves](/assets/images/eurlex_curves-06f443c4dd6bbee9554c82d5e1a82a65.png)

_Figure 4: Perplexity and eval loss during the fine-tuning on Multi EURLEX monitored in _Weights & Biases_._

### Eval[​](#eval-1 "Direct link to Eval")

In order to evaluate the fine-tuned model on relevant examples for our use cases, we selected 50 texts containing complex legal terms to be translated from French to German (such as _"Clause de non-concurrence"_, which is sometimes translated as _"Nicht-Konkurrenz-Klausel"_ instead of _"Wettbewerbsverbotsklausel"_).

We then submitted the triplets (`example`, `mistral_base_translation`, `mistral_finetuned_translation`) blindly to a bilingual legal expert, who selected the most accurate legal translation for each example.

### Results[​](#results-1 "Direct link to Results")

The legal expert preferred the legal translation of the fine-tuned model in 38 / 50 cases, with 9 cases tied. Thus, the fine-tuned model is **better or at least as good as the base model in 94% of cases**.

Example

`mistral-small-latest`

`mistral-small-finetuned`

Le vice de procédure a conduit à l'annulation du jugement.

Die Prozessirregularität führte zur Aufhebung des Urteils.

Der Verfahrensmangel hat zur Nichtigkeit des Urteils geführt.

_Table 1: Comparison of `mistral-small-latest` and its fine-tuned counterpart on Multi EURLEX. The fine-tuned model uses "Verfahrensmangel" and "Nichtigkeit des Urteils", which are the precise and correct legal terms._

## Conclusion[​](#conclusion "Direct link to Conclusion")

Our initial tests fine-tuning the `mistral-small` model using Mistral AI's endpoint have yielded promising results. **The fine-tuned model excels in generating structured, well-sourced responses and accurately translating complex legal terms**, demonstrating its potential for specialized legal applications.

The fast fine-tuning capability and _Weights & Biases_ integration made the process efficient and straightforward, allowing us to **develop cost-effective, specialized models quickly**.

We will further enhance our results by collaborating closely with our lawyer customers to refine the models' performance. Additionally, we plan to expand use cases to include legal summarization, contract analysis, and legal drafting.

We extend our thanks to Mistral AI for allowing us to test their fine-tuning API as beta testers. The Mistral AI fine-tuning endpoint has proven to be an invaluable tool for our legal AI development - these experiments were just the beginning!

## References[​](#references "Direct link to References")

*   BSARD : [paper](https://arxiv.org/abs/2108.11792)
*   FineWeb-Edu : [blogpost](https://huggingface.co/spaces/HuggingFaceFW/blogpost-fineweb-v1)
*   Multi EURLEX : [paper](https://arxiv.org/pdf/2109.00904)
*   RAGAS : [paper](https://arxiv.org/abs/2309.15217) & [library](https://github.com/explodinggradients/ragas)
*   Self-Rewarding Language Model, _Yuan et al._ : [paper](https://arxiv.org/abs/2401.10020)
*   Weights & Biases : [website](https://wandb.ai/site)

[

Previous

Model customization

](/getting-started/customization/)[

Next

Changelog

](/getting-started/changelog/)

*   [Model customization](#model-customization)
*   [Description](#description)
*   [Company Description](#company-description)
*   [Data](#data)
*   [Eval](#eval)
*   [Conclusion](#conclusion)
*   [Company Information](#company-information)
*   [Description](#description)
*   [Data and Training](#data-and-training)
*   ["RAG" Pipeline](#rag-pipeline)
*   [Benchmarking and results](#benchmarking-and-results)
*   [Example responses](#example-responses)
*   [Company Description](#company-description)
*   [Data](#data)
*   [Eval](#eval)
*   [Description](#description)
*   [Company description](#company-description)
*   [BSARD](#bsard)
*   [Data](#data)
*   [Eval](#eval)
*   [Results](#results)
*   [Multi EURLEX](#multi-eurlex)
*   [Data](#data-1)
*   [Eval](#eval-1)
*   [Results](#results-1)
*   [Conclusion](#conclusion)
*   [References](#references)

Documentation

*   [Documentation](/)
*   [Contributing](/guides/contribute/overview/)

Community

*   [Discord](https://discord.gg/mistralai)
*   [X](https://twitter.com/M