---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Dapper — Quick Reference

> [!info] How I've used it: At KocSistem, Dapper for performance-critical GPS data ingestion (high volume, simple queries). Entity Framework for standard CRUD. The choice was deliberate — right tool for each job.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#What Dapper Is\|what Dapper is]] | micro-ORM, raw SQL, minimal overhead, ~10x faster than EF | [[#Dapper vs Entity Framework\|vs EF]] | Dapper=high throughput, EF=CRUD+change tracking |
| [[#Common Patterns\|patterns]] | parameterized queries, multi-mapping, SqlBulkCopy | [[#HOW WE USED IT\|GPS ingestion]] | 250 writes/sec, SqlBulkCopy batch inserts at KocSistem |

## HOW WE USED IT

At KocSistem, the GPS warehouse management system had two data access patterns: high-volume GPS coordinate ingestion (250 writes/second) and standard application CRUD (user management, configuration). I used Dapper for the first and Entity Framework for the second.

Dapper was essential for the [[sd-redis-scaling|scaling fix]] — after splitting real-time reads to Redis, the batch writer used Dapper with [[ref-sql-databases#SQL Server (MSSQL)|SqlBulkCopy]] for bulk inserts to SQL Server. The overhead difference was significant: Entity Framework added ~5ms per operation for change tracking and object mapping. At 250 operations/second, that's 1.25 seconds of pure overhead per second — unacceptable.

---

## Key Concepts

### What Dapper Is
- **Micro-ORM** — Thin mapping layer between SQL and C# objects. You write raw SQL, Dapper maps results to typed objects.
- **Performance** — Near-raw ADO.NET speed. No change tracking, no lazy loading, no query translation overhead.
- **Extension methods** — Adds `Query<T>`, `Execute`, `QueryMultiple` to `IDbConnection`. Minimal API surface.

### Dapper vs Entity Framework
- **Dapper** — You write SQL. Full control over queries. Fast. Use for: bulk operations, complex joins, performance-critical paths, read-heavy queries.
- **Entity Framework** — You write LINQ. EF generates SQL. Migrations, change tracking, lazy loading. Use for: CRUD, domain models, developer productivity, when query performance isn't critical.
- **My rule** — If I need to think about the SQL, use Dapper. If I need to think about the domain model, use EF.

### Common Patterns
- **Parameterized queries** — `connection.Query<User>("SELECT * FROM Users WHERE Id = @Id", new { Id = 123 })`. Always parameterize — never concatenate strings.
- **Multi-mapping** — `Query<Order, Customer, Order>(sql, (order, customer) => { order.Customer = customer; return order; })`. Map joins to nested objects.
- **Bulk operations** — Combine with SqlBulkCopy for high-throughput inserts. Dapper for reads, SqlBulkCopy for writes.

## Sorulursa

> [!faq]- "When would you choose Dapper over EF in a new project?"
> If the project is read-heavy with complex queries (reporting, analytics, dashboards), Dapper. If it's a standard CRUD app where developer speed matters more than query speed, EF. In practice, I often use both in the same project — EF for the application layer, Dapper for the reporting/analytics layer. They work fine side by side on the same database.

> [!faq]- "Isn't raw SQL in code a maintenance problem?"
> It can be. I keep Dapper queries in dedicated repository classes, not scattered through the codebase. Each query has a comment explaining what it does. For complex queries, I write the SQL in a SQL editor first, test it, then paste it into the code. It's more work than LINQ but the performance is worth it for hot paths.

> [!faq]- "How do you handle SQL injection with Dapper?"
> Always use parameterized queries. Dapper's `@Parameter` syntax handles this automatically: `connection.Query<User>("SELECT * FROM Users WHERE Id = @Id", new { Id = 123 })`. Never concatenate strings into SQL — Dapper makes it easy to do the right thing. I've seen codebases where people used string interpolation with Dapper, which defeats the purpose.

---

*[[00-dashboard]]*
