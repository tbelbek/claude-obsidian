---
tags:
  - education-kit
---

# SQL Databases (MSSQL, Oracle) — Education Kit

## Key Concepts

### What SQL Databases Are

SQL databases (relational databases) store data in tables with fixed schemas, enforce relationships through foreign keys, and guarantee ACID transactions. They excel at complex queries with JOINs, aggregations, and strong consistency. Best for: transactional data, relational data with complex queries, and scenarios where data integrity is critical.

### SQL Server (MSSQL)
- **SqlBulkCopy** — Bulk insert API for high-throughput data loading. Turns hundreds of individual inserts per second into one bulk operation at an interval, dramatically improving throughput.
- **Indexed views** — Pre-computed query results stored as a table. Useful for dashboards and frequent aggregation queries where recomputing on every page load is expensive.
- **Connection pooling** — Reuse database connections across requests. Critical for high-concurrency scenarios. Default pool size (100) may not be enough under heavy load — monitor active connections and adjust accordingly.

### Dapper vs Entity Framework
- **Dapper** — Micro-ORM. You write raw SQL, Dapper maps results to C# objects. Minimal overhead. Use for performance-critical queries, complex joins, bulk operations.
- **Entity Framework** — Full ORM. Code-first or database-first. Change tracking, migrations, LINQ queries. Use for standard CRUD where developer speed matters more than query speed.
- **When to use which** — Dapper for high-volume data ingestion (simple queries, minimal overhead). EF for user management, configuration, reporting (complex models, developer convenience). They work fine side by side in the same project — same database, different access patterns.

### Oracle Integration
- **Oracle.ManagedDataAccess** — .NET provider for Oracle. Used for reading from external Oracle-based ERP systems.
- **Challenges** — Different SQL dialects (Oracle PL/SQL vs T-SQL), different date handling, different transaction isolation defaults. May require adapter layers for each schema.
- **Data sync patterns** — Scheduled jobs pulling data from Oracle, transforming it, and loading into MSSQL. Classic ETL pattern but lightweight — no separate ETL tool, just C# background services.

### Database Migrations in CI/CD
- Add database migration stages to the pipeline — run migrations against a test database snapshot, run integration tests, only apply to staging/production if tests pass. This prevents broken migrations from reaching environments where rollback is painful.

### Connection Management
- **Connection pooling** — SQL Server defaults to 100 connections per pool. High-throughput scenarios may require increasing pool size. Monitor active connections to prevent exhaustion.
- **Connection resiliency** — Transient fault handling with retry logic. Cloud SQL services have occasional connection drops — Polly retry policy with exponential backoff handles this transparently.

### SQL Performance Analysis

When something is slow, follow a systematic approach:

**Step 1 — Identify the slow query:**
- Check application-level metrics first (monitoring dashboards) — which endpoint is slow?
- Enable query logging or use SQL Server Profiler/Extended Events to capture the actual SQL being executed
- Look at execution time, not just the query text — a query that runs fast with 100 rows might be terrible with 100,000

**Step 2 — Read the execution plan:**
- `SET STATISTICS IO ON` and `SET STATISTICS TIME ON` for basic numbers
- Actual execution plan (not estimated) — shows real row counts vs estimated
- Look for: table scans (missing index), key lookups (include columns needed), hash joins (missing join index), spills to tempdb (memory grant too small)

**Step 3 — Common fixes:**
- **Missing index** — The most common cause. SQL Server's missing index suggestions in the execution plan are a starting point, but always validate: does this index make writes slower? Is it a duplicate of an existing index?
- **Covering index** — Add INCLUDE columns so the query can be satisfied entirely from the index without going back to the table (no key lookup)
- **Parameter sniffing** — A query plan cached for one parameter value is terrible for another. Fix: `OPTION (RECOMPILE)` for volatile queries, or use `OPTIMIZE FOR UNKNOWN`
- **N+1 in the application** — The database is not slow, the application is making 100 queries instead of 1. Fix in the application code (joins, batch loading), not in the database
- **Bulk operations** — Individual inserts at high rates overwhelm SQL Server. Fix: batch-insert with SqlBulkCopy at intervals
- **Indexed views** — Pre-computed results for expensive aggregations. Useful for dashboards that query the same expensive aggregation repeatedly
- **Table partitioning** — Partition large tables by time period (e.g., month). Old partitions archived. Queries on recent data stay fast because they only scan the current partition

**Step 4 — Monitor after the fix:**
- Verify the execution plan changed
- Watch query duration trends in monitoring dashboards
- Check that write performance did not degrade (new indexes slow down inserts)
- Set up alerts for query duration regression

## Sorulursa

> [!faq]- "How do you handle high write throughput to SQL Server?"
> Direct writes at high rates can overwhelm SQL Server. The fix is splitting the path: data goes to an in-memory store (e.g., Redis) first for real-time reads, then a background worker batch-inserts to SQL periodically using SqlBulkCopy. One bulk operation at intervals instead of many individual writes per second. SQL Server handles bulk inserts much better than individual ones.

> [!faq]- "How do you choose between Dapper and Entity Framework?"
> Simple rule: if you need to think about the SQL, use Dapper. If you need to think about the domain model, use EF. Batch inserts, complex reporting queries, performance-critical reads — Dapper. CRUD endpoints, domain logic, migrations — EF. They work fine side by side in the same project — same database, different access patterns.

> [!faq]- "How do you approach SQL performance analysis?"
> Systematic: identify the slow query (application metrics then SQL profiler), read the execution plan (look for table scans, key lookups, hash joins), apply the fix (index, covering index, parameter sniffing, bulk operations), monitor after. Most performance issues are missing indexes or N+1 queries from the application layer — the database is rarely the root cause, the access pattern is.

> [!faq]- "What's the most common SQL performance mistake you've seen?"
> N+1 queries from the application. Developers write a loop that queries the database for each item instead of fetching all items in one query with a JOIN or IN clause. Dapper makes it easy to write efficient queries — one round-trip, all the data. Entity Framework can hide N+1 behind lazy loading — always check the SQL EF generates, not just the LINQ.

> [!faq]- "How do you decide between adding an index vs changing the query?"
> Check the execution plan. If the query logic is correct but the plan shows a table scan, add an index. If the plan shows reasonable access but the query is fetching data it does not need (SELECT *), fix the query. If the same table has 10+ indexes and writes are slow, consider removing redundant indexes and consolidating. Indexes are a trade-off — faster reads, slower writes. Always measure both sides.

> [!faq]- "How does Oracle integration typically work?"
> Scheduled C# background services pulling data from Oracle databases, transforming it, and loading into MSSQL. Classic ETL but lightweight — no separate ETL tool, just hosted services with Oracle.ManagedDataAccess. The challenge is different SQL dialects between Oracle PL/SQL and T-SQL, different date handling, and different transaction isolation defaults. Adapter layers per schema help manage the differences.
