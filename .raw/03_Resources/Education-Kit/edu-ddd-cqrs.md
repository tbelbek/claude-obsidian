---
tags:
  - education-kit
---
# DDD & CQRS — Knowledge Base
> [!info] Domain-Driven Design and CQRS patterns for complex business domains — covering bounded contexts, aggregates, domain events, clean architecture, repository pattern, and event sourcing.

---

## Key Concepts

### What DDD and CQRS Are
Domain-Driven Design (DDD) is an approach to software design that aligns code structure with business domains — the code speaks the same language as the domain experts. CQRS (Command Query Responsibility Segregation) separates read and write models so each can be optimized independently. Together, they're powerful for complex business domains where the data you write looks different from the data you read. DDD bounded contexts naturally map to microservice boundaries.

### Domain-Driven Design
- **Bounded contexts** — Each microservice owns a bounded context. One service doesn't know about another's internals. They communicate via domain events.
- **Aggregates** — Root entities that enforce consistency. A Vehicle aggregate manages vehicle state, energy, configuration. A Transport aggregate manages job state and assignments.
- **Domain events** — Things that happened in the domain. `VehicleStateEnergyChanged`, `OrderPlaced`, `TransportAssigned`. Published to a message broker for other services to react.
- **Ubiquitous language** — The code uses the same terms as the domain experts. A "Transport" in code means the same thing as a "Transport" to domain specialists.

### CQRS (Command Query Responsibility Segregation)
- **What** — Separate models for reads and writes. Commands change state, queries read state. Different data structures optimized for each.
- **When to use** — When read and write patterns are very different. A dashboard reads 100x more than it writes. A creation form writes once and rarely reads.
- **When NOT to use** — For simple CRUD services. If your read and write models are the same shape, CQRS adds complexity without benefit.

### Clean Architecture Layers
- **ApplicationCore** — Business logic, domain models, use cases, domain event definitions. No infrastructure dependencies.
- **Infrastructure** — Database repositories, message publishers, external API clients. Implements interfaces defined in ApplicationCore.
- **API** — REST controllers, DTOs, endpoint definitions. Thin layer — delegates to ApplicationCore.

### Repository Pattern
- **What** — Abstraction over data access. ApplicationCore defines `IVehicleRepository`, Infrastructure implements it with the database.
- **Why** — Testability (mock the repository in unit tests), flexibility (swap database without changing business logic).

### Event Sourcing vs Traditional State
- **Traditional state storage** — Store current state directly. UPDATE replaces the old value. Simple, familiar, works for most cases. You lose history unless you add audit logging separately.
- **Event sourcing** — Store events (facts that happened), rebuild current state by replaying them. "OrderPlaced", "ItemAdded", "PaymentReceived" → current order state. Full audit trail built-in. Can rebuild state at any point in time. Can derive multiple read models from same events.
- **When to use event sourcing** — Financial systems (need full audit trail), workflow engines (state machines with complex transitions), systems requiring temporal queries ("what was the state at 3pm yesterday?").
- **When NOT to use** — Simple CRUD (massive overkill), high-write-throughput systems (replay gets expensive), teams unfamiliar with the pattern (steep learning curve). Most microservices are better served by traditional state + domain events published to a message broker.
- **Event sourcing + CQRS** — Natural pairing. Write side stores events, read side projects them into denormalized views optimized for queries. Events become the integration mechanism between write and read models.

---

## Sorulursa

> [!faq]- "How do you decide service boundaries in DDD?"
> Look for natural domain boundaries. If two concepts always change together, they're probably in the same service. If they change independently, separate them. Example: Vehicles and Transports seem related but change independently — a vehicle's energy level changes every second, a transport job is created once and completed once. Different lifecycles → different services.

> [!faq]- "How do you handle cross-service data consistency?"
> Eventual consistency via domain events. When a transport is assigned to a vehicle, the Transport service publishes `TransportAssigned`. The Vehicle service consumes it and updates its state. There's a brief window of inconsistency, but for most use cases, seconds of delay are acceptable. For cases where strong consistency is needed, use database transactions within a single service.

> [!faq]- "When is CQRS overkill?"
> For simple CRUD services. If your read and write models are the same shape, CQRS adds complexity without benefit. Most services should use plain repository pattern. Only complex services need CQRS. Don't add it everywhere — add it where the read/write patterns genuinely diverge.
