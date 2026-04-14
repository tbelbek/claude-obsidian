---
tags:
  - education-kit
---

# Design Patterns — Education Kit

## What Design Patterns Are

Design patterns are reusable solutions to common software design problems. They're not code you copy — they're templates for structuring code so it's maintainable, testable, and extensible. In interviews, knowing when NOT to use a pattern is as important as knowing the pattern itself — premature abstraction is the enemy of simplicity.

## Creational

- **Factory** — Creating objects without specifying exact class. DI containers are essentially factories. In .NET, `IServiceProvider` and typed factories.
- **Builder** — Step-by-step construction. Common in schema builders, configuration builders, and test container builders.
- **Singleton** — Single instance for app lifetime. DI singleton services — careful with captured scoped dependencies (captive dependency problem).

## Structural

- **Decorator** — Wrap existing behavior with new behavior. Middleware pipelines are a classic example — each middleware decorates the next. Also: retry/circuit-breaker wrapping HTTP clients.
- **Adapter** — Convert one interface to another. Useful for abstracting different implementations behind a common interface (e.g., different database dialects).
- **Facade** — Simple interface over complex subsystem. An API gateway is a facade over many services.

## Behavioral

- **Strategy** — Swap algorithms at runtime. Example: different API access patterns (GraphQL resolver vs gRPC handler vs REST controller) accessing the same service logic.
- **Observer** — Notify subscribers when state changes. Domain events published to a message broker, multiple consumers react independently.
- **Template Method** — Define skeleton, subclasses fill steps. Test factory patterns — base setup, each test overrides specific config.
- **Chain of Responsibility** — Pass request through chain of handlers. Middleware pipelines — auth, logging, routing, endpoint.

## Architectural (Most Interview-Relevant)

- **Repository** — Abstraction over data access. Interface in domain, implementation in infrastructure. Testable, swappable.
- **Unit of Work** — Group multiple operations into one transaction. Database sessions that update multiple aggregates atomically.
- **CQRS** — Separate read/write models. Command handlers for writes, query handlers for reads.
- **Mediator** — Decouple sender from receiver. MediatR in .NET — controllers send commands, handlers process them, no direct dependency.
- **Event Sourcing** — Store events, derive state. Event log tables for integration events or full event sourcing for audit-critical domains.

## Anti-Patterns to Mention

- **God class** — One class doing everything. Break into smaller, focused classes. Single Responsibility Principle.
- **Service locator** — Resolving dependencies manually instead of injecting them. Use constructor injection. Service locator hides dependencies and makes testing harder.
- **Anemic domain model** — Domain objects with only getters/setters, all logic in services. Put behavior in the domain model. Entities should enforce their own invariants.

---

## Common Questions

**"What's the difference between Repository and Unit of Work?"**
Repository abstracts data access for a single aggregate — `IVehicleRepository` knows how to load and save vehicles. Unit of Work coordinates multiple repositories in a single transaction. The database session acts as the Unit of Work: begin session, call multiple repositories, commit once. Repository is about *what* you persist, Unit of Work is about *when* you persist.

**"When would you use CQRS vs simple CRUD?"**
CQRS makes sense when read and write models diverge significantly — different shapes, different scaling needs, different optimization strategies. For a simple settings page with low traffic, CRUD is perfectly fine. CQRS adds complexity — you need a good reason.

**"How do you decide which pattern to use?"**
Start with the problem, not the pattern. If you notice duplicated conditional logic switching between behaviors, that's Strategy. If you need to add behavior without modifying existing code, that's Decorator. Ask: what changes independently? What do I need to test in isolation? The pattern should simplify the code, not add ceremony.

**"What's wrong with the Service Locator pattern?"**
It hides dependencies — you can't look at a constructor and know what a class needs. It makes testing harder because you have to set up the entire container instead of just passing mocks. It fails at runtime instead of compile time. Constructor injection makes dependencies explicit and fails fast.

**"How does the middleware pipeline relate to design patterns?"**
A middleware pipeline is a textbook Chain of Responsibility — each middleware decides whether to handle the request or pass it to the next. It's also Decorator: each middleware wraps the next handler, adding behavior before/after. Authentication middleware checks the token, logging middleware records the request, exception middleware catches errors — each one is independent and composable.
