---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Distributed Systems — Quick Reference

> [!tip] Fundamental concepts that underpin microservices, messaging, databases, and infrastructure. Not tool-specific — applies everywhere.

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#CAP Theorem\|CAP theorem]] | CP vs AP — chose CP (pause_minority) at Toyota | [[#Consistency Models\|eventual consistency]] | Kafka events at Combination, DNS, DynamoDB |
| [[#Consensus Algorithms\|Raft]] | leader election, majority quorum, used by etcd/RabbitMQ | [[#Distributed Transactions\|saga vs 2PC]] | saga=compensating actions, 2PC=blocking coordinator |
| [[#Idempotency\|idempotency]] | retries are inevitable, design for duplicate safety | [[#Clock & Ordering\|clocks & ordering]] | vector clocks, Lamport timestamps, wall-clock drift |
| [[#Failure Modes\|split-brain]] | network partition → nodes diverge, hit this at Toyota | [[#Patterns for Reliability\|circuit breaker]] | Polly, fail fast on repeated failures, prevent cascade |
| [[#How We Deal With It (Real-World Experience)\|how we deal]] | monitoring, chaos testing, graceful degradation | | |

---

### What Distributed Systems Are
A distributed system is any system where components on different machines communicate over a network to achieve a common goal. The fundamental challenges: network is unreliable (messages get lost, delayed, duplicated), clocks drift between machines, and any node can fail at any time. Understanding these constraints — CAP theorem, consistency models, consensus, failure modes — is essential for designing microservices, databases, and messaging systems that work correctly under real-world conditions.

## CAP Theorem

**Q: What is the CAP theorem?**
A: Any distributed data store can only guarantee two of three properties simultaneously: **Consistency** (every read returns the most recent write), **Availability** (every request receives a response), **Partition tolerance** (system continues operating despite network partitions between nodes). In practice, network partitions are inevitable, so the real choice is between **CP** (consistent but may be unavailable during partition) and **AP** (always available but may return stale data).

**Q: What are examples of CP systems?**
A: **MongoDB** (with majority write concern) — during a partition, minority nodes reject writes to maintain consistency. **Redis with Sentinel** — Sentinel elects a new primary, minority side becomes unavailable. **ZooKeeper** — used for coordination, chooses consistency over availability. **etcd** — Raft-based consensus, requires majority quorum. Our choice: **RabbitMQ with pause_minority** at Toyota — during a network partition, minority side pauses itself to prevent split-brain. We chose consistency because duplicate forklift commands were more dangerous than brief unavailability.

**Q: What are examples of AP systems?**
A: **Cassandra** — always accepts writes, resolves conflicts later via last-write-wins or custom resolution. **DNS** — always returns a response, propagation takes time (eventual consistency). **DynamoDB** (default mode) — eventually consistent reads for higher availability. **Kafka** — producers can write to any broker, consumers may lag behind. Our choice: Kafka for events at Combination — we accept that consumers process events with a delay (eventual consistency) because availability of event publishing is more critical.

---

## Consistency Models

**Q: What is strong consistency?**
A: Every read returns the result of the most recent write. All nodes see the same data at the same time. Achieved via: synchronous replication, distributed locks, consensus protocols. Trade-off: higher latency (must wait for acknowledgment from multiple nodes). Example: SQL database with SERIALIZABLE isolation — every transaction sees a consistent snapshot.

**Q: What is eventual consistency?**
A: If no new updates are made, all replicas will eventually converge to the same value. Reads may temporarily return stale data. The "eventually" window is usually milliseconds to seconds, but can be longer during partitions. Examples: DNS propagation (changes take minutes/hours), Kafka consumers (lag behind producers), CDN cache (stale until TTL expires). Acceptable when: data staleness is tolerable, availability is more important.

**Q: What are causal and read-your-writes consistency?**
A: **Causal consistency** — if event A causes event B, all nodes see A before B. Unrelated events can be seen in any order. Preserves logical cause-effect without the cost of strong consistency. **Read-your-writes** — a user always sees the result of their own writes immediately. Other users may see stale data. Common implementation: route reads to the same node that handled the write, or use session-scoped caching. Important for UX — user updates their profile and immediately sees the change.

**Q: How does Combination handle consistency across services?**
A: **Within a service**: strong consistency via MongoDB transactions (single-document atomicity by default, multi-document transactions when needed). **Between services**: eventual consistency via Kafka events. When Service A updates data, it publishes an event. Service B consumes the event and updates its own data store. There is a window where the two services have different views of the world. We design UIs and APIs to tolerate this (optimistic updates, loading states, retry mechanisms).

---

## Consensus Algorithms

**Q: What is Raft and how does it work?**
A: A consensus algorithm for ensuring all nodes in a cluster agree on the same state. Three roles: **Leader** (handles all writes, replicates to followers), **Follower** (replicates leader's log), **Candidate** (during leader election). Process: (1) Leader election via randomized timeout. (2) Leader appends entries to its log. (3) Leader replicates entries to followers. (4) Once majority acknowledges, entry is committed. Used by: etcd, Consul, RabbitMQ quorum queues, CockroachDB. Designed to be understandable, unlike Paxos.

**Q: What is Paxos?**
A: The original consensus algorithm (Lamport, 1989). Proves that consensus is possible in asynchronous systems with crash failures. Three roles: Proposer, Acceptor, Learner. Notoriously difficult to understand and implement correctly. Most modern systems use Raft instead because it provides the same guarantees with a more understandable design. Multi-Paxos extends it for continuous operation (similar to Raft's log replication).

**Q: Why do consensus algorithms matter in practice?**
A: Whenever you have replicated state (database replicas, distributed config, leader election), you need consensus to ensure all nodes agree. Without it: split-brain (two leaders accepting conflicting writes), data loss (writes accepted by minority that gets overwritten), inconsistency (nodes diverge). Real impact: our RabbitMQ quorum queues use Raft to ensure messages aren't lost even if a node crashes — the message is committed only after majority acknowledgment.

---

## Distributed Transactions

**Q: What is Two-Phase Commit (2PC)?**
A: A protocol for atomic transactions across multiple nodes. **Phase 1 (Prepare)**: coordinator asks all participants "can you commit?" Each participant acquires locks, writes to WAL, responds yes/no. **Phase 2 (Commit)**: if all said yes, coordinator sends "commit" to all. If any said no, coordinator sends "abort". Problem: if coordinator crashes between phases, all participants are blocked holding locks. Not used in microservices because it creates tight coupling and fragile coordination.

**Q: What is the Saga pattern?**
A: An alternative to 2PC for distributed transactions. Each service executes a local transaction and publishes an event/sends a command. If a step fails, compensating transactions undo previous steps. Two approaches: **Choreography** — services react to events (decentralized, simple but hard to track). **Orchestration** — a central coordinator tells services what to do (centralized control, easier to understand). Trade-off: no atomicity guarantees — there's a window where the system is in an inconsistent state.

**Q: How was the Saga pattern used at Toyota?**
A: Event-driven choreography saga for transport operations. Flow: (1) Transport service assigns transport, publishes `TransportAssigned` event. (2) Vehicle service consumes event, updates vehicle state to "in-transport". If vehicle update fails: (3) Vehicle service publishes `TransportAssignmentFailed` event. (4) Transport service consumes it and rolls back transport assignment (compensating action). Each step is a local transaction in its own service's database. Kafka guaranteed event delivery between steps.

**Q: When should you avoid distributed transactions entirely?**
A: If you can redesign to keep the transaction within a single service, do that first. Co-locate tightly coupled data in the same service and database. Distributed transactions add complexity, latency, and failure modes. Ask: "do these two operations truly need to be atomic, or can the system tolerate brief inconsistency?" Often, eventual consistency with idempotent retry is simpler and more resilient than trying to enforce atomicity across services.

---

## Idempotency

**Q: Why is idempotency critical in distributed systems?**
A: The network is unreliable. Requests get lost, duplicated, or retried. If a client sends a payment request and the response is lost, the client retries — without idempotency, you charge twice. Any operation that can be retried must produce the same result regardless of how many times it's executed. HTTP: GET, PUT, DELETE are idempotent by definition. POST is not — it needs explicit idempotency handling.

**Q: How do you implement idempotency?**
A: (1) **Idempotency keys** — client generates a unique key (UUID) and sends it with the request. Server stores the key and result. On retry with same key, server returns stored result without re-executing. (2) **Natural idempotency** — design operations to be naturally idempotent. `SET balance = 100` is idempotent, `INCREMENT balance BY 10` is not. (3) **Conditional writes** — use version numbers or ETags. `UPDATE ... WHERE version = 5` only succeeds once. (4) **Deduplication table** — store processed message/event IDs, skip duplicates.

**Q: How was idempotency used in the Toyota forklift system?**
A: Forklift commands had sequence numbers assigned by the command sender. When a forklift received a command, it checked the sequence number against the last processed sequence. If the sequence number was already processed or older, the command was ignored (deduplicated). This prevented dangerous scenarios like a forklift executing the same movement command twice due to network retry, which could cause collisions or incorrect positioning in the warehouse.

---

## Clock & Ordering

**Q: Why can't you trust wall clocks in distributed systems?**
A: Wall clocks (system time) are synchronized via NTP, but synchronization is imperfect. NTP drift can be milliseconds to seconds. Leap seconds cause jumps. VMs may have clock skew after suspension/migration. If two events happen 1ms apart on different machines, you cannot reliably determine which happened first using wall clocks. This breaks any logic that depends on "event A happened before event B" based on timestamps.

**Q: What are logical clocks and vector clocks?**
A: **Lamport timestamps** (logical clock) — each node maintains a counter. Increment on local event. On send: attach counter. On receive: set counter to max(local, received) + 1. Guarantees: if A happened before B, then timestamp(A) < timestamp(B). But not the reverse — same timestamp doesn't mean concurrent. **Vector clocks** — each node maintains a vector of counters (one per node). Can detect true concurrency: if neither vector dominates the other, events are concurrent. Used by Dynamo-style databases for conflict detection.

**Q: What should you use in practice for ordering?**
A: Use monotonically increasing IDs instead of timestamps. **UUID v7** — time-ordered UUIDs, sortable, unique across nodes. **Snowflake IDs** (Twitter's approach) — 64-bit IDs encoding timestamp + node ID + sequence. **Database sequences** — auto-increment within a single database. For cross-service ordering: use Kafka partition ordering (events in the same partition are ordered) or explicit sequence numbers. Never rely on wall clock timestamps for ordering across machines.

---

## Failure Modes

**Q: What is a network partition?**
A: When network issues prevent some nodes from communicating with others, splitting the cluster into isolated groups. Each group can still function internally but cannot reach the other group. This is the "P" in CAP theorem. Example: data center A can't reach data center B due to a network link failure. Both data centers are operational, but they can't synchronize state. The system must choose: stop serving (consistency) or serve potentially stale data (availability).

**Q: What is a Byzantine failure?**
A: A node behaves arbitrarily — it may send incorrect data, lie about its state, or behave maliciously. Named after the Byzantine Generals Problem. Much harder to handle than crash failures because you can't trust the node's responses. Relevant in: blockchain/cryptocurrency (untrusted nodes), security-critical systems. Most internal distributed systems assume crash-fail model (nodes either work correctly or stop) because nodes are trusted.

**Q: What is split-brain and how did you experience it?**
A: Split-brain occurs when a cluster partitions and each partition elects its own leader, resulting in two leaders accepting conflicting writes. At Toyota: our RabbitMQ cluster experienced a network partition between nodes. Both sides promoted themselves to primary, accepted messages independently, and when the partition healed, we had conflicting message states. Resolution: configured `pause_minority` mode — during a partition, the minority side pauses itself automatically, preventing split-brain. We chose brief unavailability (CP) over conflicting data.

**Q: What is cascading failure?**
A: One service becomes slow, causing callers to accumulate waiting threads, which makes the callers slow, which makes their callers slow — cascading up the call chain. Example: Database is slow. Service A waits for DB, exhausts its thread pool. Service B calls Service A, times out, exhausts its own thread pool. API Gateway calls Service B, times out. All services are now down because of one slow database. Prevention: timeouts, circuit breakers, bulkheads, async communication.

---

## Patterns for Reliability

**Q: What is the circuit breaker pattern?**
A: Prevents cascading failure by stopping calls to a failing service. Three states: **Closed** (normal, requests flow through). **Open** (service is failing, requests fail immediately without calling the service). **Half-open** (after a timeout, allow a few test requests to check if service recovered). Transitions: closed to open after N consecutive failures. Open to half-open after timeout. Half-open to closed if test requests succeed, back to open if they fail. At Combination: implemented via Polly (.NET) with configurable thresholds.

**Q: What is the bulkhead pattern?**
A: Isolate resources (thread pools, connection pools) per dependency so that one slow dependency can't consume all resources. Named after ship bulkheads that prevent one flooded compartment from sinking the whole ship. Example: Service A calls Service B and Service C. Without bulkhead: slow Service B uses all threads, Service C calls also fail. With bulkhead: Service B gets max 20 threads, Service C gets max 20 threads. If B is slow, C is unaffected.

**Q: How should retries work in distributed systems?**
A: **Exponential backoff** — wait 1s, 2s, 4s, 8s between retries. Gives the failing service time to recover. **Jitter** — add random offset to retry delay. Without jitter: if 1000 clients all fail at once, they all retry at the same time (thundering herd). With jitter: retries are spread out. **Max retries** — cap the number of retries to prevent infinite loops. **Only retry transient failures** — retry 503 (server overloaded), don't retry 400 (bad request). Combine with circuit breaker to stop retrying when service is clearly down.

**Q: Why does every external call need a timeout?**
A: Without a timeout, a call to a slow/dead service hangs forever, holding a thread/connection. Enough hanging calls exhaust the thread pool, and your service becomes unresponsive. Default timeouts are often too high (30s-60s) or infinite. Set timeouts based on expected latency: if a call normally takes 50ms, a 2s timeout is generous. If it takes 2s, something is wrong and you should fail fast. Timeouts work with circuit breakers: enough timeouts trip the breaker.

**Q: What is graceful degradation?**
A: When a dependency is down, return a reduced but functional response instead of an error. Examples: recommendation service is down — show popular items instead of personalized ones. User profile service is down — show cached profile or just the username. Search service is down — show a static category page. Requires: identifying which dependencies are critical vs nice-to-have, having fallback logic, caching previous good responses. Better UX than a 500 error page.

**Q: What are liveness and readiness health checks?**
A: **Liveness** — "Is the process stuck?" If it fails, the container is restarted. Checks: is the process running, is it deadlocked, can it respond to basic requests. Keep it simple — don't check dependencies. **Readiness** — "Can I serve traffic?" If it fails, the pod is removed from the load balancer but not restarted. Checks: are dependencies available, is the service warmed up, has it loaded required data. A service can be alive but not ready (starting up, losing database connection).

---

## How We Deal With It (Real-World Experience)

### RabbitMQ Split-Brain at Toyota
Network partition caused RabbitMQ cluster to split. Both sides accepted messages independently, leading to conflicting state when the partition healed. Root cause: default partition handling mode allowed both sides to continue operating. Fix: configured `pause_minority` — during a partition, the side with fewer nodes pauses itself. This is a CP choice — we lose availability briefly but prevent data conflicts. For forklift command queues, consistency was critical because duplicate or conflicting commands could cause physical damage.

### Eventual Consistency at Combination
60+ microservices communicate primarily via Kafka events. When Service A updates an entity, it publishes an event. Service B (and C, D, E...) consume the event and update their own projections. There is an intentional consistency window of milliseconds to seconds. We design around this: UIs use optimistic updates (show the change immediately, reconcile on next fetch), APIs return the accepted state with appropriate caching headers, and we have reconciliation jobs that detect and fix drift between services.

### Circuit Breaker via Polly at Combination
All HTTP calls between .NET services use Polly policies: circuit breaker (open after 5 failures in 30s, half-open after 60s), retry with exponential backoff and jitter (3 retries), timeout (5s default, configurable per endpoint). These are configured as cross-cutting concerns — developers get them automatically via HttpClientFactory. When a circuit opens, we log it, alert on it, and the calling service returns a degraded response if possible.

### Saga Pattern for Cross-Service Operations
For operations spanning multiple services (e.g., creating a transport assignment that affects vehicle state and driver assignment), we use choreography-based sagas via Kafka. Each service owns its local transaction and publishes success/failure events. Compensating actions are defined for each step. Key learning: keep sagas short (2-3 steps max). If a saga has many steps, it's a sign the services are too granular and should be consolidated.

### Idempotency in Forklift Commands
Forklift commands at Toyota used sequence numbers for deduplication. The command sender assigned monotonically increasing sequence numbers. The forklift controller tracked the last processed sequence number. On receiving a command: if sequence <= last processed, ignore (idempotent). If sequence = last + 1, execute. If sequence > last + 1, request retransmission of missing commands (gap detection). This ensured exactly-once execution semantics in an unreliable wireless network environment.

---

## Sorulursa (Interview Q&A)

> [!question] "Explain CAP theorem with a real example"
> CAP says a distributed system can only guarantee two of: Consistency, Availability, Partition tolerance. Since network partitions are inevitable, the real choice is C vs A. Real example: our RabbitMQ cluster at Toyota. During a network partition, we had to choose: keep accepting messages on both sides (AP — available but inconsistent, risk duplicate/conflicting forklift commands) or pause the minority side (CP — consistent but temporarily unavailable for some clients). We chose CP with `pause_minority` because inconsistent forklift commands could cause physical damage. The brief unavailability was acceptable — forklifts would buffer commands and retry.

> [!question] "How do you handle distributed transactions?"
> We avoid them where possible by designing service boundaries so that related data lives in the same service. When we must coordinate across services, we use the Saga pattern — not 2PC. Each service performs a local transaction and publishes an event. If a downstream step fails, compensating events undo previous steps. Example at Toyota: TransportAssigned event triggers vehicle state update. If that fails, a TransportAssignmentFailed event triggers rollback. Key principles: each step is idempotent, compensating actions are defined upfront, and we accept temporary inconsistency rather than distributed locking.

> [!question] "What happens when a service goes down in your architecture?"
> Multiple layers of protection. (1) K8s detects unhealthy pods via liveness probes and restarts them. (2) Readiness probes remove unhealthy pods from the load balancer — traffic goes to healthy pods. (3) Circuit breakers (Polly) prevent cascading failure — callers fail fast instead of waiting. (4) Graceful degradation — services return cached or default responses for non-critical dependencies. (5) Async communication via Kafka means events are buffered and processed when the service recovers — no data loss. (6) Alerts fire, on-call engineer investigates. Most incidents are self-healing via K8s restarts.

> [!question] "How do you ensure message ordering in a distributed system?"
> Kafka guarantees ordering within a partition. We use entity ID as the partition key — all events for the same entity go to the same partition, so they're processed in order. Example: all events for Vehicle ID 123 go to partition 7 and are consumed in order. Trade-off: ordering is only per-entity, not global. For global ordering you'd need a single partition (kills throughput). In practice, per-entity ordering is sufficient — you need Vehicle 123's events in order, but you don't need Vehicle 123's events ordered relative to Vehicle 456's events.

> [!question] "Strong vs eventual consistency — how do you choose?"
> Ask: "What happens if a user reads stale data for a few seconds?" If the answer is "nothing bad, they refresh and see the update" — eventual consistency is fine (product catalog, social feeds, analytics). If the answer is "money is lost, safety is compromised, or data is corrupted" — use strong consistency (financial transactions, inventory counts, forklift commands). At Combination: strong consistency within each service (MongoDB transactions), eventual consistency between services (Kafka events). Most user-facing reads are eventually consistent with optimistic UI updates. Financial and safety-critical paths use synchronous calls with strong consistency.
