---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Elasticsearch — Quick Reference

> [!info] How I've used it: At KocSistem, Elasticsearch for full-text search across millions of warehouse records — card access logs, production audit trails, truck GPS history.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Core Model\|core model]] | index, document, shard, replica — distributed search | [[#Search Capabilities\|search]] | full-text, fuzzy, aggregations, nested queries |
| [[#Performance\|performance]] | index lifecycle, bulk API, shard sizing | [[#vs Alternatives\|vs alternatives]] | ES=full-text+analytics, SQL=relational, Redis=cache |
| [[#HOW WE USED IT\|at KocSistem]] | millions of records, card access, GPS history, audit | | |

## HOW WE USED IT

At KocSistem, the GPS warehouse management system needed to search across millions of records — card access events, production band audits, truck movement history. SQL Server's `LIKE` queries were too slow for the volume. I added Elasticsearch as a dedicated search layer alongside SQL Server and Redis.

**What I set up:**
- Elasticsearch index for searchable records — card access logs, production audits, GPS history
- Bulk indexing from SQL Server — background job synced new records to Elasticsearch periodically
- Full-text search API — users could search across all record types with fuzzy matching, filters by date range/location/truck ID
- Index lifecycle management — old indices archived monthly to keep search performance fast

**Why Elasticsearch alongside SQL Server:** SQL Server stored the authoritative data. Elasticsearch was the search index — optimized for full-text queries, aggregations, and filtering. Write to SQL (source of truth), index to Elasticsearch (search speed), read from Redis (real-time dashboard). Each data store served its strength.

---

## Key Concepts

### What Elasticsearch Is

Elasticsearch is a distributed search and analytics engine built on Apache Lucene. It indexes documents as JSON and provides near-real-time full-text search, aggregations, and analytics across large datasets. Best for: search features (autocomplete, fuzzy matching, faceted search), log analytics (ELK stack), and any scenario where SQL LIKE queries are too slow.

### Core Model
- **Index** — Like a database table. Contains documents of the same type.
- **Document** — JSON object stored in an index. Each document has fields.
- **Mapping** — Schema definition for an index. Field types (text, keyword, date, geo_point).
- **Analyzer** — Tokenizer + filters that process text for indexing. Standard analyzer splits on whitespace and lowercases.

### Search Capabilities
- **Full-text search** — Relevance-scored search across text fields. `match` query for natural language, `term` query for exact values.
- **Fuzzy matching** — Handles typos. `"truk"` matches `"truck"` with edit distance 1.
- **Aggregations** — GROUP BY equivalent. Count events per truck, average response time per day, histogram of access times.
- **Geo queries** — Search by distance from a point, within a bounding box. Used for finding trucks near a specific warehouse gate.

### Performance
- **Sharding** — Data split across multiple shards for parallelism. More shards = more throughput but more overhead.
- **Replicas** — Each shard replicated for fault tolerance and read throughput.
- **Index lifecycle** — Create new indices periodically (daily/monthly), close old ones. Keeps active index small and fast.
- **Bulk API** — Index many documents in one request. Much faster than individual inserts.

### vs Alternatives
- **vs SQL LIKE** — Elasticsearch is orders of magnitude faster for text search. SQL LIKE does full table scans.
- **vs MongoDB text search** — Elasticsearch has more advanced text analysis, better relevance scoring, and aggregation capabilities.
- **vs Typesense/Meilisearch** — Newer, simpler alternatives. Elasticsearch is more mature and feature-rich but heavier to operate.

## Sorulursa

> [!faq]- "How did you keep Elasticsearch in sync with SQL Server?"
> Background job ran every few minutes, queried SQL for records modified since last sync, bulk-indexed them to Elasticsearch. For deletes, we used soft deletes in SQL (deleted flag) and the sync job removed them from the index. Not real-time, but the 2-3 minute delay was acceptable for our search use case.

> [!faq]- "How did you handle Elasticsearch at scale?"
> Index lifecycle management. Monthly indices — current month's index stays hot (fast SSD), older months move to warm storage. Indices older than 6 months get archived. This kept the active search dataset small and responsive. We also used index aliases so the application always queried `warehouse-records` regardless of which monthly index was behind it.

---

*[[00-dashboard]]*
