---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# C# / .NET — Senior Interview Questions

> [!tip] Quick review before interview. Answers are 2-3 sentences — enough to show you know it, detailed enough to survive a follow-up.

## Quick Scan — Ctrl+F This

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Q1. What is the difference between value types and reference types?\|value vs reference]] | stack vs heap, copy vs pointer | [[#Q2. When would you choose `struct` over `class`?\|struct vs class]] | struct: small, immutable, stack. class: heap, reference |
| [[#Q3. What is boxing and unboxing, and why does it matter?\|boxing]] | value→object heap allocation, avoid in loops | [[#Q4. What are nullable reference types (NRT)?\|nullable ref types]] | compile-time null analysis, not runtime |
| [[#Q5b. What is the difference between `string` and `StringBuilder`?\|string vs StringBuilder]] | immutable vs mutable buffer, loop→SB | [[#Q5c. Explain `sealed`, `abstract`, and `virtual` keywords.\|sealed/abstract/virtual]] | abstract=must override, virtual=can override, sealed=no override |
| [[#Q5d. What is the difference between `interface` and `abstract class` in modern C#?\|interface vs abstract class]] | interface=contract, abstract=shared state+behavior | [[#Q6. What happens under the hood when you `await` a Task?\|async state machine]] | compiler generates IAsyncStateMachine, captures locals |
| [[#Q7. What is the difference between `Task` and `ValueTask`?\|Task vs ValueTask]] | Task=heap, ValueTask=struct for sync paths | [[#Q8. When should you use `ConfigureAwait(false)`?\|ConfigureAwait(false)]] | skip SyncContext capture, use in libraries |
| [[#Q9. How do async deadlocks occur?\|async deadlock]] | .Result blocks SyncContext thread | [[#Q10. What is the danger of `async void`?\|async void]] | fire-and-forget, crashes on exception, only for events |
| [[#Q11. What is `Task.WhenAll` vs `Task.WhenAny` and when do you use each?\|WhenAll vs WhenAny]] | all=fan out parallel, any=timeout/race | [[#Q11b. What is `SemaphoreSlim` and when do you use it?\|SemaphoreSlim]] | async-friendly concurrency limiter |
| [[#Q11c. Explain `Channel<T>` and producer-consumer pattern in .NET.\|Channel\<T\>]] | async producer-consumer queue with backpressure | [[#Q11d. What is the difference between `Task` and `await`?\|Task vs await]] | Task=the promise, await=wait for it |
| [[#Q11e. What is the difference between `Task.Run` and `await`?\|Task.Run vs await]] | Run=CPU offload, await=I/O wait | [[#Q11f. Can you return `Task` without `async`?\|return Task without async]] | skip state machine for pass-through |
| [[#Q12. What is deferred (lazy) execution in LINQ?\|deferred execution]] | LINQ doesn't run until enumerated | [[#Q13. What is the difference between `IEnumerable<T>` and `IQueryable<T>`?\|IQueryable vs IEnumerable]] | IQueryable=DB query, IEnumerable=in-memory |
| [[#Q14. What does `AsNoTracking()` do and when should you use it?\|AsNoTracking]] | read-only queries skip change tracking | [[#Q16b. What is the difference between `Select` and `SelectMany`?\|Select vs SelectMany]] | 1:1 map vs 1:many flatten |
| [[#Q16c. How does `GroupBy` work and what are its performance implications?\|GroupBy]] | loads all into memory, not streaming | [[#Q17. Explain the three DI service lifetimes in ASP.NET Core.\|DI lifetimes]] | singleton/scoped/transient, captive dependency bug |
| [[#Q19. How do you resolve a scoped service inside a singleton?\|IServiceScopeFactory]] | create scoped service inside singleton | [[#Q20. What is `IOptions<T>` vs `IOptionsSnapshot<T>` vs `IOptionsMonitor<T>`?\|IOptions variants]] | IOptions=singleton, IOptionsSnapshot=scoped, IOptionsMonitor=singleton+change |
| [[#Q21. How does the .NET GC work with generations?\|GC generations]] | Gen0=short-lived, Gen1=survived, Gen2=long-lived | [[#Q22. What is `IDisposable` and when must you implement it?\|IDisposable]] | using statement, deterministic cleanup |
| [[#Q25c. Explain `Span<T>` and `Memory<T>` — when do you use which?\|Span\<T\> vs Memory\<T\>]] | Span=stack-only zero-copy, Memory=heap-friendly | [[#Q25b. What is `ArrayPool<T>` and when should you use it?\|ArrayPool]] | rent/return arrays, avoid GC in hot paths |
| [[#Q26. How does `Dictionary<TKey, TValue>` work internally?\|Dictionary internals]] | hash buckets + chaining, O(1) average | [[#Q27. What is `ConcurrentDictionary` and when do you use it?\|ConcurrentDictionary]] | thread-safe, lock-free reads, striped locks for writes |
| [[#Q30. What are `record` types and when should you use them?\|records]] | immutable data, value equality, with-expression | [[#Q31. How does pattern matching improve code in C# 10-12?\|pattern matching]] | switch expressions, is pattern, property pattern |
| [[#Q32. What are primary constructors (C# 12)?\|primary constructors]] | DI injection without boilerplate fields | [[#Q35. How does the middleware pipeline work?\|middleware pipeline]] | chain of responsibility, order matters |
| [[#Q37. How do health checks work in ASP.NET Core?\|health checks]] | liveness/readiness/startup probes | [[#Q39b. Explain Minimal APIs vs Controllers — when do you use which?\|Minimal APIs vs Controllers]] | lambda vs full MVC, perf vs features |
| [[#Q39c. How does the configuration system work in ASP.NET Core?\|config system]] | layered: json→env→args→secrets→KeyVault | [[#Common Interview Code Snippets\|async void (code smell)]] | crashes process, use Task instead |
| [[#Common Interview Code Snippets\|captured loop var]] | all lambdas share same i, use local | [[#Common Interview Code Snippets\|DI lifetime mismatch]] | scoped in singleton = captured dependency |
| [[#Q51. What are `FrozenDictionary` and `FrozenSet` and how do they differ from `ReadOnlyDictionary`?\|FrozenDictionary]] | read-optimized immutable, 40-70% faster lookup | [[#Q53. What is `TimeProvider` in .NET 8 and why does it matter for testing?\|TimeProvider]] | testable time abstraction, replaces IClock |
| [[#Q55. What is `HybridCache` in .NET 9 and how does it prevent cache stampedes?\|HybridCache]] | L1+L2 cache with stampede protection | [[#Q57. How does `IAsyncEnumerable<T>` work and when should you use it?\|IAsyncEnumerable]] | stream results one-by-one, no buffering |
| [[#Q63. How do source generators work in the compilation pipeline?\|source generators]] | compile-time code gen, IIncrementalGenerator | [[#Q66. How does `[LoggerMessage]` improve performance?\|LoggerMessage]] | zero-boxing structured logging via source gen |
| [[#Q71. What are EF Core compiled queries and when should you use them?\|compiled queries]] | pre-compiled LINQ→SQL, 40% faster | [[#Q73. What are EF Core bulk operations and how do `ExecuteUpdate`/`ExecuteDelete` work?\|bulk operations]] | single SQL, no change tracking |
| [[#Q81. How does gRPC differ from REST in .NET and when do you choose each?\|gRPC vs REST]] | HTTP/2+protobuf internal, REST external | [[#Q85. How does SignalR scale across multiple server instances?\|SignalR scaling]] | Redis backplane or Azure SignalR Service |
| [[#Q88. What is the difference between `IHostedService` and `BackgroundService`?\|background services]] | IHosted=hooks, Background=long-running loop | [[#Q92. What is the difference between convention-based middleware and `IMiddleware`?\|middleware types]] | convention=singleton, IMiddleware=scoped DI |

---

## Language Fundamentals

### Q1. What is the difference between value types and reference types?
Value types (int, bool, struct, enum) live on the stack and hold data directly; reference types (class, string, array, delegate) live on the heap and hold a pointer. When you assign a value type you get a copy; when you assign a reference type you copy the pointer, so both variables reference the same object.

### Q2. When would you choose `struct` over `class`?
Use struct for small, immutable data containers (under ~16 bytes) that are created frequently and have short lifetimes — like a `Coordinate` or `Money` type. In microservices this matters for hot-path DTOs inside gRPC serializers or GraphQL resolvers where reducing heap allocations lowers GC pressure.

### Q3. What is boxing and unboxing, and why does it matter?
Boxing wraps a value type in a heap-allocated `object`; unboxing extracts it back. Each box is a heap allocation + copy, so boxing in a tight loop (e.g., passing `int` to a `Dictionary<string, object>`) kills throughput. Generic collections eliminated most accidental boxing.

### Q4. What are nullable reference types (NRT)?
Enabled via `<Nullable>enable</Nullable>`, NRT is a compile-time analysis that flags potential null dereferences with warnings. It does not prevent nulls at runtime — it is a contract enforced by the compiler. In microservices, enabling NRT catches null-related bugs early in shared DTOs and domain models.

### Q5. What is the `default` keyword and how does it behave for value vs reference types?
`default` returns `0` / `false` / `'\0'` for value types and `null` for reference types. With NRT enabled, `default` on a non-nullable reference type triggers a warning, which is useful for catching uninitialized fields in DI-registered services.

### Q5b. What is the difference between `string` and `StringBuilder`?
`string` is immutable — every concatenation creates a new string object on the heap. In a loop with 1000 iterations, that's 1000 allocations. `StringBuilder` uses a mutable buffer and appends in-place. Rule: if you're concatenating in a loop or building a string dynamically, use `StringBuilder`. For 2-3 concatenations, `string` is fine — the overhead of `StringBuilder` isn't worth it.

### Q5c. Explain `sealed`, `abstract`, and `virtual` keywords.
`abstract` — class can't be instantiated, must be inherited. Methods have no body, must be overridden. `virtual` — method has a default implementation but can be overridden by derived classes. `sealed` — prevents a class from being inherited or a method from being overridden further. Sealing can improve performance slightly because the JIT can devirtualize calls. In microservices, you rarely seal classes but you might seal specific methods to prevent unexpected behavior in derived types.

### Q5d. What is the difference between `interface` and `abstract class` in modern C#?
Interfaces define contracts with no state (until C# 8 default implementations). Abstract classes can have state (fields), constructors, and partial implementations. Since C# 8, interfaces can have default method implementations, blurring the line. Rule of thumb: interface for "what it can do" (multiple inheritance), abstract class for "what it is" (shared state/behavior). In DI-heavy architectures, interfaces are preferred for testability — you mock `IRepository`, not `AbstractRepository`.

---

## Async / Await

### Q6. What happens under the hood when you `await` a Task?
The compiler generates a state machine (implementing `IAsyncStateMachine`) that captures local variables, registers a continuation, and yields control back to the caller. When the awaited task completes, the continuation resumes on the captured `SynchronizationContext` (or the thread pool if none exists).

### Q7. What is the difference between `Task` and `ValueTask`?
`Task` always allocates on the heap. `ValueTask` is a struct that avoids allocation when the result is available synchronously — ideal for cache-hit paths in microservices. However, a `ValueTask` must never be awaited more than once or stored for later consumption; violating this causes undefined behavior.

### Q8. When should you use `ConfigureAwait(false)`?
In library code and backend services without a `SynchronizationContext` (ASP.NET Core has none by default), `ConfigureAwait(false)` avoids capturing context and allows continuations on any thread pool thread. It is critical in shared NuGet packages that might be consumed by UI apps or legacy ASP.NET.

### Q9. How do async deadlocks occur?
Classic deadlock: calling `.Result` or `.Wait()` on an async method that captures a single-threaded `SynchronizationContext` (WPF, legacy ASP.NET). The continuation needs the context thread, but `.Result` blocks it. In ASP.NET Core this specific deadlock does not happen (no SyncContext), but `.Result` still blocks a thread pool thread and can cause thread starvation under load.

### Q10. What is the danger of `async void`?
`async void` methods are fire-and-forget: exceptions cannot be caught by the caller and instead crash the process via `TaskScheduler.UnobservedTaskException`. Only use `async void` for event handlers. In ASP.NET Core, an `async void` action method will return before the work completes, causing silent data loss.

### Q11. What is `Task.WhenAll` vs `Task.WhenAny` and when do you use each?
`WhenAll` waits for all tasks and aggregates exceptions — use it to fan out parallel calls to downstream microservices. `WhenAny` returns when the first task completes — use it for timeout patterns or racing a cache lookup against a database call.

### Q11b. What is `SemaphoreSlim` and when do you use it?
`SemaphoreSlim` limits concurrent access to a resource. Unlike `lock`, it works with async code. Example: limiting concurrent database connections or rate-limiting outgoing HTTP calls. `await semaphore.WaitAsync()` to enter, `semaphore.Release()` to exit. In microservices, use it to prevent one service from overwhelming a downstream dependency.

### Q11d. What is the difference between `Task` and `await`?
`Task` is the object — it represents an asynchronous operation that may or may not have completed. You can hold it, pass it around, check `IsCompleted`, combine it with `WhenAll`. `await` is the operator — it unwraps a `Task`, suspends the method until the task completes, and returns the result. Without `await`, the task runs but your code continues immediately (fire-and-forget — dangerous because exceptions are swallowed). Without `Task`, there's nothing to `await`. Think of it as: `Task` = the promise, `await` = waiting for the promise to resolve. Common mistake: calling an async method without `await` — the task runs in the background, nobody checks for errors, and the bug is silent.

### Q11e. What is the difference between `Task.Run` and `await`?
`Task.Run` pushes work to a thread pool thread — use it for CPU-bound work you want to offload from the current thread. `await` doesn't create a new thread — it suspends the current method and resumes when the I/O completes. For I/O-bound work (database calls, HTTP requests), just `await` the async method directly — don't wrap it in `Task.Run`, that wastes a thread pool thread waiting for I/O. Rule: `await` for I/O, `Task.Run` for CPU.

### Q11f. Can you return `Task` without `async`?
Yes. If you're just passing through another async call without doing anything after it, skip `async/await` and return the `Task` directly: `return _service.GetDataAsync()` instead of `return await _service.GetDataAsync()`. This avoids the state machine overhead. But if you need a try/catch or a using block, you must use `async/await` because the state machine handles the cleanup.

### Q11c. Explain `Channel<T>` and producer-consumer pattern in .NET.
`Channel<T>` is a thread-safe, bounded or unbounded queue for async producer-consumer scenarios. Producer writes with `channel.Writer.WriteAsync()`, consumer reads with `channel.Reader.ReadAllAsync()`. Backpressure is built in for bounded channels — producer blocks when the channel is full. We use this pattern for background processing — incoming requests write to a channel, a background worker processes them sequentially.

---

## LINQ

### Q12. What is deferred (lazy) execution in LINQ?
LINQ queries using `Select`, `Where`, `OrderBy` etc. are not executed when declared — they execute when iterated (foreach, `ToList()`, `First()`). This means calling `.Where(...)` on an `IQueryable` merely builds an expression tree; the SQL is only generated and sent to the database when you materialize the result.

### Q13. What is the difference between `IEnumerable<T>` and `IQueryable<T>`?
`IEnumerable<T>` evaluates in-memory using delegates (LINQ-to-Objects). `IQueryable<T>` builds expression trees that a provider (EF Core, MongoDB driver) translates to a query language and executes server-side. Returning `IEnumerable<T>` from a repository when you meant `IQueryable<T>` pulls the entire table into memory before filtering.

### Q14. What does `AsNoTracking()` do and when should you use it?
It tells EF Core to skip the change tracker for the returned entities, reducing memory and CPU overhead. Use it for read-only queries in microservices (GraphQL resolvers, read endpoints) where you never intend to call `SaveChanges()`.

### Q15. What is the risk of multiple enumeration?
If you enumerate an `IEnumerable<T>` backed by a database query twice, the query runs twice. ReSharper/Rider flags this. Fix by materializing to a list first or restructuring the code to enumerate once.

### Q16. Name three LINQ operators that cause immediate execution.
`ToList()`, `Count()`, `First()`, `Single()`, `Any()`, `Aggregate()`, and `ToDictionary()` all force immediate execution. In performance-critical code, prefer `Any()` over `Count() > 0` because `Any()` can short-circuit after the first match.

### Q16b. What is the difference between `Select` and `SelectMany`?
`Select` maps each element to one output (1:1). `SelectMany` maps each element to a collection and flattens the result (1:many). Example: `orders.Select(o => o.Items)` returns `IEnumerable<List<Item>>`. `orders.SelectMany(o => o.Items)` returns `IEnumerable<Item>` — flat list. Equivalent to nested foreach loops.

### Q16c. How does `GroupBy` work and what are its performance implications?
`GroupBy` collects all elements by a key function into groups. Each group is an `IGrouping<TKey, TElement>`. Warning: it needs to enumerate the entire source to group — it's not streaming. For large datasets, this means loading everything into memory. In database queries (IQueryable), GroupBy translates to SQL GROUP BY which the database handles efficiently.

---

## Dependency Injection

### Q17. Explain the three DI service lifetimes in ASP.NET Core.
**Transient** — new instance every time it is requested; use for lightweight stateless services. **Scoped** — one instance per HTTP request; the standard choice for `DbContext`. **Singleton** — one instance for the app's lifetime; use for caches, `HttpClient` factories, configuration wrappers.

### Q18. What is the "captive dependency" problem?
A singleton service that injects a scoped or transient dependency "captures" it, keeping it alive beyond its intended lifetime. Classic bug: a singleton service holding a scoped `DbContext` means all requests share the same context, causing concurrency exceptions and stale data. ASP.NET Core throws at startup if `ValidateScopes` is enabled.

### Q19. How do you resolve a scoped service inside a singleton?
Inject `IServiceScopeFactory`, create a scope, and resolve the service within that scope. This is common in background services (`IHostedService`) that need a `DbContext` per iteration.

### Q20. What is `IOptions<T>` vs `IOptionsSnapshot<T>` vs `IOptionsMonitor<T>`?
`IOptions<T>` is singleton — read once at startup. `IOptionsSnapshot<T>` is scoped — re-reads config per request (useful for feature flags from ConfigMap). `IOptionsMonitor<T>` is singleton but pushes change notifications — ideal for hot-reloading Kubernetes ConfigMaps without restarting the pod.

---

## Memory Management

### Q21. How does the .NET GC work with generations?
GC uses three generations: Gen0 (short-lived, collected most frequently), Gen1 (buffer between short and long-lived), Gen2 (long-lived objects, collected rarely and expensively). Allocating many objects that survive into Gen2 (e.g., large caches) increases full GC pauses. In containerized microservices, GC pauses can trip health check timeouts.

### Q22. What is `IDisposable` and when must you implement it?
Implement `IDisposable` when your class holds unmanaged resources (file handles, DB connections, sockets) or wraps other `IDisposable` objects. The `using` statement (or `await using` for `IAsyncDisposable`) guarantees `Dispose()` is called even if an exception occurs. Forgetting to dispose `HttpClient` causes socket exhaustion — use `IHttpClientFactory` instead.

### Q23. What is `Span<T>` and why is it important for performance?
`Span<T>` is a stack-allocated, ref-like struct that provides a memory-safe view over contiguous memory (arrays, strings, native buffers) without copying. It enables zero-allocation parsing and slicing — e.g., parsing a large JSON payload from a gRPC stream without allocating substrings. `Span<T>` cannot be stored on the heap (no fields, no async methods); use `Memory<T>` when you need heap storage.

### Q24. How do memory leaks happen in managed .NET code?
Common causes: event handler subscriptions that are never removed, static collections that grow unbounded, closures capturing large objects, un-disposed `CancellationTokenSource`, and long-lived `HttpMessageHandler` instances. In microservices, a slow memory leak eventually triggers the Kubernetes OOMKilled event, so monitoring RSS and GC metrics via Prometheus is essential.

### Q25. What is the Large Object Heap (LOH)?
Objects >= 85,000 bytes go to the LOH, which is collected only during Gen2 collections and is not compacted by default (causes fragmentation). Use `ArrayPool<T>` to rent/return large buffers instead of allocating new arrays. Enable LOH compaction via `GCSettings.LargeObjectHeapCompactionMode` only when you understand the pause cost.

### Q25b. What is `ArrayPool<T>` and when should you use it?
`ArrayPool<T>.Shared.Rent(size)` borrows an array from a pool instead of allocating. You return it with `.Return(array)`. Use it for temporary buffers in hot paths — reading streams, serialization, byte processing. Avoids GC pressure from frequent array allocations. Critical in gRPC/GraphQL resolvers that process many requests per second. The rented array may be larger than requested — always use the requested size, not `array.Length`.

### Q25c. Explain `Span<T>` and `Memory<T>` — when do you use which?
`Span<T>` is a stack-only view over contiguous memory — arrays, strings, native memory. Zero-copy slicing. Can't be stored on the heap (no async, no closures, no class fields). `Memory<T>` is the heap-friendly version — can be passed to async methods. Use `Span<T>` in synchronous hot paths (parsers, serializers). Use `Memory<T>` when you need to pass the slice to async code.

---

## Collections

### Q26. How does `Dictionary<TKey, TValue>` work internally?
It uses a hash table with separate chaining. Keys are hashed via `GetHashCode()`, modded into a bucket array, and collisions are resolved by chaining in a linked list. A poor `GetHashCode()` (e.g., always returns 0) degrades lookups from O(1) to O(n). Always override `GetHashCode()` and `Equals()` together.

### Q27. What is `ConcurrentDictionary` and when do you use it?
It is a thread-safe dictionary using fine-grained locking (lock striping, not a single lock). Use it for shared caches in singleton services. Prefer `GetOrAdd` and `AddOrUpdate` over manual lock-then-check patterns. The factory delegate in `GetOrAdd` can execute multiple times under contention — it must be side-effect-free.

### Q28. What are `FrozenDictionary` and `FrozenSet` (.NET 8+)?
They are read-only collections optimized for lookup speed at the cost of expensive one-time construction. Ideal for configuration data, routing tables, or permission maps loaded once at startup in a microservice and queried millions of times.

### Q29. When should you use `ReadOnlySpan<T>` vs `ReadOnlyMemory<T>`?
`ReadOnlySpan<T>` for synchronous, stack-only slicing (parsing headers, splitting strings). `ReadOnlyMemory<T>` when you need to store the slice in a field or pass it across an `await` boundary. In gRPC interceptors, use `ReadOnlySequence<byte>` for zero-copy reading of large streaming messages.

---

## Modern C# (10-12)

### Q30. What are `record` types and when should you use them?
Records provide value-based equality, immutability by default, and compiler-generated `ToString()`, `Equals()`, `GetHashCode()`, and deconstruction. Use `record class` for DTOs, domain events, CQRS commands/queries. Use `record struct` for small value-type DTOs on hot paths.

### Q31. How does pattern matching improve code in C# 10-12?
Pattern matching replaces verbose if-else chains with concise `switch` expressions. You can combine type patterns, property patterns, relational patterns (`> 0 and < 100`), and list patterns (`[_, .., var last]`). Practical use: validating gRPC request fields or mapping GraphQL resolver inputs to domain commands.

### Q32. What are primary constructors (C# 12)?
Primary constructors let you declare constructor parameters directly on the class/struct declaration (`class OrderService(IOrderRepository repo)`). Parameters are captured as fields implicitly. Reduces boilerplate in DI-heavy microservice classes, but be aware they generate a hidden field — do not mutate captured parameters.

### Q33. What are collection expressions (C# 12)?
Syntax like `int[] nums = [1, 2, 3];` or `List<string> tags = ["api", "grpc"];` replaces verbose initializer syntax. The spread operator `..` merges collections: `[..baseHeaders, ..customHeaders]`. Compiled to optimal code (stackalloc for small spans).

### Q34. What are file-scoped namespaces and global usings?
`namespace MyService.Api;` (no braces) saves one indentation level per file. `global using System.Text.Json;` in a single file applies the using to every file in the project, reducing repetitive imports across a microservice codebase.

---

## ASP.NET Core

### Q35. How does the middleware pipeline work?
Middleware components form a request/response pipeline. Each component calls `next(context)` to pass to the next middleware or short-circuits by not calling it. Order matters: `UseAuthentication()` must come before `UseAuthorization()`. Custom middleware is ideal for cross-cutting concerns like correlation ID propagation across microservices.

### Q36. What are Minimal APIs and when would you choose them over controllers?
Minimal APIs define endpoints as lambdas in `Program.cs` with less ceremony and slightly better performance (fewer allocations). Choose them for lightweight microservices, health endpoints, or BFF APIs. Use controllers when you need complex model binding, filters, or API versioning across many endpoints.

### Q37. How do health checks work in ASP.NET Core?
Register health checks via `builder.Services.AddHealthChecks().AddNpgSql(...).AddRedis(...)`. Map them with `app.MapHealthChecks("/healthz")`. Kubernetes uses these for liveness and readiness probes. Return `Degraded` instead of `Unhealthy` for non-critical dependencies to avoid unnecessary pod restarts.

### Q38. What is the difference between filters and middleware?
Middleware runs on every request and is pipeline-level (cross-cutting). Filters (Authorization, Resource, Action, Exception, Result) run only on MVC/Minimal API endpoints and have access to the action context. Use middleware for logging/correlation IDs; use filters for model validation or endpoint-specific authorization logic.

### Q39. How does configuration work in ASP.NET Core?
Configuration is layered: `appsettings.json` -> `appsettings.{Environment}.json` -> environment variables -> command-line args -> user secrets (dev). Later sources override earlier ones. In Kubernetes, environment variables and mounted ConfigMaps are the primary configuration sources, and `IOptionsMonitor<T>` allows hot-reloading without pod restarts.

### Q39b. Explain Minimal APIs vs Controllers — when do you use which?
Minimal APIs (`app.MapGet("/", () => "Hello")`) are lightweight — no controllers, no model binding attributes, just lambda handlers. Good for simple endpoints, microservices with few endpoints, or high-performance scenarios. Controllers are better for complex APIs with many endpoints, shared filters, versioning, and Swagger documentation. At Combination, our gRPC services don't use either — they use protobuf service definitions. REST endpoints for external partners use controllers for richer Swagger support.

### Q39c. How does the configuration system work in ASP.NET Core?
Layered configuration: `appsettings.json` → `appsettings.{Environment}.json` → environment variables → command-line args → user secrets (dev only) → Key Vault (production). Later sources override earlier ones. Bound to strongly-typed classes via `IOptions<T>` (singleton), `IOptionsSnapshot<T>` (scoped, reloads on change), `IOptionsMonitor<T>` (singleton with change notification). In K8s, we use environment variables from ConfigMaps/Secrets that override appsettings defaults.

---

## Common Gotchas

### Q40. Why is `async void` dangerous?
Exceptions in `async void` methods propagate to the `SynchronizationContext` and cannot be caught with try-catch by the caller. In ASP.NET Core, this means unhandled exceptions crash the process. Always return `Task` or `ValueTask` unless you are writing an event handler.

### Q41. What is the captured variable problem in loops?
Closures capture the variable, not the value. In `for (int i = 0; i < 5; i++) tasks.Add(() => Console.Write(i));`, all tasks print `5`. Fix by introducing a local copy: `var local = i;`. The `foreach` loop in C# 5+ captures correctly per iteration.

### Q42. Why is string concatenation in a loop bad?
`string` is immutable — each `+` creates a new string and copies the previous content, resulting in O(n^2) behavior. Use `StringBuilder` or `string.Join()`. In logging-heavy microservices, prefer structured logging (`_logger.LogInformation("Order {Id} processed", id)`) which avoids string allocation entirely when the log level is disabled.

### Q43. What are equality pitfalls with `==` vs `.Equals()`?
For reference types, `==` checks reference equality by default (unless overloaded, as with `string`). `.Equals()` checks value equality if overridden. `record` types override both. Comparing two different instances of a class DTO with `==` returns `false` even if all fields match — use records or override equality members.

### Q44. What happens if you forget to await a Task?
The task runs fire-and-forget. Exceptions are swallowed (or surface later on GC finalization as `UnobservedTaskException`). The calling method continues immediately, leading to race conditions. The compiler emits warning CS4014 — never suppress it.

---

## Performance

### Q45. When should you use `StringBuilder`?
When concatenating more than ~3-4 strings, especially in loops. `StringBuilder` maintains a mutable internal buffer, reducing allocations from O(n) to O(1) amortized. Pre-size with `new StringBuilder(estimatedCapacity)` to avoid resizing.

### Q46. What is `ArrayPool<T>` and how does it help?
`ArrayPool<T>.Shared.Rent(size)` returns a reusable buffer from a pool instead of allocating a new array. You must call `Return()` when done. Critical for high-throughput microservices processing large payloads (e.g., image processing, file uploads via gRPC streaming) to avoid LOH allocations and reduce GC pressure.

### Q47. What is `ObjectPool<T>` in ASP.NET Core?
`Microsoft.Extensions.ObjectPool` pools expensive-to-create objects like `StringBuilder` or custom serializers. Unlike `ArrayPool`, it is designed for arbitrary objects. Use it when profiling shows high allocation rates for a specific type in your hot path.

### Q48. How do you benchmark .NET code correctly?
Use BenchmarkDotNet — it handles warm-up, JIT tiering, GC collection between runs, and statistical analysis. Never benchmark with `Stopwatch` in a console app — results are unreliable due to JIT, GC, and OS scheduling noise. Always benchmark in Release mode with the `[MemoryDiagnoser]` attribute to track allocations.

### Q49. What is `ref struct` and why does it matter for performance?
A `ref struct` (like `Span<T>`, `ReadOnlySpan<T>`) can only live on the stack — it cannot be boxed, stored in fields of regular classes, or used across `await`. This constraint guarantees zero heap allocation and enables the compiler/runtime to optimize aggressively. Use it for high-performance parsing and buffer manipulation.

### Q50. What is Tiered Compilation and how does it affect microservice startup?
.NET uses tiered compilation: methods are first JIT-compiled quickly (Tier 0) for fast startup, then re-compiled with optimizations (Tier 1) after being called enough times. This benefits microservices with frequent restarts (rolling deployments in K8s). ReadyToRun (R2R) / AOT compilation can further reduce cold-start latency for serverless or scale-to-zero scenarios.

---

## Rapid Fire

| Question | Answer |
|----------|--------|
| `sealed` keyword benefit? | Prevents inheritance and enables devirtualization — the JIT can inline virtual method calls on sealed types, improving performance. |
| `const` vs `readonly`? | `const` is compile-time, inlined into callers (recompile all dependents on change). `readonly` is runtime, evaluated in constructor. Prefer `readonly` for values that could change across deployments. |
| What is `required` modifier (C# 11)? | Forces callers to set a property during initialization, enforced at compile time. Useful for DTOs where certain fields must always be populated. |
| `string.Empty` vs `""`? | Functionally identical. `string.Empty` is a single static field; `""` is interned by the compiler to the same reference. No performance difference. |
| `IHost` vs `WebApplication`? | `IHost` is the generic host for background services, workers. `WebApplication` (Minimal API host) extends it with HTTP pipeline. Use `IHost` for gRPC-only or queue-consumer microservices. |
| `record` vs `record struct`? | `record` = reference type (heap). `record struct` = value type (stack). Use `record struct` for small, frequently-created value objects. |
| What does `volatile` do? | Prevents compiler/CPU reordering of reads/writes to a field. Does NOT provide atomicity. Rarely needed — prefer `Interlocked` or `lock`. |
| `Lazy<T>` thread safety? | `Lazy<T>` with `LazyThreadSafetyMode.ExecutionAndPublication` (default) guarantees only one thread initializes the value. Use for expensive singleton initialization. |
| `Channel<T>` use case? | High-performance async producer-consumer queue. Use bounded channels for backpressure in microservices processing message broker events. |
| What is source generators? | Compile-time code generation that runs during build. Used by System.Text.Json, Minimal APIs, and gRPC for AOT-friendly serialization without reflection. |

---

## Common Interview Code Snippets

### "What's wrong with this code?"

**Async void:**
```csharp
// BAD — exceptions crash the process, can't be awaited
public async void SaveData() { await db.SaveAsync(); }
// FIX — return Task
public async Task SaveData() { await db.SaveAsync(); }
```

**Captured loop variable:**
```csharp
// BAD — all tasks capture the same 'i', print 10 ten times
for (var i = 0; i < 10; i++)
    tasks.Add(Task.Run(() => Console.WriteLine(i)));
// FIX — capture in local variable
for (var i = 0; i < 10; i++)
{
    var local = i;
    tasks.Add(Task.Run(() => Console.WriteLine(local)));
}
```

**String concatenation in loop:**
```csharp
// BAD — O(n²) allocations
string result = "";
foreach (var item in items) result += item.ToString();
// FIX — StringBuilder
var sb = new StringBuilder();
foreach (var item in items) sb.Append(item.ToString());
```

**Disposed context in async:**
```csharp
// BAD — context disposed before query executes
IEnumerable<User> GetUsers()
{
    using var db = new AppDbContext();
    return db.Users.Where(u => u.Active); // deferred execution!
}
// FIX — materialize with ToList()
List<User> GetUsers()
{
    using var db = new AppDbContext();
    return db.Users.Where(u => u.Active).ToList();
}
```

**DI lifetime mismatch:**
```csharp
// BAD — scoped DbContext injected into singleton service
// DbContext is created once and reused across all requests — connection stale, data stale
services.AddSingleton<MyService>(); // singleton
services.AddScoped<AppDbContext>(); // scoped — captured by singleton!
// FIX — use IServiceScopeFactory in the singleton
```

---

## Advanced — .NET 8/9 New Features

### Q51. What are `FrozenDictionary` and `FrozenSet` and how do they differ from `ReadOnlyDictionary`?
`FrozenDictionary<TKey,TValue>` and `FrozenSet<T>` (in `System.Collections.Frozen`, .NET 8+) are optimized for read-heavy scenarios. Unlike `ReadOnlyDictionary` which just wraps a mutable dictionary, frozen collections restructure internal data at construction time (expensive) to optimize lookup (cheap). They use optimized hash algorithms picked per-instance based on key distribution. Ideal for routing tables, permission maps, or feature flag dictionaries built once at startup and queried millions of times. Benchmark: `FrozenDictionary` can be 40-70% faster than `Dictionary` for lookups.

### Q52. What are C# 12 interceptors and when would you use them?
Interceptors are an *experimental* C# 12 feature that allow you to reroute a method call at a specific file/line location to a different implementation at compile time. The compiler substitutes the call during compilation. Primary use case: source generators that need to replace framework-generated code (e.g., replacing a `Map` call in Minimal APIs with a precompiled handler). You declare an `[InterceptsLocation]` attribute pointing to the exact source location. They are not meant for general application code — they are a compiler infrastructure feature for libraries and code generators.

### Q53. What is `TimeProvider` in .NET 8 and why does it matter for testing?
`TimeProvider` is an abstraction over `DateTime.UtcNow`, `Task.Delay`, and `CancellationTokenSource` timer operations. You inject `TimeProvider` instead of calling `DateTime.UtcNow` directly. In tests, use `FakeTimeProvider` to control time progression without actual delays. This makes testing timeout logic, token expiry, retry policies, and scheduled background tasks deterministic and fast. It replaces the common `IClock` interface pattern that teams used to create themselves.

### Q54. What is `SearchValues<T>` in .NET 8?
`SearchValues<T>` precomputes optimized lookup tables for `Span<T>.IndexOfAny()` and related methods. Instead of passing a `char[]` or `ReadOnlySpan<char>` on every call, you create a `SearchValues<char>` once and reuse it. The runtime picks SIMD-optimized implementations (SSE2, AVX2, ARM NEON) based on the input size and hardware. Use it for high-performance parsing — tokenizers, protocol parsers, log analyzers.

### Q55. What is `HybridCache` in .NET 9 and how does it prevent cache stampedes?
`HybridCache` combines in-process (L1) and distributed (L2, e.g., Redis) caching with built-in stampede protection. When multiple concurrent requests ask for the same uncached key, only one request executes the factory method; others wait for its result. Traditional `IDistributedCache` + manual locking doesn't handle this. `HybridCache` also supports tag-based invalidation and automatic serialization. It replaces the common `IMemoryCache` + `IDistributedCache` + `SemaphoreSlim` pattern.

### Q56. What are `CompositeFormat` and `string.Create` for allocation-free formatting?
`CompositeFormat.Parse("Order {0} has {1} items")` precompiles a format string once, then `string.Format(compositeFormat, ...)` avoids re-parsing the format on every call. `string.Create(length, state, (span, s) => ...)` allocates a single string and writes directly into its buffer via `Span<char>`, avoiding intermediate allocations. Use both in logging-heavy or serialization-heavy hot paths.

---

## Advanced — Async Patterns

### Q57. How does `IAsyncEnumerable<T>` work and when should you use it?
`IAsyncEnumerable<T>` produces elements asynchronously one at a time using `yield return` inside an `async` method. The consumer uses `await foreach`. Unlike returning `Task<List<T>>` (which buffers everything in memory), `IAsyncEnumerable` streams results as they become available. Use it for: streaming database rows without buffering, reading paginated API responses, gRPC server streaming, and SignalR streaming. EF Core supports `AsAsyncEnumerable()` to stream query results. Cancellation is supported via `[EnumeratorCancellation] CancellationToken`.

### Q58. What is `Parallel.ForEachAsync` and how does it differ from `Parallel.ForEach`?
`Parallel.ForEachAsync` (introduced in .NET 6) supports `async` lambda bodies and respects `CancellationToken`. It is designed for I/O-bound parallel work (e.g., calling 100 downstream APIs concurrently with a max degree of parallelism). `Parallel.ForEach` is for CPU-bound synchronous work and blocks threads. Key parameter: `MaxDegreeOfParallelism` controls concurrency. Common pattern: `await Parallel.ForEachAsync(items, new ParallelOptions { MaxDegreeOfParallelism = 10 }, async (item, ct) => { ... })`.

### Q59. How does `TaskCompletionSource<T>` bridge callback APIs to async/await?
`TaskCompletionSource<T>` creates a `Task<T>` that you manually complete via `SetResult()`, `SetException()`, or `SetCanceled()`. It bridges legacy callback/event APIs into the async/await world. Example: wrapping a WebSocket `OnMessage` callback into an awaitable `Task<string>`. Always use `TaskCreationOptions.RunContinuationsAsynchronously` to avoid inline continuation bugs where the completing thread runs the awaiter's code.

### Q60. What is `System.IO.Pipelines` and when do you use it over `Stream`?
`System.IO.Pipelines` provides `PipeReader`/`PipeWriter` for high-performance binary I/O with built-in buffer pooling, backpressure, and zero-copy reads. Unlike `Stream`, you don't allocate `byte[]` for each read — the pipe manages a `ReadOnlySequence<byte>` from pooled memory. Use it for custom network protocols, high-throughput socket servers, or processing Kestrel's raw request body. Kestrel itself is built on Pipelines internally.

### Q61. How do you properly propagate `CancellationToken` in a microservice?
Accept `CancellationToken` on every async method. In ASP.NET Core, bind it from `HttpContext.RequestAborted` (automatic in controller/minimal API parameters). Pass it to EF Core queries, `HttpClient` calls, and gRPC calls. In gRPC, the `ServerCallContext.CancellationToken` propagates client cancellation. Use `CancellationTokenSource.CreateLinkedTokenSource()` to combine request cancellation with your own timeout. Never swallow `OperationCanceledException` — let it bubble up so the framework returns 499/cancelled.

### Q62. What is `Channel<T>` backpressure and how do you configure it?
Bounded channels (`Channel.CreateBounded<T>(capacity)`) provide backpressure. When full, the `BoundedChannelFullMode` options are: `Wait` (producer blocks), `DropNewest`, `DropOldest`, `DropWrite`. For microservice event processing: use `Wait` to slow down producers when consumers can't keep up. For telemetry/logging: use `DropOldest` to never block the producer. Always call `writer.Complete()` on shutdown to signal consumers to drain and exit gracefully.

---

## Advanced — Source Generators

### Q63. How do source generators work in the compilation pipeline?
Source generators implement `IIncrementalGenerator` (preferred since .NET 6) and run between the semantic analysis and emit phases. The compiler gives the generator access to syntax trees and the semantic model. The generator produces additional `.cs` files that are compiled with the rest of the code. They are *additive only* — they cannot modify existing code (unlike Roslyn analyzers + code fixes). The incremental pipeline caches intermediate results so the generator only re-runs for changed inputs, keeping IDE responsiveness high.

### Q64. Name real-world uses of source generators in the .NET ecosystem.
**System.Text.Json**: generates type-specific serializers via `[JsonSerializable]`, eliminating runtime reflection and enabling AOT. **Minimal APIs**: generates `RequestDelegateFactory` code to bind route parameters without reflection. **gRPC**: generates client/server stubs from `.proto` files. **Logging**: `[LoggerMessage]` generates high-performance log methods with zero-boxing. **RegexGenerator**: `[GeneratedRegex]` compiles regex patterns at build time. **AutoMapper**: generates mapping code. **Mediator** (by Martin Othamar): generates `IMediator` dispatch without reflection.

### Q65. What is the difference between `ISourceGenerator` and `IIncrementalGenerator`?
`ISourceGenerator` (v1, .NET 5) re-runs on the entire compilation for every keystroke — causes IDE slowdowns. `IIncrementalGenerator` (v2, .NET 6+) builds a pipeline of transformations with caching. Only changed inputs trigger re-generation. Always use `IIncrementalGenerator`. The pipeline: `RegisterPostInitializationOutput` for static code, `SyntaxProvider.ForAttributeWithMetadataName` to filter nodes efficiently, then `RegisterSourceOutput` to emit code.

### Q66. How does `[LoggerMessage]` source generator improve logging performance?
`[LoggerMessage(EventId = 1, Level = LogLevel.Information, Message = "Order {OrderId} processed")]` generates a static partial method that: (1) checks `IsEnabled` before doing any work, (2) uses structured logging without boxing value types, (3) avoids string interpolation allocation when the log level is disabled. Benchmark: 3-5x faster than `_logger.LogInformation("Order {OrderId}...", orderId)` in hot paths because it eliminates the `params object[]` allocation.

---

## Advanced — Minimal APIs Deep Dive

### Q67. How does Minimal API route handler binding work without reflection in AOT?
Minimal APIs use source generators (`RequestDelegateGenerator`) to generate binding code at compile time. For each `app.MapGet("/orders/{id}", (int id, IOrderService svc) => ...)`, the generator creates a `RequestDelegate` that reads `id` from route values and resolves `IOrderService` from DI — all without runtime reflection. This enables Native AOT deployment. If AOT is not used, it falls back to runtime reflection-based binding.

### Q68. How do you implement filters in Minimal APIs?
Minimal APIs support endpoint filters (similar to MVC action filters) via `AddEndpointFilter<T>()` or inline `AddEndpointFilter(async (context, next) => { ... })`. Filters run in a pipeline: before the handler (validation, auth), call `next(context)`, then after (response transformation). Use `IEndpointFilter` for reusable filters. Unlike MVC filters, they don't have separate Authorization/Resource/Action/Result filter types — it's a single pipeline.

### Q69. What are route groups in Minimal APIs?
`app.MapGroup("/api/orders")` creates a group that shares prefix, filters, and metadata. You can nest groups and add filters per group: `.AddEndpointFilter<AuthFilter>()`. This replaces the organizational structure of MVC controllers — each group is like a controller, each map call is an action. Route groups also support `.RequireAuthorization()`, `.WithTags()` for OpenAPI, and `.WithMetadata()`.

### Q70. How do you handle validation in Minimal APIs without FluentValidation?
.NET 8+ supports `[AsParameters]` to bind complex types, but built-in validation is minimal. Options: (1) Manual validation in endpoint filters, (2) `FluentValidation` with a custom `AddEndpointFilter`, (3) `.NET 9` introduced `IValidatableObject` support, (4) Source-generated validators. The filter pattern: create a generic `ValidationFilter<T>` that resolves `IValidator<T>` from DI and returns `Results.ValidationProblem()` on failure.

---

## Advanced — EF Core

### Q71. What are EF Core compiled queries and when should you use them?
`EF.CompileAsyncQuery((AppDbContext db, int id) => db.Orders.First(o => o.Id == id))` pre-compiles the LINQ expression tree to SQL once. Subsequent calls skip expression tree processing. Use for queries called thousands of times per second (e.g., `GetById` in a gRPC handler). Benchmark: ~40% faster for simple queries due to eliminated expression compilation. Limitation: the query shape must be static — no dynamic `Where` clauses.

### Q72. How do EF Core interceptors work and what are common use cases?
Implement `SaveChangesInterceptor`, `DbCommandInterceptor`, or `DbConnectionInterceptor` and register with `optionsBuilder.AddInterceptors(...)`. **SaveChangesInterceptor**: automatically set `CreatedAt`/`UpdatedAt` timestamps, implement soft delete (`IsDeleted = true` instead of DELETE), enforce audit trails. **DbCommandInterceptor**: log slow queries, add query hints, modify SQL before execution. **DbConnectionInterceptor**: add Azure AD token to connection. Interceptors are cleaner than overriding `SaveChangesAsync` because they're composable and reusable across DbContexts.

### Q73. What are EF Core bulk operations and how do `ExecuteUpdate`/`ExecuteDelete` work?
`ExecuteUpdate` and `ExecuteDelete` (EF Core 7+) bypass change tracking and execute a single SQL statement directly. `db.Orders.Where(o => o.Status == "expired").ExecuteDeleteAsync()` generates `DELETE FROM Orders WHERE Status = 'expired'` — no entity loading, no change tracker overhead. `ExecuteUpdateAsync` supports setting multiple columns: `.ExecuteUpdateAsync(s => s.SetProperty(o => o.Status, "archived"))`. Use for batch operations. Limitation: no cascade via EF navigation — relies on database cascades.

### Q74. What is the difference between `Split Query` and `Single Query` in EF Core?
Single query (default) generates one SQL with JOINs — risk of "cartesian explosion" when including multiple collections (`Include(o => o.Items).Include(o => o.Payments)`), producing rows = Items x Payments. Split query (`AsSplitQuery()`) sends separate SQL queries per `Include`. Trade-off: split query avoids data explosion but creates multiple round-trips and doesn't guarantee consistency (no shared transaction by default). Use split query when including 2+ collections.

### Q75. How do you handle EF Core migrations in a microservices CI/CD pipeline?
Options: (1) `dotnet ef migrations bundle` creates a self-contained executable that applies migrations — run as an init container in Kubernetes. (2) Apply migrations in `Program.cs` only in development: `if (app.Environment.IsDevelopment()) db.Database.Migrate()`. (3) Use a separate migration job/tool (e.g., Flyway, DbUp) for production — never auto-migrate in production pods. (4) `IDesignTimeDbContextFactory` for generating migrations without running the app.

---

## Advanced — Performance & Profiling

### Q76. What profiling tools are available in .NET and when do you use each?
**dotnet-counters**: real-time runtime metrics (GC, thread pool, HTTP). Use for first-pass triage. **dotnet-trace**: captures ETW/EventPipe traces for CPU profiling. Analyze in PerfView or SpeedScope. **dotnet-dump**: captures and analyzes memory dumps. Use for memory leaks and deadlocks. **dotnet-gcdump**: lightweight GC heap snapshot without full dump. **BenchmarkDotNet**: micro-benchmarks with statistical rigor. **JetBrains dotMemory/dotTrace**: GUI-based profiling for development. In production, use `dotnet-monitor` sidecar in Kubernetes for on-demand diagnostics.

### Q77. How does `BenchmarkDotNet` work and what are common mistakes?
BenchmarkDotNet handles: warm-up iterations, JIT tiering (Tier0 → Tier1), GC collection between benchmarks, outlier detection, and statistical analysis. **Common mistakes**: (1) Benchmarking in Debug mode (no optimizations), (2) Not using `[MemoryDiagnoser]` to track allocations, (3) Benchmarking code that gets dead-code-eliminated (consume the result), (4) Comparing methods with different GC modes. Use `[Params]` for parameterized benchmarks, `[GlobalSetup]` for initialization, `[Benchmark(Baseline = true)]` for comparison.

### Q78. What are allocation-free patterns in .NET?
(1) `Span<T>` / `ReadOnlySpan<T>` for slicing without copying. (2) `stackalloc` for small temporary buffers. (3) `ArrayPool<T>.Shared.Rent/Return` for reusable arrays. (4) `string.Create()` for direct string building. (5) `ValueTask<T>` for sync-completed async paths. (6) `ref struct` for stack-only types. (7) `[SkipLocalsInit]` to skip zeroing stack memory. (8) `ObjectPool<T>` for expensive objects. (9) Value-type enumerators (struct enumerator pattern). (10) `RecyclableMemoryStream` instead of `MemoryStream` for large buffers.

### Q79. What is Native AOT and what are its trade-offs?
Native AOT (`dotnet publish -p:PublishAot=true`) compiles to a native binary — no JIT, no IL, instant startup (~10ms vs ~200ms). Trade-offs: no runtime code generation (no `Reflection.Emit`, no `Expression.Compile`), no dynamic assembly loading, trimming removes unused code (can break reflection-based libraries). Requires source generators for serialization. Ideal for cloud-native microservices, serverless functions (cold start matters), and CLI tools. Not suitable for apps using `System.Reflection` heavily.

### Q80. How do you identify and fix thread pool starvation?
Symptoms: rising response times, `ThreadPool.ThreadCount` growing beyond 200+, `dotnet-counters` showing high `threadpool-queue-length`. Cause: blocking calls (`.Result`, `.Wait()`, `Thread.Sleep`) in async context exhaust thread pool threads. Fix: (1) Replace all blocking calls with `await`, (2) Use `ConfigureAwait(false)` in libraries, (3) Increase min threads temporarily: `ThreadPool.SetMinThreads(200, 200)`, (4) Use `dotnet-trace` with `ThreadPoolStarvation` events to find the blocking call site.

---

## Advanced — gRPC in .NET

### Q81. How does gRPC differ from REST in .NET and when do you choose each?
gRPC uses HTTP/2, protobuf binary serialization, and strict contracts (`.proto` files). It is 5-10x faster than JSON REST for inter-service calls. Supports 4 patterns: unary, server streaming, client streaming, bidirectional streaming. Choose gRPC for internal microservice communication. Choose REST for external/public APIs (browser compatibility, simpler tooling). Limitation: gRPC-Web is needed for browser clients, and HTTP/2 is required (some load balancers don't support it).

### Q82. How do gRPC interceptors work in .NET?
Interceptors are gRPC middleware. Inherit from `Interceptor` and override methods: `UnaryServerHandler`, `ServerStreamingServerHandler`, etc. Register with `services.AddGrpc(o => o.Interceptors.Add<LoggingInterceptor>())`. Use cases: logging, authentication token propagation, error mapping (convert exceptions to gRPC status codes), metrics, retry with deadline propagation. Interceptors execute in registration order, similar to ASP.NET middleware.

### Q83. How do gRPC deadlines and cancellation work?
Deadlines propagate automatically across service boundaries. Client sets `CallOptions.Deadline`, server reads `context.Deadline`. If the deadline expires, the call is cancelled with `StatusCode.DeadlineExceeded`. In a chain of microservices (A calls B calls C), the deadline propagates — if A sets 5s, B has whatever time remains. Always set deadlines on gRPC calls; without them, a stuck downstream service hangs forever. Access via `ServerCallContext.CancellationToken`.

### Q84. How do you handle gRPC streaming efficiently in .NET?
Server streaming: use `IAsyncEnumerable<T>` (supported in .NET 7+) or `responseStream.WriteAsync()`. Backpressure is built into HTTP/2 flow control. Client streaming: read with `await foreach (var msg in requestStream.ReadAllAsync())`. For large payloads, chunk into messages under 4MB (default max). Use `channel.Writer.Complete()` pattern for bidirectional streaming shutdown. Monitor with `Grpc.Net.Client` metrics for stream lifecycle.

---

## Advanced — SignalR

### Q85. How does SignalR scale across multiple server instances?
By default, SignalR connections are local to the server. To scale horizontally, use a backplane: **Redis backplane** (`AddStackExchangeRedis()`), **Azure SignalR Service** (managed, serverless), or **SQL Server backplane** (slower). The backplane broadcasts messages to all servers. Sticky sessions (via cookie or connection ID) are recommended but not required with a backplane. Trade-off: Redis backplane adds latency (~1-2ms per message); Azure SignalR Service offloads connection management entirely.

### Q86. What transport protocols does SignalR use and how does fallback work?
SignalR negotiates the best transport: (1) **WebSockets** (preferred — full duplex, low overhead), (2) **Server-Sent Events** (SSE — one-way server→client), (3) **Long Polling** (fallback for restricted networks). The client negotiates during the initial HTTP request. In Kubernetes, ensure the ingress supports WebSocket upgrades (`Upgrade: websocket` header). If WebSockets are blocked, performance degrades significantly with long polling.

### Q87. How do you handle reconnection and state recovery in SignalR?
Client-side: `HubConnectionBuilder.WithAutomaticReconnect(new[] { 0, 2, 10, 30 })` configures retry delays. On reconnection, the client gets a new connection ID — you must rejoin groups and replay missed messages. Pattern: on `Reconnected`, call a hub method like `RejoinGroups(userId)` and fetch missed messages from a queue/database since `lastReceivedTimestamp`. SignalR does not buffer messages during disconnection.

---

## Advanced — Background Services

### Q88. What is the difference between `IHostedService` and `BackgroundService`?
`IHostedService` has `StartAsync` and `StopAsync` — you manage the lifetime yourself. `BackgroundService` inherits from `IHostedService` and provides `ExecuteAsync(CancellationToken)` which runs for the service lifetime. Use `BackgroundService` for long-running loops (polling, queue consumers). Use raw `IHostedService` for startup/shutdown hooks (warming caches, draining connections). Both are registered with `services.AddHostedService<T>()`.

### Q89. How do you handle exceptions in `BackgroundService` to prevent silent death?
If `ExecuteAsync` throws an unhandled exception, the service stops silently (before .NET 8) or crashes the host (in .NET 8+ with `HostOptions.BackgroundServiceExceptionBehavior = Terminate`). Best practice: wrap the entire loop in try/catch, log the error, and continue (or break and signal unhealthy via `IHealthCheck`). Use `IHostApplicationLifetime.StopApplication()` for fatal errors. Never let a background service die silently.

### Q90. How do you access scoped services (like `DbContext`) in a `BackgroundService`?
`BackgroundService` is singleton — you cannot inject scoped services directly (captive dependency). Inject `IServiceScopeFactory`, create a scope per iteration: `using var scope = _scopeFactory.CreateScope(); var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();`. Dispose the scope after each iteration to release connections. Common mistake: creating one scope and reusing it forever — this leaks memory and stales the DbContext.

### Q91. How do you implement periodic background work with `PeriodicTimer`?
`PeriodicTimer` (introduced in .NET 6) is async-friendly: `var timer = new PeriodicTimer(TimeSpan.FromMinutes(5)); while (await timer.WaitForNextTickAsync(ct)) { ... }`. Unlike `Timer` or `Task.Delay` loops, `PeriodicTimer` doesn't drift — it accounts for execution time. It also respects `CancellationToken` for clean shutdown. In .NET 8+, combine with `TimeProvider` for testability.

---

## Advanced — Middleware Deep Dive

### Q92. What is the difference between convention-based middleware and `IMiddleware`?
Convention-based middleware uses a constructor + `InvokeAsync(HttpContext, RequestDelegate)` — it's instantiated once (effectively singleton). You cannot inject scoped services into the constructor. `IMiddleware` interface is resolved from DI per request, respecting service lifetimes — you can inject scoped `DbContext` into the constructor. Trade-off: `IMiddleware` has slightly more overhead due to per-request resolution. Use `IMiddleware` when you need scoped dependencies; convention-based otherwise.

### Q93. How does short-circuiting work in the middleware pipeline?
A middleware short-circuits by not calling `await next(context)`. The remaining pipeline is skipped, and the response returns back through the already-executed middleware. Use cases: returning cached responses, rejecting unauthorized requests early, health check endpoints. Example: rate-limiting middleware that returns 429 without hitting the controller. `app.UseWhen(ctx => ctx.Request.Path.StartsWithSegments("/api"), branch => ...)` conditionally branches the pipeline.

### Q94. How do you write middleware that reads and re-reads the request body?
By default, `HttpRequest.Body` is a forward-only stream. To read it multiple times (e.g., logging middleware + model binding): call `context.Request.EnableBuffering()` before reading, then `context.Request.Body.Position = 0` to rewind. Performance warning: this buffers the entire body in memory (or disk for large payloads via `MemoryBufferThreshold`). Only enable buffering when necessary and set size limits.

### Q95. How do you implement response caching vs output caching middleware?
**Response Caching** (`app.UseResponseCaching()`) — follows HTTP `Cache-Control` headers, stores in-memory, respects `Vary` headers. Limited: doesn't work with authenticated responses. **Output Caching** (`app.UseOutputCache()`, .NET 7+) — server-side full response caching with tag-based invalidation, cache policies, and customizable storage (Redis). Output caching is more powerful: `app.MapGet("/orders", () => ...).CacheOutput(p => p.Tag("orders").Expire(TimeSpan.FromMinutes(5)))`. Invalidate with `IOutputCacheStore.EvictByTagAsync("orders")`.

---

## Sorulursa

> [!faq]- **Async/Await — Backpressure & Resource Exhaustion at Scale**
> 
> You're running an order processing microservice that ingests messages from Kafka at 10,000 msg/sec peak. Each message triggers an async handler that validates the order, calls 3 downstream HTTP services in parallel (using `Task.WhenAll`), and writes to PostgreSQL.
> 
> At 3 AM, you get paged: the service is consuming 100% CPU, response times are 30+ seconds, and the Kafka consumer lag is growing exponentially. Memory usage looks normal, but thread pool starvation is suspected.
> 
> Walk me through your diagnosis: What specific async/await anti-patterns or configuration issues could cause this? How do `Channel<T>`, `SemaphoreSlim`, and `IHttpClientFactory` interact in this scenario? And most importantly — what specific code changes would you make to introduce proper backpressure and prevent this from recurring?
> 
> **💡 Cevap Yapısı:**
> 1. **Tanı:** Thread pool starvation mı? CPU bound mı? IO bound mı? `dotnet-counters` ve `dotnet-trace` ile ne bakarsın?
> 2. **Köken Neden:** `HttpClient` timeout'ları, `Task.WhenAll` ile sınırsız paralellik, `Channel<T>` bounded olmadığı için buffer overflow, `DbContext` pool exhaustion
> 3. **Pattern Etkileşimi:** `IHttpClientFactory`'nin handler pooling'i + `SemaphoreSlim` rate limiting + `Channel<T>` backpressure — nasıl birlikte çalışır?
> 4. **Çözüm:** Bounded `Channel<T>` (capacity=1000), `SemaphoreSlim` ile concurrent call limit (max 50), `Polly` retry policy with circuit breaker, `ChannelReader` pipeline stage'leri ile iş yükü ayrıştırma
> 
> **Derin Sorular (Follow-up):**
> - "Bounded channel full olduğunda ne olur? Producer bloklanır mı, exception alır mı?"
> - "SemaphoreSlim.WaitAsync() timeout'u ne zaman vermeli?"
> - "Bu senaryoda `Parallel.ForEachAsync` kullanır mıydın, neden/neden olmaz?"

> [!faq]- "C#'ta covariance ve contravariance nedir? `out` ve `in` ne yapar?"
> **Covariance (`out T`):** Bir generic type parametresi sadece output (return) pozisyonunda kullanılıyorsa covariant olabilir. `IEnumerable<out T>` covariant çünkü `T`'yi sadece döndürüyor, asla input olarak almıyor. Bu yüzden `IEnumerable<string>` → `IEnumerable<object>` güvenli: her string zaten bir object.
> 
> **Contravariance (`in T`):** Bir generic type parametresi sadece input (parameter) pozisyonunda kullanılıyorsa contravariant olabilir. `Action<in T>` contravariant çünkü `T`'yi sadece parametre olarak alıyor. `Action<object>` → `Action<string>` güvenli: object kabul eden bir method, string de kabul edebilir.
> 
> **Neden `List<T>` invariant?** `List<T>` hem okuma (`T` döndürür — covariant ihtiyacı) hem yazma (`T` alır — contravariant ihtiyacı) yapıyor. İkisi aynı anda olamaz. Eğer `List<Cat>` bir `List<Animal>`'a atanabilseydi, o referans üzerinden `list.Add(new Dog())` yazabilirdin — ama alttaki list sadece Cat kabul ediyor. Type safety bozulur.
> 
> **`Func<in T, out TResult>` açıklaması:**
> - `T` contravariant (`in`): fonksiyonun parametresi. `Func<Animal, string>` bir `Func<Cat, string>`'e atanabilir — Animal kabul eden fonksiyon, Cat da kabul edebilir (Cat bir Animal).
> - `TResult` covariant (`out`): fonksiyonun dönüş değeri. `Func<Cat, string>` bir `Func<Cat, object>`'e atanabilir — string döndüren fonksiyon, object de döndürmüş sayılır.
> 
> **Pratik kural:** `out` = "sadece dışarı çıkar" (return), `in` = "sadece içeri girer" (parameter). Compiler bunu enforce eder — `out T`'yi parametre pozisyonunda kullanamazsın.

> [!faq]- "What C# feature do you use most in microservices?"
> Async/await and DI. Every gRPC handler, every GraphQL resolver, every HTTP endpoint is async. DI wires everything together — services, repositories, clients, config. Getting the lifetimes right (scoped DbContext, singleton HttpClient, transient handlers) is the difference between a working service and subtle production bugs.

> [!faq]- "How do you handle performance issues in .NET?"
> Profile first, don't guess. BenchmarkDotNet for micro-benchmarks, dotnet-counters for runtime metrics, dotnet-trace for CPU profiling. Most common issues: unnecessary allocations in hot paths (fix with Span/ArrayPool), N+1 queries (fix with proper LINQ/DataLoader), synchronous blocking on async code (fix with async all the way). At Combination, I fixed a GraphQL resolver from 3s to 200ms by adding DataLoader — the code looked fine, the execution plan showed 11 database calls.

> [!faq]- "What's new in C# 12 / .NET 9 that you use?"
> Primary constructors on classes — cleaner DI injection, less boilerplate. Collection expressions `[1, 2, 3]` — readable. `required` keyword on properties — compile-time enforcement of required fields without constructor parameters. For .NET 9: improved AOT compilation, better Kestrel performance, simplified auth APIs. In practice, the biggest daily impact is primary constructors — every service class gets cleaner.

> [!faq]- "How do you write testable C# code?"
> Constructor injection for dependencies (interface-based), avoid static methods with side effects, keep business logic in domain classes (not controllers), return Task for anything async. At Combination, every service has an `IServiceMarker` interface, WebApplicationFactory for in-process testing, NSubstitute for mocking external dependencies. The pattern: interface in ApplicationCore, implementation in Infrastructure, test mocks the interface.

> [!faq]- "Explain the middleware pipeline in ASP.NET Core."
> Each middleware is a function that receives the request, optionally processes it, calls the next middleware, then optionally processes the response on the way back. Order matters: auth before routing, exception handling first (to catch everything). It's the Chain of Responsibility pattern. Example pipeline: ExceptionHandler → HTTPS redirect → Static files → Auth → Routing → Endpoints. Custom middleware: logging, correlation ID injection, request timing.
