# Architecture and Technical Decisions

## Purpose

This document captures the architecture and technical decisions made during the Gothenburg congestion-tax implementation so they can be explained clearly in technical interviews and reviews.

It focuses on:

- the decision itself,
- why it was made,
- alternatives considered,
- trade-offs/risks,
- operational and testing impact.

## Scope and constraints

- Preserve the external calculation API contract (`TollFee` endpoint).
- Support year-based runtime configuration for fee bands and toll-free dates.
- Persist rules in database and return clear error for unconfigured years.
- Keep implementation KISS while still production-safe.
- Provide realistic test coverage (unit + black-box).

## Decision 1: Contract-first evolution

### Decision
Internal architecture changed while preserving `TollFee` endpoint surface.

### Why
Client compatibility and backward safety were higher priority than internal purity.

### Alternatives considered
- Change controller contract to return `ActionResult<T>` with in-controller error mapping.
- Keep controller signature stable and centralize mapping in middleware.

### Selected
Keep controller signature stable; move error-to-HTTP mapping to exception middleware.

### Trade-off
Requires consistent exception discipline in services.

## Decision 2: Centralized exception handling (ProblemDetails)

### Decision
Use one global middleware to map domain exceptions to consistent `ProblemDetails`.

### Why
- Eliminates repeated controller branching.
- Standardizes `400`/`404`/`500` responses.
- Keeps controllers thin and easier to reason about.

### Mapping
- `YearNotConfiguredException` -> `400`
- `InvalidTollRequestException` -> `400`
- `EntityNotFoundException` -> `404`
- Unexpected exception -> `500`

### Alternatives considered
- Per-controller `try/catch`.
- Result-object pattern (`bool success`, error code).

### Trade-off
Exception-based flow needs careful scoping; avoid generic catch in application services.

## Decision 3: Correct placement of exception middleware

### Decision
Place exception handling extension in API/web boundary (`ExceptionHandling`), not under application folder.

### Why
It depends on ASP.NET pipeline primitives and is not domain/application business logic.

### Trade-off
Slightly more folder complexity; much cleaner separation of concerns.

## Decision 4: Local-time normalization before rules

### Decision
Normalize all input timestamps to Gothenburg local time before validation, year resolution, daily grouping, and fee-band checks.

### Why
Congestion-tax rules are legally local-time based.

### Details
- `Utc` is converted to Gothenburg local time.
- `Local` is converted to Gothenburg local time.
- `Unspecified` is treated as already local input.
- Timezone resolution supports Linux and Windows IDs.

### Alternatives considered
- Keep everything in UTC.
- Convert only near fee lookup.

### Trade-off
Timezone logic must be explicit and tested around DST and year-boundary cases.

## Decision 5: Service orchestration vs rule-engine computation

### Decision
Split responsibilities:
- `TollService`: orchestration, validation, year/rules loading, grouping, averaging.
- `CongestionRuleEngine`: fee math (minute-band lookup, 60-minute window, daily cap).

### Why
Improves maintainability and targeted testability.

### Trade-off
Adds an extra abstraction, but keeps each class cognitively smaller.

## Decision 6: Year configuration model and management API

### Decision
Rules are year-scoped and managed via dedicated configuration endpoints (full-year upsert + granular CRUD).

### Why
- Enables runtime changes without redeploy.
- Keeps yearly behavior explicit and auditable.

### Alternatives considered
- Hardcoded rules.
- External holiday/provider integration as runtime dependency.

### Selected
DB-authoritative yearly configuration; seed once, then manage via API.

### Trade-off
Operational ownership shifts to configuration management discipline.

## Decision 7: JSON startup seed, idempotent by missing year

### Decision
Seed rules from `Application/Configuration/yearly-rules.seed.json` at startup, only for years not already in DB.

### Why
- Fast bootstrap for fresh environments.
- No overwrite risk for already curated/updated years.

### Behavior
- Missing file -> skip quietly.
- Existing year -> do not modify.
- New year in seed -> validate + insert.

### Trade-off
Seed file is an initialization source, not ongoing truth after runtime updates.

## Decision 8: Replace-as-a-whole writes + transaction

### Decision
For yearly upsert, replace fee/toll-free rows as a unit inside explicit DB transaction.

### Why
- Atomicity for a yearly config.
- Simple correctness model.
- Avoids partial state on failure.

### Implementation notes
- Set-based delete via `ExecuteDelete`.
- Reinsert normalized rows.
- Commit transaction.

### Trade-off
Higher write cost than differential patching, but much lower complexity and easier consistency guarantees.

## Decision 9: Caching strategy with explicit invalidation

### Decision
In-memory cache for:
- configured years,
- fee bands by year,
- toll-free dates by year,
with explicit invalidation on writes.

