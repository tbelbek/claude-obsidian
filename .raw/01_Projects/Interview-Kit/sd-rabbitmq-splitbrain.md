---
tags:
  - interview-kit
  - interview-kit/software-dev
up: [[sd-toyota]]
---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]] > [[sd-toyota|TOYOTA MATERIAL HANDLING]] > RABBITMQ — Split-Brain*

# RABBITMQ — Split-Brain

> [!warning] **Soru:** "Tell me about a production incident" / "Tell me about a failure"

At Toyota, we were running a 3-node [[ref-rabbitmq#Clustering & Reliability|RabbitMQ]] cluster for the T-ONE forklift system using our [[ref-rabbitmq#HOW WE USED IT|custom Tmhls.Communication.RabbitMQ NuGet package]] with typed publishers, consumers, and APM (Application Performance Monitoring) diagnostic filters.

One day a temporary network blip caused a [[ref-rabbitmq#Clustering & Reliability|split-brain]] — the cluster partitioned, each side thought the other was dead, and messages got lost. Forklifts on the warehouse floor waited for commands that never came. I spent hours manually reconciling queues while operations was breathing down my neck.

After that, I dug deep into [[ref-rabbitmq#Clustering & Reliability|partition handling strategies]], switched to `pause_minority`, built cluster health monitoring, and started [[ref-rabbitmq#Reliability Patterns|chaos testing]] — intentionally killing nodes to verify reconnection logic. Full technical details in the [[ref-rabbitmq#HOW WE USED IT|RabbitMQ reference]].

This sits in my software development experience because building distributed systems means understanding how they break, not just how they work.

## Sorulursa

> [!faq]- "Why didn't you catch this in testing?"
> Our test environment had all three nodes on the same machine. There was no real network between them, so we could never get a network partition. After this incident, we set up a test environment with nodes on separate VMs and started injecting network failures as part of our test suite.

> [!faq]- "How does RabbitMQ handle split-brain?"
> RabbitMQ has a few partition handling strategies: `ignore`, `pause_minority`, and `autoheal`. We were using `ignore`, which means it does nothing — both sides keep running independently and you end up with diverged queues. We switched to `pause_minority` — the side with fewer nodes pauses and waits for the network to come back. This means some messages queue up on the publisher side, but nothing gets lost or duplicated. In our T-ONE setup, we also had DiagnosticsPublishMessageFilter and DiagnosticsReceiveMessageFilter on every publisher and consumer for APM tracing — this is how we eventually detected the partition, because the diagnostics filters showed messages being published but not consumed on the other side.

> [!faq]- "What did the chaos tests look like?"
> In the CI pipeline, we spin up a RabbitMQ container as a sidecar. The integration tests publish messages and verify consumers process them. Then we kill the container mid-test and check that the application reconnects and picks up where it left off. We also have a separate test that simulates a network partition between nodes and verifies that the cluster recovers cleanly. We also used the Tmhls.Communication.RabbitMQ.Testing package to write loopback tests — messages published and consumed in the same process, validating serialization and routing without needing a broker. For integration tests, we used the AcceptanceTests project with a real RabbitMQ container.

> [!faq]- "What would you do differently?"
> I'd never go to production with a distributed system without testing its failure modes first. Docs tell you what happens when things work. You need chaos tests to understand what happens when things break. That's a lesson I apply to every system now — not just RabbitMQ.

> [!faq]- "Technical: RabbitMQ clustering and partition handling"
> RabbitMQ clustering uses Erlang's distributed system model. Queues live on a single node by default — if that node goes down, the queue is gone unless you use mirrored queues (classic) or [[ref-rabbitmq#Clustering & Reliability|quorum queues]] (modern, [[ref-rabbitmq#Clustering & Reliability|Raft]]-based consensus). Quorum queues are what RabbitMQ recommends now — they use the Raft consensus protocol, same as etcd and Consul. Raft guarantees that a majority of nodes must agree before a message is committed, so you can't lose acknowledged messages even during a partition. We migrated from classic mirrored queues to quorum queues after the incident.

> [!faq]- "What's the CAP theorem angle here?"
> RabbitMQ with `pause_minority` trades availability for consistency — during a partition, the minority side stops accepting messages. This is the CP choice in [[ref-rabbitmq#Clustering & Reliability|CAP theorem]] terms. For our use case (forklift commands), consistency was more important than availability — it's better to queue messages on the publisher side than to deliver duplicates or lose messages.

> [!faq]- "How did you implement chaos testing?"
> We used Toxiproxy to simulate network conditions between RabbitMQ nodes — latency, packet loss, connection drops. In the CI pipeline, we used a simpler approach: Docker container kill. The test spins up RabbitMQ, publishes messages, kills the container mid-stream, brings it back, and verifies all messages are eventually delivered. It's inspired by Netflix's Chaos Monkey approach but simpler and focused on our messaging layer.

> [!faq]- "Quorum queues vs classic mirrored queues — why?"
> Classic mirrored queues have a known problem: they can lose acknowledged messages during failover. The Pivotal/VMware team documented this. Quorum queues fix this with Raft consensus — a message isn't acknowledged until a majority of nodes have it. The trade-off is slightly higher latency per publish (consensus round-trip), but for our use case the reliability was worth it.

## Also relevant to

- [[ag-resilience]] — Same incident told from the Agile/learning perspective: how it changed our team's approach to failure testing
- [[13-pillar-agile|Agile Pillar]] — Resilience and blameless post-mortems

---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]] > [[sd-toyota|TOYOTA MATERIAL HANDLING]]*
