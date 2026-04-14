---
tags:
  - interview-kit
  - interview-kit/reference
up: "[[00-dashboard]]"
---

*[[00-dashboard]]*

# Design Patterns — Senior Interview Questions

> [!tip] Patterns I actually use in production. Not a catalog of 23 GoF patterns — focused on the ones that come up in .NET microservice interviews.

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Architectural (Most Interview-Relevant)\|Repository]] | data access abstraction, MongoDB repos at Toyota | [[#Architectural (Most Interview-Relevant)\|CQRS]] | separate read/write models, used in Workflow service |
| [[#Creational\|Factory]] | DI container is a factory, IServiceProvider in .NET | [[#Creational\|Builder/Singleton]] | fluent config, DI singleton lifetime |
| [[#Behavioral\|Strategy]] | API style selection: GraphQL/gRPC/REST at Combination | [[#Behavioral\|Observer]] | domain events via Kafka/RabbitMQ, pub/sub pattern |
| [[#Structural\|Decorator]] | middleware pipeline, logging, caching wrappers | [[#Architectural (Most Interview-Relevant)\|Mediator]] | MediatR for CQRS commands/queries, decouples handlers |
| [[#Anti-Patterns to Mention\|anti-patterns]] | god class, service locator, anemic domain model | | |

---

## HOW WE USE THEM

At Combination, patterns are embedded in the architecture: Repository pattern for data access, Factory for service resolution, Strategy for API style selection (GraphQL/gRPC/REST), Observer via domain events through Kafka. At Toyota, DDD tactical patterns: Aggregates, Domain Events, Repository, Unit of Work with MongoDB transactions.

---

### What Design Patterns Are

Design patterns are reusable solutions to common software design problems. They're not code you copy — they're templates for structuring code so it's maintainable, testable, and extensible. In interviews, knowing when NOT to use a pattern is as important as knowing the pattern itself — premature abstraction is the enemy of simplicity.

## Patterns I Use Daily

### Creational

- **Factory** — Creating objects without specifying exact class. DI container is essentially a factory. *We use `IServiceProvider` and typed factories in .NET.*
- **Builder** — Step-by-step construction. *HotChocolate schema builder, MongoDB container builder in Testcontainers.*
- **Singleton** — Single instance for app lifetime. *DI singleton services — careful with captured scoped dependencies (captive dependency problem).*

### Structural

- **Decorator** — Wrap existing behavior with new behavior. *Middleware pipeline in ASP.NET Core — each middleware decorates the next. Also: Polly retry/circuit-breaker wrapping HttpClient.*
- **Adapter** — Convert one interface to another. *Oracle adapter layers at KocSistem — different SQL dialects behind same interface.*
- **Facade** — Simple interface over complex subsystem. *GraphQL gateway is a facade over 60+ services.*

### Behavioral

- **Strategy** — Swap algorithms at runtime. *API style selection: GraphQL resolver vs gRPC handler vs REST controller — same service, different access patterns.*
- **Observer** — Notify subscribers when state changes. *Domain events: `VehicleStateChanged` published to RabbitMQ, multiple consumers react independently.*
- **Template Method** — Define skeleton, subclasses fill steps. *`WebApplicationFactory` test pattern — base setup, each test overrides specific config.*
- **Chain of Responsibility** — Pass request through chain of handlers. *ASP.NET Core middleware pipeline — auth → logging → routing → endpoint.*

### Architectural (Most Interview-Relevant)

- **Repository** — Abstraction over data access. Interface in domain, implementation in infrastructure. *Every service at Toyota had `IVehicleRepository`, `ITransportRepository` — testable, swappable.*
- **Unit of Work** — Group multiple operations into one transaction. *MongoDB sessions at Toyota — update Vehicle + Transport atomically.*
- **CQRS** — Separate read/write models. *Toyota Workflow service — command handlers for writes, query handlers for reads.*
- **Mediator** — Decouple sender from receiver. *MediatR in .NET — controllers send commands, handlers process them, no direct dependency.*
- **Event Sourcing** — Store events, derive state. *Toyota had event log tables for integration events — not full event sourcing but the pattern influenced the design.*

### Anti-Patterns to Mention

- **God class** — One class doing everything. Break into smaller, focused classes. Single Responsibility Principle.
- **Service locator** — Resolving dependencies manually instead of injecting them. Use constructor injection. Service locator hides dependencies and makes testing harder.
- **Anemic domain model** — Domain objects with only getters/setters, all logic in services. Put behavior in the domain model. Entities should enforce their own invariants.

---

## Sorulursa

### "What's the difference between Repository and Unit of Work?"

Repository abstracts data access for a single aggregate — `IVehicleRepository` knows how to load and save vehicles. Unit of Work coordinates multiple repositories in a single transaction. In practice at Toyota, the MongoDB session acted as the Unit of Work: begin session, call multiple repositories, commit once. Repository is about *what* you persist, Unit of Work is about *when* you persist.

### "When would you use CQRS vs simple CRUD?"

CQRS makes sense when read and write models diverge significantly — different shapes, different scaling needs, different optimization strategies. At Toyota Workflow, commands validated complex business rules and wrote normalized data, while queries returned denormalized views optimized for the UI. For a simple settings page with low traffic, CRUD is perfectly fine. CQRS adds complexity — you need a good reason.

### "How do you decide which pattern to use?"

Start with the problem, not the pattern. If I notice duplicated conditional logic switching between behaviors, that's Strategy. If I need to add behavior without modifying existing code, that's Decorator. I ask: what changes independently? What do I need to test in isolation? What varies? The pattern should simplify the code, not add ceremony. If applying a pattern makes the code harder to understand, it's the wrong pattern.

### "What's wrong with the Service Locator pattern?"

It hides dependencies — you can't look at a constructor and know what a class needs. It makes testing harder because you have to set up the entire container instead of just passing mocks. It violates the Dependency Inversion Principle. And it fails at runtime instead of compile time — if a dependency is missing, you get a runtime exception instead of a build error. Constructor injection makes dependencies explicit and fails fast.

### "Give an example of Strategy pattern in your code"

At Combination, each service can be accessed via GraphQL, gRPC, or REST. The core business logic is the same — `IOrderService.GetOrders()`. But how the request comes in and how the response is shaped differs. The GraphQL resolver, gRPC handler, and REST controller are strategies for accessing the same service. We select the strategy based on the client's needs: mobile app uses GraphQL for flexible queries, internal services use gRPC for performance, third-party integrations use REST for compatibility.

### "How does the middleware pipeline relate to design patterns?"

ASP.NET Core's middleware pipeline is a textbook Chain of Responsibility — each middleware decides whether to handle the request or pass it to the next. It's also Decorator: each middleware wraps the next `RequestDelegate`, adding behavior before/after. Authentication middleware checks the token, logging middleware records the request, exception middleware catches errors — each one is independent and composable. This is why you can reorder middleware and get different behavior.

### "How do you prevent retry amplification when Polly Decorators are chained across a deep service call chain?"

**The Problem:** When each service in a call chain independently wraps its HttpClient with Polly retry + timeout policies (Decorator pattern), retries multiply at each hop. Service A (3 retries × 2s) calling Service B (3 retries × 2s) calling Service C (3 retries × 2s) means a single request can cascade to 3 × (2 + 3 × 2) = 24 seconds worst-case at just 2 hops. At 4-5 hops deep, this grows exponentially and can saturate thread pools, exhaust connections, and bring down the entire chain under load.

**The Solution — Timeout Budget Pattern:**
1. **Global timeout budget:** The entry point (API gateway or first service) sets a total deadline for the entire operation (e.g., 5 seconds). This deadline propagates via a header (`X-Request-Deadline` or gRPC's `grpc-timeout`). Each downstream service subtracts elapsed time and respects the remaining budget — if only 1s remains, there's no point retrying with a 2s timeout.
2. **Retry budget per hop:** Reduce retries as you go deeper. Edge services get 2-3 retries, mid-tier services get 1 retry, leaf services get 0 retries (just fail fast). The deeper you are, the less room for retries.
3. **Circuit breaker as the outer decorator:** Polly's circuit breaker should wrap the retry policy, not the other way around. When a downstream service is consistently failing, the circuit breaker trips and stops retries entirely — preventing the amplification from even starting. Configure: 50% failure rate over 10-second window → open circuit for 30s.
4. **Hedged requests instead of retries:** For latency-sensitive paths, send a parallel (hedged) request to a second instance after a short delay (e.g., p99 latency) rather than waiting for timeout + retry. First response wins.
5. **Backpressure signals:** Return `429 Too Many Requests` or `503 Service Unavailable` with `Retry-After` headers when a service is overloaded. Callers should respect these and NOT retry immediately.

**Decorator composition order in Polly:**
```
Outer → Circuit Breaker → Retry → Timeout (per-attempt) → HttpClient
```
The outer timeout (total) wraps everything: if the global budget expires, all inner retries are cancelled via CancellationToken propagation.

**Real-world rule of thumb:** Total timeout at hop N = (Total timeout at hop N-1) / (max retries + 1). This ensures retries at each level fit within the parent's budget.
