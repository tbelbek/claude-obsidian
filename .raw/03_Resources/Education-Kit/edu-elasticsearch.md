---
tags:
  - education-kit
---

# Elasticsearch — Education Kit

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
- **Aggregations** — GROUP BY equivalent. Count events per category, average response time per day, histogram of access times.
- **Geo queries** — Search by distance from a point, within a bounding box. Useful for location-based search features.

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

> [!faq]- "How do you keep Elasticsearch in sync with a primary database?"
> Background job runs periodically, queries the primary database for records modified since last sync, bulk-indexes them to Elasticsearch. For deletes, use soft deletes (deleted flag) and the sync job removes them from the index. Not real-time, but a 2-3 minute delay is typically acceptable for search use cases.

> [!faq]- "How do you handle Elasticsearch at scale?"
> Index lifecycle management. Create time-based indices (e.g., monthly) — the current index stays hot (fast SSD), older indices move to warm storage. Very old indices get archived. This keeps the active search dataset small and responsive. Use index aliases so the application always queries a stable name regardless of which time-based index is behind it.
