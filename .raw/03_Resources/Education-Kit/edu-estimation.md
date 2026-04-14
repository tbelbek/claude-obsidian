---
tags:
  - education-kit
---

# Back-of-Envelope Estimation — Education Kit

## What Back-of-Envelope Estimation Is

Back-of-envelope estimation is the skill of quickly calculating approximate system requirements — traffic (QPS), storage, bandwidth, number of servers — using rough math and reference numbers. It's the first step in any system design interview: before choosing databases, caches, or load balancers, you need to know the scale. The goal is not exact numbers — it's demonstrating structured thinking and arriving at a reasonable order of magnitude.

## Framework: 5-Step Estimation Process

1. **Clarify** — What exactly are we estimating? What assumptions can I make? (DAU, read/write ratio, data retention)
2. **Estimate traffic** — DAU -> requests per second (QPS)
3. **Estimate storage** — Per-record size x records per day x retention period
4. **Estimate bandwidth** — QPS x average payload size
5. **Pick components** — Use the numbers to justify choices (single server vs distributed, SQL vs NoSQL, cache needed or not)

---

## Reference Numbers to Memorize

| Item | Size / Speed |
|---|---|
| 1 ASCII character | 1 byte |
| 1 UUID / GUID | 36 bytes (string), 16 bytes (binary) |
| 1 long URL | ~200 bytes |
| 1 short URL hash (7 chars) | 7 bytes |
| 1 tweet / short text | ~250 bytes |
| 1 metadata record (JSON) | ~1 KB |
| 1 thumbnail image | ~10 KB |
| 1 photo (compressed) | ~300 KB |
| 1 HD photo | ~2 MB |
| 1 minute of audio (MP3) | ~1 MB |
| 1 minute of video (720p) | ~50 MB |
| 1 minute of video (1080p) | ~150 MB |
| 1 minute of video (4K) | ~500 MB |

| Component | Latency / Throughput |
|---|---|
| L1 cache reference | 0.5 ns |
| L2 cache reference | 7 ns |
| Main memory reference | 100 ns |
| SSD random read | 100 us |
| HDD random read | 10 ms |
| Network round trip (same datacenter) | 0.5 ms |
| Network round trip (cross-continent) | 150 ms |
| Read 1 MB sequentially from memory | 250 us |
| Read 1 MB sequentially from SSD | 1 ms |
| Read 1 MB sequentially from HDD | 20 ms |
| Send 1 MB over 1 Gbps network | 10 ms |

| Server Capacity | Approximate Value |
|---|---|
| 1 server — concurrent connections | ~10K (with async I/O) |
| 1 server — QPS (web API) | ~1K-10K (depends on work per request) |
| 1 server — QPS (cache, Redis) | ~100K |
| 1 database server — QPS (SQL) | ~1K-5K (depends on query complexity) |
| 1 database server — QPS (NoSQL) | ~10K-50K |

## Power-of-Two Quick Reference

| Power | Approximate Value | Common Name |
|---|---|---|
| 2^10 | 1 Thousand | 1 KB |
| 2^20 | 1 Million | 1 MB |
| 2^30 | 1 Billion | 1 GB |
| 2^40 | 1 Trillion | 1 TB |
| 2^50 | 1 Quadrillion | 1 PB |

## Time Conversions

| Period | Seconds |
|---|---|
| 1 day | ~86,400 ~ ~100K |
| 1 month | ~2.5 Million |
| 1 year | ~30 Million |

---

## Common Estimation Formulas

**DAU -> QPS:**
- QPS = DAU x (average requests per user per day) / 86,400
- Peak QPS = QPS x 2 (or x3 for spiky traffic)
- Example: 10M DAU, 10 requests/user/day -> 10M x 10 / 100K ~ 1,000 QPS, peak ~ 2,000-3,000 QPS

**Storage estimation:**
- Daily storage = new records per day x record size
- Total storage = daily storage x retention period (days)
- Example: 100M new records/day x 1 KB/record = 100 GB/day. 3 years retention = 100 GB x 1,095 ~ 110 TB

**Bandwidth estimation:**
- Incoming = QPS x average request size
- Outgoing = QPS x average response size
- Example: 1,000 QPS x 1 KB request = 1 MB/s incoming. 1,000 QPS x 10 KB response = 10 MB/s outgoing = 80 Mbps

