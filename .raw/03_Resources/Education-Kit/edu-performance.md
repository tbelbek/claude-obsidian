---
tags:
  - education-kit
---

# Performance Profiling & Optimization — Education Kit

## What Performance Profiling Is

Performance profiling is the systematic process of measuring where time and resources are spent in your application, identifying bottlenecks, and fixing them with targeted changes. The key principle: measure first, optimize second. Most performance 'fixes' that skip profiling are wasted effort on non-bottlenecks. A profiler tells you exactly where the problem is — without it, you're guessing.

## Framework

1. **Metrics** — What does the data say? Response times, throughput, error rates, resource utilization. If you can't measure it, you can't fix it.
2. **Profiling** — Where exactly is the time going? CPU profiling, memory profiling, database query analysis, network traces.
3. **Root cause** — Why is this slow? N+1 queries, missing index, GC pressure, thread pool starvation, network latency?
4. **Fix** — Targeted change to address the root cause. Not "add caching everywhere" — fix the actual problem.
5. **Verify** — Measure again with the same metrics. Did the fix work? Any regressions?

---

## .NET Profiling Tools

- **dotnet-counters** — Real-time monitoring of .NET runtime metrics. CPU usage, GC collections, thread pool queue length, exception count, HTTP request rates. First tool to reach for — lightweight, no overhead.
  ```
  dotnet-counters monitor --process-id <pid> --counters System.Runtime
  ```

- **dotnet-trace** — Collects detailed trace data (CPU sampling, events). Analyze with Visual Studio, PerfView, or Speedscope. Shows exactly which methods are consuming CPU time.
  ```
  dotnet-trace collect --process-id <pid> --duration 00:00:30
  ```

- **dotnet-dump** — Captures a memory dump for analysis. Use when you suspect memory leaks — shows object counts, sizes, and references.
  ```
  dotnet-dump collect --process-id <pid>
  dotnet-dump analyze <dump-file>
  > dumpheap -stat    # show objects by count and size
  > gcroot <address>  # find what's keeping an object alive
  ```

- **BenchmarkDotNet** — Micro-benchmarking framework. Use for comparing implementation options (string concat vs StringBuilder, LINQ vs for loop, Span vs array). Handles warmup, statistical analysis, and memory allocation reporting.

## Common Performance Problems

### N+1 Queries
- **What** — Loading a list of N items, then making 1 additional query per item to load related data. 10 users + their orders = 1 + 10 = 11 queries.
- **Symptoms** — Linear increase in response time as data grows. Database shows many small, similar queries.
- **Fix** — Eager loading (`Include()` in EF Core), batch loading (DataLoader in GraphQL), or manual JOIN query.

### Memory Leaks
- **Event handlers not unsubscribed** — Object subscribes to a static event or long-lived publisher. Object can't be GC'd because the publisher holds a reference.
- **Static collections growing unbounded** — `static Dictionary<string, object>` used as a cache without eviction. Grows until OOMKill.
- **IDisposable not disposed** — HttpClient, DbConnection, streams not disposed -> underlying resources leak. Use `using` statements.
- **Detection** — `dotnet-dump` -> `dumpheap -stat` shows accumulating types. `gcroot` shows why they can't be collected.

### GC Pressure
- **Boxing** — Passing value types to `object` parameters causes heap allocation per call.
- **String concatenation in loops** — Each `+` creates a new string object. Use `StringBuilder` or `string.Join`.
- **Large Object Heap (LOH)** — Objects > 85KB go on the LOH, collected less frequently and not compacted by default.
- **Fix** — Use `Span<T>` and `stackalloc` for hot paths. Pool objects with `ArrayPool<T>`. Reduce allocations in tight loops.

### Thread Pool Starvation (Sync-over-Async)
- **What** — Calling `.Result` or `.Wait()` on async methods blocks a thread pool thread. Under load, all threads get blocked, the app freezes.
- **Symptoms** — Thread pool queue length growing, response times spike, but CPU is low.
- **Fix** — Go async all the way. Never `.Result` or `.Wait()` in request-handling code.

### Connection Pool Exhaustion
- **What** — Database or HTTP connections are limited. If code doesn't dispose connections properly or holds them too long, the pool fills up.
- **Symptoms** — Timeout exceptions after periods of load. "Connection pool exhausted" errors.
- **Fix** — Always `using` on connections. Use `IHttpClientFactory`. Set reasonable pool sizes and timeouts.

## Database Performance

- **Execution plans** — `EXPLAIN ANALYZE` (PostgreSQL) or `SET STATISTICS IO ON` (SQL Server). Shows how the database actually executes the query. The single most important debugging tool for slow queries.
- **Missing indexes** — Table scan on a large table is the #1 cause of slow queries. But don't add indexes blindly — each index slows writes.
- **Parameter sniffing** — SQL Server caches query plans based on first parameter values. Fix: `OPTION (RECOMPILE)` for problematic queries, or `OPTIMIZE FOR` hints.
- **Lock contention** — Long-running transactions hold locks. Use short transactions, read-committed snapshot isolation.

## API Performance

- **Response time breakdown** — Total = network + server processing + database + external calls + serialization. Often 80% is in one database query or one external API call.
- **Serialization overhead** — `System.Text.Json` is 2-3x faster than `Newtonsoft.Json`. Use source generators for zero-reflection serialization.
- **Payload size** — Use pagination, field selection (GraphQL), compression (gzip/brotli).
- **Caching strategy** — Response caching (HTTP headers), data caching (Redis/MemoryCache), computed result caching. Cache invalidation is the hard part.

## Kubernetes Performance

- **Resource limits** — Set CPU and memory requests/limits on every pod. Without limits, one pod can starve others.
- **OOMKill** — Pod exceeds memory limit -> Kubernetes kills it. Fix: increase memory limit, fix the memory leak, or reduce memory usage.
- **CPU throttling** — Pod reaches CPU limit -> throttled, response times spike. Fix: increase CPU limit or optimize code.
- **Pod startup time** — Slow startup delays scaling. Use ReadyToRun compilation, minimize startup DI registrations. Target: pod ready in <10 seconds.
- **HPA** — Scale pods based on CPU, memory, or custom metrics. Set scale-up/scale-down policies to avoid thrashing.

---

## Common Questions

**"Walk me through how you debug a slow API endpoint."**
Check metrics — response time percentiles, throughput, error rate. Is it slow for all requests or specific ones? Break down response time: database, external API, computation, serialization? For database: check execution plans. For CPU: use `dotnet-trace`. For thread issues: `dotnet-counters` shows thread pool queue length.

**"How do you decide what to optimize?"**
Measure first — don't optimize what isn't slow. Look at p95/p99, not averages. Focus on the bottleneck. Consider impact: a 100ms improvement on a 10K/sec endpoint is more valuable than a 1s improvement on a 1/min endpoint. Use Amdahl's Law intuitively.

**"Have you dealt with memory leaks in production?"**
Pattern: monitoring shows memory growing over time. Take a memory dump, analyze with `dumpheap -stat` to find accumulating types. Then `gcroot` to find what's keeping them alive. Common causes: event handlers not unsubscribed, static collections without eviction, undisposed HttpClient instances.

**"How do you prevent performance regressions?"**
Three layers: BenchmarkDotNet tests for critical paths in CI, load testing in staging before production, and production monitoring with alerting on p95 response time.
