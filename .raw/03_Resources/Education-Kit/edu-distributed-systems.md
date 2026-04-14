---
tags:
  - education-kit
---

# Distributed Systems — Education Kit

## What Distributed Systems Are

A distributed system is any system where components on different machines communicate over a network to achieve a common goal. The fundamental challenges: network is unreliable (messages get lost, delayed, duplicated), clocks drift between machines, and any node can fail at any time. Understanding these constraints — CAP theorem, consistency models, consensus, failure modes — is essential for designing microservices, databases, and messaging systems that work correctly under real-world conditions.

## CAP Theorem

**What is the CAP theorem?**
Any distributed data store can only guarantee two of three properties simultaneously: **Consistency** (every read returns the most recent write), **Availability** (every request receives a response), **Partition tolerance** (system continues operating despite network partitions between nodes). In practice, network partitions are inevitable, so the real choice is between **CP** (consistent but may be unavailable during partition) and **AP** (always available but may return stale data).

**Examples of CP systems:**
MongoDB (with majority write concern), Redis with Sentinel, ZooKeeper, etcd — these choose consistency, meaning minority nodes may become unavailable during a partition.

**Examples of AP systems:**
Cassandra (always accepts writes, resolves conflicts later), DNS (always returns a response, propagation takes time), DynamoDB (default mode), Kafka (producers can write to any broker, consumers may lag).

## Consistency Models

**Strong consistency** — Every read returns the result of the most recent write. All nodes see the same data at the same time. Achieved via synchronous replication, distributed locks, or consensus protocols. Trade-off: higher latency.

**Eventual consistency** — If no new updates are made, all replicas will eventually converge to the same value. Reads may temporarily return stale data. The window is usually milliseconds to seconds. Examples: DNS propagation, Kafka consumers, CDN caches. Acceptable when data staleness is tolerable.

**Causal consistency** — If event A causes event B, all nodes see A before B. Unrelated events can be seen in any order. Preserves logical cause-effect without the cost of strong consistency.

**Read-your-writes** — A user always sees the result of their own writes immediately. Other users may see stale data. Common implementation: route reads to the same node that handled the write, or use session-scoped caching.

## Consensus Algorithms

