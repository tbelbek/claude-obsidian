# Interview Round 2 — Scorecard

15 questions. Broad range: code, architecture, cloud, devops, code quality, general concepts.

---

## Q1: Production latency spike at 3 AM — investigation process

**Your answer:** DB queries first, then deadlocks, then memory/CPU, then network. Unstructured, jumped between causes.

**Grade: C-**

**Ideal answer:** "First: Application Insights dashboard — request duration percentiles and dependency duration. Tells me in 30 seconds if bottleneck is app, DB, or network. Second: if SQL dependency spiked → query plans, DTU usage, lock waits. If app spiked but SQL didn't → CPU, memory, GC collections, thread pool starvation. Third: if neither → infrastructure — load balancer, network latency, DNS. Always: metrics first, then logs, then code."

**Key principle:** Top-down structured investigation: dashboard → narrow scope → drill into cause. Never jump to random guesses.

---


## Q2: Optimize for 10x traffic — which step, how?

**Your answer:** Tried to parallelize steps but got dependency order wrong. Eventually said "database" but recognized cache handles it. Guessed sorting/normalizing.

**Grade: C+**

**Ideal answer:** "With warm cache, all 8 steps are already cheap — normalize O(n), sort O(n log n), calculation O(n), all on max 1000 items. The bottleneck at 10x is not per-request cost, it is request volume. The optimization is HTTP response caching: same query string = same output. ASP.NET Core output caching or a CDN eliminates all 8 steps for repeated requests. For non-cacheable requests, the current design handles 10x fine — the cache absorbs DB pressure, and the calculation is CPU-trivial."

**Key insight:** When per-request cost is already low, the 10x answer is caching the response, not speeding up the computation.

---


## Q3: AddScoped vs AddTransient vs AddSingleton

**Your answer:** "Req based, instance, app lifecycle." Couldn't explain what defines a scope or why Scoped specifically.

**Grade: C**

**Ideal answer:** "Transient = new instance every injection. Scoped = one instance per HTTP request — all services in the same request share it. Singleton = one for the app lifetime. I chose Scoped because services inject TollDbContext (Scoped). Singleton + Scoped DbContext = captive dependency (stale connection). Transient = multiple DbContexts per request (breaks transaction consistency). Scoped = one DbContext, one repository, one consistent view per request."

**Key concept:** Captive dependency — a Singleton holding a Scoped service captures a stale instance.

---

## Q4: What breaks if you remove the Docker health check?

**Your answer:** First said "other service won't start" (wrong — opposite). Then "crash" (wrong). Then corrected: "logs warning, confused with missing connection string."

**Grade: B-**

**Ideal answer:** "Without the health check, depends_on only waits for container start, not readiness. SQL Server takes 8-20 seconds to accept connections. The API starts immediately, InitializeDatabaseAsync fails silently (try-catch logs warning), seed doesn't run. API is alive but broken — first request gets YearNotConfiguredException because no years are configured. The health check ensures SQL accepts connections before the API initializes. Without it, every docker compose up is a race condition."

**Key concept:** Container started != service ready. Health checks bridge that gap.

---

## Q5: Horizontal vs vertical scaling

**Your answer:** Good analogy ("more officers" vs "genius officer") but swapped the names twice. Correctly identified cache as the horizontal scaling blocker after correction. Fix: centralized cache.

**Grade: C+**

**Ideal answer:** "Vertical = bigger machine (more CPU/RAM) — works with my architecture as-is, single instance, in-memory cache is fine. Horizontal = more instances behind a load balancer — blocked by in-memory cache divergence. Fix: Redis as distributed cache with pub/sub invalidation (L1/L2 pattern). The DB is already shared so persistence scales horizontally. The stateless calculation engine scales perfectly. Only the cache layer needs work."

**Key tip:** Get the terminology right. Vertical = up (bigger). Horizontal = out (more). Never swap them.

---

## Q6: Does sealed actually matter?

**Your answer:** "Structural decision, nothing breaks, not intended to be mutable." Confused sealed (inheritance) with mutability.

**Grade: D+**

**Ideal answer:** "Sealed prevents subclassing, not mutation — different concepts. Three benefits: (1) JIT devirtualization — runtime can inline interface dispatch when no subclass exists. (2) Design intent — communicates 'this is complete, don't extend.' Prevents accidental tight coupling via inheritance. (3) Explicit API surface — private stays truly private. Cost is zero (one keyword), benefit compounds. We seal by default and unseal intentionally when designing for extension."

**Key distinction:** sealed = no inheritance. readonly/init = no mutation. Different axes.

---

## Q7: Why ProblemDetails instead of plain string?

**Your answer:** "RFC suggests it as standard, recognizable by other parts of the system." Correct direction but couldn't name the RFC or specific fields.

**Grade: C+**

**Ideal answer:** "RFC 9457 — industry standard for HTTP API errors. ProblemDetails gives structured, machine-readable fields: title (category), detail (specific message), status (HTTP code in body). A plain string forces consumers to parse text. Example: API gateway routes retry logic on status field without string parsing. Monitoring aggregates errors by title without regex. It is the difference between structured logging and Console.WriteLine — same info, but one is queryable."

**Key point:** Name the RFC (9457). Know the fields (type, title, detail, status, instance). Give a concrete consumer example.

---

## Q8: SOLID — which principle most visible?

**Your answer:** Named all 5 correctly. Pointed to CongestionRuleEngine (SRP) and TollService (DIP). Explained DI payoff: "test without changes using in-memory repository."

**Grade: A-**

**Ideal answer is what you said, plus:** "TollService at line 7 takes ITollRulesRepository — it has no idea about EF Core, SQL Server, or caching. In production it gets TollRulesRepository with real SQL. In tests it gets InMemoryRulesRepository with dictionaries. Zero changes to the service. That is dependency inversion paying off concretely."

**Note:** First strong answer in this round. You did well when you could connect theory to your own code.

---

## Q9: CI/CD pipeline stages

**Your answer:** Described the PR workflow (branch, push, review, merge) but not the technical pipeline stages. Couldn't name specific commands or stage structure.

**Grade: C-**

**Ideal answer:** "PR pipeline: (1) dotnet restore + build + publish, (2) unit tests (fast, no Docker), (3) blackbox tests (Docker agent). All gate the merge. Main branch: (1) same build+test, (2) Docker build + push to container registry, (3) deploy to staging + smoke test, (4) manual approval gate + deploy to production + smoke test + automatic rollback on failure. Tests gate PRs, smoke tests gate deployments, production has manual approval."

**Key distinction:** Workflow (branch/PR/review) vs pipeline stages (build/test/deploy). They asked for stages.

---

## Q10: Static vs injectable — when to promote?

**Your answer:** "If we need dependency inversion for some reason." Couldn't give a specific scenario.

**Grade: C**

**Ideal answer:** "Principle: static when pure — all inputs via parameters, no dependencies, no side effects. Promote to injectable when it needs something from outside its parameters. Concrete: if the daily cap became year-configurable (DB-stored, not constant 60), the engine needs a config source. Or per-vehicle-type fee rules need a vehicle rules provider. Either introduces a dependency that can't be a method parameter — extract ICongestionRuleEngine interface, register in DI."

**Key phrase:** "Pure function = static. External dependency = injectable. The trigger is the first dependency that can't be a parameter."

---

## Q11: async Task vs async void

**Your answer:** "async void is fire and forget, can't track result." Then: "exception is swallowed."

**Grade: C**

**Ideal answer:** "async Task — caller can await, observe exceptions, track completion. async void — cannot be awaited. Critical danger: unhandled exception in async void crashes the process — it is posted to the SynchronizationContext (or thread pool if none), which terminates the app. It is not swallowed — it is a hard crash. Only acceptable for UI event handlers where the framework expects it. In ASP.NET Core, always async Task so the pipeline handles exceptions through middleware."

