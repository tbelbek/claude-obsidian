---
tags:
  - education-kit
---

# Testing Strategy — Education Kit

## What a Testing Strategy Is

A testing strategy defines what to test, how to test it, and at what level — from fast unit tests to slow but comprehensive E2E tests. The goal is confidence that the system works correctly, without tests that are so slow or flaky they get ignored. A good strategy balances speed (fast feedback in CI) with coverage (catching real bugs before production).

## Test Pyramid

| Layer | Project Pattern | What It Tests | Speed |
|-------|----------------|---------------|-------|
| Unit | `*.Tests.Unit` | Business logic, no I/O | Milliseconds |
| Component | `*.ComponentTests` | Service in-process + real DB | Seconds |
| Integration | `*.IntegrationTests` | Multiple services interacting | Seconds |
| Database | `*.Tests.Database` | Repository, queries, indexes | Seconds |
| E2E | `*.Tests.E2E` | Full request path end-to-end | Seconds |
| Load | `*.Tests.Load` | Performance under concurrent load | Minutes |
| Startup | `*.Tests.Startup` | DI container + endpoint verification | Seconds |

## Test Frameworks & Tools

| Tool | Purpose |
|------|---------|
| **xUnit** | Test framework for .NET. Consistency across services. |
| **NSubstitute** | Mocking library. Useful for external API clients, message producers. |
| **FluentAssertions** | Fluent assertion syntax. `result.Should().BeEquivalentTo(expected)`. |
| **Testcontainers** | Real dependencies (e.g., MongoDB, PostgreSQL) in Docker for component/integration tests. |
| **WebApplicationFactory** | ASP.NET Core in-process test host. Same middleware, DI, config as production. |

## Testcontainers

- **What** — Spins up real Docker containers for test dependencies. Real databases, not mocks.
- **Why not mocks** — Mocked tests can pass while production breaks. Mocks don't catch query performance, index usage, transaction semantics, serialization edge cases.
- **Pattern** — `IAsyncLifetime` fixture: `InitializeAsync()` starts container, `DisposeAsync()` stops it. Tests get a real connection string.
- **Replica set** — For databases like MongoDB, use replica set mode for transaction support.
- **CI config** — `TESTCONTAINERS_RYUK_DISABLED=true` (Ryuk cleanup daemon not needed on ephemeral CI runners).

## WebApplicationFactory

- **What** — ASP.NET Core test host. Runs the service in-process without Kestrel. Same middleware, same DI, same config.
- **Pattern** — Extend `WebApplicationFactory<TStartup>`. Override config to point to Testcontainers database. Mock external dependencies. Create typed API clients for tests.
- **Result** — Tests make real API calls, the service runs real logic against a real database, and you assert on both the response and the database state.

## Test Isolation

- **Per-test database** — Random database names. No test interference.
- **Shared containers** — Collection fixtures share one container across tests in the same collection. Container startup amortized over many tests.
- **Cleanup** — `IAsyncLifetime` guarantees teardown even on failure.

## Breaking Change Detection

- **gRPC** — `buf breaking` compares proto files against base branch. Catches: removed fields, changed numbers, renamed messages. Runs in CI workflows.
- **GraphQL** — Schema comparison tests. Compare old vs new schemas. Catches: removed fields, changed types, federation violations.

## E2E Test Patterns

**Backend E2E:**
- Test framework + fixture with containerized dependencies
- Direct API client calls via generated stubs
- Full path: API call -> service logic -> database -> response

**Frontend-to-Backend E2E:**
- Test runner + API client hitting the actual gateway
- Full path: client -> gateway -> domain service -> response
- Environment configuration loaded at setup time

## CI Test Execution

- **Strict settings** — Warnings as errors, structured logging, code coverage collection
- **Filtering** — Environment-specific tests (staging, feature-flag) skipped in regular CI, run in dedicated pipelines
- **Results** — Structured format output. Code coverage per run.

## Unit vs Integration vs E2E — When to Use Which

- **Unit tests** — Test one class/function in isolation, mock dependencies. Fast (milliseconds), run on every save. Catch logic bugs. If you only have unit tests, you don't know if components work together.
- **Integration tests** — Test multiple components together with real dependencies (database, message queue). Slower (seconds) but catch wiring bugs, serialization issues, query problems.
- **E2E tests** — Test the full request path from client to database. Slowest but highest confidence.
- **The pyramid** — Many unit tests (fast feedback), fewer integration tests (real dependencies), few E2E tests (full confidence). Inverting the pyramid (many E2E, few unit) leads to slow, flaky test suites.

## Mocking vs Real Dependencies

- **Mocking** — Create fake implementations. Fast, deterministic, no infrastructure needed. Good for testing business logic in isolation. Bad for testing data access, serialization, query behavior.
- **Real dependencies (Testcontainers)** — Spin up real databases/brokers in Docker. Slower but catches bugs mocks can't: index behavior, transaction semantics, serialization edge cases.
- **When to mock** — External APIs you don't control, expensive operations (email sending, payment processing), deterministic failure testing (force timeout, force error).
- **When to use real** — Database queries, message serialization, configuration loading, health checks. Anything where the interaction with the real system IS the thing you're testing.

---

## Common Questions

**"Why Testcontainers instead of mocking the database?"**
Mocking databases can produce false confidence. Tests pass but production breaks because the mock didn't replicate actual behavior with transactions, serialization, and index usage. Testcontainers give you a real database in a container. Tests are slower (seconds vs milliseconds) but they catch real bugs.

**"How do you keep tests fast with Testcontainers?"**
Collection fixtures. Tests in the same collection share one container. Container startup takes a few seconds, amortized across many tests. Random database names ensure isolation within the shared container.

**"What's your test coverage strategy?"**
Collect code coverage on every CI run but don't enforce a percentage threshold — that leads to gaming. Instead: every new feature needs tests, every bug fix needs a regression test, component tests cover happy path + key error paths. Code review catches gaps better than coverage numbers.
