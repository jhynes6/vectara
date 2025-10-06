---
source: "website"
content_type: "blogs_resources"
url: "https://parlant.io/docs/production/api-hardening"
title: "/docs/production/api-hardening"
domain: "parlant.io"
path: "/docs/production/api-hardening"
scraped_time: "2025-09-08T19:58:30.249935"
url_depth: 3
word_count: 1277
---

API Hardening | Parlant

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
*   [Production](/docs/category/production)
*   API Hardening

On this page

# API Hardening

## API Hardening[​](#api-hardening-1 "Direct link to API Hardening")

Parlant provides a robust authorization and rate limiting system to protect your API from unauthorized access and abuse. This guide explains how to implement custom authorization policies and rate limiters to secure your production deployment.

## Overview[​](#overview "Direct link to Overview")

The API hardening system consists of two main components:

1.  **Authorization Policies** - Control who can access what resources and perform which actions
2.  **Rate Limiters** - Prevent abuse by limiting the frequency of requests

Both components work together to provide comprehensive API protection, with support for different limits based on access tokens or user tiers.

![get-in-touch](/img/get-in-touch-button-icon.svg)Need help with API hardening?

## Authorization Policies[​](#authorization-policies "Direct link to Authorization Policies")

### Understanding the AuthorizationPolicy Abstract Class[​](#understanding-the-authorizationpolicy-abstract-class "Direct link to Understanding the AuthorizationPolicy Abstract Class")

All authorization policies inherit from the `AuthorizationPolicy` abstract base class, which defines three key methods:

class AuthorizationPolicy:    @abstractmethod    async def check_permission(        self,        request: fastapi.Request,        permission: AuthorizationPermission    ) -> bool:        """Check if the request has permission to perform the action"""        ...    @abstractmethod    async def check_rate_limit(        self,        request: fastapi.Request,        permission: AuthorizationPermission    ) -> bool:        """Check if the request is within rate limits"""        ...    async def authorize(        self,        request: fastapi.Request,        permission: AuthorizationPermission    ) -> None:        """Combined authorization check (permission + rate limit)"""        # This method usually isn't overriden, as its default implementation        # calls the two abstract methods in sequence and raises an authorization        # error if anything is denied.        ...

### Authorization Permissions[​](#authorization-permissions "Direct link to Authorization Permissions")

Parlant defines a comprehensive set of permissions as an enum covering all API operations:

*   Agent operations (create, read, update, delete)
*   Customer management
*   Session handling
*   And many more...

### Built-in Authorization Policies[​](#built-in-authorization-policies "Direct link to Built-in Authorization Policies")

#### DevelopmentAuthorizationPolicy[​](#developmentauthorizationpolicy "Direct link to DevelopmentAuthorizationPolicy")

Allows all actions - suitable for development environments only:

class DevelopmentAuthorizationPolicy(AuthorizationPolicy):    async def check_permission(        self,        request: fastapi.Request,        permission: AuthorizationPermission    ) -> bool:        return True    async def check_rate_limit(        self,        request: fastapi.Request,        permission: AuthorizationPermission    ) -> bool:        return True

#### ProductionAuthorizationPolicy[​](#productionauthorizationpolicy "Direct link to ProductionAuthorizationPolicy")

Implements stricter controls for production use with configurable rules.

## Implementing Custom Authorization Policies[​](#implementing-custom-authorization-policies "Direct link to Implementing Custom Authorization Policies")

When you implement your own authorization policy in real-world deployments, you typically want to extend the existing production policy rather than building from scratch. The recommended approach is to subclass `ProductionAuthorizationPolicy` and customize it for your specific needs.

Here's a reference implementation that demonstrates how to create a custom policy with JWT authentication:

import parlant.sdk as pimport jwtfrom fastapi import HTTPExceptionfrom limits import RateLimitItemPerMinute, RateLimitItemPerHourfrom limits.storage import RedisStoragefrom limits.strategies import SlidingWindowCounterRateLimiterclass CustomAuthorizationPolicy(p.ProductionAuthorizationPolicy):    def __init__(self, secret_key: str, algorithm: str = "HS256"):        super().__init__()        self.secret_key = secret_key        self.algorithm = algorithm    async def _extract_token(self, request: fastapi.Request) -> dict | None:        """Extract and validate JWT token from request"""        auth_header = request.headers.get("Authorization")        if not auth_header or not auth_header.startswith("Bearer "):            return None        token = auth_header.split(" ")[1]        try:            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])            return payload        except jwt.JWTError:            # Raise 403 for invalid tokens, None for missing tokens is OK            raise HTTPException(                status_code=403,                detail="Invalid access token"            )    async def check_permission(        self,        request: fastapi.Request,        operation: p.Operation    ) -> bool:        """Enhanced permission checking with M2M token support"""        token_payload = await self._extract_token(request)        # If we have a valid M2M (machine-to-machine) token, allow additional operations        if token_payload and token_payload.get("type") == "m2m":            m2m_operations = {                # Allow M2M tokens to perform administrative operations                p.Operation.CREATE_AGENT,                p.Operation.READ_AGENT,                p.Operation.UPDATE_AGENT,                p.Operation.DELETE_AGENT,                p.Operation.CREATE_CUSTOMER,                p.Operation.READ_CUSTOMER,                p.Operation.UPDATE_CUSTOMER,                p.Operation.DELETE_CUSTOMER,                p.Operation.CREATE_CUSTOMER_SESSION,                p.Operation.LIST_SESSIONS,                p.Operation.UPDATE_SESSION,                p.Operation.DELETE_SESSION,                # Add other operations your M2M integration needs            }            if operation in m2m_operations:                return True        # For all other cases, delegate to the parent ProductionAuthorizationPolicy        return await super().check_permission(request, operation)

