# Presentation Script: What I Changed and Why

Based on comparison between `1701a70` (original) and current implementation.

## Opening (1 min)

"The starter code was a .NET 5 project with 17 files. The controller overwrote the incoming request with hardcoded test data, the fee calculation was an if-else chain with no 60-minute window logic, toll-free dates were a hardcoded 2021 array, the DB context existed but was never wired up, and there were no tests. I'll walk through what I changed -- starting with the infrastructure, then the business logic, and finally the specific technical patterns."

---

# Part 1: General Updates

## Framework: .NET 5 to .NET 10

**Original (`1701a70`):** .NET 5, `Startup.cs` with `ConfigureServices` + `Configure` pattern. `Program.cs` was 6 lines (`CreateHostBuilder` boilerplate). EF Core 5.0.12, Swashbuckle 5.6.3.

**Now:** .NET 10, minimal hosting (top-level `Program.cs`, 136 lines). EF Core 10.0.5, Swashbuckle 10.1.5, Serilog, JetBrains.Annotations. Modern C# features throughout.

**Why:** .NET 5 is end-of-life. .NET 10 gives primary constructors, records, collection expressions, pattern matching, source-generated logging, `FrozenSet`, and current provider versions.

## Build Centralization

**Original:** Single `TollFee.Api.csproj` with inline `net5.0` target and inline package versions. No test projects. Legacy `TollFee.sln` (65 lines of GUIDs).

**Now:**
- `Directory.Build.props` -- centralizes `TargetFramework`, `Nullable`, `ImplicitUsings` across 3 projects
- `Directory.Packages.props` -- `ManagePackageVersionsCentrally` with version variables (`EfCoreVersion`, `TestcontainersVersion`)
- `TollFee.slnx` -- 10 lines of clean XML via `dotnet sln migrate`

**Why:** Single source of truth. No version drift. No GUID merge conflicts.

| Decision | Why | Alternative | Trade-off |
|---|---|---|---|
| Centralize build with `Directory.Build.props` + `Directory.Packages.props` | Shared settings duplicated across 3 csproj; inline versions could drift | Keep inline versions per csproj | One-time path churn in diffs; blackbox fixture needed updating for `.slnx` |

## Folder Structure

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

## Docker and Smoke Test

**Original:** None.

**Now:**
- `Dockerfile` -- multi-stage (SDK build -> runtime), `UseAppHost=false`, port 8080
- `docker-compose.yml` -- SQL Server Express with `sqlcmd` health check (20 retries, 20s start). API depends on `service_healthy`. Volume persistence. Password via env var.
- `smoke-test.sh` -- `set -euo pipefail`. 9 sequential HTTP checks covering empty request, unconfigured year, malformed date, fault endpoint stealth, config CRUD with recalculation verification.

| Decision | Why | Alternative | Trade-off |
|---|---|---|---|
| Provide Dockerfile + docker-compose + smoke test | Standardized runtime for local testing and interview/demo environments | No containerization | Compose credentials and ports are dev defaults; production needs hardened secrets/network policy |

## DI and Interfaces

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
| Consolidate data types under `DataModels` with `IFeeBandShape` + `YearScopedEntity` | Reduces duplication; clarifies DTO/contract/entity roles; reusable mapping/validation | Scatter types across folders | `IFeeBandShape` is interface (not abstract class) to allow multiple type families without inheritance coupling |

---

# Part 2: Logic and Implementation

## Calculation Engine

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
|       |   (see Timezone Normalization below)
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
|                       |       (see 60-Minute Window below)
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

## Timezone Normalization

**Original:** No timezone handling whatsoever. Timestamps used as-is. A UTC `05:10` in summer treated as 05:10 instead of 07:10 CEST.

**Now:** `ToGothenburgLocalTime` (`TollService.cs:118`) switches on `DateTimeKind`:
- `Unspecified` -> as-is (matches ASP.NET query param default)
- `Utc` -> `ConvertTimeFromUtc` to Europe/Stockholm
- `Local` -> `ConvertTime` from caller's zone

Resolution at startup (`TollService.cs:11`, `:128`): `TryFindSystemTimeZoneById` -- IANA first, Windows fallback. Throws if neither found.

