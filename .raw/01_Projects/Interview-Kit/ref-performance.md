---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Performance Profiling & Optimization — Quick Reference

> [!info] How I've used it: GraphQL N+1 fix (3s→200ms), Docker layer caching (10min→2min build), Redis scaling (frozen responses→sub-second). Systematic approach: metrics → profiling → root cause → fix → verify.

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#HOW WE USE IT\|my approach]] | metrics→profile→root cause→fix→verify | [[#.NET Profiling Tools\|.NET profiling]] | dotnet-counters, dotnet-trace, BenchmarkDotNet |
| [[#Common Performance Problems\|N+1 queries]] | GraphQL 3s→200ms with DataLoader at Combination | [[#Common Performance Problems\|memory leaks]] | undisposed connections, event handler leaks |
| [[#Common Performance Problems\|GC pressure]] | reduce allocations, Span\<T\>, ArrayPool, pooling | [[#Database Performance\|SQL perf]] | missing indexes, SELECT *, unbounded queries |
| [[#API Performance\|API perf]] | response compression, pagination, field selection | [[#Kubernetes Performance\|K8s perf]] | resource limits, HPA tuning, pod right-sizing |
| [[#How I Applied This\|real examples]] | Docker cache 10→2min, Redis GPS scaling, GraphQL N+1 | | |

## HOW WE USE IT

My approach to performance is systematic, not heroic. You don't guess — you measure, profile, identify the root cause, fix it, and verify the fix with the same measurement. Most performance "fixes" that skip profiling are wasted effort on non-bottlenecks.

**My framework:**
1. **Metrics** — What does the data say? Response times, throughput, error rates, resource utilization. If you can't measure it, you can't fix it.
2. **Profiling** — Where exactly is the time going? CPU profiling, memory profiling, database query analysis, network traces.
3. **Root cause** — Why is this slow? N+1 queries, missing index, GC pressure, thread pool starvation, network latency?
4. **Fix** — Targeted change to address the root cause. Not "add caching everywhere" — fix the actual problem.
5. **Verify** — Measure again with the same metrics. Did the fix work? Any regressions?

**Real examples from my experience:**
- **GraphQL N+1 fix at Combination** — One endpoint took 3 seconds, made 11 database calls. Added DataLoader for batching, reduced to 2 calls, response time dropped to 200ms. *(see [[ref-graphql]])*
- **Docker build optimization at Combination** — Builds took 10 minutes because layer caching was broken (COPY . . too early invalidated everything). Reordered Dockerfile: copy .csproj first, restore, then copy source. Build time: 2 minutes. *(see [[ref-docker]])*
- **Redis scaling at Combination** — Certain endpoints froze under load. Profiled and found synchronous Redis calls blocking the thread pool. Switched to async Redis operations + connection multiplexing. Response times went from frozen (timeouts) to sub-second.

---

## Key Concepts

### What Performance Profiling Is

Performance profiling is the systematic process of measuring where time and resources are spent in your application, identifying bottlenecks, and fixing them with targeted changes. The key principle: measure first, optimize second. Most performance 'fixes' that skip profiling are wasted effort on non-bottlenecks. A profiler tells you exactly where the problem is — without it, you're guessing.

### .NET Profiling Tools

- **dotnet-counters** — Real-time monitoring of .NET runtime metrics. CPU usage, GC collections, thread pool queue length, exception count, HTTP request rates. First tool to reach for — lightweight, no overhead, tells you where to look deeper.
  ```
  dotnet-counters monitor --process-id <pid> --counters System.Runtime
  ```

- **dotnet-trace** — Collects detailed trace data (CPU sampling, events) into a .nettrace file. Analyze with Visual Studio, PerfView, or Speedscope. Shows exactly which methods are consuming CPU time.
  ```
  dotnet-trace collect --process-id <pid> --duration 00:00:30
  ```

- **dotnet-dump** — Captures a memory dump for analysis. Use when you suspect memory leaks — shows object counts, sizes, and references. Analyze with `dotnet-dump analyze`.
  ```
  dotnet-dump collect --process-id <pid>
  dotnet-dump analyze <dump-file>
  > dumpheap -stat    # show objects by count and size
  > gcroot <address>  # find what's keeping an object alive
  ```

- **BenchmarkDotNet** — Micro-benchmarking framework for .NET. Use for comparing implementation options (string concat vs StringBuilder, LINQ vs for loop, Span vs array). Handles warmup, statistical analysis, and memory allocation reporting. Don't use for end-to-end performance — use for isolated method comparisons.

### Common Performance Problems

#### N+1 Queries
- **What** — Loading a list of N items, then making 1 additional query per item to load related data. 10 users + their orders = 1 + 10 = 11 queries.
- **Symptoms** — Linear increase in response time as data grows. Database shows many small, similar queries.
- **Fix** — Eager loading (`Include()` in EF Core), batch loading (DataLoader in GraphQL), or manual JOIN query. At Combination, this was the single biggest performance win — 11 queries → 2 batched queries, 3s → 200ms.

#### Memory Leaks
- **Event handlers not unsubscribed** — Object subscribes to a static event or long-lived publisher. Object can't be GC'd because the publisher holds a reference. Classic in .NET desktop apps, also happens in services with event buses.
- **Static collections growing unbounded** — `static Dictionary<string, object>` used as a cache without eviction. Grows until OOMKill.
- **IDisposable not disposed** — HttpClient, DbConnection, streams not disposed → underlying resources leak. Use `using` statements, DI container manages lifetime.
- **Detection** — `dotnet-dump` → `dumpheap -stat` shows which types are accumulating. `gcroot` shows why they can't be collected.

#### GC Pressure
- **Boxing** — Passing value types to `object` parameters causes heap allocation per call. Common with non-generic collections or `string.Format` with value types.
- **String concatenation in loops** — Each `+` creates a new string object. 1000 iterations = 1000 allocations. Use `StringBuilder` or `string.Join`.
- **Large Object Heap (LOH)** — Objects > 85KB go on the LOH, which is collected less frequently and not compacted by default. Arrays and large strings are common culprits.
- **Fix** — Use `Span<T>` and `stackalloc` for hot paths. Pool objects with `ArrayPool<T>`. Reduce allocations in tight loops. `dotnet-counters` shows GC collection rates — Gen 0 collections >10/sec is a warning sign.

#### Thread Pool Starvation (Sync-over-Async)
- **What** — Calling `.Result` or `.Wait()` on async methods blocks a thread pool thread. Under load, all threads get blocked waiting, new requests queue up, the app freezes.
- **Symptoms** — `dotnet-counters` shows thread pool queue length growing, response times spike, but CPU is low.
- **Fix** — Go async all the way. Never `.Result` or `.Wait()` in request-handling code. If you must call async from sync (legacy code), use `Task.Run()` as a last resort (it wastes a thread but doesn't block the request thread).

#### Connection Pool Exhaustion
- **What** — Database or HTTP connections are limited. If code doesn't dispose connections properly or holds them too long, the pool fills up and new requests wait or fail.
- **Symptoms** — Timeout exceptions after periods of load. "Connection pool exhausted" errors.
- **Fix** — Always `using` on connections. Use `IHttpClientFactory` (not `new HttpClient()`). Set reasonable pool sizes and timeouts. Monitor active connections with `dotnet-counters`.

### Database Performance

- **Execution plans** — `EXPLAIN ANALYZE` (PostgreSQL) or `SET STATISTICS IO ON` (SQL Server). Shows how the database actually executes the query — table scans vs index seeks, estimated vs actual rows. The single most important debugging tool for slow queries. *(see [[ref-sql-databases]])*
- **Missing indexes** — Table scan on a large table is the #1 cause of slow queries. Check execution plans for Seq Scan / Table Scan. But don't add indexes blindly — each index slows writes and uses storage.
- **Parameter sniffing** — SQL Server caches query plans based on the first parameter values. If the first call has atypical values, the cached plan may be terrible for typical calls. Fix: `OPTION (RECOMPILE)` for problematic queries, or use `OPTIMIZE FOR` hints. *(see [[ref-sql-databases]])*
- **Lock contention** — Long-running transactions hold locks that block other queries. Use short transactions, read-committed snapshot isolation, and avoid `SELECT ... FOR UPDATE` unless necessary.

### API Performance

- **Response time breakdown** — Total response time = network + server processing + database + external calls + serialization. Profile each component to find the bottleneck. Often 80% of time is in one database query or one external API call.
- **Serialization overhead** — `System.Text.Json` is 2-3x faster than `Newtonsoft.Json` for serialization. Use source generators for AOT-friendly, zero-reflection serialization. For large payloads, consider streaming serialization.
- **Payload size** — Large JSON responses slow down network transfer and client parsing. Use pagination, field selection (GraphQL), compression (gzip/brotli), and avoid returning data the client doesn't need.
- **Caching strategy** — Response caching (HTTP cache headers), data caching (Redis/MemoryCache), computed result caching. Cache invalidation is the hard part — use time-based expiry as the simplest approach, event-based invalidation for consistency.

### Kubernetes Performance

- **Resource limits** — Set CPU and memory requests/limits on every pod. Without limits, one pod can starve others. Without requests, the scheduler can't make good decisions.
- **OOMKill** — Pod exceeds memory limit → Kubernetes kills it. Check `kubectl describe pod` for OOMKilled status. Fix: increase memory limit, fix the memory leak, or reduce memory usage (smaller caches, streaming instead of buffering).
- **CPU throttling** — Pod reaches CPU limit → Kubernetes throttles it. Response times spike but the pod stays alive. `dotnet-counters` shows high CPU but `kubectl top pod` shows it capped at the limit. Fix: increase CPU limit or optimize code.
- **Pod startup time** — Slow startup delays scaling and rolling deployments. .NET apps: use ReadyToRun compilation, minimize startup DI registrations, defer non-essential initialization. Target: pod ready in <10 seconds.
- **Horizontal Pod Autoscaler (HPA)** — Scale pods based on CPU, memory, or custom metrics (QPS, queue depth). Set scale-up/scale-down policies to avoid thrashing. *(see [[ref-kubernetes]])*

---

## How I Applied This

> [!info] Real debugging stories from production systems.

**GraphQL N+1 — Combination:**
One endpoint loaded a list of entities and for each entity made a separate database call to fetch related data. 10 entities = 11 queries, 100 entities = 101 queries. Response time grew linearly with data size. Identified using query logging — saw the pattern of repeated similar queries. Fixed with HotChocolate DataLoader that batches all IDs and fetches in one query. Result: 11 queries → 2 queries, 3 seconds → 200ms.

**Docker Layer Caching — Combination:**
CI builds for 60+ services took 10 minutes each. The Dockerfile had `COPY . .` before `dotnet restore`, so every source code change invalidated the dependency restore cache. Reordered: copy only `.csproj` files first, run `dotnet restore` (cached unless dependencies change), then copy source and build. Build time dropped to 2 minutes. Across 60+ services, this saved hours of CI time per day.

**Redis Sync-over-Async — Combination:**
Certain API endpoints froze under moderate load. CPU was low, but response times spiked to timeouts. Profiled with `dotnet-counters` — thread pool queue length was growing, meaning threads were blocked. Found synchronous Redis calls (`.Result` on async methods) in the hot path. The thread pool ran out of threads, and new requests queued up. Fixed by switching to fully async Redis operations and enabling connection multiplexing in StackExchange.Redis. Response times went from timeouts to sub-second.

---

## Sorulursa

> [!faq]- "Walk me through how you debug a slow API endpoint."
> First, I check the metrics — response time percentiles (p50, p95, p99), throughput, error rate. Is it slow for all requests or specific ones? Then I break down the response time: is it database, external API, computation, or serialization? For database: check execution plans, look for table scans or N+1 patterns. For CPU: use `dotnet-trace` to find hot methods. For thread issues: `dotnet-counters` shows thread pool queue length. At Combination, the GraphQL N+1 fix started with noticing linear response time growth in our monitoring dashboard, then query logging revealed 11 similar queries per request.

> [!faq]- "How do you decide what to optimize?"
> Measure first — don't optimize what isn't slow. Look at p95/p99 response times, not averages (averages hide outliers). Focus on the bottleneck — if 80% of response time is one database query, optimizing serialization is wasted effort. Consider impact: a 100ms improvement on an endpoint called 10K times/second is more valuable than a 1-second improvement on an endpoint called once per minute. I use Amdahl's Law intuitively — the maximum speedup is limited by the fraction of time spent in the part you're optimizing.

> [!faq]- "Have you dealt with memory leaks in production?"
> Yes. The pattern is always: monitoring shows memory growing over time (saw-tooth pattern disappears, just grows). Take a memory dump with `dotnet-dump`, analyze with `dumpheap -stat` to find which object types are accumulating. Then `gcroot` to find what's keeping them alive. Common causes: event handlers not unsubscribed (object can't be GC'd because the event publisher holds a reference), static collections growing without eviction, undisposed HttpClient instances. The fix is always about breaking the reference chain — unsubscribe events, use weak references, implement proper IDisposable.

> [!faq]- "How do you prevent performance regressions?"
> Three layers. First, BenchmarkDotNet tests for critical hot paths — run in CI, alert if performance degrades beyond a threshold. Second, load testing in staging before production deployments — compare response times and resource usage against the baseline. Third, production monitoring with alerting — p95 response time exceeding SLO triggers an alert before users notice. At Combination, we caught the Redis sync-over-async issue because our monitoring showed thread pool queue length growing under load — a metric most teams don't watch but is critical for async .NET applications.

---

*[[00-dashboard]]*
