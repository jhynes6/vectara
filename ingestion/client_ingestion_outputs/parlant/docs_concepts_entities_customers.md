---
source: "website"
content_type: "other"
url: "https://parlant.io/docs/concepts/entities/customers"
title: "/docs/concepts/entities/customers"
domain: "parlant.io"
path: "/docs/concepts/entities/customers"
scraped_time: "2025-09-08T19:59:29.663868"
url_depth: 4
word_count: 908
---

Customers | Parlant

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
*   Components
*   Entities
*   Customers

On this page

# Customers

## Customers[​](#customers-1 "Direct link to Customers")

In Parlant, a **customer** is a code word for anyone who interacts with an agent—regardless of the real nature of the relationship between them. In other words, a customer can be a real person, a bot, or even a human agent.

While agents can operate anonymously (without knowing who they're talking to), Parlant allows you to track registered customers and provide deeply personalized experiences based on their identity and preferences.

By letting your agents understand who they're talking to, you can tailor interactions for different user segments: high-profile customers might receive premium offers, new users can get focused onboarding guidance, and so forth...

Parlant makes customer registration simple, requiring only minimal identification—a name is enough to get started.

import parlant.sdk as pasync with p.Server() as server:    # Register a new customer    customer = await server.create_customer(name="Alice")

## Authentication[​](#authentication "Direct link to Authentication")

Parlant aims to live as a backend service, leaving authentication and authorization to the application layer. This means that while you can register customers, you should handle their authentication (e.g., via OAuth, JWT, etc.) in your application code, in whatever way suits your needs.

Once you have identified your customer, then you can pass their ID to the agent, allowing it to personalize interactions based on the registered customer.

## Storage[​](#storage "Direct link to Storage")

You can choose where you store customers.

By default, Parlant does not persist customers, meaning that they are stored in memory and will be lost when the server restarts. This is useful for testing and development purposes.

If you want to persist customers, you can configure Parlant to use a database of your choice. For local persistence, we recommend using the integrated JSON file storage, as there's zero setup required. For production use, you can use MongoDB, which comes built-in, or another database.

### Persisting to Local Storage[​](#persisting-to-local-storage "Direct link to Persisting to Local Storage")

This will save customers under `$PARLANT_HOME/customers.json`.

import asyncioimport parlant.sdk as pasync def main():    async with p.Server(customer_store="local") as server:        # ...asyncio.run(main())

### Persisting to MongoDB[​](#persisting-to-mongodb "Direct link to Persisting to MongoDB")

Just specify the connection string to your MongoDB database when starting the server:

import asyncioimport parlant.sdk as pasync def main():    async with p.Server(customer_store="mongodb://path.to.your.host:27017") as server:        # ...asyncio.run(main())

![get-in-touch](/img/get-in-touch-button-icon.svg)We can help you ramp up

## Customer Groups[​](#customer-groups "Direct link to Customer Groups")

You can also divide your customers into different groups and control group-specific personalization by using **tags**.

For example, you can create a tag for VIP customers:

# Create a new tag to represent VIP customersvip_tag = await server.create_tag(name="VIP")# Register a new customercustomer = await server.create_customer(name="Alice", tags=[vip_tag.id])

Learn More

To learn more about advanced personalization possibilities for specific customers and groups, check out the [variables](/docs/concepts/customization/variables) section.

## Adding Metadata[​](#adding-metadata "Direct link to Adding Metadata")

You can also attach custom metadata to customers, which can be used to store additional information about them. This metadata can be used to further personalize interactions or to provide context for tool calls.

customer = await server.create_customer(name="Alice", metadata={    "external_id": "12345",    "location": "USA",})

@p.toolasync def get_customer_location(context: p.ToolContext) -> p.ToolResult:    server = p.ToolContextAccessor(context).server    if customer := await server.find_customer(id=context.customer_id):        return p.ToolResult(customer.metadata.get("location", "Unknown location"))    return p.ToolResult("Customer not found")

## Registering Customers[​](#registering-customers "Direct link to Registering Customers")

While you can register customers using the SDK itself, it's often more practical to handle customer registration through your application layer. This allows you to integrate customer management with your existing user authentication and authorization systems.

You can do this by using Parlant's REST API or native Client SDKs to create and manage customers.

from parlant.client import ParlantClient# Change localhost to your server's addressclient = ParlantClient("http://localhost:8800")client.customers.create(    name="Alice",    metadata={        "external_id": "12345",        "location": "USA",        "hobby": "reading",    },    tags=[TAG_ID]  # Optional: specify tag IDs to assign to the customer)

## Updating Customer Data[​](#updating-customer-data "Direct link to Updating Customer Data")

You can update customer data at any time, including their name, metadata, and tags. This is useful for keeping customer information up-to-date as your application evolves.

client.customers.update(    customer_id=CUSTOMER_ID,    name="Alice Smith",    metadata={        "set": {            "location": "Canada",        },        "remove": ["hobby"],    },    tags=[NEW_TAG_ID]  # Optional: specify new tag IDs to assign to the customer)

![get-in-touch](/img/get-in-touch-button-icon.svg)Reach out for help

[

Previous

Agents

](/docs/concepts/entities/agents)[

Next

Journeys

](/docs/concepts/customization/journeys)

*   [Customers](#customers-1)
*   [Authentication](#authentication)
*   [Storage](#storage)
*   [Persisting to Local Storage](#persisting-to-local-storage)
*   [Persisting to MongoDB](#persisting-to-mongodb)
*   [Customer Groups](#customer-groups)
*   [Adding Metadata](#adding-metadata)
*   [Registering Customers](#registering-customers)
*   [Updating Customer Data](#updating-customer-data)

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

Source code available on [GitHub](https://githu