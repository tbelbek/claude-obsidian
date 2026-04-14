---
tags:
  - education-kit
---

# Microservice Patterns — Education Kit

## What Microservices Are

Microservices is an architectural style where an application is composed of small, independently deployable services, each owning its own data and communicating through APIs or events. Each service can be developed, deployed, and scaled independently by a small team. Best for: large systems with clear domain boundaries, multiple teams that need to release independently, and services with different scaling requirements. The trade-off: distributed systems complexity (network failures, data consistency, observability) replaces monolith complexity (merge conflicts, coupled deployments).

## Service Communication Patterns

- **Sync (gRPC, REST) vs Async (Kafka, RabbitMQ)** — Use sync when the caller needs an immediate response (e.g., fetching user profile for a page render). Use async when the caller doesn't need to wait (e.g., "order placed" event triggers notifications, analytics, inventory update).
- **API Gateway / BFF (Backend for Frontend)** — A gateway or federated schema composes multiple services into a single client-facing endpoint. Each service exposes its own subgraph or API, the gateway aggregates them. Clients get one endpoint, one schema.
- **Service discovery** — Kubernetes handles this with DNS-based service discovery. Each service gets a ClusterIP and a DNS name. No need for Consul or Eureka when everything runs in the same cluster.
- **Circuit breaker** — When a downstream service fails repeatedly, the circuit opens and calls fail fast instead of waiting for timeouts. Prevents cascading failures — one slow service shouldn't bring down the entire system.
- **Retry with exponential backoff** — Transient failures (network blip, temporary overload) are common in distributed systems. Retries with increasing delays plus jitter prevent thundering herd when a service recovers.

## Data Management

- **Database per service** — Each service owns its data, no shared databases. If another service needs that data, it goes through the API or subscribes to events. No shortcuts.
- **Event-driven data consistency** — Eventual consistency via domain events through a message broker. When a service changes its state, it publishes an event. Other services react and update their own data. The system is eventually consistent, not immediately consistent — and that's fine for most use cases.
- **Saga pattern** — Distributed transactions across services. Choreography: each service publishes events and the next service reacts (simpler, but harder to track). Orchestration: a central coordinator tells each service what to do (easier to monitor, but single point of logic).
- **CQRS** — Separate read/write models. Write side handles complex domain logic (state machines, validations), read side is a denormalized projection optimized for queries. Avoids the compromise of one model trying to serve both purposes.
- **Event sourcing** — Store events, not state. Rebuild current state by replaying events. Powerful for audit trails and temporal queries, but adds complexity (snapshotting, schema evolution, eventual consistency). Use it when you need a full history of changes. Overkill for simple CRUD services.

## Decomposition

- **Bounded contexts (DDD)** — Service boundaries align with business domains, not technical layers. Domain experts help define where one context ends and another begins.
- **Strangler fig pattern** — Migrating from monolith to microservices gradually. Route new features to new services while the monolith still handles existing functionality. Much safer than a big-bang rewrite.
- **When NOT to use microservices** — Complexity tax is real: distributed tracing, eventual consistency, network failures, deployment orchestration, data consistency headaches. If your team is small or the domain is simple, a well-structured modular monolith is faster to develop and easier to operate.

## Resilience

- **Circuit breaker** — Three states: closed (normal), open (failing, requests rejected immediately), half-open (testing, a few requests let through to check recovery). Configure thresholds per downstream service.
- **Bulkhead** — Isolate failures. Each downstream dependency gets its own connection pool / thread pool. If one slow service exhausts its pool, other calls to different services continue normally.
- **Timeout + retry** — Every external call needs a timeout. No exceptions. Retries with jitter prevent thundering herd.
- **Health checks** — Liveness (is the process alive?), readiness (can it handle traffic?), startup (has it finished initializing?). Custom health checks can verify database connectivity, consumer lag, and downstream service availability.
- **Graceful degradation** — When a dependency is down, return cached data, a default response, or a reduced feature set instead of a 500 error.

## Observability

