---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# REST APIs — Quick Reference

> [!info] How I've used it: 10 years of REST API development across all companies. Currently at Combination for external partner APIs alongside GraphQL and gRPC. At KocSistem, all APIs were REST before I introduced the multi-protocol approach.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Design Principles\|design principles]] | resource-oriented, nouns not verbs, stateless | [[#Versioning\|versioning]] | URL /v1 simplest, header-based for advanced |
| [[#HTTP Caching\|caching]] | Cache-Control, ETag, conditional GET, 304 | [[#Rate Limiting & Security\|rate limiting]] | token bucket, 429 + Retry-After header |
| [[#When to Use REST vs Alternatives\|REST vs GraphQL vs gRPC]] | REST=external partners, GraphQL=frontend, gRPC=internal | | |

## HOW WE USE IT

REST has been my default API style for 10 years — it's the foundation everything else builds on. At Combination, REST is specifically for external partner integrations. At KocSistem, everything was REST. At Toyota, the HTTP API layer was REST.

**At Combination:**
- REST for external partner APIs — simple, well-documented with OpenAPI/Swagger, easy for third parties to consume without installing proto compilers or GraphQL clients
- Each REST service exposes `/swagger` in non-production environments for interactive documentation
- API changelogs published with each release
- The [[sd-graphql-migration|GraphQL migration]] was specifically about replacing REST for internal frontends — external APIs stayed REST

**At KocSistem:**
- All 10+ applications used REST APIs — standard .NET MVC controllers with Entity Framework
- I designed the GPS tracking API that handled 500+ trucks reporting coordinates — the [[sd-redis-scaling|scaling fix]] was in the data layer, but the API contract stayed REST
- Built reusable API patterns (auth, error handling, pagination) that got adopted into the company-wide project framework

**At Toyota:**
- REST API layer on top of T-ONE for external system integrations (WMS, system manager)
- gRPC for internal service-to-service, REST for anything external

**Why I still use REST alongside GraphQL/gRPC:** Different tools for different consumers. External partners expect REST — it's the lingua franca of web APIs. No client library needed, works with any HTTP tool, cacheable at the HTTP level. For internal use, GraphQL and gRPC are better — but for "anyone should be able to call this," REST wins.

---

## Key Concepts

### What REST Is

REST (Representational State Transfer) is an architectural style for building web APIs using HTTP methods (GET, POST, PUT, DELETE) on resources identified by URLs. It's stateless — each request contains all the information needed to process it. REST is the most widely adopted API style because it's simple, well-understood, and works with any HTTP client. At Combination, we use REST for external partner APIs alongside GraphQL (frontends) and gRPC (internal services).

### Design Principles
- **Resource-oriented** — URLs represent resources (`/users/123`), HTTP methods represent actions (GET, POST, PUT, DELETE).
- **Stateless** — Each request contains all information needed. No session state on the server.
- **HATEOAS** — Hypermedia links in responses for discoverability. In practice, few APIs implement this fully.
- **Content negotiation** — Accept/Content-Type headers for JSON, XML, etc.

### Versioning
- **URL versioning** — `/v1/users`, `/v2/users`. Simple, clear, but URLs change.
- **Header versioning** — `Accept: application/vnd.api+json;version=2`. Cleaner URLs but harder to test.
- **At Combination** — We used URL versioning for REST, but moved to GraphQL's deprecation model (`@deprecated`) which avoids versioning entirely.

### HTTP Caching
- **ETags** — Server returns a hash of the resource. Client sends `If-None-Match` on next request. Server returns 304 if unchanged.
- **Cache-Control** — Headers controlling how long responses can be cached by browsers and CDNs.
- **REST advantage over GraphQL** — HTTP-level caching works out of the box. GraphQL POST requests aren't cacheable without persisted queries.

### Rate Limiting & Security
- **Rate limiting per endpoint** — Easy in REST because each endpoint has a distinct URL. Harder in GraphQL where all queries go to `/graphql`.
- **API keys** — Per-partner API keys for external REST endpoints. Tracked per key for usage analytics.
- **Input validation** — Validate request body against a schema. Return 400 with clear error messages.

### When to Use REST vs Alternatives
- **REST** — External APIs, simple CRUD, browser-accessible endpoints, CDN (Content Delivery Network)-cacheable content.
- **GraphQL** — Internal frontends with varying data needs, avoid over-fetching.
- **gRPC** — Service-to-service, high performance, streaming.

## Sorulursa

> [!faq]- "Why do you still use REST when you have GraphQL?"
> Different tools for different consumers. External partners expect REST — it's well-understood, easy to document with OpenAPI/Swagger, and works with any HTTP client. GraphQL requires a client library and understanding of the query language. For external APIs, simplicity wins.

> [!faq]- "How do you document REST APIs?"
> OpenAPI (Swagger) spec generated from code annotations. Swagger UI for interactive documentation. At Combination, each REST service exposes `/swagger` in non-production environments. We also publish API changelogs with each release.

---

*[[00-dashboard]]*