**Key correction:** async void exceptions are NOT swallowed — they crash the process. Worse than silent.

---

## Q12: Adding 2027 holidays — operational process

**Your answer:** Use the API, Transportstyrelsen is the source, suggested a scraper.

**Grade: B-**

**Ideal answer:** "Simplest: add 2027 to the seed JSON file. On next deployment, the seed service auto-inserts missing years — no API call, version-controlled in git. For ongoing ops: scheduled job checks if next year is configured 30 days before year-end, alerts ops team if not. A scraper is fragile (layout changes break silently). The key is that someone owns the process — the seed file for initial deploy, the API for runtime adjustments, and a reminder system to prevent the January 1st 400 error."

**Key insight:** The seed file is not just for first boot — updating it and redeploying is the simplest year-rollover strategy.

---

## Q13: CAP theorem — which two does your system prioritize?

**Your answer:** Named C, A, P correctly. Said "only guarantee two." Guessed AP because of in-memory cache.

**Grade: C+**

**Ideal answer:** "CAP: in the presence of a network partition, you choose consistency or availability. My current system is single-node — CAP doesn't apply because there's no partition possible. But if scaled to multiple instances with in-memory cache, it becomes AP: each node serves responses from its own cache (available), nodes operate independently (partition tolerant), but caches diverge for up to 12 hours (consistency sacrificed). Moving to Redis with synchronous invalidation shifts toward CP — consistent across nodes, but Redis outage could block reads."

**Key insight:** CAP applies to distributed systems. Single-node = not applicable. Say that first, then discuss the multi-node scenario.

---

## Q14: CancellationToken — what happens when browser tab closes?

**Your answer:** (needed coaching)

**Grade: F**

**Ideal answer:** "Browser drops TCP connection. Kestrel detects it, cancels HttpContext.RequestAborted. ASP.NET Core binds that to the CancellationToken controller parameter. I propagate it through service → repository → ToArrayAsync(cancellationToken). At the next await, EF Core checks the token, throws OperationCanceledException, request aborts early — DB connection released, no wasted computation. Without the token, the full query and calculation would complete and the response gets thrown away. The token enables early exit, saving server resources."

**Key chain:** Browser disconnects → Kestrel → HttpContext.RequestAborted → controller param → service → repository → EF Core → OperationCanceledException → early exit.

---

## Q15: One thing you'd do differently?

**Your answer:** Start with EF Core migrations and add API rate limiting from the start. Justified rate limiting as a public API defense-in-depth principle.

**Grade: B+**

**Ideal answer:** "Two things: (1) EF Core migrations from day one — EnsureCreated blocks schema evolution and creates a painful transition later. (2) DateTimeOffset instead of DateTime for the API contract — makes timezone explicit in the wire format, eliminates the Unspecified ambiguity. Rate limiting is valid but is typically an API gateway concern (Azure API Management, nginx) rather than application-level — worth mentioning but not the top 'do differently.'"

**Note:** Good self-awareness on migrations. Rate limiting answer was solid but DateTimeOffset would have shown deeper technical reflection on a decision already in the codebase.

---

## Final Summary — Round 2

### Score Distribution

| Grade | Count | Questions |
|---|---|---|
| A- | 1 | Q8 (SOLID) |
| B+ | 1 | Q15 (do differently) |
| B- | 2 | Q4 (Docker health), Q12 (2027 holidays) |
| C+ | 3 | Q2 (optimize 10x), Q5 (horizontal/vertical), Q7 (ProblemDetails), Q13 (CAP) |
| C | 3 | Q3 (DI lifetimes), Q10 (static vs injectable), Q11 (async void) |
| C- | 2 | Q1 (incident response), Q9 (CI/CD stages) |
| D+ | 1 | Q6 (sealed) |
| F | 1 | Q14 (CancellationToken) |

### Running Average: C+

### Improvement from Round 1
- Better on code-specific questions you can connect to your own files (Q8 SOLID was strong)
- Still weak on "explain the mechanism" questions (Q14 CancellationToken, Q6 sealed, Q11 async void)
- DevOps/cloud questions need work (Q1 incident, Q9 CI/CD)

### Top 5 to Study Before Interview
1. **Q14 — CancellationToken chain:** Browser → Kestrel → HttpContext.RequestAborted → controller → service → EF Core → OperationCanceledException
2. **Q9 — CI/CD stages:** restore → build → unit test → blackbox test → Docker build+push → deploy staging + smoke → approval gate → deploy prod + smoke
3. **Q1 — Incident response:** Dashboard first (App Insights) → narrow scope (app/DB/network) → drill into cause. Metrics → logs → code.
4. **Q6 — Sealed:** Prevents inheritance (not mutation). JIT devirtualization + design intent + API surface clarity. Zero cost.
5. **Q11 — async void:** Exception crashes process (not swallowed). Only for UI event handlers. ASP.NET Core: always async Task.

### Pattern
Your strongest answers come when you can point to your own code and explain what it does. Your weakest are "explain the mechanism" questions about framework/runtime behavior. Study the *why* behind the patterns you used — not just that you used them.

---

# Mixed Session (Eliq + MARANICS)

## MQ1: Real-time stream processing vs batch request-response

**Your answer:** "WebSocket or long-running requests." Only addressed transport, not processing architecture.

**Grade: D+**

**Ideal answer:** "Architecture shifts from batch to event-driven. Message broker (Kafka/Service Bus) for ingestion. Per-vehicle state (Redis or actor-per-vehicle) holding: current window start, window max fee, daily running total. Each event processed incrementally: load state → check window → update or commit → persist state. Kafka partitioned by vehicleId guarantees per-vehicle ordering. Late arrivals: grace window or recalculation. The calculation logic (fee bands, window, cap) stays the same — the orchestration changes from batch-sort-group to incremental-per-event."

**Key distinction:** Transport (WebSocket) vs processing architecture (event-driven, per-entity state, incremental calculation). They asked about architecture, not protocol.

---

## MQ2: Docker Compose vs Kubernetes

**Your answer:** "Scaling horizontal/vertical, ingresses, traffic between services." Vague, no specific feature names.

**Grade: C-**

**Ideal answer:** "Three specific K8s capabilities Compose lacks: (1) Self-healing — restarts crashed pods, reschedules to healthy nodes. (2) Horizontal Pod Autoscaler (HPA) — auto-scales replicas on CPU/memory/custom metrics. (3) Rolling updates with automatic rollback — zero-downtime deploys, health check failure triggers rollback. Use Compose for local dev/CI/single-server. Kubernetes for production scale — multi-service, auto-scaling, self-healing, zero-downtime."

**Key tip:** Name features by their Kubernetes names (HPA, Deployment, Ingress, Service). Vague descriptions sound like you've read about it but never used it.

---

## MQ3: FeeBandClockFormat validation — trace "2500" and "07ab"

**Your answer:** Initially confused config flow with calculation flow. After correction: correctly identified InvalidTollRequestException → 400. Correctly distinguished parsable-but-invalid ("2500" → range error) from unparsable ("07ab" → format error).

**Grade: B+**

**Ideal answer:** "FeeBandClockFormat.ParseToMinuteOfDay has two validation layers. Line 9: checks length=4 and all digits — '07ab' fails here with 'must use HHmm format.' Line 17: checks hours 0-23 and minutes 0-59 — '2500' passes digit check but fails hours range with 'must be a valid 24-hour time.' Both throw InvalidTollRequestException, middleware maps to 400 ProblemDetails."

**Note:** Good recovery after initial confusion. You know the HHmm validation code well.

---

## MQ4: Three reasons NOT to go microservices

**Your answer:** Complexity of scattered services, data consistency needs modeling, operational overhead per service. When pushed for a concrete data example, described the need to notify other services to roll back but didn't name the saga pattern.