### Why
Read-heavy workloads repeatedly query the same hot year(s); caching avoids repetitive DB reads.

### Invalidation
On any year write, remove:
- configured-years key,
- fee key for target year,
- toll-free key for target year.

### Trade-off
Memory cache is process-local; multi-instance deployment would require distributed caching for strict cross-node immediacy.

## Decision 10: Data model centralization and shared abstractions

### Decision
Consolidate data-carrying types under `DataModels` with grouped folders and reusable abstractions:
- `IFeeBandShape` (shared fee-band shape contract),
- `YearScopedEntity` (shared `Id` + `Year` base for entities).

### Why
- Reduces duplication.
- Clarifies which objects are DTO/contracts/entities/models.
- Makes mapping/validation easier to reuse.

### Design note
`IFeeBandShape` remained an interface (not abstract class) to allow multiple type families (DTO/model/entity-adjacent classes) to share a shape without inheritance coupling.

## Decision 11: Folder structure refactor and ownership boundaries

### Decision
Restructure folders so they represent responsibility boundaries instead of historical/scaffold leftovers:
- Keep data-carrying types grouped under `DataModels` (entities, contracts, models, abstractions).
- Keep runtime/business flow under `Application` (calculation, configuration, persistence, swagger-related application wiring).
- Keep HTTP pipeline concerns at API boundary (`Controllers`, `ExceptionHandling`).
- Remove rogue/empty single-item folders and flatten where grouping had no value.

### Why
- Improves discoverability: new contributors can predict where classes should live.
- Reduces “where should this file go?” ambiguity and review churn.
- Separates technical concerns clearly:
  - transport/web,
  - business/application flow,
  - data shape definitions.
- Prevents scattering related DTO/entity/model classes across many tiny folders.

### Alternatives considered
- Keep original structure and only move a few files.
- Enforce strict deep clean architecture folders with more layers/interfaces.
- Keep one-class-per-folder style.

### Selected
Pragmatic middle ground: clean grouping by responsibility with minimal ceremony and KISS bias.

### Trade-off
- Any structural refactor increases short-term diff size and path churn.
- Team needs short adaptation period for new file locations.

### Interview framing
“We changed folder structure to reduce cognitive load and improve ownership clarity, not for cosmetic reasons. The refactor made feature work faster and safer because boundaries became explicit: web concerns at boundary, orchestration in application, and all data carriers centralized in `DataModels`.”

## Decision 12: Database schema and indexing choices

### Decision
Use surrogate primary keys plus unique business constraints and year-focused indexes.

### Why
- Stable row identity for EF.
- Enforce business uniqueness:
  - fee: `(Year, FromMinute, ToMinute)`
  - toll-free: `(Year, Date)`
- Optimize common year-based lookups.

### Additional choice
Include `Price` in fee unique index for read coverage of fee-band queries.

### Trade-off
More indexes increase write maintenance cost; acceptable for read-heavy pattern and moderate write volume.

## Decision 13: Input safety limits in calculation

### Decision
Hard-limit request size and date span in calculation service.

### Why
Protects service from expensive or abusive inputs and keeps runtime predictable.

### Trade-off
Some edge requests are rejected intentionally (`400`) for operational safety.

## Decision 14: Startup safety and operational resilience

### Decision
Startup attempts:
- ensure database schema exists,
- seed missing years.

Failures are logged as warnings instead of crashing startup.

### Why
Improves local/dev resilience and container bootstrap ergonomics.

### Trade-off
Runtime may start in degraded state if DB is unavailable at boot; this is visible through request failures and logs.

## Decision 15: API documentation strategy (Swagger + XML)

### Decision
Annotate endpoints with XML docs and response metadata; add request examples using Swagger filters.

### Why
Creates a self-serve API documentation center and shortens onboarding/debug loops.

### Trade-off
Documentation must be maintained as contracts evolve.

## Decision 16: Testing strategy (unit + black-box)

### Decision
Two complementary layers:
- unit tests for deterministic core logic and edge cases,
- black-box tests for full HTTP + persistence + runtime behavior.

### Why
Unit tests give fast logic feedback; black-box tests verify real integration contract and behavior.

### Coverage intent
- fee math and 60-minute aggregation,
- timezone-sensitive cases,
- year configuration CRUD flows,
- error contracts (`400`/`404`),
- cache-observable behavior after updates.

## Decision 17: Containerization for reproducibility

### Decision
Provide:
- `Dockerfile` (multi-stage .NET build),
- `docker-compose.yml` (API + SQL Server + health checks),
- `smoke-test.sh` (end-to-end quick verification).

### Why
Standardized runtime for local testing and interview/demo environments.

