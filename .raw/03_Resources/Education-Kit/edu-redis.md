---
tags:
  - education-kit
---

# Redis — Knowledge Base

> [!info] In-memory data store: caching, streams, pub/sub, session management, real-time data. Sub-millisecond reads/writes.

## What Redis Is

Redis is an **in-memory data store** — it keeps all data in RAM, which makes it extremely fast (sub-millisecond reads/writes). It's not just a cache — it's a full-featured data structure server that supports strings, hashes, lists, sets, sorted sets, streams, and more. You can use it as a **cache** (store frequently accessed data to avoid hitting the database), a **message broker** (Pub/Sub or Streams for event-driven communication), a **session store** (fast session lookups instead of hitting SQL on every request), or a **real-time data platform** (leaderboards, rate limiting, real-time tracking).

Redis is **single-threaded** for command execution — one command at a time, no locks needed — which makes it simple and predictable. It achieves high throughput through non-blocking I/O and efficient data structures, not parallelism. Persistence is optional: **RDB** snapshots for point-in-time backups, **AOF** (Append Only File) for durability where every write is logged. You can use both together.

The trade-off: everything lives in RAM, so Redis is expensive for large datasets. It's best for **hot data** that needs fast access — not for storing terabytes.

## Key Concepts

### Data Structures
- **Strings** — Simplest type. Key-value pairs. `SET user:123:session "token" EX 3600`.
- **Hashes** — Field-value maps under a key. `HSET item:456 name "widget" price 9.99`.
- **Lists** — Ordered sequences. Simple queues (LPUSH/RPOP). No consumer groups.
- **Sets** — Unordered unique values. Tags, memberships, intersection queries.
- **Sorted Sets** — Sets with scores. Leaderboards, priority queues, time-series indexes.
- **Streams** — Append-only log with consumer groups. Similar to Kafka but simpler, built into Redis.

### Redis Streams
- **Append-only log** — Events added to the end, never modified. Auto-generated ID (timestamp + sequence).
- **Consumer groups** — Multiple consumers share work. If a consumer crashes, unacked messages get reassigned.
- **Acknowledgment** — Consumer must `XACK` after processing. Unacked messages stay in PEL.
- **Replay** — Read from any position — beginning, specific ID, or "only new messages."
- **Use cases** — Real-time event ingestion, activity feeds, IoT data, lightweight event streaming.

### Caching Patterns
Caching patterns define how your application interacts with the cache and database — when to read from cache vs DB, when to write to cache, and how to handle cache misses and stale data.

- **Cache-aside** — Check cache first. Miss → read DB → write cache. Most common.
- **Write-through** — Write cache + DB simultaneously. Always up to date, adds write latency.
- **Write-behind** — Write cache first, async DB write later. Lower latency, risk of data loss.
- **TTL** — Every cached value needs expiry. Without TTL, cache grows forever with stale data.
- **Cache invalidation** — The hard problem. Strategies: event-driven, TTL-based, versioned keys.
- **Cache stampede** — Many requests hit DB when popular entry expires. Fix: background refresh or locking.

### Sentinel (High Availability)
- **What** — Monitoring system. Watches primary, detects failure, promotes replica, notifies clients.
- **Setup** — 3 Sentinel instances, 1 primary + N replicas. Majority vote for failover.
- **Failover** — Primary down → replica promoted in ~5 seconds. Auto-reconnect via Sentinel-aware connection.
- **Client-side** — Sentinel-aware connection string discovers current primary automatically.

### Redis vs Alternatives
- **vs Memcached** — Redis has data structures, persistence. Memcached is simpler key-value only.
- **vs Kafka** — Kafka wins at scale (throughput, partitioning, retention). Redis Streams is simpler when Redis is already running.
- **Cluster vs Sentinel** — Sentinel = failover (one primary). Cluster = sharding (multiple primaries).

### Performance Considerations
- **Memory** — All data in RAM. Monitor usage. Eviction starts when full.
- **Eviction policies** — `allkeys-lru` (cache), `volatile-ttl` (expiring keys first), `noeviction` (errors when full).
- **Persistence** — RDB (snapshots, fast recovery) + AOF (every write, more durable). Use both for critical data.
- **Pipeline** — Batch commands into one network round-trip. Critical for throughput.
- **Connection pooling** — Reuse connections. New TCP per request is expensive.

## Sorulursa

> [!faq]- "When would you use Redis Streams vs Kafka?"
> Redis Streams when: you already run Redis, volume is moderate, simple consumer groups. Kafka when: high throughput, multiple consumer groups at scale, long retention, event-driven architecture across many services.

> [!faq]- "How do you prevent cache stampede?"
> Two approaches: (1) background refresh — update popular entries before they expire. (2) Locking — first miss acquires lock, fetches from DB, others wait.

> [!faq]- "Redis is single-threaded — how is it fast?"
> No lock contention, no context switching. Non-blocking I/O handles thousands of connections. Bottleneck is network/memory, not CPU.
