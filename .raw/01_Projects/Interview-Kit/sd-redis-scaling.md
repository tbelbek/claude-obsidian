---
tags:
  - interview-kit
  - interview-kit/software-dev
up: [[sd-kocsistem]]
---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]] > [[sd-kocsistem|KOCSISTEM]] > REDIS — Scaling*

# REDIS — Scaling

> [!warning] **Soru:** "How do you handle scaling?" / "Performance optimization experience?"

At KocSistem, I built a GPS-based warehouse management system. With 50 trucks in testing, everything worked fine. With 500+ trucks sending coordinates every 2 seconds, the dashboard froze — 250 writes/second directly to SQL Server while the dashboard queried the same table.

I [[ref-redis#HOW WE USED IT|split the architecture]]: GPS data went into [[ref-redis#Redis Streams (What I Used)|Redis Streams]] for real-time display, a background worker batch-inserted into SQL every 30 seconds for historical queries. Dashboard went from frozen to sub-second. Full technical details in the [[ref-redis#HOW WE USED IT|Redis reference]].

I bring this up under software development because it's a pure architecture problem — the code was fine, the data model was wrong for the scale, and I had to rethink it from scratch.

## Sorulursa

> [!faq]- "Why Redis and not another cache?"
> We were already using Redis for session management in the same project. It was there, we knew it, and Redis Streams fit the use case perfectly — it's a time-series-like data structure with consumer group support. No need to bring in a new tool when the one you have does the job.

> [!faq]- "How did the batch insert work?"
> A background worker read from the Redis stream every 30 seconds, collected all the GPS points, and did a bulk insert into SQL Server using [[ref-sql-databases#SQL Server (MSSQL)|SqlBulkCopy]]. This turned 250 individual inserts per second into one bulk operation every 30 seconds. SQL Server handles bulk inserts much better than individual ones.

> [!faq]- "Did you lose data if the worker crashed?"
> No. Redis Streams keep the data until you acknowledge it. The worker uses a consumer group — if it crashes, the unacknowledged messages are still in the stream. When the worker restarts, it picks up from where it left off. We also had a health check that alerted us if the worker was down for more than 2 minutes.

> [!faq]- "What's the lesson here?"
> What works at 50 users often breaks at 500. You can't just test with small data and assume it'll scale. After this, I always do a rough calculation of expected load before choosing an architecture — writes per second, reads per second, data growth rate. If the numbers don't work on paper, they won't work in production.

> [!faq]- "Technical: Redis Streams vs Pub/Sub vs Lists"
> Redis has several data structures for messaging. Pub/Sub is fire-and-forget — if nobody's listening, the message is gone. Lists are simple queues but no consumer groups. Redis Streams (added in Redis 5.0) give you append-only log semantics with consumer groups, acknowledgment, and message replay — similar to Kafka but simpler. For our GPS use case, Streams were perfect: multiple consumers could read the same data (dashboard reads latest, batch worker reads and acknowledges), and if the batch worker crashed, unacknowledged messages stayed in the stream. The Redis documentation by Salvatore Sanfilippo explains Streams well.

> [!faq]- "Why not Kafka instead of Redis Streams?"
> We considered it. Kafka would've been technically better for pure streaming — better throughput, built-in partitioning, longer retention. But we were already running Redis for caching, and the GPS data didn't need Kafka-level durability — if we lost a few seconds of GPS data, the dashboard would just skip ahead. Adding Kafka would've meant another infrastructure component to maintain. Redis Streams was "good enough" and already there.

> [!faq]- "How did you handle Redis failover?"
> We ran Redis [[ref-redis#Sentinel (High Availability)|Sentinel]] for automatic failover — 3 Sentinel instances monitoring the primary. If the primary goes down, Sentinel promotes a replica. The application used the Sentinel-aware connection string, so it automatically reconnected to the new primary. We tested this by killing the primary during load and verifying the dashboard stayed up with a brief blip.

> [!faq]- "What about SqlBulkCopy — any gotchas?"
> SqlBulkCopy is fast but you have to be careful with column mappings and transaction handling. We wrapped each bulk insert in a transaction — if any row fails, the whole batch rolls back and gets retried. We also had to handle the schema mismatch problem: if someone adds a column to the table but doesn't update the batch worker, the insert fails silently. Added a schema validation check at worker startup.

---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]] > [[sd-kocsistem|KOCSISTEM]]*