**Number of servers:**
- Servers = Peak QPS / QPS per server
- Add 30-50% headroom for failover and rolling deployments
- Example: 3,000 peak QPS / 1,000 QPS per server = 3 servers + headroom = 5 servers

**Cache sizing (80/20 rule):**
- 20% of data serves 80% of reads
- Cache size = 20% x (daily read data volume)
- Example: 1M reads/day x 1 KB = 1 GB daily reads. Cache = 200 MB

---

## Practice Problems with Worked Solutions

### Problem 1: "How much storage does a URL shortener need?"

**Clarify:** 100M new URLs/month, keep for 5 years, store original URL + short code + metadata.

**Calculate:**
- Record size: short code (7 bytes) + long URL (200 bytes) + created timestamp (8 bytes) + metadata (50 bytes) ~ 265 bytes ~ 300 bytes
- Monthly: 100M x 300 bytes = 30 GB/month
- 5 years: 30 GB x 60 months = 1.8 TB
- With replication (3x): ~5.4 TB

**Conclusion:** ~2 TB primary storage. Fits on a single modern server's SSD, but use a distributed database for availability. Read-heavy workload (100:1 read:write), so add a cache layer.

### Problem 2: "How many servers for 1M concurrent users?"

**Clarify:** Real-time messaging app, each user maintains a WebSocket connection, sends ~1 message/minute.

**Calculate:**
- Connections: 1 server handles ~10K concurrent connections
- Servers for connections: 1M / 10K = 100 servers
- Message QPS: 1M users x 1 msg/min / 60 = ~17K messages/second
- Each message needs: receive, store, fan out = ~3 operations = 50K ops/sec
- At 5K ops/server -> 10 application servers

**Conclusion:** ~100 WebSocket servers + ~10 application servers + database layer. ~120 servers plus redundancy.

### Problem 3: "How much bandwidth for a video streaming service?"

**Clarify:** 10M DAU, average 30 min/day of video, mix of 720p and 1080p (~100 MB/min).

**Calculate:**
- Daily video consumed: 10M users x 30 min = 300M minutes/day
- Daily bandwidth: 300M min x 100 MB/min = 30 PB/day
- More realistic for a startup: 100K DAU x 30 min x 50 MB/min = 150 TB/day ~ 1.7 GB/s ~ 14 Gbps

**Conclusion:** Video streaming is bandwidth-dominated. Use CDN for edge caching (90%+ of traffic). Adaptive bitrate reduces average bandwidth.

---

## Tips for Estimation Interviews

- **Round aggressively** — Use 100K instead of 86,400 for seconds in a day. The goal is order of magnitude, not precision.
- **State assumptions explicitly** — "I'll assume 10 requests per user per day" shows structured thinking.
- **Work top-down** — Start with the big number (DAU, total users) and derive everything from it.
- **Sanity check** — Compare your result to known systems. YouTube serves 1B hours/day. Twitter handles ~300K QPS at peak.
- **Show the trade-offs** — "This needs 5 TB of storage, so a single server could hold it, but for availability we'd use 3 replicas across 3 zones."

---

## Common Questions

**"How do you approach a back-of-envelope estimation when you don't know the exact numbers?"**
Start with what you know and state assumptions explicitly. A day has ~100K seconds, a server handles ~10K connections, a typical API does ~1K-5K QPS. The interviewer cares about the approach — breaking a big question into smaller, estimable pieces — not the exact right number. Always sanity-check against known systems.

**"When does estimation actually matter in real engineering decisions?"**
It matters most when deciding architecture: do we need a cache? (yes, if QPS exceeds database capacity). Do we need sharding? (yes, if storage exceeds single-node capacity). Do we need a CDN? (yes, if bandwidth is in Gbps). It also matters for cost estimation — cloud bills are driven by storage, bandwidth, and compute.

**"How accurate do these estimates need to be?"**
Within an order of magnitude. If the real answer is 500 QPS and you estimate 1,000 QPS, that's fine — both lead to the same architecture decisions. If you estimate 500 and the real answer is 50,000, that's a problem. The goal is to be close enough to make correct architectural choices.
