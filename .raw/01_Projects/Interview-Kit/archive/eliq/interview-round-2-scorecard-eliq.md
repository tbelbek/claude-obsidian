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