**Grade: B-**

**Ideal answer:** "(1) Distributed complexity — method calls become network calls with latency, timeouts, partial failures. Debugging shifts from stack traces to distributed tracing. (2) Data consistency — no cross-service transactions. Example: Order created + inventory decremented + payment fails = need compensating transactions (saga pattern) to undo each step manually. No automatic rollback. (3) Operational overhead — each service needs its own CI/CD, Docker image, monitoring, scaling. Small team spends more time on infra than features."

**Key terms to memorize:** Saga pattern, compensating transactions, eventual consistency, distributed tracing.

---

## MQ5: Why IReadOnlyCollection not List?

**Coaching provided:** List exposes Add/Remove/Clear — caller can corrupt data. IReadOnlyCollection: only Count + enumeration, mutation prevented at compile time. Example: cache returns FrozenSet — if List, consumer could .Add() and corrupt cache. Principle: accept wide types in params, return narrow types that communicate intent.

---

**Your practice answer:** "List exposes more methods than needed, we prevent mutation. Cache is FrozenSet — List would let someone corrupt it. Principle: return as narrow as possible."

**Grade: A-** — Hit all key points concisely. To make it perfect, add "prevented at compile time, not by convention."

---

## MQ6: Why different return types — IReadOnlyCollection vs IReadOnlySet?

**Coaching:** Fee bands iterated sequentially (collection). Toll-free dates need O(1) .Contains() lookup (set). Return type communicates usage pattern.

**Your practice answer:** "Toll-free dates need fast lookup, IReadOnlySet is good at it. IReadOnlyCollection says iterate, relatively slower but more flexible."

**Grade: B+** — Got the key distinction (set = fast lookup, collection = iteration). Minor correction: collection isn't "more flexible" — it's less capable. Fee bands use collection because they don't need set lookup, they're iterated sequentially. Pick type by usage, not flexibility.

---

## MQ7: AI-assisted development — how and risks?

**Coaching:** Benefits: reviews, tracing, scaffolding, documentation. Risks: blindly accepting code, over-reliance, security (AI sees code), accountability. Key phrase: "If I can't explain it, I don't ship it."

**Your practice answer:** "Claude Code is not a silver bullet. Needs heavy supervision. Good for tracing and scaffolding small snippets, saves brainpower for bigger decisions."

**Grade: B** — Good honest take on benefits and supervision. Missing: explicit mention of risks (blindly accepting code, accountability). Add: "The risk is accepting code you don't understand. I review every line and own every decision — the tool assists, I'm accountable."

---

## MQ8: Task.WhenAll vs Task.WhenAny

**Coaching:** WhenAll = all tasks, completes when last finishes. WhenAny = completes when first finishes. WhenAll example: load bands + dates in parallel. WhenAny example: timeout pattern.

**Your practice answer:** "WhenAll waits for all tasks. WhenAny waits for one. My app loads fee bands and free dates — parallel with WhenAll since both needed. WhenAny for timeouts — if task exceeds timespan, return error instead of keeping client waiting."

**Grade: A** — Both definitions correct, both examples concrete and from your own code. Perfect.

---

## MQ9: Why ITollRulesRepository abstraction over DbContext?

**Coaching:** (1) Testability — InMemoryRulesRepository, no EF. (2) Caching hidden — service doesn't know about cache, swap strategy by changing repo only. (3) Query encapsulation — LINQ, FrozenSet, IEnumerable cast all in repo. Principle: service knows what data it needs, repo knows how to get it.

**Your practice answer:** "Principle: service knows what it needs, repo knows how to get it. Testability — inject InMemoryRulesRepository with no code change. Caching hidden — service doesn't know about it, swap cache by changing repo only. Query encapsulation — FrozenSet, IEnumerable cast workaround all contained in repo."

**Grade: A** — Led with principle, three concrete reasons with examples. Pattern: you answer well when you can connect to your own code.

---

## MQ10: ADR vs code comment — when to use which?

**Coaching:** ADR = decision with alternatives and trade-offs (someone could reasonably choose differently). Comment = explains what/how for tricky code. Test: if someone could have chosen differently → ADR. If explaining syntax/workaround → comment.

**Your practice answer:** "ADRs show what was considered, why alternatives were not chosen, and trade-offs — prevents future devs from exploring the same paths. A comment only explains the current code. An ADR explains all possibilities with their trade-offs."

**Grade: A-** — Clean distinction. To make it perfect, add one example: "Replace-as-a-whole writes vs differential patching — both valid, I chose one with trade-offs → ADR. The IEnumerable cast is a workaround, not a choice between alternatives → comment."

---

## MQ11: Middleware and exception handler pipeline order

**Coaching:** Middleware = pipeline of components, each can work before/after next() or short-circuit. Exception handler registered first = outermost layer. Request goes in through layers, exceptions bubble back out. Outermost catches everything inside it. If registered after controllers, controller exceptions bubble past uncaught.

**Your practice answer:** "Middleware handles requests and passes to next with next(). Can short-circuit. Exception handler is first in pipeline = first in contact with request."

**Grade: B** — Good middleware definition. Missing the key insight: being first matters because exceptions bubble OUTWARD — outermost layer catches everything inside it. "First in contact with request" is true but the reason is about the response/exception path, not the request path.

---

## MQ12: What makes a REST API RESTful?

**Coaching:** 4 practical constraints: stateless, resource-based URIs, HTTP verbs for actions, uniform interface with JSON. HATEOAS is a constraint almost nobody implements. Know your own violations.

**Your practice answer:** "Stateless, resource URLs not action URLs, proper HTTP verbs, uniform interface. I don't implement HATEOAS — common. My config API follows REST: configuration/years shows resource. But TollFee endpoint violates it — shows the action, not the resource."

**Grade: A-** — Named the constraints, applied them to own code, identified own violation with awareness. Strong self-critical answer. To perfect: "I preserved the original contract name. Renaming would break backward compatibility for no benefit."

---

## MQ13: record vs class — why both?

**Coaching:** Record: structural equality, ToString prints values, with expression for copies. Class: reference equality, EF Core needs reference identity for change tracking. Records can confuse change tracker — same values = equal, but might be different tracked rows.

**Your practice answer:** "Records for equality — DTOs with same values are equal. Entities need reference identity for EF Core tracking."

**Grade: B** — Core distinction correct. Missing: ToString prints values (useful in logs/tests), with expression for immutable copies. Don't just say equality — mention all three benefits.

---

## MQ14: First 30 days on a new team with legacy codebase

**Coaching:** Week 1-2: listen — read code/docs, set up local env, run tests, attend stand-ups, identify owners. Week 2-3: small wins — pick a bug, ship through their PR process, learn CI/CD by doing. Week 3-4: propose — document observations with trade-offs, discuss in team meeting, start with high-value low-disruption. Key: "Listen first, small wins second, propose third. Never rewrite day one."

**Your practice answer:** "Listen and learn first weeks, then small implementations, then proposals but still listening."

**Grade: B** — Right structure. Add one concrete action per phase to show experience: "read the code and run the tests" / "pick a backlog bug and ship through their PR process" / "document observations with trade-offs and discuss in a team meeting."

---

## MQ15: Technical debt — definition and intentional example

