---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# RabbitMQ — Quick Reference

> [!info] How I've used it: Real-time messaging for autonomous forklifts at Toyota (T-ONE). Custom Tmhls.Communication.RabbitMQ NuGet package with typed publishers/consumers. Dealt with split-brain, built chaos tests, implemented APM tracing filters.

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Core Model\|exchange/queue/binding]] | exchange routes → queue via binding rules | [[#Core Model\|routing key]] | pattern matching (VehicleState.Energy.*) |
| [[#Clustering & Reliability\|split-brain]] | network partition, nodes diverge — hit at Toyota | [[#Clustering & Reliability\|pause_minority]] | minority stops, prevents divergence |
| [[#Clustering & Reliability\|quorum queues]] | Raft consensus, replicated, durable | [[#Consumer Patterns\|consumer groups]] | competing consumers, load balancing |
| [[#Consumer Patterns\|acknowledgment]] | manual ack, nack=retry or DLQ | [[#Reliability Patterns\|publisher confirms]] | broker confirms receipt, async safety |
| [[#Reliability Patterns\|chaos testing]] | kill container mid-test, verify reconnection | [[#Monitoring\|monitoring]] | queue depth, consumer lag, connection count |
| [[#HOW WE USED IT\|custom NuGet]] | IConsumerProvider/IPublisherProvider, typed events | | |

## HOW WE USED IT

At Toyota, RabbitMQ was the messaging backbone for T-ONE — real-time commands to autonomous forklifts and status updates back. We built a custom NuGet package (`Tmhls.Communication.RabbitMQ`) with typed messaging.

**What we built:**
- Custom NuGet package with `IConsumerProvider` and `IPublisherProvider` interfaces — type-safe publishers and consumers, no raw string routing
- Typed domain events: `VehicleStateEnergyEvent`, `VehicleStateStatusEvent` — each with routing keys like `VehicleState.Energy.*` and `VehicleState.Status.*`
- Per-service exchanges — Vehicles service published to its own exchange, Transport service to its own. Consumers subscribed to specific routing key patterns
- `DiagnosticsPublishMessageFilter` and `DiagnosticsReceiveMessageFilter` on every publisher/consumer for APM tracing — this is how we eventually detected the [[sd-rabbitmq-splitbrain|split-brain]], because published messages weren't being consumed on the other side
- Loopback testing via `Tmhls.Communication.RabbitMQ.Testing` — messages published and consumed in the same process for unit-level validation
- AcceptanceTests project with real RabbitMQ container for integration testing
- After the split-brain: chaos step in CI that kills the RabbitMQ container mid-test to verify reconnection logic

**Why RabbitMQ over Kafka at Toyota:** Point-to-point commands to specific forklifts. Each command goes to one consumer. RabbitMQ's routing key model maps naturally to this. Kafka's consumer group model is better for fan-out (one event, many consumers) — which is what we use at Combination.

---

## Key Concepts

### What RabbitMQ Is
RabbitMQ is a message broker that routes messages between producers and consumers using exchanges, queues, and bindings. Messages go to an exchange, the exchange routes them to queues based on routing rules, and consumers pull from queues. Best for: point-to-point messaging (one command → one handler), request-reply patterns, and scenarios where routing logic matters (topic-based, header-based, fanout).

### Core Model
RabbitMQ's core model has three components: exchanges receive messages, queues store them, and bindings define the routing rules between exchanges and queues. A producer sends to an exchange, the exchange routes to the right queue(s) based on routing keys and binding rules, and consumers pull from queues.

- **Exchange** — Receives messages and routes them to queues based on rules. Types: direct, topic, fanout, headers. *(we used this to isolate domain events per service at Toyota — each service published to its own exchange, preventing cross-contamination of vehicle commands and transport events)*
- **Queue** — Stores messages until a consumer picks them up. Durable queues survive broker restarts.
- **Binding** — Rule connecting an exchange to a queue. Includes a routing key pattern.
- **Routing key** — Label on a message. Exchange uses it to decide which queues get the message. Example: `VehicleState.Energy.*` *(we used this to route forklift state updates to the right consumers at Toyota — energy events went to the charging service, status events went to the fleet dashboard)*

### Clustering & Reliability
- **Split-brain** — Network partition causes the cluster to split into two independent halves. [[sd-rabbitmq-splitbrain|I dealt with this in production]].
- **Partition handling** — `ignore` (dangerous), `pause_minority` (safe — minority side pauses), `autoheal` (automatic recovery). *(we switched to this to prevent message loss during network partitions at Toyota — the minority side pauses instead of accepting messages independently)*
- **Quorum queues** — Raft-based consensus. Message not acknowledged until majority of nodes have it. Replaces classic mirrored queues. More reliable, slightly higher latency. *(we migrated to this to guarantee acknowledged messages survive broker failures — classic mirrored queues could lose acked messages during failover)*
- **Classic mirrored queues** — Old approach. Can lose acknowledged messages during failover. Deprecated in favor of quorum queues.

### Consumer Patterns
- **Consumer groups** — Multiple consumers sharing work from a queue. Each message goes to one consumer. *(we used this to let multiple services process the same event stream independently at Toyota — vehicle service and dashboard service both consumed state events without interfering)*
- **Acknowledgment** — Consumer must ack a message after processing. Unacked messages get redelivered. Prevents message loss.
- **Dead-letter queue** — Messages that can't be processed (rejected, expired, too many retries) go here for investigation.
- **Prefetch count** — Limits how many unacked messages a consumer can have at once. Prevents one slow consumer from hoarding messages.

### Reliability Patterns
- **Publisher confirms** — Broker confirms to the publisher that a message was persisted. Without this, the publisher doesn't know if the broker received it. *(we used this to guarantee forklift commands were received by the broker — a lost command means a forklift stops on the warehouse floor)*
- **Chaos testing** — Kill the broker mid-stream, verify consumers reconnect and resume. [[sd-rabbitmq-splitbrain|We added this to our CI pipeline]].
- **Reconnection logic** — Client library should auto-reconnect on connection loss. Our custom package handled this with retry + exponential backoff.

### Monitoring
- **DiagnosticsPublishMessageFilter** — APM tracing on every published message. Tracks latency, errors, message counts.
- **DiagnosticsReceiveMessageFilter** — Same for consumed messages. Helped us detect the split-brain because published messages weren't being consumed on the other side.
- **Management plugin** — Web UI for queue depth, message rates, connection status. Essential for debugging.

## Sorulursa

> [!faq]- "How do you size a RabbitMQ cluster?"
> Start with 3 nodes for quorum queues (minimum for Raft consensus). Monitor memory and disk usage — RabbitMQ can use a lot of memory for queue buffering. Set memory and disk alarms so the broker stops accepting messages before running out of resources. For our T-ONE system, 3 nodes handled thousands of messages per second — the bottleneck was never RabbitMQ, it was our consumers.

> [!faq]- "How do you handle message ordering?"
> RabbitMQ guarantees order within a single queue with a single consumer. Multiple consumers on the same queue break ordering. For T-ONE, we used consistent hashing on vehicle ID — all commands for one forklift go to the same queue partition, so ordering is preserved per vehicle.

> [!faq]- "Does publisher confirms + consumer ack + quorum queues give you exactly-once delivery?"
> No. Exactly-once delivery is impossible in distributed systems (proven by the Two Generals Problem). What each piece guarantees:
> - **Publisher confirms**: Message reached the broker and was persisted to a majority of quorum queue members. Closes the "fire and forget" gap — publisher knows the broker has it. Does NOT guarantee the consumer will process it.
> - **Consumer manual ack**: Broker won't remove the message until the consumer explicitly acks. Closes the "consumer crash before processing" gap. But if the consumer processes the message and crashes before acking, the broker redelivers — causing duplicate processing.
> - **Quorum queues (Raft)**: Message survives broker node failures (majority must persist before ack to publisher). Closes the "broker crash loses messages" gap. Does NOT prevent duplicate delivery to consumers.
> 
> **The open gap**: Between "consumer processes message" and "consumer sends ack" there is always a window where a crash causes redelivery. This makes the system at-least-once, never exactly-once.

> [!faq]- "How do you make at-least-once safe for physical actuators (forklifts)?"
> **Idempotency at the device level, not just the service level.** Each command carries a unique CommandID (UUID) and a monotonic sequence number per vehicle. The forklift's onboard controller maintains a last-processed sequence number. If a command arrives with sequence ≤ last-processed, it's a duplicate — acknowledge but don't execute. This is enforced on the forklift side because the service side can have multiple instances and race conditions. The service side also maintains a command state machine (PENDING → SENT → ACKED_BY_VEHICLE → EXECUTING → COMPLETED) — if a redelivered message arrives and the state is already SENT or beyond, skip it. Defense in depth: both sides reject duplicates.

> [!faq]- "Dead-letter MOVE command: retry or alarm?"
> **Alarm, not retry.** In a physical system, a stale MOVE command is dangerous — the warehouse state may have changed (another forklift now occupies that path, a human entered the zone). Blindly retrying a minutes-old MOVE command could cause a collision. Dead-lettered commands should: (1) trigger an immediate alert to the fleet management system, (2) put the affected forklift into SAFE_STOP state, (3) require human operator review before resuming. "Message lost" (forklift stops and waits) is safer than "message replayed" (forklift moves based on stale state). In safety-critical systems, fail-safe beats fail-operational.

---

*[[00-dashboard]]*
