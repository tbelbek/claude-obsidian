# Interview Study Cards

Read each card. Memorize the **bold key phrases**. When ready, say "test me."

---

## CRITICAL — You must nail these

### Card 1: Why `IReadOnlyCollection<T>` not `List<T>`?

**Question:** "Why not just use List<T> everywhere?"

**Answer:** "`List<T>` exposes **Add, Remove, Clear** — the caller can modify data they shouldn't own. `IReadOnlyCollection<T>` exposes only **Count and enumeration** — mutation is **prevented at compile time**, not by convention. Example from my code: the repository caches fee bands. If it returned `List<FeeBand>`, a consumer could call `.Add()` and **corrupt the cache**. Returning `IReadOnlyCollection` makes that impossible. Principle: **accept wide types in parameters, return narrow types that communicate intent**."

---

### Card 2: CancellationToken — what happens when browser closes?

**Question:** "Walk me through what happens when a user closes their browser tab mid-request."

**Answer:** "**Browser drops TCP connection → Kestrel detects it → cancels `HttpContext.RequestAborted`** → ASP.NET Core binds that to the `CancellationToken` controller parameter → I propagate it through service → repository → `ToArrayAsync(cancellationToken)` → at the next `await`, EF Core checks the token → throws **`OperationCanceledException`** → request aborts early → **DB connection released, no wasted computation**. Without the token, the full query and calculation would complete and the response gets thrown away."

---

### Card 3: async Task vs async void

**Question:** "What's the difference and why never use async void?"

**Answer:** "`async Task` — caller can **await it, observe exceptions, track completion**. `async void` — cannot be awaited. Critical danger: **unhandled exception in async void crashes the entire process** — it's posted to the SynchronizationContext (or thread pool), which **terminates the app**. It is NOT swallowed — it's a **hard crash**. Only acceptable for **UI event handlers** (WPF button clicks). In ASP.NET Core: **always async Task** so the pipeline handles exceptions through middleware."

---

### Card 4: Sealed — what does it actually do?

**Question:** "Does sealed actually matter? What breaks without it?"

**Answer:** "Sealed prevents **subclassing** (not mutation — that's `readonly`/`init`). Three benefits: (1) **JIT devirtualization** — runtime can inline method calls when no subclass exists. (2) **Design intent** — communicates 'this is complete, don't extend.' Prevents accidental tight coupling via inheritance. (3) **API surface clarity** — private stays truly private. Cost is **zero** — one keyword. We **seal by default** and unseal intentionally when designing for extension."

---

### Card 5: Three DI lifetimes

**Question:** "AddScoped vs AddTransient vs AddSingleton — explain and why you chose Scoped."

**Answer:** "**Transient** = new instance **every injection**. **Scoped** = one instance **per HTTP request** — all services in same request share it. **Singleton** = one for **app lifetime**. I chose Scoped because services inject `TollDbContext` which is Scoped. **Singleton + Scoped DbContext = captive dependency** (stale connection captured forever). Transient = multiple DbContexts per request (breaks transaction consistency). Scoped = **one DbContext, one repository, one consistent view per request**."

---

### Card 6: CI/CD pipeline stages

**Question:** "Developer pushes a commit. What happens from push to production?"

**Answer:** "**PR pipeline:** (1) `dotnet restore` + `build` + `publish`, (2) unit tests (fast, no Docker), (3) blackbox tests (Docker agent). All **gate the merge**.

**Main branch after merge:** (1) same build+test, (2) **Docker build + push** to container registry, (3) **deploy to staging** + run smoke tests, (4) **manual approval gate** + deploy to production + smoke test + **automatic rollback** on failure.

Principle: **tests gate PRs, smoke tests gate deployments, production has manual approval and rollback**."

---

### Card 7: Incident response — production latency spike

**Question:** "3 AM alert — response times jumped from 50ms to 2 seconds. What do you check?"

**Answer:** "Structured top-down: **Dashboard first** (Application Insights) — request duration percentiles + dependency duration. This tells me in 30 seconds if bottleneck is **app, DB, or network**.

**If SQL dependency spiked** → query execution plans, DTU usage, lock waits.
**If app spiked but SQL didn't** → CPU, memory, GC collections, thread pool starvation.
**If neither** → infrastructure — load balancer, network latency, DNS.

