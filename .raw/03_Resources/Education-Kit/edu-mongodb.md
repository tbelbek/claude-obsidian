---
tags:
  - education-kit
---
# MongoDB — Knowledge Base
> [!info] Document database storing flexible JSON-like documents (BSON) instead of fixed-schema tables — covering document model, transactions, performance, and comparisons with SQL and PostgreSQL.

---

## Key Concepts

### What MongoDB Is
MongoDB is a document database that stores data as flexible JSON-like documents (BSON) instead of fixed-schema tables. Each document can have different fields, nested objects, and arrays — no migrations needed when the schema evolves. Best for: domain data with varied structures (each entity type has different fields), rapid iteration where schemas change frequently, and scenarios where document-level atomicity is sufficient.

### Document Model
- **Documents** — JSON-like objects stored in collections. Schema-flexible — each document can have different fields.
- **Collections** — Groups of documents. Analogous to tables in SQL, but no fixed schema.
- **Embedded documents** — Nest related data inside a document instead of joining tables. Good for data that's always read together.

### When to Use MongoDB vs SQL
- **MongoDB** — Flexible schema, document-oriented, good for event-driven data and aggregates that change shape. Works well when each entity type has different telemetry fields or varying structure.
- **SQL** — Fixed schema, ACID by default, good for structured data with complex joins. Use PostgreSQL for relational data (user accounts, permissions, audit logs).

### Transactions
- **Multi-document transactions** — Available since MongoDB 4.0. Use for operations that update multiple collections atomically — like assigning a job to an entity (update both collections in one transaction).
- **Transaction action filters** — Automatic rollback via ASP.NET action filters. If a request handler throws an exception, the transaction is rolled back.

### Performance
- **Indexes** — Critical for query performance. Index on frequently queried fields (entity ID, status, timestamp). Without indexes, queries on large collections are full scans.
- **Aggregation pipeline** — For complex queries and reporting. Used for metrics — average processing time, utilization rates.

### MongoDB vs PostgreSQL
- Both serve different purposes. MongoDB for domain-specific data (flexible schema, document-oriented). PostgreSQL for relational data (fixed schema, ACID by default).
- The choice is pragmatic: when entity fields vary by type (different entities report different data), a fixed SQL schema would require constant migrations. MongoDB's flexible schema handles this naturally.

### Best Practices
- **Database per service** — Each microservice owns its own database. No cross-service database access.
- **Repository pattern** — Generic repositories per service with custom extensions.
- **Health checks** — MongoDB connectivity checks integrated into Kubernetes readiness probes. If MongoDB is unreachable, the pod stops receiving traffic.
- **Conventions** — CamelCase elements, enum-as-string, immutable type support via standardized conventions.
- **Migration tooling** — Schema migrations and data seeding run during service startup.

---

## Sorulursa

> [!faq]- "When would you choose MongoDB over PostgreSQL?"
> When your data shape varies between records. If each entity type has different fields, a fixed SQL schema would need a new column for every new field, or a generic key-value store which defeats the purpose. MongoDB lets each document have its own shape while still being queryable. For data with a fixed, known schema and complex relationships, PostgreSQL is better.

> [!faq]- "How do you handle schema changes in MongoDB?"
> MongoDB doesn't enforce schemas, but your application code does. When you add a new field to a document, old documents without that field still load fine — the new field is just null. For breaking changes (renaming a field, changing a type), write migration scripts that run during service startup — update all documents in the collection before accepting traffic.

> [!faq]- "How do you ensure data consistency without foreign keys?"
> Eventual consistency via domain events. When a job is assigned to an entity, the assigning service publishes an event. The other service consumes it and updates its state. Within a single service, use MongoDB transactions for multi-document operations. Between services, accept a brief window of inconsistency — for most operational use cases, seconds of delay are acceptable.