- **Distributed tracing** — A trace ID flows through all services involved in a request. OpenTelemetry for instrumentation, Tempo/Jaeger for trace storage. Every gRPC/HTTP call propagates the trace context automatically.
- **Centralized logging** — Structured JSON logs with correlation IDs. All services ship logs to a centralized system. Searching by correlation ID shows the full request journey across services.
- **Metrics** — RED method per service: Rate (requests/sec), Errors (error rate), Duration (latency percentiles). Prometheus scrapes metrics, Grafana dashboards visualize them.
- **Alerting** — Rate-based, not per-event. "Error rate exceeded 5% over 5 minutes" is actionable. "One 500 error occurred" is noise. Every alert should have a runbook link.

## Deployment

- **Independent deployment** — Each service has its own CI/CD pipeline, its own release cycle. Teams deploy multiple times a day without coordinating with other teams. If you can't deploy independently, you have a distributed monolith.
- **Breaking change detection** — API schemas are validated for backward compatibility in CI. Adding fields is fine. Removing or renaming fields fails the build.
- **Feature flags** — Deploy code without releasing features. Code goes to production behind a flag, enabled gradually. If something goes wrong, flip the flag instead of rolling back a deployment.
- **Blue-green / Canary / Rolling** — Rolling deployments with readiness gates are the most common in Kubernetes. Canary deployments for risky changes — route a small percentage of traffic to the new version first.

## Microservices vs Monolith

- **Monolith advantages** — Simple to develop, test, deploy, and debug. One codebase, one database, one deployment unit. ACID transactions are trivial.
- **Monolith disadvantages** — Scaling is all-or-nothing. One bad deploy takes everything down. Technology lock-in. Large codebase becomes hard to understand. Team coupling.
- **Microservices advantages** — Independent deployment and scaling per service. Technology diversity. Team autonomy. Fault isolation. Smaller codebases per service.
- **Microservices disadvantages** — Distributed systems complexity. Operational overhead. Data consistency is hard. Requires mature DevOps.
- **When to choose monolith** — Small team (<10 developers), simple domain, no independent scaling needs, early-stage product where boundaries aren't clear yet.
- **When to choose microservices** — Independent scaling needed, multiple teams need to deploy independently, technology diversity is required, domain has clear bounded contexts.
- **Modular monolith** — Best of both: clear module boundaries inside a single deployable unit. Can be split into microservices later when the need arises. Recommended for any new project — start modular monolith, split when you have data to justify it.

## Anti-Patterns

- **Distributed monolith** — Services are deployed independently but tightly coupled through shared databases or synchronous call chains. If you can't deploy service A without also deploying service B, you have a distributed monolith with all the complexity and none of the benefits.
- **Chatty services** — Too many synchronous calls between services for a single user request. Batch calls, use async events, or reconsider service boundaries.
- **Shared database** — Two services reading/writing the same tables defeats the purpose of service independence.
- **Too many services too early** — Start with a modular monolith, split when you have clear boundaries and a genuine need for independent scaling or deployment.
- **No API versioning** — Breaking consumers without warning. Every public API needs a versioning strategy.

---

## Common Questions

**"How do you decide service boundaries?"**
Align service boundaries with DDD bounded contexts — each service maps to a business domain, not a technical layer. The key question is: "Can this team own, deploy, and operate this service independently?" If two services always change together, they should probably be one service.

**"How do you handle distributed transactions?"**
Avoid them whenever possible. Instead, use the saga pattern — a sequence of local transactions coordinated through events. Each step has a compensating action for rollback. The key insight: eventual consistency is acceptable for most business scenarios.

**"How do you debug issues across microservices?"**
Three pillars: distributed tracing (OpenTelemetry), centralized logging, and metrics (Prometheus/Grafana). Every request gets a trace ID that propagates through all services. Search by trace ID to see the full picture.

**"What's the biggest challenge with microservices?"**
Data consistency and operational complexity. With a monolith, you have one database transaction. With microservices, you have eventual consistency, saga patterns, and the possibility that one service processed an event but another didn't.
