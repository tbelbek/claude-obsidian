---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# SQL Databases (MSSQL, Oracle) — Quick Reference

> [!info] How I've used it: At KocSistem, SQL Server (MSSQL) was the primary database for the GPS warehouse management system — real-time truck tracking, card access, production audit. Used Dapper and Entity Framework for data access. Also worked with Oracle databases for enterprise client integrations (Arcelik, Beko, Bosch).

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#SQL Server (MSSQL)\|MSSQL]] | GPS tracking, 250 writes/sec, indexed views | [[#Oracle Integration\|Oracle]] | client ERP integrations (Arcelik, Bosch), ETL services |
| [[#Dapper vs Entity Framework\|Dapper vs EF]] | Dapper=high throughput, EF=standard CRUD | [[#Database Migrations in CI/CD\|migrations in CI]] | EF migrations in pipeline, rollback scripts |
| [[#Connection Management\|connections]] | connection pooling, min/max, dispose pattern | [[#SQL Performance Analysis — My Approach\|perf analysis]] | execution plan → missing index → bulk ops → monitor |

## HOW WE USED IT

At KocSistem, **SQL Server** was the backbone of the warehouse management system. Every GPS coordinate, every card access event, every production audit record went through MSSQL. I used both **Dapper** (for performance-critical queries — raw SQL with minimal overhead) and **Entity Framework** (for CRUD operations where developer productivity mattered more than raw speed).

The [[sd-redis-scaling|scaling challenge]] was directly related to SQL Server — 500+ trucks sending GPS data every 2 seconds overwhelmed it. The fix was splitting real-time reads to Redis and batch-writing to SQL.

For enterprise client integrations, I also worked with **Oracle** databases. Some clients (Arcelik, Bosch) had Oracle-based ERP systems that our warehouse management system needed to sync with — reading inventory levels, writing shipment confirmations, updating production schedules.

---

## Key Concepts

### What SQL Databases Are

SQL databases (relational databases) store data in tables with fixed schemas, enforce relationships through foreign keys, and guarantee ACID transactions. They excel at complex queries with JOINs, aggregations, and strong consistency. Best for: transactional data, relational data with complex queries, and scenarios where data integrity is critical. At KocSistem, SQL Server handled GPS tracking at 250 writes/sec with indexed views and SqlBulkCopy for throughput.

### SQL Server (MSSQL)
- **SqlBulkCopy** — Bulk insert API for high-throughput data loading. We used this for batch-inserting GPS coordinates — turned 250 individual inserts/second into one bulk operation every 30 seconds.
- **Indexed views** — Pre-computed query results stored as a table. We used these for the real-time dashboard — instead of computing truck positions on every page load, an indexed view kept the latest position per truck.
- **Connection pooling** — Reuse database connections across requests. Critical for high-concurrency scenarios. Default pool size (100) wasn't enough for our load — we increased it and monitored active connections.

### Dapper vs Entity Framework
- **Dapper** — Micro-ORM. You write raw SQL, Dapper maps results to C# objects. Minimal overhead. Use for performance-critical queries, complex joins, bulk operations.
- **Entity Framework** — Full ORM. Code-first or database-first. Change tracking, migrations, LINQ queries. Use for standard CRUD where developer speed matters more than query speed.
- **When I used which** — Dapper for GPS data ingestion (high volume, simple queries). EF for user management, configuration, reporting (complex models, developer convenience).

### Oracle Integration
- **Oracle.ManagedDataAccess** — .NET provider for Oracle. Used for reading from client ERP systems.
- **Challenges** — Different SQL dialects (Oracle PL/SQL vs T-SQL), different date handling, different transaction isolation defaults. Had to write adapter layers for each client's Oracle schema.
- **Data sync patterns** — Scheduled jobs pulling data from Oracle, transforming it, and loading into MSSQL. Classic ETL pattern but lightweight — no separate ETL tool, just C# background services.

### Database Migrations in CI/CD
- At KocSistem, I added database migration stages to the pipeline — run migrations against a test database snapshot, run integration tests, only apply to staging/production if tests pass. This prevented broken migrations from reaching environments where rollback is painful.

### Connection Management
- **Connection pooling** — SQL Server defaults to 100 connections per pool. At KocSistem, 500+ trucks writing GPS data required more. We increased the pool size and monitored active connections in Grafana to prevent exhaustion.
- **Connection resiliency** — Transient fault handling with retry logic. SQL Azure has occasional connection drops — Polly retry policy with exponential backoff handles this transparently.

### At KocSistem — Practical Setup
- **Dual ORM strategy** — Dapper for GPS data ingestion (high volume, simple queries, minimal overhead) and Entity Framework for application logic (user management, config, reporting — developer productivity).
- **Indexed views** — Pre-computed query results for the real-time truck dashboard. Instead of computing latest position per truck on every page load, an indexed view kept it ready.
- **Partitioning** — GPS history table partitioned by month. Old partitions archived to cheaper storage. Queries on recent data stayed fast.

### SQL Performance Analysis — My Approach

When something is slow, I follow a systematic approach:

**Step 1 — Identify the slow query:**
- Check application-level metrics first (Grafana/Prometheus) — which endpoint is slow?
- Enable query logging or use SQL Server Profiler/Extended Events to capture the actual SQL being executed
- Look at execution time, not just the query text — a query that runs fast with 100 rows might be terrible with 100,000

**Step 2 — Read the execution plan:**
- `SET STATISTICS IO ON` and `SET STATISTICS TIME ON` for basic numbers
- Actual execution plan (not estimated) — shows real row counts vs estimated
- Look for: table scans (missing index), key lookups (include columns needed), hash joins (missing join index), spills to tempdb (memory grant too small)

**Step 3 — Common fixes I've applied:**
- **Missing index** — The most common cause. SQL Server's missing index suggestions in the execution plan are a starting point, but I always validate: does this index make writes slower? Is it a duplicate of an existing index?
- **Covering index** — Add INCLUDE columns so the query can be satisfied entirely from the index without going back to the table (no key lookup)
- **Parameter sniffing** — A query plan cached for one parameter value is terrible for another. Fix: `OPTION (RECOMPILE)` for volatile queries, or use `OPTIMIZE FOR UNKNOWN`
- **N+1 in the application** — The database isn't slow, the application is making 100 queries instead of 1. Fix in the application code (joins, batch loading), not in the database
- **Bulk operations** — At KocSistem, individual inserts at 250/second overwhelmed SQL Server. Fix: [[ref-redis#HOW WE USED IT|split real-time to Redis]], batch-insert with SqlBulkCopy every 30 seconds
- **Indexed views** — Pre-computed results for expensive aggregations. Used for the real-time truck dashboard — instead of computing latest position per truck on every load, an indexed view kept it ready
- **Table partitioning** — GPS history table partitioned by month. Old partitions archived. Queries on recent data stayed fast because they only scanned the current partition

**Step 4 — Monitor after the fix:**
- Verify the execution plan changed
- Watch query duration trends in Grafana
- Check that write performance didn't degrade (new indexes slow down inserts)
- Set up alerts for query duration regression

## Sorulursa

> [!faq]- "How did you handle 250 writes/second to SQL Server?"
> We didn't — that was the problem. Direct writes at that rate overwhelmed SQL Server. The fix was splitting the path: GPS data goes to Redis first (real-time reads), then a background worker batch-inserts to SQL every 30 seconds using SqlBulkCopy. One bulk operation every 30 seconds instead of 250 individual writes per second. SQL Server handles bulk inserts much better than individual ones.

> [!faq]- "How do you choose between Dapper and Entity Framework?"
> Simple rule: if I need to think about the SQL, use Dapper. If I need to think about the domain model, use EF. Batch inserts, complex reporting queries, performance-critical reads → Dapper. CRUD endpoints, domain logic, migrations → EF. They work fine side by side in the same project — same database, different access patterns.

> [!faq]- "How do you approach SQL performance analysis?"
> Systematic: identify the slow query (application metrics → SQL profiler), read the execution plan (look for table scans, key lookups, hash joins), apply the fix (index, covering index, parameter sniffing, bulk operations), monitor after. At KocSistem, most performance issues were missing indexes or N+1 queries from the application layer — the database was rarely the root cause, the access pattern was.

> [!faq]- "What's the most common SQL performance mistake you've seen?"
> N+1 queries from the application. Developers write a loop that queries the database for each item instead of fetching all items in one query with a JOIN or IN clause. At KocSistem, this was the #1 cause of slow endpoints. Dapper makes it easy to write efficient queries — one round-trip, all the data. Entity Framework can hide N+1 behind lazy loading — I always check the SQL EF generates, not just the LINQ.

> [!faq]- "How do you decide between adding an index vs changing the query?"
> Check the execution plan. If the query logic is correct but the plan shows a table scan, add an index. If the plan shows reasonable access but the query is fetching data it doesn't need (SELECT *), fix the query. If the same table has 10+ indexes and writes are slow, consider removing redundant indexes and consolidating. Indexes are a trade-off — faster reads, slower writes. I always measure both sides.

> [!faq]- "How did the Oracle integration work?"
> Scheduled C# background services pulling data from client Oracle databases (Arcelik, Bosch ERP systems), transforming it, and loading into our MSSQL database. Classic ETL but lightweight — no separate ETL tool, just hosted services with Oracle.ManagedDataAccess. The challenge was different SQL dialects between Oracle PL/SQL and T-SQL, different date handling, and different transaction isolation defaults. I wrote adapter layers for each client's schema.

---

*[[00-dashboard]]*
