---
source: "website"
content_type: "blogs_resources"
url: "https://parlant.io/docs/quickstart/examples"
title: "/docs/quickstart/examples"
domain: "parlant.io"
path: "/docs/quickstart/examples"
scraped_time: "2025-09-08T20:00:33.465101"
url_depth: 3
word_count: 2404
---

Healthcare Agent Example | Parlant

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
*   Quick Start
*   Healthcare Agent Example

On this page

# Healthcare Agent Example

## Healthcare Agent Example[​](#healthcare-agent-example-1 "Direct link to Healthcare Agent Example")

This page walks you through using Parlant to design and build a healthcare agent with two customer journeys.

1.  **Schedule an appointment**: The agent helps the patient find a time for their appointment.
2.  **Lab results**: The agent retrieves the patient's lab results and explains them.

![Scheduling journey demo](/img/example-scheduling-journey.gif)

You'll learn how to:

*   Align your agent with basic domain knowledge.
*   Define **journeys** with **states** and **transitions**.
*   Use **guidelines** to control the agent's behavior in conversational edge cases.
*   Use **tools** to connect your agent to real actions and data.
*   Disambiguate vague user queries.

While this section is by no means a comprehensive guide to Parlant's features, it will give you a solid idea of what the basics look like, and how to think about building your own agents with Parlant. Let's get started!

The Art of Behavior Modeling

Building complex and reliable customer-facing AI agents is a challenging task. Don't let the hype-machine tell you otherwise.

It isn't just about having the right framework. When we automate conversations, we are automating the complex semantics of human conversations. In very real terms, this means we need to design our instructions and behavior models carefully. They need to be clear, and be at the right level of specificity, to ensure that the agent truly behaves as we expect it to.

While Parlant gives you the tools to express and enforce your instructions, _designing them_ is an art in itself, requiring practice to get right. But once you do, you can build agents that are not only functional and reliable, but also engaging and effective.

![get-in-touch](/img/get-in-touch-button-icon.svg)Consult modeling experts

## Preparing the Environment[​](#preparing-the-environment "Direct link to Preparing the Environment")

Before getting started, make sure you've

1.  [Installed](/docs/quickstart/installation) Parlant and have a Python environment set up.
2.  Chosen your NLP provider and connected it to your server (also on the [installation page](/docs/quickstart/installation)).

Download the Code

