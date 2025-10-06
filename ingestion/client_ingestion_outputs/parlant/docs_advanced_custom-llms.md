---
source: "website"
content_type: "other"
url: "https://parlant.io/docs/advanced/custom-llms"
title: "/docs/advanced/custom-llms"
domain: "parlant.io"
path: "/docs/advanced/custom-llms"
scraped_time: "2025-09-08T19:58:47.587342"
url_depth: 3
word_count: 2110
---

Custom NLP Models | Parlant

[Skip to main content](#__docusaurus_skipToContent_fallback)

[Introducing Parlant 3.0](/blog/parlant-3-0-release)

— our most significant overhaul.

Dismiss

[

![Parlant's logo](/logo/logo-full.png)![Parlant's logo](/logo/logo-full.png)

](/)

Docs

[Install](/docs/quickstart/installation)[Learn](/docs/quickstart/motivation)[Blog](/blog)[About](/docs/about)[Need Help?](/contact)

![](/img/icons/search.svg)

![](/img/icons/search.svg)Search

![](/img/icons/menu.svg)

[![](/img/icons/x.svg)](https://x.com/EmcieCo)[![](/img/icons/discord.svg)](https://discord.gg/duxWqxKk6J)

[![github](/img/icons/github.svg)**Star**](https://github.com/emcie-co/parlant)[**\--**](https://github.com/emcie-co/parlant)

* * *

* * *

[

![Parlant's logo](/logo/logo-full.png)![Parlant's logo](/logo/logo-full.png)

](/)

*   [Install](/docs/quickstart/installation)
*   [Learn](/docs/quickstart/motivation)
*   [Blog](/blog)
*   [About](/docs/about)
*   [Need Help?](/contact)

* * *

[![](/img/icons/x.svg)](https://x.com/EmcieCo)[![](/img/icons/discord.svg)](https://discord.gg/duxWqxKk6J)

*   [Quick Start](/docs/quickstart/installation)

*   [Installation](/docs/quickstart/installation)
*   [Motivation](/docs/quickstart/motivation)
*   [Healthcare Agent Example](/docs/quickstart/examples)
*   [Components](/docs/concepts/sessions)

*   [Sessions](/docs/concepts/sessions)
*   [Entities](/docs/concepts/entities/agents)

*   [Agents](/docs/concepts/entities/agents)
*   [Customers](/docs/concepts/entities/customers)
*   [Behavior Modeling](/docs/concepts/customization/journeys)

*   [Journeys](/docs/concepts/customization/journeys)
*   [Guidelines](/docs/concepts/customization/guidelines)
*   [Relationships](/docs/concepts/customization/relationships)
*   [Tools](/docs/concepts/customization/tools)
*   [Retrievers](/docs/concepts/customization/retrievers)
*   [Glossary](/docs/concepts/customization/glossary)
*   [Variables](/docs/concepts/customization/variables)
*   [Canned Responses](/docs/concepts/customization/canned-responses)
*   [Production](/docs/category/production)

*   [Agentic Design Methodology](/docs/production/agentic-design)
*   [User-Input Moderation](/docs/production/input-moderation)
*   [Human Handoff](/docs/production/human-handoff)
*   [API Hardening](/docs/production/api-hardening)
*   [Custom Frontend](/docs/production/custom-frontend)
*   [Advanced Topics](/docs/advanced/engine-extensions)

*   [Engine Extensions](/docs/advanced/engine-extensions)
*   [Custom NLP Models](/docs/advanced/custom-llms)
*   [Enforcement & Explainability](/docs/advanced/explainability)
*   [Contributing to Parlant](/docs/advanced/contributing)
*   [Engine Internals](/docs/engine-internals/overview)

*   [REST API Reference](/docs/api/create-agent)

*   [About Parlant](/docs/about)

*   [](/)
*   Advanced Topics
*   Custom NLP Models

On this page

# Custom NLP Models

## Custom NLP Models[​](#custom-nlp-models-1 "Direct link to Custom NLP Models")

Once you've understood the basic of setting up [engine extensions](/docs/advanced/engine-extensions), you can integrate other NLP models into Parlant.

A Note on Custom Models

Parlant was optimized to work with the built-in LLMs, so using other models may require additional configuration and testing.

In particular, please note that Parlant uses some complex output JSON schemas in its operation. This means that you either need a powerful model that can handle complex outputs, or, alternatively, that you use a smaller model (SLM) that has been fine-tuned on Parlant data specifically, using a larger model as a teacher.

Using smaller models is actually a great way to reduce costs, latency—and sometimes even accuracy—in production environments.

![get-in-touch](/img/get-in-touch-button-icon.svg)Help me train Parlant SLMs

## Understanding `NLPService`[​](#understanding-nlpservice "Direct link to understanding-nlpservice")

Whether you want to use a different model from a supported built-in provider, or an entirely different provider, you can do so by creating a custom `NLPService` implementation.

An `NLPService` has 3 key components:

1.  **Schematic Generators**: These are used to generate structured content based on prompts.
2.  **Embedders**: These are used to create vector representations of text for semantic retrieval.
3.  **Moderation Service**: This is used to filter out harmful or inappropriate user input in conversations.

Reference Example

You can take a look at the official [`OpenAIService`](https://github.com/emcie-co/parlant/blob/main/src/parlant/adapters/nlp/openai_service.py) for a production-ready reference implementation of an `NLPService`.

### Schematic Generation[​](#schematic-generation "Direct link to Schematic Generation")

Throughout the Parlant engine, you'll find references to `SchematicGenerator[T]` objects. These are objects that generate [Pydantic](https://docs.pydantic.dev/latest/) models using instructions in a provided prompt. Behind the scenes, they always use LLMs to generate JSON schemas that in turn are converted to Pydantic models.

All LLM requests in Parlant are actually made using these schematic generators, which means that, whatever model you use, it must be able to generate valid JSON schemas consistently. This is the only requirement for a model in Parlant.

Let's now look at a few important interfaces that you need to implement in your custom NLP service.

#### Estimating Tokenizers[​](#estimating-tokenizers "Direct link to Estimating Tokenizers")

The `EstimatingTokenizer` interface is used to estimate the number of tokens in a prompt. This is important for managing costs and rate limits when using LLM APIs. It's also used in embedding models, where Parlant needs to chunk the input text into smaller parts to fit within the model's context window.

The reason it's called "estimating" is because not all model APIs provide exact token counts.

class EstimatingTokenizer(ABC):    """An interface for estimating the token count of a prompt."""    @abstractmethod    async def estimate_token_count(self, prompt: str) -> int:        """Estimate the number of tokens in the given prompt."""        ...

![get-in-touch](/img/get-in-touch-button-icon.svg)Help me implement this

For example, with `OpenAI`, you can implement this to use the `tiktoken` library to get accurate token counts for GPT models, or estimated token counts for other popular models.

#### Schematic Generators[​](#schematic-generators "Direct link to Schematic Generators")

Now let's look at the `SchematicGenerator[T]` interface itself, which is used to generate structured content based on a prompt.

Each generation result from a `SchematicGenerator[T]` contains not just the generated object, but also additional metadata about the generation process. Here's what it looks like:

@dataclass(frozen=True)class SchematicGenerationResult(Generic[T]):    content: T  # The generated schematic content (a Pydantic model instance)    info: GenerationInfo  # Metadata about the generation process@dataclass(frozen=True)class GenerationInfo:    schema_name: str  # The name of the Pydantic schema used for the generated content    model: str  # The name of the model used for generation    duration: float  # Time taken for the generation in seconds    usage: UsageInfo  # Token usage information@dataclass(frozen=True)class UsageInfo:    input_tokens: int    output_tokens: int    extra: Optional[Mapping[str, int]] = None  # May contain metrics like cached input tokens

Now let's look at the `SchematicGenerator[T]` interface itself, which you'd need to implement for your custom model:

class SchematicGenerator(ABC, Generic[T]):    """An interface for generating structured content based on a prompt."""    @abstractmethod    async def generate(        self,        # The prompt (or PromptBuilder) containing instructions for the generation.        prompt: str | PromptBuilder,        # Hints are a good way to provide additional context or parameters for the generation,        # such as temperature, top P, logit bias, and things of that nature.        hints: Mapping[str, Any] = {},    ) -> SchematicGenerationResult[T]:        """Generate content based on the provided prompt and hints."""        # Implement this method to generate content using your own model.        ...    @property    @abstractmethod    def id(self) -> str:        """Return a unique identifier for the generator."""        # Normally, this would be the model name or ID used in the LLM API.        ...    @property    @abstractmethod    def max_tokens(self) -> int:        """Return the maximum number of tokens in the underlying model's context window."""        # Return the maximum number of tokens that can be processed by your model.        ...    @property    @abstractmethod    def tokenizer(self) -> EstimatingTokenizer:        """Return a tokenizer that approximates that of the underlying model."""        # This tokenizer should be able to estimate token counts for prompts for this model.        ...    @cached_property    def schema(self) -> type[T]:        """Return the schema type for the generated content.        This is useful for derived classes, allowing them to access the concrete        schema type for the current instance without needing to know the type parameter.        """        # You don't need to implement this method - it's an inherited convenience method.        orig_class = getattr(self, "__orig_class__")        generic_args = get_args(orig_class)        return cast(type[T], generic_args[0])

Reference Example

You can take a look at the official [`OpenAIService`](https://github.com/emcie-co/parlant/blob/main/src/parlant/adapters/nlp/openai_service.py) for a production-ready reference implementation of an `SchematicGenerator[T]`.

![get-in-touch](/img/get-in-touch-button-icon.svg)Help me implement this

### Embedding[​](#embedding "Direct link to Embedding")

In addition to generating structured content, Parlant also uses embedders to create vector representations of text. These are used for semantic retrieval where applicable throughout the response lifecycle.

#### Embedding Results[​](#embedding-results "Direct link to Embedding Results")

Every embedding operation returns an `EmbeddingResult`, which contains the vectors generated by the embedder:

@dataclass(frozen=True)class EmbeddingResult:    vectors: Sequence[Sequence[float]]

#### Embedders[​](#embedders "Direct link to Embedders")

Now let's look at the `Embedder` interface and how to implement it:

class Embedder(ABC):    @abstractmethod    async def embed(        self,        texts: list[str],        hints: Mapping[str, Any] = {},    ) -> EmbeddingResult:        # Generate embeddings for the given texts.        ...    @property    @abstractmethod    def id(self) -> str:        # Return a unique identifier for the embedder - usually the model name or ID.        ...    @property    @abstractmethod    def max_tokens(self) -> int:        # Return the maximum number of tokens in the model's context window.        ...    @property    @abstractmethod    def tokenizer(self) -> EstimatingTokenizer:        # Return a tokenizer that approximates the model's token count for prompts.        ...    @property    @abstractmethod    def dimensions(self) -> int:        # Return the dimensionality of the embedding space.        ...

Reference Example

You can take a look at the official [`OpenAIService`](https://github.com/emcie-co/parlant/blob/main/src/parlant/adapters/nlp/openai_service.py) for a production-ready reference implementation of an `Embedder`.

![get-in-touch](/img/get-in-touch-button-icon.svg)Help me implement this

### Moderation Services[​](#moderation-services "Direct link to Moderation Services")

Parlant includes a comprehensive content moderation system to filter harmful or inappropriate user input. The moderation service is the third key component of an `NLPService`, alongside schematic generators and embedders.

#### Understanding Moderation in Parlant[​](#understanding-moderation-in-parlant "Direct link to Understanding Moderation in Parlant")

Parlant's moderation system provides content filtering capabilities that can detect and flag various types of harmful content before it reaches your AI agents. The engine can integrate with all stsandard moderation providers and can be configured with different levels of strictness.

#### Moderation Interface[​](#moderation-interface "Direct link to Moderation Interface")

All moderation services implement the `ModerationService` abstract base class:

@dataclass(frozen=True)class ModerationCheck:    """Result of a moderation check."""    flagged: bool  # Whether the content was flagged as inappropriate    tags: list[str]  # Specific categories that were flaggedclass ModerationService(ABC):    """Abstract base class for content moderation services."""    @abstractmethod    async def check(self, content: str) -> ModerationCheck:        """Check content for policy violations and return moderation result."""        ...

#### Moderation Tags[​](#moderation-tags "Direct link to Moderation Tags")

Parlant uses standardized moderation tags that map to common content policy categories:

ModerationTag: TypeAlias = Literal[    "jailbreak",      # Prompt injection attempts    "harassment",     # Harassment or bullying content    "hate",          # Hate speech or discrimination    "illicit",       # Illegal activities or substances    "self-harm",     # Self-harm or suicide content    "sexual",        # Sexual or adult content    "violence",      # Violence or graphic content]

#### Implementing Custom Moderation Services[​](#implementing-custom-moderation-services "Direct link to Implementing Custom Moderation Services")

Here's how to create your own moderation service:

import httpximport parlant.sdk as pclass MyModerationService(p.ModerationService):    def __init__(self, api_key: str, logger: p.Logger):        self._api_key = api_key        self._logger = logger        self._client = httpx.AsyncClient()    async def check(self, content: str) -> p.ModerationCheck:        """Implement your moderation logic here."""        try:            # Example: Call your moderation API            response = await self._client.post(                "https://api.your-moderation-service.com/moderate",                json={"text": content},                headers={"Authorization": f"Bearer {self._api_key}"}            )            response.raise_for_status()            result = response.json()            # Map your service's response to Parlant's format            flagged = result.get("flagged", False)            categories = result.get("categories", [])            # Convert your categories to Parlant's standardized tags            tags = []            category_mapping = {                "toxic": "harassment",                "hate_speech": "hate",                "violence": "violence",                "sexual_content": "sexual",                "self_harm": "self-harm",                "illegal": "illicit",                "prompt_injection": "jailbreak",            }            for category in categories:                if category in category_mapping:                    tags.append(category_mapping[category])            return p.ModerationCheck(                flagged=flagged,                tags=tags,            )        except Exception as e:            self._logger.error(f"Moderation check failed: {e}")            # Fail closed: return unflagged to allow content through            # Or fail open: return flagged to block content            return p.ModerationCheck(flagged=False, tags=[])

![get-in-touch](/img/get-in-touch-button-icon.svg)Help me implement this

## Customizing Prompts[​](#customizing-prompts "Direct link to Customizing Prompts")

When you implement your own `SchematicGenerator[T]`, you can also customize the prompts it actually uses.

This is achieved via the `PromptBuilder` class. It's the same class used throughout the Parlant engine to build prompts for LLMs using consistent rules and formats, and it allows you to access and modify prompt templates.

One of the cool things you can do with it is to edit specific prompt sections right before you build the final prompt.

Let's look at an example of how we'd override the draft creation prompt of the `CannedResponseGenerator`.

class MySchematicGenerator(p.SchematicGenerator[p.T]):    async def generate(        self,        prompt: str | p.PromptBuilder,        hints: Mapping[str, Any] = {},    ) -> p.SchematicGenerationResult[T]:        def edit_draft_instructions(section: p.PromptSection) -> p.PromptSection:            # You can inspect the section's dynamically-passed properties            # to see what you can make use of in your modified template.            section.props            section.template = f"""            Write your custom instructions here ...            Pass in dynamic props where needed: {section.props}            """            return section        prompt.edit_section(            name="canned-response-generator-draft-general-instructions",            editor_func=edit_draft_instructions,        )        # Call the parent class's generate method with the modified prompt        return await super().generate(prompt, hints)

You can modify any section used anywhere within Parlant. You can find these sections by looking at references to `PromptBuilder.add_section()` in the Parlant codebase.

## Implementing an `NLPService`[​](#implementing-an-nlpservice "Direct link to implementing-an-nlpservice")

Now that you understand the key interfaces, you can implement your own `NLPService`. This is the easy part.

Here's what that would look like:

class MyNLPService(p.NLPService):    def __init__(self, logger: p.Logger):        self.logger = logger    async def get_schematic_generator(self, t: type[p.T]) -> p.SchematicGenerator[p.T]:        # Return your custom schematic generator for the given type.        return MySchematicGenerator[p.T](            logger=self.logger,  # Assuming you use a logger        )    async def get_embedder(self) -> p.Embedder:        return MyEmbedder(            logger=self.logger,  # Assuming you use a logger        )    async def get_moderation_service(self) -> p.ModerationService:        # Return your custom moderation service implementation.        # If you don't need moderation, return NoModeration().        return MyModerationService(logger=self.logger)

## Injecting a Custom `NLPService`[​](#injecting-a-custom-nlpservice "Direct link to injecting-a-custom-nlpservice")

Once you've implemented your custom `NLPService`, you can easily register it with your Parlant server.

You also get a reference to the dependency-injection container, from which you can access the system's logger and other services, as needed.

def load_custom_nlp_service(container: p.Container) -> p.NLPService:    return MyNLPService(        logger=container[p.Logger]    )

Then, when you start your Parlant server, pass your loader function to the `nlp_service` parameter:

async with p.Server(    nlp_service=load_custom_nlp_service,) as server:    # Your code here

![get-in-touch](/img/get-in-touch-button-icon.svg)Get help with custom models

[

Previous

Engine Extensions

](/docs/advanced/engine-extensions)[

Next

Enforcement & Explainability

](/docs/advanced/explainability)

*   [Custom NLP Models](#custom-nlp-models-1)
*   [Understanding `NLPService`](#understanding-nlpservice)
*   [Schematic Generation](#schematic-generation)
*   [Embedding](#embedding)
*   [Moderation Services](#moderation-services)
*   [Customizing Prompts](#customizing-prompts)
*   [Implementing an `NLPService`](#implementing-an-nlpservice)
*   [Injecting a Custom `NLPService`](#injecting-a-custom-nlpservice)

![Parlant's logo](/logo/logo-full-white.svg)![Parlant's logo](/logo/logo-full-white.svg)

[![GitHub](/img/icons/github-rounded.svg)](https://github.com/emcie-co/parlant)[![Discord](/img/icons/discord-rounded.svg)](https://discord.gg/duxWqxKk6J)[![X](/img/icons/x-rounded.svg)](https://x.com/EmcieCo)[![LinkedIn](/img/icons/linkedin-rounded.svg)](https://linkedin.com/company/emcie/posts/?feedView=all)[![YouTube](/img/icons/youtube-rounded.svg)](https://www.youtube.com/channel/UCmUiKJfCnLage9RhywiiUTw)

2025 parlant

[

Privacy Policy

](/privacy-policy)

Community

*   [GitHub](https://github.com/emcie-co/parlant)
*   [Discord](https://discord.gg/duxWqxKk6J)
*   [X (Twitter)](https://x.com/EmcieCo)

a

Copyright 2025 [Emcie](https://emcie.co).

Licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).

Source code available on [GitHub]