---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Microservice Patterns — Senior Interview Questions

> [!tip] Covers architecture patterns, not specific tools. For tools see [[ref-graphql]], [[ref-grpc]], [[ref-kafka]], [[ref-rabbitmq]], [[ref-kubernetes]].

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Service Communication Patterns\|sync vs async]] | gRPC for queries, Kafka for events at Combination | [[#Data Management\|database per service]] | no cross-service DB access, each owns its data |
| [[#Data Management\|saga]] | distributed transaction across services, compensating actions | [[#Resilience\|circuit breaker]] | Polly in .NET, fail fast on repeated downstream failures |
| [[#Decomposition\|bounded contexts]] | DDD decomposition, one service per domain | [[#Observability\|observability]] | OTel traces, structured logs, health probes per service |
| [[#Deployment\|deployment]] | rolling updates, canary, blue-green, feature flags | [[#Anti-Patterns\|anti-patterns]] | distributed monolith, shared DB, chatty services |
| [[#Microservices vs Monolith\|micro vs monolith]] | start modular monolith, split when data justifies it | | |

---

## HOW WE USE IT

At Combination, 60+ microservices with federated GraphQL gateway, gRPC for service-to-service, Kafka for async events, Kubernetes for orchestration. At Toyota, 30+ microservices with DDD/CQRS, RabbitMQ for real-time messaging, MongoDB for document storage.

---

## Key Concepts

### What Microservices Are
Microservices is an architectural style where an application is composed of small, independently deployable services, each owning its own data and communicating through APIs or events. Each service can be developed, deployed, and scaled independently by a small team. Best for: large systems with clear domain boundaries, multiple teams that need to release independently, and services with different scaling requirements. The trade-off: distributed systems complexity (network failures, data consistency, observability) replaces monolith complexity (merge conflicts, coupled deployments).

### Service Communication Patterns
- **Sync (gRPC, REST) vs Async (Kafka, RabbitMQ)** — Use sync when the caller needs an immediate response (e.g., fetching user profile for a page render). Use async when the caller doesn't need to wait (e.g., "order placed" event triggers notifications, analytics, inventory update). At Combination, gRPC for queries between services, Kafka for domain events.
- **API Gateway / BFF (Backend for Frontend)** — Our federated GraphQL gateway acts as the API gateway. Each microservice exposes a subgraph, Apollo Router composes them. Clients get one endpoint, one schema. No need for a separate BFF layer — GraphQL already lets each client request exactly the fields it needs.
- **Service discovery** — Kubernetes handles this with DNS-based service discovery. Each service gets a ClusterIP and a DNS name (e.g., `user-service.default.svc.cluster.local`). No need for Consul or Eureka — K8s DNS is enough when everything runs in the same cluster.
- **Circuit breaker** — Polly in .NET. When a downstream service fails repeatedly, the circuit opens and calls fail fast instead of waiting for timeouts. Prevents cascading failures — one slow service shouldn't bring down the entire system.
- **Retry with exponential backoff** — Transient failures (network blip, temporary overload) are common in distributed systems. Polly retries with increasing delays (e.g., 1s, 2s, 4s) plus jitter to avoid thundering herd. Every external call in our services goes through a Polly policy.

### Data Management
- **Database per service** — Each service owns its data, no shared databases. At both Combination and Toyota, every microservice has its own database (PostgreSQL, MongoDB, etc.). If another service needs that data, it goes through the API or subscribes to events. No shortcuts.
- **Event-driven data consistency** — Eventual consistency via domain events through Kafka (Combination) or RabbitMQ (Toyota). When a service changes its state, it publishes an event. Other services react and update their own data. The system is eventually consistent, not immediately consistent — and that's fine for most use cases.
- **Saga pattern** — Distributed transactions across services. Choreography: each service publishes events and the next service reacts (simpler, but harder to track). Orchestration: a central coordinator tells each service what to do (easier to monitor, but single point of logic). We use choreography for simple flows, orchestration for complex multi-step processes.
- **CQRS** — Separate read/write models. Used at Toyota for the Workflow service — write side handles complex domain logic (state machines, validations), read side is a denormalized projection optimized for queries. Avoids the compromise of one model trying to serve both purposes.
- **Event sourcing** — Store events, not state. Rebuild current state by replaying events. Powerful for audit trails and temporal queries, but adds complexity (snapshotting, schema evolution, eventual consistency). Use it when you need a full history of changes (financial transactions, workflow states). Overkill for simple CRUD services.

### Decomposition
- **Bounded contexts (DDD)** — Service boundaries align with business domains, not technical layers. At Toyota, each bounded context (Workflow, Inventory, User Management) became its own microservice with its own data store and ubiquitous language. The domain experts helped define where one context ends and another begins.
- **Strangler fig pattern** — Migrating from monolith to microservices gradually. Route new features to new services while the monolith still handles existing functionality. Over time, strangle the monolith by extracting pieces one by one. Much safer than a big-bang rewrite.
- **When NOT to use microservices** — Complexity tax is real: distributed tracing, eventual consistency, network failures, deployment orchestration, data consistency headaches. If your team is small or the domain is simple, a well-structured modular monolith is faster to develop and easier to operate. Start monolithic, split when you have clear boundaries and a reason to scale independently.

### Resilience
- **Circuit breaker** — Three states: closed (normal, requests flow through), open (failing, requests rejected immediately), half-open (testing, a few requests let through to check recovery). Polly implements this in .NET. We configure thresholds per downstream service — critical services get shorter timeouts and faster circuit breaks.
- **Bulkhead** — Isolate failures. Each downstream dependency gets its own connection pool / thread pool. If one slow service exhausts its pool, other calls to different services continue normally. Like watertight compartments on a ship — one breach doesn't sink the whole thing.
- **Timeout + retry** — Every external call needs a timeout. No exceptions. Without a timeout, one hung service holds threads indefinitely. Retries with jitter (randomized delay) prevent thundering herd when a service recovers and all clients retry simultaneously.
- **Health checks** — Liveness (is the process alive?), readiness (can it handle traffic?), startup (has it finished initializing?). We use custom health checks at Combination that verify database connectivity, Kafka consumer lag, and downstream service availability. Kubernetes uses these to route traffic and restart unhealthy pods.
- **Graceful degradation** — When a dependency is down, return cached data, a default response, or a reduced feature set instead of a 500 error. Example: if the recommendation service is down, show popular items instead of personalized ones. The user gets a slightly worse experience, not a broken page.

### Observability
- **Distributed tracing** — A trace ID flows through all services involved in a request. When a user reports slowness, we look up the trace and see exactly which service took how long. We use OpenTelemetry for instrumentation, Tempo for trace storage. Every gRPC/HTTP call propagates the trace context automatically.
- **Centralized logging** — Structured JSON logs with correlation IDs. All services ship logs via Promtail to Loki. Searching by correlation ID shows the full request journey across services. Without centralized logging, debugging distributed systems is guesswork.
- **Metrics** — RED method per service: Rate (requests/sec), Errors (error rate), Duration (latency percentiles). Prometheus scrapes metrics, Grafana dashboards visualize them. Each service exposes `/metrics` endpoint. We alert on anomalies, not absolute thresholds.
- **Alerting** — Rate-based, not per-event. "Error rate exceeded 5% over 5 minutes" is actionable. "One 500 error occurred" is noise. PagerDuty for on-call, with escalation policies. Every alert should have a runbook link.

### Deployment
- **Independent deployment** — Each service has its own CI/CD pipeline, its own release cycle. Teams deploy multiple times a day without coordinating with other teams. This is the whole point of microservices — if you can't deploy independently, you have a distributed monolith.
- **Breaking change detection** — gRPC proto files and GraphQL schemas are validated for backward compatibility in CI. Adding fields is fine. Removing or renaming fields fails the build. We catch breaking changes before they reach production, not after consumers start failing.
- **Feature flags** — Deploy code without releasing features. Code goes to production behind a flag, enabled gradually (percentage rollout, specific users, specific regions). If something goes wrong, flip the flag instead of rolling back a deployment.
- **Blue-green / Canary / Rolling** — We use rolling deployments with readiness gates in Kubernetes. New pods start, pass health checks, then old pods are terminated. If readiness checks fail, the rollout stops automatically. Canary deployments for risky changes — route a small percentage of traffic to the new version first.

### Microservices vs Monolith
- **Monolith advantages** — Simple to develop, test, deploy, and debug. One codebase, one database, one deployment unit. No network latency between components, no distributed transaction headaches, no eventual consistency. ACID transactions are trivial. A well-structured modular monolith can serve many teams effectively.
- **Monolith disadvantages** — Scaling is all-or-nothing (can't scale just the hot component). One bad deploy takes everything down. Technology lock-in (entire app must use the same language/framework). Large codebase becomes hard to understand and modify. Long CI/CD times as codebase grows. Team coupling — merge conflicts, coordination overhead.
- **Microservices advantages** — Independent deployment and scaling per service. Technology diversity (Python ML service alongside .NET API). Team autonomy — each team owns and operates its service. Fault isolation — one service crash doesn't bring down the system. Smaller codebases per service, easier to understand and onboard.
- **Microservices disadvantages** — Distributed systems complexity: network failures, eventual consistency, distributed tracing, saga patterns. Operational overhead: monitoring 60+ services, managing deployments, debugging across service boundaries. Data consistency is hard — no cross-service transactions. Requires mature DevOps (CI/CD, observability, container orchestration).
- **When to choose monolith** — Small team (<10 developers), simple domain, no independent scaling needs, early-stage product where boundaries aren't clear yet. *(KocSistem started as a monolith — appropriate for the team size and domain)*
- **When to choose microservices** — Independent scaling needed (one service gets 100x traffic), multiple teams need to deploy independently, technology diversity is required, domain has clear bounded contexts. *(Combination: 60+ services evolved as team and product grew. Toyota: DDD bounded contexts made the split natural)*
- **Modular monolith** — Best of both: clear module boundaries inside a single deployable unit. Modules communicate through well-defined interfaces, not direct database access. Can be split into microservices later when the need arises. *(this is what I'd recommend for any new project — start modular monolith, split when you have data to justify it)*

### Anti-Patterns
- **Distributed monolith** — Services are deployed independently but tightly coupled through shared databases or synchronous call chains. If you can't deploy service A without also deploying service B, you don't have microservices — you have a distributed monolith with all the complexity and none of the benefits.
- **Chatty services** — Too many synchronous calls between services for a single user request. If rendering one page requires 15 sequential service calls, performance is terrible and failure probability is high. Batch calls, use async events, or reconsider service boundaries.
- **Shared database** — Two services reading/writing the same tables defeats the purpose of service independence. Schema changes in one service break the other. Each service owns its data — no exceptions.
- **Too many services too early** — Start with a modular monolith, split when you have clear boundaries and a genuine need for independent scaling or deployment. Premature decomposition leads to wrong boundaries that are painful to refactor later.
- **No API versioning** — Breaking consumers without warning. Every public API (gRPC, GraphQL, REST) needs a versioning strategy. Deprecate old versions, give consumers time to migrate, then remove.

---

## Sorulursa

> [!faq]- "How do you decide service boundaries?"
> We align service boundaries with DDD bounded contexts — each service maps to a business domain, not a technical layer. At Toyota, domain experts helped define where one context ends and another begins (Workflow, Inventory, User Management). The key question is: "Can this team own, deploy, and operate this service independently?" If two services always change together, they should probably be one service.

> [!faq]- "How do you handle distributed transactions?"
> We avoid them whenever possible. Instead, we use the saga pattern — a sequence of local transactions coordinated through events. At Combination, choreography-based sagas via Kafka for simple flows (service publishes event, next service reacts). For complex multi-step processes, orchestration-based sagas where a coordinator manages the sequence. Each step has a compensating action for rollback. The key insight: eventual consistency is acceptable for most business scenarios.

> [!faq]- "Microservices vs monolith — when do you choose which?"
> Start with a modular monolith unless you have a clear reason not to. Microservices make sense when you need independent scaling (one service gets 100x more traffic), independent deployment (teams can't release without coordinating), or technology diversity (one service needs Python ML, another needs .NET). At Toyota, we started with clear domain boundaries from DDD, which made the microservice split natural. At Combination, the 60+ services evolved over time as the team and product grew.

> [!faq]- "How do you handle data consistency across services?"
> Eventual consistency through domain events. When a service changes its state, it publishes an event to Kafka (Combination) or RabbitMQ (Toyota). Other services consume and update their local data. For cases where consistency is critical (e.g., payment processing), we use the saga pattern with compensating actions. The trick is designing the system so that brief inconsistency windows are acceptable to the business — and they almost always are.

> [!faq]- "How do you debug issues across microservices?"
> Three pillars: distributed tracing (OpenTelemetry to Tempo), centralized logging (Promtail to Loki), and metrics (Prometheus to Grafana). Every request gets a trace ID that propagates through all services. When something fails, I search by trace ID in Loki to see logs from every service involved, then check the trace in Tempo to see timing and error details. Without this observability stack, debugging distributed systems is like finding a needle in 60 haystacks.

> [!faq]- "What's the biggest challenge with microservices?"
> Data consistency and operational complexity. With a monolith, you have one database transaction. With microservices, you have eventual consistency, saga patterns, and the possibility that one service processed an event but another didn't. The second challenge is observability — when something breaks, the cause might be three services away from the symptom. At Combination, we invested heavily in our observability stack (OpenTelemetry, Loki, Tempo, Grafana) to make this manageable.

> [!faq]- "How do you handle service-to-service authentication?"
> Inside the Kubernetes cluster, we use mTLS (mutual TLS) for service-to-service communication — both sides verify each other's certificates. For gRPC calls, this is handled at the infrastructure level. External traffic goes through the GraphQL gateway, which handles user authentication (JWT tokens). The gateway passes the authenticated user context to downstream services via gRPC metadata. No service trusts another service blindly.

> [!faq]- "How do you prevent a distributed monolith?"
> Three rules: each service owns its data (no shared databases), services communicate through well-defined APIs or events (no backdoor data access), and each service can be deployed independently. At Combination, we enforce this through CI — schema compatibility checks for GraphQL and gRPC, independent pipelines per service. If deploying one service requires deploying another, we treat it as a design smell and refactor the boundary. The litmus test: can you deploy and release this service without talking to any other team?

---

*[[00-dashboard]]*
