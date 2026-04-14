# Interview Preparation Scorecard

## Q1: Top 3 problems and prioritization

**Question:** "Walk me through the original codebase — what were the top 3 problems you identified, and how did you prioritize which to fix first?"

**Your answer:** Identified missing rules, checked official source, reorganized repo first, then features.

**Grade: B-**

**Ideal answer:** "Three problems: (1) the controller overwrote input with hardcoded test data — the API was non-functional, (2) the 60-minute window rule was completely absent — the most important business rule was missing, (3) toll-free dates were hardcoded to 2021 with incomplete holidays. I prioritized structural cleanup first because the original had no separation of concerns — business logic in the controller, static classes, no interfaces, no tests. I needed a testable foundation before implementing the window rule, which is the most complex and correctness-critical logic."

---

## Q2: Why restructure before features?

**Question:** "That's risky — why not implement features first on the existing structure?"

**Your answer:** "Leaving technical debt even if I have time."

**Grade: B**

**Ideal answer:** "The original had no interfaces, no DI usage, no tests. Implementing the window rule on that structure would mean untestable code. I needed the engine/service/repository separation to write tests that verify the window boundary — the most critical business rule. The restructure enabled the feature work to be correct from the start."

---

## Q3: Restructure with parallel developers?

**Question:** "How would you handle this if two other developers were working in parallel?"

**Your answer:** "PoC so not applicable, but prioritization matters in agile."

**Grade: C+**

**Ideal answer:** "In a team, I'd break it into small, mergeable PRs: (1) extract interfaces + DI wiring, (2) move files to new folder structure, (3) implement features on the new structure. Each PR is independently reviewable and produces minimal conflicts. I'd communicate the plan upfront so the team knows the folder structure is moving. In this case it was a solo PoC so I did it in one pass."

---

## Q4: Why `int` minute-of-day internally?

**Question:** "Why not use HHmm strings all the way through?"

**Your answer:** Talked about DB indexing and storage, deflected to other type changes.

**Grade: C**

**Ideal answer:** "Integer arithmetic is the natural representation for range comparisons. `minuteOfDay >= fromMinute && minuteOfDay <= toMinute` is a single CPU comparison — no parsing, no allocation. If I used strings internally, I'd either rely on lexicographic comparison (fragile, relies on zero-padding) or parse to TimeSpan on every passage in the hot path (unnecessary overhead). The HHmm format is a human-facing concern — it belongs at the API boundary. Internally, minute-of-day is mathematically correct and performant."

---

## Q5: Multi-instance cache — business impact

**Question:** "What happens on instances 2 and 3 for 12 hours?"

**Your answer:** "Need to wait until 12h exceeds."

**Grade: B-**

**Ideal answer:** "For up to 12 hours, two-thirds of traffic calculates fees with stale rules. If an admin increased a fee from 22 to 30 SEK, those instances undercharge — that's a revenue leak. If they decreased, those instances overcharge — that's a compliance risk. For a government tax system, both are unacceptable at scale. That's why I documented this as a known limitation for single-instance only."

---

## Q6: Multi-instance mitigation

**Question:** "What's your mitigation plan?"

**Your answer:** Redis or event-based invalidation, Redis preferred.

**Grade: B+**

**Ideal answer:** "Redis as a distributed cache with pub/sub for invalidation. On write: invalidate Redis key, publish invalidation event on a Redis channel. All instances subscribe — when they receive the event, they clear their local IMemoryCache. This gives you L1/L2 caching: nanosecond reads from in-process L1 for the common case, Redis as L2 for cross-instance consistency, pub/sub for near-instant invalidation. Event sourcing from the DB is an alternative but adds significant complexity for this use case."

---

## Q7: Redis network overhead

**Question:** "Redis adds network latency to every request. Worth it?"

**Your answer:** "Maybe a middle cache — caching the cache with IMemoryCache — layers of caches."

**Grade: A-**