| | |
|---|---|
| **Why first** | Tax rules are legally local-time. UTC `2025-12-31T23:30Z` = local `2026-01-01`. Must normalize before year validation. |
| **Trade-off** | `Unspecified = assumed local` is implicit. `DateTimeOffset` would be explicit -- change I'd make if starting over. |

| Decision | Why | Alternative | Trade-off |
|---|---|---|---|
| Normalize all timestamps to Gothenburg local time before any business logic | Congestion-tax rules are legally local-time based | Keep everything in UTC; convert only near fee lookup | Timezone logic must be explicit and tested around DST and year-boundary cases |

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
- Winter (CET): UTC+1. Example: `06:10 UTC => 07:10 local`.
- Summer (CEST): UTC+2. Example: `05:10 UTC => 07:10 local`.
- DST transition handled automatically by `TimeZoneInfo`.

## Year-Scoped Configuration

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
|   (see Validation Rules below)
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

## Persistence and Caching

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
| Surrogate PK + unique business constraints + year indexes | Stable row identity for EF; enforce business uniqueness; optimize year lookups | Keep composite business key as PK | More indexes increase write maintenance cost; acceptable for read-heavy + moderate writes |
| NoTracking as global DbContext default | Every read query already called `.AsNoTracking()` individually; global eliminates repetition | Per-query `.AsNoTracking()` | Future write paths needing tracking must explicitly opt in with `.AsTracking()` |
| SQL Server retry with execution strategy | SQL Server can return transient errors; automatic retry | No retry | Retries add latency on transient failures; acceptable for correctness |
| Connection string fail-fast (`?? throw`) | Hardcoded fallback masks config errors and is a security risk | Hardcoded fallback connection string | Requires connection string in config; already the case for all environments |
| Entity classes sealed | EF Core does not require inheritance here; JIT devirtualization; communicates "not an extension point" | Leave unsealed | None; abstract base `YearScopedEntity` remains abstract, concrete subclasses sealed |

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

## Error Handling

**Original:** No exception handling. No error responses. `Startup.cs` used `UseDeveloperExceptionPage()` in dev but no production error handling. An unconfigured year or any exception -> unhandled 500 with stack trace.

**Now:**

Centralized middleware (`ExceptionHandling/ExceptionHandlingExtensions.cs:11`):
- `YearNotConfiguredException` -> 400
- `InvalidTollRequestException` -> 400
- `EntityNotFoundException` -> 404
- Anything else -> 500, sanitized ("An unexpected error occurred.")
- All ProblemDetails (RFC 9457)

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
- All error responses use `ProblemDetails` (RFC 9457) format.
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
    +-- Exception middleware catches it (see Exception-to-HTTP Mapping above)
    +-- Returns 500 ProblemDetails with sanitized message