Principle: **metrics first → logs second → code third**. Never jump to random guesses."

---

### Card 8: Horizontal vs Vertical scaling

**Question:** "Define both. Which does your system support?"

**Answer:** "**Vertical = bigger machine** (more CPU/RAM). **Horizontal = more machines** behind a load balancer. My system supports **vertical today** (single instance, in-memory cache works fine). **Horizontal is blocked** by in-memory cache divergence — each instance has its own cache, they diverge for up to 12 hours. Fix: **Redis as distributed cache** with pub/sub invalidation (L1/L2 pattern)."

**Never swap the names.** Vertical = UP (bigger). Horizontal = OUT (more).

---

### Card 9: CAP theorem

**Question:** "What is CAP and which does your system prioritize?"

**Answer:** "**Consistency, Availability, Partition tolerance** — in the presence of a network partition, you must choose between C and A. My system is **single-node — CAP doesn't apply** because there's no partition possible. But if scaled to multiple instances with in-memory cache, it becomes **AP**: each node serves from its own cache (available), nodes operate independently (partition tolerant), but **caches diverge** (consistency sacrificed). Moving to Redis with synchronous invalidation shifts toward **CP**."

**Say "single-node, CAP doesn't apply" FIRST, then discuss the multi-node scenario.**

---

### Card 10: Docker Compose vs Kubernetes — three differences

**Question:** "When would you use each?"

**Answer:** "Three K8s capabilities Compose lacks: (1) **Self-healing** — restarts crashed pods, reschedules to healthy nodes. Compose: container dies, stays dead. (2) **Horizontal Pod Autoscaler (HPA)** — auto-scales replicas on metrics. Compose: manual replica count. (3) **Rolling updates with automatic rollback** — zero-downtime deploys, health check failure triggers rollback. Compose: restarts everything at once.

**Compose** = local dev, CI, single-server. **Kubernetes** = production at scale, multi-service, auto-scaling, self-healing."

---

## IMPORTANT — Know these well

### Card 11: Why int minute-of-day internally, not HHmm string?

**Answer:** "**Integer range comparison is the natural representation.** `minuteOfDay >= fromMinute && minuteOfDay <= toMinute` is one CPU comparison — no parsing, no allocation. Strings would require lexicographic comparison (fragile, relies on zero-padding) or TimeSpan parsing per passage (overhead). HHmm is a **human-facing concern at the API boundary**. Internally, minute-of-day is **mathematically correct and performant**."

---

### Card 12: Func delegate mutation pattern — why and how?

**Answer:** "**8 mutation endpoints, same 7-step flow**, only the mutation differs. The Func pattern puts shared flow in two helpers. Each endpoint supplies its mutation as a lambda. The **`bool Updated` return** = not-found signal. Example: `RemoveTollFreeDate` filters the collection, compares lengths — if equal, date wasn't there, `Updated = false`. **Lambda reports, helper decides** — helper throws `EntityNotFoundException` (→ 404). Eliminates **15 lines of duplication across 8 methods**."

---

### Card 13: Three exception types — why not one with error code?

**Answer:** "(1) Each type maps to a **different ProblemDetails Title** — determined by type, not message. (2) Source-generated logging has **separate EventIds** per type — enables filtering alerts by category. (3) **Type-safe catch in tests** — `Assert.ThrowsAsync<YearNotConfiguredException>()` is compile-time safe. Plus **open/closed principle**: new category = new type + new case, not modifying an existing enum."

---

### Card 14: EF Core migrations — how to switch from EnsureCreated

**Answer:** "Five steps: (1) **Remove `EnsureCreatedAsync`** — conflicts with migrations. (2) Install EF tools. (3) **Create initial migration** as baseline. (4) For existing DBs with data, **mark migration as already applied** — insert into `__EFMigrationsHistory` or use idempotent script. (5) **Replace with `MigrateAsync()`** in startup. Main risk: `EnsureCreated` doesn't create `__EFMigrationsHistory` — **migrations have no baseline** on existing databases."

---

### Card 15: `IEnumerable<int>` cast in EF Core

**Answer:** "`int[].Contains()` resolves to **`Array.Contains()`** which EF Core can't translate to SQL. Casting to `IEnumerable<int>` forces **`Enumerable.Contains<T>()`** which EF Core maps to **SQL `WHERE Year IN (@p0, @p1)`**. Without the cast: **runtime translation error**. It's about **LINQ method overload resolution**, not about arrays vs collections."