**Coaching:** Tech debt = conscious shortcut, borrow speed now, pay maintenance later. Not bad code (that's unintentional). Your examples: EnsureCreated, decimal(2,0), in-memory cache, read-modify-write race. Key: documenting it so team knows the interest rate.

**Your practice answer:** "Technical debt is a shortcut taken consciously — quick fix now but interest later. You will need to pay it. Example: EnsureCreated instead of migrations. Not needed for current scope — no schema changes planned. Interest: when schema evolves, transition to migrations is harder than starting with them. Documented in known risks."

**Grade: A-** — Clean definition, concrete example from own code, articulated the trade-off (no schema changes planned vs harder transition later), mentioned documentation. To perfect: add one more example to show breadth — "also the in-memory cache — works now, blocks horizontal scaling later."

---

## Mixed Session Summary

| Grade | Count | Questions |
|---|---|---|
| A / A- | 5 | MQ5, MQ8, MQ9, MQ10, MQ12 |
| B / B+ | 4 | MQ3, MQ6, MQ7, MQ14 |
| B- | 1 | MQ4 |
| C- | 1 | MQ2 |
| D+ | 1 | MQ1 |

### Running Average: B

### Improvement Trend
- Round 1: C+
- Round 2: C+
- Mixed session: **B**

### What improved
- You're connecting answers to your own code consistently now
- Clean definitions (tech debt, REST, middleware, IReadOnlyCollection)
- Self-critical awareness (identified TollFee endpoint REST violation yourself)

### Still needs work
- Event-driven / streaming architecture (MQ1)
- Kubernetes specifics — name features by their K8s names (MQ2)
- When pushed for concrete examples, add one immediately — don't wait to be asked twice

---

# Session 3 — Mixed with short technical questions

## S3Q1: Value type vs reference type

**Coaching:** Value types = stack, copied by value (int, DateTime, struct, enum). Reference types = heap, copied by reference (class, record class, string, array). record struct = value type. record class = reference type. Boxing: value type cast to interface = copied to heap. Your FeeBand implements IFeeBandShape — passed as IFeeBandShape = boxed.

**Your practice answer:** "Value types like int, datetime, dateonly, bool stored in stack, copied by value. Records, strings, arrays, interfaces stored in heap, copied by reference."

**Grade: B-** — Correct basics but two errors: (1) record struct is value type not reference. (2) Interfaces aren't stored anywhere — they're contracts. Value type cast to interface = boxing (heap allocation).

---

## S3Q2: init vs set keyword

**Coaching:** set = mutable anytime. init = only during initialization (constructor/object initializer), then read-only. JSON deserialization uses object initializers so init works. After deserialization, immutable. init + sealed record = immutable by design, compiler-enforced.

**Your practice answer:** "set allows change after construction, init only during initialization. TotalFee should be immutable after calculation — we should not modify it after."

**Grade: A** — Precise definition with concrete reasoning from own code.

---

## S3Q3: IEnumerable vs ICollection vs IList vs IReadOnlyList

**Coaching:** Two separate hierarchies. Mutable: IEnumerable → ICollection (Add/Remove/Count) → IList (index/Insert). Read-only: IEnumerable → IReadOnlyCollection (Count) → IReadOnlyList (Count + index). They don't inherit from each other. Parameter rule: prefer read-only branch unless mutation needed.

**Your practice answer:** Correctly described the mutable hierarchy additions. Confused IReadOnlyList as "IList minus mutation" — it's actually a separate branch that never had mutation.

**Grade: B-** — Good on the mutable side. Key correction: two parallel families, not one family with methods removed. Memorize the two-branch diagram.

---

## S3Q4: ConfigureAwait(false) — what and why not used?

**Coaching:** Tells awaiter not to capture SynchronizationContext — resume on any thread pool thread. Old ASP.NET/WPF have SyncContext → deadlock risk without it. ASP.NET Core has no SyncContext → no-op. Still needed in library code (NuGet packages) that might be consumed by WPF/legacy apps.

**Your practice answer:** "Needed in old frameworks like WPF. Continuation needs context thread, context thread waits for await — deadlock. Modern .NET Core has no sync context so it's a no-op."

**Grade: A-** — Correctly explained the deadlock mechanism and the no-op in Core. Missed the library code scenario — libraries still need it because they don't know their consumer.

---

## S3Q5: Authentication vs Authorization

**Coaching:** Authentication = who are you (JWT, API key, OAuth). Authorization = what can you do (roles, policies, claims). Your API has neither — UseAuthorization is in pipeline but no auth scheme registered, no [Authorize] attributes. Fault injection uses manual token check, not real auth. "Public API" still needs API key for tracking/rate limiting. Honest answer: PoC, auth out of scope.

**Your practice answer:** "Authentication: who are you. Authorization: what your ID allows you in. None implemented — intended as public API."

**Grade: B** — Clean definitions, correct that none implemented. Missed: "public API" still needs auth (API keys for tracking/abuse prevention). Better framing: "PoC — auth out of scope. Production needs API key at minimum."

---

## S3Q6: params keyword and recent changes

**Coaching:** params packages variable arguments into array. Accessed like normal array. C# 13: params works with any collection type — ReadOnlySpan<T> enables stack allocation (zero heap). Old params T[] always heap-allocated.

**Your practice answer:** "params packs parameters into array automatically. Latest version allows any collection type. ReadOnlySpan allows stack allocation for small lists."

**Grade: B+** — Correct definition, knew the C# 13 change and the ReadOnlySpan benefit. Minor: don't ask the interviewer questions back — answer confidently.

---

## S3Q7: Optimistic vs pessimistic concurrency — how in your code?

**Coaching:** Pessimistic = lock before read, blocks others. Optimistic = read freely, check version before write, retry on conflict. Implementation: add rowversion column (SQL Server auto-increments), EF Core adds WHERE clause automatically, throws DbUpdateConcurrencyException on mismatch. Translate to 409 Conflict.

**Your practice answer:** "Pessimistic: lock before read. Optimistic: no lock, fails if version changed between read and write, retry. Add rowversion, increment on write, upsert checks version, mismatch throws concurrency exception. Unlikely for PoC but theoretically needed."

**Grade: A-** — Clear definitions, correct implementation approach with rowversion, practical context (unlikely for PoC). Minor: SQL Server rowversion auto-increments — you don't manually increment it. EF Core throws DbUpdateConcurrencyException automatically.

---

## S3Q8: string.Empty vs "" and why in DTOs

**Coaching:** No functional difference — both interned to same object. string.Empty is readability convention for intentional empty. Real point: non-nullable string with default prevents null — JSON deserialization gets empty string instead of null if field omitted.

**Your practice answer:** "No difference in C#, same thing but shows intention. The real reason is nullability."

**Grade: A** — Cut past the trivia, identified the real design point. Exactly what an interviewer wants to hear.

---

## S3Q9: p99 tail latency — what does it mean, what to investigate?

**Coaching:** 99% fine, 1% takes 15x longer = tail latency. Common .NET causes: (1) GC pauses (Gen2 stops all threads), (2) thread pool starvation, (3) cache miss on TTL expiration, (4) SQL lock contention, (5) cold start / JIT. Tool: App Insights dependency tracking correlated with slow requests.

**Your practice answer:** "99% responded in 200ms. Edge cases: thread starvation from thread pool, cache miss, SQL slowness, cold start after restart."

**Grade: B+** — Good spread of causes. Missed GC pauses — the most common .NET-specific tail latency cause. Add to checklist: "In .NET, first check for p99 spikes is GC Gen2 collections."

---

## S3Q10: Abstract class vs interface — decision rule

**Coaching:** Abstract class: state + constructors + shared implementation. Interface: behavioral contract, multiple inheritance, cross-type-family sharing. Decision: abstract when types share state/initialization, interface when types share contract across different families or for DI.

**Your practice answer:** "Abstract is concrete with shared logic, constructors, state. Interface is signatures with different logic per implementation. Struct can't inherit class so interface is only option. YearScopedEntity: abstract — Fee and TollFree share state with constructor. IFeeBandShape: interface — different type families (struct, record class). ITollRulesRepository: interface — behavioral contract, no shared state."

**Grade: A** — Correct principles with three concrete examples from own code, each with clear reasoning. Minor: "abstract is concrete" isn't precise — abstract classes can have abstract (bodyless) methods too. Unique advantage is state + constructors.

---

## S3Q11: const vs static readonly

**Coaching:** const = compile-time, baked into IL, must be literal. static readonly = runtime, can use new/methods/computation. Gotcha: changing public const requires consumer recompile (value baked in). Your code: DailyCap = 60 (literal → const). CacheTtl = TimeSpan.FromHours(12) (method call → static readonly).

**Your practice answer:** "const baked at compile time. static readonly set at runtime, can use new, method calls, computations. CacheTtl uses method call so must be static readonly. DailyCap is static value, no computation, so const."

**Grade: A** — Correct distinction, correct reasoning for both examples from own code.

---

## S3Q12: Idempotency — which endpoints?

**Coaching:** Idempotent = same result on repeated calls. GET/PUT/DELETE idempotent by design. POST not — but deduplication can make it effectively idempotent. Your DELETEs: second call returns 404 but state unchanged = idempotent.

**Your practice answer:** "Idempotent = same result for same action. Calculate fee, year updates, band updates are idempotent. POSTs should be non-idempotent but ours are effectively idempotent due to .Distinct() deduplication and overlap validation."

**Grade: A** — Clean definition, correct categorization, identified the nuance that POST endpoints are effectively idempotent through business logic. This is the kind of answer that impresses.

---

## S3Q13: nameof() — what and when

**Coaching:** Returns string name of variable/type/member at compile time. Refactoring safe — rename updates automatically, hardcoded string doesn't. Common: ArgumentNullException, logging, INotifyPropertyChanged.

**Your practice answer:** "Instead of hardcoding item names, nameof returns the string name. Won't break when root item renamed. Example: ArgumentNullException with nameof(passages)."

**Grade: A-** — Correct definition, refactoring benefit, concrete example.

---

## S3Q14: Code review — junior catches Exception in controller

**Coaching:** Three issues: (1) Security — exception.Message can leak internals (stack traces, SQL, paths). Return generic message, log real error. (2) Architecture — per-controller catch = inconsistent error responses. Use centralized middleware. (3) Specificity — bare Exception treats validation errors (400) and DB timeouts (500) the same.

**Your practice answer:** "Don't return full exception to user. Per-controller catch means no centralized mechanism — inconsistent responses across controllers. Generic exception swallows details by catching everything the same way."

**Grade: A** — All three points hit cleanly: security, consistency, specificity. This is a senior developer's answer.

---

## Session 3 Summary

| Grade | Count | Questions |
|---|---|---|
| A / A- | 8 | S3Q2, S3Q4, S3Q7, S3Q8, S3Q10, S3Q11, S3Q12, S3Q14 |
| B+ | 2 | S3Q6, S3Q9 |
| B / B- | 3 | S3Q1, S3Q3, S3Q5 |

### Session 3 Average: A-/B+

### Trend Across All Sessions
- Round 1: C+
- Round 2: C+
- Mixed session: B
- **Session 3: A-/B+**

### What improved
- Consistently connecting theory to your own code
- Strong on C# language features (init, const, sealed, nameof, params)
- Architectural reasoning getting sharper (abstract vs interface with 3 examples, optimistic concurrency implementation)
- Code review answer was senior-level

### Remaining weak spots
- Collection interface hierarchy (two branches, not one minus methods)
- Value type vs reference type precision (record struct vs record class distinction)
- Remember GC pauses as .NET-specific tail latency cause

### Ready for interview: YES — with study card review

---

# Session 4 — Architectural deep-dives

## S4Q1: Linear scan vs alternatives for fee band lookup

**Coaching:** Alternatives: (1) sorted array + binary search O(log n), (2) minute-indexed lookup array int[1440] O(1) ~6KB, (3) interval tree (overkill). Linear scan on 9 structs is effectively O(1) — branch predictor handles small loops. At 10K+ RPS: pre-computed lookup array. KISS: don't optimize what isn't slow.

**Your practice answer:** "Nine bands, KISS. Alternatives: sorted array, minute-indexed lookup array, minute range dictionary. At scale: minute-indexed array — low cost."

**Grade: B+** — Good alternatives listed, correct pick (lookup array). Couldn't state the cost (1440 × 4 bytes = ~6KB, O(1)). Know the number: 1440 minutes per day.

---

## S4Q2: Replace-as-a-whole vs differential patching — validation problem

**Coaching:** Overlap validation needs complete set regardless — differential doesn't reduce validation work. Differential adds merge logic (which rows to INSERT/UPDATE/leave). Concurrent differential patches can each pass validation independently but create invalid combined state. Defense: config changes few times per year — 9 rows wasted is microseconds. Differential merge logic maintained forever. Optimize for developer time, not database time.

**Your practice answer:** "Validation work is the same — need complete set either way. Differential adds insert/update logic = more complex. I chose maintainability since updates happen few times per year. Waste is negligible but differential logic maintained forever."

**Grade: A-** — Identified equal validation work, correct trade-off (frequency vs maintenance cost). Needed coaching on the defense but delivered it cleanly after.

---

## S4Q3: Normalize-first vs UTC-everywhere — multi-city trade-off

**Coaching:** Single city: normalize first = simpler, one conversion, all logic uses local time. Multi-city with different timezones: store UTC, pass timezone as parameter so engine is city-agnostic. Current approach correct for single-city scope. Multi-city refactoring: service level only — engine already takes fee bands as input, doesn't know about timezones.

**Your practice answer:** "Single city/timezone: normalize first is easier for dev, familiar times, no UTC/local confusion. Multi-country: keep UTC as standard, parse to each city's timezone — more complexity but necessary. Current approach correct for single city."

**Grade: B+** — Correct trade-off for both scenarios. Missed the specific architectural impact: static timezone field → parameter, service refactoring needed but engine stays unchanged.

---

## S4Q4: Is IFeeBandShape still earning its keep after HHmm change?

**Coaching:** After HHmm change, UpsertFeeBandRequest and FeeBandResponse no longer implement IFeeBandShape (string properties vs int). Only FeeBand implements it. One type + one consumer = borderline dead weight. Honest answer: acknowledge it, say you'd evaluate removing it. Shows you can judge whether abstractions still earn their complexity.

**Your practice answer:** "Good catch. Original implementation had int-based shape across three types. After HHmm change, request and response diverged. Interface lost most consumers. Correct analysis — I might remove it."

**Grade: A-** — Honest acknowledgment, explained the evolution (why it existed, what changed). Didn't defensively justify keeping a dead abstraction. Shows architectural maturity.

---

## S4Q5: Why not put weekends and July in the database too?

**Coaching:** Hardcoded = legal constants (law), short-circuit before DB lookup (perf), no operational risk of accidental removal. Configurable dates handle what varies (holidays per year). Multi-city might need them in DB. Back pocket: "accidental removal = illegal charging."

**Your practice answer:** "Filter early — weekend/July drops before cache/DB. Setting weekends per year in DB is unnecessary overhead. Basic checks: month and day-of-week. But multi-city might need it in DB if rules differ."

**Grade: A-** — Performance reasoning, operational simplicity, multi-city awareness. Dismissed the legal argument but acknowledged it's a consideration.

---

## S4Q6: Testcontainers vs WebApplicationFactory with in-memory provider

**Coaching:** In-memory provider: no SQL translation (IEnumerable cast untested), no constraints (unique/decimal truncation), no transactions (execution strategy untested), different behavior. Real SQL: catches query translation failures, constraint violations, transaction behavior. 10-second cost paid once, 48 tests in 350ms after.

**Your practice answer:** "In-memory tests C# code, not the full chain. I want HTTP → controller → service → EF Core → SQL Server including transactions. 10 seconds per build is worth 48 edge case tests. In-memory misses: decimal truncation, unique constraint violations."

**Grade: A** — Correct reasoning, concrete bug examples (decimal truncation, unique constraints). Clean cost-benefit framing.

---

## S4Q7: Static IsTollFreeDate vs extracted service vs repository method

**Coaching:** Static on TollService: simple, one consumer, no extra abstraction. Repository: wrong — business rule, not data access. Separate service: over-engineering for one consumer. Extract when second consumer appears. YAGNI.

**Your practice answer:** "YAGNI — one consumer, static is fine. Second consumer → extract. Repository? No — it's a business rule, not data access."

**Grade: A** — Clean YAGNI reasoning, correct rejection of repository with precise reason (business rule ≠ data access). Concise.

---

## S4Q8: Three initialization mechanisms — consolidate?

**Coaching:** Current: EnsureCreated + seed JSON + config API = three mechanisms. Ideal: migrations (schema + seed in one versioned unit via HasData or InsertData) + config API (runtime). Seed JSON becomes unnecessary. Adding new year = new migration, version controlled, PR reviewed.

**Your practice answer:** "Config API stays — runtime requirement. DB and seed can consolidate into migration system — initial migration contains seed data. Schema + seed = one versioned unit."

**Grade: A-** — Correct consolidation (three → two). Identified the right mechanism (migration with seed). Needed coaching on the verbal explanation of how HasData/InsertData works. Know the phrase: "HasData in OnModelCreating or InsertData in migration Up method."

---

## S4Q9: Custom exception middleware vs built-in UseExceptionHandler

**Coaching:** Built-in maps all exceptions to 500. Per-type mapping (400/404/500), per-type titles, per-type logging with EventIds all require customization. Custom middleware is 40 lines — same effort as customizing the built-in, more control.

**Your practice answer:** "Needed per-type mapping — 400, 404, 500 per exception. Built-in doesn't have that extensibility. We still need to code the mapping either way."

**Grade: A-** — Correct reasoning. Could add: "40 lines, not complex. Plus I get source-generated logging with stable EventIds per exception type — built-in doesn't offer that."

---

## S4Q10: Explain architecture to non-technical stakeholder

**Coaching:** No code, no patterns, no acronyms. Business value: what it does + what makes it reliable.

**Your practice answer:** "We built a tax calculation system where you can configure free dates — any regulatory change applied instantly. 127 test cases for a simple calculator, so quality ensured on every build."

**Grade: A** — Business value, no jargon, two sentences. Configurability + quality. Exactly right.

---

## Session 4 Summary

| Grade | Count | Questions |
|---|---|---|
| A / A- | 8 | S4Q2, S4Q4, S4Q5, S4Q6, S4Q7, S4Q8, S4Q9, S4Q10 |
| B+ | 2 | S4Q1, S4Q3 |

### Session 4 Average: A-

### Trend Across All Sessions
- Round 1: C+
- Round 2: C+
- Mixed session: B
- Session 3: A-/B+
- **Session 4: A-**

### Pattern
Your architectural reasoning is now consistently strong. You articulate trade-offs clearly, point to your own code, and know when to say "YAGNI" vs "I'd extract when there's a second consumer." The remaining B+ answers were about knowing specific numbers (1440 minutes, 6KB) and architectural impacts of multi-city (timezone as parameter). Minor gaps — you're interview-ready.

---

# Session 5 — Hard push test

## S5Q1: 07:00 and 08:00 — how many charges and why?

**Your answer:** "2 charges. Window ends at 07:59."

**Grade: C** — Correct answer (2) but wrong boundary (07:59 vs 08:00). The window end is start + 60 min = 08:00. Comparison is strict less-than: 08:00 NOT < 08:00 → new window. Must memorize: window end = start + 60, comparison is strict <.

## S5Q2: async void exception — what happens?

**Your answer:** First "crash and burn" (vague). After coaching: "No task to observe, thread pool thinks uncaught, triggers AppDomain.UnhandledException, terminates process."

**Grade: B-** — Needed coaching but retained the mechanism correctly on repeat.

## S5Q3: NoTracking global — does SaveChanges work after modifying queried entity?

**Your answer:** "Won't save, need to add to DbContext explicitly." Then said "AddOrUpdate" — which doesn't exist in EF Core.

**Grade: C-** — Correct diagnosis (won't save, not tracked). Wrong fix (AddOrUpdate isn't EF Core). Correct fixes: context.Update(entity) or query with .AsTracking(). Must memorize both options.

---

## S5Q4: Crash between commit and cache invalidation — what happens?

**Your answer:** "Old cache, wait until invalidated." Then "invalidate on restart, first hit." Then "invalidate on error?" Then "catch transaction error?"

**Grade: D+** — Struggled through multiple wrong approaches. Key insight: if app crashes, IMemoryCache is empty on restart — problem fixes itself. Real risk: app doesn't crash, stale for 12h. Fix: invalidate BEFORE the write — cache miss on failed write is harmless (repopulates from unchanged DB). Eliminates stale window entirely.

---

## S5Q5: Task<T> vs ValueTask<T>

**Your answer:** "Task always allocates on heap. ValueTask returns from cache if sync, otherwise same as Task since it's a struct."

**Grade: B** — Core distinction correct (allocation avoidance on sync path). Confused the rules: said "should not await a ValueTask" — wrong, you do await it. Rules: never await twice, never .Result before completion. Use when hot path often completes synchronously (cache hits). Default to Task otherwise.

---

## S5Q6: FrozenSet for dates but array for bands — why different?

**Your answer:** "FrozenSet has Contains for equality. Array better for range comparison — in-between LINQ check."

**Grade: B+** — Correct distinction: equality lookup vs range scan. Could be sharper: "FrozenSet.Contains uses Equals — can't check 'which band's range covers this minute.' That's a predicate scan, needs iteration."

---

## S5Q7: Transient error mid-transaction — what happens?

**Your answer (first):** "Data rolled back, won't retry." (Half right — rollback yes, but it DOES retry.)
**Your answer (after coaching):** "Transaction rolls back completely, execution strategy retries from the start."

**Grade: B-** — Needed coaching but delivered the clean one-sentence answer after. Key: execution strategy DOES retry — the entire callback re-executes with a fresh transaction. That's why transaction must be inside the callback.

---

## S5Q8: CancellationToken chain — browser to database (retry)

**Your answer:** "Browser drops TCP, Kestrel cancels with RequestAborted, controller token fires, goes through app, EF Core throws OperationCanceledException, DB connection releases."

**Grade: B+** — Got the full chain on retry. Previously was F (needed full coaching). Improvement. Missing detail: "HttpContext.RequestAborted" and "bound to controller parameter" but the chain is correct end to end.

---

## S5Q9: Double sort — Array.Sort in service + OrderBy in engine

**Your answer:** "Waste. Remove the one in service, leave sorting to engine." Then correctly identified that one global sort is less work than N daily sorts.

**Grade: B+** — Correct that it's waste, correct instinct on which to remove. The nuance: .OrderBy() on already-sorted data is O(n) not O(n log n) — so keeping both is wasteful but not catastrophically so. Cleanest: keep engine defensive (sorts internally), remove service sort (redundant).

---

## Session 5 Summary

| Grade | Count | Questions |
|---|---|---|
| A | 0 | |
| B / B+ | 4 | S5Q2, S5Q5, S5Q6, S5Q8, S5Q9 |
| C / C- | 2 | S5Q1, S5Q3 |
| D+ | 1 | S5Q4 |

### Session 5 Average: B-

### This was the hard push session — expected lower scores.

### Key weaknesses confirmed under pressure:
1. **60-minute window boundary** — still says 07:59 instead of 08:00. The comparison is < 08:00, not <= 07:59. MUST fix.
2. **EF Core update with NoTracking** — said AddOrUpdate (doesn't exist). Fix: context.Update(entity) or .AsTracking() on query.
3. **Cache invalidation timing** — didn't know to invalidate before write. Memorize: before = harmless cache miss. After = stale risk on crash.
4. **CancellationToken** — improving (B+ from F) but still needs the chain memorized cold.

### Overall Trend
- Round 1: C+
- Round 2: C+
- Mixed: B
- Session 3: A-/B+
- Session 4: A-
- Session 5 (hard push): B-

### Ready for interview: YES
Your A-level sessions show you can perform. The B- under pressure shows your floor. Study the 4 weaknesses above — those are the exact questions that will separate a "hire" from a "strong hire."

---

# Session 6 — Broad coverage, varied depth

## S6Q1: throw vs throw ex

**Your answer:** "throw throws same, throw ex generates new ex and resets stack."

**Grade: B+** — Correct behavior. Minor: throw ex doesn't generate a NEW exception — same object, reset stack trace.

## S6Q2: float vs decimal vs double for AverageFeePerDay

**Your answer:** "Precision. Financial report needs decimal, but not the intention here so float is fine."

**Grade: B** — Correct reasoning (display vs financial). Couldn't distinguish float vs double — the honest answer is "preserved original contract, display-only metric, float vs double doesn't matter here."

---

## S6Q3: Clustered vs non-clustered index — what does your Fee table have?

**Your answer:** "Clustered: data is the index, one per table. Non-clustered: separate structure, many per table. Fee has both — clustered on Id, non-clustered on Year/FromMinute/ToMinute with included Price. No key lookup when that query runs — won't touch the table."

**Grade: A** — Definitions correct, applied to own table, explained covering index benefit (no key lookup). Complete answer.

---

## S6Q4: SQL vs NoSQL — when which, was SQL Server right?

**Your answer:** "SQL: structured, relational, FK, ACID. NoSQL: flexible schema, various models, eventual consistency, horizontal scale. SQL Server right — small relational data, transactions needed by design."

**Grade: B+** — Correct distinctions, correct choice for project. Needed coaching on ACID definition and why NoSQL scales horizontally (partition key, no cross-node joins). Memorize ACID: Atomicity, Consistency, Isolation, Durability.

---

## S6Q5: Span<T> — what and should you use it?

**Your answer:** "Good for slicing arrays without copying. Not needed for my project."

**Grade: B** — Core benefit correct (zero-copy slicing). Know also: stack-only (can't store in fields, can't cross await), used for string parsing and byte buffers. Correctly identified project doesn't need it.

---

## S6Q6: Middleware order — swap exception handler and auth?

**Your answer:** "Middleware is onion/FIFO. If auth goes first and has an error, exception handler can't catch it."

**Grade: A** — Correct mechanism (onion model), correct consequence (auth exceptions bypass handler). Clean one-sentence answer.

---

## S6Q7: ?? and ??= operators

**Your answer:** "Returns right side if null, else left. ??= assigns instead. Null coalescing."

**Grade: A** — Correct behavior, correct name. Clean.

---

## S6Q8: Health check endpoint — what, why, do you have one?

**Your answer:** "Infrastructure provider needs small endpoint to check if alive. 503 if unhealthy. Don't have one. Would add /health with MapHealthChecks."

**Grade: B+** — Correct purpose, honest that it's missing, knew the fix (MapHealthChecks). Could add: "AddHealthChecks().AddSqlServer() to verify DB dependency, not just app liveness."

---

## S6Q9: IDisposable vs IAsyncDisposable

**Your answer:** "IDisposable sync, IAsyncDisposable async. Need async because sync dispose blocks thread during rollback — could cause thread pool starvation." Asked for starvation explanation.

**Grade: B+** — Correct distinction, correct reasoning for async dispose, correctly linked to thread pool starvation. Needed coaching on the starvation mechanism itself. Key: limited threads + sync blocking = no threads for new requests.

---

## S6Q10: Static extension vs IExceptionHandler — would you switch?

**Your answer:** "Current scale, KISS is enough. Would switch for chained handling, DI needs, or testability."

**Grade: A-** — Correct trade-off, knew the triggers for switching. Could add: "IExceptionHandler is ASP.NET Core 8+ — supports DI, multiple chained handlers, and works with AddProblemDetails() for automatic formatting."

---

## Session 6 Summary

| Grade | Count | Questions |
|---|---|---|
| A / A- | 4 | S6Q3, S6Q6, S6Q7, S6Q10 |
| B / B+ | 5 | S6Q1, S6Q2, S6Q4, S6Q5, S6Q8, S6Q9 |

### Session 6 Average: B+/A-

### Trend Across All Sessions
- Round 1: C+
- Round 2: C+
- Mixed: B
- Session 3: A-/B+
- Session 4: A-
- Session 5 (hard push): B-
- **Session 6: B+/A-**

### Pattern
Consistently strong now. Your B+ answers are close to A — just missing one precision detail (ACID definition, Span stack-only constraint, health check DB dependency). No C or D grades this session. You've stabilized at B+/A- range even across varied topics (SQL indexing, C# operators, middleware ordering, DevOps health checks, disposal patterns).

### Overall assessment: Interview ready.

---

# Session 7 — Project explanation + follow-ups

## S7Q1: Tell me about the project
**Grade: B+** — Good overview: framework upgrade, DB, runtime config, separation of concerns, tests. Could be tighter — mention the 60-minute window rule as the key missing business logic.

## S7Q2: Why standalone engine?
**Grade: A** — "Parameters vs rules. App changes parameters (bands, dates), engine enforces rules (60-min window, daily cap) set by law. Engine doesn't know where bands came from." Strong principle.

## S7Q3: Break down the 127 tests
**Grade: B** — Mentioned unit + e2e, real-life scenarios. Concrete examples (week calculation, feeband change, cache test). Could add: "79 unit for logic isolation, 48 blackbox for full HTTP stack."

## S7Q4: Test gaps
**Grade: B** — Listed gaps honestly (no auth, no concurrent, no UTC e2e). Justified auth/concurrency as intentional. UTC justification was weak — say "covered in unit tests" not "only one city."

## S7Q5: Explain caching non-technically
**Grade: A** — "Printed page" analogy. Cost = DB read. Happens every 12h or on update. Normal users never wait for the printer.

## S7Q6: Admin adds a holiday — end to end
**Grade: A** — All 6 steps in order: POST → load → add → validate → persist atomically → invalidate → next request picks up.

## S7Q7: What is a pure function?
**Grade: B** — First said "no dependencies" (incomplete). After coaching: "Same input same output, no side effects." Said thread-safe because deterministic — correction: thread-safe because no shared mutable state, not because deterministic.

## Session 7 Average: B+

### Overall Trend
- Round 1: C+
- Round 2: C+
- Mixed: B
- Session 3: A-/B+
- Session 4: A-
- Session 5: B-
- Session 6: B+/A-
- **Session 7: B+**

### Strong points in this session
- Rules vs parameters distinction (A — original insight)
- Non-technical cache analogy (A — memorable)
- End-to-end admin flow (A — all steps, correct order)
- Honest about gaps with justification

### Key corrections to memorize
- Pure function: same input/output + no side effects (not just "no dependencies")
- Thread-safe: because no shared mutable state (not because deterministic)
- UTC gap mitigation: "covered in unit tests" not "only one city"

---

# Session 8 — Continued

## S8Q1: Daily cap change — how many files?
**Grade: A** — "Const and engine." One file, one constant. Clean.

## S8Q2: Move toll-free storage from SQL to Redis — what changes?
**Grade: C+** — Struggled. Said service and dbcontext need to change. Missed the key insight: service talks to ITollRulesRepository (interface) — create new RedisTollRulesRepository, swap DI registration, everything else untouched. This IS separation of concerns — use this example next time.

**Key phrase to memorize:** "New repository class implementing same interface, one DI registration swap. Service, engine, controllers, tests — all untouched."

---

## S8Q3: Why keep PUT when POST can add everything?

**Your answer (first):** "Against RFC and REST standards." — too abstract.
**Your answer (after coaching):** "PUT sets everything in one batch. Without it, 25 POSTs instead of one. Open for mistakes. PUT gives a reset — change payload, send again, done."

**Grade: B** — Needed coaching but delivered the practical answer cleanly. Key lesson: never lead with "the standard says." Lead with practical impact, then mention standards if asked.

---

## S8Q4: Manual HHmm parsing vs TimeSpan.TryParseExact

**Your answer:** "TryParse is fiddly with format specifiers. Only gives bool — still need to determine why it failed for custom error messages. Manual parsing is straightforward and readable."

**Grade: B+** — Correct practical reasoning. Could add: "6 lines, anyone reads it and understands it instantly."

---

## S8Q5: One more week — what would you spend it on?

**Your answer:** "Migrations, fix decimal cap bug, add validation for > 99."

**Grade: B+** — Good priorities. Defended YAGNI on column widening when challenged: "Don't need to support > 99, but need to give clean 400 instead of raw 500 when someone sends bad input." Good reframe — input validation vs feature expansion.

## S8Q6: YAGNI challenge — widen column vs add validator

**Your answer:** "We don't need fees above 99 but someone might send it by mistake. Should not show direct DB error to user."

**Grade: A-** — Reframed from capacity problem to UX problem. Validator is input validation (clean error), not feature expansion. Well defended under pressure.

---

## S8Q7: Exceptions vs Result<T> — defend your choice

**Your answer (first):** "I prefer to throw and catch in middleware." — just restated the choice, no reasoning.
**Your answer (after coaching):** "Result types for business errors, exceptions for truly exceptional cases. Exceptions short-circuit instead of continuing. Centralized middleware."

**Grade: B** — Needed coaching but got to the right reasoning. Key distinction to memorize: "My errors are exceptional (misconfiguration, invalid input) not expected business outcomes (insufficient funds). Exceptions short-circuit the stack, one middleware catches all. Result would add unwrap boilerplate at every layer for the same mapping."

---

## S8Q8: What does checked keyword do?

**Your answer:** "Throws exception if decimal doesn't fit in int. Instead of silent truncation, throws when data might be lost."

**Grade: A-** — Correct. Needed coaching but delivered clean answer. Key phrase: "fail-fast instead of corrupt data."

---

## Session 8 Summary

| Grade | Count | Questions |
|---|---|---|
| A / A- | 3 | S8Q1, S8Q6, S8Q8 |
| B / B+ | 4 | S8Q3, S8Q4, S8Q5, S8Q7 |
| C+ | 1 | S8Q2 |

### Session 8 Average: B+

### Overall Trend
- Round 1: C+
- Round 2: C+
- Mixed: B
- Session 3: A-/B+
- Session 4: A-
- Session 5: B-
- Session 6: B+/A-
- Session 7: B+
- **Session 8: B+**

### Key takeaways from this session
- Strong: YAGNI defense under pressure (decimal validator vs column widening)
- Strong: daily cap change = one file (separation of concerns proof)
- Weak: separation of concerns explanation — forgot the interface is the boundary (Redis swap = new repo class + DI registration, nothing else changes)
- Weak: defending exceptions vs Result — lead with "my errors are exceptional not expected" not "I prefer to throw"

### Rule: Never lead with "I prefer" or "the standard says." Lead with the practical reason.

---

# Session 9 — 30-question marathon

| Q# | Topic | Grade | Key Note |
|---|---|---|---|
| 1 | Dependency injection | B+ | Good — add "testability" to answer |
| 2 | abstract vs virtual | B- | virtual = has default, optional override. abstract = no body, must override |
| 3 | API versioning | F→coached | URL path (/v1/), query string, header. Lead with URL path for public APIs |
| 4 | yield return | B | Lazy iterator, produces one at a time. Add "not all in memory at once" |
| 5 | sync vs async | B+ | Async for I/O (releases thread), unnecessary for CPU-bound |
| 6 | record positional vs property | F→coached | Positional = constructor params, all required. Property = body with init, supports defaults/JSON |
| 7 | Middleware short-circuit | B+ | Correct — not calling next(). Exception handler example |
| 8 | FirstOrDefault vs SingleOrDefault | D→coached | First = first match silently. Single = expects 0 or 1, throws on multiple |
| 9 | Technical debt | A | Intentional (migrations), inherited (hardcoded values, paid back). Active management |
| 10 | volatile keyword | F→coached | Don't cache in register, always read main memory. Almost never needed in modern C# |
| 11 | Task<T> vs ActionResult<T> | B+ | Task = always 200. ActionResult = controller decides status. Different endpoints, different needs |
| 12 | String interpolation perf | B- | Modern interpolation ≥ concat > Format. Readability matters more |
| 13 | 3 juniors joining | B | Branching, docs, code reviews. Add: branch protection, CI gate, pair programming |
| 14 | == vs Equals | C→coached | Reference types: == checks reference, Equals checks value (unless overloaded). Opposite of what you said |
| 15 | N+1 query problem | B+ | Correct — data loaded from cache before loops, all in-memory |
| 16 | IQueryable vs IEnumerable | C→coached | IQueryable = expression tree → SQL server-side. IEnumerable = all loaded, filter in C# |
| 17 | Observability | C | Right direction but vague. Three pillars: logs, metrics, traces |
| 18 | Deadlock | B | DB deadlock correct. App low-risk — short transactions, execution strategy retries |
| 19 | PUT vs PATCH | A- | Full replace vs partial. Don't need PATCH — granular endpoints cover it |
| 20 | using statement | A | Disposes after block. await using = async dispose |
| 21 | Monolith vs microservices | B- | Split triggers: team scaling, different scaling needs, deployment cadence, tech mismatch |
| 22 | in parameter modifier | B+ | Read-only reference. Avoids copy for large structs |
| 23 | Composition vs inheritance | B+ | Inherit for shared structure, compose for delegation. Entities inherit, services compose |
| 24 | Fail fast | B | Connection string example. Also: timezone resolution, input validation, checked cast |
| 25 | Task.Run vs await | C→coached | await = release thread (I/O). Task.Run = another thread (CPU). Never Task.Run in ASP.NET Core |
| 26 | Smoke vs blackbox tests | A- | Different stage, different depth. Smoke = deployment. Blackbox = correctness |
| 27 | Expression-bodied members | B | => replaces { return } for single expressions |
| 28 | Debug wrong fee | F→coached | Reproduce → config → timezone → toll-free → trace calc → cache → write test before fix |
| 29 | Open/Closed principle | B+ | Repository + config API examples. Extension without modification |
| 30 | Garbage collection | B | GC cleans heap. Correction: causes pauses not starvation. Gen2 = expensive, stops all threads |

### Session 9 Average: B

### Grade Distribution
- A / A-: 5 (Q9, Q19, Q20, Q26, Q30 post-coaching)
- B / B+: 14
- C / C-: 4
- D / F (needed coaching): 7

### Overall Trend
- Round 1: C+
- Round 2: C+
- Mixed: B
- Session 3: A-/B+
- Session 4: A-
- Session 5: B-
- Session 6: B+/A-
- Session 7: B+
- Session 8: B+
- **Session 9 (30Q marathon): B**

### Strengths confirmed
- Architecture and design decisions (YAGNI, separation of concerns, repository pattern)
- Your own code knowledge (middleware order, test layers, configuration flow)
- Practical reasoning over theoretical (PUT vs PATCH, smoke vs blackbox)

### Areas that still need study cards
- == vs Equals (opposite of what you think)
- IQueryable vs IEnumerable (server-side vs client-side)
- FirstOrDefault vs SingleOrDefault (silent vs throws)
- Task.Run vs await (almost never Task.Run in ASP.NET Core)
- Observability three pillars (logs + metrics + traces)
- GC generations (Gen0 fast, Gen2 expensive, pauses all threads)