![get-in-touch](/img/get-in-touch-button-icon.svg)Need help with API hardening?

## Rate Limiting Customization Options[​](#rate-limiting-customization-options "Direct link to Rate Limiting Customization Options")

The `ProductionAuthorizationPolicy` provides several ways to customize rate limiting behavior:

### 1\. Override the Default Rate Limiter (Recommended)[​](#1-override-the-default-rate-limiter-recommended "Direct link to 1. Override the Default Rate Limiter (Recommended)")

The most common approach is to override `self.default_limiter` with your own `BasicRateLimiter` configuration. **Note that BasicRateLimiter limits apply per IP address** - so when you configure `RateLimitItemPerMinute(100)`, it means 100 requests per minute per IP address.

from limits import RateLimitItemPerMinute, RateLimitItemPerHourfrom limits.storage import RedisStoragefrom limits.strategies import SlidingWindowCounterRateLimiter# Example with Redis storage and custom limitsclass CustomAuthorizationPolicy(p.ProductionAuthorizationPolicy):    def __init__(self, ...):        super().__init__()        # ...        self.default_limiter = p.BasicRateLimiter(            rate_limit_item_per_operation={                # Use the default rate limit for most operations                **self.default_limiter.rate_limit_item_per_operation,                # Override specific operations with custom limits                p.Operation.READ_SESSION: RateLimitItemPerMinute(200),                p.Operation.LIST_EVENTS: RateLimitItemPerMinute(1000),            },            # Use a custom storage backend (e.g., Redis)            storage=RedisStorage("redis://localhost:6379"),            # Use a custom window strategy            limiter_type=SlidingWindowCounterRateLimiter,        )

The `BasicRateLimiter` uses the `limits` library and supports:

*   **Rate limit items**: `RateLimitItemPerMinute(n)`, `RateLimitItemPerSecond(n)`, `RateLimitItemPerHour(n)`
*   **Storage options**: `RedisStorage()`, `MemoryStorage()`, and others from the limits library
*   **Limiter strategies**: `MovingWindowRateLimiter`, `FixedWindowRateLimiter`, `SlidingWindowCounterRateLimiter`

Custom Rate Limiter

For complete control, you can implement your own `RateLimiter` from scratch by subclassing the abstract `RateLimiter` class and assigning it to `self.default_limiter`.

### 2\. Custom Limiter Functions for Specific Operations[​](#2-custom-limiter-functions-for-specific-operations "Direct link to 2. Custom Limiter Functions for Specific Operations")

Use `self.specific_limiters` to provide custom rate limiting functions for particular operations. These are functions that take a request and operation and return a boolean indicating whether the rate is within the limit.

class CustomAuthorizationPolicy(p.ProductionAuthorizationPolicy):    def __init__(self, ...):        super().__init__()        # ...        self.specific_limiters[p.Operation.DELETE_AGENT] = self._custom_delete_limiter    async def _custom_delete_limiter(        self,        request: fastapi.Request,        operation: p.Operation    ) -> bool:        # Implement your custom logic here        ...

Complete Customization

If you need complete control over both permission checking and rate limiting, you can also subclass the abstract `AuthorizationPolicy` directly and implement all methods from scratch. This gives you full flexibility but requires more implementation work. The approach shown above is recommended for most use cases as it builds on the robust foundation of `ProductionAuthorizationPolicy`.

## Integrating Your Custom Authorization Policy[​](#integrating-your-custom-authorization-policy "Direct link to Integrating Your Custom Authorization Policy")

### Using configure\_container[​](#using-configure_container "Direct link to Using configure_container")

Integrate your custom authorization policy and rate limiter with your Parlant agent:

async def configure_container(    container: p.Container) -> p.Container:    container[p.AuthorizationPolicy] = CustomAuthorizationPolicy(        secret_key="your-jwt-secret-key",        algorithm="HS256",    )    return container

async def main():    # Create Parlant server with custom authorization    async with p.Server(        configure_container=configure_container,    ) as server:        # Your agent logic here        await server.serve()if __name__ == "__main__":    asyncio.run(main())

![get-in-touch](/img/get-in-touch-button-icon.svg)Need help with API hardening?

[

Previous

Human Handoff

](/docs/production/human-handoff)[

Next

Custom Frontend

](/docs/production/custom-frontend)

*   [API Hardening](#api-hardening-1)
*   [Overview](#overview)
*   [Authorization Policies](#authorization-policies)
*   [Understanding the AuthorizationPolicy Abstract Class](#understanding-the-authorizationpolicy-abstract-class)
*   [Authorization Permissions](#authorization-permissions)
*   [Built-in Authorization Policies](#built-in-authorization-policies)
*   [Implementing Custom Authorization Policies](#implementing-custom-authorization-policies)
*   [Rate Limiting Customization Options](#rate-limiting-customization-options)
*   [1\. Override the Default Rate Limiter (Recommended)](#1-override-the-default-rate-limiter-recommended)
*   [2\. Custom Limiter Functions for Specific Operations](#2-custom-limiter-functions-for-specific-operations)
*   [Integrating Your Custom Authorization Policy](#integrating-your-custom-authorization-policy)
*   [Using configure\_container](#using-configure_container)

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

Source code available on [GitHub](https:/