**Raft** — A consensus algorithm for ensuring all nodes in a cluster agree on the same state. Three roles: Leader (handles all writes), Follower (replicates leader's log), Candidate (during leader election). Leader election via randomized timeout, entries committed once majority acknowledges. Used by: etcd, Consul, RabbitMQ quorum queues, CockroachDB.

**Paxos** — The original consensus algorithm (Lamport, 1989). Proves that consensus is possible in asynchronous systems with crash failures. Notoriously difficult to understand and implement. Most modern systems use Raft instead.

**Why consensus matters in practice** — Whenever you have replicated state, you need consensus to ensure all nodes agree. Without it: split-brain, data loss, inconsistency.

## Distributed Transactions

**Two-Phase Commit (2PC)** — Coordinator asks all participants "can you commit?" If all say yes, commit. If any says no, abort. Problem: if coordinator crashes between phases, all participants are blocked holding locks. Not used in microservices because it creates tight coupling.

**Saga pattern** — Each service executes a local transaction and publishes an event/sends a command. If a step fails, compensating transactions undo previous steps. Two approaches: Choreography (decentralized, simple but hard to track) and Orchestration (centralized control, easier to understand). Trade-off: no atomicity guarantees — there's a window of inconsistency.

**When to avoid distributed transactions** — If you can redesign to keep the transaction within a single service, do that first. Co-locate tightly coupled data in the same service. Distributed transactions add complexity, latency, and failure modes.

## Idempotency

**Why idempotency is critical** — The network is unreliable. Requests get lost, duplicated, or retried. Any operation that can be retried must produce the same result regardless of how many times it's executed. HTTP: GET, PUT, DELETE are idempotent by definition. POST is not — it needs explicit idempotency handling.

**How to implement idempotency:**
1. **Idempotency keys** — Client generates a unique key (UUID) and sends it with the request. Server stores the key and result. On retry, returns stored result without re-executing.
2. **Natural idempotency** — Design operations to be naturally idempotent. `SET balance = 100` is idempotent, `INCREMENT balance BY 10` is not.
3. **Conditional writes** — Use version numbers or ETags. `UPDATE ... WHERE version = 5` only succeeds once.
4. **Deduplication table** — Store processed message/event IDs, skip duplicates.

## Clock & Ordering

**Why you can't trust wall clocks** — Wall clocks are synchronized via NTP, but synchronization is imperfect. NTP drift can be milliseconds to seconds. If two events happen 1ms apart on different machines, you cannot reliably determine which happened first using wall clocks.

**Logical clocks** — Lamport timestamps: each node maintains a counter. Increment on local event. On send: attach counter. On receive: set counter to max(local, received) + 1. Guarantees: if A happened before B, then timestamp(A) < timestamp(B).

**Vector clocks** — Each node maintains a vector of counters (one per node). Can detect true concurrency: if neither vector dominates the other, events are concurrent. Used by Dynamo-style databases for conflict detection.

**What to use in practice** — Monotonically increasing IDs instead of timestamps. UUID v7 (time-ordered), Snowflake IDs (Twitter's approach), or Kafka partition ordering. Never rely on wall clock timestamps for ordering across machines.

## Failure Modes

**Network partition** — When network issues prevent some nodes from communicating with others. The system must choose: stop serving (consistency) or serve potentially stale data (availability).

**Byzantine failure** — A node behaves arbitrarily — it may send incorrect data, lie about its state, or behave maliciously. Relevant in blockchain and security-critical systems. Most internal distributed systems assume crash-fail model (nodes either work correctly or stop).

**Split-brain** — A cluster partitions and each partition elects its own leader, resulting in two leaders accepting conflicting writes. Prevention: `pause_minority` mode — during a partition, the minority side pauses itself automatically.

**Cascading failure** — One service becomes slow, causing callers to accumulate waiting threads, which makes the callers slow, cascading up the call chain. Prevention: timeouts, circuit breakers, bulkheads, async communication.

## Patterns for Reliability

**Circuit breaker** — Prevents cascading failure by stopping calls to a failing service. Three states: Closed (normal), Open (fail immediately), Half-open (test requests). Transitions based on failure thresholds.

**Bulkhead** — Isolate resources per dependency so one slow dependency can't consume all resources. Like watertight compartments on a ship.

**Retries** — Exponential backoff (wait 1s, 2s, 4s, 8s). Jitter (add randomness to prevent thundering herd). Max retries to prevent infinite loops. Only retry transient failures.

**Timeouts** — Every external call needs a timeout. Without it, a call to a dead service hangs forever, holding a thread/connection.

**Graceful degradation** — When a dependency is down, return a reduced but functional response instead of an error. Show popular items instead of personalized recommendations. Show cached profiles instead of live data.

**Health checks** — Liveness ("is the process stuck?"), Readiness ("can it serve traffic?"). A service can be alive but not ready (starting up, losing database connection).

---

## Common Questions

**"Explain CAP theorem with a real example"**
CAP says a distributed system can only guarantee two of: Consistency, Availability, Partition tolerance. Since network partitions are inevitable, the real choice is C vs A. Example: during a network partition in a message broker cluster, you must choose between keeping both sides accepting messages (AP — available but inconsistent, risk of duplicate or conflicting messages) or pausing the minority side (CP — consistent but temporarily unavailable).

**"How do you handle distributed transactions?"**
Avoid them where possible by designing service boundaries so that related data lives in the same service. When you must coordinate across services, use the Saga pattern — not 2PC. Each service performs a local transaction and publishes an event. Key principles: each step is idempotent, compensating actions are defined upfront, and you accept temporary inconsistency rather than distributed locking.

**"Strong vs eventual consistency — how do you choose?"**
Ask: "What happens if a user reads stale data for a few seconds?" If the answer is "nothing bad" — eventual consistency is fine (product catalog, social feeds, analytics). If the answer is "money is lost, safety is compromised, or data is corrupted" — use strong consistency (financial transactions, inventory counts, safety-critical commands).
