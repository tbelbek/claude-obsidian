---
tags:
  - education-kit
---
# RabbitMQ — Knowledge Base
> [!info] Message broker that routes messages between producers and consumers using exchanges, queues, and bindings — covering core model, clustering, consumer patterns, reliability, and monitoring.

---

## Key Concepts

### What RabbitMQ Is
RabbitMQ is a message broker that routes messages between producers and consumers using exchanges, queues, and bindings. Messages go to an exchange, the exchange routes them to queues based on routing rules, and consumers pull from queues. Best for: point-to-point messaging (one command → one handler), request-reply patterns, and scenarios where routing logic matters (topic-based, header-based, fanout).

### Core Model
RabbitMQ's core model has three components: exchanges receive messages, queues store them, and bindings define the routing rules between exchanges and queues. A producer sends to an exchange, the exchange routes to the right queue(s) based on routing keys and binding rules, and consumers pull from queues.

- **Exchange** — Receives messages and routes them to queues based on rules. Types: direct, topic, fanout, headers. Each service can publish to its own exchange to isolate domain events, preventing cross-contamination of different event types.
- **Queue** — Stores messages until a consumer picks them up. Durable queues survive broker restarts.
- **Binding** — Rule connecting an exchange to a queue. Includes a routing key pattern.
- **Routing key** — Label on a message. Exchange uses it to decide which queues get the message. Example: `VehicleState.Energy.*` routes energy events to the charging service, status events to the fleet dashboard.

### Clustering & Reliability
- **Split-brain** — Network partition causes the cluster to split into two independent halves. This is a real production risk in distributed RabbitMQ clusters.
- **Partition handling** — `ignore` (dangerous), `pause_minority` (safe — minority side pauses), `autoheal` (automatic recovery). `pause_minority` prevents message loss during network partitions — the minority side pauses instead of accepting messages independently.
- **Quorum queues** — Raft-based consensus. Message not acknowledged until majority of nodes have it. Replaces classic mirrored queues. More reliable, slightly higher latency. Guarantees acknowledged messages survive broker failures — classic mirrored queues could lose acked messages during failover.
- **Classic mirrored queues** — Old approach. Can lose acknowledged messages during failover. Deprecated in favor of quorum queues.

### Consumer Patterns
- **Consumer groups** — Multiple consumers sharing work from a queue. Each message goes to one consumer. Multiple services can process the same event stream independently without interfering.
- **Acknowledgment** — Consumer must ack a message after processing. Unacked messages get redelivered. Prevents message loss.
- **Dead-letter queue** — Messages that can't be processed (rejected, expired, too many retries) go here for investigation.
- **Prefetch count** — Limits how many unacked messages a consumer can have at once. Prevents one slow consumer from hoarding messages.

### Reliability Patterns
- **Publisher confirms** — Broker confirms to the publisher that a message was persisted. Without this, the publisher doesn't know if the broker received it. Critical for commands where a lost message means a stopped operation.
- **Chaos testing** — Kill the broker mid-stream, verify consumers reconnect and resume. Add this to the CI pipeline for resilience validation.
- **Reconnection logic** — Client library should auto-reconnect on connection loss. Handle this with retry + exponential backoff.

### Monitoring
- **Publish message tracing** — APM tracing on every published message. Tracks latency, errors, message counts.
- **Receive message tracing** — Same for consumed messages. Helps detect issues like split-brain because published messages aren't being consumed on the other side.
- **Management plugin** — Web UI for queue depth, message rates, connection status. Essential for debugging.

---

## Sorulursa

> [!faq]- "How do you size a RabbitMQ cluster?"
> Start with 3 nodes for quorum queues (minimum for Raft consensus). Monitor memory and disk usage — RabbitMQ can use a lot of memory for queue buffering. Set memory and disk alarms so the broker stops accepting messages before running out of resources. 3 nodes can handle thousands of messages per second — the bottleneck is rarely RabbitMQ itself, it's the consumers.

> [!faq]- "How do you handle message ordering?"
> RabbitMQ guarantees order within a single queue with a single consumer. Multiple consumers on the same queue break ordering. Use consistent hashing on entity ID — all commands for one entity go to the same queue partition, so ordering is preserved per entity.
