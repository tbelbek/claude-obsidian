---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Redis — Quick Reference

> [!info] How I've used it: At KocSistem, Redis was the backbone of the real-time GPS tracking system — Streams for GPS data ingestion, caching for session management, Sentinel for failover. Solved the scaling problem when SQL Server couldn't handle 500+ trucks writing every 2 seconds.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Data Structures\|data structures]] | strings, hashes, lists, sets, sorted sets, streams | [[#Redis Streams (What I Used)\|Streams]] | append-only log, consumer groups, ack, replay |
| [[#Sentinel (High Availability)\|Sentinel]] | 3 instances, auto-failover, 5-second promotion | [[#Caching Patterns\|cache-aside]] | check cache → miss → read DB → write cache |
| [[#Caching Patterns\|TTL]] | every cached value needs expiry, prevent stale data | [[#Performance Considerations\|eviction]] | volatile-ttl for cache, noeviction for streams |
| [[#Redis vs Alternatives\|vs Kafka]] | Redis=simple streaming, Kafka=scale+fan-out | [[#HOW WE USED IT\|GPS scaling]] | 500 trucks → SQL overwhelmed → Redis Streams + SQL batch |
| [[#What Redis Is\|what Redis is]] | in-memory data store, sub-ms, cache+broker+session+realtime | | |

## HOW WE USED IT

At KocSistem, Redis started as a session cache but became the critical layer that [[sd-redis-scaling|saved the GPS tracking system]].

**What happened:**
- 500+ trucks sending GPS coordinates every 2 seconds overwhelmed SQL Server (250 writes/second + dashboard reads on the same table)
- I split the architecture: GPS data went into Redis Streams for real-time display, background worker batch-inserted into SQL every 30 seconds for historical queries
- Dashboard went from frozen to sub-second response

**What I set up:**
- Redis Streams with consumer groups — dashboard read latest entry per truck (`XREVRANGE`), batch worker read and acknowledged entries for SQL insertion. If the worker crashed, unacked entries stayed until restart
- Redis Sentinel (3 instances) for automatic failover — tested by killing the primary under load, confirmed replica promotion in ~5 seconds
- Session caching with TTL — user sessions stored in Redis with 1-hour expiry
- Eviction policy: `volatile-ttl` for cache data, `noeviction` for stream data (never lose GPS coordinates)
- AOF persistence for the GPS stream — every write logged, recoverable after restart
- Pipeline batching — batch worker read 1000 stream entries per pipeline call to minimize network round-trips

---

## Key Concepts

### What Redis Is
Redis is an **in-memory data store** — it keeps all data in RAM, which makes it extremely fast (sub-millisecond reads/writes). It's not just a cache — it's a full-featured data structure server that supports strings, hashes, lists, sets, sorted sets, streams, and more. You can use it as a **cache** (store frequently accessed data to avoid hitting the database), a **message broker** (Pub/Sub or Streams for event-driven communication), a **session store** (fast session lookups instead of hitting SQL on every request), or a **real-time data platform** (leaderboards, rate limiting, GPS tracking).

Redis is **single-threaded** for command execution — one command at a time, no locks needed — which makes it simple and predictable. It achieves high throughput through non-blocking I/O and efficient data structures, not parallelism. Persistence is optional: **RDB** snapshots for point-in-time backups, **AOF** (Append Only File) for durability where every write is logged. You can use both together.

The trade-off: everything lives in RAM, so Redis is expensive for large datasets. It's best for **hot data** that needs fast access — not for storing terabytes. For cold data, use a database. For hot data that needs sub-millisecond access, Redis is hard to beat.

### Data Structures
- **Strings** — Simplest type. Key-value pairs. Used for session tokens, feature flags, simple caching. `SET user:123:session "token" EX 3600` (expires in 1 hour).
- **Hashes** — Field-value maps under a key. Used for storing objects without serialization overhead. `HSET truck:456 lat 57.7 lng 11.9 speed 42`.
- **Lists** — Ordered sequences. Used for simple queues (LPUSH/RPOP). No consumer groups — if you need those, use Streams.
- **Sets** — Unordered unique values. Used for tags, memberships, intersection queries.
- **Sorted Sets** — Sets with scores. Used for leaderboards, priority queues, time-series indexes. `ZADD active-trucks 1679000000 "truck:456"` (score = timestamp).
- **Streams** — Append-only log with consumer groups. The data structure that solved our GPS problem. Similar to Kafka but simpler, built into Redis.

### Redis Streams (What I Used)
- **Append-only log** — Events are added to the end, never modified. Each entry has an auto-generated ID (timestamp + sequence).
- **Consumer groups** — Multiple consumers share work from a stream. Each message goes to one consumer in the group. If a consumer crashes, unacked messages get reassigned.
- **Acknowledgment** — Consumer must `XACK` after processing. Unacked messages stay in the pending entries list (PEL) until acknowledged or claimed by another consumer.
- **Replay** — Can read from any position — beginning, a specific ID, or "only new messages." Useful for recovery after a crash.
- **At KocSistem** — GPS coordinates went into a stream. Dashboard read the latest entry per truck (`XREVRANGE`). Batch worker read and acknowledged entries for SQL insertion. If the worker crashed, unacked entries stayed until it restarted.

### Caching Patterns
Caching patterns define how your application interacts with the cache and the database — when to read from cache vs DB, when to write to cache, and how to handle cache misses and stale data. The pattern you choose determines your consistency guarantees and performance characteristics.

- **Cache-aside** — Application checks cache first. Cache miss → read from database → write to cache. Most common pattern. Used for session data and frequently accessed configs.
- **Write-through** — Write to cache and database simultaneously. Guarantees cache is always up to date but adds latency to writes.
- **TTL (Time-to-Live)** — Every cached value should have an expiry. Without TTL, cache grows forever and serves stale data.
- **Cache invalidation** — The hard problem. When the source data changes, the cache must be invalidated. At KocSistem, GPS data was naturally time-series — we didn't invalidate, we just wrote the latest position and the old one expired.

### Sentinel (High Availability)
- **What** — Monitoring system for Redis. Watches the primary, detects failure, promotes a replica to primary, notifies clients.
- **Setup** — 3 Sentinel instances watching 1 primary + N replicas. Majority vote required to trigger failover (prevents split-brain).
- **At KocSistem** — 3 Sentinel instances monitoring the primary. When the primary went down during our failover test, Sentinel promoted a replica in ~5 seconds. The application used the Sentinel-aware connection string, so it reconnected automatically.
- **Client-side** — Use Sentinel-aware connection string (e.g., StackExchange.Redis `ServiceName` option). The client discovers the current primary through Sentinel.

### Redis vs Alternatives
- **Redis vs Memcached** — Redis has data structures (Streams, Sorted Sets, Hashes). Memcached is simpler key-value only. Redis has persistence, Memcached doesn't. Use Memcached only if you need pure in-memory caching with no fancy features.
- **Redis vs Kafka** — For event streaming at scale, Kafka wins (better throughput, partitioning, retention). For "I need a stream and I already have Redis," Redis Streams is simpler. We chose Redis Streams because Redis was already running for caching.
- **Redis Cluster vs Sentinel** — Sentinel provides failover (one primary, replicas for reads). Cluster provides sharding (data split across multiple primaries). For our GPS use case, Sentinel was enough — data volume was high but not sharding-level.

### Performance Considerations
- **Memory** — Redis is in-memory. All data must fit in RAM. Monitor memory usage — when Redis fills up, it starts evicting keys based on the configured policy.
- **Eviction policies** — `allkeys-lru` (evict least recently used), `volatile-ttl` (evict keys closest to expiry), `noeviction` (return errors when full). We used `volatile-ttl` for caching and `noeviction` for Streams (don't lose GPS data).
- **Persistence** — RDB (periodic snapshots) and AOF (append-only file, logs every write). RDB is faster for recovery, AOF is more durable. We used AOF for the GPS stream data.
- **Pipeline** — Batch multiple commands into one network round-trip. Critical for high-throughput scenarios. The batch worker read 1000 stream entries per pipeline call.

## Sorulursa

> [!faq]- "Why Redis Streams instead of Kafka for GPS data?"
> We were already running Redis for session caching. Adding Kafka would mean another infrastructure component to deploy, monitor, and maintain. Redis Streams gave us consumer groups, acknowledgment, and replay — everything we needed — without adding a new tool. The GPS data didn't need Kafka-level durability — if we lost a few seconds of data, the dashboard just skipped ahead. Pragmatic choice.

> [!faq]- "How did you handle Redis failover?"
> Redis Sentinel with 3 instances monitoring the primary. Tested by killing the primary under load — Sentinel promoted a replica in ~5 seconds, application reconnected automatically via Sentinel-aware connection string. Dashboard had a brief blip but no data loss because the replica had the latest data.

> [!faq]- "How do you prevent cache stampede?"
> Cache stampede happens when many requests hit the database simultaneously after a cache entry expires. Two approaches: (1) background refresh — a background job refreshes popular cache entries before they expire, so they're never missing. (2) Locking — first request to find a cache miss acquires a lock, fetches from DB, and populates cache. Other requests wait briefly and then read from cache. We used background refresh for the truck dashboard — a scheduled task updated each truck's latest position in cache every few seconds.

> [!faq]- "What's the difference between Redis Streams and Pub/Sub?"
> Pub/Sub is fire-and-forget — if nobody is subscribed when a message is published, it's gone. No persistence, no replay, no acknowledgment. Streams are persistent — messages stay until you acknowledge them, you can read from any point in history, and consumer groups let multiple workers share the load. For GPS data, we needed persistence and replay (worker crash recovery). Pub/Sub would have lost data.

> [!faq]- "How do you monitor Redis in production?"
> `INFO` command gives you memory usage, connected clients, hit/miss ratio, and command statistics. We fed these metrics into Prometheus with the redis-exporter. Key alerts: memory usage > 80% (risk of OOM), hit ratio dropping (cache isn't helping), connected clients spiking (connection leak). Grafana dashboards showed real-time cache performance alongside application metrics.

---

*[[00-dashboard]]*
