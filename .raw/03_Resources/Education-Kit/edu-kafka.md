---
tags:
  - education-kit
---
# Kafka — Knowledge Base
> [!info] Distributed event streaming platform — a durable, ordered, append-only log covering topics, partitions, consumer groups, Kafka vs RabbitMQ, topic management, and reliability patterns.

---

## Key Concepts

### What Kafka Is
Apache Kafka is a distributed event streaming platform — a durable, ordered, append-only log that multiple producers write to and multiple consumers read from independently. Unlike traditional message queues, Kafka retains events for a configurable period, so consumers can replay from any point. Best for: event-driven architectures where multiple services need to react to the same event independently, data pipeline ingestion, and any scenario requiring high-throughput, durable message processing.

### Core Model
Kafka's core model is a distributed commit log: producers write events to topics, topics are split into partitions for parallelism, and consumers read from partitions at their own pace using consumer groups. Unlike traditional queues, messages aren't deleted after consumption — they stay for a configurable retention period.

- **Topics** — Named streams of events. Each topic can have multiple partitions.
- **Partitions** — Ordered, immutable log of events. Enables parallelism — multiple consumers can read different partitions simultaneously.
- **Producers** — Write events to topics. Choose partition by key (e.g., user ID) for ordering guarantees.
- **Consumers** — Read events from topics. Consumer groups enable load balancing across instances.
- **Offsets** — Position in the log. Consumers track their offset — can replay from any point.

### Kafka vs RabbitMQ
- **Kafka** — Distributed log. Events persist for a retention period. Multiple consumers can read the same events independently. Better for event streaming, analytics, and fan-out.
- **RabbitMQ** — Message broker. Messages consumed and removed. Better for point-to-point commands and request/reply patterns.
- **When to choose** — Kafka for domain events (multiple consumers), RabbitMQ for commands (single consumer per command).

### Topic Management
- **Partitioning** — More partitions = more parallelism, but more overhead. Size based on expected throughput and consumer count.
- **Retention** — How long events are kept. Default 7 days. Some topics (audit events) kept longer.
- **Compaction** — Keep only the latest event per key. Used for state snapshots.

### Reliability
- **Replication** — Each partition replicated across multiple brokers. If one broker dies, others have the data.
- **Acks** — Producer can wait for `acks=all` (all replicas confirm) for maximum durability, or `acks=1` for speed.
- **Exactly-once semantics** — Kafka supports idempotent producers and transactional writes for exactly-once delivery.

---

## Sorulursa

> [!faq]- "Why Kafka for events and not just RabbitMQ everywhere?"
> Different tools for different patterns. RabbitMQ is great for command-style messaging where one consumer processes each message. Kafka is better when multiple services need to react to the same event independently — one event, many consumers. A single domain event (like "user updated profile") might be consumed by the feed service, the search service, the notification service, and the analytics pipeline. Kafka's consumer group model handles this naturally.

> [!faq]- "How do you handle Kafka in CI/CD?"
> Topic creation and configuration are managed as infrastructure as code. In integration tests, use embedded Kafka (Confluent's testcontainers) to test producer/consumer logic without needing a real cluster.

> [!faq]- "How do you handle schema evolution in Kafka?"
> Use schema registry with Avro or Protobuf schemas. Producers register schemas before publishing. Consumers validate against the registry. Backward-compatible changes (adding optional fields) are allowed. Breaking changes require a new topic version. This prevents producers from publishing events that consumers can't deserialize.