### Trade-off
Compose credentials and ports are developer-focused defaults; production deployment needs hardened secrets/network policy.

## Decision 18: Fault injection endpoint for blackbox testing

### Decision
Added `TestOnlyController` with a `POST /_test/fault/throw` endpoint that throws a controlled exception for verifying error-contract behavior in blackbox tests.

### Why
The exception middleware maps unhandled exceptions to `500 ProblemDetails`. Blackbox tests need to trigger this path to verify the response shape and that internal details are not leaked.

### Safety measures
- Gated by environment (Development or Integration only) AND a config flag (`TestOnly:EnableFaultInjection`).
- Requires `X-Test-Token` header matching the configured token.
- Token comparison uses `CryptographicOperations.FixedTimeEquals` to prevent timing attacks.
- Returns `404` (not `403`) when disabled or token is wrong, making the endpoint indistinguishable from a missing route.
- Hidden from Swagger via `[ApiExplorerSettings(IgnoreApi = true)]`.

### Trade-off
Test-only code in production binary. Mitigated by multi-layer gating and stealth 404 response.

## Decision 19: Source-generated logging

### Decision
Use `[LoggerMessage]` source generator for all structured log messages in the exception handler.

### Why
- Zero-allocation logging at runtime (no string interpolation or boxing).
- Compile-time validation of message templates and parameters.
- Consistent event IDs for log filtering and alerting.

### Trade-off
Requires partial class split (`ExceptionHandlingExtensions.Log.cs`), adding one file.

## Decision 20: FeeBand as readonly record struct

### Decision
The core fee band type is a `readonly record struct` (12 bytes: 3 ints).

### Why
- Stack-allocated, no GC pressure when stored in arrays or passed by value.
- Free structural equality for deduplication and comparison.
- Implements `IFeeBandShape` interface for shared mapping logic across DTOs.

### Alternatives considered
- `record class`: heap-allocated, unnecessary for a 12-byte value type.
- Plain `struct`: no built-in equality or `ToString`.

### Trade-off
`FirstOrDefault` on a struct returns `default(FeeBand)` with `Amount=0` when no band matches. This is intentional (no fee outside configured bands) but requires awareness.

## Decision 21: Connection string fail-fast

### Decision
`Program.cs` throws `InvalidOperationException` if the `TollDb` connection string is missing from configuration, instead of falling back to a hardcoded default.

### Why
A hardcoded fallback masks configuration errors and is a maintenance/security risk. Failing immediately at startup with a clear message is safer.

### Trade-off
Requires the connection string to be present in `appsettings.json` or environment variables. This is already the case for all environments.

## Decision 22: SQL Server retry with execution strategy

### Decision
Enable `sql.EnableRetryOnFailure()` on the SQL Server provider and wrap transactional writes in `CreateExecutionStrategy().ExecuteAsync()`.

### Why
SQL Server can return transient errors (network blips, Azure SQL throttling). The execution strategy automatically retries these.

### Implementation note
Transactions must be created inside the strategy callback, not outside. This is an EF Core requirement for retry-safe transactions.

### Trade-off
Retries add latency on transient failures. Acceptable for correctness.

## Decision 23: Structured logging with Serilog

### Decision
Use Serilog with dual sinks: console (all levels) and rolling file (warnings and above, 14-day retention).

### Why
- Console output for container/development visibility.
- File sink for persistent warning/error history without external infrastructure.
- Suppressed `Microsoft` namespace noise (`LogEventLevel.Warning` override).

### Trade-off
File sink is local to the container/host. Production environments should add a centralized sink (e.g. Seq, Application Insights).

## Decision 24: Project structure modernization

### Decision
Introduced `Directory.Build.props`, `Directory.Packages.props`, and migrated `TollFee.sln` to `TollFee.slnx`.

### Why
- Shared settings (`TargetFramework`, `Nullable`, `ImplicitUsings`) were duplicated across 3 csproj files.
- Package versions were inline and could drift between projects.
- Legacy `.sln` format (65 lines of GUIDs) produces noisy diffs and merge conflicts.

### What changed
- `Directory.Build.props`: centralizes framework and language settings.
- `Directory.Packages.props`: single source of truth for all NuGet versions with version variables for related packages (EF Core, Testcontainers).
- `.slnx`: 10-line XML replaces 65-line legacy format.
- All 3 csproj files stripped to project-specific config only.

### Trade-off
One-time path churn in diffs. Blackbox test fixture needed updating to find `.slnx` instead of `.sln`.

## Decision 25: NoTracking as global default on DbContext

### Decision
Set `QueryTrackingBehavior.NoTracking` globally in `TollDbContext.OnConfiguring`.

### Why
Read-heavy workload. Every read query was already calling `.AsNoTracking()` individually. Global default eliminates repetition and prevents forgetting it on future queries.