The runnable code for this fully worked example can be found in the `examples/` folder of [Parlant's GitHub repository](https://github.com/emcie-co/parlant).

## Overview[​](#overview "Direct link to Overview")

We'll implement the agent in the following steps:

1.  Create the baseline program with a simple agent description.
2.  Add the **scheduling** journey, with states, transitions, and tools.
3.  Add the **lab results** journey in a similar way.

## Getting Started[​](#getting-started "Direct link to Getting Started")

We'll implement the entire program in a single file, `healthcare.py`, but in real-world use cases you would likely want to split it into multiple files for better organization. A good approach in those cases is to have a file per journey.

But now let's get to creating our initial agent.

# healthcare.pyimport parlant.sdk as pimport asyncioasync def add_domain_glossary(agent: p.Agent) -> None:  await agent.create_term(    name="Office Phone Number",    description="The phone number of our office, at +1-234-567-8900",  )  await agent.create_term(    name="Office Hours",    description="Office hours are Monday to Friday, 9 AM to 5 PM",  )  await agent.create_term(    name="Charles Xavier",    synonyms=["Professor X"],    description="The renowned doctor who specializes in neurology",  )  # Add other specific terms and definitions here, as needed...async def main() -> None:    async with p.Server() as server:        agent = await server.create_agent(            name="Healthcare Agent",            description="Is empathetic and calming to the patient.",        )        await add_domain_glossary(agent)if __name__ == "__main__":    asyncio.run(main())

## Creating the Scheduling Journey[​](#creating-the-scheduling-journey "Direct link to Creating the Scheduling Journey")

To understand how journeys work in Parlant, please check out the [Journeys documentation](/docs/concepts/customization/journeys). Here, we'll jump straight into it, but it's recommended to review their documentation first.

### Adding Tools[​](#adding-tools "Direct link to Adding Tools")

First, add the tools we need to support this journey.

from datetime import datetime@p.toolasync def get_upcoming_slots(context: p.ToolContext) -> p.ToolResult:  # Simulate fetching available times from a database or API  return p.ToolResult(data=["Monday 10 AM", "Tuesday 2 PM", "Wednesday 1 PM"])@p.toolasync def get_later_slots(context: p.ToolContext) -> p.ToolResult:  # Simulate fetching later available times  return p.ToolResult(data=["November 3, 11:30 AM", "November 12, 3 PM"])@p.toolasync def schedule_appointment(context: p.ToolContext, datetime: datetime) -> p.ToolResult:  # Simulate scheduling the appointment  return p.ToolResult(data=f"Appointment scheduled for {datetime}")

Tools in Parlant

Parlant has a more intricate tool system than most agentic frameworks, since it is optimized for conversational, sensitive customer-facing use cases. We highly recommend perusing the documentation in the [Tools section](/docs/concepts/customization/tools) to learn its power.

### Building the Journey[​](#building-the-journey "Direct link to Building the Journey")

We'll now create the journey according to the following diagram:

# <<Add this function>>async def create_scheduling_journey(server: p.Server, agent: p.Agent) -> p.Journey:  # Create the journey  journey = await agent.create_journey(    title="Schedule an Appointment",    description="Helps the patient find a time for their appointment.",    conditions=["The patient wants to schedule an appointment"],  )  # First, determine the reason for the appointment  t0 = await journey.initial_state.transition_to(chat_state="Determine the reason for the visit")  # Load upcoming appointment slots into context  t1 = await t0.target.transition_to(tool_state=get_upcoming_slots)  # Ask which one works for them  # We will transition conditionally from here based on the patient's response  t2 = await t1.target.transition_to(chat_state="List available times and ask which ones works for them")  # We'll start with the happy path where the patient picks a time  t3 = await t2.target.transition_to(    chat_state="Confirm the details with the patient before scheduling",    condition="The patient picks a time",  )  t4 = await t3.target.transition_to(    tool_state=schedule_appointment,    condition="The patient confirms the details",  )  t5 = await t4.target.transition_to(chat_state="Confirm the appointment has been scheduled")  await t5.target.transition_to(state=p.END_JOURNEY)  # Otherwise, if they say none of the times work, ask for later slots  t6 = await t2.target.transition_to(    tool_state=get_later_slots,    condition="None of those times work for the patient",  )  t7 = await t6.target.transition_to(chat_state="List later times and ask if any of them works")  # Transition back to our happy-path if they pick a time  await t7.target.transition_to(state=t3.target, condition="The patient picks a time")  # Otherwise, ask them to call the office  t8 = await t7.target.transition_to(    chat_state="Ask the patient to call the office to schedule an appointment",    condition="None of those times work for the patient either",  )  await t8.target.transition_to(state=p.END_JOURNEY)  return journey

Then call this function in your `main` function to add the journey to your agent:

async def main() -> None:  async with p.Server() as server:    agent = await server.create_agent(      name="Healthcare Agent",      description="Is empathetic and calming to the patient.",    )    # <<Add this line>>    scheduling_journey = await create_scheduling_journey(server, agent)

### Handling Edge Cases[​](#handling-edge-cases "Direct link to Handling Edge Cases")

In real-world scenarios, patients do not always followed the scripted path of your journeys. They might ask questions, express concerns, or provide other unexpected responses.

For Parlant agents, this is their bread and butter! While they will still be able to respond contextually to the patient, you might still like to guide and improve _how_ they respond in particular scenarios that you've observed.

To do this, you can add **guidelines** to your agent. Guidelines are like contextual rules that tell the agent how to respond in specific situations. And you can scope them to specific journeys, so they only apply when the agent is in that journey.

Let's add a few guidelines to our agent to handle some common edge cases in the scheduling journey.

async def create_scheduling_journey(server: p.Server, agent: p.Agent) -> p.Journey:  # ... continued  # <<Add this to the end of the create_scheduling_journey function>>  await journey.create_guideline(    condition="The patient says their visit is urgent",    action="Tell them to call the office immediately",  )  # Add more edge case guidelines as needed...  return journey

### Running the Program[​](#running-the-program "Direct link to Running the Program")

When you run the program, you should first see Parlant evaluating the semantic properties of your configuration. It does this in order to optimize how your guidelines and journeys are retrieved, processed and followed behind the scenes.

![Evaluation of the agent configuration](/img/example-evaluation.gif)

Once the server is ready, open your browser and navigate to [http://localhost:8800](http://localhost:8800) to interact with your agent.

![Scheduling journey demo](/img/example-scheduling-journey.gif)

Handling Unsupported Queries

You may notice that your agent, at this point, is happy to try and assist customers while completely overstepping the boundaries of its knowledge and capabilities. While this is normal with LLMs, it is untolerable in many real-life use cases.

Parlant provides multiple structured ways to achieve absolute control over your agent's (mis)behavior. This example is only the beginning; rest assured that as you learn more about Parlant, it can help you deploy an agent you can actually trust.

![get-in-touch](/img/get-in-touch-button-icon.svg)Consult modeling experts

## Creating the Lab Results Journey[​](#creating-the-lab-results-journey "Direct link to Creating the Lab Results Journey")

We'll speed through this journey, as it will be very similar in structure to the other journey (and any other journey you'd be likely to build).

### Adding Tools[​](#adding-tools-1 "Direct link to Adding Tools")

@p.toolasync def get_lab_results(context: p.ToolContext) -> p.ToolResult:  # Simulate fetching lab results from a database or API,  # using the customer ID from the context.  lab_results = await MY_DB.get_lab_results(context.customer_id)  if lab_results is None:    return p.ToolResult(data="No lab results found for this patient.")  return p.ToolResult(data={    "report": lab_results.report,    "prognosis": lab_results.prognosis,  })

### Building the Journey[​](#building-the-journey-1 "Direct link to Building the Journey")

async def create_lab_results_journey(server: p.Server, agent: p.Agent) -> p.Journey:  # Create the journey  journey = await agent.create_journey(    title="Lab Results",    description="Retrieves the patient's lab results and explains them.",    conditions=["The patient wants to see their lab results"],  )  t0 = await journey.initial_state.transition_to(tool_state=get_lab_results)  await t0.target.transition_to(    chat_state="Tell the patient that the results are not available yet, and to try again later",    condition="The lab results could not be found",  )  await t0.target.transition_to(    chat_state="Explain the lab results to the patient - that they are normal",    condition="The lab results are good - i.e., nothing to worry about",  )  await t0.target.transition_to(    chat_state="Present the results and ask them to call the office "     "for clarifications on the results as you are not a doctor",    condition="The lab results are not good - i.e., there's an issue with the patient's health",  )  # Handle edge cases with guidelines...  await agent.create_guideline(    condition="The patient presses you for more conclusions about the lab results",    action="Assertively tell them that you cannot help and they should call the office"  )  return journey

Finally, call this function in your `main` function to add the journey to your agent:

async def main() -> None:  async with p.Server() as server:    agent = await server.create_agent(      name="Healthcare Agent",      description="Is empathetic and calming to the patient.",    )    scheduling_journey = await create_scheduling_journey(server, agent)    # <<Add this line>>    lab_results_journey = await create_lab_results_journey(server, agent)

Restart the program, open your browser and navigate to [http://localhost:8800](http://localhost:8800) to interact with your agent. Try saying something like, _"Did my lab results come in?"_ or _"I want to schedule an appointment"_.

## Disambiguating Patient Intent[​](#disambiguating-patient-intent "Direct link to Disambiguating Patient Intent")

In some cases, the patient might say something that could be interpreted in multiple ways, leading to confusion about which action to take or what they wish to achieve.

An easy way to handle this is to use **disambiguation**. This will get the agent to ask the patient to clarify their intent when multiple actions could be taken. Here's how you can do it:

async def main() -> None:  async with p.Server() as server:    agent = await server.create_agent(      name="Healthcare Agent",      description="Is empathetic and calming to the patient.",    )    scheduling_journey = await create_scheduling_journey(server, agent)    lab_results_journey = await create_lab_results_journey(server, agent)    # <<Add the following lines>>    # First, create an observation of an ambiguous situation    status_inquiry = await agent.create_observation(      "The patient asks to follow up on their visit, but it's not clear in which way",    )    # Use this observation to disambiguate between the two journeys    await status_inquiry.disambiguate([scheduling_journey, lab_results_journey])

Now, if the patient inquires in an ambiguous way about a follow-up, the agent will ask them to clarify whether they want to schedule an appointment or see their lab results.

Restart the program, open your browser and navigate to [http://localhost:8800](http://localhost:8800) to interact with your agent. Try saying something like, _"I need to follow up on my last visit"_ and see what the agent responds with.

## Global Guidelines[​](#global-guidelines "Direct link to Global Guidelines")

There are usually some guidelines that you might want to apply to all journeys of your agent, not just a specific one (or, for that matter, even if a patient is not in the middle of a journey). For example, you might want to provide information about insurance providers in an informed manner.

To achieve this, you just need to add guidelines to the agent itself, rather than to a specific journey.

await agent.create_guideline(  condition="The patient asks about insurance",  action="List the insurance providers we accept, and tell them to call the office for more details",  tools=[get_insurance_providers],)await agent.create_guideline(  condition="The patient asks to talk to a human agent",  action="Ask them to call the office, providing the phone number",)await agent.create_guideline(  condition="The patient inquires about something that has nothing to do with our healthcare",  action="Kindly tell them you cannot assist with off-topic inquiries - do not engage with their request.",)

## Next Steps[​](#next-steps "Direct link to Next Steps")

1.  Download and try out the runnable code file for this example: [healthcare.py](https://github.com/emcie-co/parlant/blob/develop/examples/healthcare.py)
2.  Tailor and constrain the content and style of agent messages with canned responses: [Canned Responses](/docs/concepts/customization/canned-responses)
3.  Learn how to deploy your agent in a [production environment](/docs/category/production)
4.  Add the [React widget](https://github.com/emcie-co/parlant-chat-react) to your website to interact with the agent

[

Previous

Motivation

](/docs/quickstart/motivation)[

Next

Sessions

](/docs/concepts/sessions)

*   [Healthcare Agent Example](#healthcare-agent-example-1)
*   [Preparing the Environment](#preparing-the-environment)
*   [Overview](#overview)
*   [Getting Started](#getting-started)
*   [Creating the Scheduling Journey](#creating-the-scheduling-journey)
*   [Adding Tools](#adding-tools)
*   [Building the Journey](#building-the-journey)
*   [Handling Edge Cases](#handling-edge-cases)
*   [Running the Program](#running-the-program)
*   [Creating the Lab Results Journey](#creating-the-lab-results-journey)
*   [Adding Tools](#adding-tools-1)
*   [Building the Journey](#building-the-journey-1)
*   [Disambiguating Patient Intent](#disambiguating-patient-intent)
*   [Global Guidelines](#global-guidelines)
*   [Next Steps](#next-steps)

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

Source code available on [GitHub](https