```

Security measures:
- Returns `404` (not `403`) when disabled or token invalid -- indistinguishable from missing route.
- `CryptographicOperations.FixedTimeEquals` prevents timing-based token extraction.
- Hidden from Swagger via `[ApiExplorerSettings(IgnoreApi = true)]`.
- Purpose: allows blackbox tests to verify the `500` error contract without risking production exposure.

## Testing

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

## Startup and Swagger

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

---

# Part 3: Technical Implementation Details

## C# Language Features

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

## EF Core Patterns

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

## Caching Patterns

| Pattern | Where | Why |
|---|---|---|
| `IMemoryCache` + 12h TTL | `TollRulesRepository.cs:14` | Config rarely changes. TTL = safety net. Explicit invalidation = immediate consistency on writes. |
| `FrozenSet<T>` | `TollRulesRepository.cs:33`, `:79` | Immutable after construction -- can't corrupt cache. Optimized internal layout for faster lookups than `HashSet`. |
| Cache key memoization | `TollRulesRepository.cs:18-19` | `ConcurrentDictionary` caches interpolated key strings. `static` lambda avoids closure allocation. |
| Multi-year delegation | `TollRulesRepository.cs:53-65` | Batch methods call cached single-year methods. Original bypassed cache. Zero DB on warm cache. |
| Explicit invalidation | `TollRulesRepository.cs:179-184` | 3 keys removed per write. Next read repopulates from DB. TTL-only = up to 12h stale. |

## Type Design

| Pattern | Where | Why |
|---|---|---|
| `IFeeBandShape` | `IFeeBandShape.cs:7` | Shared shape across struct + record class types. Abstract base won't work (struct can't inherit class). One mapping method for all sources. |
| `YearScopedEntity` abstract class | `YearScopedEntity.cs:6` | Entities share `Id` + `Year` with constructor logic. Interface can't provide implementation. Abstract = structural sharing. |
| Domain/entity separation | `FeeBand` vs `Fee` | Engine shouldn't depend on EF Core. `FeeBand` is minimal (3 ints). Repository handles projection. |
| `Func` delegate mutation | `YearConfigurationService.cs:170` | 8 mutations share one read-modify-write flow. Func returns `(bool Updated, collection)`. Eliminates duplication. |

## Security

| Pattern | Where | Why |
|---|---|---|
| `FixedTimeEquals` | `TestOnlyController.cs:57` | Constant-time comparison prevents timing-based token extraction. One line, eliminates a vulnerability class. |
| Stealth 404 | `TestOnlyController.cs:31` | 403 reveals endpoint exists. 404 = indistinguishable from missing route. |
| `[ApiExplorerSettings(IgnoreApi = true)]` | `TestOnlyController.cs:14` | Hidden from Swagger. Combined with `_test/` prefix = invisible. |
| Sanitized 500 | `ExceptionHandlingExtensions.cs:65-66` | Original leaked stack traces. Now: generic message to client, full detail logged server-side. |
| Fail-fast config | `Program.cs:39` | Original: hardcoded fallback -> silent wrong-DB. Now: throw at startup = catch during deployment. |

## Testing Patterns

| Pattern | Where | Why |
|---|---|---|
| Stubs over mocks | `TestHelpers/InMemoryRulesRepository.cs` | Tests behavior, not call patterns. 80-line real implementation. One class to update on interface change. |
| Shared test data | `TestHelpers/TestFeeBands.cs` | Single source of truth. Was duplicated in 3 files -- drift risk. |
| Factory methods | `TollServiceTests.CreateDefaultService()` | Reduces 4-8 line setup to 1 line. Test intent more visible. |
| `try/finally` cleanup | `YearRulesSeedServiceTests.cs` | Temp dir always deleted even if assertions fail. |
| `[Collection]` serialization | `BlackBoxTestFixture.cs` | 48 tests share one Docker fixture (~10s startup). Prevents parallel container conflicts. |
| Always-on blackbox | No skip guard | Original had `Enabled` flag -> silent green passes without running. Now: Docker required, fails loudly if unavailable. |

## Logging

| Pattern | Where | Why |
|---|---|---|
| Serilog dual sinks | `Program.cs:22-37` | Console for dev/container logs. File for persistent warnings/errors. |
| `InvariantCulture` | `Program.cs:24` | Locale-independent log formatting. Prevents `1234,56` on French servers breaking parsers. |
| Microsoft -> Warning | `Program.cs:27` | Suppresses per-request framework noise. Keeps `Hosting.Lifetime` at Info for startup/shutdown. |
| `Log.CloseAndFlush()` in finally | `Program.cs:103` | Serilog buffers writes. Crash without flush = lost crash message. Finally block guarantees flush. |

---

# Known Risks and Mitigations

| # | Risk | Mitigation |
|---|---|---|
| 1 | Multi-instance cache consistency: in-memory cache invalidation is node-local | Migrate to distributed cache/event invalidation when scaling out |
| 2 | `EnsureCreated` limitations for schema evolution: not a migration workflow | Switch to migrations-first deployment in production environments |
| 3 | `DateTime` kind ambiguity (`Unspecified`): caller intent may differ from "already local" assumption | Document API expectation; optionally enforce/normalize stricter input contracts later |
| 4 | Replace-as-a-whole write amplification: many updates on huge year configs can create extra churn | Acceptable now (KISS); differential update strategy can be introduced if needed |

**Why this is "KISS but production-aware":**
- Kept core flows straightforward (year upsert, deterministic rule engine, thin controllers).
- Added only high-value complexity: centralized errors, cache invalidation, transactional writes, tests, and containerized reproducibility.
- Deferred heavyweight patterns (distributed cache, event bus, advanced migration orchestration) until scaling justifies them.

---

## Q&A Reference

### Contract and compatibility

**"Did you change the HTTP contract?"** -- No. Same route, query param, response shape (`TotalFee: int`, `AverageFeePerDay: float`). Response class was in `Models/TollFeeController.cs` (misnamed file) -- moved to `DataModels/Contracts/Responses/CalculateFeeResponse.cs`, upgraded from class to record.

**"What did you keep from the original?"** -- HTTP contract, Fee/TollFree column names, collation, `decimal(2,0)` for Price. Everything else was rewritten.

**"What about the average calculation?"** -- Original: `totalFee / request.Distinct().Count()` (distinct timestamps). Now: `totalFee / distinctDays.Count` (distinct calendar days including toll-free days).

### Calculation rules

**"What's the window boundary rule?"** -- Strict less-than. Exactly 60 min apart -> new window. Original had no window rule at all -- charged every passage independently.

**"Why static for the engine?"** -- No dependencies, no state. Pure computation. Original was also static (`TollFeeService`) but mixed all concerns.

**"Why not use the Fee entity directly?"** -- Entity has DB concerns (`Id`, `decimal`, `Year`, `long` types). Engine needs none of that. Keeps engine independent of EF Core. Original used `Fee` entity shape indirectly through hardcoded if-else.

### Configuration and persistence

**"Why replace-as-a-whole writes?"** -- Differential update needs partial-state validation. Replace validates the complete set. Config changes are rare. Original had no writes at all.

**"What about concurrent config writes?"** -- Read-modify-write race exists. Admin-only, low concurrency. Fix: row version. Documented.

**"Why EnsureCreated instead of Migrate?"** -- No migrations exist. Original had no startup DB logic at all.

**"Why not distributed cache?"** -- Single-instance. IMemoryCache sufficient. Original had no caching.

**"Why did you change the entity types?"** -- `long FromMinute/ToMinute` -> `int` (minutes-of-day max 1439, doesn't need 64 bits). `DateTime Date` -> `DateOnly` (available since .NET 6, semantically correct -- it's a date, not a datetime). `partial class` -> `sealed class` (no scaffold partial needed, sealing enables devirtualization).

### Error handling

**"Why exceptions instead of Result<T>?"** -- Three cases mapping to HTTP codes. Original had no error handling at all.

**"Why 404 instead of 403 on fault endpoint?"** -- 403 reveals existence. 404 gives nothing. Original had no fault endpoint.

### Testing

**"Why no mocking framework?"** -- Stub exercises real code. Mock verifies call patterns. Original had no tests.

**"How do you know blackbox tests run?"** -- Removed skip guard. Docker always starts. Verbose output proves it.

### EF Core internals

**"If NoTracking is global, how does SaveChangesAsync insert?"** -- `NoTracking` only affects queried entities. `AddRange` explicitly sets state to `Added` -- always works regardless of the query tracking default.

**"How does EF Core set Id if it's get-only and constructor passes 0?"** -- EF Core uses constructor binding and backing field access. `ValueGeneratedOnAdd` tells the DB to generate it. EF reads it back after insert.

**"Two admins add a fee band at the same time?"** -- Last-write-wins, silent data loss. Fix: optimistic concurrency via row version on the year aggregate. Acceptable for admin-only, low-concurrency endpoints.

**"Why Swashbuckle instead of built-in OpenAPI in .NET 10?"** -- Swashbuckle has richer filter support (schema, operation, document filters) for examples and tag descriptions. Built-in OpenAPI is still maturing.

### Production readiness

**"What would you change for production?"** -- (1) EF Core migrations. (2) Widen `decimal(2,0)` to `decimal(5,0)`. (3) HTTP response caching. Original wasn't production-ready at all.

**"What if 10,000 req/s?"** -- Redis, response caching, precomputed 1440-slot lookup array.

**"What was the hardest part?"** -- The 60-minute window. Original didn't have it. Strict-less-than boundary matters. 5 boundary tests + manually traced all 48 blackbox scenarios.

**"How confident in correctness?"** -- Every blackbox expected value manually calculated. Every band boundary tested. 2026 holidays verified against Transportstyrelsen. Cross-check traced all 48 scenarios.

**"What if starting over?"** -- `DateTimeOffset` instead of `DateTime`. EF Core migrations from day one.

---

## Interview Talking Points

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