**Ideal answer:** "L1/L2 caching. In-process IMemoryCache as L1 with a short TTL (30 seconds), Redis as L2 with explicit invalidation via pub/sub. Read path: check L1 (nanoseconds), miss → check L2 (sub-millisecond), miss → DB. Write path: invalidate Redis, publish event, all instances clear their L1. Common case hits L1 — zero network cost. Worst case is a 30-second window of staleness on L1 after a write, which is acceptable for config that changes a few times per year."

---

## Q8: `IEnumerable<int>` cast

**Question:** "Why the cast to `IEnumerable<int>` before `.Contains()`?"

**Your answer (first):** "I have no idea." **(F)**
**Your answer (retry):** "EF Core doesn't know how to translate an array into SQL IN. Documented workaround."

**Grade: B-**

**Ideal answer:** "`int[].Contains()` resolves at compile time to `Array.Contains()`, which EF Core's LINQ translator has no mapping for. Casting to `IEnumerable<int>` forces it to resolve to `Enumerable.Contains<T>()`, which EF Core does know how to translate to SQL `WHERE Year IN (@p0, @p1)`. Without the cast, you get a runtime translation error. It's a documented EF Core quirk around method overload resolution."

---

## Q9: `Func` delegate mutation pattern

**Question:** "Why the Func pattern instead of separate methods?"

**Your answer:** Steps were duplicated across mutations in the service, centralized them. Couldn't explain `bool Updated` flow precisely.

**Grade: C+**

**Ideal answer:** "All 8 mutation endpoints follow the same 7-step flow: load config, check year exists, apply mutation, check if mutation succeeded, re-validate complete config, persist via replace-as-a-whole, invalidate cache. Only the mutation itself differs. The Func pattern puts the shared flow in two helpers — `TryUpdateTollFreeDatesAsync` and `TryUpdateFeeBandsAsync` — and each endpoint supplies just its mutation as a lambda.

