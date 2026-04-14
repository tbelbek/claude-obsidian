---
tags:
  - education-kit
---

# System Design — Education Kit

## What System Design Interviews Are

System design interviews test your ability to design large-scale distributed systems under constraints — traffic, storage, latency, availability, cost. You're evaluated on structured thinking, trade-off analysis, and practical experience — not memorized architectures. The key is showing how you break down an ambiguous problem into concrete technical decisions, using real numbers to justify component choices.

## Approach (5 Steps)

### Step 1: Clarify Requirements (2 min)

- **Functional** — What does the system do? What are the core use cases?
- **Non-functional** — How many users? Requests per second? Latency requirements? Availability target (99.9%)?
- **Constraints** — Budget? Team size? Existing infrastructure? Compliance requirements?
- **Ask questions** — Don't assume. "Should this be real-time or can we batch?" "How important is consistency vs availability?"

### Step 2: High-Level Design (5 min)

- Draw the main components: clients, load balancer, API layer, services, databases, caches, message queues
- Identify the data flow: request -> API -> service -> database -> response
- Choose communication patterns: sync (REST/gRPC) vs async (Kafka/RabbitMQ)
- Choose data storage: SQL vs NoSQL vs both (polyglot persistence)

### Step 3: Deep Dive (10 min)

- **Data model** — What are the main entities? How do they relate? SQL schema or document structure.
- **API design** — Key endpoints, request/response shapes, versioning.
- **Scaling** — What's the bottleneck? Database reads -> add cache. Database writes -> add queue. CPU -> add instances.
- **Caching** — What to cache, TTL, invalidation strategy.
- **Trade-offs** — Every decision has a trade-off. Name them explicitly.

### Step 4: Handle Edge Cases (3 min)

- What happens when the database is down?
- What happens with duplicate requests?
- What about data consistency across services?
- How do you handle spikes in traffic?

### Step 5: Observability & Operations (2 min)

- How do you monitor this system?
- How do you deploy changes?
- How do you debug issues in production?
- What alerts would you set up?

---

## Common System Design Questions & Angles

### "Design a URL shortener"

Simple CRUD + high read volume. Redis for hot URLs, PostgreSQL for persistence. Hash collision handling via base62 encoding with a counter or retry. Analytics pipeline via message queue — every redirect publishes an event, consumers aggregate click counts, referrers, geo data.

### "Design a notification system"

Event-driven architecture. Services publish events to a message broker, notification service consumes and routes (email/push/SMS). Priority queues for urgent vs marketing. Rate limiting per user to avoid spam. Template engine for message formatting. Delivery status tracking with retry.

### "Design a real-time dashboard"

Streaming data -> in-memory store (Redis Streams) -> dashboard reads latest position. SQL for historical queries and reporting. WebSocket for live updates to the browser. Aggregation layer for fleet-level metrics.

### "Design a file upload service"

Direct upload to blob storage (S3/Azure Blob) with pre-signed URLs — never proxy large files through your API. Metadata in database. Virus scanning via async queue. CDN for downloads. Chunked upload for large files with resume support.

### "Design a CI/CD pipeline"

Shared templates so teams don't reinvent the wheel. Quality gates: build -> test -> lint -> security scan -> deploy to staging -> smoke test -> deploy to prod. Breaking change detection for shared contracts. DORA metrics for measuring pipeline health.

### "Design a microservices platform"

Federated API gateway for external clients, gRPC for service-to-service, message broker for async events, container orchestration, environment-specific config, CI/CD per service, integration testing with containers. Service mesh for observability. Shared packages for cross-cutting concerns.

---

## Common Questions

**"How do you handle trade-offs in system design?"**
Every decision is a trade-off — consistency vs availability, simplicity vs scalability, build vs buy. Name the trade-off explicitly: "If we use eventual consistency here, we gain availability but users might see stale data for a few seconds. Is that acceptable for this use case?"

**"When would you choose SQL vs NoSQL?"**
SQL when you need ACID transactions, complex joins, or naturally relational data. NoSQL when your data is document-shaped, you need flexible schemas, or you need horizontal scaling for massive write throughput. You can use both in the same system (polyglot persistence).

**"How do you design for scalability from day one?"**
Don't over-engineer, but don't paint yourself into a corner. Stateless services for horizontal scaling. Database behind a repository interface. Async communication for operations that don't need immediate response. Feature flags to decouple deployment from release. Design for 10x current load, plan for 100x, have a strategy for 1000x — but don't build for 1000x on day one.

**"What's your approach to capacity planning?"**
Start with the numbers: expected users, requests per second, data growth rate. Work backwards to determine instance count, storage, and bandwidth. Use load testing to validate assumptions. Run periodic load tests before major launches.

**"How do you handle data consistency in a distributed system?"**
Accept that strong consistency across services is expensive and often unnecessary. Use the Saga pattern for distributed transactions. For read models, eventual consistency with events is usually fine. For critical flows, use the Outbox pattern: write to database and outbox table in the same transaction, a separate process publishes the event. Guarantees at-least-once delivery without distributed transactions.
