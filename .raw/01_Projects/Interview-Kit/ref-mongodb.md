---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# MongoDB — Quick Reference

> [!info] How I've used it: At Toyota and Combination, MongoDB stored fleet state for autonomous forklifts (T-ONE). Custom Tmhls.MongoDb.Extensions NuGet package with repository pattern, ACID transactions, health checks. Collections for vehicles, transports, missions, workflows.

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Document Model\|documents]] | flexible schema, BSON, nested objects | [[#Transactions\|transactions]] | ACID with replica set, multi-document consistency |
| [[#When to Use MongoDB vs SQL\|vs SQL]] | MongoDB=flexible+scale, SQL=relational+joins | [[#Performance\|indexes]] | compound indexes, explain plans, TTL indexes |
| [[#At Toyota — Practical Setup\|custom NuGet]] | Tmhls.MongoDb.Extensions, repository pattern, health checks | [[#MongoDB vs PostgreSQL at Toyota\|vs PostgreSQL]] | flexible schema won, no migration overhead |
| [[#HOW WE USED IT\|at Combination]] | per-service DB, shared framework conventions | | |

## HOW WE USED IT

At Toyota, MongoDB was the persistence layer for T-ONE — the autonomous forklift system. Each domain service had its own database context: VehiclesDbContext for vehicle state, TransportsContext for transport jobs, LayoutDbContext for warehouse layouts, WorkflowContext for workflow definitions. We built a custom Tmhls.MongoDb.Extensions NuGet package that provided:
- **Repository pattern** — generic repositories per service
- **ACID transactions** — MongoDbTransaction for multi-document consistency
- **Conventions** — CamelCase elements, enum-as-string, immutable type support
- **Health checks** — MongoDB connectivity checks integrated into K8s readiness probes
- **Input validation** — BsonIdValidation attribute for document ID validation

**At Combination:**
- MongoDB is used across the platform for services that need flexible document storage — feed data, social posts, entity profiles, casino data
- The shared `GP-Infra-ServiceBase-Framework` provides MongoDB integration via `MongoClientSettingsExtensions` with standardized conventions
- Each service owns its own database — no cross-service database access, same pattern as Toyota
- Health checks for MongoDB connectivity integrated into Kubernetes readiness probes — if the database is unreachable, the pod stops receiving traffic

---

## Key Concepts

### What MongoDB Is
MongoDB is a document database that stores data as flexible JSON-like documents (BSON) instead of fixed-schema tables. Each document can have different fields, nested objects, and arrays — no migrations needed when the schema evolves. Best for: domain data with varied structures (each vehicle type has different telemetry), rapid iteration where schemas change frequently, and scenarios where document-level atomicity is sufficient.

### Document Model
- **Documents** — JSON-like objects stored in collections. Schema-flexible — each document can have different fields.
- **Collections** — Groups of documents. Analogous to tables in SQL, but no fixed schema.
- **Embedded documents** — Nest related data inside a document instead of joining tables. Good for data that's always read together.

### When to Use MongoDB vs SQL
- **MongoDB** — Flexible schema, document-oriented, good for event-driven data and aggregates that change shape. We used it for vehicle state because each vehicle type had different telemetry fields.
- **SQL** — Fixed schema, ACID by default, good for structured data with complex joins. We used PostgreSQL alongside MongoDB at Toyota for relational data.

### Transactions
- **Multi-document transactions** — Available since MongoDB 4.0. We used them for operations that updated multiple collections atomically — like assigning a transport job to a vehicle (update both Transport and Vehicle documents).
- **Transaction action filters** — Our custom package had automatic rollback via ASP.NET action filters. If a request handler threw an exception, the transaction was rolled back.

### Performance
- **Indexes** — Critical for query performance. We indexed on vehicle ID, transport status, and timestamp fields. Without indexes, queries on large collections are full scans.
- **Aggregation pipeline** — For complex queries and reporting. We used it for fleet metrics — average transport time, vehicle utilization rates.

### At Toyota — Practical Setup
- **Custom NuGet package** — Tmhls.MongoDb.Extensions with repository pattern, ACID transactions, health checks, and conventions (CamelCase, enum-as-string, immutable types).
- **Database contexts** — Each service owns its database: VehiclesDbContext, TransportsContext, LayoutDbContext, WorkflowContext. No cross-service database access.
- **Health checks** — MongoDB connectivity checks integrated into Kubernetes readiness probes. If MongoDB is down, the pod stops receiving traffic.
- **Migration tooling** — Tmhls.MongoDb.Tools for schema migrations and data seeding. Ran during service startup.

### MongoDB vs PostgreSQL at Toyota
- Both used at Toyota. MongoDB for domain-specific data (vehicle state, transport jobs — flexible schema, document-oriented). PostgreSQL for relational data (user accounts, permissions, audit logs — fixed schema, ACID by default).
- The choice was pragmatic: vehicle telemetry fields vary by vehicle type (different AGVs report different data), so a fixed SQL schema would require constant migrations. MongoDB's flexible schema handled this naturally.

## Sorulursa

> [!faq]- "When would you choose MongoDB over PostgreSQL?"
> When your data shape varies between records. At Toyota, each vehicle type had different telemetry fields — SEW Palletrunner reports different data than a Kollmorgen forklift. A fixed SQL schema would need a new column for every new field, or a generic key-value store which defeats the purpose. MongoDB lets each document have its own shape while still being queryable. For data with a fixed, known schema and complex relationships, PostgreSQL is better.

> [!faq]- "How do you handle schema changes in MongoDB?"
> MongoDB doesn't enforce schemas, but your application code does. When we added a new field to the Vehicle document, old documents without that field still loaded fine — the new field was just null. For breaking changes (renaming a field, changing a type), we wrote migration scripts in Tmhls.MongoDb.Tools that ran during service startup — update all documents in the collection before accepting traffic.

> [!faq]- "How do you ensure data consistency without foreign keys?"
> Eventual consistency via domain events. When a transport is assigned to a vehicle, the Transport service publishes TransportAssigned. The Vehicle service consumes it and updates its state. Within a single service, we use MongoDB transactions for multi-document operations. Between services, we accept a brief window of inconsistency — for warehouse operations, seconds of delay are acceptable.

---

*[[00-dashboard]]*
