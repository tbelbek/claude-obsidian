---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Testing Strategy — Quick Reference

> [!info] How I've used it: At Combination, standardized testing across 60+ microservices — test pyramid from unit to E2E, Testcontainers for real dependencies, WebApplicationFactory for component tests, breaking change detection for gRPC/GraphQL. At Toyota, TextTest for fleet simulation. At KocSistem, built testing culture from scratch.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Test Pyramid\|test pyramid]] | unit→component→integration→DB→E2E→startup | [[#Test Frameworks & Tools\|frameworks]] | xUnit v3 + NSubstitute + FluentAssertions v7 |
| [[#Testcontainers\|Testcontainers]] | real MongoDB in Docker, not mocks, catches real bugs | [[#Testcontainers\|why not mocks]] | mocked tests passed, production broke — switched to containers |
| [[#WebApplicationFactory\|WebApplicationFactory]] | in-process test host, same middleware/DI/config | [[#Test Isolation\|test isolation]] | random DB names, shared container, IAsyncLifetime cleanup |
| [[#Breaking Change Detection\|breaking changes]] | buf breaking for gRPC, schema comparison for GraphQL | [[#E2E Test Patterns\|E2E patterns]] | C# gRPC + TypeScript GraphQL, full path tests |
| [[#CI Test Execution\|CI execution]] | dotnet test --warnaserror, TRX logging, env filtering | [[#Unit vs Integration vs E2E — When to Use Which\|unit vs integration vs E2E]] | many unit, fewer integration, few E2E — pyramid |
| [[#Mocking vs Real Dependencies\|mocking vs real]] | mock external APIs, real for DB/serialization | | |

## HOW WE TEST

When I joined Combination, each team had its own way of testing — some had unit tests, some had none, some mocked the database, some didn't. The first thing I did was standardize. Every service now follows the same test pyramid, the same project structure, the same tools.

The key decision was **Testcontainers over mocks**. We tried mocking MongoDB early on — tests passed, production broke. The mock didn't replicate real transaction behavior, index usage, or serialization edge cases. After that, every component and integration test runs against a real MongoDB container. Tests are slower (seconds instead of milliseconds) but they catch real bugs. That confidence trade-off was worth it.

Each service has a **test factory** that extends WebApplicationFactory — it spins up a MongoDB container, overrides the connection string, mocks external dependencies like Kafka producers, and creates typed gRPC clients. The test makes a real gRPC call, the service runs real logic against a real database, and the test asserts on both the response and the database state. It runs exactly as production would — same middleware, same DI, same config — just with a containerized database.

For **test isolation**, each test collection shares one MongoDB container (3-second startup amortized over 50+ tests), but each test gets a random database name. Tests run in parallel without interfering. After each test, cleanup happens via the async dispose pattern.

On the **CI side**, GitHub Actions runs `dotnet test` with strict settings — warnings as errors, TRX logging, XPlat code coverage. Tests are filtered by environment — staging and feature-flag tests skip in regular CI and run in dedicated pipelines. This keeps developer feedback fast.

For **breaking changes**, we have dedicated CI workflows: `buf breaking` for gRPC protos and `SchemaRegistry.Validation.Tests` for GraphQL schemas. With 60+ services and 100+ proto files, one breaking change can cascade. Catching it at PR time is 100x cheaper than catching it in production.

We also run **E2E tests** in two flavors: C# gRPC E2E tests that hit the service in-process with a full container stack, and TypeScript GraphQL E2E tests that hit the actual federated gateway to verify the full path from client to database and back.

**The test pyramid:**
- **Unit tests** — Business logic in isolation. xUnit + NSubstitute + FluentAssertions.
- **Component tests** — Service in-process with real MongoDB via Testcontainers.
- **Integration tests** — Full stack with real dependencies.
- **Database tests** — Data layer against real MongoDB with replica set.
- **E2E tests** — C# gRPC + TypeScript GraphQL.
- **Startup tests** — DI wiring, hosted services, health checks.
- **Breaking change tests** — gRPC proto + GraphQL schema compatibility.

---

## Key Concepts

### What a Testing Strategy Is
A testing strategy defines what to test, how to test it, and at what level — from fast unit tests to slow but comprehensive E2E tests. The goal is confidence that the system works correctly, without tests that are so slow or flaky they get ignored. A good strategy balances speed (fast feedback in CI) with coverage (catching real bugs before production). At Combination, we standardized the strategy across 60+ services so every team follows the same pyramid.

### Test Pyramid

| Layer | Project pattern | What it tests | Speed |
|-------|----------------|---------------|-------|
| Unit | `*.Tests.Unit` | Business logic, no I/O | Milliseconds |
| Component | `*.ComponentTests` | Service in-process + real DB | Seconds |
| Integration | `*.IntegrationTests` | Multiple services interacting | Seconds |
| Database | `*.Tests.Database` | Repository, queries, indexes | Seconds |
| E2E | `*.Tests.E2E` + `tests/e2e/` | Full request path end-to-end | Seconds |
| Load | `*.Tests.Load` | Performance under concurrent load | Minutes |
| Startup | `*.Tests.Startup` | DI container + endpoint verification | Seconds |

### Test Frameworks & Tools

| Tool | Purpose |
|------|---------|
| **xUnit v3** | Only test framework. No NUnit, no MSTest. Consistency across 60+ services. |
| **NSubstitute** | Primary mocking. Kafka producers, external API clients. |
| **FluentAssertions v7** | Fluent assertions. `result.Should().BeEquivalentTo(expected)`. |
| **Testcontainers.MongoDb** | Real MongoDB in Docker for component/integration tests. |
| **WebApplicationFactory** | ASP.NET Core in-process test host. Same middleware, DI, config. |
| **Custom Traits** | `EnvironmentAttribute` for filtering. `--filter "Environment!=Staging"`. |

### Testcontainers
- **What** — Spins up real Docker containers for test dependencies. Real MongoDB, not mocks.
- **Why not mocks** — We got burned early: mocked tests passed, production broke. Mocks don't catch query performance, index usage, transaction semantics, serialization edge cases. *(we switched to containers to solve this mock/prod divergence)*
- **Pattern** — `IAsyncLifetime` fixture: `InitializeAsync()` starts container, `DisposeAsync()` stops it. Tests get a real connection string.
- **Replica set** — MongoDB container with `WithReplicaSet()` — required for transaction support.
- **CI config** — `TESTCONTAINERS_RYUK_DISABLED=true` (Ryuk cleanup daemon not needed on ephemeral CI runners).

### WebApplicationFactory
- **What** — ASP.NET Core test host. Runs the service in-process without Kestrel. Same middleware, same DI, same config.
- **Pattern** — `ServiceFactory` extends `WebApplicationFactory<IServiceMarker>`. Overrides config to point to Testcontainers MongoDB. Mocks Kafka producers with NSubstitute. Creates typed gRPC channels for test clients.
- **Result** — Tests make real gRPC calls → service runs real logic → real MongoDB reads/writes → assertions on response + DB state.

### Test Isolation
- **Per-test database** — Random MongoDB database names. No test interference.
- **Shared containers** — `[Collection("...")]` shares one container across tests in the same collection. 3-second startup amortized over 50+ tests.
- **Cleanup** — `IAsyncLifetime` guarantees teardown even on failure. `RemoveAll<T>()` clears hosted services between tests.

### Breaking Change Detection
- **gRPC** — `buf breaking` compares proto files against base branch. Catches: removed fields, changed numbers, renamed messages. Runs in `breaking.yml` GitHub Actions workflow. *(we used this to prevent cascading breaks across 60+ services with 100+ proto files)*
- **GraphQL** — `SchemaRegistry.Validation.Tests` with `BreakingChangesTests.cs`. HotChocolate's `Utf8GraphQLParser` compares schemas. Catches: removed fields, changed types, federation violations. *(we used this to protect the federated gateway from service-level schema breaks)*

### E2E Test Patterns

**C# gRPC E2E:**
- xUnit + `IClassFixture<WebApplicationFixture>` with MongoDB Testcontainer
- Direct gRPC client calls via proto-generated stubs
- Theory-based parameterized tests
- Full path: gRPC call → service logic → MongoDB → response

**TypeScript GraphQL E2E:**
- Vitest test runner + `graphql-request` client
- Hits the actual gateway URL (configured via `.env`)
- Full federation path: client → gateway → domain service → response
- `globalSetup.ts` loads environment configuration

### CI Test Execution
- **Centralized** — `DevEnv-GitHub-Workflows/.github/workflows/check-common.yml` runs tests for every service
- **Command** — `dotnet test --warnaserror --configuration Debug --logger trx --collect:"XPlat Code Coverage" --filter "Environment!=Staging&Environment!=Feature"`
- **Strict** — `--warnaserror` means compiler warnings fail the build
- **Filtering** — Staging and feature-flag tests skipped in regular CI, run in dedicated deployment pipelines
- **Results** — TRX format in `.artifacts/reports/vstest/`. Code coverage per run.

### Unit vs Integration vs E2E — When to Use Which
- **Unit tests** — Test one class/function in isolation, mock dependencies. Fast (milliseconds), run on every save. Catch logic bugs. If you only have unit tests, you don't know if components work together.
- **Integration tests** — Test multiple components together with real dependencies (database, message queue). Slower (seconds) but catch wiring bugs, serialization issues, query problems. At Combination, Testcontainers runs real MongoDB. *(we caught bugs that unit tests with mocked MongoDB missed)*
- **E2E tests** — Test the full request path from client to database. Slowest but highest confidence. We run gRPC E2E (C# client → service → MongoDB) and GraphQL E2E (TypeScript client → gateway → domain service). *(we use both because they catch different classes of bugs)*
- **The pyramid** — Many unit tests (fast feedback), fewer integration tests (real dependencies), few E2E tests (full confidence). Inverting the pyramid (many E2E, few unit) leads to slow, flaky test suites.

### Mocking vs Real Dependencies
- **Mocking** — NSubstitute/Moq create fake implementations. Fast, deterministic, no infrastructure needed. Good for testing business logic in isolation. Bad for testing data access, serialization, query behavior.
- **Real dependencies (Testcontainers)** — Spin up real MongoDB/RabbitMQ in Docker. Slower but catches bugs mocks can't: index behavior, transaction semantics, serialization edge cases. *(we switched to Testcontainers after mocked tests passed but production broke — the mock didn't replicate real MongoDB transaction behavior)*
- **When to mock** — External APIs you don't control (Kafka producers, third-party services), expensive operations (email sending, payment processing), deterministic failure testing (force timeout, force error).
- **When to use real** — Database queries, message serialization, configuration loading, health checks. Anything where the interaction with the real system IS the thing you're testing.

## Sorulursa

> [!faq]- "Why Testcontainers instead of mocking the database?"
> We tried mocking MongoDB early on. Tests passed, production broke — the mock didn't replicate actual behavior with transactions, serialization, and index usage. Testcontainers give you a real database in a container. Tests are slower (seconds vs milliseconds) but they catch real bugs. The confidence trade-off is worth it.

> [!faq]- "How do you keep tests fast with Testcontainers?"
> Collection fixtures. Tests in the same `[Collection("...")]` share one MongoDB container. Container startup takes ~3 seconds, amortized across 50+ tests. Random database names ensure isolation within the shared container.

> [!faq]- "How do you handle E2E tests across microservices?"
> Two approaches. Backend-to-backend: C# gRPC E2E with WebApplicationFactory — each service tested with its own container stack. Frontend-to-backend: TypeScript GraphQL E2E hitting the federated gateway — tests verify the full path from client query through gateway to domain service. Both run in CI, E2E tests filtered by environment.

> [!faq]- "How do you test breaking changes in a federated GraphQL system?"
> SchemaRegistry has dedicated validation tests. When a service changes its schema, CI compares old vs new. Removed field or changed type → PR blocked. Catches federation breaks before they reach the gateway.

> [!faq]- "What's your test coverage strategy?"
> We collect XPlat Code Coverage on every CI run but don't enforce a percentage threshold — that leads to gaming. Instead: every new feature needs tests, every bug fix needs a regression test, component tests cover happy path + key error paths. Code review catches gaps better than coverage numbers.

> [!faq]- "How do you test gRPC services?"
> WebApplicationFactory hosts the service in-process. Create a GrpcChannel pointing to the test host, use the generated proto client to make calls. Assert on response + database state. For errors, verify correct gRPC status code (NOT_FOUND, INVALID_ARGUMENT, etc.).

---

*[[00-dashboard]]*
