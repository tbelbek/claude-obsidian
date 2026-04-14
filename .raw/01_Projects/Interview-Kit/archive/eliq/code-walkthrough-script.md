# Gothenburg Congestion Tax Calculator — Code Presentation

## Quick Introduction (for interviewers)

This is a **.NET 10 REST API** that calculates Gothenburg congestion tax for vehicle passages. I received a broken .NET 5 starter project and restructured it into a production-quality application.

### How I approached it

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**Step 1 — Research the domain.** I went to Transportstyrelsen (the Swedish Transport Agency website) and verified the actual Gothenburg congestion tax rules: the 9 fee bands with their time ranges and amounts ([see Calculation Engine](#calculation-engine)), the 60-minute rolling window semantics (strict less-than comparison, [see Step 24](#step-24-window-boundary-precision)), the 60 SEK daily cap ([see Step 25](#step-25-daily-cap)), and which days are toll-free. I compiled the correct 2026 Swedish public holidays including day-before-holiday dates — 16 dates total ([see Step 20](#step-20-toll-free-date-check)).

**Step 2 — Restructure before implementing.** The original had business logic in the controller calling static classes directly — no interfaces, no DI usage, no testable boundaries. I couldn't implement the 60-minute window rule and test it correctly on that structure. So I restructured first: created a static pure-function engine for the calculation ([Part 2](#part-2-code-walkthrough----request-flow), testable with arrays, no infrastructure), an orchestration service for cross-cutting concerns (timezone, validation, caching, grouping — [Steps 11–21](#step-11-controller-delegates-to-service)), a repository with interfaces for data access ([Part 3](#part-3-code-walkthrough----data-layer), swappable for test stubs), and moved error handling to centralized middleware ([Part 5](#part-5-code-walkthrough----error-handling), controllers stay thin). This restructuring was the foundation — every feature built on top of it ([folder structure in Part 1](#folder-structure)).

**Step 3 — Implement incrementally.** With the structure in place, I fixed each problem and built the corresponding feature. Along the way, I upgraded from .NET 5 to .NET 10 ([Part 1](#framework-net-5-to-net-10), [Part 7](#part-7-technical-details)) because the modern language features directly enabled cleaner implementations for each fix.

Here is each problem from the original codebase, why it mattered, what I built to fix it, what modern C# features I used, and what the result looks like:

**Functional problems — the API produced wrong results:**

1. **Controller ignoring input** — the `CalculateFee` action overwrote the incoming `request` parameter with a hardcoded `List<DateTime>`, so the API returned the same result regardless of what the caller sent.

   > **Fix:** Thin controller that passes input straight to the service ([Step 10](#step-10-controller-entry-point)).
   >
   > **Why this design:** The controller's only job is HTTP concern translation — binding query parameters, returning status codes. Business logic lives in the service layer where it can be tested without HTTP infrastructure.
   >
   > **Modern C# used:** Primary constructor injects `ITollService` directly as a constructor parameter, eliminating the private field + constructor + null-check boilerplate that .NET 5 required ([Step 7](#step-7-di-registrations)). The `sealed` keyword enables JIT devirtualization — the runtime compiler replaces indirect virtual-method-table lookups with direct calls because it can prove no subclass overrides exist.
   >
   > **Result:** I separated the calculation logic into a static pure-function engine (no dependencies, trivially testable) and an orchestration service that handles timezone normalization to Gothenburg local time (CET/CEST — Central European Time / Central European Summer Time), input validation, year configuration loading from an in-memory cache backed by SQL Server, toll-free date filtering, and per-day grouping before delegating to the engine ([see request flow walkthrough](#part-2-code-walkthrough----request-flow)).

2. **60-minute window rule completely absent** — the fee calculation (`TollFeeService.GetFee`) was a 69-line if-else chain that summed every passage's fee independently. A commuter at 07:00 and 07:30 would be charged 44 SEK instead of 22 SEK — the core business rule was missing.

   > **Fix:** Static pure-function engine with sliding-window algorithm and 5 boundary-precision tests ([Steps 22–24](#step-22-getfeeforpassage)).
   >
   > **Why this design:** A static class with pure functions (input in, output out, no side effects) means the core business logic can be tested with plain arrays — no mocking, no infrastructure, no DI container. The sliding window uses strict less-than comparison (`passage.timestamp < windowEnd`, not `<=`) because the Transportstyrelsen specification says "within 60 minutes", which means the 60th minute itself starts a new window.
   >
   > **Modern C# used:** `readonly record struct FeeBand` — 12 bytes on the stack instead of heap-allocated, zero garbage-collector pressure in the hot calculation path where thousands of band comparisons happen per request ([Step 26](#step-26-feeband-struct)). Pattern matching for fee band lookup reads like English and avoids logic-inversion bugs common with negated `!=` chains ([Step 20](#step-20-toll-free-date-check)).

3. **Toll-free dates hardcoded to wrong year** — a static `DateTime[]` with 13 entries for 2021, missing several Swedish holidays (only 13 vs the correct 16 including day-before-holiday dates).

   > **Fix:** Database-driven, year-scoped toll-free dates configurable at runtime without redeployment ([Step 20](#step-20-toll-free-date-check), [Part 4](#part-4-code-walkthrough----configuration)).
   >
   > **Why this design:** Toll-free dates change every year (Easter moves, government may add holidays). Hardcoding requires a code deployment for each year change. A configuration API lets operations update rules without involving developers.
   >
   > **Modern C# used:** `DateOnly` for toll-free dates — semantically correct (no time component), prevents accidental time-of-day comparison bugs, and matches the SQL `date` column type ([Step 29](#step-29-fee-entity)). `FrozenSet` for the cached toll-free date collection — immutable after construction and optimized for repeated `.Contains()` lookups, preventing accidental modification of cached data and providing faster lookups than `HashSet` ([Step 32](#step-32-repository-caching-with-frozenset)).
   >
   > **Result:** A full REST API with year-scoped endpoints: PUT for complete year upsert (atomic replace-as-a-whole via transaction), plus granular CRUD (Create, Read, Update, Delete) for individual fee bands and toll-free dates. All mutations funnel through a single validation path and a Func-delegate pattern that eliminates duplication across 8 mutation endpoints. A JSON seed file bootstraps fresh environments idempotently on startup ([see configuration walkthrough](#part-4-code-walkthrough----configuration)).

4. **Average calculation wrong** — the original divided by `request.Distinct().Count()` which counted distinct timestamps, not distinct calendar days. Two passages at the same time counted as one divisor.

   > **Fix:** Single-pass grouping by calendar day using `.GroupBy(d => DateOnly.FromDateTime(d))` ([Step 19](#step-19-single-pass-grouping)).
   >
   > **Why this design:** `DateOnly.FromDateTime()` strips the time component, so all passages on the same calendar day land in the same group regardless of their time. The engine then calculates fee per day, and the service averages across actual calendar days — not distinct timestamps.

5. **No timezone handling** — timestamps were used as-is with no conversion. A UTC timestamp of `05:10` in summer would be treated as 05:10 instead of 07:10 Gothenburg time (CEST, UTC+2).

   > **Fix:** CET/CEST normalization as first step in the pipeline, with cross-platform timezone resolution for Windows/Linux/macOS ([Steps 13–14](#step-13-timezone-normalization)).
   >
   > **Why this design:** Gothenburg congestion tax is based on local time (when you physically pass the toll station). The same UTC instant maps to different local times depending on whether DST is active. Normalizing first means all downstream logic (fee band lookup, toll-free date check, day grouping) operates on correct local time. The timezone ID differs across platforms (`Central European Standard Time` on Windows, `Europe/Stockholm` on Linux/macOS), so the resolver tries both.

**Structural problems — the codebase couldn't be extended or tested:**

6. **Database never used** — `TollDBContext` was scaffold-generated with `Fee` and `TollFree` DbSets, proper table configuration, and even a connection string — but no code anywhere called it. The controller used static classes directly.

   > **Fix:** Fully wired EF Core with global NoTracking, covering indexes, execution strategy with transactions, and in-memory cache with 12-hour TTL and explicit invalidation ([Part 3](#part-3-code-walkthrough----data-layer), [Steps 30–35](#step-30-tolldbcontext-notracking)).
   >
   > **Why this design:** The workload is read-heavy (many fee calculations per config change), so NoTracking as the global default avoids change-tracker overhead on every query. The covering index on `(Year, FromMinute, ToMinute) INCLUDE (Price)` means EF Core's fee-band query is answered entirely from the index without touching the table — an index-only scan. The execution strategy with explicit transactions handles SQL Server transient faults (network blips, deadlocks) by automatically retrying, but writes must be wrapped in an explicit transaction inside the strategy's callback so that retries replay the entire transaction, not individual statements.
   >
   > **Modern C# used:** `sealed` classes for entities enable JIT devirtualization. `init` properties — the property can only be set during object initialization (in the constructor or object initializer), not after. This makes entities effectively immutable after EF Core materializes them, preventing accidental modification of loaded data.
   >
   > **Result:** The database context is now fully wired with Entity Framework Core, using a global NoTracking default, surrogate primary keys with covering indexes for fast fee-band lookups, and an execution strategy with explicit transactions for transient-fault-safe writes. An in-memory cache with 12-hour TTL (time-to-live) and explicit invalidation on writes eliminates database round-trips on the hot calculation path ([see data layer walkthrough](#part-3-code-walkthrough----data-layer)).

7. **Empty interface and empty service** — `ITollService` had zero methods. `TollService` had zero implementation. The DI registration (`AddTransient<ITollService, TollService>`) existed for an empty service while the controller called `TollFeeService` and `TollFreeService` (static classes) directly.

   > **Fix:** Interface-driven DI with 3 interfaces (`ITollService`, `ITollRulesRepository`, `IYearConfigurationService`), all Scoped to match DbContext lifetime ([Step 7](#step-7-di-registrations)).
   >
   > **Why this design:** Scoped (not Transient, not Singleton) because all services share the same `TollDbContext` which is Scoped by default in EF Core. A Transient service would get a different DbContext instance than the repository it calls. A Singleton service would hold a DbContext across requests, which is not thread-safe. Scoped means one instance per HTTP request — all layers share the same DbContext and the same unit of work.
   >
   > **Modern C# used:** Primary constructors on all services — `public sealed class TollService(ITollRulesRepository repository, ...)` eliminates the private field declaration, constructor body, and null-guard that .NET 5 required for each dependency.

8. **No separation of concerns** — business logic (fee calculation, toll-free filtering, response building) was all in the controller action. No layers, no testable boundaries.

   > **Fix:** Layered architecture — static pure-function engine (testable with arrays, no infrastructure) + orchestration service (timezone, validation, caching, grouping) + repository with interfaces (swappable for test stubs) + thin controllers ([Part 2](#part-2-code-walkthrough----request-flow), [Steps 11–21](#step-11-controller-delegates-to-service)).
   >
   > **Why this design:** Each layer has exactly one reason to change. The engine changes only when calculation rules change. The service changes only when orchestration logic changes (new cross-cutting concern). The repository changes only when the data access pattern changes. The controller changes only when the HTTP contract changes. This makes each layer independently testable — unit tests use the engine directly, integration tests swap the repository with `InMemoryRulesRepository`.

9. **No error handling** — no exception handling middleware, no ProblemDetails. Any runtime error returned a raw 500 with a stack trace to the client.

   > **Fix:** One global middleware mapping 3 domain exception types to ProblemDetails ([RFC 9457](#rfc-9457-problemdetails) — the HTTP standard for structured error responses) with `application/problem+json` content type. Fault injection endpoint with constant-time token comparison for testing sanitized 500s ([Part 5](#part-5-code-walkthrough----error-handling), [Steps 41–45](#step-41-exception-middleware-switch)).
   >
   > **Why this design:** Three separate exception types (not one with an error code) because: each maps to a different ProblemDetails `Title` (determined by type, not message), source-generated logging has separate EventIds per type (filterable alerts), `Assert.ThrowsAsync<T>()` in tests is compile-time safe, and adding a new error category means adding a new type + case — not modifying an enum. Exceptions (not `Result<T>`) because these are exceptional (misconfiguration, invalid input), not expected business outcomes — exceptions short-circuit the stack without requiring unwrap-per-layer.
   >
   > **Modern C# used:** Source-generated `[LoggerMessage]` for each exception type — the compiler generates logging methods at build time with zero allocation at runtime and compile-time validation of message templates, compared to `ILogger.LogWarning()` which allocates a string even when the log level is disabled ([Logging table](#logging)).
   >
   > **Result:** One global middleware maps three domain exception types to ProblemDetails responses with `application/problem+json` content type. A fault injection endpoint with constant-time token comparison and stealth 404 response allows blackbox tests to verify the sanitized 500 error contract ([see error handling walkthrough](#part-5-code-walkthrough----error-handling)).

10. **Misnamed file** — `Models/TollFeeController.cs` was actually the `CalculateFeeResponse` DTO, not a controller.

    > **Fix:** Restructured folders — contracts under `DataModels/Contracts`, entities under `DataModels/Entities`, clear separation of DTOs and domain types ([Part 1](#part-1-general-updates), [folder structure](#folder-structure)).
    >
    > **Why this design:** The folder name tells you the type's role: `Contracts` = what crosses the API boundary (request/response shapes), `Entities` = what maps to database tables, `Abstractions` = shared interfaces and base classes. A DTO in a `Models` folder next to a controller with the same name is confusing.
    >
    > **Modern C# used:** `sealed record` for DTOs — immutable data carriers with free structural equality, eliminating manual `Equals`/`GetHashCode` overrides and preventing accidental mutation after construction. File-scoped namespaces save one indentation level across every file.

**Infrastructure problems — no way to run, test, or deploy reliably:**

11. **No tests** — zero test projects, zero test coverage, no way to verify any calculation is correct.

    > **Fix:** 79 unit tests (fee band boundaries, 60-minute window edge cases, daily cap, timezone/DST transitions, validation, configuration CRUD, validator edge cases) + 48 blackbox tests (Testcontainers with real SQL Server verifying full HTTP chain including EF Core query translation and cache invalidation) ([Part 6](#part-6-testing), [Steps 46–50](#step-46-test-project-overview)).
    >
    > **Why this design:** Unit tests use `InMemoryRulesRepository` (an 80-line real implementation, not a mock) so tests verify behavior, not call patterns. One class to update when the interface changes. Blackbox tests use Testcontainers to spin up real SQL Server in Docker — no SQLite fakes, no in-memory provider that behaves differently from real SQL Server. The `[Collection]` attribute serializes 48 tests to share one Docker fixture (~10s startup), preventing parallel container conflicts.
    >
    > **Result:** 79 unit tests cover every fee band boundary, 60-minute window edge case, daily cap, timezone conversion (including DST — Daylight Saving Time transitions), input validation, configuration CRUD, and validator edge cases. 48 blackbox tests use Testcontainers to spin up real SQL Server and the API in Docker, verifying the full HTTP chain including EF Core query translation, cache invalidation after configuration mutations, and real-life commuter scenarios ([see testing walkthrough](#part-6-testing)).

12. **Outdated framework** — .NET 5 (end-of-life since May 2022), EF Core 5.0.12, Swashbuckle 5.6.3.

    > **Fix:** Upgraded to .NET 10 with modern C# patterns ([Part 1](#framework-net-5-to-net-10), [Part 7](#part-7-technical-details)).
    >
    > **Why this matters:** .NET 5 has been out of support for over 3 years — no security patches, no bug fixes. .NET 10 is the current LTS track. The upgrade also unlocked the modern language features used throughout the fixes above:
    > - **`sealed record` for DTOs** — immutable data carriers with free structural equality, eliminating manual `Equals`/`GetHashCode` overrides and preventing accidental mutation after construction
    > - **`readonly record struct` for FeeBand** — 12 bytes on the stack instead of heap-allocated, zero garbage-collector pressure in the hot calculation path where thousands of band comparisons happen per request ([Step 26](#step-26-feeband-struct))
    > - **Primary constructors** — eliminates 3 lines of boilerplate per service (private field + constructor + null check), making dependency injection concise and idiomatic ([Step 7](#step-7-di-registrations))
    > - **Source-generated `[LoggerMessage]`** — the compiler generates logging methods at build time with zero allocation at runtime and compile-time validation of message templates, compared to `ILogger.LogWarning()` which allocates a string even when the log level is disabled ([Logging table](#logging))
    > - **`FrozenSet` for cached collections** — immutable after construction and optimized for repeated lookups, preventing accidental modification of cached data and providing faster lookups than `HashSet` ([Step 32](#step-32-repository-caching-with-frozenset))
    > - **Collection expressions `[]`** — shorter and compiler-optimized compared to `Array.Empty<T>()` or `new List<T>()` ([C# Language Features table](#c-language-features))
    > - **Pattern matching** — `date.DayOfWeek is DayOfWeek.Saturday or DayOfWeek.Sunday` reads like English and avoids logic-inversion bugs common with negated `!=` chains ([Step 20](#step-20-toll-free-date-check))
    > - **`DateOnly` for toll-free dates** — semantically correct (no time component), prevents accidental time-of-day comparison bugs, matches the SQL `date` column type ([Step 29](#step-29-fee-entity))
    > - **File-scoped namespaces** — saves one indentation level across every file
    > - **Central package management** — `Directory.Build.props` and `Directory.Packages.props` eliminate duplicated framework settings and package versions across 3 projects ([Build Centralization](#build-centralization))

13. **No Docker support** — no Dockerfile, no compose, no containerized run option.

    > **Fix:** Multi-stage Dockerfile (SDK build to runtime), docker-compose with SQL Server health checks, smoke test script ([Docker and Smoke Test](#docker-and-smoke-test)).
    >
    > **Why this design:** Multi-stage build means the production image (~220 MB runtime) never contains the SDK (~900 MB), source code, or intermediate build artifacts. The compose health check uses `sqlcmd` to verify SQL Server is actually accepting queries — `depends_on` alone only waits for the container to start, not for the service inside it to be ready. The smoke test script (`set -euo pipefail`) runs 9 sequential HTTP checks that verify the full deployed stack end-to-end.

14. **Hardcoded connection string** — the connection string was embedded in `OnConfiguring` with `#nullable disable`, not in configuration.

    > **Fix:** `?? throw` fail-fast pattern in Program.cs — app never starts with a missing connection string ([Step 6](#step-6-fail-fast-connection-string)).
    >
    > **Why this design:** A hardcoded fallback connection string means the app silently connects to the wrong database if the environment variable is missing. The `?? throw new InvalidOperationException(...)` pattern fails at startup with a clear error — the mistake is caught during deployment, not when the first customer hits a 500.

15. **Entity types unnecessarily wide** — `Fee` entity used `long` for `FromMinute` and `ToMinute` (minutes-of-day max 1439, doesn't need 64 bits), `DateTime` for toll-free dates instead of `DateOnly`.

    > **Fix:** `readonly record struct FeeBand` (12 bytes, stack-allocated), `DateOnly` for toll-free dates, `int` for minute-of-day ([Steps 26–29](#step-26-feeband-struct)).
    >
    > **Why this design:** Minutes-of-day ranges from 0 to 1439 — `int` (4 bytes) is sufficient, `long` (8 bytes) wastes memory and widens the covering index for no reason. `DateOnly` communicates intent — a toll-free date has no time component, so using `DateTime` invites bugs where someone compares including time-of-day.

---

### What I would improve next

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

The implementation is production-aware but intentionally KISS — I deferred heavyweight patterns until scaling or operational needs justify them. Here are the 13 documented improvement points, grouped by priority, with the reasoning for why each was deferred and how I would implement it:

**High priority — correctness and schema evolution:**

1. **EF Core migrations** ([Step 9](#step-9-startup-safety)) — Currently using `EnsureCreatedAsync` which creates the schema once but cannot evolve it. Schema changes (new columns, wider types) are impossible without dropping and recreating the database.
   **How:** Remove `EnsureCreatedAsync` from Program.cs. Install `dotnet-ef` tools. Run `dotnet ef migrations add InitialCreate`. For existing databases, mark the migration as applied by inserting into `__EFMigrationsHistory`. Replace startup call with `MigrateAsync()`.
   **Alternative:** Use raw SQL scripts (e.g., DbUp or FluentMigrator) instead of EF Core migrations. This decouples schema management from EF Core entirely, which is useful if the team prefers SQL-first or if multiple non-.NET services share the same database. Trade-off: you lose the C#-based migration model and EF Core's automatic snapshot diffing — every schema change must be hand-written in SQL.
   **Another alternative:** Keep `EnsureCreated` but add a version-check table that the app queries at startup to detect schema drift. This is a half-measure that detects the problem but doesn't solve it — good for alerting, not for evolution.
   **Deferred because:** The schema is stable for this version — no pending column changes — and `EnsureCreated` is simpler for demo/interview environments.

2. **Fee amount validator gap** ([Step 15](#step-15-input-validation)) — The validator only checks `amount < 0`, no upper bound. A fee of 100 passes validation but the `decimal(2,0)` column rejects it with a raw 500 instead of a clean 400.
   **How:** Add `if (amount > 99)` check in `YearRuleConfigurationValidator.Validate()` after the negative-amount check. Throws `InvalidTollRequestException` with a clear message.
   **Alternative:** Use FluentValidation instead of the manual validator. FluentValidation provides a declarative rule syntax (`RuleFor(x => x.Amount).InclusiveBetween(0, 99)`) with built-in error message formatting and integration with ASP.NET model validation. Trade-off: adds a NuGet dependency for 5 validation rules — overkill for this project size, but scales better if validation complexity grows.
   **Another alternative:** Let the database reject it and catch `DbUpdateException` in the exception middleware, mapping it to a 400. Trade-off: the database becomes the validator, which couples error messages to SQL Server's exception format and makes the validation logic invisible in the codebase.
   **Deferred because:** The 2026 fee schedule maxes at 22 SEK, so no real-world input hits this gap — but it is a latent bug.

3. **`decimal(2,0)` column width** ([Step 29](#step-29-fee-entity)) — Max 99 is sufficient now but fragile.
   **How:** Create a migration: `dotnet ef migrations add WidenPriceColumn`. In the `Up()` method, alter the column to `decimal(5,0)`. Update the validator upper bound to match.
   **Alternative:** Use `decimal(18,2)` (the EF Core default) to avoid ever hitting this limit again. Trade-off: wastes storage and covering-index width for a value that realistically stays under 100 SEK — over-provisioning for a known small domain.
   **Deferred because:** Needs the migration infrastructure from improvement #1 first.

**Medium priority — scalability and operational hardening:**

4. **Distributed cache** ([Step 7](#step-7-di-registrations)) — `IMemoryCache` is single-instance only. When scaling to multiple API instances, each has its own cache and invalidation is node-local.
   **How:** Replace `IMemoryCache` injection with `IDistributedCache` (Redis). Add `AddStackExchangeRedisCache()` in Program.cs. Use Redis pub/sub for cross-instance invalidation. Optionally keep `IMemoryCache` as L1 with short TTL.
   **Alternative:** Use SQL Server as the distributed cache via `AddDistributedSqlServerCache()`. This avoids adding Redis infrastructure — the database you already have becomes the cache store. Trade-off: every cache read hits SQL Server, which defeats the purpose of caching if the goal is to reduce database load. Works better when the cache goal is cross-instance consistency rather than performance.
   **Another alternative:** Use a short TTL (e.g., 30 seconds) on `IMemoryCache` across all instances without explicit invalidation. Each instance's cache naturally refreshes within 30 seconds of a configuration change. Trade-off: 30-second stale window — acceptable if configuration changes are rare and eventual consistency is fine.
   **Deferred because:** The API runs as a single instance — adding Redis infrastructure for one node is complexity without benefit.

5. **Read-modify-write race** ([Step 39](#step-39-tryupdatetollfreedatesasync)) — Configuration mutations use last-write-wins on concurrent writes. Two admins updating the same year can silently overwrite each other.
   **How:** Add a `RowVersion` column (SQL Server `rowversion` type) to Fee/TollFree entities. Configure in EF Core with `IsRowVersion()`. EF Core auto-adds `WHERE RowVersion = @loaded` to updates. Catch `DbUpdateConcurrencyException`, return 409 Conflict.
   **Alternative:** Use pessimistic locking with `SELECT ... WITH (UPDLOCK, ROWLOCK)` via raw SQL or `FromSqlRaw`. This locks the row for the duration of the transaction, preventing concurrent reads-for-update. Trade-off: holds a database lock during the entire mutation flow (read + validate + write), which blocks other writers — fine for rare admin operations, problematic under high concurrency.
   **Another alternative:** Use an `ETag` header pattern — the GET endpoint returns the current configuration with an ETag (hash of the content), and PUT requires `If-Match` with the same ETag. Trade-off: more REST-idiomatic but requires the client to cooperate (send the ETag back), and adds header management logic.
   **Deferred because:** Configuration changes are rare and typically done by one person — the risk of concurrent writes is low in the current deployment model.

6. **`DateTime` API contract** ([Step 14](#step-14-timezone-resolution)) — The API accepts `DateTime` with `Unspecified` kind, assuming the caller means local time. This is ambiguous.
   **How:** Change controller parameter from `DateTime[]` to `DateTimeOffset[]`. Update `ToGothenburgLocalTime` to work with `DateTimeOffset`. Update all tests. JSON serialization handles `DateTimeOffset` natively.
   **Alternative:** Keep `DateTime` but add a custom model binder that rejects timestamps without explicit timezone info (no `Z` suffix, no `+02:00` offset). This forces callers to be explicit without changing the parameter type. Trade-off: custom model binder is more code to maintain, and `DateTime` still loses the offset information after parsing.
   **Another alternative:** Accept ISO 8601 strings instead of `DateTime` and parse manually with `DateTimeOffset.ParseExact`. This gives full control over the expected format. Trade-off: loses ASP.NET's automatic model binding and validation.
   **Deferred because:** Changing the parameter type is a breaking API contract change — the existing callers send `DateTime` format.

7. **Health check endpoint** ([Step 5](#step-5-top-level-statements-and-serilog)) — No `/health` endpoint exists.
   **How:** Add `builder.Services.AddHealthChecks().AddSqlServer(connectionString)` in Program.cs. Add `app.MapHealthChecks("/health")` after middleware.
   **Alternative:** Use a simple custom middleware that returns 200 if the app is running and 503 if the database is unreachable (manual `try { await db.Database.CanConnectAsync() } catch { return 503 }`). Trade-off: reinvents what `AddHealthChecks` already provides, but avoids the Microsoft health checks NuGet package.
   **Another alternative:** Rely on Docker's `HEALTHCHECK` instruction with `curl --fail http://localhost:8080/TollFee` — if the calculation endpoint responds, the app is healthy. Trade-off: couples health to a business endpoint, and a 400 (bad request) would fail the health check even though the app is healthy.
   **Deferred because:** Required for Kubernetes liveness/readiness probes, but the current deployment is Docker Compose — the compose health check on the SQL Server container serves the same purpose for now.

8. **API rate limiting** ([Step 8](#step-8-middleware-order)) — No rate limiting on public endpoints.
   **How:** Add `builder.Services.AddRateLimiter()` with a fixed-window or sliding-window policy. Apply `[EnableRateLimiting("policy")]` on the TollFee controller or globally via `app.UseRateLimiter()`.
   **Alternative:** Use an API gateway (e.g., YARP, Kong, AWS API Gateway) in front of the API and configure rate limiting there. Trade-off: adds infrastructure complexity but centralizes rate limiting for all services, not just this one — better for a microservices architecture.
   **Another alternative:** Use a reverse proxy like nginx with `limit_req_zone`. Trade-off: rate limiting logic lives outside the application — harder to test and version alongside the code.
   **Deferred because:** The API is not publicly exposed yet — rate limiting matters when external consumers can hit the endpoint.

**Low priority — refinements:**

9. **Authentication** ([Step 10](#step-10-controller-entry-point)) — No auth, anonymous API.
   **How:** Add `builder.Services.AddAuthentication().AddJwtBearer()` or a custom API key middleware. Add `[Authorize]` on controllers that need protection.
   **Alternative:** Use API key authentication via a custom middleware that checks a header (`X-Api-Key`) against a configured list. Simpler than JWT for machine-to-machine calls. Trade-off: no token expiration, no claims, no identity — just access control.
   **Another alternative:** Rely on network-level security (VPC, internal load balancer, service mesh mTLS) instead of application-level auth. Trade-off: no per-caller identity or audit trail, but avoids authentication complexity in the application code.
   **Deferred because:** Auth strategy depends on the deployment context (internal vs public, API gateway in front, etc.) — adding JWT now might be the wrong choice.

10. **`IFeeBandShape` dead weight** ([Step 27](#step-27-ifeebandshape-interface)) — Only `FeeBand` implements it after the HHmm change.
    **How:** Check if any code still calls `ToFeeBand(this IFeeBandShape)` on types other than `FeeBand` itself. If only `FeeBand` implements it, remove the interface and change extension methods to take `FeeBand` directly.
    **Alternative:** Keep the interface but mark it with `[Obsolete("Consider removing — only FeeBand implements this")]` to signal the debt without breaking anything. Trade-off: the warning is visible in IDE but doesn't force action.
    **Deferred because:** It is harmless — one unused abstraction that might become useful if a second band representation appears.

11. **Response caching** ([Step 21](#step-21-daily-fee-delegation)) — No HTTP response caching. Same input always produces the same output.
    **How:** Add `builder.Services.AddOutputCache()` and `app.UseOutputCache()`. Apply `[OutputCache(Duration = 60)]` on the `CalculateFee` action. Invalidate on config changes.
    **Alternative:** Use `ResponseCaching` middleware with `[ResponseCache]` attribute instead of output caching. This sets HTTP cache headers (`Cache-Control`, `ETag`) and lets the client or a CDN cache the response. Trade-off: relies on client compliance with cache headers — a misbehaving client can ignore them.
    **Another alternative:** Cache at the reverse proxy / CDN level (e.g., Cloudflare, Varnish) based on the full query string. Trade-off: cache invalidation on config changes requires purging the CDN cache, which adds operational complexity.
    **Deferred because:** The in-memory cache on the data layer already eliminates DB round-trips — output caching would add a second cache layer with its own invalidation concerns.

12. **UTC blackbox test** ([Step 46](#step-46-test-project-overview)) — Blackbox tests strip the UTC `Z` suffix from timestamps before sending. There is no test that verifies the timezone conversion works through the full HTTP chain with explicitly UTC input.
    **How:** In `GatewayRealLifeBlackBoxTests`, add one test case that sends timestamps WITH the `Z` suffix (don't strip `DateTimeKind.Utc` in `BuildEndpoint`). Assert the timezone conversion produces the correct fee.
    **Alternative:** Add a dedicated timezone integration test class with winter (CET, UTC+1) and summer (CEST, UTC+2) test cases that send UTC timestamps and assert the local-time fee band applies. Trade-off: more thorough but adds another test file and more Docker startup time.
    **Deferred because:** Unit tests cover the timezone logic thoroughly, but an end-to-end test would increase confidence.

13. **Docker hardening** ([Docker and Smoke Test](#docker-and-smoke-test)) — No `.dockerignore` (the entire repo including `.git/`, test projects, docs is sent to the Docker daemon), the container runs as root, and base image tags are floating (not pinned to a digest).
    **How:** Create `.dockerignore` (exclude `bin/`, `obj/`, `.git/`, `docs/`, test projects). Add `USER app` after `EXPOSE 8080` (the `aspnet` base image already creates an `app` user). Pin base images to digest for reproducible builds. Add `deploy.resources.limits` in compose for CPU and memory.
    **Alternative:** Use distroless base images (e.g., `mcr.microsoft.com/dotnet/runtime-deps` with a self-contained publish) instead of the `aspnet` image. The distroless image has no shell, no package manager, no user utilities — minimal attack surface. Trade-off: debugging is harder (no `bash` in the container to exec into), and self-contained publish increases the image size because the .NET runtime is bundled.
    **Another alternative:** Use `PublishAot` for ahead-of-time compilation, producing a native binary that doesn't need the .NET runtime at all — the final image can be as small as 30 MB on Alpine. Trade-off: AOT requires all code paths to be statically analyzable (no `dynamic`, limited reflection), which needs careful testing with EF Core since EF Core uses reflection for entity materialization.
    **Deferred because:** These are production hardening concerns — the current Dockerfile is intentionally simple for demo environments.

**Known risks and mitigations:**

| # | Risk | Mitigation |
|---|---|---|
| 1 | Multi-instance cache consistency: in-memory cache invalidation is node-local | Migrate to distributed cache/event invalidation when scaling out (improvement #4) |
| 2 | `EnsureCreated` limitations for schema evolution: not a migration workflow | Switch to migrations-first deployment in production environments (improvement #1) |
| 3 | `DateTime` kind ambiguity (`Unspecified`): caller intent may differ from "already local" assumption | Document API expectation; optionally enforce/normalize stricter input contracts later (improvement #6) |
| 4 | Replace-as-a-whole write amplification: many updates on huge year configs can create extra churn | Acceptable now (KISS); differential update strategy can be introduced if needed |

**Why this is "KISS but production-aware":** I kept core flows straightforward (year upsert, deterministic rule engine, thin controllers). I added only high-value complexity: centralized errors, cache invalidation, transactional writes, tests, and containerized reproducibility. I deferred heavyweight patterns (distributed cache, event bus, advanced migration orchestration) until scaling justifies them.

### Tech stack

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

.NET 10, C#, Entity Framework Core, SQL Server, IMemoryCache, Serilog (structured logging), Docker + Docker Compose, xUnit, Testcontainers, Swashbuckle (OpenAPI/Swagger)

### At a glance

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

| Metric | Value |
|---|---|
| Source files | ~30 |
| Production code | ~1,500 lines |
| Unit tests | 79 |
| Blackbox integration tests | 48 |
| Architecture decisions documented | 29 |
| API endpoints | 11 (1 calculation + 10 configuration) |
| Inline code comments (interview-ready) | 176 (WHY / ALTERNATIVE / NOTE / ADR) |
| Prepared Q&A in this document | 165 questions with answers |
| Documented improvement points | [13 with implementation plans](#improvement-points) |

---

## How to read this document

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

| Marker | Meaning |
|---|---|
| 🗣️ **SAY** | What to say out loud — the main presentation narrative |
| 📂 **OPEN** | File to open in the IDE — click to navigate |
| 📍 **LINE** | Line number to point at in the open file |
| 🖥️ **TERMINAL** | Command to run live in the terminal |
| 💬 **Q** / ✅ **A** | Likely interview question with a prepared answer |
| 📝 **CODE NOTE** | Technical detail extracted from the inline code comments |
| ⚠️ **IMPROVE** | Known improvement point — links to the [Improvement Points](#improvement-points) table |
| 🔗 **SEE ALSO** | Cross-reference to a detailed table in [Part 7](#part-7-technical-details) |

---

## Opening

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

"The starter code was a .NET 5 project with 17 files. The controller overwrote the incoming request with hardcoded test data, the fee calculation was an if-else chain with no 60-minute window logic, toll-free dates were a hardcoded 2021 array, the DB context existed but was never wired up, and there were no tests. I'll walk through what I changed -- starting with the infrastructure, then the business logic, and finally the specific technical patterns."

### Phase 1: Quick Demo (2 min)

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

### Step 1: Start the application

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**🖥️ TERMINAL:**

    cd TollFee.Api
    dotnet run

**🗣️ SAY:** "The API starts, seeds the 2026 configuration from JSON, and is ready on localhost:5062."
> 💬 **Q:** "What happens if the database is unreachable at startup?"
>
> ✅ **A:** Startup catches the exception and logs a warning -- the app starts degraded rather than crashing, so it can still serve cached data or return clear errors.

> 💬 **Q:** "Why seed from JSON instead of a migration with INSERT statements?"
>
> ✅ **A:** JSON is human-readable and editable by non-developers; migrations are for schema, not volatile business config that changes per year.

> 💬 **Q:** "What if someone deploys with a wrong connection string?"
>
> ✅ **A:** The `?? throw` on line 57 of Program.cs fails fast at startup with InvalidOperationException -- the app never starts, and the error is immediately visible in logs.

> 💬 **Q:** "What if the database is down but the app is already running with a warm cache?"
>
> ✅ **A:** Cached data continues serving requests normally; only cache misses fail, and those bubble up as 500s through the exception middleware.

### Step 2: Empty request returns zero

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**🖥️ TERMINAL:**

    curl -s "http://localhost:5062/TollFee" | jq

**🗣️ SAY:** "An empty request returns totalFee 0 and averageFeePerDay 0 -- the empty-input guard at line 35 of TollService handles this."
> 💬 **Q:** "Why return a 200 with zeros instead of a 400 for empty input?"
>
> ✅ **A:** Zero passages is a valid calculation (the answer is zero), not a malformed request -- returning 400 would force every client to special-case empty arrays before calling.

> 💬 **Q:** "What happens if someone sends non-date strings in the query?"
>
> ✅ **A:** ASP.NET model binding fails to parse them into DateTime[] and the [ApiController] attribute auto-returns a 400 ProblemDetails with validation errors before our code runs.

> 💬 **Q:** "What's the result if the input is null instead of empty?"
>
> ✅ **A:** ASP.NET model binding deserializes a missing query parameter as an empty array, so `passages.Length == 0` catches it and returns zero -- null never reaches TollService.

### Step 3: Calculate a fee

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**🖥️ TERMINAL:**

    curl -s "http://localhost:5062/TollFee?request=2026-02-02T07:10:00&request=2026-02-02T17:10:00" | jq

**🗣️ SAY:** "Two passages on a weekday -- 07:10 hits the 22 SEK (Swedish Krona) band and 17:10 hits the 13 SEK band, totaling 35 SEK."
> 💬 **Q:** "Why use GET with query parameters instead of POST with a body?"
>
> ✅ **A:** The calculation is idempotent with no side effects, which matches GET semantics; GET responses are also cacheable by proxies, and some proxies/CDNs strip the body from GET requests.

> 💬 **Q:** "What happens if both passages are within 60 minutes of each other?"
>
> ✅ **A:** The 60-minute window rule kicks in and only the highest fee is charged; e.g., 07:10 (22 SEK) and 07:50 (22 SEK) would yield 22 SEK, not 44.

> 💬 **Q:** "What if all passages in a day fall in one 60-minute window?"
>
> ✅ **A:** Only the single highest fee from that window is charged -- the loop commits just one window's highest fee, then Math.Min caps it at 60 SEK.

> 💬 **Q:** "What path does the code take when a passage falls outside all fee bands (e.g., 03:00 AM)?"
>
> ✅ **A:** GetFeeForPassage's FirstOrDefault finds no matching band, returns default(FeeBand) with Amount=0, so the passage contributes zero to the total.

### Step 4: Change config and recalculate

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**🖥️ TERMINAL:**

    curl -s -X PUT "http://localhost:5062/configuration/years/2026/fee-bands/0700/0759" \
      -H "Content-Type: application/json" \
      -d '{"amount": 50}'
    curl -s "http://localhost:5062/TollFee?request=2026-02-02T07:10:00&request=2026-02-02T17:10:00" | jq

**🗣️ SAY:** "I changed the 07:00-07:59 band to 50 SEK -- the cache was invalidated on write, so the recalculation picks up the new amount immediately."
> 💬 **Q:** "What if the app crashes between the DB commit and the cache invalidation?"
>
> ✅ **A:** IMemoryCache lives in-process, so a crash loses the cache entirely; on restart the cache is empty and reloads fresh data from the DB -- no stale entries.

> 💬 **Q:** "How would you handle this in a multi-instance deployment?"
>
> ✅ **A:** Replace IMemoryCache with IDistributedCache (e.g., Redis) and use pub/sub or cache-aside with short TTL (time-to-live — how long cached data stays valid before expiring)s so all nodes see the update.

> 💬 **Q:** "What if cache expires mid-request between loading bands and loading dates?"
>
> ✅ **A:** Each GetOrCreateAsync call is atomic per key -- bands may come from cache while dates hit DB, but each per-year result is internally consistent because the factory is idempotent.

> 💬 **Q:** "What if two admins update the same year simultaneously?"
>
> ✅ **A:** Last-write-wins with silent data loss since UpsertYearConfiguration does a full replace; a fix would be optimistic concurrency with a row version check.

---

## Part 1: General Updates

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

### Framework: .NET 5 to .NET 10

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**Original (`1701a70`):** .NET 5, `Startup.cs` with `ConfigureServices` + `Configure` pattern. `Program.cs` was 6 lines (`CreateHostBuilder` boilerplate). EF Core 5.0.12, Swashbuckle 5.6.3.

**Now:** .NET 10, minimal hosting (top-level `Program.cs`, 136 lines). EF Core 10.0.5, Swashbuckle 10.1.5, Serilog, JetBrains.Annotations. Modern C# features throughout.

**Why:** .NET 5 is end-of-life. .NET 10 gives primary constructors, records, collection expressions, pattern matching, source-generated logging, `FrozenSet`, and current provider versions.

### Build Centralization

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**Original:** Single `TollFee.Api.csproj` with inline `net5.0` target and inline package versions. No test projects. Legacy `TollFee.sln` (65 lines of GUIDs).

**Now:**
- `Directory.Build.props` -- centralizes `TargetFramework`, `Nullable`, `ImplicitUsings` across 3 projects
- `Directory.Packages.props` -- `ManagePackageVersionsCentrally` with version variables (`EfCoreVersion`, `TestcontainersVersion`)
- `TollFee.slnx` -- 10 lines of clean XML via `dotnet sln migrate`

**Why:** Single source of truth. No version drift. No GUID merge conflicts.

| Decision | Why | Alternative | Trade-off |
|---|---|---|---|
| Centralize build with `Directory.Build.props` + `Directory.Packages.props` | Shared settings duplicated across 3 csproj; inline versions could drift | Keep inline versions per csproj | One-time path churn in diffs; blackbox fixture needed updating for `.slnx` |

### Folder Structure

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**Original:** Flat layout:
- `Models/` -- `Fee.cs`, `TollFree.cs`, `TollDBContext.cs`, plus a misnamed `TollFeeController.cs` that actually contained only `CalculateFeeResponse`
- `Services/` -- `ITollService.cs` (empty interface), `TollService.cs` (empty class), `TollFeeService.cs` (static fee calc), `TollFreeService.cs` (static toll-free filter)
- `Controllers/` -- `TollFeeController.cs`

**Now:**
- `Application/Calculation/` -- engine + service
- `Application/Configuration/` -- year config service, validator, seed service, interfaces, mappers
- `Application/Persistence/` -- DbContext + repository
- `Application/Swagger/` -- filters
- `DataModels/` -- entities, DTOs, contracts, abstractions
- `Controllers/` -- thin controllers
- `ExceptionHandling/` -- middleware (ASP.NET pipeline concern, separate from business logic)

**Why:** Predictable locations, clear ownership boundaries, responsibility-based grouping.

| Decision | Why | Alternative | Trade-off |
|---|---|---|---|
| Restructure folders by responsibility boundaries | Improves discoverability; reduces "where should this file go?" ambiguity; separates transport/business/data concerns | Keep original structure; strict deep clean architecture; one-class-per-folder | Short-term diff size and path churn; team needs adaptation period for new locations |
| Place exception middleware at API boundary, not under `Application/` | Depends on ASP.NET pipeline primitives, not domain logic | Keep under `Application/` | Slightly more folder complexity; much cleaner separation of concerns |

### Docker and Smoke Test

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**Original:** None.

**Now:**
- `Dockerfile` -- multi-stage (SDK build -> runtime), `UseAppHost=false`, port 8080
- `docker-compose.yml` -- SQL Server Express with `sqlcmd` health check (20 retries, 20s start). API depends on `service_healthy`. Volume persistence. Password via env var.
- `smoke-test.sh` -- `set -euo pipefail`. 9 sequential HTTP checks covering empty request, unconfigured year, malformed date, fault endpoint stealth, config CRUD (Create, Read, Update, Delete — the four basic data operations) with recalculation verification.

| Decision | Why | Alternative | Trade-off |
|---|---|---|---|
| Provide Dockerfile + docker-compose + smoke test | Standardized runtime for local testing and interview/demo environments | No containerization | Compose credentials and ports are dev defaults; production needs hardened secrets/network policy |

> 💬 **Q:** "What Docker optimizations could you make to this Dockerfile?"
>
> ✅ **A:** Several things:
> - **`.dockerignore` file** — currently missing. Without it, `COPY . .` sends the entire repo to the Docker daemon including `bin/`, `obj/`, `.git/`, test projects, and docs. A `.dockerignore` excluding those would shrink the build context significantly and speed up builds.
> - **Non-root user** — the container runs as root by default. Adding `USER app` (the `aspnet` base image already creates an `app` user) reduces the blast radius if the process is compromised.
> - **Pinned image digests** — `sdk:10.0` and `aspnet:10.0` are floating tags. Pinning to a specific digest (e.g., `aspnet:10.0@sha256:...`) guarantees reproducible builds and avoids surprise breakage from upstream image updates.
> - **Multi-platform builds** — adding `--platform linux/amd64,linux/arm64` to `docker buildx build` produces images that run natively on both Intel and Apple Silicon without emulation overhead.
> - **Layer caching for NuGet** — the current Dockerfile already separates `COPY *.csproj` + `dotnet restore` from `COPY . .` + `dotnet publish`, which is the main layer caching optimization. NuGet packages only re-download when the `.csproj` or `.props` files change.
> - **`PublishTrimmed` and `PublishAot`** — for a small API like this, ahead-of-time compilation or IL trimming could reduce the final image from ~220 MB to ~30 MB and improve cold-start time. Trade-off: AOT requires all code paths to be statically analyzable (no `dynamic`, limited reflection), which needs careful testing with EF Core.
> - **Alpine base image** — switching from `aspnet:10.0` (Debian) to `aspnet:10.0-alpine` cuts the base layer from ~220 MB to ~100 MB. Trade-off: Alpine uses musl libc instead of glibc, which can cause subtle runtime differences — needs integration testing.
> - **Health check in Dockerfile** — adding a `HEALTHCHECK` instruction (e.g., `HEALTHCHECK CMD curl --fail http://localhost:8080/health || exit 1`) lets Docker itself monitor the API container, not just the SQL Server container.

> 💬 **Q:** "What would you optimize in the docker-compose for production?"
>
> ✅ **A:** The current compose is intentionally dev-focused. For production:
> - **Secrets management** — move `MSSQL_SA_PASSWORD` from environment variable to Docker secrets (`docker secret create`) or an external vault (HashiCorp Vault, Azure Key Vault). The current `${MSSQL_SA_PASSWORD:-PocOnly!Passw0rd1}` default is fine for local dev but would be a security risk in production.
> - **Resource limits** — add `deploy.resources.limits` for CPU and memory to prevent a single container from starving the host. SQL Server in particular can consume all available memory by default.
> - **Network isolation** — create an internal Docker network so only the API container can reach SQL Server. Currently both containers bind to host ports, exposing the database directly.
> - **Read-only filesystem** — add `read_only: true` to the API container and mount only the specific paths that need writes (e.g., temp directories). Prevents an attacker from modifying the application binaries at runtime.
> - **Logging driver** — configure a centralized logging driver (e.g., `fluentd`, `json-file` with rotation) instead of the default unbounded stdout logging.
> - **Named volumes with backup** — the `tollfee-sql-data` volume is correct for persistence, but production needs a backup strategy (SQL Server backup to a mounted volume or object storage).

> 💬 **Q:** "Why `UseAppHost=false` in the publish command?"
>
> ✅ **A:** `UseAppHost=false` skips generating the native executable wrapper. In a container, we always run with `dotnet TollFee.Api.dll` via the `ENTRYPOINT`, so the native host binary would just be wasted space in the image. It also avoids platform mismatch issues — the native host is compiled for the build machine's OS, which may differ from the container's.

> 💬 **Q:** "Why multi-stage build instead of a single stage?"
>
> ✅ **A:** The SDK image is ~900 MB (includes compiler, NuGet, MSBuild). The runtime image is ~220 MB. Multi-stage copies only the published output to the final image, so the production image never contains the SDK, source code, or intermediate build artifacts. Smaller image = faster pulls, smaller attack surface, less storage cost.

### DI and Interfaces

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**Original:** `ITollService` was empty (`{}`). `TollService` was empty. `Startup.cs` registered `AddTransient<ITollService, TollService>` -- a transient registration for a service with no methods. The controller injected `ITollService` but never used it -- it called `TollFeeService` and `TollFreeService` (static classes) directly.

**Now:**
- `ITollService` (`Application/Calculation/ITollService.cs:5`) -- `CalculateFeeAsync` with XML docs
- `ITollRulesRepository` (`Application/Configuration/Interfaces/ITollRulesRepository.cs:6`) -- 7 methods
- `IYearConfigurationService` (`Application/Configuration/Interfaces/IYearConfigurationService.cs:6`) -- 10 methods
- `IFeeBandShape` (`DataModels/Abstractions/IFeeBandShape.cs:7`) -- shared shape contract
- All services Scoped (`Program.cs:42-48`), matching DbContext lifetime

**Why:** Interface-driven DI enables testability. Scoped matches EF Core's per-request pattern. The original's Transient registration with empty interface served no purpose.

| Decision | Why | Alternative | Trade-off |
|---|---|---|---|
| Contract-first evolution: preserve `TollFee` endpoint surface | Client compatibility and backward safety higher priority than internal purity | Change controller contract to return `ActionResult<T>` with in-controller error mapping | Requires consistent exception discipline in services |
| Consolidate data types under `DataModels` with `IFeeBandShape` + `YearScopedEntity` | Reduces duplication; clarifies DTO (Data Transfer Object — carries data between layers without business logic)/contract/entity roles; reusable mapping/validation | Scatter types across folders | `IFeeBandShape` is interface (not abstract class) to allow multiple type families without inheritance coupling |

---

## Part 2: Code Walkthrough -- Request Flow

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

### Calculation Engine

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**Original (`TollFeeService.cs`):** A 69-line static class with a `GetFee` method -- an if-else chain using `TimeSpan.FromMinutes()` comparisons. It iterated every passage and summed fees directly. **No 60-minute window logic.** A commuter at 07:00 and 07:30 was charged 22+22=44 instead of just 22. The daily cap existed (`GetActualFee`: `if totalFee > 60 return 60`) but the window rule -- the most important business rule -- was completely absent. No per-day grouping. No year awareness.

**Now -- two-class split:**

`CongestionRuleEngine` (`Application/Calculation/CongestionRuleEngine.cs:5`) -- static, pure functions:

- `GetFeeForPassage` (`:15`) -- converts to minute-of-day (`hour * 60 + minute`), linear scan via `FirstOrDefault`. `FeeBand` is a struct so `FirstOrDefault` returns `default` with `Amount=0` on no match -- no fee outside configured hours, no null check.
- `CalculateDailyFee` (`:29`) -- the 60-minute window. Sorts passages internally, then iterates. `passage < currentWindowEnd` (strict `<`) = same window, upgrade max only. `>= windowEnd` = commit max, start new window. After loop, commit last window. `Math.Min(totalFee, 60)` cap.

`TollService` (`Application/Calculation/TollService.cs:7`) -- orchestration:

1. Timezone normalization (`:20`) -- first operation, before any logic
2. Input validation (`:100`) -- max 1000 passages, max 370-day range
3. Year extraction + validation (`:69`, `:74`) -- all years must be configured
4. Load fee bands + toll-free dates from cache (`:29-30`)
5. Global sort (`:33`) -- `Array.Sort` in-place once
6. Single-pass grouping (`:36-52`) -- `HashSet` for distinct days + `Dictionary` for chargeable by day
7. Sum daily fees (`:54`) -- delegates to engine per day with that year's bands
8. Average (`:58`) -- `totalFee / distinctDays.Count` including toll-free days

| | Original | Now |
|---|---|---|
| **Split** | All logic in controller + static classes | Engine (pure math) + Service (orchestration) |
| **Window rule** | None -- charged every passage | Strict `<` 60 min. 07:00+08:00 = 2 charges. 07:00+07:59 = 1. |
| **Average** | `request.Distinct().Count()` (distinct timestamps) | Distinct calendar days including toll-free |
| **Trade-off** | N/A | Static = no DI. Promote to injectable if caps vary by vehicle type. |

| Decision | Why | Alternative | Trade-off |
|---|---|---|---|
| Split orchestration (`TollService`) from pure computation (`CongestionRuleEngine`) | Improves maintainability and targeted testability | Keep all logic in one class | Adds an extra abstraction, but keeps each class cognitively smaller |
| `FeeBand` as `readonly record struct` (12 bytes, 3 ints) | Stack-allocated, no GC pressure; free structural equality for dedup | `record class` (heap-allocated); plain `struct` (no built-in equality) | `FirstOrDefault` returns `default(FeeBand)` with `Amount=0` on no match -- intentional but requires awareness |
| Hard-limit request size and date span | Protects service from expensive/abusive inputs; keeps runtime predictable | No limits | Some edge requests rejected intentionally (`400`) for operational safety |

**Flow: Toll Fee Calculation**

Source: `TollFeeController.cs:27`, `TollService.cs:13`, `CongestionRuleEngine.cs:29`

```
GET /TollFee?request=...
|
+-- request null or empty?
|   |
|   +-- [YES] --> Return { totalFee=0, averageFeePerDay=0 }
|   |
|   +-- [NO]
|       |
|       +-- Convert all timestamps to Gothenburg local time
|       |   (see [Timezone Normalization](#timezone-normalization) below)
|       |
|       +-- passages.Length > 1000?
|           |   |
|           |   +-- [YES] --> InvalidTollRequestException --> 400
|           |
|           +-- [NO]
|               |
|               +-- date range > 370 days?
|               |   |
|               |   +-- [YES] --> InvalidTollRequestException --> 400
|               |
|               +-- [NO]
|                   |
|                   +-- Get distinct years from passages
|                   |
|                   +-- All years configured in DB?
|                   |   |
|                   |   +-- [NO] --> YearNotConfiguredException --> 400
|                   |
|                   +-- [YES]
|                       |
|                       +-- Load fee bands per year (cached)
|                       +-- Load toll-free dates per year (cached)
|                       |
|                       +-- Sort all passages once (Array.Sort, in-place)
|                       |
|                       +-- Single pass: collect distinct days + group chargeable passages
|                       |   (toll-free check per passage)
|                       |
|                       +-- For each day:
|                       |   +-- CongestionRuleEngine.CalculateDailyFee(...)
|                       |       (see [60-Minute Window](#flow-60-minute-window--daily-cap) below)
|                       |
|                       +-- totalFee = sum of all daily totals
|                       |
|                       +-- distinctDayCount = all input days (incl. toll-free)
|                       |
|                       +-- averageFeePerDay = totalFee / distinctDayCount
|                       |
|                       +-- Return { totalFee, averageFeePerDay }
```

Key decision points:
- Empty input returns a zeroed response directly.
- Validation happens after timezone normalization.
- Year validation happens before loading fee bands/toll-free dates.
- Toll-free filtering happens before per-day fee calculation.
- Average uses distinct days from the original normalized input, including toll-free days.

**Flow: 60-Minute Window + Daily Cap**

Source: `CongestionRuleEngine.cs:29` (`CalculateDailyFee`), `:15` (`GetFeeForPassage`)

```
CalculateDailyFee(passages, feeBands)
|
+-- Sorts passages internally before processing.
|
+-- Any passages?
|   |
|   +-- [NO] --> Return 0
|
+-- [YES]
    |
    +-- windowMax   = GetFeeForPassage(first passage)
    +-- totalFee    = 0
    |
    +-- For each subsequent passage:
    |   |
    |   +-- passageFee = GetFeeForPassage(passage)
    |   |
    |   +-- passage < windowStart + 60 minutes?
    |   |   |
    |   |   +-- [YES] (same window)
    |   |   |   |
    |   |   |   +-- passageFee > windowMax?
    |   |   |       +-- [YES] --> windowMax = passageFee
    |   |   |       +-- [NO]  --> (no change)
    |   |   |
    |   |   +-- [NO] (new window, >= 60 min apart)
    |   |       |
    |   |       +-- totalFee += windowMax
    |   |       +-- windowStart = passage
    |   |       +-- windowMax = passageFee
    |   |
    |   +-- (continue loop)
    |
    +-- totalFee += windowMax   (close final window)
    |
    +-- totalFee > 60?
        |
        +-- [YES] --> Return 60  (daily cap)
        +-- [NO]  --> Return totalFee

GetFeeForPassage(passage, feeBands):
    minuteOfDay = (passage.Hour * 60) + passage.Minute
    match = first band where minuteOfDay >= fromMinute AND minuteOfDay <= toMinute
    return match.Amount or 0 if no match
```

Window semantics:
- Same window condition is strictly `< 60` minutes from current window start.
- Exactly 60 minutes starts a new charge window.
- Daily cap is applied after summing all window maxima.

**Flow: Toll-Free Determination**

Source: `TollService.cs:84` (`IsTollFreeDate`)

```
IsTollFreeDate(date, tollFreeDatesByYear)
|
+-- Saturday or Sunday?
|   +-- [YES] --> toll-free (return true)
|
+-- Month == July?
|   +-- [YES] --> toll-free (return true)
|
+-- Date in configured toll-free set for that year?
|   +-- [YES] --> toll-free (return true)
|
+-- [NONE MATCHED] --> chargeable (return false)
```

Evaluation order matters:
1. Weekend check (cheapest)
2. July check
3. Configured toll-free set lookup
4. Otherwise chargeable

### Timezone Normalization

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**Original:** No timezone handling whatsoever. Timestamps used as-is. A UTC `05:10` in summer treated as 05:10 instead of 07:10 CEST (Central European Summer Time, UTC+2).

**Now:** `ToGothenburgLocalTime` (`TollService.cs:118`) switches on `DateTimeKind`:
- `Unspecified` -> as-is (matches ASP.NET query param default)
- `Utc` -> `ConvertTimeFromUtc` to Europe/Stockholm
- `Local` -> `ConvertTime` from caller's zone

Resolution at startup (`TollService.cs:11`, `:128`): `TryFindSystemTimeZoneById` -- IANA (Internet Assigned Numbers Authority — maintains timezone database used on Linux/macOS) first, Windows fallback. Throws if neither found.

| | |
|---|---|
| **Why first** | Tax rules are legally local-time. UTC `2025-12-31T23:30Z` = local `2026-01-01`. Must normalize before year validation. |
| **Trade-off** | `Unspecified = assumed local` is implicit. `DateTimeOffset` would be explicit -- change I'd make if starting over. |

| Decision | Why | Alternative | Trade-off |
|---|---|---|---|
| Normalize all timestamps to Gothenburg local time before any business logic | Congestion-tax rules are legally local-time based | Keep everything in UTC; convert only near fee lookup | Timezone logic must be explicit and tested around DST (Daylight Saving Time — clocks shift forward in spring, back in autumn) and year-boundary cases |

**Flow: Timezone Normalization**

Source: `TollService.cs:118` (`ToGothenburgLocalTime`), `:128` (`ResolveGothenburgTimeZone`), `:11` (static field)

```
ToGothenburgLocalTime(dateTime)
|
+-- dateTime.Kind?
    |
    +-- [Unspecified] --> return as-is (assumed already local)
    |
    +-- [Utc] --> ConvertTimeFromUtc to Europe/Stockholm
    |
    +-- [Local] --> ConvertTime to Europe/Stockholm
```

Timezone resolution (static, resolved once at startup):
```
ResolveGothenburgTimeZone()
|
+-- TryFindSystemTimeZoneById("Europe/Stockholm")?
|   +-- [FOUND] --> use it (Linux/macOS IANA ID)
|
+-- TryFindSystemTimeZoneById("W. Europe Standard Time")?
|   +-- [FOUND] --> use it (Windows zone ID)
|
+-- [NEITHER FOUND] --> throw InvalidOperationException (app cannot start)
```

CET/CEST handling:
- Winter (CET (Central European Time, UTC+1)): UTC+1. Example: `06:10 UTC => 07:10 local`.
- Summer (CEST): UTC+2. Example: `05:10 UTC => 07:10 local`.
- DST transition handled automatically by `TimeZoneInfo`.

### Code Walkthrough Steps: Entry Point and Request Flow

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

### Step 5: Top-level statements and Serilog

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Program.cs

**📍 LINE:** 20

**🗣️ SAY:** "Top-level statements with try/finally so Serilog flushes on crash -- dual sinks: console for all levels, rolling file for warnings with 14-day retention."
> 💬 **Q:** "Why Serilog instead of the built-in ILogger?"
>
> ✅ **A:** Serilog provides structured logging, multiple sinks (console + file), and per-namespace log-level overrides in a single fluent config -- built-in ILogger would need additional packages for file sinks.

> 💬 **Q:** "What does the try/finally do here without a catch?"
>
> ✅ **A:** It ensures Log.CloseAndFlush() runs even on unhandled exceptions so buffered log entries are written to disk before the process exits; the exception still propagates and crashes the app.

> 💬 **Q:** "Why Serilog over NLog or log4net?"
>
> ✅ **A:** Three main reasons:
> - **Structured logging is native, not bolted on.** Serilog was designed from the ground up around structured events — when you write `Log.Information("Processing {Year}", year)`, the `Year` property is stored as a typed key-value pair, not interpolated into a string. NLog added structured logging later (NLog 4.5+) as `${event-properties}`, but the core API was designed around string templates — structured properties feel like an afterthought. log4net has no real structured logging support at all.
> - **Sink ecosystem is wider and more actively maintained.** Serilog has 200+ community sinks including first-party integrations for Seq, Elasticsearch, Application Insights, Grafana Loki, and OpenTelemetry. NLog has comparable core sinks but fewer third-party options. log4net's appender ecosystem has largely stagnated since the project moved to maintenance mode.
> - **Fluent configuration with `IConfiguration` binding.** Serilog's `ReadFrom.Configuration()` lets you change sinks, levels, and enrichers entirely from `appsettings.json` without recompiling. NLog uses its own XML-based `nlog.config` file with a different schema from `appsettings.json` — two configuration systems to maintain. log4net uses XML configuration that predates the .NET Core configuration model entirely.
> - **Trade-off acknowledged:** NLog is slightly faster in high-throughput benchmarks (NLog's async target wrapper has less overhead than Serilog's async sink). For this API's logging volume (hundreds of events per minute, not millions), the difference is irrelevant. If we were building a logging pipeline processing millions of events per second, NLog's raw throughput advantage would matter more.

> 💬 **Q:** "What if you need to ship logs to a centralized system like Elasticsearch?"
>
> ✅ **A:** Add a Serilog Elasticsearch sink in the fluent config -- no code changes needed, just a new `.WriteTo.Elasticsearch()` call alongside the existing console and file sinks.

>
> 📝 **CODE NOTE:** [Program.cs:15] — ALTERNATIVE: block-scoped namespace -- not used because file-scoped namespace saves one indent level and is the modern C# convention since C# 10.
>
> 📝 **CODE NOTE:** [Program.cs:27] — ADR-23: Serilog with dual sinks -- trade-off: file sink is local to container/host; production should add a centralized sink.

> ⚠️ **IMPROVE:** Add a /health endpoint via app.MapHealthChecks with a SQL Server check -- required for Kubernetes liveness/readiness probes.

### Step 6: Fail-fast connection string

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Program.cs

**📍 LINE:** 56-57

**🗣️ SAY:** "Fail-fast on missing connection string -- throws at startup instead of silently connecting to a wrong database."
> 💬 **Q:** "Why throw instead of using a default connection string?"
>
> ✅ **A:** A hardcoded fallback masks misconfiguration -- the app would start, connect to the wrong DB, and potentially corrupt data silently; throwing at startup surfaces the problem immediately in logs.

> 💬 **Q:** "What does the `??` operator do here with `throw`?"
>
> ✅ **A:** The null-coalescing operator `??` evaluates the right side when the left is null; since C# 7, `throw` is an expression, so `?? throw` is a concise null-guard pattern.

> 💬 **Q:** "What if the connection string key exists but the value is an empty string?"
>
> ✅ **A:** GetConnectionString returns the empty string (not null), so `?? throw` does not fire -- the app starts but EF Core fails on the first DB call with a connection error, which the exception middleware maps to 500.

### Step 7: DI registrations

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Program.cs

**📍 LINE:** 61-74

**🗣️ SAY:** "All services are Scoped to match DbContext lifetime -- Singleton with Scoped DbContext would create a captive dependency."
> 💬 **Q:** "What is a captive dependency and why is it dangerous?"
>
> ✅ **A:** A captive dependency is when a Singleton captures a Scoped service -- the Scoped instance is never disposed/recreated, so it holds a stale DB connection for the app's entire lifetime, causing connection pool exhaustion and data staleness.

> 💬 **Q:** "Why not register services as Transient?"
>
> ✅ **A:** Transient would create multiple DbContext instances per request, breaking transaction consistency -- two repository calls in the same request would see different snapshots.

> 💬 **Q:** "Have you considered using Dapper instead of EF Core for reads?"
>
> ✅ **A:** Dapper is faster for raw SQL, but EF Core's LINQ projections and DbContext tracking are sufficient here; I would consider Dapper for complex reporting queries where hand-tuned SQL outperforms generated LINQ.

> 💬 **Q:** "Why AddMemoryCache instead of a distributed cache like Redis?"
>
> ✅ **A:** IMemoryCache is sufficient for single-instance deployment with no network latency; for multi-instance scaling, replace with IDistributedCache backed by Redis for cross-node consistency.

> 💬 **Q:** "You used interface for ITollRulesRepository — why not an abstract class?"
>
> ✅ **A:** Services share a behavioral contract, not state. Interface allows multiple implementations (real repo + test stub) without inheritance coupling.

>
> 📝 **CODE NOTE:** [Program.cs:59] — NOTE: EnableRetryOnFailure: automatic retry on transient SQL errors (network blips, deadlocks). Skip when using an outer retry policy (e.g. Polly) to avoid compounding retry delays.
>
> 📝 **CODE NOTE:** [Program.cs:77] — ADR-15: Swagger + XML docs for self-serve API documentation. Trade-off: documentation must be maintained as contracts evolve.

> ⚠️ **IMPROVE:** Replace IMemoryCache with Redis IDistributedCache + pub/sub invalidation when horizontal scaling is needed -- current in-process cache cannot share state across instances.

### Step 8: Middleware order

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Program.cs

**📍 LINE:** 125

**🗣️ SAY:** "Exception handler is the outermost middleware layer so it catches exceptions from all inner middleware -- order matters in the onion model."
> 💬 **Q:** "What happens if you register the exception handler after MapControllers?"
>
> ✅ **A:** Controller exceptions would bubble past the handler uncaught and result in the default developer exception page or a raw 500, not a ProblemDetails response.

> 💬 **Q:** "What is the ASP.NET middleware onion model?"
>
> ✅ **A:** Each middleware wraps the next like onion layers; requests flow inward and responses/exceptions flow outward, so the outermost middleware sees all exceptions from all inner layers.

> 💬 **Q:** "What HTTP response does a client get if someone throws an ArgumentException that is not one of the three domain types?"
>
> ✅ **A:** It falls through all three switch cases, hits the catch-all branch, and returns a 500 with the sanitized message "An unexpected error occurred" -- the real exception is logged server-side only.

> ⚠️ **IMPROVE:** Add rate limiting middleware on public endpoints to prevent abuse/DDoS on the calculation endpoint.

### Step 9: Startup safety

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Program.cs

**📍 LINE:** 133-134

**🗣️ SAY:** "Database init and year seeding run at startup with CancellationToken from ApplicationStopping, and failures are logged as warnings, not fatal."
> 💬 **Q:** "Why use EnsureCreatedAsync instead of migrations?"
>
> ✅ **A:** EnsureCreated is a dev/demo convenience for quick schema setup; in production you'd use migrations for versioned, reversible, auditable schema evolution.

> 💬 **Q:** "Why pass ApplicationStopping as the CancellationToken?"
>
> ✅ **A:** If the host is shutting down during startup, the token cancels the seeding task so it doesn't delay graceful shutdown by running to completion on a dying process.

> 💬 **Q:** "What if the database is completely down at startup?"
>
> ✅ **A:** InitializeDatabaseAsync catches the exception and logs a warning -- the app starts degraded and returns 500s on the first request that triggers a cache miss against the unavailable DB.

> 💬 **Q:** "Why use EnsureCreatedAsync instead of EF Core migrations in production?"
>
> ✅ **A:** EnsureCreated is a dev/demo shortcut that cannot evolve schema incrementally; in production, migrations provide versioned, reversible, CI-auditable schema changes.

>
> 📝 **CODE NOTE:** [Program.cs:145] — ADR-14: Startup safety -- ensure schema + seed; failures logged as warnings, not fatal. Trade-off: runtime may start degraded if DB is unavailable at boot.
> 
>
> 📝 **CODE NOTE:** [Program.cs:148] — NOTE: static local functions: no captured state, explicit parameter passing. Use non-static local functions when you intentionally need closures.
> 
>
> 📝 **CODE NOTE:** [Program.cs:154] — ALTERNATIVE: async void -- never used because void exceptions crash the process (no Task to observe the exception), making failures silent and unrecoverable.
>
> 📝 **CODE NOTE:** [Program.cs:129] — ALTERNATIVE: without CancellationToken -- not used because startup tasks would run to completion even during shutdown, delaying graceful stop.
>
> 📝 **CODE NOTE:** [YearRulesSeedService.cs:22] — ADR-7: JSON startup seed, idempotent by missing year. Missing file = skip; existing year = no overwrite. Seed file is initialization source, not ongoing truth.
>
> 📝 **CODE NOTE:** [YearRulesSeedService.cs:72] — NOTE: Private nested DTOs: seed JSON shape is an implementation detail -- not exposed outside this class.

> ⚠️ **IMPROVE:** Switch from EnsureCreatedAsync to MigrateAsync with versioned migration files -- without migrations, schema changes like widening decimal(2,0) are impossible.

### Step 10: Controller entry point

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Controllers/TollFeeController.cs

**📍 LINE:** 52

**🗣️ SAY:** "GET with DateTime[] from query string -- avoids a request body on GET which some proxies drop."
> 💬 **Q:** "Why does the controller return Task<CalculateFeeResponse> instead of Task<ActionResult<CalculateFeeResponse>>?"
>
> ✅ **A:** The exception middleware handles all error-to-status-code mapping, so the controller never needs to return NotFound/BadRequest directly; returning the DTO directly keeps it thinner.

> 💬 **Q:** "What does the `sealed` keyword on the controller do?"
>
> ✅ **A:** It prevents subclassing, which enables the JIT compiler to devirtualize method calls (replace vtable lookups with direct calls) since it can prove no override exists.

>
> 📝 **CODE NOTE:** [TollFeeController.cs:8] — NOTE: [ApiController] enables automatic model validation (returns 400 on invalid model state), automatic [FromBody] inference, and ProblemDetails for validation errors.
>
> 📝 **CODE NOTE:** [TollFeeController.cs:12] — NOTE: [Route("[controller]")] uses controller name as URL segment -- token replaced at runtime with class name minus "Controller" suffix. ALTERNATIVE: hardcoded [Route("TollFee")] breaks if class is renamed.
>
> 📝 **CODE NOTE:** [TollFeeController.cs:21] — NOTE: ControllerBase (not Controller): no View support needed for a pure API -- smaller base class, no Razor dependency.
>
> 📝 **CODE NOTE:** [TollFeeController.cs:27] — ADR-1: Contract-first evolution -- internal architecture changed while preserving the TollFee endpoint surface. Trade-off: requires consistent exception discipline in services.
>
> 📝 **CODE NOTE:** [TollFeeController.cs:50] — ALTERNATIVE: async void -- never used because void exceptions crash the process (no Task to observe the exception), making failures silent and unrecoverable.

> 🔗 **SEE ALSO:** [Part 7 — C# Language Features](#c-language-features) for the full pattern/where/why table.

> 💬 **Q:** "What's the HTTP response if the query string has 1001 passages?"
>
> ✅ **A:** TollService.ValidateInput throws InvalidTollRequestException with "exceeds the limit 1000", which the exception middleware maps to a 400 ProblemDetails with title "Invalid toll calculation request."

> 💬 **Q:** "You sealed this class — what if someone needs to extend it?"
>
> ✅ **A:** They shouldn't — this is a final implementation. If extension is needed later, unseal it deliberately. Seal by default, unseal intentionally.

> ⚠️ **IMPROVE:** Add API key or JWT authentication to track usage and prevent unauthorized access -- currently the API is fully anonymous.

### Step 11: Controller delegates to service

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Controllers/TollFeeController.cs

**📍 LINE:** 54

**🗣️ SAY:** "The controller is a thin pass-through -- all logic lives in TollService."
> 💬 **Q:** "Why not put the calculation logic directly in the controller?"
>
> ✅ **A:** Separating orchestration into TollService makes the business logic unit-testable without spinning up the ASP.NET pipeline, and keeps controllers as thin HTTP adapters.

> 💬 **Q:** "What is the primary constructor syntax `TollFeeController(ITollService tollService)`?"
>
> ✅ **A:** C# 12 primary constructors capture the parameter as an implicit field, eliminating the boilerplate of declaring a private field, writing a constructor body, and null-checking.

### Step 12: Empty-input guard

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Calculation/TollService.cs

**📍 LINE:** 35-38

**🗣️ SAY:** "Empty input returns immediately with zero values -- no DB hit needed."
> 💬 **Q:** "Why check `passages.Length == 0` before validation?"
>
> ✅ **A:** Validation calls `.Min()` and `.Max()` which throw on empty arrays; the early return avoids that and also skips the unnecessary DB roundtrip for configured-year checks.

> 💬 **Q:** "What happens if the database is down when a request with passages comes in?"
>
> ✅ **A:** GetOrCreateAsync's factory fails, the exception bubbles up through TollService, and the exception middleware catches it and returns a 500 ProblemDetails with "An unexpected error occurred."

### Step 13: Timezone normalization

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Calculation/TollService.cs

**📍 LINE:** 46

**🗣️ SAY:** "All timestamps are normalized to Gothenburg local time before any business logic using Array.ConvertAll for a single allocation."
> 💬 **Q:** "Why not keep everything in UTC and convert only when looking up fee bands?"
>
> ✅ **A:** Converting once upfront simplifies all downstream logic (grouping by day, toll-free checks, fee band lookup) -- scattering conversions risks inconsistency, especially around DST boundaries.

> 💬 **Q:** "Why Array.ConvertAll instead of LINQ Select().ToArray()?"
>
> ✅ **A:** ConvertAll allocates a single array directly, while Select creates an intermediate iterator object before materializing -- slightly more efficient for a pure element-wise transformation.

### Step 14: Timezone resolution

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Calculation/TollService.cs

**📍 LINE:** 181-186

**🗣️ SAY:** "The switch expression dispatches on DateTimeKind: Unspecified is assumed local, UTC is converted, and Local from another zone is re-mapped."
> 💬 **Q:** "What happens during a DST transition -- does a passage at 02:30 CET get double-counted?"
>
> ✅ **A:** TimeZoneInfo.ConvertTimeFromUtc handles ambiguous/invalid times according to the system's adjustment rules; the code normalizes once so downstream logic sees consistent local times.

> 💬 **Q:** "Why is `DateTimeKind.Unspecified` assumed to be local?"
>
> ✅ **A:** JSON deserialization of timestamps without offset produces Unspecified kind; assuming local matches the common case where a Swedish client sends local Gothenburg times without specifying the zone.

> 💬 **Q:** "What happens if the system has neither 'Europe/Stockholm' nor 'W. Europe Standard Time' time zone?"
>
> ✅ **A:** ResolveGothenburgTimeZone throws InvalidOperationException at static field initialization, crashing the app on the first request that touches TollService -- a fail-fast design.

>
> 📝 **CODE NOTE:** [TollService.cs:178] — ALTERNATIVE: if-else chain -- not used because switch expression is exhaustive (compiler warns if a case is missing) and more concise for dispatching on an enum value.

> ⚠️ **IMPROVE:** Switch from DateTime to DateTimeOffset in the API contract to eliminate timezone ambiguity -- Unspecified kind assumed as local is implicit and error-prone.

### Step 15: Input validation

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Calculation/TollService.cs

**📍 LINE:** 155-170

**🗣️ SAY:** "Guard-rails: max 1000 passages and max 370-day date range to prevent abuse or accidental excessive DB load."
> 💬 **Q:** "Why 370 days instead of 365?"
> 
> ✅ **A:** 370 accommodates leap years plus a small buffer so a request spanning Jan 1 to Dec 31 of a leap year (366 days) is not rejected, while still capping unreasonably wide ranges.

> 💬 **Q:** "What's the alternative to throwing exceptions for validation?"
>
> ✅ **A:** A Result<T> pattern avoids exception overhead, but here the invalid input is exceptional (abuse/misconfiguration), and the exception middleware maps it to a clean 400 ProblemDetails without per-layer unwrapping.

> 💬 **Q:** "What's the max passages and what happens at 1001?"
>
> ✅ **A:** MaxPassagesPerRequest is 1000; at 1001, ValidateInput throws InvalidTollRequestException with a message about exceeding the limit, mapped to a 400 ProblemDetails by the exception middleware.

> 💬 **Q:** "What if the date range spans exactly 370 days?"
>
> ✅ **A:** The check is `dateRangeDays > MaxDateRangeDays` (strict greater-than), so exactly 370 days passes validation -- only 371+ days triggers the 400 rejection.

> 💬 **Q:** "What if a fee band amount is 100 but the SQL decimal(2,0) column max is 99?"
>
> ✅ **A:** The validator only checks `Amount < 0` and does not enforce an upper bound -- the DB rejects the value with a truncation error, resulting in a 500 instead of a 400. This is a known validation gap.

>
> 📝 **CODE NOTE:** [TollService.cs:153] — ADR-13: Hard-limit request size and date span to protect against expensive/abusive inputs. Trade-off: some edge requests are rejected intentionally (400).
>
> 📝 **CODE NOTE:** [YearRuleConfigurationValidator.cs:6] — NOTE: Static class with pure validation logic, no dependencies or state. ALTERNATIVE: injectable service -- not used because there is nothing to inject or mock.
>
> 📝 **CODE NOTE:** [YearRuleConfigurationValidator.cs:18] — ALTERNATIVE: if (year < 1 || year > 9999) -- not used because pattern matching reads like English and avoids logic-inversion bugs with compound boolean expressions.

> ⚠️ **IMPROVE:** Add an upper-bound check (amount > 99) in the validator so invalid fees return a clean 400 instead of a DB truncation 500.

### Step 16: Year configuration check

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Calculation/TollService.cs

**📍 LINE:** 113-121

**🗣️ SAY:** "Before calculating, we verify all requested years are configured -- if not, a YearNotConfiguredException triggers a 400 ProblemDetails."
> 💬 **Q:** "Why check configured years before loading fee bands?"
>
> ✅ **A:** Loading fee bands for an unconfigured year would silently return empty results and calculate zero fees -- checking first gives a clear 400 error telling the client which years are missing.

> 💬 **Q:** "Why a separate exception type (YearNotConfiguredException) instead of a generic BadRequestException?"
>
> ✅ **A:** Separate types give type-safe catch in tests (`Assert.ThrowsAsync<T>`), distinct ProblemDetails titles, and separate Serilog EventIds for filterable alerting.

> 💬 **Q:** "What happens when you request passages spanning both a configured and an unconfigured year?"
>
> ✅ **A:** EnsureAllYearsAreConfiguredAsync collects all unconfigured years and throws YearNotConfiguredException listing them all, so the client knows exactly which years to configure.

### Step 17: Cache-backed data loading

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Calculation/TollService.cs

**📍 LINE:** 54-55

**🗣️ SAY:** "Fee bands and toll-free dates are loaded per-year from cache; DB is only hit on cache miss."
> 💬 **Q:** "What is the cache TTL and why?"
>
> ✅ **A:** 12 hours -- toll rules change rarely (admin action only), so a long TTL is acceptable; explicit invalidation on writes handles the common case, and TTL is just a safety net.

> 💬 **Q:** "Why per-year cache keys instead of one big cache entry?"
>
> ✅ **A:** Per-year keys allow invalidating only the changed year on write, avoiding a full cache flush; it also keeps entries small and lookup O(1) per year.

> 💬 **Q:** "What if the GetOrCreateAsync factory throws because the DB is down?"
>
> ✅ **A:** The exception is not cached -- subsequent requests retry the factory, so a transient DB outage does not permanently poison the cache with a failed entry.

### Step 18: In-place sort

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Calculation/TollService.cs

**📍 LINE:** 62

**🗣️ SAY:** "Array.Sort in-place once globally so per-day slices are already ordered -- avoids re-sorting inside the engine and avoids the extra allocation of OrderBy().ToArray()."
> 💬 **Q:** "Why Array.Sort instead of OrderBy().ToArray()?"
>
> ✅ **A:** Array.Sort sorts in-place with zero extra allocation, while OrderBy creates an intermediate iterator and a new array copy -- for a hot path this avoids unnecessary GC pressure.

> 💬 **Q:** "Is it safe to mutate the localPassages array since it was created by ConvertAll?"
>
> ✅ **A:** Yes, ConvertAll already returned a new array, so sorting it in-place does not affect the caller's original `passages` parameter.

### Step 19: Single-pass grouping

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Calculation/TollService.cs

**📍 LINE:** 65-88

**🗣️ SAY:** "One loop collects distinct days for the average calculation and groups chargeable passages by day, skipping toll-free dates."
>
> 📝 **CODE NOTE:** [TollService.cs:75] — NOTE: TryGetValue performs a single dictionary lookup returning both existence check and value. Alternative: ContainsKey + indexer does two lookups.
>
> 📝 **CODE NOTE:** [TollService.cs:77] — NOTE: out var list -- inline variable declaration in the out parameter (C# 7). Alternative: declare on a separate line.
>
> 📝 **CODE NOTE:** [TollService.cs:82] — ALTERNATIVE: new List<DateTime>() -- not used because [] is shorter and the compiler can optimize the collection expression into the most efficient form.

> 💬 **Q:** "Why not use LINQ GroupBy instead of a manual loop?"
>
> ✅ **A:** The loop does two things in one pass: collecting distinct days (including toll-free) for the average denominator, and grouping only chargeable passages -- GroupBy would need a second pass or post-processing to separate toll-free days.

> 💬 **Q:** "Why include toll-free days in the average denominator?"
>
> ✅ **A:** The average divides across ALL days the vehicle was seen, including toll-free ones; this gives a realistic per-day cost metric rather than inflating it by excluding zero-fee days.

> 💬 **Q:** "What if every single passage in the request is on a toll-free date?"
>
> ✅ **A:** chargeablePassagesByDay is empty, the `.Sum()` returns 0, and distinctDays still counts the days for the average -- the response is totalFee=0 with averageFeePerDay=0.

> 💬 **Q:** "You used float for average and not decimal — why?"
>
> ✅ **A:** Average is a display metric, not a financial amount used in further calculations. Decimal is slower and overkill for a rounded display value.

### Step 20: Toll-free date check

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Calculation/TollService.cs

**📍 LINE:** 134-151

**🗣️ SAY:** "Weekends and July are toll-free by code, and configured holiday dates use a FrozenSet for constant-time Contains lookup."
> 💬 **Q:** "Why are weekends and July hardcoded but holidays are configurable?"
>
> ✅ **A:** Weekends and July are fixed by Gothenburg regulation and unlikely to change, while public holidays vary by year and need configuration flexibility.

> 💬 **Q:** "What is FrozenSet and why use it over HashSet?"
>
> ✅ **A:** FrozenSet (.NET 8+) is optimized for repeated read-only lookups on data that never changes after creation; it also prevents accidental Add/Remove that could corrupt shared cached data.

> 💬 **Q:** "What if a passage falls on a Saturday in July?"
>
> ✅ **A:** The weekend check (`DayOfWeek is Saturday or Sunday`) returns true first -- the July check never runs because IsTollFreeDate short-circuits on the first true condition.

> 💬 **Q:** "What if the toll-free dates dictionary has no entry for the passage's year?"
>
> ✅ **A:** TryGetValue returns false, the `&&` short-circuits, and the method returns false -- the passage is not treated as toll-free from the configured-dates perspective (weekends/July checks still apply above).

> 💬 **Q:** "Why FrozenSet and not just a regular array?"
>
> ✅ **A:** Need constant-time Contains() for toll-free date checks. Array.Contains() scans every element. FrozenSet hashes for instant lookup.

> 💬 **Q:** "Why pattern matching instead of if/else with ==?"
>
> ✅ **A:** Pattern matching reads like English ('is Saturday or Sunday') and the compiler enforces exhaustiveness. Avoids logic-inversion bugs from negated boolean chains.

>
> 📝 **CODE NOTE:** [TollService.cs:123] — WHY: IReadOnlySet<DateOnly>: constant-time Contains lookup for toll-free date checks (FrozenSet at runtime). ALTERNATIVE: IReadOnlyCollection.Contains() scans every element linearly.
>
> 📝 **CODE NOTE:** [TollService.cs:129] — WHY: DateOnly (not DateTime): toll-free is a date concept, no time component needed. Prevents accidental time-of-day comparisons.

> 🔗 **SEE ALSO:** [Part 7 — Caching Patterns](#caching-patterns) for the full pattern/where/why table.

### Step 21: Daily fee delegation

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Calculation/TollService.cs

**📍 LINE:** 91-92

**🗣️ SAY:** "Delegates to the static CongestionRuleEngine per day -- TollService is orchestration-only, the engine does the math."
> 💬 **Q:** "Why is CongestionRuleEngine a static class instead of an injected service?"
>
> ✅ **A:** It contains only pure functions with no dependencies and no state, so there is nothing to inject or mock -- static is simpler and avoids unnecessary DI registration.

> 💬 **Q:** "How would you change this if the daily cap became configurable per year?"
>
> ✅ **A:** Move the DailyCap constant into the year configuration (DB/cache), pass it as a parameter to CalculateDailyFee, and promote the engine to an injectable service if it needs repository access.

> 💬 **Q:** "What if a day has only one passage at a toll-free time like 03:00 AM?"
>
> ✅ **A:** IsTollFreeDate does not catch it (03:00 on a weekday non-July non-holiday is not toll-free), but GetFeeForPassage returns 0 because no fee band covers 03:00 -- so the daily fee is 0.

> ⚠️ **IMPROVE:** Add output caching on the calculation endpoint -- same input produces the same output, so caching eliminates all computation for repeated requests.

### Step 22: GetFeeForPassage

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Calculation/CongestionRuleEngine.cs

**📍 LINE:** 32-41

**🗣️ SAY:** "Converts time to minute-of-day for a single int comparison per band, and FeeBand being a struct means FirstOrDefault returns default with Amount=0 when no band matches."
>
> 📝 **CODE NOTE:** [CongestionRuleEngine.cs:8] — ADR-5: Service orchestration vs rule-engine computation -- TollService handles orchestration, CongestionRuleEngine handles pure fee math. Trade-off: extra abstraction, but each class is cognitively smaller.
>
> 📝 **CODE NOTE:** [CongestionRuleEngine.cs:28] — WHY: int (not decimal): fees are whole SEK by regulation. Avoids floating-point rounding in aggregation. ALTERNATIVE: SingleOrDefault -- not used because it throws when multiple bands match.
>
> 📝 **CODE NOTE:** [CongestionRuleEngine.cs:38] — INTERVIEW: "What does FirstOrDefault return when no band matches?" -- "FeeBand is a struct so default(FeeBand) has Amount=0 (all fields zero-initialized). If it were a record class, FirstOrDefault would return null and .Amount would throw NullReferenceException."

> 💬 **Q:** "What does FirstOrDefault return when FeeBand is a struct and no band matches?"
>
> ✅ **A:** It returns `default(FeeBand)` which zero-initializes all fields (FromMinute=0, ToMinute=0, Amount=0); accessing .Amount gives 0 (no fee) without a null check -- if it were a class, it would return null and .Amount would throw NullReferenceException.

> 💬 **Q:** "Why use minute-of-day integers instead of TimeSpan or TimeOnly?"
>
> ✅ **A:** Integer range comparison (`minuteOfDay >= from && minuteOfDay <= to`) is a single CPU comparison per band with no parsing or allocation; TimeSpan adds overhead for what is fundamentally a simple range check.

> 💬 **Q:** "What if two fee bands overlap and a passage falls in both?"
>
> ✅ **A:** FirstOrDefault returns the first matching band in iteration order; the validator prevents overlaps at configuration time, but if data is manually corrupted, the first match wins silently.

### Step 23: 60-minute window logic

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Calculation/CongestionRuleEngine.cs

**📍 LINE:** 68-98

**🗣️ SAY:** "Iterates sorted passages: if the next passage is within 60 minutes of the window start, keep only the highest fee; otherwise commit the window and start a new one."
> 💬 **Q:** "What happens if the passages are not sorted?"
>
> ✅ **A:** The window logic assumes chronological order; unsorted input would create wrong windows and miss the highest-fee-in-window rule -- that is why TollService sorts globally before delegating.

> 💬 **Q:** "Why track the window with a start+60min end time instead of comparing each pair of consecutive passages?"
>
> ✅ **A:** The window anchors on the first passage in the group; comparing only consecutive pairs would create a sliding window that could chain indefinitely (A->B within 60, B->C within 60, but A->C could be 90 minutes apart and still grouped).

> 💬 **Q:** "What if all 1000 passages are in one 60-minute window?"
>
> ✅ **A:** The loop iterates all 1000 passages, keeps only the highest fee from that single window, commits it once, and Math.Min caps at 60 SEK -- only one fee is charged.

> 💬 **Q:** "What if the passages list for a day is empty?"
>
> ✅ **A:** CalculateDailyFee's `passages.Count == 0` guard returns 0 immediately -- this can happen if all passages on that day were filtered out as toll-free before reaching the engine.

### Step 24: Window boundary precision

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Calculation/CongestionRuleEngine.cs

**📍 LINE:** 80-83

**🗣️ SAY:** "Strict less-than on window end: 07:00 and 08:00 are 60 minutes apart so they are in different windows and both are charged."
> 💬 **Q:** "Why strict less-than (`<`) instead of less-than-or-equal (`<=`)?"
>
> ✅ **A:** The spec says within 60 minutes; 07:00 to 08:00 is exactly 60 minutes, which means the window has expired -- using `<=` would incorrectly merge them into one window.

> 💬 **Q:** "What if two passages happen at the exact same time?"
>
> ✅ **A:** The second passage is strictly less than windowEnd, so it stays in the same window; only the higher fee is kept, which is correct behavior.

> 💬 **Q:** "What if a passage is at 07:00 and the next is at 07:59:59?"
>
> ✅ **A:** 07:59:59 is still less than 08:00 (the window end), so both are in the same window and only the highest fee is charged -- the boundary is at the minute level via AddMinutes(60).

### Step 25: Daily cap

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Calculation/CongestionRuleEngine.cs

**📍 LINE:** 106

**🗣️ SAY:** "Math.Min applies the 60 SEK daily cap from Gothenburg regulation."
> 💬 **Q:** "Why is the daily cap a const instead of configurable?"
>
> ✅ **A:** The 60 SEK cap is defined by Gothenburg regulation and unlikely to change per-year; if it does become per-year, it would move to the DB configuration alongside fee bands.

> 💬 **Q:** "Why Math.Min instead of an if-else?"
>
> ✅ **A:** Both are equivalent, but Math.Min is a single expression that is more concise and clearly communicates the intent of clamping to a maximum value.

> 💬 **Q:** "What if a vehicle has 10 passages across 5 different windows totaling 80 SEK?"
>
> ✅ **A:** Math.Min(80, 60) returns 60 -- the daily cap clamps the total, so the vehicle is never charged more than 60 SEK regardless of how many windows or passages exist.

---

## Part 3: Code Walkthrough -- Data Layer

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

### Persistence and Caching

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**Original:** `TollDBContext` was a scaffold-generated partial class with:
- Composite business key on Fee: `HasKey(e => new { e.Year, e.FromMinute, e.ToMinute, e.Price })`
- Composite key on TollFree: `HasKey(e => new { e.Year, e.Date })`
- Connection string hardcoded in `OnConfiguring`: `"Server=(localdb)\\MSSQLLocalDB;Database=TollDB;Trusted_Connection=True;"`
- `#nullable disable`
- `partial class` with `OnModelCreatingPartial` -- scaffold pattern
- `Fee` had `long FromMinute`, `long ToMinute` -- unnecessarily wide types
- `TollFree` had `DateTime Date` -- no date-only type in .NET 5
- **Never used.** No code called the context.

**Now:**

`TollDbContext` (`Application/Persistence/TollDbContext.cs:6`):
- Primary constructor: `TollDbContext(DbContextOptions<TollDbContext> options)`
- Global NoTracking (`:13`) -- removed 5 per-query `.AsNoTracking()` calls
- Surrogate `Id` PK (was composite business key) with separate unique constraints
- `(Year, FromMinute, ToMinute)` unique with included `Price` (covering index)
- `(Year, Date)` unique for TollFree
- Standalone year indexes for lookups
- Collation kept from original. `decimal(2,0)` also kept -- max 99, sufficient for current fees (0-22 SEK) and daily cap (60). Widening requires a migration, which I deferred since no migration infrastructure exists yet
- `EnableRetryOnFailure()` for transient faults
- Connection string from config with fail-fast (`Program.cs:39`): `?? throw new InvalidOperationException(...)`

Entity changes from original:
- `Fee.FromMinute`: `long` -> `int` (minutes don't need 64 bits)
- `Fee.ToMinute`: `long` -> `int`
- `TollFree.Date`: `DateTime` -> `DateOnly` (available since .NET 6)
- Both entities: `partial class` with `#nullable disable` -> `sealed class` with nullable enabled
- Both inherit `YearScopedEntity` (`DataModels/Abstractions/YearScopedEntity.cs:6`) -- abstract class sharing `Id` + `Year`

`TollRulesRepository` (`Application/Persistence/Repositories/TollRulesRepository.cs:12`):
- `IMemoryCache` with 12-hour TTL (`:14`)
- Three cache key patterns: configured-years (`FrozenSet<int>`), fees-per-year (`FeeBand[]`), tollfree-per-year (`FrozenSet<DateOnly>`)
- Cache key memoization via `ConcurrentDictionary<int, string>` (`:18-19`, `:186-190`) -- `static` lambda prevents closure allocation
- Multi-year delegation (`:53`) -- calls cached single-year methods (original had none of this)
- Transactional writes (`:97-133`) -- `ExecuteDeleteAsync` + `AddRange` inside execution strategy callback
- Cache invalidation (`:179`) -- 3 keys removed per year write

| | |
|---|---|
| **Why** | Original had DB schema but ignored it. Now DB is authoritative. Caching eliminates hot-path round-trips. |
| **Trade-off: cache** | Process-local. Multi-instance -> Redis. Documented. |
| **Trade-off: schema** | `EnsureCreated` -- no migration support yet. Schema evolution -> `MigrateAsync`. Documented. |

| Decision | Why | Alternative | Trade-off |
|---|---|---|---|
| Caching with explicit invalidation (`IMemoryCache` + 12h TTL) | Read-heavy workload; same hot year(s) queried repeatedly | No caching; TTL-only without explicit invalidation | Process-local; multi-instance needs distributed cache for cross-node immediacy |
| Multi-year queries delegate to cached single-year methods | Hot path was bypassing per-year cache and hitting DB every request; 1-2 cache lookups instead of 2 DB round-trips | Multi-year composite cache keys; no change | Sequential lookups per year; negligible for 1-2 years; batch approach can return as fallback |
| Surrogate PK (Primary Key) + unique business constraints + year indexes | Stable row identity for EF; enforce business uniqueness; optimize year lookups | Keep composite business key as PK | More indexes increase write maintenance cost; acceptable for read-heavy + moderate writes |
| NoTracking as global DbContext default | Every read query already called `.AsNoTracking()` individually; global eliminates repetition | Per-query `.AsNoTracking()` | Future write paths needing tracking must explicitly opt in with `.AsTracking()` |
| SQL Server retry with execution strategy | SQL Server can return transient errors; automatic retry | No retry | Retries add latency on transient failures; acceptable for correctness |
| Connection string fail-fast (`?? throw`) | Hardcoded fallback masks config errors and is a security risk | Hardcoded fallback connection string | Requires connection string in config; already the case for all environments |
| Entity classes sealed | EF Core does not require inheritance here; JIT devirtualization (replacing indirect method-table lookups with direct calls); communicates "not an extension point" | Leave unsealed | None; abstract base `YearScopedEntity` remains abstract, concrete subclasses sealed |

**Flow: Caching Strategy**

Source: `TollRulesRepository.cs:37`, `:53`, `:179`, `TollDbContext.cs:13`

```
Read path (fee bands or toll-free dates for a year):
|
+-- IMemoryCache.GetOrCreateAsync(key)
    |
    +-- [HIT] --> return cached FrozenSet/array (no DB query)
    |
    +-- [MISS]
        |
        +-- Query DB (NoTracking global default, projection only)
        +-- Materialize as FrozenSet (toll-free) or array (fee bands)
        +-- Cache with 12-hour absolute expiration
        +-- Return result

Multi-year read path (hot calculation path):
|
+-- For each distinct year:
    +-- Delegate to cached single-year method above
    +-- Aggregate into dictionary
|
+-- Return dictionary (0 DB queries on cache-warm requests)

Write path (after transaction commits):
|
+-- InvalidateCache(year):
    +-- Remove "tollrules:configured-years"
    +-- Remove "tollrules:fees:{year}"
    +-- Remove "tollrules:tollfree:{year}"
```

Cache key memoization:
- `ConcurrentDictionary<int, string>` avoids allocating interpolated key strings on every lookup.

Design constraints:
- Process-local `IMemoryCache`. Multi-instance deployment would need distributed cache for cross-node immediacy.
- `FrozenSet<T>` for toll-free dates gives O(1) lookup after one-time construction cost.
- `QueryTrackingBehavior.NoTracking` set globally on `TollDbContext` -- all read queries skip change tracking.

### Code Walkthrough Steps: Data Layer

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

### Step 26: FeeBand struct

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/DataModels/FeeBand.cs

**📍 LINE:** 34

**🗣️ SAY:** "Readonly record struct -- 12 bytes on the stack, no heap allocation, free structural equality, and default gives Amount=0."
>
> 📝 **CODE NOTE:** [FeeBand.cs:8] — ADR-20: FeeBand as readonly record struct (12 bytes, stack-allocated). Alternatives: record class (heap, unnecessary GC), plain struct (no built-in equality). Trade-off: FirstOrDefault returns default(FeeBand) with Amount=0.
>
> 📝 **CODE NOTE:** [FeeBand.cs:29] — INTERVIEW: "Why int minute-of-day instead of HHmm strings or TimeSpan?" -- "Integer range comparison is a single CPU comparison per band -- no parsing, no allocation. Strings need parsing or fragile lexicographic comparison. TimeSpan adds unnecessary overhead."

> 💬 **Q:** "Why a record struct instead of a record class?"
>
> ✅ **A:** FeeBand is only 12 bytes (3 ints), so it fits on the stack with no heap allocation or GC pressure; a record class would allocate on the heap unnecessarily for such a small value type.

> 💬 **Q:** "What does `readonly` on a record struct guarantee?"
>
> ✅ **A:** It guarantees all fields are immutable after construction -- the compiler enforces that no method can modify any field, enabling safe sharing without defensive copies.

> 💬 **Q:** "Why int Amount instead of decimal?"
>
> ✅ **A:** Fees are whole SEK by regulation, so int provides simpler arithmetic without floating-point rounding concerns; decimal would be appropriate if fees had fractional parts.

> 💬 **Q:** "What happens if you pass a FeeBand with negative FromMinute to the rule engine?"
>
> ✅ **A:** The rule engine does not validate -- it relies on the upstream YearRuleConfigurationValidator to reject negative values at configuration time. Passing corrupted data would silently match no bands (Amount=0).

> 💬 **Q:** "You used record for DTOs — why not a regular class?"
>
> ✅ **A:** Records give structural equality, ToString with all property values, and with-expression for copies — all free. A class needs manual Equals/GetHashCode overrides.

> 🔗 **SEE ALSO:** [Part 7 — Type Design](#type-design) for the full pattern/where/why table.

### Step 27: IFeeBandShape interface

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/DataModels/Abstractions/IFeeBandShape.cs

**📍 LINE:** 12-22

**🗣️ SAY:** "Shared shape interface so one ToFeeBand() extension works across DTOs, entities, and seed types -- interface because structs cannot inherit from an abstract class."
> 💬 **Q:** "Why an interface instead of an abstract class here?"
>
> ✅ **A:** FeeBand is a struct and structs cannot inherit from classes in C#; an interface is the only way to share a contract across both structs and classes.

> 💬 **Q:** "What is the benefit of a shared ToFeeBand() extension method?"
>
> ✅ **A:** One mapping method works for any IFeeBandShape implementor (DTOs, entities, seed types), eliminating duplicate mapping code for each type.

>
> 📝 **CODE NOTE:** [IFeeBandShape.cs:3] — ADR-10: Data model centralization -- IFeeBandShape + YearScopedEntity reduce duplication across DTO/entity/model types. Interface (not abstract class) so both structs and classes can implement it.

> ⚠️ **IMPROVE:** Evaluate removing IFeeBandShape -- only FeeBand implements it after the HHmm change, so the interface may be unnecessary abstraction.

### Step 28: YearScopedEntity base

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/DataModels/Abstractions/YearScopedEntity.cs

**📍 LINE:** 11

**🗣️ SAY:** "Abstract base class for Fee and TollFree entities -- shares Id (get-only, DB-generated) and Year (init-only, write-once)."
> 💬 **Q:** "What is the difference between `get` and `init` on properties?"
>
> ✅ **A:** `get`-only (Id) means the value can only be set in the constructor and never changed; `init` (Year) allows setting during object initialization (`new Fee { Year = 2026 }`) but is read-only after that.

> 💬 **Q:** "Why an abstract class here but an interface for IFeeBandShape?"
>
> ✅ **A:** Fee and TollFree share state (Id, Year) and constructor logic, which interfaces cannot provide; IFeeBandShape only shares a contract across structs and classes where inheritance is impossible.

### Step 29: Fee entity

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/DataModels/Entities/Fee.cs

**📍 LINE:** 23-28

**🗣️ SAY:** "Persistence entity with decimal Price matching the SQL decimal(2,0) column -- a checked cast on read catches overflow bugs immediately."
> 💬 **Q:** "Why decimal Price in the entity but int Amount in the domain FeeBand?"
>
> ✅ **A:** decimal matches the SQL `decimal(2,0)` column for type safety at the persistence layer; the `checked((int)x.Price)` cast on read catches overflow bugs immediately if a value exceeds int range.

> 💬 **Q:** "What does the `checked` keyword do?"
>
> ✅ **A:** It enables arithmetic overflow checking -- if the decimal-to-int cast truncates or overflows, it throws OverflowException instead of silently returning a wrong value.

> 💬 **Q:** "What if a fee band's decimal Price in the DB is 99.5 but Amount is int?"
>
> ✅ **A:** The `checked((int)99.5m)` cast truncates to 99 -- `checked` only catches overflow, not truncation of fractional parts. The decimal(2,0) column constraint prevents fractional values at the DB level.

> 💬 **Q:** "Why not just cast without checked?"
>
> ✅ **A:** Unchecked cast silently truncates on overflow — corrupted data. Checked throws immediately. Fail-fast over silent corruption.

> 💬 **Q:** "Why not DateTime for toll-free dates?"
>
> ✅ **A:** A toll-free date has no time component. DateTime would allow 2026-01-01 00:00 vs 2026-01-01 12:00 to compare unequal for the same date.

>
> 📝 **CODE NOTE:** [Fee.cs:8] — ADR-28: Entity classes sealed -- EF Core does not require inheritance here; sealing enables JIT devirtualization.
>
> 📝 **CODE NOTE:** [Fee.cs:20] — ALTERNATIVE: set -- not used because init (write-once after construction) enforces immutability, preventing accidental reassignment after entity creation.

> ⚠️ **IMPROVE:** Widen the decimal(2,0) column to decimal(5,0) via a migration to future-proof against fee increases beyond 99 SEK.

### Step 30: TollDbContext NoTracking

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Persistence/TollDbContext.cs

**📍 LINE:** 26

**🗣️ SAY:** "NoTracking globally because the workload is read-heavy -- AddRange still works because it explicitly sets state to Added."
>
> 📝 **CODE NOTE:** [TollDbContext.cs:20] — ADR-25: NoTracking as global default -- every read query was calling .AsNoTracking() individually. Trade-off: future write paths needing tracking must explicitly opt in.
>
> 📝 **CODE NOTE:** [TollDbContext.cs:29] — ADR-12: Surrogate primary keys + unique business constraints + year-focused indexes. Trade-off: more indexes increase write maintenance cost; acceptable for read-heavy pattern.

> 💬 **Q:** "What does NoTracking save you?"
>
> ✅ **A:** EF Core skips creating change-tracking snapshots for every queried entity, reducing memory and CPU overhead; for read-heavy workloads where you never update queried entities, it is pure savings.

> 💬 **Q:** "How would you update an entity if NoTracking is the default?"
>
> ✅ **A:** Either query with `.AsTracking()` to opt in, or use `context.Update(entity)` which explicitly attaches and marks all properties as modified.

> 💬 **Q:** "Have you considered using Dapper for the read queries in the repository?"
>
> ✅ **A:** EF Core's LINQ projections generate efficient SQL here, and the caching layer means DB reads are infrequent; Dapper would add raw SQL maintenance burden for minimal performance gain on already-cached data.

> 💬 **Q:** "What if a developer writes code that modifies a queried entity?"
>
> ✅ **A:** The modification won't be saved — SaveChangesAsync does nothing for untracked entities. They need to explicitly call context.Update(entity) or query with .AsTracking().

### Step 31: Covering index

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Persistence/TollDbContext.cs

**📍 LINE:** 43-45

**🗣️ SAY:** "Covering index on Year+FromMinute+ToMinute with Price included -- queries read the index only, no table lookup needed."
> 💬 **Q:** "What is a covering index and why does it matter?"
>
> ✅ **A:** A covering index includes all columns the query needs, so the DB reads the index B-tree only without a second lookup to the table heap -- this eliminates random I/O and can be 2-10x faster.

> 💬 **Q:** "Why is there a separate index on just Year?"
>
> ✅ **A:** The `ExecuteDeleteAsync WHERE Year = X` during upsert only filters by Year; the composite index (Year+FromMinute+ToMinute) is less efficient for a Year-only predicate because of the wider key.

> 💬 **Q:** "Would you use a different database for high-throughput toll collection?"
>
> ✅ **A:** For high-throughput writes, a time-series database or event store would be more appropriate; SQL Server is well-suited here because the workload is read-heavy with infrequent admin writes.

### Step 32: Repository caching with FrozenSet

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Persistence/Repositories/TollRulesRepository.cs

**📍 LINE:** 46-60

**🗣️ SAY:** "GetOrCreateAsync is atomic: cache hit returns immediately, cache miss runs the factory, and results are stored as FrozenSet for immutable, optimized lookups."
>
> 📝 **CODE NOTE:** [TollRulesRepository.cs:23] — ADR-9: In-memory cache with explicit invalidation on writes for read-heavy workloads. Trade-off: process-local cache; multi-instance deployment needs distributed caching.
>
> 📝 **CODE NOTE:** [TollRulesRepository.cs:37] — NOTE: Static ConcurrentDictionary for cache key memoization -- keys are pure functions of year, shared across all repository instances (thread-safe).
>
> 📝 **CODE NOTE:** [TollRulesRepository.cs:74] — ALTERNATIVE: unchecked -- not used because unchecked silently truncates on overflow. checked(int) throws OverflowException, catching data integrity issues immediately.

> 💬 **Q:** "Is GetOrCreateAsync truly atomic under concurrent requests?"
>
> ✅ **A:** It is thread-safe for cache access, but the factory can execute multiple times concurrently on a cold cache; this is acceptable here because the factory is idempotent (same DB query, same result).

> 💬 **Q:** "Why the `!` (null-forgiving) on the GetOrCreateAsync result?"
>
> ✅ **A:** GetOrCreateAsync returns `T?` because the factory could theoretically return null, but our factory always returns a non-null FrozenSet; the `!` suppresses the nullable warning.

> 💬 **Q:** "Why ConcurrentDictionary for cache key generation instead of a regular Dictionary?"
>
> ✅ **A:** ConcurrentDictionary is lock-free for reads and thread-safe for concurrent GetOrAdd -- a regular Dictionary would need explicit locking since multiple request threads may generate cache keys simultaneously.

> 💬 **Q:** "Why IMemoryCache and not a static Dictionary?"
>
> ✅ **A:** IMemoryCache has built-in TTL expiration, size limits, thread safety, and DI integration. Static Dictionary needs manual implementation of all of these.

> 💬 **Q:** "Why ConcurrentDictionary and not a regular Dictionary with lock?"
>
> ✅ **A:** ConcurrentDictionary is lock-free for reads and has simpler API. Regular Dictionary with lock blocks all readers during any write.

### Step 33: Cache invalidation

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Persistence/Repositories/TollRulesRepository.cs

**📍 LINE:** 238-243

**🗣️ SAY:** "Invalidation happens after commit -- if the app crashes between commit and invalidation, IMemoryCache is lost on restart anyway."
> 💬 **Q:** "Why invalidate after commit instead of before?"
>
> ✅ **A:** Pre-commit invalidation would cause a brief window where a read request hits the DB and re-caches old data if the write transaction is still in progress; post-commit ensures the cache only clears after new data is persisted.

> 💬 **Q:** "What is the worst case if invalidation fails without a crash?"
>
> ✅ **A:** The cache serves stale data for up to the 12-hour TTL safety net; subsequent reads after TTL expiry will reload the correct data from the DB.

### Step 34: Execution strategy with transaction

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Persistence/Repositories/TollRulesRepository.cs

**📍 LINE:** 168-181

**🗣️ SAY:** "Execution strategy retries the entire callback on transient errors, and the transaction must be inside the callback so retry does not reuse a dead transaction."
>
> 📝 **CODE NOTE:** [TollRulesRepository.cs:162] — ADR-22: SQL Server retry with execution strategy -- retries transient errors automatically. Trade-off: retries add latency on transient failures; acceptable for correctness.

> 💬 **Q:** "Why must the transaction be inside the ExecuteAsync callback?"
>
> ✅ **A:** If the transaction were outside, a transient error would roll it back, but the retry would reuse the dead/rolled-back transaction object; inside the callback, each retry creates a fresh transaction.

> 💬 **Q:** "What kind of errors does EnableRetryOnFailure handle?"
>
> ✅ **A:** Transient SQL Server errors like network blips, deadlocks, and connection timeouts -- it retries with exponential backoff, not permanent errors like constraint violations.

> 💬 **Q:** "What if a transient error occurs after DELETE but before INSERT in the transaction?"
>
> ✅ **A:** The transaction rolls back (DELETE is undone), the execution strategy retries the entire callback from scratch with a fresh transaction -- no data is lost.

### Step 35: ExecuteDeleteAsync

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Persistence/Repositories/TollRulesRepository.cs

**📍 LINE:** 174-175

**🗣️ SAY:** "ExecuteDeleteAsync sends a single SQL DELETE WHERE with zero entities loaded -- constant memory versus load-then-remove."
> 💬 **Q:** "What is the alternative to ExecuteDeleteAsync?"
>
> ✅ **A:** Load all entities with `.ToList()`, call `RemoveRange()`, then `SaveChanges()` -- this SELECTs all rows into memory first and issues N individual DELETE statements, using O(N) memory vs O(1).

> 💬 **Q:** "Does ExecuteDeleteAsync work with the NoTracking default?"
>
> ✅ **A:** Yes, it bypasses the change tracker entirely -- it translates directly to a SQL DELETE statement without loading any entities, so tracking behavior is irrelevant.

>
> 📝 **CODE NOTE:** [TollRulesRepository.cs:86] — ADR-26: Multi-year queries delegate to cached single-year methods instead of direct DB query. Trade-off: sequential cache lookups per year; negligible for 1-2 years.
>
> 📝 **CODE NOTE:** [TollRulesRepository.cs:131] — ADR-8: Replace-as-a-whole writes -- delete + reinsert fee/toll-free rows atomically per year. Trade-off: higher write cost than diffing, but much lower complexity.
>
> 📝 **CODE NOTE:** [TollRulesRepository.cs:135] — INTERVIEW: "Why replace-as-a-whole instead of differential update?" -- "Validation needs the complete set (e.g. overlap detection). Differential still requires loading full config. Replace is simpler (DELETE all + INSERT all) and avoids subtle merge bugs."
>
> 📝 **CODE NOTE:** [TollRulesRepository.cs:219] — INTERVIEW: "Why the cast to IEnumerable<int> before .Contains()?" -- "int[].Contains() resolves to Array.Contains() which EF Core can't translate. Cast to IEnumerable<int> forces Enumerable.Contains<T>() which EF Core translates to SQL WHERE Year IN (...)."
>
> 📝 **CODE NOTE:** [TollRulesRepository.cs:245] — NOTE: static keyword on the lambda prevents capturing `this` or any local variables, avoiding a closure allocation.

> 🔗 **SEE ALSO:** [Part 7 — EF Core Patterns](#ef-core-patterns) for the full pattern/where/why table.

---

## Part 4: Code Walkthrough -- Configuration

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

### Year-Scoped Configuration

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**Original:** Fee bands were hardcoded in `TollFeeService.GetFee` as if-else conditions -- not configurable, not year-aware. Toll-free dates were a static `DateTime[]` in `TollFreeService.OtherFreeDays` -- 13 entries for 2021, hardcoded, missing Swedish holidays (only 13 vs the correct 16 for day-before-holiday pattern), wrong year. The DB entities (`Fee`, `TollFree`) and `TollDBContext` existed (scaffold-generated from a database) but were **never used** -- no code read from or wrote to the database. The controller called static services that ignored the DB entirely.

**Now -- runtime API:**

`YearConfigurationController` (`Controllers/YearConfigurationController.cs:11`) at `configuration/years/{year:int}`:
- GET (`:21`) -- full config or 404
- PUT (`:40`) -- full upsert, 204
- POST/PUT/DELETE for fee-bands (`:135`, `:154`, `:176`, `:195`) and toll-free-dates (`:63`, `:82`, `:101`, `:119`)

All mutations funnel through `YearConfigurationService` (`Application/Configuration/Services/YearConfigurationService.cs:8`):

1. Load existing from cache. Missing year -> `EntityNotFoundException` -> 404.
2. Apply mutation via `Func<IReadOnlyCollection<T>, (bool Updated, IReadOnlyCollection<T>)>` delegate (`TryUpdateTollFreeDatesAsync` `:170`, `TryUpdateFeeBandsAsync` `:191`). Example: `RemoveTollFreeDate` (`:95`) returns `(updatedDates.Length != existing.Count, updatedDates)`.
3. If `Updated == false` -> 404.
4. `UpsertYearConfigurationAsync` (`:30`) -- dedup + sort, validate, persist.

Validation: `YearRuleConfigurationValidator.Validate()` (`YearRuleConfigurationValidator.cs:11`) -- year 1-9999, minutes 0-1439, no negative amounts, no overlapping bands (`.Zip(Skip(1))`), dates must belong to target year. Static, called from upsert + every mutation + seed.

Seed: `YearRulesSeedService` (`YearRulesSeedService.cs:16`) -- loads seed JSON, inserts only missing years, validates through same validator. Idempotent. Missing file -> skip. Invalid data -> warning, app starts.

2026 holidays (`yearly-rules.seed.json`): 16 dates verified against Transportstyrelsen. Weekend + July hardcoded in `IsTollFreeDate` (`TollService.cs:84`) -- universal rules, not year-specific.

| | |
|---|---|
| **Why year-scoped** | Original had no way to change rules without code. Different tariffs per year, no redeployment. |
| **Why single mutation path** | One validation path for all endpoints. Impossible to bypass. |
| **Why seed** | Bootstraps fresh environments without manual API calls. Idempotent -- won't overwrite runtime changes. |
| **Trade-off: writes** | Replace-as-a-whole = higher write cost, simpler validation. Config changes rare. |
| **Trade-off: concurrency** | Read-modify-write race. Admin-only, low concurrency. Fix: row version. Documented. |

| Decision | Why | Alternative | Trade-off |
|---|---|---|---|
| Year-scoped rules managed via runtime API | Enables runtime changes without redeploy; yearly behavior explicit and auditable | Hardcoded rules; external holiday/provider integration | Operational ownership shifts to configuration management discipline |
| JSON startup seed, idempotent by missing year | Fast bootstrap for fresh environments; no overwrite risk for curated years | Manual API calls to populate; migration-based seed | Seed file is initialization source, not ongoing truth after runtime updates |
| Replace-as-a-whole writes + transaction | Atomicity for yearly config; avoids partial state on failure | Differential patching | Higher write cost; much lower complexity and easier consistency guarantees |
| `Func` delegate mutation pattern | 8 mutations share one read-modify-write flow; eliminates duplication | Separate method per mutation | Slightly more abstract; one pattern to understand |

**Flow: Year Configuration Management**

Source: `YearConfigurationController.cs:40`, `YearConfigurationService.cs:30`, `TollRulesRepository.cs:97`

```
GET /configuration/years/{year}
|
+-- year in configured set?
    +-- [NO]  --> Return 404
    +-- [YES] --> Return 200 + { year, feeBands[], tollFreeDates[] }
PUT /configuration/years/{year}  (full upsert)
|
+-- Validate(year, feeBands, tollFreeDates)
|   (see [Validation Rules](#flow-validation-rules) below)
|   |
|   +-- [INVALID] --> InvalidTollRequestException --> 400
|
+-- [VALID]
    |
    +-- Begin transaction
    |   +-- ExecuteDelete existing Fees for year
    |   +-- ExecuteDelete existing TollFrees for year
    |   +-- AddRange new Fees
    |   +-- AddRange new TollFrees
    |   +-- SaveChanges
    +-- Commit transaction
    |
    +-- Invalidate cache:
    |   +-- tollrules:configured-years
    |   +-- tollrules:fees:{year}
    |   +-- tollrules:tollfree:{year}
    |
    +-- Return 204
POST/PUT/DELETE mutation endpoints (fee bands, toll-free dates)
|
+-- year configured?
|   |
|   +-- [NO] --> EntityNotFoundException --> 404
|
+-- [YES]
    |
    +-- target entity exists? (for update/remove operations)
    |   |
    |   +-- [NO] --> EntityNotFoundException --> 404
    |
    +-- [YES]
        |
        +-- Apply mutation lambda (add/replace/remove in collection)
        |
        +-- Re-run full Validate(year, updatedBands, updatedDates)
        |   +-- [INVALID] --> InvalidTollRequestException --> 400
        |
        +-- [VALID]
            |
            +-- UpsertYearConfiguration (same transactional path as PUT)
            +-- Return 204
```

Important behavior:
- All mutation endpoints eventually route through `UpsertYearConfiguration(...)`.
- This guarantees one validation path and one cache invalidation path for writes.
- Missing year or missing target entity produces `EntityNotFoundException` -> HTTP 404.

**Flow: Validation Rules**

Source: `YearRuleConfigurationValidator.cs:11`

```
Validate(year, feeBands, tollFreeDates)
|
+-- year < 1 or year > 9999?
|   +-- [YES] --> InvalidTollRequestException
|
+-- For each fee band:
|   +-- fromMinute < 0 or toMinute > 1439 or fromMinute > toMinute?
|       +-- [YES] --> InvalidTollRequestException
|
+-- For each fee band:
|   +-- amount < 0?
|       +-- [YES] --> InvalidTollRequestException
|
+-- Sort bands by fromMinute, check adjacent pairs:
|   +-- right.fromMinute <= left.toMinute?  (overlap)
|       +-- [YES] --> InvalidTollRequestException
|
+-- For each toll-free date:
|   +-- date.Year != year?
|       +-- [YES] --> InvalidTollRequestException
|
+-- All checks passed --> OK
```

Validation outcomes:
- Any failed rule throws `InvalidTollRequestException` (maps to 400).
- Successful validation allows repository write execution.

**Flow: Startup Seed**

Source: `Program.cs:123`, `YearRulesSeedService.cs:16`

```
Application startup
|
+-- Seed JSON file exists?
|   |
|   +-- [NO] --> Skip seeding (log warning if exception)
|
+-- [YES]
    |
    +-- Deserialize yearly-rules.seed.json
    |
    +-- Load configured years from DB
    |
    +-- Filter seed years: keep only those NOT already in DB
    |
    +-- Any missing years?
    |   |
    |   +-- [NO] --> Done (idempotent, no writes)
    |
    +-- [YES]
        |
        +-- For each missing year:
        |   +-- Map seed data to FeeBand[] and DateTime[]
        |   +-- Validate(year, feeBands, tollFreeDates)
        |   +-- UpsertYearConfiguration(year, feeBands, tollFreeDates)
        |
        +-- Done
```

Seed characteristics:
- Idempotent: existing years are not overwritten.
- Validation is reused, so invalid seed data fails consistently with runtime rules.
- Seed file path defaults to `Application/Configuration/yearly-rules.seed.json`.

### Code Walkthrough Steps: Configuration Management

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

### Step 36: Year configuration REST endpoints

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Controllers/YearConfigurationController.cs

**📍 LINE:** 13

**🗣️ SAY:** "Year-scoped route at /configuration/years/{year} with full CRUD: GET, PUT for full replacement, POST for granular adds, DELETE for removals."
>
> 📝 **CODE NOTE:** [YearConfigurationController.cs:9] — ADR-6: Year-scoped configuration managed via dedicated endpoints (full-year upsert + granular CRUD). Alternatives: hardcoded rules, external holiday-provider as runtime dependency.

> 💬 **Q:** "Why year-scoped routes instead of a flat /configuration endpoint?"
>
> ✅ **A:** Year-scoping makes the resource hierarchy explicit in the URL, enables per-year cache invalidation, and prevents accidentally mixing fee bands from different years in one request.

> 💬 **Q:** "Why did you choose PUT for full replacement and POST for granular adds?"
>
> ✅ **A:** PUT is idempotent (same request = same result) which matches full-replacement semantics; POST is for creating sub-resources (adding a single fee band or date) where each call adds something new.

> 💬 **Q:** "Why Swashbuckle over NSwag for Swagger generation?"
>
> ✅ **A:** Swashbuckle has richer filter support (SchemaFilter, OperationFilter, DocumentFilter) for custom examples and tag descriptions; NSwag is better for client code generation, but Swashbuckle was simpler for our documentation needs.

> 💬 **Q:** "What happens if someone sends a PUT to a year that doesn't exist yet?"
>
> ✅ **A:** UpsertYearConfiguration creates the year -- it is an upsert (DELETE WHERE Year + INSERT), so the year is implicitly created by inserting new rows, and the cache is invalidated to reflect the new configuration.

### Step 37: 204 No Content pattern

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Controllers/YearConfigurationController.cs

**📍 LINE:** 66

**🗣️ SAY:** "All mutation endpoints return 204 No Content consistently -- the client already knows the data it sent."
> 💬 **Q:** "Why 204 instead of 200 with the updated resource?"
>
> ✅ **A:** The client already has the data it sent; echoing it back wastes bandwidth -- 204 with an empty body is the standard signal for "mutation succeeded, nothing to return."

> 💬 **Q:** "When would you prefer returning 200 with the resource?"
>
> ✅ **A:** When the server modifies the resource beyond what the client sent (e.g., server-generated IDs, computed fields, or timestamps) so the client has the canonical version.

### Step 38: Func delegate pattern in service

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Configuration/Services/YearConfigurationService.cs

**📍 LINE:** 181-185

**🗣️ SAY:** "Eight mutation endpoints share one 7-step flow through the Func delegate pattern -- only the mutation lambda differs, eliminating 15 lines of duplication per endpoint."
>
> 📝 **CODE NOTE:** [YearConfigurationService.cs:48] — NOTE: DistinctBy removes duplicate fee bands based on the tuple of all three fields. Alternative: .Distinct() uses record equality, but DistinctBy makes the key explicit.
>
> 📝 **CODE NOTE:** [YearConfigurationService.cs:67] — NOTE: Append creates a new sequence with the item added at the end without modifying the original collection. Alternative: list.Add() -- but Append works on IEnumerable (immutable operation).
>
> 📝 **CODE NOTE:** [YearConfigurationService.cs:81] — NOTE: Concat merges two sequences into one without modifying either. Alternative: AddRange on a List -- but Concat works on IEnumerable, keeping the pipeline functional.

> 💬 **Q:** "What is the Func delegate pattern here?"
>
> ✅ **A:** Each mutation endpoint passes a lambda (Func) that takes existing data and returns a (Updated bool, new data) tuple; the shared helper handles loading, year-check, 404 signaling, validation, and persistence.

> 💬 **Q:** "What's the alternative to this pattern?"
>
> ✅ **A:** Each endpoint could implement the full load-check-mutate-validate-persist flow inline, but that would duplicate approximately 15 lines per endpoint across 8 endpoints -- roughly 120 lines of near-identical boilerplate.

> 💬 **Q:** "What if the validator rejects the mutation -- does the DB change?"
>
> ✅ **A:** No, validation runs before persistence in the shared helper flow -- if the validator throws InvalidTollRequestException, the repository's UpsertYearConfiguration is never called.

> 💬 **Q:** "Why IReadOnlyCollection and not just IEnumerable?"
>
> ✅ **A:** Need .Count property for the empty check. IEnumerable only gives GetEnumerator — no Count without enumerating the entire sequence.

### Step 39: TryUpdateTollFreeDatesAsync

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Configuration/Services/YearConfigurationService.cs

**📍 LINE:** 187-206

**🗣️ SAY:** "The shared helper loads config, applies the mutation Func, checks the Updated bool for 404 signaling, validates, and persists."
> 💬 **Q:** "What does the `Updated` bool in the tuple signal?"
>
> ✅ **A:** The lambda reports whether the mutation found its target (e.g., RemoveTollFreeDate compares array lengths); if false, the helper throws EntityNotFoundException which the middleware maps to 404.

> 💬 **Q:** "Is there a race condition if two admins update the same year simultaneously?"
>
> ✅ **A:** Yes, the last write wins because UpsertYearConfiguration does a full replace; for this use case it is acceptable since admin writes are rare and the full config is always valid as a whole.

> ⚠️ **IMPROVE:** Add optimistic concurrency via a RowVersion column on the year aggregate to prevent silent data loss on concurrent config writes.

### Step 40: FeeBandClockFormat conversion

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Application/Configuration/Mappers/FeeBandClockFormat.cs

**📍 LINE:** 22-40

**🗣️ SAY:** "Parses HHmm strings like 0630 into minute-of-day integers for constant-time comparison in the rule engine, with validation on format and range."
>
> 📝 **CODE NOTE:** [FeeBandClockFormat.cs:12] — NOTE: static class -- pure formatting/parsing with no state. Centralized HHmm <-> minuteOfDay conversion used by both request and response mapping.
>
> 📝 **CODE NOTE:** [FeeBandClockFormat.cs:32] — ALTERNATIVE: if (hours < 0 || hours > 23 || ...) -- not used because pattern matching reads like English and avoids logic-inversion bugs with compound boolean expressions.

> 💬 **Q:** "Why HHmm strings in the API instead of TimeSpan or integers?"
>
> ✅ **A:** HHmm is human-readable in JSON and unambiguous (no negative values, no days); internally it converts to minute-of-day integers for efficient comparison, keeping the API friendly and the engine fast.

> 💬 **Q:** "Why is this class `internal` instead of `public`?"
>
> ✅ **A:** It is an implementation detail (HHmm-to-minutes conversion); making it public would add it to the API surface and create a backward-compatibility burden -- internal lets us refactor or delete it freely.

> 💬 **Q:** "What if someone sends '2500' as a fromTime?"
>
> ✅ **A:** The minute-of-day conversion produces 25*60+0=1500, which exceeds 1439 (23:59); the validator catches this with the `b.ToMinute > 1439` check and throws InvalidTollRequestException (400).

---

## Part 5: Code Walkthrough -- Error Handling

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

### Error Handling

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**Original:** No exception handling. No error responses. `Startup.cs` used `UseDeveloperExceptionPage()` in dev but no production error handling. An unconfigured year or any exception -> unhandled 500 with stack trace.

**Now:**

Centralized middleware (`ExceptionHandling/ExceptionHandlingExtensions.cs:11`):
- `YearNotConfiguredException` -> 400
- `InvalidTollRequestException` -> 400
- `EntityNotFoundException` -> 404
- Anything else -> 500, sanitized ("An unexpected error occurred.")
- All ProblemDetails ([RFC 9457](#rfc-9457-problemdetails) — the HTTP standard for structured error responses)

Source-generated logging (`ExceptionHandlingExtensions.Log.cs:3`): 5 `[LoggerMessage]` methods, stable EventIds, zero allocation, compile-time validated.

Serilog (`Program.cs:22-37`): Console + File (warnings+, rolling daily, 14-day retention). `InvariantCulture`. `try/finally` with `Log.CloseAndFlush()`.

Fault injection (`Controllers/TestOnlyController.cs:16`): `POST /_test/fault/throw` (`:27`). Four gates: environment (`:37`), config flag, token header, `FixedTimeEquals` (`:44`). Any fail -> stealth 404. `[ApiExplorerSettings(IgnoreApi = true)]`. Blackbox test verifies sanitized 500.

Middleware ordering (`Program.cs:91-93`): exception handler first -> authorization -> controllers.

| | |
|---|---|
| **Why** | One middleware, one mapping, all endpoints consistent. Original leaked stack traces. |
| **Trade-off** | Exceptions vs Result<T> -- three HTTP-code cases. Result adds ceremony without benefit at this scale. |

| Decision | Why | Alternative | Trade-off |
|---|---|---|---|
| Centralized exception handling (ProblemDetails) | Eliminates repeated controller branching; standardizes 400/404/500; keeps controllers thin | Per-controller `try/catch`; Result-object pattern | Exception-based flow needs careful scoping; avoid generic catch in application services |
| Fault injection endpoint for blackbox testing | Need to trigger unhandled exception path to verify 500 ProblemDetails shape and no detail leak | No fault endpoint; mock exceptions | Test-only code in production binary; mitigated by multi-layer gating and stealth 404 |
| Source-generated logging (`[LoggerMessage]`) | Zero-allocation at runtime; compile-time validated templates; consistent EventIds for filtering | String interpolation logging | Requires partial class split, adding one file |
| Structured logging with Serilog dual sinks | Console for container/dev; file for persistent warning/error history | Built-in logging only | File sink is local; production should add centralized sink (Seq, App Insights) |
| Startup safety: `EnsureCreated` + seed with warning on failure | Improves local/dev resilience and container bootstrap ergonomics | Crash on DB unavailability | Runtime may start in degraded state; visible through request failures and logs |

**Flow: Exception-to-HTTP Mapping**

Source: `ExceptionHandlingExtensions.cs:11`, `ExceptionHandlingExtensions.Log.cs:3`

```
Exception thrown at any layer
|
+-- YearNotConfiguredException?
|   +-- [YES] --> 400  Title: "Year is not configured"
|                       Detail: domain message (e.g. "...missing for: 2030.")
|
+-- InvalidTollRequestException?
|   +-- [YES] --> 400  Title: "Invalid toll calculation request"
|                       Detail: domain message
|
+-- EntityNotFoundException?
|   +-- [YES] --> 404  Title: "Resource not found"
|                       Detail: domain message
|
+-- Any other exception?
    +-- [YES] --> 500  Title: "Unexpected server error"
                       Detail: "An unexpected error occurred."  (sanitized)
```

Additional notes:
- Model binding errors (for malformed query/body input) can return framework-generated `400` before controller logic executes.
- All error responses use `ProblemDetails` ([RFC 9457](#rfc-9457-problemdetails)) format.
- Source-generated logging via `[LoggerMessage]` emits structured events with stable EventIds for each exception type.

**Flow: Fault Injection Endpoint**

Source: `TestOnlyController.cs:27`, `:37`, `:44`

```
POST /_test/fault/throw
|
+-- IsFaultInjectionEnabled()?
|   |
|   +-- Environment is Development or Integration?
|   |   +-- [NO] --> return 404 (stealth)
|   |
|   +-- Config "TestOnly:EnableFaultInjection" == true?
|       +-- [NO] --> return 404 (stealth)
|
+-- HasValidToken()?
|   |
|   +-- Config "TestOnly:FaultInjectionToken" set and non-empty?
|   |   +-- [NO] --> return 404 (stealth)
|   |
|   +-- Request header "X-Test-Token" present?
|   |   +-- [NO] --> return 404 (stealth)
|   |
|   +-- FixedTimeEquals(configured token, provided token)?
|       +-- [NO] --> return 404 (stealth)
|
+-- All gates passed:
    +-- throw InvalidOperationException("Test-only fault injection.")
    +-- Exception middleware catches it (see [Exception-to-HTTP Mapping](#flow-exception-to-http-mapping) above)
    +-- Returns 500 ProblemDetails with sanitized message
```

Security measures:
- Returns `404` (not `403`) when disabled or token invalid -- indistinguishable from missing route.
- `CryptographicOperations.FixedTimeEquals` prevents timing-based token extraction.
- Hidden from Swagger via `[ApiExplorerSettings(IgnoreApi = true)]`.
- Purpose: allows blackbox tests to verify the `500` error contract without risking production exposure.

### Code Walkthrough Steps: Error Handling

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

### Step 41: Exception middleware switch

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/ExceptionHandling/ExceptionHandlingExtensions.cs

**📍 LINE:** 48-74

**🗣️ SAY:** "Switch dispatches on exception type: YearNotConfigured and InvalidTollRequest map to 400, EntityNotFound maps to 404, and everything else becomes a sanitized 500."
>
> 📝 **CODE NOTE:** [ExceptionHandlingExtensions.cs:7] — ADR-2: Centralized exception handling -- one global middleware maps domain exceptions to ProblemDetails. Alternatives: per-controller try/catch, Result-object pattern.
>
> 📝 **CODE NOTE:** [ExceptionHandlingExtensions.cs:11] — ADR-3: Placed in ExceptionHandling (API boundary), not Application, because it depends on ASP.NET pipeline primitives. Trade-off: slightly more folder complexity; much cleaner separation.
>
> 📝 **CODE NOTE:** [ExceptionHandlingExtensions.cs:14] — NOTE: Static extension method integrates into ASP.NET pipeline via app.UseTollFeeExceptionHandler(). Centralizes exception-to-ProblemDetails mapping in one place.

> 💬 **Q:** "Why use exceptions for error flow instead of a Result<T> pattern?"
>
> ✅ **A:** These are exceptional cases (misconfiguration, invalid input), not expected business outcomes; exceptions short-circuit the call stack without requiring unwrap logic at every layer.

> 💬 **Q:** "Why three separate exception types instead of one with an error code enum?"
>
> ✅ **A:** Each type maps to a different HTTP status and ProblemDetails title, enables type-safe `Assert.ThrowsAsync<T>()` in tests, and produces distinct Serilog EventIds for filterable alerting.

> 💬 **Q:** "What happens if someone throws an ArgumentException (not one of the three domain types)?"
>
> ✅ **A:** It falls through the switch, hits the catch-all `if (exception is not null)` branch, gets logged as an unhandled exception, and returns a 500 with the sanitized "An unexpected error occurred" message.

> 💬 **Q:** "What if exception is null in the exception handler?"
>
> ✅ **A:** The `else` branch logs a warning via `UnhandledNoExceptionFeature` (indicating the exception handler feature had no error object), and still returns a 500 with the generic message.

### Step 42: ProblemDetails format

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/ExceptionHandling/ExceptionHandlingExtensions.cs

**📍 LINE:** 113-119

**🗣️ SAY:** "All errors use [RFC 9457](#rfc-9457-problemdetails) ProblemDetails with application/problem+json content type so clients can programmatically distinguish errors from normal responses."
>
> 📝 **CODE NOTE:** [ExceptionHandlingExtensions.cs:98] — ALTERNATIVE: plain string response -- not used because ProblemDetails is a machine-readable error format ([RFC 9457](#rfc-9457-problemdetails)) that clients can parse programmatically.

> 💬 **Q:** "What is RFC 9457 and why use it?" ([see full explanation](#rfc-9457-problemdetails))
>
> ✅ **A:** It is the standard for machine-readable HTTP error responses with structured fields (title, detail, status); clients can programmatically parse errors instead of guessing from status codes alone. It supersedes RFC 7807, defines the `application/problem+json` content type, and is natively supported by ASP.NET Core's `ProblemDetails` class.

> 💬 **Q:** "Why `application/problem+json` instead of just `application/json`?"
>
> ✅ **A:** The distinct content type lets clients auto-detect error responses by MIME type without inspecting the body; `application/json` would be ambiguous between normal data and errors.

> 💬 **Q:** "Why Swagger only in Development environment?"
>
> ✅ **A:** The `app.Environment.IsDevelopment()` guard on line 116 of Program.cs prevents exposing the full API schema in production, reducing the attack surface; in staging you could add a similar check with authentication.

> 💬 **Q:** "Why ProblemDetails and not just return a plain error string?"
>
> ✅ **A:** ProblemDetails is machine-readable ([RFC 9457](#rfc-9457-problemdetails)) with structured fields (title, detail, status). Clients can parse programmatically instead of regex-matching error strings.

### Step 43: Sanitized 500

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/ExceptionHandling/ExceptionHandlingExtensions.cs

**📍 LINE:** 87-91

**🗣️ SAY:** "Unhandled exceptions return a generic message -- the real error is logged server-side but never leaked to the client."
> 💬 **Q:** "Why not return the exception message to help API consumers debug?"
>
> ✅ **A:** Exception messages can contain stack traces, connection strings, or internal class names that reveal attack surface; the real error is logged server-side where developers can access it safely.

> 💬 **Q:** "What does `is not null` do differently from `!= null`?"
>
> ✅ **A:** `is not null` is a pattern-matching null check that cannot be overloaded; `!= null` calls the type's `operator ==` which could be overridden to give unexpected results.

> 💬 **Q:** "What if the exception occurs during response writing (e.g., after headers are sent)?"
>
> ✅ **A:** The exception handler checks `context.Response.HasStarted` implicitly via ASP.NET's pipeline -- if headers are already sent, the response cannot be modified and the connection is aborted.

>
> 📝 **CODE NOTE:** [ExceptionHandlingExtensions.Log.cs:3] — ADR-19: Source-generated logging via [LoggerMessage] -- zero-allocation, compile-time validated templates. Trade-off: requires partial class split.
>
> 📝 **CODE NOTE:** [ExceptionHandlingExtensions.Log.cs:6] — WHY: partial class + [LoggerMessage]: source-generated logging avoids all allocation when log level is disabled. ALTERNATIVE: ILogger.LogWarning() allocates a string on every call even when disabled.
>
> 📝 **CODE NOTE:** [ExceptionHandlingExtensions.Log.cs:12] — NOTE: Separate file (*.Log.cs) keeps log method definitions cleanly separated from handler logic.

> 🔗 **SEE ALSO:** [Part 7 — Logging](#logging) for the full pattern/where/why table.

### Step 44: Fault injection endpoint

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Controllers/TestOnlyController.cs

**📍 LINE:** 36-42

**🗣️ SAY:** "Test-only endpoint gated by environment plus config flag plus X-Test-Token -- returns 404 when disabled so the surface is indistinguishable from a missing route."
>
> 📝 **CODE NOTE:** [TestOnlyController.cs:7] — ADR-18: Fault injection endpoint for blackbox testing of the 500 ProblemDetails error contract. Gated by environment + config flag + X-Test-Token with constant-time comparison.

> 💬 **Q:** "Why return 404 instead of 403 when disabled?"
>
> ✅ **A:** 403 reveals that the endpoint exists but access is denied; 404 makes it indistinguishable from a truly missing route, hiding the attack surface from unauthorized users.

> 💬 **Q:** "Why three layers of gating (environment + config + token)?"
>
> ✅ **A:** Defense in depth: even if one check is misconfigured, the other two prevent exposure; the environment check prevents production use, the config flag is an explicit opt-in, and the token prevents unauthorized access.

### Step 45: Constant-time token comparison

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api/Controllers/TestOnlyController.cs

**📍 LINE:** 67-69

**🗣️ SAY:** "FixedTimeEquals prevents timing side-channel attacks -- string equality would short-circuit on the first differing byte, letting attackers guess one character at a time."
> 💬 **Q:** "What is a timing side-channel attack?"
>
> ✅ **A:** String `==` short-circuits on the first differing byte, so a wrong token with the correct first character takes slightly longer to reject; an attacker can measure response times to guess the token one character at a time.

> 💬 **Q:** "What does CryptographicOperations.FixedTimeEquals guarantee?"
>
> ✅ **A:** It always compares every byte regardless of where they differ, taking constant time proportional to the input length; this prevents attackers from inferring any information from response timing.

> 💬 **Q:** "What if the fault injection token is not set in configuration?"
>
> ✅ **A:** The config flag check (`EnableFaultInjection`) fails first, so the endpoint returns 404 before ever checking the token -- the three layers of gating are evaluated in order.

> 🔗 **SEE ALSO:** [Part 7 — Security](#security) for the full pattern/where/why table.

---

## Part 6: Testing

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

### Testing

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**Original:** No test projects. No tests of any kind. Zero.

**Now -- 127 tests in two layers:**

**79 unit tests** (`TollFee.Api.Tests/`):
- `TestHelpers/TestFeeBands.cs` -- canonical 9-band set, one source of truth
- `TestHelpers/InMemoryRulesRepository.cs` -- 80-line stub, no mocking framework
- Factory methods: `CreateDefaultService(year, tollFreeDates?)`, `CreateService()` -> `(service, repository)`
- Coverage: 23 fee band boundaries, window semantics (same/new/60min/59min/duplicates/gap/single-band), daily cap, timezone (CET/CEST/spring-forward/fall-back/year-boundary), input validation, config CRUD, validator edge cases (negative/zero/empty/duplicate), seed idempotency
- `try/finally` temp dir cleanup in seed tests

**48 blackbox tests** (`TollFee.Api.BlackBoxTests/`):
- `BlackBoxTestFixture`: Testcontainers with SQL Server + API in Docker, `[Collection("blackbox-tests")]`
- `BlackBoxHelpers.BuildEndpoint()`, shared DTOs
- Coverage: HTTP contracts, ProblemDetails, config flows, cache invalidation, fault injection, performance (<4s), commuter scenarios (daily/weekly/monthly), January 2026 randomized edge cases
- Always enabled -- skip guard removed

**Why two layers:** Unit = logic in isolation. Blackbox = full stack (HTTP + EF Core + SQL Server + cache). Neither alone sufficient.

| Decision | Why | Alternative | Trade-off |
|---|---|---|---|
| Two-layer testing (unit + blackbox) | Unit = fast logic feedback; blackbox = real integration contract and behavior | Unit only; integration only | Blackbox requires Docker; acceptable since separate project filterable with `--filter` |
| Stubs over mocks | Tests behavior, not call patterns; 80-line real implementation | Mocking framework | One class to update on interface change |
| Blackbox tests always enabled (skip guard removed) | Tests were passing silently without running when guard was hit | Keep `Enabled` flag | Every test run requires Docker; fails loudly if unavailable |
| Records for all DTOs and models | Immutable data carriers; free structural equality, `ToString()`, `with` expressions; no serialization impact | Keep mutable classes | None |

### Code Walkthrough Steps: Testing

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

### Step 46: Test project overview

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**🗣️ SAY:** "We have 79 unit tests in TollFee.Api.Tests and 48 blackbox tests in TollFee.Api.BlackBoxTests that hit the running API over HTTP."
> 💬 **Q:** "Why both unit tests and blackbox tests?"
>
> ✅ **A:** Unit tests verify internal logic fast and in isolation (rule engine, service orchestration); blackbox tests verify the full HTTP contract (status codes, ProblemDetails shape, end-to-end scenarios) and catch integration issues unit tests miss.

> 💬 **Q:** "How would you run the blackbox tests in CI?"
>
> ✅ **A:** Start the API in a background process or Docker container, run the blackbox test suite against it, then tear it down; alternatively use WebApplicationFactory for in-process integration tests.

> 💬 **Q:** "Why xUnit over NUnit or MSTest?"
>
> ✅ **A:** xUnit is the most widely used test framework in the .NET Core ecosystem, has clean assertion syntax, and supports `[Collection]` attributes for shared test fixtures like the Testcontainers-based BlackBoxTestFixture.

> 💬 **Q:** "What if Docker is not running when blackbox tests execute?"
>
> ✅ **A:** The Testcontainers MsSqlBuilder.StartAsync fails, the catch in BlackBoxTestFixture.InitializeAsync wraps it in InvalidOperationException with "Ensure Docker daemon is running" -- tests fail loudly with a clear message.

> 💬 **Q:** "Could you use SQLite instead of SQL Server containers for blackbox tests?"
>
> ✅ **A:** SQLite does not support SQL Server features like execution strategies, covering indexes, or decimal column types -- using real SQL Server via Testcontainers catches integration bugs that SQLite would miss.

> ⚠️ **IMPROVE:** Add at least one blackbox test sending timestamps with Z suffix to verify UTC timezone conversion through the full HTTP stack -- current blackbox tests strip UTC kind.

### Step 47: Unit test structure

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📁 POINT AT FOLDER:** TollFee.Api.Tests/Application/

**🗣️ SAY:** "Unit tests mirror the source structure: Calculation/ has CongestionRuleEngineTests and TollServiceTests, Configuration/ has YearConfigurationServiceTests and ValidatorTests."
> 💬 **Q:** "Why mirror the source structure in tests?"
>
> ✅ **A:** It makes it trivial to find the test for any given class, and makes missing test coverage immediately visible by comparing the two folder trees.

### Step 48: InMemoryRulesRepository

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api.Tests/TestHelpers/InMemoryRulesRepository.cs

**📍 LINE:** 9

**🗣️ SAY:** "Shared in-memory stub that implements ITollRulesRepository -- tracks configured years explicitly so tests match production cache behavior without a database."
> 💬 **Q:** "Why a hand-written stub instead of a mocking framework like Moq?"
>
> ✅ **A:** The repository has stateful behavior (configured years, cache-like lookups) that is easier to reason about in a purpose-built stub; mocking frameworks are better for simple one-off return values, not stateful test doubles.

> 💬 **Q:** "Why does the stub track configured years explicitly?"
>
> ✅ **A:** Production code calls `GetConfiguredYearsAsync` before loading fee bands; the stub must replicate this behavior or tests would pass without exercising the year-check guard, missing real bugs.

> 💬 **Q:** "Why not use WebApplicationFactory for integration tests instead of Testcontainers?"
>
> ✅ **A:** WebApplicationFactory runs in-process and is great for API-level integration tests, but the blackbox tests verify the full Docker deployment pipeline including container networking, environment variable injection, and startup behavior.

> 🔗 **SEE ALSO:** [Part 7 — Testing Patterns](#testing-patterns) for the full pattern/where/why table.

### Step 49: TestFeeBands

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📂 OPEN:** TollFee.Api.Tests/TestHelpers/TestFeeBands.cs

**📍 LINE:** 8

**🗣️ SAY:** "Canonical 2026 Gothenburg fee band set shared across all test files -- single source of truth for expected band values."
> 💬 **Q:** "Why share test data instead of defining it per test?"
>
> ✅ **A:** A single source of truth means updating fee bands for a regulation change requires editing one file, not hunting through dozens of tests; it also ensures all tests use identical, consistent data.

> 💬 **Q:** "What if you need a test with non-standard fee bands?"
>
> ✅ **A:** The test can create its own custom FeeBand array and pass it directly to the engine or stub; the shared set is a convenience default, not a constraint.

### Step 50: Blackbox test structure

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**📁 POINT AT FOLDER:** TollFee.Api.BlackBoxTests/Scenarios/

**🗣️ SAY:** "Blackbox tests are split into contract tests (response shapes, status codes, ProblemDetails) and real-life scenario tests (multi-day, weekends, July, daily cap)."
> 💬 **Q:** "What is a contract test vs a scenario test?"
>
> ✅ **A:** Contract tests verify the HTTP surface (correct status codes, ProblemDetails shape, content types); scenario tests verify business correctness (multi-day totals, weekend exemptions, daily cap application).

> 💬 **Q:** "How would you add a new toll-free rule (e.g., December 24)?"
>
> ✅ **A:** Add December 24 to the year's toll-free dates via the PUT /configuration/years/{year} endpoint or the POST toll-free-dates endpoint; no code change needed since it is data-driven.

> 💬 **Q:** "When would you move from Docker Compose to Kubernetes?"
>
> ✅ **A:** When you need auto-scaling, self-healing, rolling updates, or multi-node deployment -- Docker Compose is a single-host tool for dev/demo, Kubernetes handles production-grade orchestration.

> 💬 **Q:** "What does the [Collection("blackbox-tests")] attribute do in xUnit?"
>
> ✅ **A:** It groups test classes that share the BlackBoxTestFixture via ICollectionFixture, so xUnit creates the Testcontainers infrastructure once and reuses it across all blackbox test classes in the collection.

---

## Part 7: Technical Details

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

### Startup and Swagger

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**Original (`Startup.cs`):** `ConfigureServices` registered empty `ITollService` as Transient. `Configure` had routing + authorization + Swagger in dev only. No startup logic, no seeding, no database initialization.

**Now (`Program.cs`):**
1. Build host: Serilog (`:22`), DbContext (`:42`), DI (`:44-48`), Swagger (`:51-81`), controllers (`:50`)
2. Middleware (`:91-93`): exception handler -> authorization -> controllers
3. `InitializeDatabaseAsync` (`:108`) -- `EnsureCreatedAsync`, try-catch, warning on failure
4. `SeedConfiguredYearsAsync` (`:123`) -- seed service, try-catch, warning on failure
5. `app.RunAsync()` (`:99`)
6. `finally { Log.CloseAndFlush(); }` (`:101-104`)

Swagger (`:51-81`): detailed API description, custom tag grouping (`:69-73`), XML docs (`:76-78`), three filters:
- `TagDescriptionsDocumentFilter` (`Application/Swagger/TagDescriptionsDocumentFilter.cs`)
- `RequestExamplesOperationFilter` (`Application/Swagger/RequestExamplesOperationFilter.cs`)
- `YearConfigurationExamplesSchemaFilter` (`Application/Swagger/YearConfigurationExamplesSchemaFilter.cs`)

`[UsedImplicitly]` on filter classes -- suppresses warnings since only referenced via config.

| Decision | Why | Alternative | Trade-off |
|---|---|---|---|
| API documentation via Swagger + XML docs + filters | Self-serve API documentation center; shortens onboarding/debug loops | No Swagger; built-in OpenAPI | Documentation must be maintained as contracts evolve; Swashbuckle has richer filter support than built-in OpenAPI (still maturing) |

### C# Language Features

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

| Pattern | Where | Why |
|---|---|---|
| Primary constructors | `TollService.cs:7` | Eliminates field+constructor+null-check boilerplate. Dependency explicit in class declaration. |
| `readonly record struct` | `FeeBand.cs:8` | 12 bytes stack-allocated, no GC. `readonly` prevents defensive copies. `record` gives free structural equality for dedup. Original: mutable `partial class` with `long` fields. |
| `sealed record` | All DTOs/models | Immutable data carriers. Free `ToString()`, equality, `with` expression. Original: mutable `{ get; set; }`. |
| `sealed class` | All entities/services/controllers | JIT devirtualization. Communicates "not an extension point." Original: unsealed partial classes. |
| `DateOnly` | `TollFree.cs:10` | Semantically a date, not a datetime. Eliminates time-component equality bugs. Original: `DateTime` (no `DateOnly` in .NET 5). |
| Collection expressions | Everywhere | `[]` -- shorter, compiler-optimized. Replaces `Array.Empty<T>()`. |
| Pattern matching | `TollService.cs:86` | `is Saturday or Sunday` reads like English. Original: negated `!=` chain -- logic inversion risk. |
| File-scoped namespaces | Everywhere | One less indentation level. Modern C# convention. |
| Source-generated `[LoggerMessage]` | `ExceptionHandlingExtensions.Log.cs:3` | Zero allocation (no interpolation/boxing). Compile-time validated templates. Stable EventIds for filtering. |

### EF Core Patterns

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

| Pattern | Where | Why |
|---|---|---|
| Global NoTracking | `TollDbContext.cs:13` | Read-heavy workload -- tracking unused entities wastes memory. `AddRange` still works (sets state to `Added` explicitly). |
| Surrogate PK | `TollDbContext.cs:23-24` | Original composite key included `Price` -- changing amount created new row. Surrogate `Id` gives stable identity. |
| Covering index | `TollDbContext.cs:27-28` | `(Year, FromMinute, ToMinute)` + included `Price` -- query satisfied from index alone, no table lookup. |
| `ExecuteDeleteAsync` | `TollRulesRepository.cs:127` | Single SQL `DELETE WHERE`. No entity loading into memory. O(1) memory. |
| Execution strategy + transaction inside | `TollRulesRepository.cs:123-132` | Retries entire callback on transient errors. Transaction outside = retry reuses dead transaction = crash. |
| `IEnumerable<int>` cast | `TollRulesRepository.cs:165-166` | Forces EF Core to translate `.Contains()` on `int[]` to SQL `IN`. Documented workaround. |
| `checked` cast | `TollRulesRepository.cs:48` | `checked((int)x.Price)` -- fail-fast on overflow instead of silent truncation. Documents the assumption. |
| `EnsureCreatedAsync` | `Program.cs:114` | Creates tables if empty DB. Simpler than migrations for no-evolution project. Try-catch for degraded startup. |
| Connection string fail-fast | `Program.cs:39` | `?? throw`. Original hardcoded fallback -> silent wrong-DB connection. |

### Caching Patterns

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

| Pattern | Where | Why |
|---|---|---|
| `IMemoryCache` + 12h TTL | `TollRulesRepository.cs:14` | Config rarely changes. TTL = safety net. Explicit invalidation = immediate consistency on writes. |
| `FrozenSet<T>` | `TollRulesRepository.cs:33`, `:79` | Immutable after construction -- can't corrupt cache. Optimized internal layout for faster lookups than `HashSet`. |
| Cache key memoization | `TollRulesRepository.cs:18-19` | `ConcurrentDictionary` caches interpolated key strings. `static` lambda avoids closure allocation. |
| Multi-year delegation | `TollRulesRepository.cs:53-65` | Batch methods call cached single-year methods. Original bypassed cache. Zero DB on warm cache. |
| Explicit invalidation | `TollRulesRepository.cs:179-184` | 3 keys removed per write. Next read repopulates from DB. TTL-only = up to 12h stale. |

### Type Design

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

| Pattern | Where | Why |
|---|---|---|
| `IFeeBandShape` | `IFeeBandShape.cs:7` | Shared shape across struct + record class types. Abstract base won't work (struct can't inherit class). One mapping method for all sources. |
| `YearScopedEntity` abstract class | `YearScopedEntity.cs:6` | Entities share `Id` + `Year` with constructor logic. Interface can't provide implementation. Abstract = structural sharing. |
| Domain/entity separation | `FeeBand` vs `Fee` | Engine shouldn't depend on EF Core. `FeeBand` is minimal (3 ints). Repository handles projection. |
| `Func` delegate mutation | `YearConfigurationService.cs:170` | 8 mutations share one read-modify-write flow. Func returns `(bool Updated, collection)`. Eliminates duplication. |

### Security

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

| Pattern | Where | Why |
|---|---|---|
| `FixedTimeEquals` | `TestOnlyController.cs:57` | Constant-time comparison prevents timing-based token extraction. One line, eliminates a vulnerability class. |
| Stealth 404 | `TestOnlyController.cs:31` | 403 reveals endpoint exists. 404 = indistinguishable from missing route. |
| `[ApiExplorerSettings(IgnoreApi = true)]` | `TestOnlyController.cs:14` | Hidden from Swagger. Combined with `_test/` prefix = invisible. |
| Sanitized 500 | `ExceptionHandlingExtensions.cs:65-66` | Original leaked stack traces. Now: generic message to client, full detail logged server-side. |
| Fail-fast config | `Program.cs:39` | Original: hardcoded fallback -> silent wrong-DB. Now: throw at startup = catch during deployment. |

### Testing Patterns

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

| Pattern | Where | Why |
|---|---|---|
| Stubs over mocks | `TestHelpers/InMemoryRulesRepository.cs` | Tests behavior, not call patterns. 80-line real implementation. One class to update on interface change. |
| Shared test data | `TestHelpers/TestFeeBands.cs` | Single source of truth. Was duplicated in 3 files -- drift risk. |
| Factory methods | `TollServiceTests.CreateDefaultService()` | Reduces 4-8 line setup to 1 line. Test intent more visible. |
| `try/finally` cleanup | `YearRulesSeedServiceTests.cs` | Temp dir always deleted even if assertions fail. |
| `[Collection]` serialization | `BlackBoxTestFixture.cs` | 48 tests share one Docker fixture (~10s startup). Prevents parallel container conflicts. |
| Always-on blackbox | No skip guard | Original had `Enabled` flag -> silent green passes without running. Now: Docker required, fails loudly if unavailable. |

### Logging

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

| Pattern | Where | Why |
|---|---|---|
| Serilog dual sinks | `Program.cs:22-37` | Console for dev/container logs. File for persistent warnings/errors. |
| `InvariantCulture` | `Program.cs:24` | Locale-independent log formatting. Prevents `1234,56` on French servers breaking parsers. |
| Microsoft -> Warning | `Program.cs:27` | Suppresses per-request framework noise. Keeps `Hosting.Lifetime` at Info for startup/shutdown. |
| `Log.CloseAndFlush()` in finally | `Program.cs:103` | Serilog buffers writes. Crash without flush = lost crash message. Finally block guarantees flush. |

### RFC 9457: ProblemDetails

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

RFC 9457 (published March 2023, supersedes RFC 7807) defines a standard JSON format for HTTP API error responses. Instead of returning a plain string or an ad-hoc JSON object when something goes wrong, the API returns a structured object with well-known fields that any client can parse programmatically:

```json
{
  "type": "https://tools.ietf.org/html/rfc9457",
  "title": "Year is not configured",
  "detail": "No fee configuration found for year 2025.",
  "status": 400
}
```

**Why it matters:**
- **Machine-readable errors** — clients parse `status`, `title`, and `detail` fields instead of regex-matching error strings or guessing from HTTP status codes alone
- **Content type discrimination** — the response uses `application/problem+json` (not `application/json`), so clients can auto-detect "this is an error, not data" by checking the `Content-Type` header without inspecting the body
- **Extensible** — the spec allows custom fields (e.g., `traceId`, `errorCode`) alongside the standard ones, so teams can add domain-specific error metadata without breaking the standard contract
- **Framework support** — ASP.NET Core has built-in `ProblemDetails` class that serializes to the RFC format. The `[ApiController]` attribute auto-returns ProblemDetails for model validation errors. The exception middleware maps domain exceptions to ProblemDetails manually for full control over `title` and `detail`.

**Where used in this project:** The centralized exception middleware ([Step 41](#step-41-exception-middleware-switch)) maps 3 domain exception types to ProblemDetails: `YearNotConfiguredException` → 400, `InvalidTollRequestException` → 400, `EntityNotFoundException` → 404. Unhandled exceptions → sanitized 500 with generic detail (no stack trace leak). The `application/problem+json` content type is set explicitly in `WriteProblemDetailsAsync` ([Step 42](#step-42-problemdetails-format)).

**RFC 7807 vs 9457:** RFC 9457 is the updated version. The main changes: `type` field now defaults to `about:blank` instead of being required, and the spec clarifies that `type` should be a URI that resolves to documentation (not just an identifier). The ProblemDetails class in ASP.NET Core supports both versions — the JSON shape is identical.

---

## Improvement Points

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

See the expanded improvement points with implementation details, alternatives, and deferral reasoning in the [What I would improve next](#what-i-would-improve-next) section of the introduction.

---

## Known Risks and Mitigations

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

See the known risks table and KISS rationale in the [What I would improve next](#what-i-would-improve-next) section of the introduction.

---

## Q&A Reference

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

### Contract and compatibility

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**"Did you change the HTTP contract?"** -- No. Same route, query param, response shape (`TotalFee: int`, `AverageFeePerDay: float`). Response class was in `Models/TollFeeController.cs` (misnamed file) -- moved to `DataModels/Contracts/Responses/CalculateFeeResponse.cs`, upgraded from class to record.

**"What did you keep from the original?"** -- HTTP contract, Fee/TollFree column names, collation, `decimal(2,0)` for Price. Everything else was rewritten.

**"What about the average calculation?"** -- Original: `totalFee / request.Distinct().Count()` (distinct timestamps). Now: `totalFee / distinctDays.Count` (distinct calendar days including toll-free days).

### Calculation rules

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**"What's the window boundary rule?"** -- Strict less-than. Exactly 60 min apart -> new window. Original had no window rule at all -- charged every passage independently.

**"Why static for the engine?"** -- No dependencies, no state. Pure computation. Original was also static (`TollFeeService`) but mixed all concerns.

**"Why not use the Fee entity directly?"** -- Entity has DB concerns (`Id`, `decimal`, `Year`, `long` types). Engine needs none of that. Keeps engine independent of EF Core. Original used `Fee` entity shape indirectly through hardcoded if-else.

### Configuration and persistence

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**"Why replace-as-a-whole writes?"** -- Differential update needs partial-state validation. Replace validates the complete set. Config changes are rare. Original had no writes at all.

**"What about concurrent config writes?"** -- Read-modify-write race exists. Admin-only, low concurrency. Fix: row version. Documented.

**"Why EnsureCreated instead of Migrate?"** -- No migrations exist. Original had no startup DB logic at all.

**"Why not distributed cache?"** -- Single-instance. IMemoryCache sufficient. Original had no caching.

**"Why did you change the entity types?"** -- `long FromMinute/ToMinute` -> `int` (minutes-of-day max 1439, doesn't need 64 bits). `DateTime Date` -> `DateOnly` (available since .NET 6, semantically correct -- it's a date, not a datetime). `partial class` -> `sealed class` (no scaffold partial needed, sealing enables devirtualization).

### Error handling

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**"Why exceptions instead of Result<T>?"** -- Three cases mapping to HTTP codes. Original had no error handling at all.

**"Why 404 instead of 403 on fault endpoint?"** -- 403 reveals existence. 404 gives nothing. Original had no fault endpoint.

### Testing

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**"Why no mocking framework?"** -- Stub exercises real code. Mock verifies call patterns. Original had no tests.

**"How do you know blackbox tests run?"** -- Removed skip guard. Docker always starts. Verbose output proves it.

### EF Core internals

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**"If NoTracking is global, how does SaveChangesAsync insert?"** -- `NoTracking` only affects queried entities. `AddRange` explicitly sets state to `Added` -- always works regardless of the query tracking default.

**"How does EF Core set Id if it's get-only and constructor passes 0?"** -- EF Core uses constructor binding and backing field access. `ValueGeneratedOnAdd` tells the DB to generate it. EF reads it back after insert.

**"Two admins add a fee band at the same time?"** -- Last-write-wins, silent data loss. Fix: optimistic concurrency via row version on the year aggregate. Acceptable for admin-only, low-concurrency endpoints.

**"Why Swashbuckle instead of built-in OpenAPI in .NET 10?"** -- Swashbuckle has richer filter support (schema, operation, document filters) for examples and tag descriptions. Built-in OpenAPI is still maturing.

### Production readiness

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

**"What would you change for production?"** -- (1) EF Core migrations. (2) Widen `decimal(2,0)` to `decimal(5,0)`. (3) HTTP response caching. Original wasn't production-ready at all.

**"What if 10,000 req/s?"** -- Redis, response caching, precomputed 1440-slot lookup array.

**"What was the hardest part?"** -- The 60-minute window. Original didn't have it. Strict-less-than boundary matters. 5 boundary tests + manually traced all 48 blackbox scenarios.

**"How confident in correctness?"** -- Every blackbox expected value manually calculated. Every band boundary tested. 2026 holidays verified against Transportstyrelsen. Cross-check traced all 48 scenarios.

**"What if starting over?"** -- `DateTimeOffset` instead of `DateTime`. EF Core migrations from day one.

---

## Interview Talking Points

[go to top](#gothenburg-congestion-tax-calculator--code-presentation)

- "We preserved public API contracts and moved complexity behind stable boundaries."
- "We standardized failures with domain exceptions + global ProblemDetails mapping."
- "We normalized to Gothenburg local time before any business decision to prevent timezone bugs."
- "We chose DB-authoritative year rules with idempotent seed and runtime CRUD for operational flexibility."
- "We used cache with explicit invalidation on writes to keep hot-year reads fast and correct."
- "The hot calculation path hits zero DB round-trips on cache-warm requests by delegating multi-year lookups to cached single-year methods."
- "We kept write consistency with transactional replace-as-a-whole semantics."
- "We validated architecture through both fast unit tests and real black-box integration scenarios."
- "We centralized build configuration with Directory.Build.props and central package management to eliminate duplication across projects."
- "All DTOs and models are records -- immutable by design, with free structural equality and no serialization impact."
- "NoTracking is the global default because the workload is read-heavy and write paths use AddRange/ExecuteDeleteAsync which bypass change tracking."
- "Blackbox tests are always-on -- they spin up real Docker containers with SQL Server and verify the full HTTP contract on every run."

---

**End of walkthrough.** Total: ~15 minutes at normal pace.
