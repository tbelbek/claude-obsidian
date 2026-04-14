---
tags:
  - education-kit
---
# REST APIs — Knowledge Base
> [!info] Architectural style for building web APIs using HTTP methods on resources — covering design principles, versioning, HTTP caching, rate limiting, and when to use REST vs alternatives.

---

## Key Concepts

### What REST Is
REST (Representational State Transfer) is an architectural style for building web APIs using HTTP methods (GET, POST, PUT, DELETE) on resources identified by URLs. It's stateless — each request contains all the information needed to process it. REST is the most widely adopted API style because it's simple, well-understood, and works with any HTTP client.

### Design Principles
- **Resource-oriented** — URLs represent resources (`/users/123`), HTTP methods represent actions (GET, POST, PUT, DELETE).
- **Stateless** — Each request contains all information needed. No session state on the server.
- **HATEOAS** — Hypermedia links in responses for discoverability. In practice, few APIs implement this fully.
- **Content negotiation** — Accept/Content-Type headers for JSON, XML, etc.

### Versioning
- **URL versioning** — `/v1/users`, `/v2/users`. Simple, clear, but URLs change.
- **Header versioning** — `Accept: application/vnd.api+json;version=2`. Cleaner URLs but harder to test.
- **GraphQL alternative** — GraphQL's deprecation model (`@deprecated`) avoids versioning entirely.

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

---

## Sorulursa

> [!faq]- "Why do you still use REST when you have GraphQL?"
> Different tools for different consumers. External partners expect REST — it's well-understood, easy to document with OpenAPI/Swagger, and works with any HTTP client. GraphQL requires a client library and understanding of the query language. For external APIs, simplicity wins.

> [!faq]- "How do you document REST APIs?"
> OpenAPI (Swagger) spec generated from code annotations. Swagger UI for interactive documentation. Each REST service exposes `/swagger` in non-production environments. API changelogs published with each release.
