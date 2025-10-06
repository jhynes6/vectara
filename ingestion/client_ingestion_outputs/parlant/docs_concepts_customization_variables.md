---
source: "website"
content_type: "blogs_resources"
url: "https://parlant.io/docs/concepts/customization/variables"
title: "/docs/concepts/customization/variables"
domain: "parlant.io"
path: "/docs/concepts/customization/variables"
scraped_time: "2025-09-08T19:59:58.749358"
url_depth: 4
word_count: 1074
---

Variables | Parlant

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
*   Behavior Modeling
*   Variables

On this page

# Variables

## Variables[​](#variables-1 "Direct link to Variables")

Every customer is unique, and your agent may choose to treat them as such where appropriate.

Variables enrich the context that an agent sees about the customer it's talking to. They're meant to give your agent awareness to information that helps it personalize its service, much like how a thoughtful customer service representative knows and remembers important details about each client, to make them feel heard and understood.

When a customer interacts with an agent, their variables are automatically loaded into its context, allowing the agent to tailor its responses based on their specific situation.

### Real World Applications[​](#real-world-applications "Direct link to Real World Applications")

Let's walk through how variables transform customer interactions. Imagine you're running a SaaS platform's support agent. You might track variables like subscription plan, last login date, which features each customer uses, and their company size.

Consider two different customers reaching out about data exports. Sarah, a startup founder on the free plan, asks "Can I export my data to Excel?" Your agent, aware of her free plan status, can respond thoughtfully: "While Excel export is a premium feature, I can show you how to use our basic CSV export. Would you also like to learn about the advanced reporting capabilities in our premium plan?"

Now imagine Tom from an enterprise account reaches out with the same question. The agent sees his enterprise status but also notices his team hasn't explored many advanced features. It might respond: "I'll help you with Excel exports! I notice your team hasn't tried our automated reporting suite yet - this is included in your enterprise plan and could save you hours each week. Would you like me to show you both features?"

### Working with Variables[​](#working-with-variables "Direct link to Working with Variables")

A single variable identifies a particular piece of information. For example, you might create a variable called `"subscription_plan"`.

Each customer can then have a unique value assigned to them under that variable. For example, Tom might have `"enterprise"` as the variable's value.

There are two ways to set variable values.

1.  Set their values manually
2.  Attach them to a tool that automatically retrieves a value based on dynamic data

#### Creating Manually Set Variables[​](#creating-manually-set-variables "Direct link to Creating Manually Set Variables")

variable = await agent.create_variable(    name=NAME,    description=DESCRIPTION,)

#### Creating Tool-Enabled Variables[​](#creating-tool-enabled-variables "Direct link to Creating Tool-Enabled Variables")

A variable that's associated with a tool will automatically update its value based on the tool's output. This is useful for dynamic data that changes frequently and of which the agent always needs to be aware.

Suppose you have the following tool:

@p.toolasync def get_variable_value(context: p.ToolContext) -> p.ToolResult:  ...

You can then create an auto-updating variable based on this tool as follows:

variable = await agent.create_variable(    name=NAME,    description=DESCRIPTION,    tool=get_variable_value,)

By default, the associated tool would update the variable's value before every agent response. If this frequent reload of data is unnecessary, you can control the refresh interval of the value (controlling how often the associated tool is called to generate a fresh value) by specifying its _freshness rules_.

variable = await agent.create_variable(    name=NAME,    description=DESCRIPTION,    tool=get_variable_value,    freshness_rules=CRON_EXPRESSION,)

Freshness rules follow the [cron expression](https://en.wikipedia.org/wiki/Cron) syntax. If you're new to cron, you can use tools like [crontab generator](https://crontab.cronhub.io/) to help you define the period syntax more easily.

Manual Values

Even tool-enabled variables can have their values set manually, if needed. This is useful for when you want to override the tool's output for specific customers or customer groups.

#### Setting a Variable Value for a Customer[​](#setting-a-variable-value-for-a-customer "Direct link to Setting a Variable Value for a Customer")

await variable.set_value_for_customer(    customer=CUSTOMER,    value=VALUE,)

#### Setting a Variable Value for a Customer Group[​](#setting-a-variable-value-for-a-customer-group "Direct link to Setting a Variable Value for a Customer Group")

You can also set the value of a variable for a [customer group](/docs/concepts/entities/customers#customer-groups) by specifying the group's tag.

await variable.set_value_for_tag(    tag=TAG_ID,    value=VALUE,)

![get-in-touch](/img/get-in-touch-button-icon.svg)Questions? Reach out!

## Working Example[​](#working-example "Direct link to Working Example")

Here's how we'd implement a subscription plan variable.

@p.toolasync def get_subscription_plan(context: p.ToolContext) -> p.ToolResult:    # Fetch the customer's subscription plan from your database    return p.ToolResult(await get_plan_from_database(context.customer_id))

variable = await agent.create_variable(    name="subscription_plan",    description="The customer's subscription plan",    tool=get_subscription_plan,)await variable.set_value_for_customer(    customer=p.Customer.guest(),    value="Free Plan",  # Default value for non-registered customers)

### Combining Context Variables with Guidelines[​](#combining-context-variables-with-guidelines "Direct link to Combining Context Variables with Guidelines")

Let's explore how guidelines and context variables work together to create truly intelligent interactions. Imagine you're running an AI support agent for a digital bank where customers have different account tiers and transaction patterns.

Here's a focused guideline:

await agent.create_guideline(    condition="the customer's account_tier is 'basic' "      "AND they ask about instant international transfers",    action="highlight our same-day domestic transfers that are free on their plan, "      "then mention how the premium tier enables instant global payments with lower fees",)

When Mark, who is on the basic tier, asks about sending money to his daughter studying abroad, instead of a flat "that's premium only" response, he hears: "I can help you send that money today using our standard international transfer. By the way, our premium accounts get this done instantly with lower fees—would you like to know more?"

![get-in-touch](/img/get-in-touch-button-icon.svg)We can help you ramp up!

[

Previous

Glossary

](/docs/concepts/customization/glossary)[

Next

Canned Responses

](/docs/concepts/customization/canned-responses)

*   [Variables](#variables-1)
*   [Real World Applications](#real-world-applications)
*   [Working with Variables](#working-with-variables)
*   [Working Example](#working-example)
*   [Combining Context Variables with Guidelines](#combining-context-variables-with-guidelines)

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

Source code available on [GitHub](https://github.