---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# GraphQL (HotChocolate) — Quick Reference

> [!info] How I've used it: Led REST→GraphQL migration at Combination. 60+ microservices with federated schemas via HotChocolate Fusion. GP-GraphQL-Gateway + SchemaRegistry. DataLoader for N+1, query depth limiting, persisted queries.

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Federation (HotChocolate Fusion)\|federation (Fusion)]] | 60+ subgraphs composed at gateway, SchemaRegistry | [[#DataLoader & N+1 Problem\|DataLoader]] | batch+cache per request, 3s→200ms at Combination |
| [[#Performance & Security\|query depth limit]] | max 5 levels, complexity analysis prevents abuse | [[#Performance & Security\|persisted queries]] | client sends hash not query text, smaller+safer |
| [[#Performance & Security\|introspection]] | disabled in prod, schema via registry only | [[#Versioning\|no versioning]] | additive changes only, deprecate old fields |
| [[#When NOT to Use GraphQL\|when NOT GraphQL]] | file uploads, simple CRUD, external partners use REST | [[#HOW WE USE IT\|migration story]] | REST→GraphQL in 6 months, zero breaking changes |

## HOW WE USE IT

At Combination, I [[sd-graphql-migration|led the migration from REST to GraphQL]]. The platform has 60+ microservices, each exposing its own GraphQL schema with Query/Mutation/Subscription types. The GP-GraphQL-Gateway federates all schemas via HotChocolate Fusion, and the GP-GraphQL-SchemaRegistry tracks which service owns which types.

**What I built/changed:**
- Led the gradual migration from REST to federated GraphQL — 6 months, zero breaking changes for existing clients
- Set up the API style rules: GraphQL for internal frontends, gRPC for service-to-service, REST for external partners
- Fixed N+1 query problems using HotChocolate's DataLoader — one endpoint went from 3 seconds (11 DB calls) to 200ms (2 DB calls)
- Configured query depth limiting (max 5 levels) and complexity analysis to prevent query abuse
- Disabled introspection in production — schema exposed only through the registry, not via the API
- Set up persisted queries — clients send a hash instead of the full query text
- Breaking change detection in CI (`breaking.yml`) — schema changes checked for backward compatibility before merge

**Why GraphQL over REST for frontends:** The frontend was making 5-6 requests per page and over-fetching data. GraphQL lets the client describe exactly what data it needs in one request. With 60+ services behind a federated gateway, the frontend sees one API surface instead of 60 endpoints.

---

## Key Concepts

### What GraphQL Is
GraphQL is a query language for APIs where the client specifies exactly what data it needs — no over-fetching, no under-fetching. Instead of multiple REST endpoints, there's one endpoint with a typed schema. The client sends a query, the server returns exactly that shape. Best for: frontend-facing APIs where different clients (web, mobile, admin) need different fields from the same data, and where reducing round-trips matters.

### Federation (HotChocolate Fusion)
- **What** — Multiple services each expose a GraphQL schema. A gateway composes them into one API.
- **How** — Each service registers its schema with the SchemaRegistry. The gateway fetches and composes them. *(we used this to give the frontend one API surface instead of 60+ endpoints at Combination — each service owns its schema, the gateway composes them)*
- **Why** — Frontend sees one API. Backend teams own their own schemas independently.
- **Schema Registry** — Tracks which service owns which types. Gateway uses this for query routing.

### DataLoader & N+1 Problem
- **N+1 problem** — Query 10 users → 1 query for users + 10 queries for their orders = 11 queries. Classic GraphQL trap.
- **DataLoader** — Facebook's batching pattern. Collects all IDs requested in a single resolver execution cycle, then fetches them in one batch query. *(we used this to solve an N+1 problem at Combination — one endpoint went from 11 DB calls (3 seconds) to 2 batched calls (200ms))*
- **HotChocolate** — Built-in DataLoader support. You register a batch data loader and HotChocolate handles the batching automatically.

### Performance & Security
- **Query depth limiting** — Prevent deeply nested queries that consume server resources. We limit to 5 levels. *(we used this to prevent query complexity attacks at Combination — without depth limits, someone could write a deeply nested query that takes down the server)*
- **Complexity analysis** — Assign cost to each field. Reject queries that exceed a total cost threshold.
- **Persisted queries** — Client sends a hash instead of the full query. Server looks up the query by hash. Prevents arbitrary queries and reduces bandwidth. *(we used this to reduce bandwidth and prevent arbitrary queries at Combination — client sends a hash, server looks up the known query)*
- **Introspection** — Disabled in production. Exposes the full schema to anyone who asks.

### Versioning
- **No API versioning** — Unlike REST (/v1, /v2), GraphQL deprecates fields with `@deprecated` and adds new ones. Old clients keep working with old fields. *(we used this to eliminate version management at Combination — deprecate old fields, add new ones, no breaking changes, no /v1 vs /v2)*
- **Breaking change detection** — CI checks if schema changes are backward-compatible before allowing merge.

### When NOT to Use GraphQL
- **Simple CRUD APIs** — REST is simpler and has better HTTP-level caching.
- **External partners** — REST is more discoverable, easier to rate-limit per endpoint.
- **Service-to-service** — gRPC is faster and type-safe. We use gRPC between services, GraphQL only for frontend.

## Sorulursa

> [!faq]- "How do you handle schema evolution in a federated setup?"
> Each service owns its schema independently. The schema registry tracks all schemas and the gateway composes them. When a service adds new fields, it's backward-compatible — no coordination needed. When a service deprecates a field, it marks it with @deprecated and we track usage before removing it. Breaking change detection in CI prevents accidental removals.

> [!faq]- "How do you monitor GraphQL performance?"
> We track resolver execution time per field, query complexity scores, and error rates. The gateway logs slow queries (>500ms) with the full query plan showing which service calls took the longest. DataLoader batch sizes are monitored — if a batch is always size 1, the DataLoader isn't helping and we have a configuration issue.

---

*[[00-dashboard]]*
