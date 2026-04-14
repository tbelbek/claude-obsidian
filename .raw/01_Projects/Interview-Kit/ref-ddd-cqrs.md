---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# DDD & CQRS — Quick Reference

> [!info] How I've used it: At Toyota, T-ONE used DDD with CQRS across 30+ microservices. Domain events (VehicleStateStatusChanged, NodeStatusChangedEvent), aggregates per service, repository pattern, clean architecture layers (ApplicationCore/Infrastructure/API).

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Domain-Driven Design\|bounded contexts]] | each microservice owns a context, communicate via events | [[#Domain-Driven Design\|aggregates]] | root entities enforce consistency (Vehicle, Transport) |
| [[#Domain-Driven Design\|domain events]] | VehicleStateEnergyChanged, published via RabbitMQ at Toyota | [[#CQRS (Command Query Responsibility Segregation)\|CQRS]] | separate command/query paths where read/write models diverge |
| [[#Clean Architecture Layers\|clean architecture]] | ApplicationCore / Infrastructure / API layers at Toyota | [[#Repository Pattern\|repository pattern]] | generic repos per service, custom MongoDB extensions |
| [[#Event Sourcing vs Traditional State\|event sourcing vs state]] | events=full audit+replay, state=simple+familiar | | |

## HOW WE USED IT

At Toyota, the T-ONE platform followed Domain-Driven Design across 30+ microservices. Each service owned its domain — Vehicles, Transport, Missions, Workflows, Locations, Inventory. The architecture was clean: ApplicationCore for business logic and domain models, Infrastructure for data access (MongoDB repositories, RabbitMQ publishers), and API for REST controllers and DTOs.

CQRS was used in services where read and write models diverged — Workflow service had separate command handling and query paths. Domain events like `VehicleStateStatusChanged` and `NodeStatusChangedEvent` drove cross-service communication via RabbitMQ.

---

## Key Concepts

### What DDD and CQRS Are
Domain-Driven Design (DDD) is an approach to software design that aligns code structure with business domains — the code speaks the same language as the domain experts. CQRS (Command Query Responsibility Segregation) separates read and write models so each can be optimized independently. Together, they're powerful for complex business domains where the data you write looks different from the data you read. At Toyota, DDD bounded contexts naturally mapped to microservice boundaries.

### Domain-Driven Design
- **Bounded contexts** — Each microservice owns a bounded context. Vehicles service doesn't know about Transport internals. They communicate via domain events.
- **Aggregates** — Root entities that enforce consistency. Vehicle aggregate manages vehicle state, energy, configuration. Transport aggregate manages job state and assignments.
- **Domain events** — Things that happened in the domain. `VehicleStateEnergyChanged`, `NodeValueChangedEvent`. Published to RabbitMQ for other services to react.
- **Ubiquitous language** — The code uses the same terms as the domain experts. A "Transport" in code means the same thing as a "Transport" to warehouse operators.

### CQRS (Command Query Responsibility Segregation)
- **What** — Separate models for reads and writes. Commands change state, queries read state. Different data structures optimized for each.
- **At Toyota** — Workflow service used CQRS: commands created/updated workflow instances, queries read execution state and history. Write model was event-sourced, read model was a projection.
- **When to use** — When read and write patterns are very different. A vehicle dashboard reads 100x more than it writes. A transport creation form writes once and rarely reads.

### Clean Architecture Layers
- **ApplicationCore** — Business logic, domain models, use cases, domain event definitions. No infrastructure dependencies.
- **Infrastructure** — MongoDB repositories, RabbitMQ publishers, external API clients. Implements interfaces defined in ApplicationCore.
- **API** — REST controllers, DTOs, endpoint definitions. Thin layer — delegates to ApplicationCore.
- **WorkflowPlugin** — Services extend the workflow engine via plugins. Domain-specific activities (custom metrics, REST calls, Python scripts).

### Repository Pattern
- **What** — Abstraction over data access. ApplicationCore defines `IVehicleRepository`, Infrastructure implements it with MongoDB.
- **Why** — Testability (mock the repository in unit tests), flexibility (swap MongoDB for another store without changing business logic).
- **At Toyota** — Each service had its own repositories: `VehicleRepository`, `TransportRepository`, `MissionsRepository`, `WorkflowRepository`.

### Event Sourcing vs Traditional State
- **Traditional state storage** — Store current state directly. UPDATE replaces the old value. Simple, familiar, works for most cases. You lose history unless you add audit logging separately.
- **Event sourcing** — Store events (facts that happened), rebuild current state by replaying them. "OrderPlaced", "ItemAdded", "PaymentReceived" → current order state. Full audit trail built-in. Can rebuild state at any point in time. Can derive multiple read models from same events.
- **When to use event sourcing** — Financial systems (need full audit trail), workflow engines (state machines with complex transitions), systems requiring temporal queries ("what was the state at 3pm yesterday?"). *(at Toyota, Workflow service had complex state machines where event history was valuable)*
- **When NOT to use** — Simple CRUD (massive overkill), high-write-throughput systems (replay gets expensive), teams unfamiliar with the pattern (steep learning curve). Most microservices are better served by traditional state + domain events published to a message broker.
- **Event sourcing + CQRS** — Natural pairing. Write side stores events, read side projects them into denormalized views optimized for queries. Events become the integration mechanism between write and read models.

## Sorulursa

> [!faq]- "How do you decide service boundaries in DDD?"
> Look for natural domain boundaries. If two concepts always change together, they're probably in the same service. If they change independently, separate them. At Toyota: Vehicles and Transports seem related but change independently — a vehicle's energy level changes every second, a transport job is created once and completed once. Different lifecycles → different services.

> [!faq]- "How do you handle cross-service data consistency?"
> Eventual consistency via domain events. When a transport is assigned to a vehicle, the Transport service publishes `TransportAssigned`. The Vehicle service consumes it and updates its state. There's a brief window of inconsistency, but for our use case (warehouse operations), seconds of delay are acceptable. For cases where we need strong consistency, we use MongoDB transactions within a single service.

> [!faq]- "When is CQRS overkill?"
> For simple CRUD services. If your read and write models are the same shape, CQRS adds complexity without benefit. At Toyota, most services used plain repository pattern. Only Workflow and a few complex services needed CQRS. Don't add it everywhere — add it where the read/write patterns genuinely diverge.

---

*[[00-dashboard]]*