### Implementation note
Write paths use `AddRange` and `ExecuteDeleteAsync`, neither of which depend on change tracking. No behavior change for writes.

### Trade-off
If a future write path needs tracking, it must explicitly opt in with `.AsTracking()`.

## Decision 26: Multi-year queries delegate to cached single-year methods

### Decision
`GetFeeBandsForYearsAsync` and `GetTollFreeDatesForYearsAsync` now loop over requested years and call the cached single-year methods instead of issuing a direct DB query.

### Why
The hot calculation path was bypassing the per-year cache and hitting the database on every request. Typical requests span 1-2 years, so this is 1-2 cache lookups instead of 2 DB round-trips.

### Alternatives considered
- Multi-year composite cache keys (e.g. `"fees:2026,2027"`): creates many key combinations, harder to invalidate.
- No change: acceptable latency but wasteful when cache infrastructure already exists.

### Trade-off
Sequential cache lookups per year instead of a single batched DB query. Negligible for 1-2 years; if requests ever span many years, the batch approach could be reintroduced as a fallback.

## Decision 27: Records for all DTOs and models

### Decision
Converted all request DTOs, response DTOs, and internal models from `sealed class` to `sealed record`.

### Why
These types are immutable data carriers. Records provide structural equality, `ToString()`, and `with` expressions for free. No behavior change for JSON serialization or ASP.NET model binding.

### Types converted
- Response: `CalculateFeeResponse`, `FeeBandResponse`, `YearConfigurationResponse`
- Request: all 6 configuration request types
- Internal: `YearRuleConfiguration`

### Trade-off
None. Records with `init` properties serialize identically to classes with `init` properties.

## Decision 28: Entity classes sealed

### Decision
Sealed `Fee` and `TollFree` entity classes.

### Why
EF Core does not require entity inheritance here. Sealing enables JIT devirtualization and communicates that these are not extension points.

### Trade-off
None. The abstract base `YearScopedEntity` remains abstract (cannot be sealed); its concrete subclasses are now sealed.

## Decision 29: Blackbox tests always enabled

### Decision
Removed the `Enabled` flag, `IsEnabled()` guard, and all early-return checks from blackbox tests.

### Why
The tests were passing silently without actually running when the guard was hit. Every test run should exercise the full Docker-based integration path to catch real regressions.

### Trade-off
Every test run requires Docker. This is acceptable since the blackbox tests are already in a separate project and can be filtered out with `--filter` if needed.

## Known risks and mitigations

### 1) Multi-instance cache consistency
- Risk: in-memory cache invalidation is node-local.
- Mitigation: migrate to distributed cache/event invalidation when scaling out.

### 2) `EnsureCreated` limitations for schema evolution
- Risk: not a migration workflow.
- Mitigation: switch to migrations-first deployment in production environments.

### 3) DateTime kind ambiguity (`Unspecified`)
- Risk: caller intent may differ from “already local” assumption.
- Mitigation: document API expectation; optionally enforce/normalize stricter input contracts later.

### 4) Replace-as-a-whole write amplification
- Risk: many updates on huge year configs can create extra churn.
- Mitigation: acceptable now (KISS); differential update strategy can be introduced if needed.

## Why this is “KISS but production-aware”

- Kept core flows straightforward (year upsert, deterministic rule engine, thin controllers).
- Added only high-value complexity: centralized errors, cache invalidation, transactional writes, tests, and containerized reproducibility.
- Deferred heavyweight patterns (distributed cache, event bus, advanced migration orchestration) until scaling justifies them.

## Interview talking points

- “We preserved public API contracts and moved complexity behind stable boundaries.”
- “We standardized failures with domain exceptions + global ProblemDetails mapping.”
- “We normalized to Gothenburg local time before any business decision to prevent timezone bugs.”
- “We chose DB-authoritative year rules with idempotent seed and runtime CRUD for operational flexibility.”
- “We used cache with explicit invalidation on writes to keep hot-year reads fast and correct.”
- “The hot calculation path hits zero DB round-trips on cache-warm requests by delegating multi-year lookups to cached single-year methods.”
- “We kept write consistency with transactional replace-as-a-whole semantics.”
- “We validated architecture through both fast unit tests and real black-box integration scenarios.”
- “We centralized build configuration with Directory.Build.props and central package management to eliminate duplication across projects.”
- “All DTOs and models are records — immutable by design, with free structural equality and no serialization impact.”
- “NoTracking is the global default because the workload is read-heavy and write paths use AddRange/ExecuteDeleteAsync which bypass change tracking.”
- “Blackbox tests are always-on — they spin up real Docker containers with SQL Server and verify the full HTTP contract on every run.”