The `bool Updated` return handles the 'target not found' case. For example, `RemoveTollFreeDate` filters the collection and compares lengths — if equal, the date wasn't there, so `Updated = false`. The lambda doesn't throw — it just reports. The *helper* checks the bool and throws `EntityNotFoundException` (→ 404). This separates detection (lambda knows what it's looking for) from error handling (centralized in helper). Without this pattern, I'd duplicate 15 lines of orchestration across 8 methods."

---

## Q10: `FirstOrDefault` on struct

**Question:** "What does `FirstOrDefault` return when no band matches, and why does that work correctly?"

**Your answer:** "Returns default value, new instance with int values are 0."

**Grade: B**

**Ideal answer:** "`FirstOrDefault` on a struct returns `default(FeeBand)` — all fields zero: `FromMinute=0`, `ToMinute=0`, `Amount=0`. Accessing `.Amount` gives `0` — no fee outside configured hours, no null check needed. If `FeeBand` were a `record class`, `FirstOrDefault` would return `null`, and `.Amount` would throw `NullReferenceException`. The struct default behavior is what makes this null-safe without any conditional logic."

---

## Q11: Why three exception types instead of one with error code?

**Question:** "Why three separate exception types instead of one `TollFeeException` with an error code?"

**Your answer:** "Better documentation, best practice, different HTTP codes, logging." Couldn't articulate the specific reasons when pushed.

**Grade: C-**

**Ideal answer:** "Three reasons: (1) Each type maps to a different ProblemDetails `Title` — the title is determined by type, not message. A generic exception would need a switch on error codes for the same result. (2) Source-generated logging has separate EventIds per type (1, 2, 3) — enables filtering alerts by category without string matching. (3) Type-safe catch in tests — `Assert.ThrowsAsync<YearNotConfiguredException>()` is compile-time safe, checking an error code property is not. Plus open/closed principle: adding a new category (e.g., 409 Conflict) means adding a new type and a new case, not modifying an existing enum."

---

## Q12: Multi-stage Dockerfile

**Question:** "Walk me through the stages — what's in each, why not single stage?"

**Your answer:** "First installs and builds, second runs. Decreases build time and image size." Couldn't explain layer caching order clearly.

**Grade: B-**

**Ideal answer:** "Two stages: (1) SDK image — copy `.csproj` + `Directory.Build.props` + `Directory.Packages.props`, run `dotnet restore` (cached layer — only invalidated when packages change), then copy source and `dotnet publish`. (2) Runtime image — copy only the published output. SDK image is ~900MB, runtime is ~200MB — the final container has no compiler, no SDK tools, no source code. The layer ordering is key: `restore` before `COPY source` means NuGet downloads are cached when only `.cs` files change. The multi-stage itself is about image size; the layer ordering is about build speed."

---

## Q13: `decimal(2,0)` for Price

**Question:** "What does `decimal(2,0)` mean, max value, why didn't you change it?"

**Your answer:** (needed coaching)

**Grade: F**

**Ideal answer:** "`decimal(2,0)` = 2 digits precision, no decimals — max 99. Current fees are 0-22 SEK, daily cap 60 — sufficient. I changed `long` → `int` because it was unnecessarily wide, `DateTime` → `DateOnly` because a better type exists. `decimal(2,0)` isn't wrong — it's narrow. Widening to `decimal(5,0)` requires a migration, and I have no migration infrastructure (using `EnsureCreated`). Documented as a production improvement: add migrations first, then widen."

---

## Q14: Fee amount of 100 — what catches it?

**Question:** "If someone configures a fee of 100, does the validator catch it, the DB reject it, or the checked cast throw?"

**Your answer:** "That should return a validation error?" (guessing)

**Grade: D**

**Ideal answer:** "The validator only checks `amount < 0` — no upper bound. So 100 passes validation and hits the database, where `decimal(2,0)` rejects it with a SQL truncation error — the user gets a 500 instead of a clean 400. That's a gap. The `checked` cast is on the read path, not the write path, so it doesn't help here. Fix: either add `amount > 99` to the validator to match the column constraint, or widen the column to `decimal(5,0)` and just keep the negative check."

**Action item:** This is a real bug in the code. Consider fixing it before the interview — either add the upper bound check or widen the column.

---

## Q15: Switch to EF Core migrations — steps and risks

**Question:** "If I asked you to switch to migrations right now — exact steps and risks?"

**Your answer:** (needed coaching)

**Grade: F**

**Ideal answer:** "Five steps: (1) Remove `EnsureCreatedAsync` — it conflicts with migrations. (2) Install EF tools (`dotnet tool install dotnet-ef`). (3) Create initial migration as baseline: `dotnet ef migrations add InitialCreate`. (4) For existing databases with data, mark initial migration as already applied — insert into `__EFMigrationsHistory` manually or use idempotent script. Fresh DBs just run `database update`. (5) Replace `EnsureCreatedAsync` with `MigrateAsync()` in startup.

Main risk: `EnsureCreated` doesn't create `__EFMigrationsHistory`, so migrations have no baseline on existing databases. Must establish that baseline manually before switching. After that, standard `migrations add` / `database update` workflow."

---

## Q16: Blackbox tests worth the Docker cost?

**Question:** "Convince me blackbox tests are worth the 10-second Docker startup."

**Your answer:** "E2E replication, test the whole mechanism, cache invalidation after update."

**Grade: B**

**Ideal answer:** "Unit tests verify logic in isolation with stubs — no real cache, no real SQL, no real HTTP serialization. The blackbox test for cache invalidation exercises the full chain: HTTP DELETE toll-free date → controller → service → repository → SQL Server → cache invalidation → HTTP GET recalculate → cache miss → SQL Server re-query → new fee in response. That specific chain can't be tested with a stub. Other examples: EF Core query translation errors (the `IEnumerable<int>` cast workaround would only surface against real SQL Server), JSON serialization mismatches between DTOs and the HTTP contract, and model binding edge cases. The 10-second startup is paid once per test run — all 48 tests share one fixture."

---

## Q17: UTC timestamp trace-through

**Question:** "Walk me through `2026-06-15T05:10:00Z` — from controller to fee amount."

**Your answer:** Listed the flow but said 9 SEK (wrong — it's 22 SEK). Refused to trace the numbers.

**Grade: D+**

**Ideal answer:** "June = CEST (UTC+2). `05:10 UTC + 2h = 07:10 local`. Minute-of-day = `7*60+10 = 430`. Band `0700-0759` (minutes 420-479) = 22 SEK. Single passage, single day → `totalFee = 22`, `averageFeePerDay = 22`."

**Study tip:** Don't memorize all 9 bands. Know the shape: morning peak 07:00-07:59 = 22, evening peak 15:30-16:59 = 22, shoulders = 16, off-peak daytime = 9, outside 06:00-18:29 = 0. Know June = UTC+2, January = UTC+1.

---

## Q18: KISS vs under-engineering — where's the line?

**Question:** "You claim KISS but built 10 endpoints, caching, Func delegates, FrozenSet, source-gen logging. Where do you draw the line?"

**Your answer:** "DRY, easier to use, coding style." Couldn't articulate a decision framework.

**Grade: D+**

**Ideal answer:** "My line: does this solve a problem I have today, or a hypothetical one? Each piece earns its complexity — CRUD API eliminates code changes for config updates, caching eliminates repetitive DB reads, Func pattern eliminates 15-line duplication across 8 methods, FrozenSet is one method call for immutability + perf, source-gen logging is same effort as interpolation but zero allocation.

What I did NOT add: distributed cache, event bus, CQRS, migrations, API versioning, rate limiting, auth. Those solve problems I don't have yet.

KISS doesn't mean minimal features — it means every feature earns its complexity."

---

## Q19: Hand off to a team of 5 — watch out + first change

**Question:** "What's the first thing you'd tell them to watch out for, and the first thing you'd ask them to change?"

**Your answer:** Rate limiting, migrations, centralized cache. Good prioritization on retry but missed the existing race condition.

**Grade: B-**

**Ideal answer:** "'Watch out: the read-modify-write race in `YearConfigurationService` — two concurrent config writes to the same year silently overwrite each other. It's fine for solo use but with 5 people testing config changes, you'll hit it. First change: add EF Core migrations — you can't evolve the schema without them, and every feature that touches the DB will need a migration. Second: add optimistic concurrency (row version) on year config writes. Third: plan the move to Redis for cache when you're ready to scale to multiple instances.'

The key insight they're looking for: mention problems that *already exist in the code* before listing things you'd add."

---

## Final Summary

### Running Average: C+

### Strengths
- You understand the architecture and can describe what you built
- Good instincts on caching (L1/L2), prioritization (security → workflow → scale)
- Honest when you don't know something

### Weaknesses — Study These
1. **Precision under pressure** — When pushed past your first answer, you give vague responses instead of naming exact mechanisms. Practice: answer the *specific* question, name the components, describe the flow step by step.
2. **Domain knowledge gaps** — You couldn't trace a timestamp through your own fee bands (said 9 SEK instead of 22). Know the peak bands (07:00-07:59 = 22, 15:30-16:59 = 22) and timezone offsets (June = UTC+2, January = UTC+1).
3. **EF Core internals** — The `IEnumerable<int>` cast, `EnsureCreated` vs migrations transition, `NoTracking` + `AddRange` interaction. These are implementation details *in your code* — you must own them.
4. **Validator gap** — No upper bound check on fee amount. `decimal(2,0)` rejects at DB level with a 500 instead of a clean 400. Fix this or be ready to acknowledge it.
5. **"Why" articulation** — For every pattern (Func delegate, separate exception types, struct default, sealed classes), practice the one-sentence technical reason, not "best practice" or "documentation."

### Top 5 Questions to Re-Study Before Interview
1. Q4 — Why int minute-of-day internally (integer range comparison, not string/parsing)
2. Q9 — Func delegate pattern (8 mutations, same flow, bool Updated = not-found signal)
3. Q11 — Three exception types (different Title, different EventId, type-safe catch, open/closed)
4. Q14 — Fee amount 100 (validator gap, DB rejects, 500 instead of 400)
5. Q15 — EF Core migrations transition (5 steps, `__EFMigrationsHistory` baseline risk)

**Pattern:** You understand the *what* but struggle with the *why* at the precise technical level. When pushed past your first answer, you tend to give vague responses ("fails gracefully," "gets confused") instead of naming the exact mechanism.

**Key rule:** Answer the specific question asked, be specific, name the components, describe the flow step by step. Then expand.