---

### Card 16: Microservices risks — three reasons NOT to

**Answer:** "(1) **Distributed complexity** — method calls become network calls with latency, timeouts, partial failures. Debugging → distributed tracing. (2) **Data consistency** — no cross-service transactions. Need **saga pattern** with **compensating transactions**. Example: order created + inventory decremented + payment fails = manually undo each step. (3) **Operational overhead** — each service needs its own CI/CD, Docker image, monitoring, scaling config. Small team spends more time on infra than features."

---

### Card 17: Real-time streaming vs batch architecture

**Answer:** "Architecture shifts from **batch to event-driven**. Message broker (**Kafka/Service Bus**) for ingestion. **Per-vehicle state** (Redis or actor-per-vehicle) holding: current window start, window max fee, daily total. Each event processed **incrementally**: load state → check window → update or commit → persist. **Kafka partitioned by vehicleId** guarantees per-vehicle ordering. Late arrivals: grace window or recalculation. Calculation logic stays the same — **orchestration changes**."

---

### Card 18: ProblemDetails — why not plain string?

**Answer:** "**RFC 9457**. Structured, machine-readable fields: **title** (category), **detail** (message), **status** (HTTP code in body). Plain string forces consumers to parse text. Example: API gateway routes retry logic on `status` field without string parsing. Monitoring aggregates errors by `title` without regex. It's the difference between **structured logging and Console.WriteLine**."

---

### Card 19: KISS line — where do you stop adding complexity?

**Answer:** "My line: does this solve **a problem I have today, or a hypothetical one**? Each piece earns its complexity — CRUD API eliminates code changes, caching eliminates DB reads, Func pattern eliminates 15-line duplication. What I did NOT add: distributed cache, event bus, CQRS, migrations, API versioning, auth. Those solve problems I don't have yet. **KISS doesn't mean minimal features — it means every feature earns its complexity.**"

---

### Card 20: Fee amount > 99 — validator gap

**Answer:** "Validator only checks `amount < 0` — **no upper bound**. Fee of 100 passes validation, hits database where `decimal(2,0)` rejects it with **SQL truncation error** — user gets **500 instead of clean 400**. The `checked` cast is on the **read path, not write path** — doesn't help. Fix: add `amount > 99` to validator to match column constraint, or widen column to `decimal(5,0)`. **I kept `decimal(2,0)` because widening requires migration infrastructure I deferred.**"

---

## MARANICS-SPECIFIC

### Card 21: End-to-end ownership

**Question:** "Describe a time you owned a service end to end."

**Answer:** "The toll fee API. I restructured it from a broken starter into a production-ready service: **designed the architecture** (engine/service/repository split), **implemented all business logic** (60-minute window, daily cap, timezone normalization), **persistence** (EF Core, SQL Server, caching), **API surface** (REST configuration endpoints), **testing** (79 unit + 48 blackbox), **containerization** (Dockerfile, docker-compose, health checks, smoke tests), and **documentation** (29 architectural decisions, flow diagrams, test coverage docs). From empty repo to deployable in Docker with verified correctness."

---

### Card 22: Architectural improvements you've driven

**Answer:** "Starting state: controller with hardcoded data, no separation of concerns, no tests, scaffold DB context never used. I drove: **separation into engine/service/repository**, **interface-driven DI** for testability, **centralized exception handling** with ProblemDetails, **in-memory caching** with explicit invalidation, **runtime configuration API** to eliminate code changes for rule updates, **HHmm format** for user-friendly API surface while keeping integer math internally, and **two-layer testing** (unit + blackbox with Testcontainers). Each improvement addressed a specific problem, not theoretical best practice."

---

### Card 23: Working in small distributed teams

**Answer:** "Key principles: **clear ownership boundaries** (my folder structure reflects this — each folder has one responsibility), **async communication** (well-documented code with XML docs, ADRs, and inline comments reduces 'ask the author' dependency), **small PRs** (I'd break the restructure into incremental, mergeable pieces in a team), and **comprehensive tests as documentation** (127 tests describe the system's behavior — a new team member reads the tests to understand the rules)."

---

Say "test me" when you're ready to be quizzed on any of these.
