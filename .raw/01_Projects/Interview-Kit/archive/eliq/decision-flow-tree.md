# Decision / Calculation / Business Flow Tree

## Contents

- [What this delivers](#what-this-delivers)
- [Flow 1: Toll Fee Calculation](#flow-1-toll-fee-calculation)
- [Flow 2: 60-Minute Window + Daily Cap](#flow-2-60-minute-window--daily-cap)
- [Flow 3: Toll-Free Determination](#flow-3-toll-free-determination)
- [Flow 4: Timezone Normalization](#flow-4-timezone-normalization)
- [Flow 5: Year Configuration Management](#flow-5-year-configuration-management)
- [Flow 6: Validation Rules](#flow-6-validation-rules)
- [Flow 7: Startup Seed](#flow-7-startup-seed)
- [Flow 8: Exception-to-HTTP Mapping](#flow-8-exception-to-http-mapping)
- [Flow 9: Caching Strategy](#flow-9-caching-strategy)
- [Flow 10: Fault Injection Endpoint](#flow-10-fault-injection-endpoint)

## What this delivers

This document provides a single, implementation-accurate tree for:

1. Calculation flow (request to response, including all branches)
2. Configuration management flow (CRUD, validation, cache invalidation)
3. Startup seed flow (idempotent JSON seed behavior)
4. Exception-to-HTTP mapping

All flows are derived from the current code paths in:
- `TollFee.Api/Controllers/TollFeeController.cs`
- `TollFee.Api/Controllers/YearConfigurationController.cs`
- `TollFee.Api/Controllers/TestOnlyController.cs`
- `TollFee.Api/Application/Calculation/TollService.cs`
- `TollFee.Api/Application/Calculation/CongestionRuleEngine.cs`
- `TollFee.Api/Application/Configuration/Services/YearConfigurationService.cs`
- `TollFee.Api/Application/Configuration/Services/YearRuleConfigurationValidator.cs`
- `TollFee.Api/Application/Configuration/Services/YearRulesSeedService.cs`
- `TollFee.Api/Application/Persistence/Repositories/TollRulesRepository.cs`
- `TollFee.Api/Application/Persistence/TollDbContext.cs`
- `TollFee.Api/ExceptionHandling/ExceptionHandlingExtensions.cs`

## Flow 1: Toll Fee Calculation

**Why:** This is the core business operation. Separating orchestration (TollService) from pure computation (CongestionRuleEngine) keeps each class testable in isolation.

**Source:**
- `TollFee.Api/Controllers/TollFeeController.cs:27` — HTTP entry point
- `TollFee.Api/Application/Calculation/TollService.cs:13` — orchestration
- `TollFee.Api/Application/Calculation/CongestionRuleEngine.cs:29` — fee math

Entry path:
- `GET /TollFee?request=...`
- `TollFeeController.CalculateFee(...)`
- `TollService.CalculateFeeAsync(...)`

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
|       |   (see Flow 4: Timezone Normalization)
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
|                       +-- Load fee bands per year (see Flow 9: Caching)
|                       +-- Load toll-free dates per year (see Flow 9: Caching)
|                       |
|                       +-- Sort all passages once (Array.Sort, in-place)
|                       |
|                       +-- Single pass: collect distinct days + group chargeable passages
|                       |   (toll-free check per passage, see Flow 3)
|                       |
|                       +-- For each day:
|                       |   +-- CongestionRuleEngine.CalculateDailyFee(...)
|                       |       (see Flow 2: 60-Minute Window + Daily Cap)
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

## Flow 2: 60-Minute Window + Daily Cap

**Why:** The 60-minute window and daily cap are the most complex business rules. Isolating them in a static pure function makes them deterministic and trivial to unit test without any infrastructure.

**Source:** `TollFee.Api/Application/Calculation/CongestionRuleEngine.cs:29` (`CalculateDailyFee`), `:15` (`GetFeeForPassage`)

Sub-flow inside `CongestionRuleEngine.CalculateDailyFee(...)`.

```
CalculateDailyFee(passages, feeBands)
|
+-- Assumes passages are pre-sorted by the caller.
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

## Flow 3: Toll-Free Determination

**Why:** Toll-free rules combine hardcoded logic (weekends, July) with configurable data (per-year holidays). Checking cheapest conditions first (weekend, July) avoids unnecessary set lookups.

**Source:** `TollFee.Api/Application/Calculation/TollService.cs:84` (`IsTollFreeDate`)

Sub-flow inside `TollService.IsTollFreeDate(...)`.

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

## Flow 4: Timezone Normalization

**Why:** Congestion tax rules are legally local-time based. Normalizing all inputs to Gothenburg local time before any business logic prevents timezone bugs, especially around DST transitions and year boundaries.

**Source:** `TollFee.Api/Application/Calculation/TollService.cs:118` (`ToGothenburgLocalTime`), `:128` (`ResolveGothenburgTimeZone`), `:11` (static field initialization)

Sub-flow inside `TollService.ToGothenburgLocalTime(...)`.

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

## Flow 5: Year Configuration Management

**Why:** Rules are year-scoped and managed at runtime so that new years can be configured without code changes or redeployment. All mutation endpoints funnel through a single validation+upsert path for consistency.

**Source:**
- `TollFee.Api/Controllers/YearConfigurationController.cs:40` — HTTP upsert entry
- `TollFee.Api/Application/Configuration/Services/YearConfigurationService.cs:30` — normalize + validate + persist
- `TollFee.Api/Application/Persistence/Repositories/TollRulesRepository.cs:97` — transactional write

Entry path:
- `YearConfigurationController` -> `YearConfigurationService`
- -> `YearRuleConfigurationValidator` (see Flow 6) + `TollRulesRepository`

```
GET /configuration/years/{year}
|
+-- year in configured set?
    +-- [NO]  --> Return 404
    +-- [YES] --> Return 200 + { year, feeBands[], tollFreeDates[] }


PUT /configuration/years/{year}  (full upsert)
|
+-- Validate(year, feeBands, tollFreeDates)
|   (see Flow 6: Validation Rules)
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

## Flow 6: Validation Rules

**Why:** Validating before persistence prevents invalid data from entering the database. A single static validator reused by all write paths (full upsert, granular mutations, seed) guarantees consistent enforcement.

**Source:** `TollFee.Api/Application/Configuration/Services/YearRuleConfigurationValidator.cs:11` (`Validate`)

Validation inside `YearRuleConfigurationValidator.Validate(...)`. Called from Flow 5 before any write.

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

## Flow 7: Startup Seed

**Why:** Fresh environments need initial data without manual API calls. Idempotent seeding (skip existing years) prevents overwriting runtime-curated configurations.

**Source:**
- `TollFee.Api/Program.cs:123` — `SeedConfiguredYearsAsync` startup call
- `TollFee.Api/Application/Configuration/Services/YearRulesSeedService.cs:16` — `SeedMissingYearsFromJsonAsync`

Startup path in `Program.cs` -> `YearRulesSeedService.SeedMissingYearsFromJsonAsync()`.

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

## Flow 8: Exception-to-HTTP Mapping

**Why:** Centralizing exception-to-HTTP mapping in one middleware keeps controllers thin and ensures consistent ProblemDetails responses across all endpoints. Domain exceptions carry business context; the middleware translates them to the correct HTTP status.

**Source:**
- `TollFee.Api/ExceptionHandling/ExceptionHandlingExtensions.cs:11` — `UseTollFeeExceptionHandler`
- `TollFee.Api/ExceptionHandling/ExceptionHandlingExtensions.Log.cs:3` — source-generated log messages

Mapping from `ExceptionHandlingExtensions`.

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

Additional note:
- Model binding errors (for malformed query/body input) can return framework-generated `400` before controller logic executes.
- All error responses use `ProblemDetails` (RFC 9457) format.
- Source-generated logging via `[LoggerMessage]` emits structured events with stable EventIds for each exception type.

## Flow 9: Caching Strategy

**Why:** The calculation hot path repeatedly queries the same year's fee bands and toll-free dates. In-memory caching with explicit invalidation on writes eliminates DB round-trips for cache-warm requests. Multi-year queries delegate to cached single-year methods so the hot path benefits from per-year cache.

**Source:**
- `TollFee.Api/Application/Persistence/Repositories/TollRulesRepository.cs:37` — `GetFeeBandsForYearAsync` (cached)
- `TollFee.Api/Application/Persistence/Repositories/TollRulesRepository.cs:53` — `GetFeeBandsForYearsAsync` (delegates to cached)
- `TollFee.Api/Application/Persistence/Repositories/TollRulesRepository.cs:179` — `InvalidateCache`
- `TollFee.Api/Application/Persistence/TollDbContext.cs:13` — `NoTracking` global default

Read-side caching inside `TollRulesRepository`. Write-side invalidation after upserts.

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
- `QueryTrackingBehavior.NoTracking` set globally on `TollDbContext` — all read queries skip change tracking.

## Flow 10: Fault Injection Endpoint

**Why:** The exception middleware maps unhandled exceptions to sanitized 500 ProblemDetails. Blackbox tests need to trigger this path to verify the response shape and that internal details are not leaked. The endpoint is multi-gated and returns 404 when disabled to avoid revealing its existence.

**Source:** `TollFee.Api/Controllers/TestOnlyController.cs:27` (`Throw`), `:37` (`IsFaultInjectionEnabled`), `:44` (`HasValidToken`)

Entry path: `POST /_test/fault/throw` -> `TestOnlyController.Throw()`.

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
    +-- Exception middleware catches it (see Flow 8)
    +-- Returns 500 ProblemDetails with sanitized message
```

Security measures:
- Returns `404` (not `403`) when disabled or token invalid — indistinguishable from missing route.
- `CryptographicOperations.FixedTimeEquals` prevents timing-based token extraction.
- Hidden from Swagger via `[ApiExplorerSettings(IgnoreApi = true)]`.
- Purpose: allows blackbox tests to verify the `500` error contract without risking production exposure.
