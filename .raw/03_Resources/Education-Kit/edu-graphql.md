---
tags:
  - education-kit
---
# GraphQL — Knowledge Base
> [!info] Query language for APIs where the client specifies exactly what data it needs — covering federation, DataLoader, performance, security, versioning, and when NOT to use GraphQL.

---

## Key Concepts

### What GraphQL Is
GraphQL is a query language for APIs where the client specifies exactly what data it needs — no over-fetching, no under-fetching. Instead of multiple REST endpoints, there's one endpoint with a typed schema. The client sends a query, the server returns exactly that shape. Best for: frontend-facing APIs where different clients (web, mobile, admin) need different fields from the same data, and where reducing round-trips matters.

### Federation
- **What** — Multiple services each expose a GraphQL schema. A gateway composes them into one API.
- **How** — Each service registers its schema with a Schema Registry. The gateway fetches and composes them, giving the frontend one API surface instead of many endpoints — each service owns its schema, the gateway composes them.
- **Why** — Frontend sees one API. Backend teams own their own schemas independently.
- **Schema Registry** — Tracks which service owns which types. Gateway uses this for query routing.

### DataLoader & N+1 Problem
- **N+1 problem** — Query 10 users → 1 query for users + 10 queries for their orders = 11 queries. Classic GraphQL trap.
- **DataLoader** — Facebook's batching pattern. Collects all IDs requested in a single resolver execution cycle, then fetches them in one batch query. This can reduce endpoints from 11 DB calls (3 seconds) to 2 batched calls (200ms).
- **HotChocolate** — Built-in DataLoader support. You register a batch data loader and HotChocolate handles the batching automatically.

### Performance & Security
- **Query depth limiting** — Prevent deeply nested queries that consume server resources. Typically limited to 5 levels. Without depth limits, someone could write a deeply nested query that takes down the server.
- **Complexity analysis** — Assign cost to each field. Reject queries that exceed a total cost threshold.
- **Persisted queries** — Client sends a hash instead of the full query. Server looks up the query by hash. Prevents arbitrary queries and reduces bandwidth.
- **Introspection** — Disabled in production. Exposes the full schema to anyone who asks.

### Versioning
- **No API versioning** — Unlike REST (/v1, /v2), GraphQL deprecates fields with `@deprecated` and adds new ones. Old clients keep working with old fields. This eliminates version management — deprecate old fields, add new ones, no breaking changes.
- **Breaking change detection** — CI checks if schema changes are backward-compatible before allowing merge.

### When NOT to Use GraphQL
- **Simple CRUD APIs** — REST is simpler and has better HTTP-level caching.
- **External partners** — REST is more discoverable, easier to rate-limit per endpoint.
- **Service-to-service** — gRPC is faster and type-safe. Use gRPC between services, GraphQL only for frontend.

---

## Sorulursa

> [!faq]- "How do you handle schema evolution in a federated setup?"
> Each service owns its schema independently. The schema registry tracks all schemas and the gateway composes them. When a service adds new fields, it's backward-compatible — no coordination needed. When a service deprecates a field, it marks it with @deprecated and usage is tracked before removing it. Breaking change detection in CI prevents accidental removals.

> [!faq]- "How do you monitor GraphQL performance?"
> Track resolver execution time per field, query complexity scores, and error rates. The gateway logs slow queries (>500ms) with the full query plan showing which service calls took the longest. DataLoader batch sizes are monitored — if a batch is always size 1, the DataLoader isn't helping and there is a configuration issue.
