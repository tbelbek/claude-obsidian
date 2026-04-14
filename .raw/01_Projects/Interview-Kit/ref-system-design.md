---
tags:
  - interview-kit
  - interview-kit/reference
up: "[[00-dashboard]]"
cssclasses:
  - cards
  - wide-page
---

*[[00-dashboard]]*

# System Design — Complete Interview Guide

> [!tip] Full system design interview guide: DRIVE decision trees (17 aspects), domain defaults (12 domains), validation checklists, debug flowchart, tool glossary, and scenario templates.

> [!abstract] 1-hour session structure
> **5 min** Clarify: users, RPS, latency, availability, constraints
> **10 min** High-level: client → LB → API → services → data, sync vs async
> **20 min** Deep dive: data model, API, scaling bottleneck, trade-offs
> **10 min** Edge cases: failures, duplicates, spikes, consistency
> **5 min** Ops: monitoring, deployment, alerting, rollback
> **10 min** Discussion: alternatives rejected and why

---


## DRIVE: Define & Reduce — Decision Trees by Aspect

> [!danger|no-icon] **Define** the problem by asking one root question per aspect. **Reduce** by branching based on the answer to reach the right pattern/tool. If no answer, follow the default path.

### Aspect Dashboard — Ask in This Order

|                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| | | |
|---|---|---|
| <div style="background:rgba(239,68,68,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 1 System Shape\|1. SYSTEM SHAPE]]**</span> <br> [[#User Flow\|What does the user do step by step?]] <br> [[#New or Existing\|Is this new or extending something existing?]] <br> [[#User Types\|Who uses it? End users, admins, partners?]] <br> [[#Multi-Tenancy\|Do different customers share the system?]] <br> *Draws: diagram skeleton, proxy layer, client boxes*</div> | <div style="background:rgba(239,68,68,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 3 Data Storage\|2. DATA STORAGE]]**</span> <br> [[#Entities\|What are the main entities and relations?]] <br> [[#Data Shape\|Fixed structure or varies per record?]] <br> [[#Read Write Ratio\|Is it read-heavy or write-heavy?]] <br> [[#Search Needs\|Do we need full-text search?]] <br> [[#Data Retention\|How long do we keep the data?]] <br> *Draws: database, cache, search engine, archival*</div> | <div style="background:rgba(239,68,68,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 4 Communication\|3. COMMUNICATION]]**</span> <br> [[#Sync or Async\|Does the user need results immediately?]] <br> [[#Event Reactions\|Do other parts react when something happens?]] <br> [[#Live Updates\|Does the UI need live updates?]] <br> [[#External Systems\|Does it talk to external systems?]] <br> [[#Cross-Service Failure\|What if one service fails halfway?]] <br> *Draws: queues, event bus, WebSocket, webhooks*</div> |
| <div style="background:rgba(249,115,22,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 6 API Design\|4. API DESIGN]]**</span> <br> [[#Service Count\|How many backend services will there be?]] <br> [[#Client API Style\|Do different clients need different data shapes?]] <br> [[#Internal Communication\|Do services need to call each other?]] <br> *Draws: gateway, REST/GraphQL label, gRPC arrows*</div> | <div style="background:rgba(249,115,22,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 2 Scale & Traffic\|5. SCALE & TRAFFIC]]**</span> <br> [[#Daily Active Users\|How many daily active users?]] <br> [[#Traffic Pattern\|Is traffic steady or spiky?]] <br> *Draws: load balancer, auto-scaling, CDN, sharding*</div> | <div style="background:rgba(249,115,22,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 7 Security\|6. SECURITY]]**</span> <br> [[#Authentication Method\|How do users log in?]] <br> [[#Permission Levels\|Are there different permission levels?]] <br> [[#Tenant Isolation\|Is this multi-tenant? How isolated?]] <br> *Draws: identity provider, JWT flow, RBAC, tenant filter*</div> |
| <div style="background:rgba(59,130,246,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 5 Consistency & Failure\|7. CONSISTENCY & FAILURE]]**</span> <br> [[#Cross-Service Operations\|Can one operation span multiple services?]] <br> [[#Duplicate Handling\|Can the same request arrive twice?]] <br> [[#Database Failure\|What if the database is down?]] <br> [[#Downstream Failure\|What if a downstream service is slow or down?]] <br> *Draws: saga, outbox, idempotency, circuit breaker, DLQ*</div> | <div style="background:rgba(59,130,246,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 10 Frontend\|8. FRONTEND]]**</span> <br> [[#Frontend Type\|What kind of frontend? Web, mobile, API-only?]] <br> [[#Frontend Connection\|How does the frontend connect to the backend?]] <br> *Draws: browser/mobile box, CDN, API connection*</div> | <div style="background:rgba(59,130,246,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 15 Performance\|9. PERFORMANCE]]**</span> <br> [[#Performance Requirements\|What are the latency and throughput targets?]] <br> [[#Performance Testing\|How do we verify it handles the load?]] <br> *Draws: cache layers, SLO targets, load test*</div> |
| <div style="background:rgba(34,197,94,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 11 Testing Strategy\|10. TESTING]]**</span> <br> [[#Test Approach\|How do we test this system?]] <br> [[#Test Environments\|How many environments do we need?]] <br> *Draws: test pyramid, CI pipeline stages*</div> | <div style="background:rgba(34,197,94,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 14 Compliance & Audit\|11. COMPLIANCE & AUDIT]]**</span> <br> [[#Compliance Requirements\|GDPR? PCI? SOC2? Any regulations?]] <br> [[#Audit Log Design\|How do we track who did what?]] <br> *Draws: audit log, consent service, deletion pipeline*</div> | <div style="background:rgba(34,197,94,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 8 Operations & Deployment\|12. OPERATIONS]]**</span> <br> [[#Team Structure\|How many teams will work on this?]] <br> [[#Deploy Tolerance\|Can we tolerate downtime during deploys?]] <br> [[#Production Monitoring\|How will we know if something breaks?]] <br> [[#Project Timeline\|Is this an MVP or production-ready?]] <br> *Draws: CI/CD pipeline, observability stack*</div> |
| <div style="background:rgba(168,85,247,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 9 Infrastructure\|13. INFRASTRUCTURE]]**</span> <br> [[#Cloud Provider\|What cloud provider?]] <br> [[#Infrastructure Management\|How do we manage infrastructure?]] <br> [[#Production Pipeline\|How does code get to production?]] <br> *Draws: cloud services, Terraform, deploy pipeline*</div> | <div style="background:rgba(168,85,247,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 13 Internationalization\|14. INTERNATIONALIZATION]]**</span> <br> [[#i18n Scope\|Multiple languages, timezones, or currencies?]] <br> *Draws: translation service, UTC storage*</div> | <div style="background:rgba(168,85,247,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 12 Data Migration\|15. DATA MIGRATION]]**</span> <br> [[#Migration Strategy\|Does this need to migrate data from an old system?]] <br> *Draws: ETL pipeline, CDC sync*</div> |
| <div style="background:rgba(168,85,247,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 16 Disaster Recovery\|16. DISASTER RECOVERY]]**</span> <br> [[#Recovery Strategy\|What happens if a region goes down?]] <br> *Draws: backups, multi-AZ, failover*</div> | <div style="background:rgba(168,85,247,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Aspect 17 Cost Estimation\|17. COST ESTIMATION]]**</span> <br> [[#Cost Awareness\|How do we estimate and manage infra costs?]] <br> *Reference: rough monthly costs per component*</div> | <div style="background:rgba(107,114,128,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#After All Aspects — Validate Your Design\|VALIDATE YOUR DESIGN]]**</span> <br> Single point of failure? <br> Bottleneck? Data loss? <br> Security? Debugging? <br> Consistency? Scalability? Cost?</div> |

Red (1-3) = ask first, defines the skeleton. Orange (4-6) = shapes the architecture. Blue (7-9) = design details. Green (10-12) = quality and operations. Purple (13-17) = situational, ask if relevant.

[[#When the Interviewer Says "You Decide" — Domain Defaults|DOMAIN DEFAULTS]] — use when the interviewer says "you decide" or "what would you suggest?"

[[#Debug Flowchart — Top-Down Approach|DEBUG FLOWCHART]] — top-down incident debugging: error → latency → data → outage flows

---

### Aspect 1: System Shape

#### User Flow

```
"What does a user do, step by step?"
 │
 ├── they gave a clear flow ──→ each noun = a service, each verb = an API call
 │                                draw the flow as boxes and arrows
 │
 └── vague / unclear ──→ ask: "what's the input and what's the output?"
                          draw: [Input] → [???] → [Output]
                          fill the middle as you learn more

```

#### New or Existing

```
"Is this new or does it extend something existing?"
 │
 ├── new (greenfield)
 │    └── draw: [Client] → [API] → [Service] → [Database]
 │         clean start, no constraints from legacy
 │
 ├── extending existing system
 │    └── draw: [Client] → [Reverse Proxy] ─┬─→ [Existing System]
 │                                           └─→ [New Service]
 │         use Strangler Fig pattern: migrate one path at a time
 │         keep both running in parallel, route by URL path
 │
 └── no answer / default ──→ assume greenfield, note the assumption
     if interviewer says "you decide" ──→ say "I'll assume greenfield so we
     can focus on the design, but in practice I'd use Strangler Fig if there's
     an existing system to protect"
```

**Reverse Proxy**: a server that sits between clients and your backend servers. Clients talk to the proxy, not directly to your services. The proxy forwards requests, handles TLS termination (decrypts HTTPS so internal traffic can be plain HTTP), caching, compression, and routing. Examples: Nginx, HAProxy, Envoy, Traefik. In Kubernetes, the Ingress Controller acts as the reverse proxy.

**Strangler Fig pattern**: a migration strategy where you build new functionality as separate services alongside the old system. A reverse proxy routes requests — old URLs go to the legacy system, migrated URLs go to the new service. Over time, the old system shrinks and the new one grows. Named after a fig vine that grows around a tree and eventually replaces it. Every step is reversible — if the new service has a problem, route traffic back to the old one.

#### User Types

```
"Who uses this system? End users, admins, other services, external partners?"
 │
 ├── one type (end users only)
 │    └── draw: [Client] → [API] — single API surface
 │         why: one user type = one API, one auth flow, simplest setup
 │
 ├── end users + admins
 │    └── draw: [Client] → [API] + [Admin] → [Admin API]
 │         why: admins need elevated permissions (delete users, change config)
 │         separating surfaces means admin endpoints aren't accidentally exposed
 │         to end users, and you can add stricter auth (MFA) on admin only
 │
 ├── end users + external API consumers (machines, partners)
 │    └── draw: [Client] → [GraphQL or REST] + [Partner] → [REST + API key]
 │         why: humans and machines have different auth (JWT vs API key),
 │         different rate limits, different SLAs, and different error formats.
 │         Separate surfaces let you version and rate-limit independently
 │
 ├── internal services only (no public-facing users)
 │    └── draw: [Service A] → [gRPC] → [Service B]
 │         why: no browser clients = no need for REST/GraphQL.
 │         gRPC is faster (binary), type-safe (proto contracts), and
 │         generates client code automatically
 │
 └── no answer / "you decide" ──→ assume end users + admins (most common)
```

#### Multi-Tenancy

```
"Is this multi-tenant? Do different customers share the same system?"
 │
 ├── no, single tenant
 │    └── no change — standard architecture, skip tenant concerns
 │
 ├── yes, many small tenants (100+)
 │    └── shared database with tenant_id column on every table
 │         draw: [API Gateway: extract tenant_id from JWT] → [Service: filter every query by tenant_id]
 │         cheapest, simplest. Enforce tenant filter at the data access layer so developers can't skip it
 │
 ├── yes, few large tenants with strict isolation
 │    └── database per tenant
 │         draw: [API Gateway: route by tenant] → [Service] → [Tenant DB pool: tenant_123_db, tenant_456_db]
 │         more isolation, independent scaling per tenant, but higher operational cost
 │
 ├── yes, with data residency requirements (GDPR — EU data must stay in EU)
 │    └── regional deployment
 │         draw: [GeoDNS] → [EU Region (EU tenant data)] / [US Region (US tenant data)]
 │         each region has its own database and services
 │
 └── no answer / "you decide" ──→ shared DB + tenant_id (start here, evolve if needed)
     say: "I'll start with shared database and a tenant_id column on every table.
     It's the simplest approach. We can evolve to database-per-tenant later if compliance
     or tenant size demands it"
```

**Multi-tenant isolation**: the technique of serving multiple customers (tenants) from the same application instance while keeping their data completely separate. The most critical security concern: one missing `WHERE tenant_id = @tenant` clause in any query means Customer A can see Customer B's data. Enforce at the data access layer (base repository class or query interceptor), not in controllers. Write automated tests that attempt cross-tenant access and verify zero results returned.

---

### Aspect 2: Scale & Traffic

#### Daily Active Users

```
"How many daily active users?"
 │
 ├── hundreds ──→ single instance is fine
 │                draw: [Client] → [API] → [Database]
 │                why: at this scale, one server handles everything.
 │                adding cache, scaling, or CDN would be over-engineering
 │
 ├── thousands ──→ add a load balancer, 2-3 instances
 │                  draw: [Client] → [Load Balancer] → [API x2] → [Database]
 │                  why: one instance can't handle the load reliably.
 │                  the load balancer distributes traffic and provides failover
 │                  if one instance crashes, the other keeps serving
 │
 ├── hundreds of thousands ──→ add cache + auto-scaling
 │    │  draw: [Client] → [CDN] → [LB] → [API x N (auto-scale)] → [Redis Cache] → [Database]
 │    │  why: at this scale, the database becomes the bottleneck.
 │    │  Redis cache absorbs 90% of reads (sub-ms response).
 │    │  CDN serves static assets without touching your servers.
 │    │  auto-scaling adds/removes instances based on demand
 │    │
 │    └── "Is traffic steady or spiky?"
 │         ├── steady ──→ Horizontal Pod Autoscaler on CPU (target 75%)
 │         │    why: CPU-based scaling is simple and predictable for steady load
 │         ├── spiky (predictable, e.g. morning rush) ──→ HPA + scheduled scaling
 │         │    why: pre-scale before the spike hits, HPA handles the variation
 │         └── spiky (unpredictable, e.g. viral event) ──→ add Message Queue to buffer
 │              draw: [API] → [Queue] → [Workers]
 │              why: the queue absorbs the burst instantly (API returns 202).
 │              workers process at a steady rate the database can handle.
 │              use KEDA to auto-scale workers based on queue depth —
 │              1000 messages waiting = 10 workers, 0 messages = 0 workers
 │
 ├── millions ──→ all of the above + database sharding + multi-region
 │                draw: [CDN] → [GeoDNS] → [Region A / Region B]
 │                why: one database can't handle millions of users.
 │                sharding splits data across multiple databases (by tenant/user ID).
 │                multi-region puts servers close to users (EU users → EU servers)
 │
 └── no answer / "you decide" ──→ check the domain defaults table above
     say: "For a [SaaS/e-commerce/etc.] system, I'd assume [N] users
     and design for 10x that with a scaling plan for 100x"
```

#### Traffic Pattern

The traffic pattern sub-question appears inside the "hundreds of thousands" branch above. If the interviewer gives a clear user count, also ask: "Is the traffic steady throughout the day, or does it spike at certain times (morning rush, campaigns, seasonal events)?" Steady → basic auto-scaling. Spiky → add a message queue to buffer bursts + event-driven auto-scaling (KEDA) on queue depth.

**Load Balancer**: a component that distributes incoming requests across multiple server instances. If one server dies, the load balancer routes to the healthy ones. Examples: Nginx, HAProxy, AWS ALB (Application Load Balancer). In Kubernetes, the Ingress controller acts as the load balancer.

**CDN (Content Delivery Network)**: a global network of edge servers that cache static files (images, CSS, JavaScript) close to users. A user in Europe gets the file from a European server instead of the origin server in the US. Examples: CloudFront (AWS), CloudFlare, Akamai. Reduces latency and offloads your servers.

**HPA (Horizontal Pod Autoscaler)**: a Kubernetes feature that automatically adds or removes pod instances based on CPU or memory usage. You set a target (e.g., 75% CPU) — when average CPU across pods exceeds the target, HPA adds a pod. When it drops, HPA removes one. Requires your services to be stateless (no in-memory session data).

**KEDA (Kubernetes Event-Driven Autoscaling)**: an extension to Kubernetes that scales pods based on external metrics like message queue depth. Example: if 500 messages are waiting in a Kafka topic, KEDA spins up 5 worker pods. When the queue is empty, KEDA scales to zero. More reactive than HPA for queue-processing workloads because it scales on the actual work backlog, not CPU usage.

**GeoDNS**: a DNS configuration that returns different server IP addresses based on the user's geographic location, routing them to the nearest data center. Example: European users resolve to the EU region, US users to the US region. Implemented via AWS Route 53 or CloudFlare DNS.

**Nginx**: an open-source web server and reverse proxy. Used as a load balancer (distributes requests across multiple backend instances), reverse proxy (TLS termination, caching, compression), and static file server. Configuration-file based — you define routing rules in `nginx.conf`. The most widely deployed reverse proxy/load balancer on the internet.

**HAProxy**: an open-source load balancer focused on high performance and reliability. Handles millions of connections. Supports TCP (Layer 4) and HTTP (Layer 7) load balancing. Used when you need maximum throughput and advanced health checking. Configuration-file based like Nginx, but more focused on load balancing than serving static files.

**ALB (Application Load Balancer)**: AWS's managed Layer 7 load balancer. Routes HTTP/HTTPS requests based on URL path, host header, or query parameters. Supports WebSocket, gRPC, and HTTP/2. Integrated with AWS services (ECS, EKS, Lambda). You don't manage any servers — AWS handles availability and scaling. Use for any web application or API running on AWS.

**CloudFront**: AWS's CDN (Content Delivery Network). Caches and serves content from 400+ edge locations worldwide. Integrates with S3 (serve files), ALB (cache API responses), and Lambda@Edge (run code at the edge). You create a "distribution" pointing at your origin (S3 bucket or load balancer), and CloudFront handles global caching and delivery.

**CloudFlare**: a CDN and security platform. Provides CDN caching, DDoS protection, WAF (Web Application Firewall), DNS hosting, and edge compute (CloudFlare Workers). You point your domain's DNS to CloudFlare, and all traffic flows through their network — they cache static content, block attacks, and forward legitimate requests to your origin server. Free tier available.

**Database sharding**: splitting a database into multiple smaller databases (shards), each holding a subset of the data. You choose a shard key (e.g., tenant_id or user_id) that determines which shard holds each record. Distributes write load across multiple machines. The application or a proxy routes queries to the correct shard.

---

### Aspect 3: Data Storage

#### Entities

```
"What are the main things this system stores? How do they relate to each other?"
 │
 └── list them on the board as boxes with arrows
     entities that change together = same service later
     entities that change independently = candidate for separate services

How to discover entities — ask these:
 │
 ├── "What does the user create or interact with?"
 │    → those are your core entities (Ticket, Order, Document, Message)
 │
 ├── "Who are the actors?" 
 │    → User, Admin, Agent, Customer, Partner — these are entity types too
 │
 ├── "What gets assigned, tracked, or has a status?"
 │    → that entity has a state machine (Ticket: open→assigned→resolved)
 │
 ├── "What belongs to what?"
 │    → those are relationships (Order has LineItems, User has Addresses)
 │
 ├── "What is shared vs what is owned?"
 │    → shared = reference data (Product catalog, Categories)
 │      owned = transactional data (Order, Payment, Session)
 │
 └── "What would break if we deleted this?"
      → that tells you the dependency direction

Draw them with cardinality:
  [User] 1──* [Order] *──* [Product]     (many-to-many via OrderLine)
  [Ticket] *──1 [Agent]                   (many tickets per agent)
  [Tenant] 1──* [User] 1──* [Session]     (hierarchy)
```

**Domain examples — common entity patterns:**

```
Help Desk / Ticket System:
  [Tenant] 1──* [User] 1──* [Ticket] 1──* [Comment]
  [Ticket] *──1 [Agent]  (assignment)
  [Ticket] *──1 [Queue/Team]  (routing)
  [Ticket] 1──* [Attachment]  (files stored in object storage)
  [Tenant] 1──* [SLA Policy]  (response time rules per tenant)
  state machine: open → assigned → in_progress → waiting → resolved → closed

E-Commerce / Marketplace:
  [User] 1──* [Order] 1──* [OrderLine] *──1 [Product]
  [Product] 1──* [Variant] (size, color)
  [Product] *──* [Category] (many-to-many)
  [Order] 1──1 [Payment]
  [Order] 1──1 [Shipment] 1──* [TrackingEvent]
  [User] 1──1 [Cart] 1──* [CartItem]  (temporary, lives in Redis)
  state machine: cart → placed → paid → shipped → delivered → returned

CRM / Sales Pipeline:
  [Company] 1──* [Contact] 
  [Contact] *──* [Deal]  (many contacts per deal)
  [Deal] *──1 [Pipeline Stage]  (kanban column)
  [Deal] 1──* [Activity] (calls, emails, meetings — append-only log)
  [User] 1──* [Task] *──1 [Deal]
  state machine: lead → qualified → proposal → negotiation → won/lost

Notification / Messaging:
  [User] 1──* [NotificationPreference] (per channel: email, push, SMS)
  [Template] 1──* [Notification]  (rendered from template)
  [Notification] has: channel, status, recipient, payload, sent_at
  state machine: pending → sent → delivered → read → bounced/failed

Chat / Conversation:
  [Conversation] *──* [Participant]  (group chats)
  [Conversation] 1──* [Message]
  [Message] has: sender, content, timestamp, read_receipts
  [User] 1──1 [PresenceStatus]  (online/offline/typing — stored in Redis)

Real-Time Dashboard / IoT:
  [Device] 1──* [Reading] (append-only, time-series)
  [Device] *──1 [DeviceGroup]
  [Device] 1──1 [LatestState]  (stored in Redis for fast dashboard reads)
  [Alert Rule] evaluates [Reading] → produces [Alert]
```

**How entities become services**: group entities that change together into one service. If Ticket, Comment, and Attachment always change when a ticket is updated, they belong in the Ticket Service. If User and Notification change independently (user updates their profile ≠ notification being sent), they belong in separate services. The boundary test: "can this team deploy this service without coordinating with another team?"

#### Data Shape

```
"Does the data have a fixed structure or vary per record?"
 │
 ├── fixed structure, clear relations between entities
 │    └── PostgreSQL (open-source, rich features, JSON support)
 │        or MS SQL Server (if .NET ecosystem)
 │        why: you need joins, foreign keys, transactions
 │
 ├── varies per record, nested/self-contained documents
 │    └── MongoDB (flexible schema, good drivers, horizontal scaling)
 │        why: no migrations needed when adding fields, natural document shape
 │
 ├── simple key-value lookups or counters
 │    └── Redis (sub-millisecond reads, rich data structures)
 │        why: purpose-built for fast lookups, also handles sessions and caching
 │
 ├── time-series (IoT, metrics, logs, sensor data)
 │    └── TimescaleDB (PostgreSQL extension, compression, downsampling)
 │        why: time-bucketed storage, automatic rollups, familiar SQL interface
 │
 ├── relationships are the core of the model (social graph, recommendations)
 │    └── Neo4j (relationship-first queries, traversals)
 │        why: "friends of friends who bought X" is one query, not 5 recursive joins
 │
 └── no answer / "you decide" ──→ PostgreSQL (safest general-purpose choice)
     say: "Without knowing more, I'll start with PostgreSQL because it handles
     relational data, has JSON support for flexible fields, and scales with
     read replicas. We can add a document store later if the data shape demands it"

```

#### Read Write Ratio

```
"Is this read-heavy, write-heavy, or balanced?"
 │
 ├── read-heavy (>10x more reads than writes)
 │    │
 │    ├── moderate (10:1) ──→ add Redis cache (cache-aside pattern)
 │    │                        draw: [API] → [Redis] → miss → [Database]
 │    │                        why: Redis serves reads in <1ms, reduces DB load by 90%
 │    │
 │    └── extreme (100:1+) ──→ Redis + Database Read Replicas + CDN for static
 │                              draw: [CDN] → [API] → [Redis] → [Read Replica]
 │                                                                [Primary DB for writes only]
 │                              why: even Redis can't absorb all reads alone at this ratio.
 │                              read replicas distribute DB reads across multiple instances.
 │                              CDN serves static content without touching your servers at all.
 │                              the primary DB only handles writes — no read contention
 │
 ├── write-heavy (more writes than reads)
 │    └── add a message queue as write buffer
 │         draw: [API] → [Kafka or SQS] → [Worker] → [Database]
 │         why: queue absorbs bursts, workers write at DB's pace
 │         if single DB still can't keep up → shard by tenant/user ID
 │
 ├── both heavy ──→ CQRS pattern (Command Query Responsibility Segregation)
 │                   draw: [Write API] → [Primary DB]
 │                         [Primary DB] → [Event] → [Read Store (Redis or denormalized DB)]
 │                         [Read API] → [Read Store]
 │                   why: optimize write model and read model independently
 │
 └── balanced / low volume / no answer ──→ API → Database directly, don't add complexity
      why: adding a cache or queue when you don't need one adds operational cost
      (monitoring, invalidation, failure modes) without benefit.
      start simple — you can always add Redis/Kafka later when the bottleneck appears

```

#### Search Needs

```
"Do we need search beyond simple filters?"
 │
 ├── no ──→ SQL WHERE clauses + proper indexes, no extra component
 │         why: for simple filters (status = 'open' AND priority = 'high'),
 │         a composite index on (status, priority) is fast enough.
 │         no need for a separate search engine
 │
 ├── full-text search with relevance ranking
 │    └── add Elasticsearch (or OpenSearch)
 │         draw: [Database] → [Events/CDC] → [Elasticsearch]
 │               [Client] → [Search API] → [Elasticsearch]
 │         why: SQL LIKE '%keyword%' can't rank results by relevance,
 │         doesn't support fuzzy matching ("recieve" → "receive"),
 │         and can't do faceted filters (filter by category + price + rating
 │         simultaneously). Elasticsearch does all of this natively because
 │         it builds an inverted index — for every word, it knows which
 │         documents contain it
 │         sync: keep Elasticsearch in sync with the primary database via
 │         Change Data Capture (Debezium watches the DB log) or application
 │         events (publish an event after each write, a consumer updates ES)
 │
 ├── just autocomplete
 │    └── Redis with prefix matching (sorted sets or edge-ngram)
 │         why: lighter than running a full Elasticsearch cluster.
 │         store searchable terms in a Redis sorted set and query
 │         by prefix. Good enough for "type 3 letters, see suggestions"
 │
 └── no answer / "you decide" ──→ skip search for now, add when users ask for it
      why: Elasticsearch adds operational complexity (cluster management,
      index mapping, sync logic). Only add it when simple SQL filters
      aren't meeting the user's search needs

```

#### Data Retention

```
"How long do we keep the data?"
 │
 ├── days/weeks ──→ TTL on records, background cleanup job
 │    why: set a TTL (time-to-live) on each record. A nightly cleanup job
 │    deletes expired records. Prevents the database from growing indefinitely
 │
 ├── months/years ──→ standard DB storage, partition by date for performance
 │    why: partitioning by date (e.g., one partition per month) keeps queries
 │    fast — a query for "last 30 days" only scans one partition, not the
 │    entire table. Old partitions can be dropped instantly when no longer needed
 │
 ├── 7+ years (compliance) ──→ add cold storage
 │    draw: [Database] → [Archival Job (nightly)] → [S3 Glacier]
 │    why: keeping 7 years of data in PostgreSQL is expensive and slows backups.
 │    S3 Glacier costs $0.004/GB/month (vs $0.023 for standard S3).
 │    data is rarely accessed — retrieval takes minutes to hours, which is
 │    acceptable for compliance queries that happen once a year during audits
 │
 ├── forever + need full history ──→ consider Event Sourcing
 │    why: if you need "what was the state at 3pm last Tuesday?" or a complete
 │    audit trail of every change, event sourcing stores every event as an
 │    append-only log. Current state is derived by replaying events.
 │    trade-off: adds significant complexity (snapshotting, schema evolution)
 │    — only use when the audit/time-travel capability is a core requirement
 │
 └── no answer / "you decide" ──→ assume months, add TTL/cleanup
      why: safe default. Note archival as a future concern if compliance surfaces
```

**PostgreSQL**: an open-source relational database. Stores data in tables with typed columns. Supports complex joins, foreign key constraints, ACID transactions, and advanced features: JSON columns (semi-structured data), array columns, full-text search, window functions, Common Table Expressions (CTEs for recursive queries), and native table partitioning. The most feature-rich open-source database. Use as the default choice when you're unsure.

**MS SQL Server (Microsoft SQL Server)**: Microsoft's relational database. Deep integration with .NET, Entity Framework, and Azure. Enterprise features: Always On Availability Groups (high availability), column store indexes (analytics), in-memory OLTP (high-throughput transactions). Choose over PostgreSQL when the team and infrastructure are Microsoft-oriented.

**MongoDB**: a document database that stores data as JSON-like documents (BSON format) in collections. Each document can have different fields — no schema migrations needed when adding new fields. Supports nested objects and arrays within a single document. ACID transactions available with replica sets. Built-in horizontal scaling via sharding. Choose when your data is naturally document-shaped (e.g., product catalog where each product type has different attributes) and you rarely need cross-collection joins.

**Redis**: an in-memory data store that supports multiple data structures: strings (simple cache), hashes (object-like key-value pairs), lists (queues, activity feeds), sets (unique members, tags), sorted sets (leaderboards, rankings — O(log N) insert, O(1) rank lookup), streams (append-only event log with consumer groups), and pub/sub (broadcasting events to subscribers). All operations are atomic. Sub-millisecond latency because everything is in memory. Can persist to disk for durability. Use for caching, sessions, real-time features, rate limiting, and lightweight messaging.

**Elasticsearch**: a distributed search and analytics engine based on Apache Lucene. Builds an inverted index — for every word, it stores which documents contain it. Supports full-text search with relevance scoring (BM25), fuzzy matching ("did you mean?"), autocomplete (edge-ngram analyzer), faceted filtering (filter by category + price range + rating simultaneously), and aggregations (count, sum, average, histogram). Not a primary database — sync data from your main database via CDC (Debezium) or application events.

**OpenSearch**: AWS's fork of Elasticsearch (created after Elastic changed its license). API-compatible with Elasticsearch. AWS offers it as a managed service (Amazon OpenSearch Service). Functionally equivalent to Elasticsearch for most use cases. Choose OpenSearch on AWS; choose Elasticsearch elsewhere.

**TimescaleDB**: a PostgreSQL extension optimized for time-series data. Automatically partitions data into time-based chunks (hypertables). Features: 10-20x compression, continuous aggregates (pre-computed rollups that update automatically), retention policies (auto-delete data older than N days), and familiar SQL interface (because it IS PostgreSQL). Choose for IoT sensor data, application metrics, financial tick data — any data with a timestamp as the primary dimension.

**InfluxDB**: a purpose-built time-series database with its own query language (Flux). Optimized for high write throughput and time-range queries. Choose InfluxDB when you want a standalone time-series database with its own ecosystem. Choose TimescaleDB when you want time-series capabilities within PostgreSQL.

**Neo4j**: a graph database that stores nodes (entities) and edges (relationships) as first-class citizens. Query language: Cypher. Example: `MATCH (u:User)-[:BOUGHT]->(p:Product)<-[:BOUGHT]-(other:User) RETURN other` — "find users who bought the same products as this user" is one query. In SQL, this requires multiple recursive joins that become exponentially slow at depth 3+. Choose for social networks, recommendation engines, knowledge graphs, fraud detection — any domain where relationship traversal is the core operation.

**DynamoDB**: AWS's fully managed key-value and document database. Zero operational burden — AWS handles scaling, availability, and replication automatically. Single-digit millisecond latency. Pay-per-request pricing (no provisioning). Designed for massive write throughput with linear horizontal scaling. Choose when you're on AWS, need extreme scale, and can design around its constraints (no joins, single-table design, partition key + sort key access patterns).

**Cassandra (Apache Cassandra)**: a distributed wide-column database designed for high write throughput across multiple data centers. No single point of failure — every node can accept writes (no primary/replica distinction). Linear horizontal scaling — add nodes to increase capacity. Choose for massive write volumes (100K+ writes/second), multi-datacenter replication, and use cases where you can model data around your query patterns (one table per query, denormalized).

**Debezium**: an open-source Change Data Capture (CDC) platform. Reads the database's transaction log (PostgreSQL WAL, MySQL binlog, MongoDB oplog) and publishes every insert/update/delete as an event to Kafka. The application code doesn't change — Debezium captures changes at the database level. Use to keep a search index (Elasticsearch), cache (Redis), or another database in sync with the primary database without the application having to publish events explicitly.

**Cache-aside pattern**: the application checks the cache first. On hit: return cached data instantly. On miss: query the database, store the result in the cache with a TTL (expiration time), return the data. The cache is lazy — it only caches data that is actually requested. On write: update the database, then delete the cache key (the next read repopulates it).

**Read Replica**: a copy of the primary database that stays in sync via streaming replication. Handles only read queries — all writes go to the primary. Distributes read load across multiple machines. If you have 10 read replicas, each handles 10% of read traffic. Most managed databases support this (RDS, Cloud SQL, Azure SQL).

**CQRS (Command Query Responsibility Segregation)**: a pattern that uses completely separate models for writing and reading data. The write side (commands) goes through domain logic to a primary database optimized for writes. The read side (queries) reads from a separate store optimized for fast queries (often a denormalized table or Redis cache). The read store is updated by consuming events from the write side. Use when reads and writes have fundamentally different shapes or performance needs.

**CDC (Change Data Capture)**: a technique that watches the database transaction log and streams every change (insert, update, delete) as an event. Tools like Debezium read the PostgreSQL/MySQL write-ahead log and publish changes to Kafka. The application code doesn't need to change — CDC captures changes at the database level. Use to keep a search index (Elasticsearch) or cache (Redis) in sync with the primary database.

**TTL (Time to Live)**: an expiration time set on a cached value or database record. After the TTL expires, the value is automatically deleted or marked for refresh. Example: cache a user profile with a 5-minute TTL — after 5 minutes, the next request fetches fresh data from the database. Every cached value should have a TTL to prevent stale data from living forever.

**Event Sourcing**: instead of storing the current state of an entity (overwriting the old value), you store every event that happened to it as an append-only log. To get the current state, you replay all events. Example: instead of `balance = 500`, you store `Deposited 1000`, `Withdrew 300`, `Deposited 100`, `Withdrew 300` — replay gives you 500. Gives you a full audit trail, the ability to rebuild state at any point in time, and the option to derive multiple read models from the same events. Adds complexity — only use when you need the audit trail or time-travel capability.

**S3 Glacier**: Amazon's cold storage service for data archival. Extremely cheap storage ($0.004/GB/month vs $0.023/GB for standard S3) but retrieval takes minutes to hours. Use for compliance data that must be kept for years but is rarely accessed (financial records, audit logs, regulatory archives).

---

### Aspect 4: Communication

#### Sync or Async

```
"Does the user need the result immediately, or can work happen in the background?"
 │
 ├── always immediate ──→ synchronous only
 │    draw: [Client] → [API] → [Database] → response
 │    why: the user expects to see the result right away (create a ticket,
 │    see it in the list). Synchronous is simplest — one request, one response.
 │    use REST (simple, cacheable) or GraphQL (flexible field selection)
 │
 ├── some things can be background
 │    draw both paths:
 │      sync:  [Client] → [API] → [Database] → response (for reads, simple writes)
 │      async: [API] → [Queue (Kafka/SQS/RabbitMQ)] → [Worker] → [Database]
 │    why: some operations take seconds or minutes (sending email, generating
 │    a report, processing an image). Making the user wait is bad UX.
 │    the API accepts the request (returns 202 Accepted) and puts it on a queue.
 │    a worker picks it up and processes it in the background.
 │    NOTE: if you draw async, you MUST address duplicates and failures later
 │    (the queue guarantees at-least-once, not exactly-once — duplicates happen)
 │
 └── mostly background ──→ thin API + fat queue processing
     draw: [API] → [Queue] → [Workers (auto-scaled)]
     why: when most operations are heavy (data pipeline, batch processing,
     event-driven system), the API is just a thin layer that validates and
     enqueues. All real logic lives in workers that auto-scale based on
     queue depth. Good for: email sending, report generation, ETL pipelines

```

#### Event Reactions

```
"When something happens, do other parts of the system need to react?"
 │
 ├── no ──→ no event bus needed, keep it simple
 │    why: an event bus adds operational complexity (Kafka cluster or RabbitMQ broker
 │    to manage, monitor, and debug). If only one service handles each event,
 │    a direct function call or database transaction is simpler and more reliable
 │
 ├── yes, 1-2 other things react
 │    └── RabbitMQ (simple routing, exchanges, ack/nack)
 │         or SNS+SQS on AWS (managed, zero ops)
 │         draw: [Service A] → [Event] → [Consumer B] + [Consumer C]
 │         why RabbitMQ: flexible routing patterns (routing keys, topic exchanges)
 │         why SNS+SQS: zero operational burden, AWS handles everything
 │
 ├── yes, 3+ things react, or need to replay old events
 │    └── Apache Kafka (durable log, independent consumer groups, replay)
 │         draw: [Service A] → [Kafka Topic] → [Consumer Group 1]
 │                                             [Consumer Group 2]
 │                                             [Consumer Group 3]
 │         why Kafka: each consumer reads at its own pace, can rewind and reprocess
 │         NOTE: Kafka = at-least-once delivery → consumers MUST be idempotent
 │
 └── no answer / "you decide" ──→ check domain defaults table
     SaaS / e-commerce / notification systems almost always need events
     say: "I'll add an event bus now because [notification/analytics/search]
     will need to react to [core action]. If not, we can remove it"

```

#### Live Updates

```
"Does the UI need live updates?"
 │
 ├── no, user refreshes ──→ REST/GraphQL, no persistent connections
 │    why: the simplest approach. No persistent connections to manage,
 │    no WebSocket scaling challenges, standard HTTP caching works.
 │    most CRUD applications work perfectly fine with pull-based UX
 │
 ├── yes, bidirectional (chat, collaboration)
 │    └── WebSocket
 │         draw: [Client] ←──WebSocket──→ [Server] ←── [Redis Pub/Sub]
 │         why: full-duplex, low latency, both sides send
 │         use Redis Pub/Sub to broadcast across multiple server instances
 │
 ├── yes, server pushes only (dashboards, notifications)
 │    └── Server-Sent Events (SSE)
 │         draw: [Client] ←──SSE──── [Server] ←── [Event source]
 │         why: simpler than WebSocket, auto-reconnect built in, just HTTP
 │
 └── near-real-time OK (5-30 second delay) ──→ short polling, simplest option
      why: the client calls GET every N seconds. No persistent connections,
      no WebSocket infrastructure, works through every proxy and CDN.
      trade-off: wastes bandwidth when nothing changed (most polls return
      empty). Use when "almost real-time" is good enough and simplicity wins

```

#### External Systems

```
"Does this system talk to external systems?"
 │
 ├── no ──→ skip
 │
 ├── we call them (outbound)
 │    └── draw: [Service] → [HTTP Client + Circuit Breaker + Retry] → [External API]
 │         why circuit breaker: if their API is down, fail fast instead of hanging
 │         tool: Polly (.NET), Resilience4j (Java), tenacity (Python)
 │
 ├── they call us (inbound)
 │    └── draw: [External System] → [Webhook Endpoint + Signature Verify] → [Queue] → [Processor]
 │         why queue: respond 200 immediately, process async
 │         why signature: verify the sender is who they claim (HMAC-SHA256)
 │
 └── both ──→ draw both arrows, add an Integration Layer service
```

#### Cross-Service Failure

```
"Can one user action trigger work across multiple services? What if one fails?"
 │
 ├── no, each action stays within one service
 │    └── use a normal database transaction, no distributed complexity
 │
 ├── yes, and partial completion is unacceptable (money, orders, safety)
 │    └── Saga Pattern — each service does a local transaction and publishes an event
 │         if a downstream step fails, compensating events undo previous steps
 │         draw: [Svc A: local tx] → event → [Svc B: local tx] → event → [Svc C]
 │
 ├── yes, but a few seconds of inconsistency is acceptable
 │    └── Eventual Consistency — Svc A writes and publishes event, Svc B consumes later
 │         no saga overhead, just accept the brief delay
 │
 └── no answer / "you decide" ──→ eventual consistency for most flows,
     saga only for the critical path (payment, inventory)
```

**Saga Pattern**: a way to handle operations that span multiple services without distributed transactions. Each service performs its own local database transaction and publishes an event. The next service reacts to that event and does its own transaction. If any step fails, compensating actions undo previous steps (e.g., refund payment if inventory reservation fails). Two styles: choreography (services react to events independently — simpler, 2-3 steps) or orchestration (a central coordinator directs the flow — easier to monitor, 4+ steps).

**Eventual Consistency**: a model where different services may have temporarily different views of the same data, but they converge over time (milliseconds to seconds). Service A writes to its database and publishes an event. Service B consumes the event and updates its own data. During the gap, A and B disagree — but for most use cases (dashboards, feeds, search results), users don't notice a 2-second delay. Use for 90% of cross-service data synchronization. Reserve strong consistency for money, safety, and inventory.

**202 Accepted**: an HTTP status code meaning "I received your request and will process it later." The server puts the work on a queue and responds immediately. The client can poll a status endpoint or receive a callback/webhook when processing is complete. Use for any operation that takes more than a few seconds (report generation, file processing, email sending).

**Kafka**: an open-source distributed event streaming platform by Apache. Works as an append-only log — producers write events to topics, consumers read at their own pace. Events are retained on disk for days/weeks and can be replayed from any point. Topics are split into partitions for parallel processing. Each consumer group tracks its own read position (offset) independently. Use when you have multiple consumers reacting to the same event or need to replay/reprocess historical events.

**RabbitMQ**: an open-source message broker. Producers publish messages to exchanges, which route messages to queues based on binding rules and routing keys. Consumers pull from queues and acknowledge (ack) or reject (nack) messages. Supports flexible routing patterns: direct (exact match), topic (pattern matching like `order.*.created`), fanout (broadcast to all queues). Messages are deleted after acknowledgment — no replay. Use for point-to-point commands and flexible routing.

**SQS (Simple Queue Service)**: AWS's fully managed message queue. Zero operational burden — no clusters, no brokers, auto-scales. You send messages, receive messages, delete after processing. Built-in Dead Letter Queue support. Use when you need simple async processing on AWS without managing infrastructure.

**SNS+SQS pattern**: AWS's fan-out pattern. SNS (Simple Notification Service) is a pub/sub topic — you publish once, and SNS delivers a copy to every subscriber. Each subscriber is an SQS queue. This gives you Kafka-like fan-out (multiple consumers each get all messages) using fully managed AWS services with zero operational burden.

**WebSocket**: a protocol that upgrades an HTTP connection to a persistent, full-duplex TCP connection. Both client and server can send messages at any time. The connection stays open — no HTTP overhead per message. Use for chat, live collaboration, real-time gaming. To broadcast across multiple server instances, feed WebSocket servers from Redis Pub/Sub (Redis pushes the event to all connected servers).

**SSE (Server-Sent Events)**: a one-way HTTP protocol where the server holds the connection open and pushes events to the client. The browser automatically reconnects if the connection drops. Simpler than WebSocket because it's standard HTTP — works through all proxies and load balancers. Use for dashboards, notification feeds, live status updates where only the server sends data.

**Circuit Breaker**: a pattern that stops calling a failing service to prevent cascading failures. Three states: **Closed** (normal, requests flow through), **Open** (service is failing — all calls rejected immediately without contacting the service, returning a fallback response), **Half-Open** (after a cooldown, a few test requests check if the service recovered). Prevents one slow service from bringing down your entire system by exhausting thread pools.

**Polly**: a .NET resilience library that implements timeout, retry, circuit breaker, bulkhead, and fallback as composable policies. You wrap your HTTP client with Polly policies: `services.AddHttpClient("UserService").AddPolicyHandler(GetRetryPolicy()).AddPolicyHandler(GetCircuitBreakerPolicy())`. Every outbound HTTP call automatically gets retry + circuit breaker without changing the calling code.

**Resilience4j**: the Java equivalent of Polly. Provides circuit breaker, retry, rate limiter, bulkhead, and time limiter as decorators. Integrates with Spring Boot. The standard resilience library for Java microservices.

**Dead Letter Queue (DLQ)**: a separate queue where messages that failed processing after N retries are moved. Without a DLQ, a bad message either blocks the queue forever (poison message — all processing stops behind it) or is silently dropped (data loss). With a DLQ: message fails 3 times → moved to DLQ → an engineer inspects it, fixes the bug, replays the message. Always monitor DLQ depth and alert when it's greater than zero. Every production async system needs one.

**Redis Pub/Sub**: Redis's built-in publish/subscribe messaging. A publisher sends a message to a channel, and all subscribers connected to that channel receive it instantly. Messages are fire-and-forget — not persisted, no replay, no acknowledgment. Use for broadcasting real-time events to multiple WebSocket server instances: when User A sends a chat message, the API publishes to Redis Pub/Sub, and all WebSocket servers receive it and push to their connected clients. Not a replacement for Kafka or RabbitMQ — no durability, no consumer groups, no replay.

**SendGrid**: a cloud email delivery service (owned by Twilio). Send transactional emails (password resets, order confirmations) and marketing emails via API. Handles deliverability, bounce management, and reputation. You call their REST API with the email content; they handle SMTP delivery, ISP throttling, and compliance.

**Twilio**: a cloud communications platform. Send SMS text messages, make/receive phone calls, and send WhatsApp messages via API. You call their REST API with the message content and recipient phone number; they handle carrier delivery. The standard choice for SMS in system design.

**FCM (Firebase Cloud Messaging)**: Google's service for sending push notifications to mobile devices (Android and iOS) and web browsers. Your backend sends a notification payload to FCM; FCM delivers it to the user's device. For iOS, FCM routes through Apple's APNs (Apple Push Notification service). Free to use.

**HMAC-SHA256**: a method to verify that a webhook payload hasn't been tampered with and actually came from the expected sender. The sender computes a hash of the payload using a shared secret key and puts it in a header. The receiver recomputes the hash with the same secret and compares. If they match, the payload is authentic.

---

### Aspect 5: Consistency & Failure

#### Cross-Service Operations

```
"Can one operation span multiple services? What if one fails?"
 │
 ├── no, everything is within one service
 │    └── use a normal database transaction, no distributed complexity
 │
 ├── yes, and partial completion is unacceptable (orders, payments)
 │    └── Saga Pattern
 │         draw: [Svc A: local tx] → event → [Svc B: local tx] → event → [Svc C: local tx]
 │               failure at any step → compensating events undo previous steps
 │         choreography (simple, 2-3 steps): services react to events independently
 │         orchestration (complex, 4+ steps): central coordinator directs the flow
 │
 ├── yes, but a few seconds of inconsistency is OK
 │    └── Eventual Consistency via events
 │         draw: [Svc A: write + publish event] → [Svc B: consume + update own data]
 │         no saga overhead, just accept the brief delay
 │
 ├── yes, and I can't afford to lose the event between DB write and publish
 │    └── Transactional Outbox Pattern
 │         draw: [Svc A: write data + write event to outbox TABLE in same DB transaction]
 │               [Poller or Debezium CDC reads outbox → publishes to Kafka/RabbitMQ]
 │         why: guarantees event is published if and only if data was committed
 │
 └── no answer / "you decide" ──→ start with eventual consistency for most paths
     add saga only for the money/safety-critical path (if any)
     say: "Most cross-service flows can tolerate a few seconds of inconsistency.
     For the [payment/order/safety] path I'd use a saga with compensating actions"

```

#### Duplicate Handling

```
"What happens if duplicates arrive?" (mandatory if you have async/events)
 │
 ├── doesn't matter (reads are naturally idempotent)
 │    └── no special handling
 │
 ├── duplicates are dangerous (payments, commands)
 │    └── Idempotency Key pattern
 │         client sends a UUID with each request (Idempotency-Key header)
 │         server stores processed keys in a dedup table (unique constraint)
 │         on duplicate: return the cached previous response, don't re-execute
 │
 └── for async consumers
      └── dedup table: store processed message IDs, check before processing
          or design operations as naturally idempotent (SET not INCREMENT, UPSERT not INSERT)

```

#### Database Failure

```
"What happens if the database is down?"
 │
 ├── system can be down too ──→ no special handling, acceptable
 │
 ├── must still serve reads ──→ Graceful Degradation
 │    draw: [API] → [Redis Cache: serve last known good data]
 │    if you already added Redis for read-heavy, the cache IS the fallback
 │
 ├── must still accept writes ──→ Queue-Based Load Leveling
 │    draw: [API] → [Queue: buffer writes] → [Worker: drain when DB recovers]
 │
 └── must never go down ──→ Multi-AZ database with automatic failover
     (RDS Multi-AZ, or PostgreSQL + Patroni)
     + Redis for read fallback + Queue for write buffer

```

#### Downstream Failure

```
"What happens if a downstream service is slow or down?"
 │
 └── always apply the full resilience stack:
      1. Timeout (2s internal, 5s external) — don't hang indefinitely
      2. Retry with exponential backoff + jitter (1s, 2s, 4s) — handle transient failures
      3. Circuit Breaker — after 5 failures in 30s, stop calling for 60s
      4. Graceful Degradation — return cached/default data when circuit is open
      draw: [Service A] → [Timeout + Retry + Circuit Breaker] → [Service B]
                                    ↓ circuit open
                              [Fallback: cached/default response]
```

**Saga Pattern**: a way to handle operations that span multiple services without using distributed transactions. Each service performs its own local database transaction and publishes an event. The next service reacts to that event and does its own transaction. If any step fails, compensating actions undo previous steps (e.g., refund payment if inventory reservation fails). Two styles: **choreography** — services react to events independently, no central coordinator (simpler, good for 2-3 steps); **orchestration** — a central saga coordinator tells each service what to do step by step (easier to monitor and debug, better for 4+ steps).

**Transactional Outbox**: solves the problem "how do I write to the database AND publish an event reliably?" — if the app crashes between the DB write and the Kafka publish, the event is lost. The outbox pattern writes the event to an outbox table in the same database transaction as the data change. A separate process (a poller that checks the outbox table every second, or Debezium CDC that watches the database transaction log) reads unpublished events from the outbox and publishes them to the message broker. The event is guaranteed to be published if and only if the data was committed.

**Idempotency**: the property that doing the same operation multiple times produces the same result as doing it once. Critical in distributed systems because retries are inevitable — the network can drop the response after the server processed the request, causing the client to retry. `SET balance = 100` is idempotent (same result every time). `INCREMENT balance BY 10` is not (accumulates on each retry). For non-idempotent operations, use an idempotency key: the client generates a UUID and sends it with the request. The server stores processed keys in a deduplication table. On retry with the same key, the server returns the cached previous response without re-executing.

**Graceful Degradation**: when a dependency fails, return a reduced but functional response instead of an error. Examples: recommendation service down → show popular items instead of personalized ones. Profile service down → show just the username from the JWT token. Search service down → show category browsing. The user gets a slightly worse experience, not a broken page.

**RDS (Relational Database Service)**: AWS's managed relational database. Supports PostgreSQL, MySQL, MS SQL Server, Oracle, and MariaDB. AWS handles backups, patching, replication, and failover. RDS Multi-AZ automatically creates a standby replica in another availability zone and promotes it within seconds if the primary fails. You manage the database schema and queries; AWS manages the server.

**Patroni**: an open-source tool for running a highly available PostgreSQL cluster. Manages automatic leader election and failover using a distributed consensus store (etcd, ZooKeeper, or Consul). If the primary PostgreSQL node dies, Patroni promotes a replica to primary within seconds. Use when running PostgreSQL outside of managed services (on-premises or self-hosted on VMs) and you need automatic failover.

**Multi-AZ (Multi-Availability Zone)**: running your database and services across multiple physically separate data centers within the same cloud region. If one data center loses power or network, the system continues in the others. Amazon RDS Multi-AZ automatically replicates to a standby in another AZ and promotes it within seconds if the primary fails. Costs roughly 2x the single-AZ price.

**Exponential backoff + jitter**: a retry strategy where each retry waits longer than the previous one (1 second, 2 seconds, 4 seconds) with a random offset (jitter) added. The increasing delays give the failing service time to recover. The jitter prevents the thundering herd problem — without jitter, if 1000 clients all fail at the same time, they all retry at exactly 1 second, overwhelming the service again. With jitter, retries are spread out randomly.

---

### Aspect 6: API Design

#### Service Count

```
"How many backend services?"
 │
 ├── one (monolith) ──→ no gateway needed
 │    draw: [Client] → [API]
 │    why: one service = one endpoint. No routing needed. Adding a gateway
 │    or load balancer for one service is over-engineering.
 │    good for: small team, early stage, unclear domain boundaries
 │
 ├── 2-5 services ──→ load balancer with path-based routing
 │    draw: [Client] → [Load Balancer (Nginx/ALB)] → [Service A / B / C]
 │    why: the LB routes /users → User Service, /orders → Order Service.
 │    simpler than a full API gateway — just path routing + TLS termination.
 │    each service still handles its own auth (JWT validation)
 │
 ├── 10+ services ──→ API Gateway
 │    draw: [Client] → [API Gateway (Kong/Envoy/custom)] → [Services]
 │    why: with 10+ services, you don't want each service reimplementing
 │    auth (JWT validation), rate limiting, logging, and CORS.
 │    the gateway centralizes these cross-cutting concerns in one place.
 │    also: single endpoint for clients (they don't need to know about 10 URLs)
 │
 └── no answer / default ──→ start with load balancer, add gateway when >5 services

```

#### Client API Style

```
"What API style for client-facing?"
 │
 ├── simple endpoints, same data for everyone ──→ REST
 │    why: universal, HTTP cacheable, easy for external partners
 │
 ├── different clients need different fields ──→ GraphQL
 │    why: client picks exactly what it needs, one endpoint, no over-fetching
 │    tools: Apollo Server (Node), HotChocolate (.NET), Strawberry (Python)
 │
 └── no answer / default ──→ REST (simplest, broadest compatibility)

```

#### Internal Communication

```
"How do services talk to each other internally?"
 │
 ├── need immediate response (get user profile, check inventory)
 │    └── gRPC (binary Protocol Buffers, HTTP/2, typed client generation)
 │         why: 10x smaller than JSON, compile-time type safety, fast
 │         draw: [Svc A] ──gRPC──→ [Svc B]
 │
 ├── fire-and-forget (order placed, user updated)
 │    └── use the event bus from Aspect 4 (Kafka/RabbitMQ)
 │         draw: [Svc A] ──event──→ [Svc B]
 │
 ├── both ──→ solid arrows for sync (gRPC), dashed arrows for async (events)
 │
 └── no answer / default ──→ gRPC for sync, events for async
```

**API Gateway**: a single entry point for all client requests. Sits between clients and your backend services. Centralizes cross-cutting concerns: authentication (validate JWT tokens before requests reach services), rate limiting (protect services from abuse), routing (direct `/users` to User Service, `/orders` to Order Service), protocol translation (accept REST from clients, call gRPC internally). Without a gateway, every service reimplements auth and rate limiting. Examples: Kong, AWS API Gateway, Envoy, or a custom GraphQL federation gateway.

**REST (Representational State Transfer)**: an API style where each URL represents a resource (`/users/123`). Uses standard HTTP methods (GET = read, POST = create, PUT = update, DELETE = remove). Returns JSON. Stateless — each request contains everything needed. Biggest advantage: native HTTP caching (GET responses cached via Cache-Control, ETag headers) and universal tooling (curl, Postman, any HTTP client). Best for public/external APIs.

**GraphQL**: an API query language where the client writes a query specifying exactly which fields it wants. The server returns only those fields. Single endpoint (`POST /graphql`) instead of many REST endpoints. Eliminates over-fetching (getting 50 fields when you need 3) and under-fetching (needing 5 REST calls to assemble one page). Best for frontend-facing APIs where web, mobile, and admin panels each need different data shapes. Tools: Apollo Server (Node.js), HotChocolate (.NET), Strawberry (Python).

**Kong**: an open-source API Gateway built on Nginx. Handles authentication, rate limiting, request transformation, logging, and routing as plugins. Deploy as a standalone service in front of your APIs. Managed version (Kong Konnect) available. Choose when you need a feature-rich gateway with a large plugin ecosystem.

**Envoy**: a high-performance Layer 7 proxy originally built by Lyft. Used as the data plane in service meshes (Istio) and as an API gateway/ingress controller (Contour). Supports HTTP/2, gRPC natively, advanced load balancing (weighted, circuit breaking), and rich observability (metrics, tracing). More powerful than Nginx for microservice environments. Configuration is API-driven (not file-based), allowing dynamic updates without restarts.

**Apollo Server**: a GraphQL server for Node.js. Implements the GraphQL specification, handles query parsing, validation, and execution. Supports schema federation (composing multiple GraphQL services into one gateway). Large ecosystem of tools: Apollo Studio for monitoring, Apollo Client for frontend caching and state management.

**HotChocolate**: a GraphQL server for .NET. Microsoft's ecosystem equivalent of Apollo Server. Supports schema federation (HotChocolate Fusion) for composing multiple .NET microservices into one GraphQL gateway. Generates typed resolvers from C# classes.

**Protocol Buffers (protobuf)**: Google's binary serialization format used by gRPC. You define message types and service methods in `.proto` files. A code generator creates typed classes and client/server stubs in your language (C#, Java, Python, Go). Payloads are 10x smaller than JSON because fields are encoded as binary numbers instead of text key names. Not human-readable — you need the `.proto` file to decode them.

**gRPC (Google Remote Procedure Call)**: a framework for calling functions on a remote service using binary Protocol Buffers over HTTP/2. You define the API contract in a `.proto` file, and a code generator creates typed client and server code in your language. Payloads are 10x smaller than JSON. A field change in the `.proto` file causes a compile error in the consumer, not a runtime crash. HTTP/2 multiplexing means many calls share one connection. Best for internal service-to-service communication where performance and type safety matter.

---

### Aspect 7: Security

#### Authentication Method

```
"How do users authenticate?"
 │
 ├── web app (browser) ──→ OAuth2 + OIDC with PKCE
 │    draw: [Browser] → [Identity Provider (Auth0/Keycloak/Cognito)] → [JWT Token] → [API validates]
 │    why PKCE: browser can't store a secret safely, PKCE protects the auth code
 │    short-lived access tokens (15 min) + long-lived refresh tokens (7 days)
 │
 ├── machine-to-machine (other services, cron jobs) ──→ Client Credentials flow
 │    draw: [Service] → [Identity Provider] → [JWT] → [Target API]
 │    why: no user is involved — the service itself authenticates using its
 │    client_id + client_secret (stored in a secrets manager, never in code).
 │    the identity provider returns a JWT the service uses to call other services
 │
 ├── external partners / third-party ──→ API Keys
 │    draw: [Partner] → [API Gateway: validate key + rate limit per key] → [Service]
 │    why: API keys are the simplest auth for machine clients. Partners include
 │    the key in a header; the gateway validates and rate-limits per key.
 │    simpler than OAuth2 for partners who just want to call your API with curl
 │
 ├── internal service-to-service within cluster ──→ mTLS or Pod Identity
 │    mTLS: both sides verify certificates (handled by service mesh or Cilium)
 │    Pod Identity (IRSA on AWS, Workload Identity on Azure): no stored credentials
 │    why: inside the cluster, there are no users — services call each other.
 │    mTLS ensures only authorized services can communicate (certificates prove
 │    identity). Pod Identity lets pods access cloud services (S3, databases)
 │    without storing any API keys or passwords — credentials rotate automatically
 │
 └── no answer / "you decide" ──→ OAuth2 + OIDC + JWT (industry standard)
     say: "I'll use OAuth2 with OIDC for authentication and JWT tokens for
     authorization. Short-lived access tokens (15 min) + refresh tokens (7 days).
     This is the industry standard and works with any identity provider"

```

#### Permission Levels

```
"Are there different permission levels?"
 │
 ├── no ──→ simple authenticated/not check, no authorization layer
 │    why: if all logged-in users can do everything, a simple "is the token valid?"
 │    check is enough. No roles, no policies, no extra complexity
 │
 ├── roles (admin, editor, viewer) ──→ RBAC (Role-Based Access Control)
 │    store roles in JWT claims, check at each service
 │    why: RBAC is the simplest authorization model that covers most cases.
 │    the role is in the JWT — no database lookup needed on every request.
 │    each endpoint checks: does this user's role have permission for this action?
 │
 ├── resource-level (users can only see their own data) ──→ ownership check
 │    every query: WHERE user_id = @requesting_user AND ...
 │    why: RBAC alone isn't enough when User A shouldn't see User B's data
 │    at the same role level. Every database query must verify ownership.
 │    without this, changing `/orders/123` to `/orders/124` in the URL
 │    would show another user's order (this is called IDOR vulnerability)
 │
 ├── tenant-level (multi-tenant isolation) ──→ tenant_id scoping
 │    tenant_id in JWT, every single database query filtered by tenant
 │    why: the most critical security layer in a multi-tenant system.
 │    one missing WHERE tenant_id = @tenant clause in ANY query means
 │    Customer A sees Customer B's data. Enforce at the data access layer
 │    (base repository or query interceptor), not in controllers.
 │    test for this explicitly with cross-tenant integration tests
 │
 ├── complex / policy-based ──→ Policy Engine (OPA, Casbin, Cedar)
 │    externalize rules: "users can edit if same department AND doc not locked"
 │    why: when authorization rules go beyond simple roles — conditions like
 │    time of day, department membership, document state, approval chains.
 │    OPA evaluates rules at runtime from a centralized policy store.
 │    changes to rules don't require code deployment — just update the policy
 │
 └── no answer / default ──→ RBAC (covers 90% of cases)

```

#### Tenant Isolation

```
"Is this multi-tenant?"
 │
 ├── no ──→ standard architecture, skip tenant concerns
 │
 ├── yes, many small tenants (100+)
 │    └── shared database with tenant_id column on every table
 │         cheapest, simplest, enforce tenant filter at the data access layer
 │
 ├── yes, few large tenants with isolation needs
 │    └── database per tenant
 │         more isolation, independent scaling, but higher operational cost
 │
 ├── yes, with data residency requirements (GDPR)
 │    └── regional deployment: route each tenant to the region where their data must reside
 │         draw: [GeoDNS] → [EU Region (EU tenant data)] / [US Region (US tenant data)]
 │
 └── no answer / "you decide" ──→ shared DB + tenant_id (start here, evolve if needed)
     say: "I'll start with shared database and a tenant_id column on every table.
     It's the cheapest and simplest approach. If compliance or large customer
     isolation demands it, we can evolve to database-per-tenant later"
```

**Auth0**: a managed identity platform. Handles user registration, login, multi-factor authentication, social login (Google, GitHub), and token management. You don't build login flows — Auth0 provides hosted login pages and APIs. Returns JWT tokens. Pay per active user. Choose for fast implementation without building auth from scratch.

**Keycloak**: an open-source identity and access management server by Red Hat. Same functionality as Auth0 (login, registration, social login, SSO, token management) but self-hosted — you run it on your infrastructure. Free. Choose when you need full control, on-premises deployment, or want to avoid per-user pricing.

**Cognito (Amazon Cognito)**: AWS's managed identity service. Handles user sign-up, sign-in, and access control. Integrates with AWS services. User pools store user credentials; identity pools grant temporary AWS credentials. Choose when you're on AWS and want tight integration with other AWS services.

**Istio**: a service mesh for Kubernetes. Injects a sidecar proxy (Envoy) into every pod. The sidecar handles mTLS (mutual certificate verification between services), traffic routing (canary, blue-green, fault injection), retry/timeout/circuit breaker at the infrastructure level, and observability (metrics, traces). Adds complexity and resource overhead (one extra container per pod). Choose when you need automatic mTLS and advanced traffic management across many services.

**Linkerd**: a lightweight service mesh for Kubernetes. Same concept as Istio (sidecar proxy per pod) but simpler and less resource-intensive. Focuses on mTLS, observability, and reliability. Written in Rust (Linkerd2-proxy) for low latency and memory usage. Choose over Istio when you want service mesh features without the complexity.

**OAuth2**: an authorization framework that lets users grant third-party applications access to their data without sharing passwords. The application redirects to an identity provider (Google, Auth0, Keycloak), the user logs in there, and the provider returns an authorization code. The application exchanges the code for access tokens. The application never sees the user's password.

**OIDC (OpenID Connect)**: a layer on top of OAuth2 that adds user identity. OAuth2 alone only gives you authorization ("this token can access these resources"). OIDC adds an ID token that tells you who the user is (name, email, user ID). Use for "Login with Google/GitHub" flows.

**PKCE (Proof Key for Code Exchange)**: a security extension for OAuth2 that protects the authorization code from interception. The client generates a random secret (`code_verifier`), hashes it into a `code_challenge`, and sends the challenge with the login request. When exchanging the code for tokens, the client sends the original verifier — the server verifies the hash matches. Required for Single Page Applications and mobile apps because they can't safely store a `client_secret` (the browser/app code is visible to the user).

**JWT (JSON Web Token)**: a signed token containing user claims (user ID, roles, tenant ID, expiration) encoded as JSON. The API gateway or service verifies the signature using the identity provider's public key — no database lookup needed (stateless). The token itself contains everything to identify and authorize the user. Short-lived (15 minutes) to limit damage if stolen. Paired with a long-lived refresh token (7 days) to get new access tokens without re-login.

**mTLS (mutual TLS)**: standard TLS only verifies the server ("am I talking to the real api.example.com?"). Mutual TLS also verifies the client ("is this caller actually the Order Service?"). Both sides present certificates. Used for service-to-service communication inside a cluster where you need to ensure only authorized services can call each other. Handled by a service mesh (Istio, Linkerd) or network infrastructure — no application code changes needed.

**IRSA (IAM Roles for Service Accounts)**: an AWS feature that lets a Kubernetes pod access AWS services (S3, RDS, Secrets Manager) without storing any credentials. The pod's Kubernetes service account is federated with AWS IAM. The pod receives temporary credentials that rotate automatically. No API keys, no passwords, nothing to leak. Azure equivalent: Workload Identity.

**RBAC (Role-Based Access Control)**: users are assigned roles (admin, editor, viewer). Each role has permissions (admin can delete, editor can create/update, viewer can only read). The system checks the role before allowing an action. Store roles in JWT claims so every service can check without a database lookup: `{ "roles": ["admin"], "tenant_id": "lime-corp" }`.

**OPA (Open Policy Agent)**: an external policy engine for complex authorization rules that go beyond simple RBAC. You write rules in a declarative language (Rego): "users can edit documents only if they are in the same department AND the document is not locked AND it's during business hours." OPA evaluates the rules at runtime. Useful when authorization logic is complex, changes frequently, or needs to be consistent across multiple services.

**GDPR (General Data Protection Regulation)**: EU regulation affecting architecture. Key requirements: personal data must stay in the EU (data residency — may need multi-region deployment), users can request deletion of their data (right to be forgotten — need to find and delete data across all services), all access to personal data must be logged (audit trail), users must consent to data processing. Non-compliance fines up to 4% of global revenue.

---

### Aspect 8: Operations & Deployment

#### Team Structure

```
"How many teams will work on this?"
 │
 ├── one team (2-5 devs) ──→ Modular Monolith
 │    one deployable, clear internal module boundaries
 │    why: microservices add overhead that small teams can't afford
 │    split into services later when boundaries are proven
 │
 ├── multiple teams, each owning a domain ──→ Microservices
 │    each team owns a service + its database + its deployment pipeline
 │    why: independent releases, independent scaling, team autonomy
 │    service boundaries = team boundaries (Conway's Law)
 │
 └── no answer / default ──→ modular monolith (can always split later, can't easily merge)

```

#### Deploy Tolerance

```
"Can we tolerate downtime during deploys?"
 │
 ├── yes ──→ simple deploy (stop old, start new)
 │    why: simplest possible deployment. Acceptable for internal tools,
 │    dev/staging environments, or systems where a 30-second gap is fine
 │
 ├── no, zero downtime required ──→ Rolling Update
 │    new pod starts → passes readiness probe → old pod removed
 │    maxUnavailable: 0 (never remove before replacement is healthy)
 │    preStop hook: 5 second sleep to drain in-flight requests
 │    why: the standard approach for production services. Users never see
 │    downtime because old pods aren't removed until new pods are ready.
 │    low cost (only +1 pod during rollover). default for Kubernetes
 │
 ├── need instant rollback ──→ Blue-Green Deployment
 │    two environments: Blue (current) + Green (new)
 │    test on Green, switch load balancer, rollback = switch back
 │    why: if the new version has a problem, switching back to Blue is
 │    instant (seconds) vs re-deploying the old version (minutes).
 │    costs 2x resources during deployment but gives you a safety net
 │
 ├── risky change, want gradual validation ──→ Canary Deployment
 │    route 5% traffic to new version → monitor → increase if healthy
 │    needs weighted routing at load balancer or ingress (Nginx, Envoy, Istio)
 │    why: you test with real production traffic, not just staging.
 │    if the canary shows increased errors at 5%, you catch it before
 │    100% of users are affected. Data-driven confidence before full rollout
 │
 └── no answer / default ──→ rolling update (safe, standard, low cost)

```

#### Production Monitoring

```
"How will we know if something breaks?"
 │
 └── always draw the observability stack:
      [All Services + OpenTelemetry SDK]
           ├── traces → Tempo or Jaeger (which service was slow, full request path)
           ├── metrics → Prometheus + Grafana (request rate, error rate, latency)
           └── logs → Loki or ELK (structured logs with trace ID for correlation)
      
      alert on rates, not individual events:
        good: "error rate >5% over 5 minutes"
        bad:  "one 500 error occurred"
      
      this is never optional — include it in every design
```

**Modular Monolith**: a single deployable application with clear internal module boundaries. Modules communicate via interfaces, never by accessing each other's database tables directly. You get the simplicity of one deployment with the organizational clarity of separate domains. When a module boundary is proven stable, you can extract it into a microservice. The key insight: it's much easier to split a well-structured monolith into services than to merge poorly-designed microservices back together.

**Conway's Law**: "organizations design systems that mirror their communication structures." If you have 3 teams, you'll end up with 3 services. This isn't a bug — it's a feature. Align service boundaries with team boundaries so each team can develop, deploy, and operate their service independently without coordinating with other teams.

**Rolling Update**: Kubernetes replaces pods one at a time. A new pod starts → passes its readiness probe (confirms it can serve traffic) → Kubernetes routes traffic to it → removes one old pod. With `maxUnavailable: 0`, no old pod is removed until its replacement is healthy. Add a `preStop` hook (a 5-second sleep before shutdown) to let in-flight requests finish before the old pod is killed.

**Blue-Green Deployment**: run two identical environments. Blue is the current production. Green is the new version. Deploy and test on Green. When ready, switch the load balancer to point at Green. If something is wrong, switch back to Blue instantly. The downside: you need 2x the resources during the deployment window.

**Canary Deployment**: deploy the new version to a small number of instances and route a small percentage of real traffic (e.g., 5%) to them. Monitor error rates and latency. If the canary is healthy, gradually increase traffic (25%, 50%, 100%). If the canary shows problems, route all traffic back to the old version. Requires weighted routing at the load balancer or ingress controller.

**Readiness probe**: a health check endpoint that Kubernetes calls periodically to determine if a pod can receive traffic. If the readiness probe fails (returns non-200 or times out), Kubernetes removes the pod from the load balancer — no new requests are routed to it, but it is NOT killed. When the probe passes again, the pod is added back. Use for checking: can the database be reached? Has the initial data been loaded? Are all dependent services available? Different from liveness probe (which kills/restarts the pod on failure — only check if the process is stuck, never check dependencies in liveness).

**preStop hook**: a command that Kubernetes runs inside a container just before killing it during a shutdown (rolling update, scale-down, node drain). Typically a `sleep 5` — this gives the load balancer time to stop sending new requests and lets in-flight requests finish before the container stops. Without the preStop hook, active connections are dropped abruptly when the pod is removed.

**Kubernetes**: an open-source container orchestration platform. You describe the desired state (which containers to run, how many replicas, resource limits) and Kubernetes makes it happen — scheduling containers across a cluster of machines, auto-scaling, self-healing (restarting crashed containers), rolling updates, service discovery (DNS-based), and load balancing. Managed versions: EKS (AWS), AKS (Azure), GKE (Google Cloud). You write YAML configuration files (Deployments, Services, ConfigMaps) and apply them with `kubectl`.

**EKS (Elastic Kubernetes Service)**: AWS's managed Kubernetes. AWS runs the control plane (API server, etcd, scheduler); you manage worker nodes and deploy your applications. Integrates with AWS services: ALB for ingress, ECR for container images, IAM for pod permissions (IRSA), CloudWatch for monitoring.

**AKS (Azure Kubernetes Service)**: Azure's managed Kubernetes. Same concept as EKS but on Azure. Integrates with Azure services: Azure Load Balancer, ACR for images, Azure AD for identity, Azure Monitor for observability.

**GKE (Google Kubernetes Engine)**: Google Cloud's managed Kubernetes. Google invented Kubernetes internally (Borg), so GKE is considered the most mature managed offering. Features: Autopilot mode (Google manages nodes too), built-in Istio service mesh, integrated with Google Cloud services.

**Pod**: the smallest deployable unit in Kubernetes. A Pod contains one or more containers that share network (same IP address) and storage. In practice, most pods run a single container. Pods are ephemeral — they can be killed and replaced at any time. Don't store state in pods; use databases, caches, or queues.

**Namespace**: a logical partition within a Kubernetes cluster. Used to isolate teams, environments (dev/staging/prod), or tenants. Resources in one namespace can't see resources in another by default. Network policies can restrict cross-namespace communication. Resource quotas can limit CPU/memory per namespace.

**Kustomize**: a Kubernetes configuration management tool built into kubectl. Lets you customize YAML files without templating. You define a base configuration (deployment.yaml) and create overlays for each environment (dev: 1 replica, prod: 3 replicas, different image tag). Apply with `kubectl apply -k overlays/prod/`. Simpler than Helm because there's no template language — just plain YAML with patches.

**Helm**: a package manager for Kubernetes. Bundles YAML templates, default values, and documentation into versioned, installable packages called Charts. Use for deploying complex third-party software (Prometheus, Nginx Ingress, Cilium, cert-manager) where the upstream project maintains the chart. Pin chart versions for reproducible deployments.

**Docker**: a platform for building and running containers. A container packages your application and all its dependencies into an isolated, portable unit. You write a Dockerfile (build instructions), build an image, push to a registry (ECR, ACR, Docker Hub), and Kubernetes pulls and runs it. Docker builds the image; Kubernetes orchestrates running it at scale.

**ECR (Elastic Container Registry)**: AWS's managed Docker image registry. You push container images here after building them in CI; EKS pulls images from here when deploying pods. Supports image scanning (Trivy integration), lifecycle policies (auto-delete old images), and cross-region replication.

**ACR (Azure Container Registry)**: Azure's managed Docker image registry. Same concept as ECR but on Azure. Push images from CI, AKS pulls for deployment. Supports geo-replication, image scanning, and retention policies.

**S3 (Amazon Simple Storage Service)**: AWS's object storage. Stores files (images, videos, documents, backups, logs) as objects in buckets. Designed for 99.999999999% durability. Supports pre-signed URLs (temporary access for uploads/downloads), lifecycle policies (move to cheaper storage after N days), versioning (keep previous versions), and event notifications (trigger a Lambda or SQS message when a file is uploaded). The de facto standard for file storage in cloud architectures.

**Route 53**: AWS's managed DNS service. Translates domain names to IP addresses. Supports GeoDNS (route based on user location), health-check-based failover (route away from unhealthy endpoints), weighted routing (split traffic by percentage), and latency-based routing (route to the lowest-latency region).

**OpenTelemetry (OTel)**: a vendor-neutral open standard for instrumenting applications to produce traces, metrics, and logs. Add the OpenTelemetry SDK to your service — it automatically captures HTTP requests, database calls, gRPC calls, and message processing as spans in a distributed trace. Each request gets a unique trace ID that flows through all services. Data is exported to backends: traces to Tempo or Jaeger, metrics to Prometheus, logs to Loki. No vendor lock-in — switch backends without changing application code.

**Prometheus**: an open-source monitoring system that collects time-series metrics. It scrapes a `/metrics` HTTP endpoint on each service every 15 seconds. You query metrics with PromQL. Use for request rate, error rate, latency percentiles, CPU/memory usage. Visualize with Grafana dashboards. Alert on trends, not individual events: "error rate >5% for 5 minutes" is actionable.

**Grafana**: an open-source visualization platform. Connects to Prometheus (metrics), Loki (logs), Tempo (traces) and displays them in dashboards. You can click a metric spike → see the traces that caused it → click a trace → see the logs from that service at that time. All three signals connected by trace ID.

```
```

#### Project Timeline

```
"What's the timeline?"
 │
 ├── MVP / prove it works ──→ simplify everything
 │    monolith, one database, basic auth, skip observability for now
 │    focus on the core user flow, nothing else
 │
 ├── production-ready ──→ full architecture
 │    proper service boundaries, OAuth2 + JWT, observability,
 │    CI/CD pipeline, security scanning, health checks
 │
 └── no answer / default ──→ design for production, note what can be deferred
```

---

### Aspect 9: Infrastructure

#### Cloud Provider

```
"What cloud provider?"
 │
 ├── AWS ──→ EKS (Kubernetes), S3 (files), RDS (database), SQS (queue), MSK (Kafka)
 ├── Azure ──→ AKS, Blob Storage, Azure SQL, Azure Queue, Event Hubs
 ├── GCP ──→ GKE, GCS, Cloud SQL, Pub/Sub
 ├── multi-cloud ──→ use cloud-agnostic tools: Kubernetes, Terraform, Kafka, PostgreSQL
 └── no answer / default ──→ use generic names (object storage, managed DB, message queue)
                              swap in provider-specific names when you know

```

#### Infrastructure Management

```
"How do we manage infrastructure?"
 │
 ├── Terraform (declarative, cloud-agnostic, state file tracks what exists)
 │    why: same tool for AWS/Azure/GCP, plan shows exactly what changes before applying
 │
 ├── Pulumi (real programming languages: Python, TypeScript, C#, Go)
 │    why: complex logic (loops, conditionals) is easier in real code than HCL
 │
 ├── CloudFormation / CDK (AWS only)
 │    why: zero external dependencies, AWS manages the state
 │
 └── no answer / default ──→ Terraform (broadest compatibility, largest community)

```

#### Production Pipeline

```
"How does code get to production?"
 │
 └── always draw the CI/CD pipeline:
      [Git Push] → [Build] → [Unit Tests] → [Integration Tests (Testcontainers)]
                 → [Security Scan (SAST + dependency scan + container scan)]
                 → [Quality Gate: all pass?]
                 → [Container Registry]
                 → [Deploy to Dev (auto)] → [Deploy to Staging (auto + smoke test)]
                 → [Deploy to Production (manual approval or canary)]
      
      shared pipeline templates across all services (change once, propagate everywhere)
      breaking change detection in CI for API contracts (protobuf, GraphQL schema)
```

**HCL (HashiCorp Configuration Language)**: the declarative language used by Terraform. Looks like simplified JSON. Example: `resource "aws_s3_bucket" "data" { bucket = "my-app-data" }`. You describe what you want to exist; Terraform figures out what to create, change, or destroy.

**Pulumi**: an Infrastructure-as-Code tool like Terraform but uses real programming languages (Python, TypeScript, Go, C#) instead of HCL. Complex logic (loops, conditionals, abstractions) is easier in real code. State managed by Pulumi Cloud or self-hosted. Choose when the team prefers writing infrastructure definitions in the same language as their application.

**CloudFormation**: AWS's native Infrastructure-as-Code service. Define infrastructure in YAML or JSON templates. AWS-only (no multi-cloud). AWS manages the state — no external state file to worry about. Free to use. Choose when you're a pure AWS shop and want zero external dependencies. Verbose syntax compared to Terraform.

**CDK (Cloud Development Kit)**: AWS CDK lets you define CloudFormation resources using real programming languages (TypeScript, Python, Java, C#) instead of YAML. The CDK generates CloudFormation templates under the hood. Choose when you want CloudFormation's integration with AWS but find YAML too verbose and want the power of a real programming language.

**Ingress Controller**: a Kubernetes component that reads Ingress resource definitions and configures HTTP routing from outside the cluster to internal services. It runs as pods inside the cluster and acts as the reverse proxy / load balancer for all incoming HTTP traffic. Examples: Nginx Ingress Controller (most common), Contour (Envoy-based, used at Combination), Traefik (auto-discovery). Handles TLS termination (HTTPS), path-based routing (`/api` → API service, `/web` → frontend), host-based routing, and rate limiting.

**Terraform**: an Infrastructure-as-Code tool by HashiCorp. You write declarative configuration files (HCL language) describing the cloud resources you want (databases, Kubernetes clusters, networks, DNS records). Terraform compares the desired state with the actual state and shows you a plan of what it will create, change, or destroy. You review the plan and apply it. State is stored in a remote backend (S3, Azure Blob) with locking to prevent two people from applying at the same time. Cloud-agnostic — same tool for AWS, Azure, GCP. The key benefit: infrastructure changes are reviewed like code changes in a pull request.

**Testcontainers**: a library that spins up real Docker containers for test dependencies (databases, message brokers, caches) during integration tests. Instead of mocking MongoDB, you run a real MongoDB instance in a container. Tests are slower (seconds instead of milliseconds) but catch real bugs that mocks miss — schema issues, serialization edge cases, transaction behavior. The container starts before the test and is destroyed after. Available for .NET, Java, Python, Node.js.

**SAST (Static Application Security Testing)**: analyzes source code for security vulnerabilities without running the application. Finds patterns like SQL concatenation (injection risk), hardcoded passwords, insecure deserialization. Tools: SonarQube, Semgrep, CodeQL. Run in CI on every pull request — block merge if critical findings are detected.

**Container Registry**: a server that stores Docker container images. You push images after building them in CI, and Kubernetes pulls images from the registry when deploying. Examples: Amazon ECR (Elastic Container Registry), Azure ACR (Azure Container Registry), Docker Hub, GitHub Container Registry. Use retention policies to clean up old images and save storage costs.

---

### Aspect 10: Frontend

#### Frontend Type

```
"What kind of frontend does this system need?"
 │
 ├── web application (browser-based)
 │    │
 │    ├── mostly static content, blog, marketing site
 │    │    └── Static Site Generator (Next.js, Gatsby, Hugo) + CDN
 │    │         why: pages are pre-built at deploy time, served from CDN.
 │    │         fastest possible load time, cheapest hosting, no server needed
 │    │
 │    ├── interactive web app (dashboards, forms, data management)
 │    │    └── Single Page Application — React, Vue, or Angular
 │    │         draw: [Browser: SPA] → [REST or GraphQL API] → [Backend Services]
 │    │         why: the entire UI runs in the browser, API calls fetch data.
 │    │         rich interactions, fast navigation (no full page reloads).
 │    │         React: largest ecosystem, most jobs. Vue: simpler learning curve.
 │    │         Angular: opinionated, batteries-included, enterprise teams
 │    │
 │    ├── SEO matters (public content must be indexed by search engines)
 │    │    └── Server-Side Rendering — Next.js (React) or Nuxt.js (Vue)
 │    │         why: SPAs render in the browser — search engine crawlers see
 │    │         an empty HTML page. SSR renders on the server first, so
 │    │         crawlers see full content. Also faster initial page load
 │    │
 │    └── admin panel / internal tool (minimal UI investment)
 │         └── low-code admin frameworks — React Admin, Retool, or Appsmith
 │              why: admin panels are CRUD tables + forms. Building from
 │              scratch wastes time. These frameworks auto-generate UI from
 │              your API schema. Ship an admin panel in days, not weeks
 │
 ├── mobile application
 │    ├── one codebase for iOS + Android
 │    │    └── React Native or Flutter
 │    │         why: one team writes one codebase, deploys to both platforms.
 │    │         React Native: JavaScript, leverages React web knowledge.
 │    │         Flutter: Dart, better performance, consistent UI across platforms
 │    │
 │    └── platform-specific (maximum performance, platform features)
 │         └── Swift (iOS) + Kotlin (Android)
 │              why: best performance, full access to platform APIs (camera,
 │              biometrics, notifications). Requires two teams or two codebases
 │
 ├── no frontend (API-only, consumed by other services or partners)
 │    └── skip frontend entirely, focus on API documentation (OpenAPI/Swagger)
 │         why: partners and machines consume your API directly.
 │         invest in good documentation, SDKs, and developer portal instead
 │
 └── no answer / "you decide" ──→ React SPA for web (largest ecosystem),
     REST or GraphQL API, CDN for static assets
```

#### Frontend Connection

**How the frontend connects to the backend in your diagram:**
```
[Browser: SPA (React/Vue/Angular)]
     │
     ├── static assets (JS/CSS/images) served from [CDN]
     │    why: the SPA bundle is a static file — serve it from CDN for
     │    fast global delivery. Versioned filenames for instant cache invalidation
     │
     ├── API calls → [API Gateway or Load Balancer] → [Backend Services]
     │    REST: separate endpoints per resource, HTTP caching with ETag
     │    GraphQL: single endpoint, client specifies fields, one round-trip
     │
     ├── real-time → [WebSocket or SSE connection] ← [Redis Pub/Sub]
     │    for live updates (chat, notifications, dashboard refresh)
     │
     └── file uploads → [Pre-signed URL from API] → [Direct upload to S3/Blob]
          why: large files bypass the API server entirely
```

**SPA (Single Page Application)**: a web application that loads one HTML page, then dynamically updates content using JavaScript. All rendering happens in the browser — the server only provides data via API calls. Navigation between pages doesn't reload the page (client-side routing). Frameworks: React (component-based, virtual DOM, huge ecosystem), Vue (simpler API, reactive data binding), Angular (TypeScript-first, dependency injection, full framework with routing/forms/HTTP built-in).

**SSR (Server-Side Rendering)**: the server renders the HTML for each page request and sends the complete HTML to the browser. The browser displays content immediately (fast first paint). After the HTML loads, JavaScript "hydrates" the page to make it interactive. Combines the SEO benefits of server rendering with the interactivity of SPAs. Frameworks: Next.js (React + SSR), Nuxt.js (Vue + SSR).

**CSR vs SSR vs SSG**: Client-Side Rendering (CSR) = browser renders everything (SPA). Server-Side Rendering (SSR) = server renders each request. Static Site Generation (SSG) = pages are pre-built at deploy time. Use CSR for dashboards/admin (no SEO needed). Use SSR for public-facing content that needs SEO. Use SSG for content that rarely changes (blogs, docs, marketing).

---

### Aspect 11: Testing Strategy

#### Test Approach

```
"How do we test this system?"
 │
 ├── single service / monolith
 │    └── unit tests + integration tests with real database (Testcontainers)
 │         draw: [Unit Tests] → [Integration Tests (Testcontainers)] → [E2E Tests]
 │         why: unit tests verify business logic in isolation (fast, milliseconds).
 │         integration tests verify the full path (API → service → real database)
 │         using Testcontainers — a real database in Docker, not mocks.
 │         why not mocks: mocked DB tests can pass while production breaks because
 │         the mock doesn't replicate real transaction behavior, index usage, or
 │         serialization edge cases
 │
 ├── multiple services / microservices
 │    └── unit + integration per service + contract tests + E2E
 │         draw: [Unit] → [Integration (Testcontainers)] → [Contract Tests] → [E2E]
 │         why: each service is tested independently with its own database container.
 │         contract tests verify that API changes don't break consumers
 │         (buf breaking for gRPC protobuf, schema comparison for GraphQL).
 │         E2E tests hit the actual running services to verify the full path
 │
 ├── event-driven / async system
 │    └── all of the above + event contract tests + eventual consistency tests
 │         why: async systems have extra failure modes — events can be lost,
 │         duplicated, or arrive out of order
 │
 │         test examples:
 │         ├── idempotency test: send the same event twice → verify the consumer
 │         │    processes it only once (check DB state, not just response)
 │         ├── ordering test: send events A, B, C → verify consumer processes
 │         │    in correct order (especially for Kafka partition-key ordering)
 │         ├── compensating action test: trigger a saga, fail step 3 →
 │         │    verify steps 1 and 2 are rolled back via compensating events
 │         ├── eventual consistency test: write in Service A, wait N seconds,
 │         │    verify Service B's read model is updated (poll with timeout)
 │         ├── dead letter test: send a poison message (invalid payload) →
 │         │    verify it lands in the DLQ after N retries, not blocking the queue
 │         └── event schema test: change an event schema → verify consumers
 │              still handle the old format (backward compatibility)
 │
 └── no answer / "you decide" ──→ test pyramid: many unit, fewer integration, few E2E
      why: unit tests are fast and cheap (run in milliseconds, no infrastructure).
      integration tests are slower but catch real bugs (seconds, need Docker).
      E2E tests are slowest but verify the full user flow. Invest most in unit,
      least in E2E — the "testing pyramid"
```

#### Test Environments

```
"How many environments do we need?"
 │
 ├── dev + staging + production (minimum for any team)
 │    why: dev for active development (can break). staging mirrors production
 │    (same config, same data shape) for final validation. production is live.
 │
 ├── dev + staging + production + feature environments (per PR)
 │    draw: [PR created] → [Deploy to feature env] → [Test] → [Merge] → [Staging] → [Prod]
 │    why: each pull request gets its own isolated environment for testing.
 │    prevents "works on my machine" and lets multiple features be tested in parallel.
 │    cleaned up automatically when the PR is closed or merged
 │
 └── no answer / "you decide" ──→ dev + staging + production
      add feature environments later if the team is large enough to benefit
```

**Testcontainers**: a library that spins up real Docker containers (databases, message brokers, caches) during tests. Instead of mocking MongoDB, you run a real MongoDB in a Docker container. The test creates the container before the test suite, runs all tests against it, and destroys it after. Catches real bugs that mocks miss: schema mismatches, transaction behavior differences, serialization edge cases. Available for .NET (xUnit + Testcontainers.MongoDb), Java (JUnit + Testcontainers), Python (pytest-testcontainers), Node.js (testcontainers-node).

**Contract testing**: verifying that when Service A changes its API, it doesn't break Service B (the consumer). For gRPC: `buf breaking` compares proto files against the base branch and fails if backward-incompatible changes are detected (removed fields, changed field numbers). For GraphQL: schema comparison tools check if the new schema is backward-compatible. For REST: OpenAPI diff tools compare endpoint signatures. Run in CI on every PR that touches API definitions.

**Test pyramid**: a testing strategy that says: write many fast unit tests (test business logic in isolation), fewer integration tests (test with real dependencies), and very few E2E tests (test the full user flow). The pyramid shape means most bugs are caught cheaply at the bottom (unit), and only the critical user flows are verified at the top (E2E). Inverting the pyramid (many E2E, few unit) leads to slow, flaky, expensive test suites.

---

### Aspect 12: Data Migration

#### Migration Strategy

```
"Does this system need to migrate data from an existing system?"
 │
 ├── no, greenfield — starting with empty data
 │    └── skip this aspect entirely
 │
 ├── yes, one-time migration from an old database
 │    └── ETL pipeline: Extract from old → Transform to new schema → Load into new DB
 │         draw: [Old DB] → [Migration Script] → [New DB]
 │         why: a one-time script is the simplest approach. Run it during a
 │         maintenance window. Validate row counts and checksums after migration.
 │         keep the old DB read-only as a fallback for 2 weeks after migration
 │
 ├── yes, ongoing sync during migration (can't have downtime)
 │    └── dual-write or CDC (Change Data Capture)
 │         draw: [App writes to Old DB] → [CDC (Debezium)] → [New DB]
 │         OR: [App writes to both Old DB + New DB] (dual-write)
 │         why: during the migration period, both databases must stay in sync.
 │         CDC is safer (watches the DB transaction log, no application changes).
 │         dual-write is simpler but risky (if one write fails, DBs diverge).
 │         after validation, switch reads to the new DB, then stop writing to the old
 │
 ├── yes, migrating from monolith shared DB to database-per-service
 │    └── Strangler Fig for data: extract one domain at a time
 │         draw: [Shared DB] → [Extract User tables] → [User Service DB]
 │               [Shared DB] → [Extract Order tables] → [Order Service DB]
 │         why: don't try to split the entire database at once. Pick one bounded
 │         context (e.g., User), create its own database, migrate its tables,
 │         update the service to use the new DB, sync via events during transition.
 │         keep the old tables read-only as fallback until the new service is proven
 │
 └── no answer / "you decide" ──→ assume no migration for the design,
      but note that if there's an existing system, a migration plan is needed
```

**ETL (Extract, Transform, Load)**: a data migration pattern. Extract: read data from the source system. Transform: convert to the new schema (rename fields, merge tables, clean data, convert formats). Load: write to the target system. For one-time migrations, a script is enough. For ongoing sync, use CDC (Debezium) or a dedicated ETL tool (Apache Airflow, dbt, AWS Glue).

**Dual-write**: writing to two databases simultaneously from the application. Simple but dangerous — if the write to DB-A succeeds but the write to DB-B fails, the databases diverge. There's no easy way to make dual-writes atomic without distributed transactions. CDC is safer because it reads from the database's transaction log — if the write was committed, CDC captures it. If it wasn't, CDC doesn't.

---

### Aspect 13: Internationalization

#### i18n Scope

```
"Does this system need to support multiple languages, timezones, or currencies?"
 │
 ├── no, single language + single timezone + single currency
 │    └── skip this aspect, but store all timestamps in UTC anyway
 │         why: even if you're single-timezone now, storing in UTC prevents
 │         problems if you expand later. Convert to local time only in the UI
 │
 ├── multiple languages (UI text, emails, notifications)
 │    └── externalize all user-facing text into translation files
 │         draw: [UI] → [Translation Service or JSON files] → rendered text
 │         why: hardcoded strings like "Submit" or "Error occurred" can't be
 │         translated. Store translations as key-value pairs per language:
 │         { "submit_button": { "en": "Submit", "sv": "Skicka" } }
 │         frameworks: react-intl (React), vue-i18n (Vue), @angular/localize (Angular)
 │         backend: resource files (.resx in .NET, .properties in Java, gettext in Python)
 │
 ├── multiple timezones (users in different regions)
 │    └── store all timestamps in UTC in the database, convert in the UI
 │         why: if you store "2024-01-15 14:00 Stockholm time" and a user in New York
 │         reads it, they see the wrong time. Store UTC, convert to the user's
 │         timezone in the frontend: `new Date(utcTimestamp).toLocaleString(userTimezone)`
 │         store the user's preferred timezone in their profile
 │
 ├── multiple currencies (pricing, billing, financial data)
 │    └── store amounts in the smallest unit (cents) as integers, store currency code
 │         why: floating-point math causes rounding errors with money.
 │         $10.30 stored as float = 10.300000000000001. Stored as 1030 cents = exact.
 │         always store the currency code alongside the amount: { amount: 1030, currency: "SEK" }
 │         convert between currencies using an exchange rate service at display time,
 │         never store converted amounts (rates change)
 │
 └── no answer / "you decide" ──→ single language, UTC timestamps, single currency
      but build with i18n-ready patterns (externalized strings, UTC storage)
      so adding languages later doesn't require a rewrite
```

**UTC (Coordinated Universal Time)**: the global time standard. No daylight saving time, no timezone offset. Store all timestamps in UTC in the database and APIs. Convert to the user's local timezone only when displaying in the UI. This prevents confusion when users in different timezones look at the same data. Example: a ticket created at "2024-01-15T14:00:00Z" (UTC) displays as "15:00" in Stockholm (UTC+1) and "09:00" in New York (UTC-5).

---

### Aspect 14: Compliance & Audit

#### Compliance Requirements

```
"Are there compliance or regulatory requirements?"
 │
 ├── no regulatory requirements
 │    └── still add basic audit logging (who changed what, when)
 │         why: even without compliance, audit logs help debugging ("who deleted
 │         this record?") and security investigation ("when was this account accessed?")
 │
 ├── GDPR (European Union — personal data of EU residents)
 │    └── draw: [Consent Service] + [Data Deletion Service] + [Audit Log] + [Regional Deploy]
 │         requirements and how to implement:
 │         ├── data residency: EU personal data must stay in EU
 │         │    → deploy database in EU region, route EU users via GeoDNS
 │         ├── right to deletion: user requests "delete all my data"
 │         │    → build a deletion pipeline that finds and removes user data
 │         │      across ALL services and databases (including backups, logs, caches)
 │         ├── consent management: track what the user consented to
 │         │    → consent service stores per-user, per-purpose consent records
 │         ├── data access log: record who accessed personal data
 │         │    → audit log of all reads and writes to personal data fields
 │         └── data portability: user can export their data
 │              → build an export endpoint that collects user data from all services
 │
 ├── PCI DSS (Payment Card Industry — credit card data)
 │    └── draw: [Isolated Payment Service] + [Encryption] + [Audit Log] + [Network Isolation]
 │         requirements and how to implement:
 │         ├── network segmentation: payment service in its own network segment
 │         │    → separate Kubernetes namespace with strict NetworkPolicies
 │         ├── encryption: cardholder data encrypted at rest and in transit
 │         │    → TLS for transit, AES-256 with KMS-managed keys for storage
 │         ├── access control: limit who can access cardholder data
 │         │    → separate RBAC roles, MFA for payment admin access
 │         ├── audit trail: log all access to cardholder data
 │         │    → immutable audit log (append-only, tamper-proof)
 │         └── regular scanning: vulnerability scans, penetration tests
 │              → quarterly external scans, annual penetration test
 │         alternative: use Stripe/Adyen and never touch card data yourself
 │         why: letting Stripe handle PCI compliance means YOU are out of scope
 │
 ├── SOC 2 (Service Organization Controls — SaaS data security)
 │    └── draw: [Access Control] + [Audit Log] + [Encryption] + [Incident Response]
 │         requirements:
 │         ├── access controls: RBAC, MFA, least privilege
 │         ├── audit logging: who did what, when, immutable
 │         ├── encryption: at rest + in transit
 │         ├── monitoring: detect and alert on security events
 │         └── incident response: documented process for breaches
 │
 └── no answer / "you decide" ──→ add audit logging + UTC timestamps + encrypted secrets
      these are free to implement and cover the basics for any future compliance need
```

#### Audit Log Design

```
"How do we track who did what?"
 │
 ├── simple audit log (covers most cases)
 │    └── append-only table: { who, what, when, entity, old_value, new_value }
 │         store in the same database as the application data
 │         why: simple, queryable, no extra infrastructure.
 │         append-only (INSERT only, never UPDATE or DELETE) = tamper-proof
 │
 ├── compliance-grade audit log (GDPR, PCI, SOC2)
 │    └── separate, immutable audit store
 │         draw: [Application] → [Audit Events] → [Immutable Audit Store]
 │         options: append-only database table with no DELETE permission,
 │         Amazon CloudTrail, or a dedicated audit service writing to S3
 │         why: the audit log must be tamper-proof — if an attacker compromises
 │         the application database, they shouldn't be able to delete audit records.
 │         separate storage with write-only access (no delete permission) prevents this
 │
 └── no answer / "you decide" ──→ simple append-only audit table
      add: who (user_id), what (action: create/update/delete), when (UTC timestamp),
      which entity (entity_type + entity_id), what changed (old_value, new_value)
```

**Audit log**: a chronological record of who did what, when, and what changed. Stored as append-only (INSERT only, never UPDATE or DELETE) to prevent tampering. Each entry contains: who (user_id), what (action: create/update/delete), when (UTC timestamp), which entity (entity_type + entity_id), and what changed (old_value → new_value). Query it when investigating security incidents ("who accessed this account last week?"), debugging data issues ("who deleted this record?"), or compliance audits ("show all changes to customer data in the last year").

**GDPR right to deletion**: when a user requests "delete all my data", you must find and remove their data across ALL services, databases, caches, backups, and logs. This is architecturally challenging in a microservices system where user data is spread across many databases. Solution: build a deletion pipeline — a service that receives a deletion request and orchestrates removal across all data stores. Test it regularly — an untested deletion pipeline is a compliance risk.

**PCI DSS scope reduction**: instead of building your own payment processing (which requires full PCI compliance — network segmentation, encryption, regular audits, quarterly scans), use a payment provider like Stripe or Adyen. The provider handles card data; your system only stores a token (reference to the card, not the actual card number). This moves most PCI requirements to the provider and dramatically reduces your compliance scope and cost.

---

### Aspect 15: Performance

#### Performance Requirements

```
"What are the latency and throughput requirements?"
 │
 ├── no specific requirements ("just make it fast")
 │    └── target: p50 < 200ms, p99 < 1 second for API responses
 │         why: these are reasonable defaults. Users perceive anything under
 │         200ms as "instant". Anything over 1 second feels "slow". Over 3
 │         seconds and users start leaving. Measure at the API level, not
 │         just the database level — network, serialization, and middleware
 │         all add latency
 │
 ├── strict latency requirements (< 100ms, < 50ms)
 │    └── draw: [CDN] → [Edge Cache] → [API] → [Redis (cache-aside)] → [DB]
 │         why: to hit < 100ms consistently you must cache hot data in Redis
 │         (0.5ms reads), serve static content from CDN (edge-cached globally),
 │         and minimize database calls (precompute common queries).
 │         measure p99, not just p50 — the slowest 1% of requests matter most
 │
 ├── high throughput requirements (> 10K requests per second)
 │    └── draw: [CDN] → [LB] → [API x N (auto-scale)] → [Cache] → [Read Replicas]
 │         why: a single API instance handles ~1-5K RPS depending on complexity.
 │         for 10K+ you need multiple instances behind a load balancer, aggressive
 │         caching to keep database load low, and read replicas to distribute queries.
 │         horizontally scale stateless API instances with HPA
 │
 └── no answer / "you decide" ──→ p50 < 200ms, p99 < 1s, plan for 10x current load
      set up performance monitoring from day one (Prometheus + Grafana)
      so you see degradation before users feel it
```

#### Performance Testing

```
"How do we verify the system handles the expected load?"
 │
 ├── load testing before launch
 │    └── run load tests against staging with realistic traffic patterns
 │         tools: k6 (scriptable, developer-friendly), Locust (Python), Gatling (JVM)
 │         why: you can't know if the system handles 10K RPS unless you test it.
 │         run load tests that simulate real user behavior (browse, search, checkout)
 │         at 1x, 2x, 5x, 10x expected load. Find the breaking point before users do
 │
 ├── continuous performance testing in CI
 │    └── run a baseline load test on every deploy, compare against previous results
 │         why: a code change can accidentally add a slow query or an N+1 problem.
 │         running a load test in CI catches performance regressions before production.
 │         alert if p99 latency increases by more than 20% compared to the previous deploy
 │
 └── no answer / "you decide" ──→ load test before launch at minimum
      k6 is the easiest to start with (JavaScript scripts, open-source, runs locally)
```

**SLO (Service Level Objective)**: an internal target for performance. Example: "99.9% of requests complete in under 200ms." Different from SLA (Service Level Agreement), which is a contractual commitment with financial penalties. Set SLOs first (what you aim for), then SLAs (what you promise customers). Monitor SLOs with Prometheus and alert when the error budget (the allowed 0.1% failure rate) is being consumed too fast.

**p50, p95, p99 latency**: percentile measurements. p50 = the median (50% of requests are faster than this). p99 = 99% of requests are faster than this. p99 matters more than average because it represents the worst experience your users actually have. An average of 100ms might hide a p99 of 5 seconds (1 in 100 users waits 5 seconds). Always monitor and optimize p99.

**k6**: an open-source load testing tool. You write test scenarios in JavaScript that simulate user behavior (login, browse products, add to cart, checkout). k6 runs these scenarios with configurable concurrency (100 virtual users, 1000 virtual users) and reports latency percentiles, error rates, and throughput. Run locally during development or in CI for regression testing.

---

### Aspect 16: Disaster Recovery

#### Recovery Strategy

```
"What happens if a region goes down, or we lose data?"
 │
 ├── low criticality (internal tools, non-revenue systems)
 │    └── daily backups + restore procedure documented and tested
 │         RTO: hours. RPO: up to 24 hours of data loss
 │         why: daily backups are cheap and cover most scenarios.
 │         the key: TEST the restore procedure. An untested backup is not a backup
 │
 ├── medium criticality (SaaS product, customer-facing)
 │    └── automated backups (every hour) + multi-AZ + failover tested quarterly
 │         RTO: minutes. RPO: up to 1 hour of data loss
 │         draw: [Primary DB (AZ-1)] ←── sync replication ──→ [Standby DB (AZ-2)]
 │               [Automated Backups every hour → S3]
 │         why: multi-AZ database (RDS Multi-AZ, PostgreSQL + Patroni) handles
 │         AZ failure automatically. Hourly backups handle corruption/accidental
 │         deletion. Test failover quarterly to verify it actually works
 │
 ├── high criticality (payments, healthcare, financial, SLA commitments)
 │    └── multi-region active-passive + real-time replication + automated failover
 │         RTO: seconds to minutes. RPO: near-zero (synchronous replication)
 │         draw: [Primary Region] ←── async replication ──→ [DR Region]
 │               [GeoDNS: failover routing if primary health check fails]
 │         why: if an entire region goes down (rare but happens — AWS us-east-1
 │         has had multi-hour outages), the DR region takes over automatically.
 │         real-time replication keeps the DR database within seconds of primary.
 │         GeoDNS (Route 53 health checks) detects the failure and routes traffic
 │
 └── no answer / "you decide" ──→ medium criticality defaults
      daily automated backups, multi-AZ database, documented restore procedure
```

**RTO (Recovery Time Objective)**: how long can the system be down after a disaster before the business is critically impacted? RTO of 4 hours means you need to be back up within 4 hours. Drives your failover strategy: RTO of seconds → automatic failover. RTO of hours → manual restore from backup is acceptable.

**RPO (Recovery Point Objective)**: how much data can you afford to lose? RPO of 1 hour means you can lose up to 1 hour of data. Drives your backup frequency: RPO of 1 hour → hourly backups. RPO of near-zero → synchronous replication (every write is replicated before acknowledged). RPO of 24 hours → daily backups.

**Multi-region active-passive**: the primary region handles all traffic. The disaster recovery (DR) region has a replica of the database and can take over if the primary fails. The DR region is passive — it doesn't serve traffic normally. GeoDNS health checks detect when the primary region is down and route traffic to the DR region. More expensive than single-region (you pay for infrastructure in two regions) but protects against region-wide outages.

---

### Aspect 17: Cost Estimation

#### Cost Awareness

```
"How do we estimate and manage infrastructure costs?"
 │
 ├── early stage / MVP
 │    └── minimize: managed services, single region, smallest instance sizes
 │         rough cost: $100-500/month (small RDS + small EKS + S3)
 │         why: don't over-provision. Start with the smallest instance that
 │         works, monitor actual usage, right-size after 2 weeks of data.
 │         use managed services (RDS, SQS, S3) — the operational cost of
 │         self-hosting (your time) exceeds the managed service premium
 │
 ├── growth stage (proven product, increasing users)
 │    └── optimize: reserved instances, auto-scaling, cache to reduce DB load
 │         rough cost: $1,000-10,000/month
 │         why: reserved instances (1-year commitment) save 30-40% over on-demand.
 │         auto-scaling (HPA) prevents over-provisioning during off-peak hours.
 │         Redis cache reduces expensive database queries by 90%
 │
 ├── scale stage (thousands of customers, high traffic)
 │    └── govern: cost allocation per service/team, budgets, alerts on anomalies
 │         rough cost: $10,000-100,000+/month
 │         why: at this scale, a misconfigured auto-scaler or an unoptimized query
 │         can cost $10K/month. Tag all resources with service/team/environment.
 │         set budget alerts (AWS Budgets, Azure Cost Management). Review monthly
 │
 └── no answer / "you decide" ──→ start small, monitor, right-size
      say: "I'd start with the smallest instances that work, monitor actual usage
      for 2 weeks, then right-size. Managed services over self-hosted to reduce
      operational overhead. Reserved instances once traffic patterns are stable"
```

**Cost estimation shortcuts for the interview:**

```
Rough monthly costs (AWS, on-demand pricing, single region):
 │
 ├── Compute
 │    small EKS cluster (3 nodes, t3.medium): ~$200/month
 │    medium EKS cluster (5 nodes, m5.large): ~$700/month
 │    each additional pod: negligible (shares node resources)
 │
 ├── Database
 │    RDS PostgreSQL (db.t3.medium, single-AZ): ~$70/month
 │    RDS PostgreSQL (db.r5.large, multi-AZ): ~$400/month
 │    MongoDB Atlas (M10, shared): ~$60/month
 │
 ├── Cache
 │    ElastiCache Redis (cache.t3.micro): ~$15/month
 │    ElastiCache Redis (cache.r5.large): ~$200/month
 │
 ├── Storage
 │    S3: $0.023/GB/month (standard), $0.004/GB/month (Glacier)
 │    100 GB in S3 = ~$2.30/month
 │
 ├── Messaging
 │    SQS: $0.40 per million messages (extremely cheap)
 │    MSK (managed Kafka, 3 brokers): ~$500/month (expensive — use SQS if you can)
 │
 ├── CDN
 │    CloudFront: $0.085/GB for first 10 TB
 │    CloudFlare: free tier covers most small-medium sites
 │
 └── Observability
      Grafana Cloud free tier: up to 10K metrics, 50 GB logs, 50 GB traces
      Datadog: ~$15/host/month (expensive at scale — 60 services = $900/month)
      self-hosted Prometheus + Grafana + Loki: free software, pay for compute only
```

---

### After All Aspects — Validate Your Design

Go through each check. For each one, look at your diagram and ask the question. If the answer reveals a problem, add the fix to your diagram.

#### Validate: Single Point of Failure

```
Ask yourself for EVERY box on your diagram: "If this box dies, does the whole system stop?"
 │
 ├── database dies → everything stops?
 │    fix 1: multi-AZ database (RDS Multi-AZ, PostgreSQL + Patroni) — standby promotes in seconds
 │    fix 2: connection pooling (PgBouncer) — survives brief failover without dropping all connections
 │    fix 3: read replica as warm standby — promote manually if automatic failover isn't configured
 │    fix 4: if using MongoDB — replica set with 3 nodes, automatic election of new primary
 │
 ├── API server dies → no requests served?
 │    fix 1: run 2+ instances behind a load balancer — one dies, LB routes to healthy ones
 │    fix 2: Kubernetes Deployment with replicas: 3 + PodDisruptionBudget — K8s handles restarts
 │    fix 3: health checks on the LB — unhealthy instance is removed from rotation in seconds
 │    fix 4: preStop hook + graceful shutdown — in-flight requests finish before pod is killed
 │
 ├── cache (Redis) dies → database overwhelmed by all the reads it was shielded from?
 │    fix 1: Redis Sentinel — 3 sentinel instances monitor primary, auto-promote replica in ~5 seconds
 │    fix 2: Redis Cluster — data sharded across multiple nodes, one node failure doesn't lose everything
 │    fix 3: design the system to work without cache (graceful degradation) — slower but not down
 │    fix 4: use a managed Redis (ElastiCache, Azure Cache for Redis) — provider handles failover
 │
 ├── message queue dies → async processing stops, events lost?
 │    fix 1: Kafka — replication factor 3, messages stored on 3 brokers, survives any single broker failure
 │    fix 2: use managed service (Amazon MSK, Confluent Cloud) — provider handles broker health
 │    fix 3: Amazon SQS — fully managed, no brokers to worry about, AWS guarantees availability
 │    fix 4: Transactional Outbox — if the broker is down, events are saved in the DB outbox table
 │           and published when the broker recovers. No events lost even during a total broker outage
 │
 ├── API Gateway dies → nothing reaches any backend service?
 │    fix 1: run multiple gateway instances behind a load balancer (Kubernetes Deployment + HPA)
 │    fix 2: use a managed gateway (AWS API Gateway, CloudFlare) — provider handles availability
 │    fix 3: if using Kubernetes Ingress — Ingress Controller runs as a Deployment with replicas + PDB
 │
 ├── DNS dies → domain unreachable, users can't even find you?
 │    fix 1: use a managed DNS provider with global anycast (Route 53, CloudFlare) — 100% SLA
 │    fix 2: low TTL on critical records — if you need to switch providers, changes propagate fast
 │    fix 3: multiple DNS providers — configure both Route 53 AND CloudFlare as NS records
 │
 ├── single availability zone → datacenter power outage kills everything?
 │    fix 1: deploy across multiple AZs — each AZ is a separate data center with independent power
 │    fix 2: database multi-AZ — standby in another AZ, automatic failover
 │    fix 3: load balancer spans AZs — traffic automatically routes to healthy AZ
 │    fix 4: for critical systems — multi-region with GeoDNS failover (if entire region goes down)
 │
 ├── CDN dies → static assets and cached responses unavailable?
 │    fix 1: multi-CDN strategy — CloudFront primary, CloudFlare fallback
 │    fix 2: origin server can serve directly (slower, but functional) if CDN fails
 │    fix 3: CDN providers rarely go fully down — they have thousands of edge locations
 │
 ├── external dependency dies (payment provider, email service, SMS gateway)?
 │    fix 1: circuit breaker — fail fast, don't hang waiting for the dead service
 │    fix 2: queue the request — retry when the provider recovers (DLQ for persistent failures)
 │    fix 3: fallback provider — if Stripe is down, route to Adyen. If SendGrid is down, queue for later
 │    fix 4: graceful degradation — show "payment temporarily unavailable" instead of a 500 error
 │
 └── Quick test: point at each box and say "if I unplug this, what happens?"
      if the answer is "everything stops" → SPOF → add one of the fixes above
      if the answer is "that part is slower/degraded" → acceptable, not a SPOF
```

#### Validate: Bottleneck

```
 ├── "Is there one box that gets ALL the traffic?"
 │    example: all reads hit the database directly → database is the bottleneck
 │    fix 1: add Redis cache (cache-aside) — absorbs 90% of reads at sub-ms latency
 │    fix 2: add database read replicas — distribute reads across multiple instances
 │    fix 3: add CDN for static content — images, CSS, JS never hit your servers
 │    fix 4: pre-compute and materialize heavy queries — dashboard aggregations run once, not per-request
 │
 ├── "Is there one box doing too many things?"
 │    example: one service handles users + billing + notifications + admin
 │    fix 1: split by domain (bounded contexts) into separate services
 │    fix 2: if not ready to split — separate into internal modules with clear interfaces
 │    fix 3: add a queue in front of the heavy operation — decouple the work from the request
 │
 ├── "Is there a synchronous chain that's only as fast as the slowest link?"
 │    example: API → Service A → Service B → Service C — if any is slow, everything is slow
 │    fix 1: parallelize independent calls — if A and B don't depend on each other, call them concurrently
 │    fix 2: make non-critical calls async — if the notification can be sent later, don't wait for it
 │    fix 3: cache the result of expensive downstream calls — don't call Service B if you called it 5 seconds ago
 │    fix 4: use GraphQL DataLoader pattern — batch multiple calls to the same service into one
 │
 ├── "Is the database doing too much work per query?"
 │    fix 1: add proper indexes — composite indexes for multi-column WHERE clauses
 │    fix 2: analyze query plans (EXPLAIN ANALYZE) — find sequential scans, missing indexes
 │    fix 3: denormalize hot read paths — pre-join data into a read-optimized table (CQRS read model)
 │    fix 4: paginate — don't return 10,000 rows when the user sees 20 per page
 │
 └── "What happens at 10x current traffic?"
      walk through the flow at 10x and find the first thing that breaks:
      ├── LB can't handle it? → add more LB instances or use a managed LB (ALB auto-scales)
      ├── API can't handle it? → HPA auto-scales pods based on CPU
      ├── database can't handle it? → cache + read replicas + connection pooling
      ├── queue backs up? → add more consumer instances (KEDA on queue depth)
      └── single service too hot? → split into smaller services or add cache in front
```

#### Validate: Data Loss

```
 ├── "If this box crashes mid-write, is the data lost?"
 │    database crash → committed transactions are safe (WAL/journal protects them)
 │    but: data in transit (in API memory, in a variable, in a half-written response) IS lost
 │    fix 1: write to database BEFORE returning success to the client
 │    fix 2: use database transactions — either all operations commit or none do
 │    fix 3: for multi-step operations — Saga with compensating actions to undo partial work
 │
 ├── "If the queue crashes, are messages lost?"
 │    Kafka: messages persisted to disk with replication → safe (unless all replicas die simultaneously)
 │    RabbitMQ with quorum queues: messages replicated across cluster → safe
 │    Redis Pub/Sub: messages NOT persisted → lost if subscriber is down or Redis restarts
 │    Amazon SQS: fully managed, messages stored redundantly → safe
 │    fix 1: use Kafka or SQS for important messages, never Redis Pub/Sub for anything you can't afford to lose
 │    fix 2: Kafka replication factor 3 — message is on 3 brokers before it's acknowledged
 │    fix 3: RabbitMQ quorum queues (Raft-based) — message committed after majority acknowledges
 │
 ├── "Can an event be published but the database write fail (or vice versa)?"
 │    scenario: app writes to DB, then publishes to Kafka. App crashes between the two → event lost
 │    fix 1: Transactional Outbox — write data + event to outbox table in the SAME DB transaction.
 │           A separate poller or CDC (Debezium) reads the outbox and publishes to the broker.
 │           Event is guaranteed to be published if and only if the data was committed
 │    fix 2: CDC (Change Data Capture) with Debezium — watches the DB transaction log and publishes
 │           every committed change as an event. No application code changes needed
 │
 ├── "What happens if a consumer processes a message but crashes before acknowledging?"
 │    the message is redelivered → the consumer processes it again → duplicates
 │    fix 1: idempotent consumers — check a dedup table before processing (store processed message IDs)
 │    fix 2: design operations to be naturally idempotent — SET (same result every time) not INCREMENT
 │
 ├── "Are backups actually working? When was the last restore test?"
 │    fix 1: automated daily backups with retention policy (keep 30 days)
 │    fix 2: test the restore procedure quarterly — an untested backup is not a backup
 │    fix 3: point-in-time recovery (RDS PITR) — restore to any second within the retention window
 │    fix 4: store backups in a different region — protects against region-wide disasters
 │
 └── "What about accidental deletion? A developer runs DELETE without a WHERE clause?"
      fix 1: soft delete (mark as deleted, don't actually remove) — recoverable instantly
      fix 2: database point-in-time recovery — restore the table from before the deletion
      fix 3: audit log — at least you know who deleted what and when
      fix 4: limited database permissions — developers get read-only in production, only the app user can write
```

#### Validate: Security

```
 ├── "Can an unauthenticated user reach any service?"
 │    fix 1: auth validation at the API gateway — reject requests without valid JWT before they reach services
 │    fix 2: Kubernetes NetworkPolicy — only the gateway can reach backend services, not the public internet
 │    fix 3: zero-trust networking — even internal services verify the caller's identity (mTLS or pod identity)
 │
 ├── "Can a user access another user's data by changing an ID in the URL?"
 │    this is IDOR (Insecure Direct Object Reference) — OWASP Top 10
 │    fix 1: ownership check on every query — WHERE user_id = @requesting_user AND id = @requested_id
 │    fix 2: use UUIDs instead of sequential IDs — harder to guess, but this is obfuscation, NOT security
 │    fix 3: authorization middleware that checks resource ownership before the handler runs
 │    fix 4: write integration tests that specifically attempt cross-user access and verify 403 Forbidden
 │
 ├── "Can a tenant see another tenant's data?"
 │    most critical security issue in multi-tenant systems — one missing filter = data breach
 │    fix 1: tenant_id filter enforced at the data access layer (base repository), not in controllers
 │    fix 2: database row-level security (PostgreSQL RLS) — database itself rejects cross-tenant queries
 │    fix 3: integration tests that create data in tenant A and verify tenant B gets zero results
 │    fix 4: separate database schemas or databases per tenant for maximum isolation
 │
 ├── "Are secrets (passwords, API keys) in code, env vars, or Git?"
 │    fix 1: secrets manager (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault) — centralized, encrypted, audited
 │    fix 2: CSI Secrets Store Driver — mounts secrets as files in K8s pods, not environment variables
 │    fix 3: pod identity (IRSA, Workload Identity) — pods access cloud services without any stored credentials
 │    fix 4: pre-commit hooks that scan for secret patterns — catch leaked secrets before they reach Git
 │    fix 5: if a secret was ever committed to Git — rotate it immediately, then clean Git history (git filter-branch)
 │
 ├── "Is the API vulnerable to common attacks?"
 │    fix 1: rate limiting at the gateway — prevent brute force, DDoS, and credential stuffing
 │    fix 2: input validation — reject unexpected input types, lengths, and formats
 │    fix 3: parameterized queries (always) — never concatenate user input into SQL strings
 │    fix 4: CORS configuration — restrict which domains can call your API from a browser
 │    fix 5: security headers — HSTS, CSP, X-Frame-Options, X-Content-Type-Options on all responses
 │    fix 6: WAF (CloudFlare, AWS WAF) at the edge — blocks known attack patterns before they reach your app
 │
 ├── "Are container images scanned for vulnerabilities?"
 │    fix 1: Trivy or Grype scan in CI — block push to registry if critical CVE found
 │    fix 2: pin base image digests — aspnet:9.0@sha256:abc123, not just aspnet:9.0
 │    fix 3: use minimal base images — Alpine or distroless (smaller attack surface)
 │    fix 4: run containers as non-root user — USER appuser in Dockerfile
 │
 └── "Is there an audit trail of who accessed what?"
      fix 1: append-only audit log — who, what, when, which entity, old value → new value
      fix 2: separate audit storage — if the app DB is compromised, audit logs survive
      fix 3: log all authentication events — login success, login failure, MFA challenges, password resets
```

#### Validate: Debugging

```
 ├── "If a user reports 'it's slow', how do I find which service is slow?"
 │    fix 1: distributed tracing (OpenTelemetry → Tempo/Jaeger) — one trace shows the full
 │           request path with timing per service and per database call
 │    fix 2: trace ID in every response header — user support can copy the trace ID from the
 │           browser dev tools and look up the exact trace
 │    fix 3: Grafana dashboards with service-level latency (p50, p95, p99) — spot degradation
 │           before users report it
 │
 ├── "If a request fails, how do I find the error message?"
 │    fix 1: structured logging with trace ID — search by trace ID in Loki/ELK to see all
 │           log entries across all services for that single request
 │    fix 2: correlation ID propagation — every service passes the same ID through HTTP headers,
 │           gRPC metadata, and Kafka message headers
 │    fix 3: error tracking service (Sentry, Bugsnag) — groups similar errors, shows stack traces,
 │           tracks frequency and impact
 │
 ├── "How do I know if the system is degrading before users notice?"
 │    fix 1: RED method alerts — Rate (requests/sec dropping?), Errors (error % increasing?),
 │           Duration (latency p99 increasing?). Alert on trends, not individual events
 │    fix 2: SLO-based alerting — "99.9% of requests under 200ms." Alert when error budget
 │           is being consumed too fast (burn rate alert)
 │    fix 3: synthetic monitoring — a cron job calls key endpoints every minute and alerts if
 │           response time exceeds threshold or status code is not 200
 │    fix 4: real user monitoring (RUM) — JavaScript in the browser reports actual page load
 │           times to your monitoring system. Shows real user experience, not just server metrics
 │
 ├── "Can I see what's happening right now in production?"
 │    fix 1: live Grafana dashboards — request rate, error rate, latency, CPU, memory per service
 │    fix 2: kubectl top pods — real-time CPU/memory usage per pod
 │    fix 3: Kafka consumer lag monitoring — shows if consumers are falling behind producers
 │    fix 4: database connection pool metrics — shows if connections are exhausted
 │
 └── "Can I reproduce a production issue locally?"
      fix 1: structured logs with full request context — replay the exact request locally
      fix 2: feature flags — enable debug logging for a specific user or tenant in production
      fix 3: Testcontainers — run the exact same database/queue/cache versions locally in Docker
      fix 4: continuous profiling (Pyroscope) — CPU/memory flamegraphs show WHERE time is spent
```

#### Debug Flowchart — Top-Down Approach

When something goes wrong in production, follow this flow from the top down. Each level narrows the problem.

```
INCIDENT REPORTED: "something is wrong"
 │
 ├─ 1. WHAT is the symptom?
 │    ├── errors (500s, timeouts, failures)  ──→ go to ERROR FLOW below
 │    ├── slow (requests take too long)      ──→ go to LATENCY FLOW below
 │    ├── wrong data (stale, missing, wrong) ──→ go to DATA FLOW below
 │    ├── system down (nothing works)        ──→ go to OUTAGE FLOW below
 │    └── high resource usage (CPU/mem/disk) ──→ go to RESOURCE FLOW below
 │
 │
 ═══ ERROR FLOW ═══════════════════════════════════════════════════
 │
 ├─ 2. WHERE is the error?
 │    │   check: Grafana dashboard → error rate per service
 │    │   check: is it one service or many? one endpoint or all?
 │    │   check: when did it start? correlate with deploys, config changes, traffic spikes
 │    │
 │    ├── one service has errors, others are fine
 │    │    └─ 3. WHAT is the error?
 │    │       │   check: search logs by service name in Loki/ELK
 │    │       │   look for: exception message, stack trace, HTTP status code
 │    │       │   check: did it start after a deploy? → git log → diff the change
 │    │       │
 │    │       ├── database error (connection refused, timeout, deadlock)
 │    │       │    check: database metrics (active connections, CPU, disk I/O, replication lag)
 │    │       │    check: pg_stat_activity → which queries are running, which are waiting on locks
 │    │       │    check: connection pool metrics → pool exhausted? max connections reached?
 │    │       │    fix 1: connection pool exhausted → add PgBouncer (connection pooler), increase pool size
 │    │       │    fix 2: slow query holding locks → find it with pg_stat_activity, kill it, add index
 │    │       │    fix 3: deadlock → analyze the lock graph, reorder operations to prevent circular waits
 │    │       │    fix 4: disk full → check disk usage, add retention/cleanup, increase volume size
 │    │       │    fix 5: replication lag → read replica is behind, check replica I/O, network between primary and replica
 │    │       │    fix 6: too many connections → each pod opens 10 connections × 20 pods = 200. PgBouncer pools to 50
 │    │       │    prevention: set connection pool metrics alert, disk usage alert at 80%, slow query log at >1s
 │    │       │
 │    │       ├── out of memory (OOMKilled in Kubernetes)
 │    │       │    check: kubectl describe pod → see OOMKilled reason and last restart time
 │    │       │    check: Grafana memory graph → gradual leak (linear growth) or sudden spike?
 │    │       │    check: Pyroscope memory flamegraph → which objects are consuming memory?
 │    │       │    fix 1: gradual leak → find the growing collection (list/map/cache not evicted), add bounds
 │    │       │    fix 2: sudden spike → large file loaded into memory, or unbounded query result
 │    │       │    fix 3: increase memory limit if the service genuinely needs more (GC pressure at limit)
 │    │       │    fix 4: add OutOfMemoryCheck health check → detect pressure before OOM killer acts
 │    │       │    fix 5: stream large data instead of loading into memory (IAsyncEnumerable, streaming JSON)
 │    │       │    prevention: set memory usage alert at 80% of limit, review memory limits quarterly
 │    │       │
 │    │       ├── external dependency error (payment provider, email, third-party API)
 │    │       │    check: is the circuit breaker open? (Polly/Resilience4j metrics in Grafana)
 │    │       │    check: outbound request logs → what HTTP status did the external API return?
 │    │       │    check: third-party status page (status.stripe.com, status.sendgrid.com)
 │    │       │    check: did our API key expire or get rotated?
 │    │       │    check: are we hitting their rate limit? (429 Too Many Requests in response)
 │    │       │    fix 1: their fault, temporary → circuit breaker should protect, check fallback is working
 │    │       │    fix 2: their fault, prolonged → queue outbound requests, retry when recovered (DLQ for failures)
 │    │       │    fix 3: our API key expired → rotate in secrets manager, restart pods
 │    │       │    fix 4: rate limited → implement client-side rate limiting to stay under their quota
 │    │       │    fix 5: timeout too high → requests hang for 30s before failing. Lower to 2-5s + circuit breaker
 │    │       │    prevention: monitor circuit breaker state, alert when circuit opens, test fallback regularly
 │    │       │
 │    │       ├── application error (null reference, validation failure, business logic bug)
 │    │       │    check: stack trace in logs → find the exact line of code and method
 │    │       │    check: what input caused it? → log the request body/params (sanitized, no PII)
 │    │       │    check: what changed? → git log → which commit/deploy introduced this?
 │    │       │    check: is it reproducible? → try the same input in staging
 │    │       │    fix 1: recent deploy caused it → rollback immediately, investigate after
 │    │       │    fix 2: specific input triggers it → add input validation, fix the edge case
 │    │       │    fix 3: null reference → defensive coding, null checks, or use Option/Maybe types
 │    │       │    fix 4: intermittent → likely a race condition or timing issue → add logging, reproduce under load
 │    │       │    prevention: unit tests for edge cases, integration tests for the affected flow, code review
 │    │       │
 │    │       ├── config error (wrong environment variable, missing secret, wrong URL)
 │    │       │    check: kubectl describe pod → environment variables and mounted secrets
 │    │       │    check: was there a config change recently? → audit log, Helm release history
 │    │       │    check: does the secret exist in the secrets manager? → was it deleted or rotated?
 │    │       │    fix 1: secret rotated but pod not restarted → restart the pod to pick up new secret
 │    │       │    fix 2: wrong env var → fix the ConfigMap/Kustomize overlay, redeploy
 │    │       │    fix 3: missing secret → create it in the secrets manager, mount via CSI driver
 │    │       │    fix 4: wrong URL (pointing to wrong DB or service) → fix the config, redeploy
 │    │       │    prevention: startup health checks that verify config (database connectivity, secret existence)
 │    │       │
 │    │       ├── timeout errors (504 Gateway Timeout, DEADLINE_EXCEEDED)
 │    │       │    check: which downstream call is timing out? → distributed trace shows the hanging span
 │    │       │    check: is the downstream service alive? → its health check, its metrics
 │    │       │    check: is the timeout too short? → legitimate operations might take longer than configured
 │    │       │    fix 1: downstream is dead → circuit breaker should open, check if it's configured
 │    │       │    fix 2: downstream is slow → optimize it (see LATENCY FLOW), or increase timeout if legitimate
 │    │       │    fix 3: network issue between services → check DNS resolution, NetworkPolicy, service mesh
 │    │       │    fix 4: connection pool to downstream is exhausted → increase pool or add bulkhead isolation
 │    │       │    prevention: timeout on every external call (never leave default 30s/infinite), circuit breaker
 │    │       │
 │    │       └── authentication/authorization error (401 Unauthorized, 403 Forbidden)
 │    │            check: is the JWT token expired? → clock skew between services?
 │    │            check: was the user's role/permission changed? → audit log
 │    │            check: is the identity provider (Auth0, Keycloak) up? → their status page
 │    │            check: did the JWT signing key rotate? → services need the new public key
 │    │            fix 1: expired token → check token refresh flow, is the refresh token also expired?
 │    │            fix 2: clock skew → sync clocks with NTP (Chrony), add clock skew tolerance in JWT validation
 │    │            fix 3: signing key rotated → services cache the old key, add JWKS endpoint auto-refresh
 │    │            fix 4: role change → user needs to re-login to get a new token with updated claims
 │    │            prevention: short-lived tokens (15 min), JWKS auto-refresh, clock sync on all nodes
 │    │
 │    └── multiple services have errors simultaneously
 │         └─ likely a shared dependency is down or saturated
 │            check: database health → connections, CPU, replication, disk
 │            check: Redis health → memory usage, connected clients, eviction rate
 │            check: Kafka health → broker status, under-replicated partitions, disk space
 │            check: network → DNS resolution working? NetworkPolicy changed? certificate expired?
 │            check: Kubernetes → node drain happening? AZ outage? cluster autoscaler stuck?
 │            check: did someone apply a global config change? → Helm release, Kustomize, Terraform
 │            fix 1: database down → automatic failover (Multi-AZ) should handle it. If not → promote replica manually
 │            fix 2: Redis down → Sentinel should promote. If no Sentinel → system works without cache (slower)
 │            fix 3: Kafka broker down → replication should handle it. Consumer lag will spike temporarily
 │            fix 4: network/DNS → check kube-dns pods, CoreDNS logs, NetworkPolicy changes
 │            fix 5: node drain → PDB should protect. Check if PDB is configured. Reschedule pods to other nodes
 │            fix 6: certificate expired → renew cert (cert-manager should auto-renew). Check cert-manager logs
 │            prevention: health dashboards for all shared dependencies, synthetic monitoring every 60s
 │
 │
 ═══ LATENCY FLOW ════════════════════════════════════════════════
 │
 ├─ 2. WHERE is the latency?
 │    │   check: distributed trace (OpenTelemetry → Tempo/Jaeger)
 │    │   find a slow request → open the trace → see time per span
 │    │   check: is the latency in the gateway, in a service, in the database, or in an external call?
 │    │   check: is it all requests or specific endpoints? → route-level metrics in Grafana
 │    │
 │    ├── one service/span is slow, others are fast
 │    │    └─ 3. WHY is that service slow?
 │    │       │
 │    │       ├── database span is slow (most common cause)
 │    │       │    check: EXPLAIN ANALYZE on the slow query → sequential scan? missing index? large result set?
 │    │       │    check: pg_stat_activity → is the query waiting on a lock?
 │    │       │    check: database CPU → is it maxed? → query optimization or read replicas needed
 │    │       │    check: is it an N+1 query? → 10 users → 10 separate queries instead of 1 batch query
 │    │       │    fix 1: add a composite index on the filtered/sorted columns
 │    │       │    fix 2: rewrite N+1 as a batch query (DataLoader pattern, IN clause, JOIN)
 │    │       │    fix 3: add Redis cache for hot data (cache the result with TTL)
 │    │       │    fix 4: add read replicas to distribute query load
 │    │       │    fix 5: denormalize the query path (CQRS read model, materialized view)
 │    │       │    fix 6: paginate large result sets (LIMIT/OFFSET or cursor-based pagination)
 │    │       │    prevention: slow query log (>1s), query plan review in code review, load testing
 │    │       │
 │    │       ├── external API call is slow
 │    │       │    check: timeout config → is it the default 30s? most calls should timeout at 2-5s
 │    │       │    check: are retries amplifying latency? → 3 retries × 5s timeout = 15s total
 │    │       │    check: is the external API degraded? → their status page, their latency metrics
 │    │       │    fix 1: lower timeout to 2-5s → fail fast, don't wait for a dead/slow service
 │    │       │    fix 2: add circuit breaker → after N failures, stop calling for a cooldown period
 │    │       │    fix 3: cache the response if it's cacheable → Redis with TTL, don't call every time
 │    │       │    fix 4: make the call async if the user doesn't need the result immediately
 │    │       │    fix 5: add a fallback/default response when the external API is slow or down
 │    │       │    prevention: circuit breaker on every outbound call, latency dashboards per external dependency
 │    │       │
 │    │       ├── CPU-bound processing (serialization, encryption, computation)
 │    │       │    check: continuous profiling (Pyroscope CPU flamegraph) → which function is hottest?
 │    │       │    check: is it happening on every request or just specific ones?
 │    │       │    common causes and fixes:
 │    │       │    ├── N+1 queries → batch into one query (DataLoader, .Include() in EF, SELECT IN)
 │    │       │    ├── JSON serialization of huge objects → serialize only needed fields, use streaming
 │    │       │    ├── regex on large strings → pre-compile regex, limit input size
 │    │       │    ├── encryption/hashing → use hardware acceleration, cache encrypted results
 │    │       │    ├── sorting/filtering large in-memory collections → push to database (SQL ORDER BY)
 │    │       │    └── logging too much → reduce log level in production, sample verbose logs
 │    │       │    prevention: performance benchmarks in CI, Pyroscope always-on in production
 │    │       │
 │    │       ├── GC (garbage collection) pauses
 │    │       │    check: GC metrics → pause duration, frequency, heap size after GC
 │    │       │    check: is it a full GC (stop-the-world) or minor GC?
 │    │       │    fix 1: reduce object allocations → reuse objects, use object pools for hot paths
 │    │       │    fix 2: increase heap size → more room before GC triggers
 │    │       │    fix 3: tune GC settings → concurrent GC, lower pause time target
 │    │       │    fix 4: use value types instead of reference types where possible (structs in .NET, primitives in Java)
 │    │       │    prevention: monitor GC metrics, alert on pause duration > 100ms
 │    │       │
 │    │       ├── network latency between services
 │    │       │    check: are services in different AZs? → cross-AZ latency adds 1-2ms per hop
 │    │       │    check: DNS resolution slow? → check CoreDNS cache, ndots setting in resolv.conf
 │    │       │    check: service mesh overhead? → Istio/Linkerd sidecar adds 1-5ms per hop
 │    │       │    fix 1: co-locate services that call each other frequently in the same AZ
 │    │       │    fix 2: reduce number of hops → batch calls, aggregate at the gateway
 │    │       │    fix 3: fix DNS resolution → set ndots: 2 in pod spec, use FQDN for external domains
 │    │       │    fix 4: if service mesh overhead → check if you actually need the mesh features
 │    │       │
 │    │       └── cold start / initialization
 │    │            check: is the latency only on the first few requests after a deploy/scale-up?
 │    │            check: startup probe → is the service warming up caches, loading data, compiling JIT?
 │    │            fix 1: add a startup probe with generous timeout → prevent traffic before warm-up completes
 │    │            fix 2: pre-warm caches on startup → load hot data from DB into Redis before accepting traffic
 │    │            fix 3: use readiness probe → only route traffic after warm-up is done
 │    │            fix 4: for JVM/.NET → enable tiered compilation, ahead-of-time compilation (AOT)
 │    │
 │    └── everything is slow (all services, all endpoints)
 │         └─ shared resource is saturated
 │            check: database connections exhausted → all pods waiting for a connection
 │            check: Kubernetes node CPU/memory → nodes overloaded → add nodes or bigger nodes
 │            check: network saturation → large payloads, misconfigured logging, debug mode left on
 │            check: did traffic spike? → HPA should have scaled → check HPA config and max replicas
 │            check: Redis latency → if Redis is slow, everything using cache-aside is slow
 │            check: CDN miss rate → if CDN isn't caching, all requests hit origin
 │            fix 1: database connections → add PgBouncer, reduce pool size per pod, increase DB max_connections
 │            fix 2: node overload → Cluster Autoscaler should add nodes. Check if it's at max node count
 │            fix 3: traffic spike → HPA scales on CPU but may hit maxReplicas. Increase max or add queue
 │            fix 4: Redis → check if Redis is evicting keys (memory full), increase Redis memory or add cluster
 │            fix 5: CDN miss → check cache headers, cache key configuration, TTL settings
 │            prevention: load testing at 2x and 10x expected traffic before launch
 │
 │
 ═══ DATA FLOW ═══════════════════════════════════════════════════
 │
 ├─ 2. WHAT kind of data issue?
 │    │
 │    ├── stale data (user updated something but sees the old version)
 │    │    check: is this an eventual consistency issue? → read from read replica or cache?
 │    │    check: cache TTL → is stale data being served from Redis?
 │    │    check: search index lag → how far behind is Elasticsearch? check Kafka consumer lag
 │    │    check: CDN caching → is the CDN serving an old version of an API response?
 │    │    check: browser cache → did the browser cache the old response locally?
 │    │    fix 1: invalidate the specific cache key in Redis → DEL user:123:profile
 │    │    fix 2: for critical paths → read from primary database, bypass replica/cache
 │    │    fix 3: lower cache TTL for data that changes frequently (30s instead of 5min)
 │    │    fix 4: event-based cache invalidation → publish event on write, subscriber deletes cache key
 │    │    fix 5: CDN → purge the specific URL, or add cache-busting query parameter
 │    │    fix 6: browser → set proper Cache-Control headers (no-cache for dynamic, max-age for static)
 │    │    prevention: cache invalidation strategy designed upfront, not afterthought
 │    │
 │    ├── missing data (record exists in DB but not visible in the UI)
 │    │    check: tenant_id filter → is the user's JWT tenant_id matching the record's tenant_id?
 │    │    check: permissions → does the user's role allow viewing this record?
 │    │    check: soft delete → is the record marked as deleted (is_deleted = true)?
 │    │    check: pagination → is the record on a page the user hasn't scrolled to?
 │    │    check: search index → if using Elasticsearch, is the record indexed? check CDC consumer lag
 │    │    check: date filter → is there a default date range filter hiding older records?
 │    │    fix 1: tenant mismatch → investigate how the record got a different tenant_id
 │    │    fix 2: permission issue → check role assignment, check policy rules
 │    │    fix 3: search index lag → check Debezium/CDC consumer, manually trigger re-index
 │    │    fix 4: soft deleted accidentally → check audit log for who deleted it, restore if needed
 │    │    prevention: cross-tenant tests, search index lag monitoring, audit trail for all deletes
 │    │
 │    ├── wrong data (calculation error, wrong status, duplicate records)
 │    │    check: audit log → who/what changed this record last? when?
 │    │    check: event history → was the same event processed twice? (idempotency failure)
 │    │    check: race condition → did two concurrent requests update the same record?
 │    │    check: data migration → was there a migration that corrupted data?
 │    │    check: timezone → is a date/time displayed in the wrong timezone?
 │    │    fix 1: duplicate records → find via unique constraint violation, merge or remove duplicate
 │    │    fix 2: idempotency failure → fix the dedup check, add idempotency-key to the consumer
 │    │    fix 3: race condition → add optimistic locking (version column, If-Match ETag header)
 │    │    fix 4: calculation error → fix the formula, run a data correction script for affected records
 │    │    fix 5: timezone issue → ensure all dates stored as UTC, convert only in UI
 │    │    prevention: unique constraints in DB, idempotent consumers, optimistic locking on concurrent entities
 │    │
 │    ├── data in wrong state (saga stuck, workflow halted, state machine inconsistent)
 │    │    check: saga state table → which step succeeded, which failed, which is pending?
 │    │    check: DLQ → is there a failed event stuck in the Dead Letter Queue?
 │    │    check: did a service crash mid-saga? → the next event was never published
 │    │    check: compensating action failed? → the rollback itself got stuck
 │    │    fix 1: replay the stuck event from the DLQ after fixing the consumer
 │    │    fix 2: manually advance the saga state in the database (with audit trail)
 │    │    fix 3: trigger the compensating action manually for the stuck step
 │    │    fix 4: add a saga timeout → if a step doesn't complete in N minutes, auto-compensate
 │    │    prevention: saga state persistence, DLQ monitoring with alerts, saga timeout with auto-compensation
 │    │
 │    └── data lost (record existed before but is gone now)
 │         check: audit log → was it deliberately deleted? by who?
 │         check: database backup → restore the record from the latest backup
 │         check: soft delete → was it soft-deleted and can be restored?
 │         check: cascade delete → did deleting a parent record cascade-delete children?
 │         check: TTL expiry → was a retention policy too aggressive?
 │         fix 1: restore from backup → point-in-time recovery (RDS PITR)
 │         fix 2: restore from soft delete → flip is_deleted back to false
 │         fix 3: event sourcing → replay events to rebuild the record's state
 │         fix 4: fix cascade delete rules → add ON DELETE RESTRICT instead of CASCADE
 │         prevention: soft delete by default, point-in-time recovery enabled, audit all destructive operations
 │
 │
 ═══ OUTAGE FLOW ═════════════════════════════════════════════════
 │
 ├─ 2. HOW much is down?
 │    │
 │    ├── everything is down (no responses at all)
 │    │    follow this checklist top-down — each level is closer to the user:
 │    │    check 1: DNS → can you resolve the domain? (dig api.example.com, nslookup)
 │    │         if no → DNS provider issue, or domain expired, or NS records misconfigured
 │    │    check 2: CDN/edge → is CloudFlare/CloudFront responding? check their status page
 │    │         if no → edge provider outage, switch to backup CDN if configured
 │    │    check 3: load balancer → is the ALB/NLB healthy? → AWS console health check
 │    │         if no → target group has no healthy targets, check instances/pods
 │    │    check 4: Kubernetes cluster → are nodes running? (kubectl get nodes)
 │    │         if no → node pool scaling issue, or cloud provider node shortage
 │    │    check 5: pods → are pods running? (kubectl get pods -A)
 │    │         if no → all pods crashed → check events (kubectl get events --sort-by=.metadata.creationTimestamp)
 │    │    check 6: recent deploy → was there a deploy in the last hour? → rollback immediately
 │    │    check 7: certificate → TLS cert expired? cert-manager not renewing?
 │    │         cert expiry causes instant total outage — browsers refuse to connect
 │    │    check 8: cloud provider → check AWS/Azure/GCP status page → region-wide outage?
 │    │    fix 1: bad deploy → rollback (kubectl rollout undo deployment/my-app)
 │    │    fix 2: cert expired → manually renew cert, check cert-manager logs
 │    │    fix 3: cloud outage → wait, or failover to DR region if configured
 │    │    fix 4: DNS → check domain registrar, NS records, TTL
 │    │    prevention: synthetic monitoring (call your API every 60s from outside), cert expiry alerts at 30/14/7 days
 │    │
 │    ├── partially down (some endpoints work, others don't)
 │    │    check: which service is down? → kubectl get pods → status column
 │    │    ├── CrashLoopBackOff → pod is crashing on startup, restarting, crashing again
 │    │    │    check: kubectl logs <pod> -p → previous container logs (show crash reason)
 │    │    │    check: kubectl describe pod → events show OOMKilled, config errors, probe failures
 │    │    │    common: missing env var, wrong DB URL, missing secret, startup probe timeout
 │    │    │    fix: fix the config/secret, redeploy. If unclear → rollback to last working version
 │    │    │
 │    │    ├── ImagePullBackOff → can't download the container image
 │    │    │    check: image name and tag correct? (typo in image tag)
 │    │    │    check: registry credentials → imagePullSecret configured? token expired?
 │    │    │    check: image exists? → did the CI pipeline actually push it?
 │    │    │    fix: correct image tag, refresh registry credentials, verify CI pipeline succeeded
 │    │    │
 │    │    ├── Pending → pod can't be scheduled to a node
 │    │    │    check: kubectl describe pod → "Insufficient cpu" or "Insufficient memory"
 │    │    │    check: are all nodes full? → kubectl top nodes
 │    │    │    check: is the Cluster Autoscaler adding nodes? → check autoscaler logs
 │    │    │    fix: increase node pool max size, reduce resource requests on pods, add a larger node pool
 │    │    │
 │    │    └── Running but not receiving traffic
 │    │         check: readiness probe failing? → kubectl describe pod, check probe endpoint
 │    │         check: Service selector matches pod labels? → kubectl get endpoints
 │    │         check: Ingress/HTTPProxy configured correctly? → check ingress resource
 │    │         fix: fix readiness probe, fix label selectors, fix ingress routing rules
 │    │
 │    └── intermittent (works sometimes, fails sometimes)
 │         check: is it time-based? → correlate with cron jobs, traffic patterns, scaling events
 │         check: is it user-based? → specific tenant, specific user role, specific browser?
 │         check: is it endpoint-based? → one endpoint fails while others work?
 │         check: is it pod-based? → one pod is bad while others are healthy?
 │         │
 │         ├── health check flapping → readiness probe too aggressive
 │         │    check: probe timeout vs actual startup/response time
 │         │    fix: increase probe timeout, add startup probe for slow starters
 │         │
 │         ├── OOMKill cycle → pod starts, memory grows, gets killed, restarts, repeat
 │         │    check: memory graph → sawtooth pattern (grow → kill → grow → kill)
 │         │    fix: find the memory leak (Pyroscope), or increase memory limit if legitimate need
 │         │
 │         ├── connection pool exhaustion → works until pool is full, then errors until a connection is freed
 │         │    check: connection pool metrics → active connections = max pool size?
 │         │    fix: increase pool size, add PgBouncer, fix slow queries that hold connections
 │         │
 │         ├── rate limiting → hitting provider rate limits at peak traffic
 │         │    check: 429 responses in outbound logs, correlate with traffic spikes
 │         │    fix: implement client-side rate limiting, cache responses, request quota increase
 │         │
 │         ├── auto-scaling lag → new pods starting up → brief errors during initialization
 │         │    check: do errors correlate with HPA scale-up events?
 │         │    fix: startup probe, readiness probe, pre-warm cache on startup
 │         │
 │         └── DNS resolution intermittent → some lookups fail
 │              check: CoreDNS logs and metrics, kube-dns pod health
 │              check: ndots setting → pod resolves "my-service" by trying 5 FQDN variants before the right one
 │              fix: set ndots: 2 in pod spec, use FQDN for external domains, increase CoreDNS replicas
 │
 │
 ═══ RESOURCE FLOW ═══════════════════════════════════════════════
 │
 └─ 2. WHICH resource is running out?
      │
      ├── CPU maxed (pods throttled, slow responses)
      │    check: kubectl top pods → which pods are using the most CPU?
      │    check: Pyroscope CPU flamegraph → which function/method consumes CPU?
      │    check: is HPA scaling? → has it reached maxReplicas?
      │    fix 1: optimize hot code path (see CPU-bound in LATENCY FLOW above)
      │    fix 2: increase HPA maxReplicas → allow more pods to be created
      │    fix 3: increase CPU request/limit → give each pod more CPU
      │    fix 4: move expensive computation to async workers → don't block the API thread
      │    prevention: CPU usage alerts at 80%, load test to find the breaking point
      │
      ├── memory growing (approaching OOM)
      │    check: Grafana memory graph → linear growth (leak) or step function (each request adds)?
      │    check: Pyroscope heap flamegraph → which objects are growing?
      │    fix 1: if leak → find unbounded collection, add eviction/bounds, fix the code
      │    fix 2: if legitimate → increase limit, or split the workload across more instances
      │    fix 3: if cache → set maxmemory in Redis with eviction policy, bound in-memory caches
      │    prevention: memory alerts at 80% of limit, periodic review of memory usage trends
      │
      ├── disk full (database, logs, Kafka, container filesystem)
      │    check: which volume is full? → kubectl describe pod → volume mounts
      │    check: database disk → AWS console, or df -h inside container
      │    check: logs eating disk? → misconfigured log volume, debug logging left on
      │    check: Kafka disk → topic retention too long, messages not compacted
      │    fix 1: increase volume size (EBS resize, PVC expand)
      │    fix 2: add retention policy → delete old data, old logs, old Kafka messages
      │    fix 3: compress old data → Kafka compression, database table compression
      │    fix 4: archive to cold storage → S3 Glacier for old data
      │    prevention: disk usage alerts at 70% and 85%, retention policies on all storage
      │
      ├── file descriptors / connections exhausted
      │    check: "too many open files" or "connection refused" in logs
      │    check: lsof -p <pid> | wc -l → count open file descriptors
      │    check: connection pool metrics → all connections in use?
      │    fix 1: increase file descriptor limit (ulimit in container)
      │    fix 2: fix connection leak → connections opened but never closed
      │    fix 3: add connection pooling → PgBouncer for PostgreSQL, pool for HTTP clients
      │    fix 4: reduce connection pool size per pod → 5-10 is usually enough
      │    prevention: monitor open file descriptors and active connections, alert at 80%
      │
      └── Kafka consumer lag growing (events piling up, processing falling behind)
           check: Grafana → consumer lag per topic per consumer group
           check: are consumer pods running? → maybe they crashed
           check: is each message taking too long to process? → optimize consumer logic
           check: is the consumer doing synchronous external calls during processing?
           fix 1: crashed consumers → fix the crash, redeploy, they'll catch up
           fix 2: slow processing → optimize, or process in batch instead of one-by-one
           fix 3: not enough consumers → KEDA on consumer lag, add more consumer pods
           fix 4: add more partitions → allows more parallel consumers (but requires topic recreation)
           fix 5: separate fast consumers from slow ones → don't let a slow analytics consumer block notifications
           prevention: consumer lag alert (>1000 messages or >5 minutes behind), KEDA auto-scaling
```

**Debug tools quick reference:**

| Symptom | First tool to check | What to look for |
|---------|---------------------|------------------|
| Errors spiking | Grafana dashboard (error rate per service) | Which service? When did it start? Correlate with deploys |
| Slow requests | Distributed trace (Tempo/Jaeger) | Which span is slow? DB? External API? CPU? Network? |
| Specific request failed | Logs by trace ID (Loki/ELK) | Error message, stack trace, input that caused it |
| Memory growing | Grafana memory graph + Pyroscope heap flamegraph | Gradual leak (linear) or sudden spike? Which objects? |
| CPU maxed | Pyroscope CPU flamegraph | Which function is hottest? N+1? Serialization? Regex? |
| Database slow | pg_stat_activity + EXPLAIN ANALYZE | Slow queries, lock waits, sequential scans, missing indexes |
| Database connections exhausted | Connection pool metrics (Grafana) | Active = max? → PgBouncer, reduce pool per pod |
| Kafka lag growing | Kafka consumer lag metrics (Grafana) | Consumer crashed? Processing too slow? Not enough consumers? |
| Pod restarting | kubectl describe pod + kubectl logs -p | OOMKilled? Config error? Crash? Startup probe timeout? |
| Pod stuck Pending | kubectl describe pod → Events section | Insufficient CPU/memory on nodes? Node pool at max? |
| CrashLoopBackOff | kubectl logs pod -p (previous container) | Missing env var? Wrong DB URL? Missing secret? |
| ImagePullBackOff | kubectl describe pod → Events section | Wrong image tag? Registry credentials expired? Image not pushed? |
| Everything down | DNS → CDN → LB → K8s nodes → pods → logs | Follow the request path from user to DB, find where it breaks |
| Intermittent failures | Correlate with time, user, endpoint, pod | Pattern reveals root cause: scaling? pool? rate limit? DNS? |
| Certificate errors | cert-manager logs + certificate resource status | Expired? Auto-renew failed? Wrong issuer? DNS challenge failed? |
| External API failing | Circuit breaker metrics + outbound request logs | Their status page? Our API key expired? Rate limited (429)? |
| Data stale after update | Cache TTL + read replica lag + ES consumer lag | Which cache? What TTL? How far behind is the replica/index? |
| Disk full | df -h in container, EBS volume metrics, Kafka disk | Logs? DB growth? Kafka retention? Old images not cleaned? |
| Auth failures (401/403) | JWT token inspection + identity provider status | Token expired? Clock skew? Key rotated? Role changed? |

#### Validate: Consistency

```
 ├── "Can two users see contradicting data?"
 │    if acceptable for a few seconds → eventual consistency (events) is fine
 │    if never acceptable (money, inventory) → strong consistency (DB transaction or saga)
 │    fix 1: identify which paths need strong vs eventual — usually 90% eventual, 10% strong
 │    fix 2: for the strong paths — use database transactions (single service) or saga (multi-service)
 │    fix 3: for the eventual paths — set expectations in the UI ("changes may take a few seconds")
 │
 ├── "If I read immediately after writing, do I see my own change?"
 │    fix 1: read-your-own-writes — route the user's reads to the primary database for N seconds after their write
 │    fix 2: optimistic UI — the frontend shows the change immediately (before server confirms) and reconciles on next fetch
 │    fix 3: write-through cache — update Redis at the same time as the database, so the next read sees the fresh value
 │
 ├── "Can the search index show stale results?"
 │    fix 1: accept it — search lagging 2-5 seconds behind the primary database is fine for most use cases
 │    fix 2: CDC (Debezium) for near-real-time sync — changes appear in Elasticsearch within seconds
 │    fix 3: nightly full re-index as a safety net — catches any events that were missed
 │
 ├── "Can two services process the same event and end up in different states?"
 │    fix 1: idempotent consumers — processing the same event twice produces the same result
 │    fix 2: Kafka partition ordering — events for the same entity go to the same partition, processed in order
 │    fix 3: version/sequence numbers on events — consumers reject out-of-order events
 │
 └── "What if the saga compensating action also fails?"
      fix 1: compensating actions must be idempotent — safe to retry indefinitely
      fix 2: dead letter queue for failed compensations — alert and manual intervention
      fix 3: saga state machine with persistent state — resume from the last successful step after recovery
      fix 4: human escalation — some failures can't be resolved automatically (alert the operations team)
```

#### Validate: Scalability

```
 ├── "Are all services stateless?"
 │    stateless = can add instances freely. stateful = can't scale horizontally
 │    fix 1: move session data to Redis — any instance can handle any user
 │    fix 2: move uploaded files to S3 — don't store on local disk
 │    fix 3: move temp state to database — don't keep processing state in memory across requests
 │    fix 4: use external locks (Redis SETNX) instead of in-memory locks — works across instances
 │
 ├── "If traffic doubles, what breaks first?"
 │    walk through each component:
 │    ├── LB? → managed LBs (ALB) auto-scale. Self-managed (Nginx) → add instances
 │    ├── API? → HPA auto-scales on CPU/memory. Check if auto-scale is configured
 │    ├── database? → read replicas for reads, connection pooling for connections, cache for hot data
 │    ├── queue? → add consumer instances (KEDA on queue depth), Kafka partitions limit parallelism
 │    ├── cache? → Redis Cluster for horizontal scaling, or bigger instance (vertical)
 │    └── CDN? → CDN handles traffic spikes by design, this rarely breaks
 │
 ├── "Can the database handle the connection count?"
 │    each API instance opens N connections × M instances = many connections
 │    fix 1: connection pooling (PgBouncer for PostgreSQL) — limits total connections to the DB
 │    fix 2: serverless-friendly pooling (RDS Proxy, Neon) — manages connection pooling as a service
 │    fix 3: reduce connections per instance — pool size of 5-10 per pod is usually enough
 │
 └── "Can I scale down to save cost during low traffic?"
      fix 1: HPA with minReplicas: 2 — scales down overnight but keeps 2 for redundancy
      fix 2: KEDA scale-to-zero for workers — no traffic = no pods = no cost
      fix 3: spot/preemptible instances for non-critical workloads — 60-70% cheaper
      fix 4: reserved instances for baseline — on-demand for bursts
```

#### Validate: Cost

```
 ├── "Am I adding components I don't need at this scale?"
 │    a cache for 100 users is waste
 │    a message queue when everything is synchronous is waste
 │    Kafka for 10 messages/day is waste — use SQS ($0.40/million messages)
 │    Elasticsearch for simple WHERE filters is waste — use SQL indexes
 │    a service mesh for 3 services is waste — use plain HTTP + circuit breaker library
 │    microservices for a 3-person team is waste — use a modular monolith
 │    fix: start simple. Add complexity when data shows a bottleneck, not when you imagine one
 │
 ├── "Am I using managed services where I should?"
 │    self-hosting Kafka costs engineering time: cluster management, upgrades, monitoring, on-call
 │    Amazon MSK or Confluent Cloud costs money but saves engineer-weeks per year
 │    fix: calculate the total cost of ownership — managed service $ vs engineer hours for self-hosted
 │    rule of thumb: if the team has <5 engineers, always use managed services
 │
 ├── "Are there quick cost wins I'm missing?"
 │    fix 1: reserved instances (1-year commitment) — 30-40% cheaper than on-demand
 │    fix 2: right-size instances — check actual CPU/memory usage, downsize over-provisioned pods
 │    fix 3: S3 lifecycle policies — move old data to Glacier automatically (5x cheaper)
 │    fix 4: CDN for static assets — stops your servers from serving images and CSS ($0.085/GB vs compute cost)
 │    fix 5: auto-scaling down at night — if traffic drops 80% overnight, so should your instance count
 │    fix 6: log retention policies — don't keep debug logs for 90 days, 7 days is enough for most
 │
 └── "What's the monthly cost roughly?"
      use the reference in Aspect 17 (Cost Estimation) for per-component estimates
      for the interview: "I'd estimate $X-Y/month at this scale, with the main cost
      being [database/CDN bandwidth/compute], and I'd optimize that first"
```

### When the Interviewer Says "You Decide" — Domain Defaults

> [!tip] When the interviewer says "that's up to you" or "what would you suggest?", pick the domain that matches and use the defaults below. Say: "For a typical [domain], I'd assume these defaults — let me know if you'd adjust any of them."
> Fold/unfold each domain section below using the arrow next to the heading (Obsidian heading fold).

#### Domain Dashboard

|                                                                                                                                                                                                                         |                                                                                                                                                                                                                         |                                                                                                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <div style="background:rgba(239,68,68,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#SaaS B2B Platform\|SaaS / B2B]]**</span> <br> Help desk, CRM, project mgmt <br> PostgreSQL · Redis · Kafka · ES <br> OAuth2+JWT · RBAC · Multi-tenant <br> </div> | <div style="background:rgba(249,115,22,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#E-Commerce Marketplace\|E-COMMERCE]]**</span> <br> Online store, marketplace <br> PostgreSQL · Redis · Kafka · S3 <br> Saga for checkout · CDN <br> *Spiky traffic, strong consistency*</div> | <div style="background:rgba(59,130,246,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Real-Time IoT Dashboard\|REAL-TIME / IoT]]**</span> <br> Monitoring, dashboards, sensors <br> TimescaleDB · Redis · Kafka · WS <br> CQRS · KEDA · 3-tier retention <br> *Write-heavy + read-heavy*</div> |
| <div style="background:rgba(34,197,94,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Notification Messaging Platform\|NOTIFICATION / CHAT]]**</span> <br> Multi-channel messaging <br> MongoDB · Redis · Kafka · WS <br> DLQ · SendGrid · Twilio · FCM <br> *Fan-out, per-channel adapters*</div> | <div style="background:rgba(168,85,247,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Internal Tool Back-Office\|INTERNAL TOOL]]**</span> <br> Admin panel, back-office <br> PostgreSQL · REST · OIDC <br> Simple deploy, basic monitoring <br> *Small user base, minimal*</div> | <div style="background:rgba(168,85,247,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#API Developer Platform\|API PLATFORM]]**</span> <br> Developer portal, integration hub <br> PostgreSQL · Redis · REST · Webhooks <br> API keys · Rate limiter <br> *Machine clients*</div> |
| <div style="background:rgba(239,68,68,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Healthcare Telemedicine\|HEALTHCARE]]**</span> <br> Patient portal, telemedicine <br> PostgreSQL · WebRTC · S3 <br> HIPAA · MFA · Field encryption <br> *Compliance-heavy, zero data loss*</div> | <div style="background:rgba(249,115,22,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#EdTech Learning Management System\|EDTECH / LMS]]**</span> <br> Courses, quizzes, progress <br> PostgreSQL · MongoDB · CDN · Kafka <br> Video streaming, certificates <br> *Read-heavy, video bandwidth*</div> | <div style="background:rgba(59,130,246,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Social Media Content Platform\|SOCIAL MEDIA]]**</span> <br> Feeds, posts, followers <br> PostgreSQL · MongoDB · Redis · Kafka <br> Fan-out-on-write · ES · CDN <br> *Feed generation is the core*</div> |
| <div style="background:rgba(34,197,94,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Logistics Supply Chain\|LOGISTICS]]**</span> <br> Shipment tracking, fleet mgmt <br> PostgreSQL · TimescaleDB · Redis <br> Kafka · GPS · Mobile apps <br> *Multi-timezone, chain of custody*</div> | <div style="background:rgba(168,85,247,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Banking Fintech\|BANKING / FINTECH]]**</span> <br> Accounts, transfers, payments <br> PostgreSQL · Kafka · Redis <br> Serializable isolation · MFA · HSM <br> *Zero tolerance for data loss*</div> | <div style="background:rgba(168,85,247,0.15);padding:10px;border-radius:8px"><span style="font-size:1.3em">**[[#Media Streaming\|MEDIA STREAMING]]**</span> <br> Video/music, VOD, live <br> S3 · CDN · KEDA · Redis <br> HLS · Transcoding · Recs <br> *Bandwidth is the primary cost*</div> |

---

#### SaaS B2B Platform
*Help desk, CRM, project management, marketing automation*

| Aspect | Default | Tool | Why |
|--------|---------|------|-----|
| Users | 10K-100K daily active users | — | Typical B2B SaaS range |
| Primary database | Relational, multi-tenant | PostgreSQL with tenant_id column | Relational data (users, tickets, deals), ACID transactions, shared DB is cheapest to start |
| Cache | Read-heavy dashboards and lists | Redis (cache-aside, 5 min TTL) | Agents browse lists 100x more than they create tickets |
| Search | Ticket/document full-text search | Elasticsearch synced via events | Users search tickets by text, need relevance ranking and faceted filters |
| Events | Ticket created → notify agent, update analytics, check SLA | Apache Kafka | 3+ consumers react to the same event, need independent processing |
| Real-time | Agent notifications, live ticket updates | Server-Sent Events (SSE) | One-way server push is enough, simpler than WebSocket |
| Auth | User login, admin panel, API access | OAuth2 + OIDC + JWT, RBAC | Industry standard, tenant_id in JWT, roles per tenant |
| Multi-tenant | Many customers share the system | Shared DB + tenant_id on every table | Start cheapest, evolve to DB-per-tenant only if compliance requires |
| File storage | Ticket attachments | S3 with pre-signed URLs | Never proxy files through API |
| Deploy | Zero downtime | Kubernetes, rolling updates | B2B SaaS can't have maintenance windows during business hours |
| Observability | Full stack | OpenTelemetry → Tempo + Prometheus + Loki + Grafana | SLA tracking requires knowing when and why things are slow |

**Questions still to define for this domain:**
- [[#Entities\|What entities?]] → likely: Tenant, User, Ticket/Deal, Comment, Agent, Queue, SLA Policy, Notification
- [[#Cross-Service Failure\|What if assignment or notification fails?]] → eventual consistency for notifications, strong for ticket state
- [[#Permission Levels\|Permission model?]] → RBAC with tenant scoping: admin, agent, viewer per tenant
- [[#External Systems\|Integrations?]] → likely webhooks outbound (Slack, email), inbound (form submissions)
- [[#Data Retention\|How long keep data?]] → tickets: years (compliance). Logs: 30 days. Analytics: aggregated monthly

**Why these choices — how to defend them:**
- **Why PostgreSQL over MongoDB?** Tickets, users, agents, queues have clear relationships (foreign keys). You need joins (list all tickets assigned to agent X in queue Y). You need ACID transactions (assigning a ticket must atomically update ticket state + agent workload). PostgreSQL handles all of this natively.
- **Why Redis cache?** An agent dashboard lists 50 tickets sorted by priority — this query runs every time an agent looks at their screen. Caching the dashboard result in Redis (5-minute TTL) means the database handles this query once every 5 minutes instead of every second per agent.
- **Why Kafka over RabbitMQ?** When a ticket is created, the notification service, the analytics service, the SLA monitor, and the search indexer all need to know. That's 4+ consumers for one event — Kafka's consumer group model lets each consume independently. RabbitMQ would require explicit exchange bindings for each consumer.
- **Why Elasticsearch?** Users search tickets by subject, description, tags, customer name — this is full-text search with relevance ranking. SQL `LIKE '%keyword%'` can't rank results by relevance and doesn't support fuzzy matching ("recieve" should match "receive"). Elasticsearch does this natively.
- **Why shared DB + tenant_id?** With 100+ tenants, creating a separate database per tenant means 100+ database instances to manage, migrate, and back up. A shared database with a `tenant_id` column is operationally trivial. The trade-off: one large tenant's heavy queries could slow others (noisy neighbor) — mitigate with per-tenant rate limiting.
- **Why eventual consistency for notifications?** When a ticket is created, the agent notification can arrive 1-2 seconds later — no one notices. But the ticket itself must be immediately visible to the creator (strong consistency via the primary database). Notifications are fire-and-forget events via Kafka.
- **Why SSE over WebSocket?** Agent notifications are one-way: server pushes "new ticket assigned to you." The agent doesn't send messages back through this channel. SSE is simpler than WebSocket for one-way push — it's just HTTP, auto-reconnects, works through all proxies. Use WebSocket only if the product includes live chat.

---

#### E-Commerce Marketplace
*Online store, product catalog, shopping cart, checkout, shipping*

| Aspect | Default | Tool | Why |
|--------|---------|------|-----|
| Users | 100K-1M daily active, spiky during sales | — | Traffic spikes 10x during Black Friday, flash sales |
| Primary database | Product catalog, orders, users | PostgreSQL | Relational: orders have line items, products belong to categories, foreign keys prevent orphans |
| Cache | Product pages, category listings | Redis (cache-aside) + CDN for images | Product pages are read 1000x per purchase. CDN serves images globally |
| Cart | Temporary, per-user, expires | Redis with TTL (30 min expiry) | Cart is temporary (not worth persisting to SQL), needs fast access, shared across sessions |
| Events | Order placed → inventory, payment, shipping, notification, analytics all react | Apache Kafka | 5+ consumers for one event, need ordering per order_id (partition key) |
| Consistency | Strong for payment+inventory, eventual for catalog+search | Saga pattern for checkout, eventual for rest | Can't oversell inventory or double-charge. Catalog search can lag 2 seconds |
| File storage | Product images, invoices | S3 + CloudFront CDN | Images served millions of times, CDN caches globally |
| Auth | User accounts, admin panel | OAuth2 + JWT, user roles + admin roles | Separate auth for customers vs store admins |
| Deploy | Canary for checkout, rolling for rest | Kubernetes, canary for payment/checkout path | A checkout bug directly loses revenue — test with 5% traffic first |

**Questions still to define for this domain:**
- [[#Entities\|What entities?]] → User, Product, Variant, Category, Cart, Order, OrderLine, Payment, Shipment, Review
- [[#Search Needs\|Product search?]] → Elasticsearch with faceted filters (category, price range, brand, rating)
- [[#Cross-Service Operations\|Checkout saga steps?]] → Create Order → Charge Payment → Reserve Inventory → Schedule Shipping → Notify
- [[#Daily Active Users\|Peak traffic?]] → 10x normal during sales events → queue + KEDA auto-scaling
- [[#Live Updates\|Order tracking?]] → SSE for live shipment status, polling is also acceptable

**Why these choices — how to defend them:**
- **Why PostgreSQL for orders but Redis for cart?** Orders are permanent, relational (order → line items → products), and need ACID transactions (charging + creating the order must be atomic). Cart is temporary (expires in 30 minutes), needs fast reads (user adds/removes items frequently), and doesn't need joins — Redis hash with TTL is perfect.
- **Why Saga instead of a database transaction for checkout?** Checkout spans multiple services: Order Service creates the order, Payment Service charges the card, Inventory Service reserves stock, Shipping Service schedules delivery. These are separate databases — you can't wrap them in one transaction. The Saga pattern executes each step as a local transaction and publishes an event. If Payment fails → compensating action cancels the order. If Inventory fails → refund the payment. Each step is independently retryable and has a defined rollback.
- **Why strong consistency for payments but eventual for catalog?** If inventory shows "5 in stock" but the real count is 3, two customers could buy the last item — one gets an oversell error. Strong consistency (saga + idempotency) prevents this. Catalog search can lag 2 seconds — a new product appearing in search results 2 seconds late is harmless.
- **Why Kafka for order events?** When an order is placed, inventory must decrement stock, payment must charge, shipping must schedule, notifications must send, and analytics must record. That's 5 independent consumers processing the same "OrderPlaced" event. Kafka's consumer groups let each service consume at its own pace without blocking others.
- **Why canary deploys for checkout?** A bug in the checkout path directly loses revenue. Canary deploys route only 5% of checkout traffic to the new version and monitor error rates. If the canary shows increased errors, all traffic stays on the old version. Rolling updates are fine for the catalog or search service — a brief display glitch is less costly than a payment failure.

---

#### Real-Time IoT Dashboard
*Sensor data, GPS tracking, monitoring, metrics dashboards*

| Aspect | Default | Tool | Why |
|--------|---------|------|-----|
| Users | Varies, but data volume is very high | — | 1000+ devices sending data every 1-5 seconds |
| Primary database | Time-series readings, device metadata | TimescaleDB (time-series) + PostgreSQL (device metadata) | TimescaleDB: time-bucketed compression, downsampling, retention policies built-in |
| Hot data | Latest device state for dashboard | Redis (latest value per device) | Dashboard shows current state, not history — Redis serves in <1ms |
| Cold data | Historical readings for reports | TimescaleDB (months) → S3 Glacier (years) | 3-tier retention: hot (Redis, hours), warm (TimescaleDB, months), cold (S3, years) |
| Ingestion | High-throughput device data | Apache Kafka (millions of events/sec) | Kafka absorbs bursts, workers process at their own pace |
| Processing | Transform and aggregate readings | KEDA-scaled workers consuming from Kafka | Scale workers on consumer lag — if devices spike, add more workers automatically |
| Dashboard | Live updates, current state | WebSocket or SSE fed by Redis Pub/Sub | Dashboard refreshes every 2 seconds with latest readings |
| Pattern | Write-heavy ingestion + read-heavy dashboards | CQRS | Write path: Kafka → worker → TimescaleDB. Read path: Redis (latest) + TimescaleDB (historical) |

**Questions still to define for this domain:**
- [[#Entities\|What entities?]] → Device, DeviceGroup, Reading, Alert, AlertRule, Dashboard, User
- [[#Data Retention\|Retention policy?]] → raw data: 30 days. Aggregated (hourly/daily): 1 year. Archived: 7 years
- [[#Downstream Failure\|What if TimescaleDB is slow?]] → Redis serves dashboard (graceful degradation), Kafka buffers writes
- [[#External Systems\|Device protocol?]] → MQTT or HTTP ingestion endpoint → Kafka
- [[#Duplicate Handling\|Duplicate readings?]] → devices retry on network failure → deduplicate by device_id + timestamp

**Why these choices — how to defend them:**
- **Why TimescaleDB over regular PostgreSQL?** Sensor readings are append-only, time-stamped, and queried by time range ("show temperature for the last 24 hours"). TimescaleDB automatically partitions by time (hypertables), compresses old data 10-20x, and supports continuous aggregates (pre-computed hourly/daily averages that update automatically). Regular PostgreSQL would need manual partitioning, no built-in compression, and no continuous aggregates.
- **Why CQRS here?** The write path (1000+ devices writing every second) and the read path (dashboards querying latest state + historical charts) have completely different requirements. Writing raw readings to TimescaleDB is optimized for sequential append. Reading the latest device state from Redis is optimized for sub-millisecond key lookups. One database model can't optimize for both patterns simultaneously.
- **Why Redis for latest state and not just query TimescaleDB?** The dashboard shows "current temperature: 23°C" for 500 devices. Querying TimescaleDB for `SELECT * FROM readings WHERE device_id = X ORDER BY timestamp DESC LIMIT 1` for 500 devices on every dashboard refresh is expensive. Writing the latest reading to Redis (`SET device:123:latest {temp: 23}`) and reading from Redis is sub-millisecond per device — the dashboard loads in <50ms instead of 2 seconds.
- **Why Kafka for ingestion?** 1000 devices × 1 reading every 2 seconds = 500 writes/second sustained, with spikes to 5000/second when devices reconnect after a network outage. Kafka absorbs the spike (messages queue up) and workers process at TimescaleDB's pace. Without Kafka, the spike overwhelms the database directly.
- **Why KEDA over HPA?** HPA scales on CPU — but ingestion workers are I/O bound (reading from Kafka, writing to TimescaleDB), not CPU bound. KEDA scales on Kafka consumer lag — if 10,000 unprocessed messages are waiting, KEDA spins up more workers. When the lag drops to zero, KEDA scales to zero (saving cost overnight when fewer devices report).
- **Why 3-tier retention?** Storing every raw reading forever is expensive (TB/month). Raw data (every reading, every second) is only useful for a few weeks of debugging. After that, hourly/daily aggregates are sufficient for dashboards and reports. After a year, aggregated data moves to cold storage (S3 Glacier at $0.004/GB/month) for compliance.

---

#### Notification Messaging Platform
*Email, push, SMS, in-app notifications, chat*

| Aspect | Default | Tool | Why |
|--------|---------|------|-----|
| Event bus | One event triggers multiple channels | Apache Kafka | "Order confirmed" → email + push + in-app + SMS all consume independently |
| Message store | Conversations, notification history | MongoDB or PostgreSQL | Messages are document-shaped (varying content per channel). PostgreSQL if relations matter |
| Real-time | Chat, typing indicators, presence | WebSocket + Redis Pub/Sub | WebSocket for bidirectional chat. Redis Pub/Sub broadcasts across server instances |
| Presence | Online/offline/typing status | Redis with TTL (60 sec expiry) | Ephemeral state, sub-ms reads, auto-expires when user disconnects |
| Email delivery | Transactional + marketing emails | SendGrid or Amazon SES | Managed deliverability, bounce handling, ISP reputation |
| Push notifications | Mobile + web | Firebase Cloud Messaging (FCM) | Free, handles both Android and iOS, web push supported |
| SMS | Text messages | Twilio | Industry standard, global coverage, delivery receipts |
| Failure handling | Delivery failures | Dead Letter Queue + retry with backoff | Email/SMS delivery can fail (invalid address, carrier issue) — park in DLQ, alert, retry |
| Priority | Urgent vs marketing | Separate Kafka topics or priority queues | Password reset email must send in seconds, newsletter can wait hours |

**Questions still to define for this domain:**
- [[#Entities\|What entities?]] → User, NotificationPreference, Template, Notification, Conversation, Message, Channel
- [[#Permission Levels\|Who can send?]] → per-tenant rate limits (prevent spam), admin controls templates
- [[#Data Retention\|How long keep notifications?]] → in-app: 90 days. Email logs: 30 days. SMS logs: 7 days
- [[#Cross-Service Failure\|What if SendGrid is down?]] → circuit breaker, queue the email, retry when recovered
- [[#Tenant Isolation\|Multi-tenant?]] → tenant-branded templates, per-tenant sender addresses, rate limits per tenant

**Why these choices — how to defend them:**
- **Why Kafka for fan-out instead of calling each channel directly?** One "OrderConfirmed" event needs to send an email AND a push notification AND an in-app notification AND an SMS. If the API calls each channel synchronously, one slow channel (SMS gateway taking 3 seconds) blocks the response. With Kafka, the API publishes one event and returns immediately. Each channel has its own consumer processing at its own pace. If the SMS gateway is slow, email and push are unaffected.
- **Why Dead Letter Queue for delivery failures?** Email can bounce (invalid address), SMS can fail (carrier issue), push can fail (user uninstalled the app). You can't just drop these — the business needs to know delivery failed. After 3 retries with backoff, the message moves to the DLQ. An operator inspects the DLQ dashboard, sees "500 emails bounced for tenant X due to invalid addresses", and takes action (update the address list). Without DLQ, failures are silently lost.
- **Why separate adapter per channel?** Each channel has different APIs (SendGrid REST API, Twilio REST API, FCM HTTP v1 API), different rate limits (ISP throttling for email, carrier limits for SMS), different failure modes (email bounces vs SMS delivery receipts), and different retry strategies. A single "notification sender" trying to handle all channels becomes a god class. Separate adapters keep each channel's complexity isolated.
- **Why Redis for presence/typing?** "User is typing..." and "User is online" are ephemeral state — they expire in seconds and don't need to survive a restart. Redis with a 30-second TTL per user is perfect: set `user:123:typing = true EX 3` (expires in 3 seconds). If the user stops typing, the key auto-expires. No database writes needed for this transient state.
- **Why WebSocket for chat but SSE for notifications?** Chat is bidirectional — both the user and the server send messages. WebSocket supports full-duplex communication. Notifications are one-way — the server pushes "you have a new notification" and the client never responds on the same connection. SSE is simpler for one-way push (standard HTTP, auto-reconnect). Using WebSocket for one-way notifications adds unnecessary complexity.

---

#### Internal Tool Back-Office
*Admin panel, reporting, data management, employee-facing tools*

| Aspect | Default | Tool | Why |
|--------|---------|------|-----|
| Users | <1K daily active (internal employees) | — | Small, known user base |
| Database | Single relational database | PostgreSQL | No cache needed at this scale. No sharding. Simple indexes |
| API | Simple CRUD | REST with OpenAPI | No need for GraphQL (one client type), no need for gRPC (no internal services) |
| Auth | Company SSO | OIDC with company identity provider (Azure AD, Okta, Google Workspace) | Employees log in with their company account, no separate user management |
| Permissions | Admin, editor, viewer | RBAC in JWT claims | Simple role check per endpoint |
| Deploy | Downtime is acceptable | Simple deploy (stop old, start new) or basic rolling update | Employees can wait 30 seconds during a deploy |
| Monitoring | Basic | Structured logging + health check endpoint | Skip distributed tracing — one service, one database, logs are enough |
| Architecture | Monolith | Single service + single database | Do not over-engineer. No microservices, no Kafka, no Redis |

**Questions still to define for this domain:**
- [[#Entities\|What entities?]] → depends on the tool. Common: User, Role, AuditLog, [domain-specific entities]
- [[#Data Retention\|Audit logs?]] → keep for compliance (1-7 years), everything else standard retention
- [[#External Systems\|Integrations?]] → likely reads from other internal systems (databases, APIs)

---

#### API Developer Platform
*Developer portal, API gateway, integration hub, partner API*

| Aspect | Default | Tool | Why |
|--------|---------|------|-----|
| Users | Machine clients (API consumers), not humans | — | Bots, scripts, partner integrations calling your API |
| Database | API keys, client metadata, usage tracking | PostgreSQL | Relational: clients have API keys, keys have scopes, usage tracked per key |
| Rate limiting | Critical component | Redis (token bucket algorithm with INCR + EXPIRE) | Every API request checks the rate limit — must be sub-ms. Redis is shared across all API instances |
| API style | External-facing | REST with OpenAPI specification | Partners expect REST, documentation via Swagger/OpenAPI, standard HTTP status codes |
| Internal | Service-to-service behind the API | gRPC | Fast, typed, binary. Partners never see gRPC — it's internal only |
| Auth | API keys for partners, OAuth2 for trusted | API key validation at API Gateway + rate limit per key | Simple for partners (include key in header), OAuth2 client credentials for trusted integrations |
| Outbound notifications | Notify partners when events happen | Webhooks (HTTP POST callbacks) with HMAC signature | Partners register a URL, you POST events to it. Sign payloads so they can verify authenticity |
| Monitoring | Per-client metrics | Prometheus + Grafana | Track request count, error rate, and latency per API key/client. Alert on unusual patterns |
| Scaling | API gateway is the bottleneck | Kubernetes HPA on the gateway pods + Redis for rate limiting | Rate limiter (Redis) must never go down — it's the protection layer |

**Questions still to define for this domain:**
- [[#Entities\|What entities?]] → Client, APIKey, Scope, UsageRecord, WebhookSubscription, WebhookDelivery
- [[#Search Needs\|API documentation search?]] → static docs site, no Elasticsearch needed
- [[#Duplicate Handling\|Idempotency for partner calls?]] → support Idempotency-Key header on create/update endpoints
- [[#Downstream Failure\|What if a webhook delivery fails?]] → retry 3x with backoff → Dead Letter Queue → dashboard for partners to see failed deliveries

---

#### Healthcare Telemedicine
*Patient portal, telemedicine, medical records, appointment scheduling*

| Aspect | Default | Tool | Why |
|--------|---------|------|-----|
| Users | Patients + doctors + admins | — | Three user types with very different access levels |
| Primary database | Patient records, appointments | PostgreSQL with field-level encryption | Relational (patient → appointments → prescriptions). HIPAA requires encryption of Protected Health Information (PHI) at field level, not just disk-level |
| Video calls | Real-time doctor-patient consultation | WebRTC for peer-to-peer, or Twilio Video for managed | WebRTC is free but requires TURN servers for NAT traversal. Twilio Video is managed but costs per minute. Both encrypt in transit |
| File storage | Medical images (X-rays, scans), documents | S3 with server-side encryption (SSE-KMS) | HIPAA requires encryption at rest with customer-managed keys. S3 SSE-KMS encrypts each object with a unique key managed by AWS KMS |
| Auth | Patient login + doctor login + admin | OAuth2 + OIDC + MFA mandatory for doctors | HIPAA requires multi-factor authentication for accessing PHI. Patients get standard auth, doctors get MFA-enforced auth |
| Audit | Every access to PHI must be logged | Immutable audit log (append-only, separate storage) | HIPAA requires audit trails showing who accessed what patient data, when, and why. Must be tamper-proof |
| Compliance | HIPAA (US) or equivalent | Field-level encryption + audit log + access control + BAA with cloud provider | A Business Associate Agreement (BAA) with your cloud provider (AWS, Azure, GCP) is legally required. It confirms they meet HIPAA requirements for storing PHI |
| Deploy | Zero downtime | Rolling updates, multi-AZ database | Patient-facing system can't have scheduled maintenance windows |

**Questions still to define:**
- [[#Entities\|What entities?]] → Patient, Doctor, Appointment, MedicalRecord, Prescription, Invoice, AuditEntry
- [[#Data Retention\|How long keep records?]] → medical records: 7-10 years (varies by jurisdiction). Audit logs: 6 years (HIPAA)
- [[#Disaster Recovery\|Recovery strategy?]] → RPO near-zero (no lost medical data ever), RTO minutes. Multi-AZ mandatory

---

#### EdTech Learning Management System
*Online courses, quizzes, student progress, certificates*

| Aspect | Default | Tool | Why |
|--------|---------|------|-----|
| Users | Students (many) + instructors (few) + admins | — | Students are read-heavy (watch videos, take quizzes). Instructors write content. Very different access patterns |
| Primary database | Users, courses, enrollment, grades | PostgreSQL | Relational: students enroll in courses, courses have modules, modules have quizzes, quizzes have grades. Foreign keys prevent orphaned records |
| Content storage | Course content (text, metadata, quiz definitions) | MongoDB | Course content varies per type — text lessons have different fields than quizzes, which differ from assignments. Flexible schema fits well |
| Video storage | Lecture videos, recorded sessions | S3 + CloudFront CDN + transcoding workers | Videos are large (GBs), stored in S3, transcoded to multiple resolutions (480p, 720p, 1080p) via workers (KEDA-scaled), served via CDN for global low-latency playback |
| Events | Student completed lesson → update progress, check certificate eligibility | Apache Kafka | Multiple consumers: progress tracker, certificate generator, analytics, notification service |
| Real-time | Quiz timer, live classroom features | WebSocket for live sessions, REST for standard browsing | WebSocket only for live interactive features (live quiz, virtual classroom). Standard course browsing is plain REST |
| Auth | Student login, instructor panel, admin | OAuth2 + OIDC, RBAC (student, instructor, admin) | Students can only see their own progress. Instructors see their course analytics. Admins see everything |
| Cache | Course catalog, popular lessons | Redis (cache-aside) + CDN for videos | Course catalog is read-heavy (thousands of students browse, few instructors update). Cache catalog in Redis, serve videos from CDN |

**Questions still to define:**
- [[#Entities\|What entities?]] → Student, Instructor, Course, Module, Lesson, Quiz, Question, Grade, Certificate, Enrollment
- [[#Search Needs\|Course search?]] → Elasticsearch for full-text course search (search by title, description, topic, instructor)
- [[#Performance Requirements\|Video latency?]] → CDN handles this. Focus on adaptive bitrate streaming (HLS) so quality adjusts to user's connection speed
- [[#Compliance Requirements\|Student data privacy?]] → FERPA (US) or GDPR if EU students. Requires consent, access controls, data portability

---

#### Social Media Content Platform
*User posts, feeds, followers, likes, comments, media sharing*

| Aspect | Default | Tool | Why |
|--------|---------|------|-----|
| Users | End users (millions potentially), content creators, admins | — | Very read-heavy (scrolling feed) with write spikes (posting, liking) |
| Primary database | Users, posts, follows, likes | PostgreSQL (users, relationships) + MongoDB (posts, comments) | User relationships (follower graph) are relational. Posts are document-shaped (varying content types, embedded media refs, flexible metadata) |
| Feed generation | Home feed = posts from people you follow | Fan-out-on-write: when User A posts, pre-compute the feed for all followers by writing to their feed cache | Why fan-out-on-write: reading the feed is 1000x more frequent than posting. Pre-computing means the feed read is a simple Redis sorted set lookup — sub-millisecond. Trade-off: celebrities with millions of followers create massive fan-out — use fan-out-on-read for users with >100K followers |
| Feed cache | Pre-computed per-user feed | Redis sorted sets (score = timestamp) | Why Redis sorted set: chronological ordering with O(log N) insert, O(1) range read. Each user's feed is a sorted set of post IDs, scored by publish time. Trim to last 1000 posts |
| Media storage | Images, videos uploaded by users | S3 + CloudFront CDN + resize/transcode workers | Users upload images/videos → S3 → workers resize to multiple sizes (thumbnail, medium, full) → CDN serves globally. Never serve original full-resolution — wasteful bandwidth |
| Events | Post created → fan-out to followers, update analytics, index for search | Apache Kafka | 3+ consumers per event, need ordering per user (partition by user_id), need replay for feed rebuilds |
| Search | Search posts, users, hashtags | Elasticsearch synced via Kafka | Full-text search with relevance, hashtag aggregation, user search with fuzzy matching |
| Real-time | New post notification, like count live update | SSE or WebSocket for notifications, polling acceptable for feed refresh | Full live feed update via WebSocket is expensive at scale. Most social apps use pull-to-refresh (polling) for the feed and push only for notifications |

**Questions still to define:**
- [[#Entities\|What entities?]] → User, Post, Comment, Like, Follow, Feed, Media, Hashtag, Notification
- [[#Daily Active Users\|Scale?]] → feed generation is the hardest problem. 1M DAU × 200 followers average = 200M feed entries per day
- [[#Duplicate Handling\|Double-like prevention?]] → unique constraint on (user_id, post_id) in likes table. Idempotent by design
- [[#Performance Requirements\|Feed load time?]] → < 200ms for home feed. Pre-computed in Redis, not queried at read time

---

#### Logistics Supply Chain
*Shipment tracking, fleet management, warehouse operations, delivery scheduling*

| Aspect | Default | Tool | Why |
|--------|---------|------|-----|
| Users | Warehouse operators + drivers + dispatchers + customers (tracking) | — | Multiple user types with different devices (desktop for dispatchers, mobile for drivers, web for customers) |
| Primary database | Shipments, orders, routes, warehouses | PostgreSQL | Relational: shipment has items, assigned to route, route has stops, stops have timestamps. ACID for inventory counts |
| Location tracking | GPS positions from vehicles/drivers | TimescaleDB (time-series) + Redis (latest position) | TimescaleDB for historical route replay (where was truck X at 3pm?). Redis for live dashboard (where are all trucks RIGHT NOW?) |
| Events | Shipment scanned → update status, notify customer, trigger next step | Apache Kafka | Chain of custody: item picked → packed → shipped → in transit → delivered. Each scan is an event consumed by status tracker, customer notification, billing, analytics |
| Real-time | Live fleet map, delivery ETA updates | WebSocket + Redis Pub/Sub | Dispatchers see live fleet positions on a map. Customers see live ETA for their delivery. Both need sub-second updates |
| Mobile | Driver app (scan barcodes, capture signatures, GPS) | React Native or Flutter | One codebase for iOS + Android. Drivers need offline capability — app must work when cellular is poor and sync when back online |
| Offline sync | Driver app works without internet | Local SQLite on device, sync queue to server | Why: warehouses and delivery routes often have poor connectivity. App stores scans/signatures locally, syncs when connection is available. Conflict resolution needed (last-write-wins or manual merge) |
| Auth | Driver login (mobile), dispatcher (web), customer (tracking page) | OAuth2 + JWT. Customer tracking: no auth (public link with tracking ID) | Drivers get full auth. Customers just need a tracking link — no account required |

**Questions still to define:**
- [[#Entities\|What entities?]] → Shipment, Package, Route, Stop, Vehicle, Driver, Warehouse, Scan, DeliveryProof, Customer
- [[#Data Retention\|How long keep tracking data?]] → chain of custody records: years (legal). GPS history: months. Compress/archive older data
- [[#i18n Scope\|Multi-timezone?]] → critical. Shipments cross timezones. Store all timestamps in UTC, display in local time per user

---

#### Banking Fintech
*Accounts, transfers, payments, transaction history, compliance*

| Aspect | Default | Tool | Why |
|--------|---------|------|-----|
| Primary database | Accounts, balances, transactions | PostgreSQL with SERIALIZABLE isolation for balance operations | Why serializable: two concurrent transfers from the same account must not overdraw. Serializable isolation prevents race conditions at the database level. No eventual consistency for money |
| Ledger | Double-entry bookkeeping | Append-only transaction log (event sourcing) | Every money movement is recorded as two entries: debit from Account A, credit to Account B. Append-only — never update or delete a transaction. Why: full audit trail, reconciliation, regulatory requirement |
| Events | Transfer completed → update balances, send receipt, report to compliance | Apache Kafka with exactly-once semantics (transactions) | Financial events must not be lost or duplicated. Kafka transactions guarantee exactly-once processing. Each consumer processes within a Kafka transaction |
| Idempotency | Every transfer has a unique transaction ID | Idempotency key + dedup table (mandatory, not optional) | Why mandatory: if a transfer request is retried (network timeout), the system must not transfer the money twice. Every write operation must check the dedup table first |
| Auth | Customer login + banker login + compliance officer | OAuth2 + OIDC + MFA mandatory + session timeout (5 min idle) | MFA is non-negotiable for financial systems. Short session timeouts prevent unauthorized access from unattended terminals |
| Encryption | Encryption at rest + in transit + field-level for PII | TLS 1.3 + AES-256 (KMS-managed) + field encryption for SSN, account numbers | Regulatory requirement. Even database administrators should not see plaintext PII. Field-level encryption means the value is encrypted in the database column itself |
| Compliance | PCI DSS + SOC 2 + local banking regulations | Immutable audit log + separate compliance reporting database | Every access to financial data is logged. Compliance officers have read-only access to a separate reporting database (not production). Regular external audits |
| Deploy | Blue-green with extensive pre-deploy testing | Blue-green deployment + automated regression tests + canary for non-critical | Why blue-green: instant rollback if anything is wrong. Financial systems cannot tolerate a broken deploy for even 5 minutes. Run the full regression test suite against Green before switching |

**Questions still to define:**
- [[#Entities\|What entities?]] → Customer, Account, Transaction, Transfer, Card, Statement, AuditEntry, ComplianceReport
- [[#Disaster Recovery\|Recovery strategy?]] → RPO zero (no lost transactions, ever). Synchronous replication to standby. Multi-region for DR
- [[#Performance Requirements\|Transfer latency?]] → < 2 seconds for domestic transfers. Balance query < 100ms (cached in Redis, invalidated on every transaction)
- [[#Multi-Tenancy\|Multi-tenant?]] → rarely. Banks are single-tenant. Fintech platforms serving multiple businesses → database-per-tenant for regulatory isolation

---

#### Media Streaming
*Video on demand, music streaming, live streaming, content delivery*

| Aspect | Default | Tool | Why |
|--------|---------|------|-----|
| Content storage | Video/audio files (raw masters + encoded versions) | S3 (or equivalent object storage) | Videos are large (GBs per file). S3 is designed for this — durable, cheap, integrates with CDN and transcoding |
| Transcoding | Convert raw video to multiple formats/resolutions | Worker pods auto-scaled by KEDA on queue depth | When a creator uploads a video, workers transcode it to 480p/720p/1080p/4K in H.264/H.265. This is CPU-intensive — KEDA scales workers based on the transcoding queue depth. Scale to zero when no uploads are pending |
| Delivery | Stream video to users globally | CloudFront CDN + HLS (HTTP Live Streaming) | Why CDN: video is bandwidth-heavy, edge caching is critical. HLS splits the video into small chunks (2-10 seconds each) and an index file (m3u8). The player downloads chunks sequentially, enabling adaptive bitrate — quality adjusts to the user's connection speed |
| Metadata database | Users, content library, playlists, watch history | PostgreSQL (users, subscriptions) + MongoDB (content metadata) | User subscriptions are relational (user → plan → payment). Content metadata is document-shaped (movies have different fields than TV shows, which differ from music albums) |
| Recommendations | "Because you watched X, try Y" | Kafka (user events) → batch ML pipeline (nightly) → Redis (serving cache) | Recommendations don't need real-time retraining. A nightly batch job processes viewing history and generates recommendations. Serve pre-computed recs from Redis (sub-millisecond). If the ML service is down, show "Popular" as fallback (graceful degradation) |
| View counting | Track plays, watch duration, skip points | Kafka (high-throughput event ingestion) → batch aggregation → analytics DB | Why Kafka: millions of concurrent viewers × events every few seconds = massive write volume. Kafka buffers events, batch workers aggregate (count plays per hour, not per event) and write to the analytics database |
| Real-time | Live streaming (sports, events, concerts) | RTMP ingest → transcoding → HLS via CDN | Creator streams via RTMP (Real-Time Messaging Protocol) to your ingest server. Server transcodes to HLS in real-time and pushes to CDN. Viewers watch via CDN with 5-30 second latency. For ultra-low latency (< 3s), use WebRTC instead of HLS |
| Auth | Free tier + premium subscription | OAuth2 + JWT with subscription tier in claims | JWT contains `{ "tier": "premium" }`. Content service checks the tier before serving premium content. Payment handled by Stripe — you store the subscription status, not card data |
| Cost | CDN bandwidth is the primary cost | CloudFront: $0.085/GB. 1M users × 1 hour/day × 1 GB/hour = 1 PB/month = ~$85K/month | Bandwidth dominates all other costs. Optimize: adaptive bitrate (lower quality on mobile saves 60% bandwidth), edge caching (popular content served from cache, not origin), and compression (H.265 is 50% smaller than H.264 at same quality) |

**Questions still to define:**
- [[#Entities\|What entities?]] → User, Subscription, Content, Episode, Playlist, WatchHistory, ViewEvent, Creator, Encoding
- [[#Performance Requirements\|Start-to-play latency?]] → < 2 seconds for VOD (first chunk loads from CDN). < 10 seconds for live
- [[#Disaster Recovery\|CDN failover?]] → multi-CDN strategy (CloudFront primary, Akamai fallback). Content is replicated across both
- [[#Daily Active Users\|Scale?]] → 100K concurrent viewers × 2 Mbps average = 200 Gbps of CDN bandwidth. CDN handles this, not your servers

---



---


### Phase 1 — Shape the System

**Q1: "Can you describe the main user flow in 2-3 sentences?"**
→ The answer IS your diagram skeleton. Each verb = an API call. Each noun = a service or entity.

```
Example answer: "Users create tickets, agents get assigned, customers get notified"
Draw:          [User] → [Ticket Svc] → [Assignment Svc] → [Notification Svc]
```

**Q2: "Is this a new system or does it replace / extend something existing?"**

| Answer | Draw |
|--------|------|
| New (greenfield) | `[Client] → [API] → [Service] → [DB]` — clean start |
| Extends existing | `[Client] → [Proxy] → [Existing System] + [New Service]` — strangler fig |
| Replaces old | `[Client] → [Proxy] ──→ [Old] (shrinking) ──→ [New] (growing)` |

**Q3: "How many distinct types of users are there?"**

| Answer | Draw |
|--------|------|
| One type (end users) | `[Client] → [API]` — single API surface |
| End users + admins | `[Client] → [API]` + `[Admin] → [Admin API]` — separate surface, elevated auth |
| End users + API consumers (machines) | `[Client] → [GraphQL/REST]` + `[Partner] → [REST + API key]` — separate auth |
| Internal services only | `[Service A] → [gRPC] → [Service B]` — no public API, internal only |

**Q4: "Is this multi-tenant? Do different customers share the system?"**

| Answer | Draw |
|--------|------|
| No, single tenant | No change — standard architecture |
| Yes, shared system | Add `[API Gateway: tenant routing]` + `tenant_id` on every DB query |
| Yes, strict isolation needed | Add `[Tenant DB pool]` or separate namespace per tenant in K8s |

---

### Phase 2 — Choose the Data Layer

**Q5: "What are the main entities? How do they relate to each other?"**
→ Write them on the board. Draw arrows for relationships.

```
Example: [User] 1──* [Ticket] *──1 [Agent] 1──* [Comment]
This IS your data model. Each cluster of tightly-related entities may become a service.
```

**Q6: "Does the data have a fixed structure or does it vary per record?"**

| Answer | Draw |
|--------|------|
| Fixed structure, clear relations | `[Relational DB]` (PostgreSQL, MySQL, MS SQL) — ACID, joins, constraints |
| Varies per record, nested objects | `[Document DB]` (MongoDB, DynamoDB, Firestore) — flexible schema |
| Key-value lookups, counters | `[Key-Value Store]` (Redis, DynamoDB, Memcached) — fast, simple |
| Time-series (IoT, metrics, logs) | `[Time-Series DB]` (TimescaleDB, InfluxDB, Prometheus) — optimized for append |
| Graph relationships (social, recommendations) | `[Graph DB]` (Neo4j, Neptune) — relationship-first queries |
| Mix of types | Polyglot: use the right store for each data type |

**Q7: "Is this read-heavy, write-heavy, or balanced?"**

| Answer | Draw |
|--------|------|
| Read-heavy (>10:1) | Add `[Redis]` between API and database using cache-aside pattern — because Redis serves cached reads in <1ms, removing load from the database. Choose Redis over Memcached because Redis supports richer data structures (hashes, sorted sets, streams) and persistence |
| Very read-heavy (>100:1) | Add `[Redis]` + `[Database Read Replicas]` + `[CDN]` for static content — because at this ratio, even Redis alone isn't enough; replicas handle overflow reads and CDN offloads static assets entirely |
| Write-heavy | Add `[Apache Kafka]` or `[Amazon SQS]` as a write buffer before the database — because the queue absorbs bursts and workers write at a pace the database can handle. Consider database sharding if single-node write throughput is the limit |
| Both heavy (reads and writes) | Add `[CQRS pattern]`: separate `[Write Path → Primary Database]` and `[Read Path → Denormalized Read Store / Redis]` — because optimizing one model for both reads and writes is a losing trade-off; CQRS lets you optimize each independently |
| Balanced / low volume | `[API] → [Database]` directly — no cache, no queue, don't add complexity you don't need yet |

**Q8: "How much data? Thousands, millions, or billions of records?"**
`→ NEXT: Q9` | `DRAWS: partitioning strategy or specialized DB`

| Answer | Draw |
|--------|------|
| Thousands | Single database instance, no special handling needed |
| Millions | Single database + proper indexes — mention composite indexes, covering indexes, and query plan analysis |
| Hundreds of millions | Database partitioning (by date, tenant_id, or hash key) — because single-table scans become too slow. PostgreSQL native partitioning or application-level sharding |
| Billions | Purpose-built store: Apache Cassandra (linear write scaling, multi-datacenter), Amazon DynamoDB (fully managed, auto-scaling), or TimescaleDB (if time-series) — because traditional relational databases can't handle this volume efficiently |

**Q9: "Do we need full-text search, autocomplete, or filtering beyond simple queries?"**
`→ NEXT: Q10` | `If yes → DRAWS: search engine box + sync arrow from main DB`

| Answer | Draw |
|--------|------|
| No, simple filters work | SQL WHERE + indexes — no extra component |
| Yes, full-text with relevance | Add `[Search Engine]` (Elasticsearch, OpenSearch, Typesense, Meilisearch) ← synced via events/CDC |
| Just autocomplete | Add `[Cache]` with prefix matching or trie — simpler than full search engine |
| Complex faceted search + analytics | Add `[Elasticsearch/OpenSearch]` — aggregations, facets, nested filtering |

**Q10: "How long do we keep the data?"**
`→ NEXT: Q11 (communication)` | `If compliance → DRAWS: cold storage + archival pipeline`

| Answer | Draw |
|--------|------|
| Days/weeks | TTL on records, background cleanup job |
| Months/years | Standard DB storage, maybe partition by date |
| Years (compliance) | Add `[Cold Storage / S3 Glacier]` for archival |
| Forever, need full history | Consider event sourcing or append-only audit log |

---

### Phase 3 — Choose the Communication Style

**Q11: "When a user does something, do they need the result immediately?"**
`→ NEXT: Q12` | `If async path chosen → Q28 (duplicates) and Q29 (async failure) become MANDATORY later` | `DRAWS: sync path, async path with queue + workers, or both`

| Answer | Draw |
|--------|------|
| Yes, always | `[Client] → [API] → [Database] → response` — synchronous request/response. Use REST or GraphQL for the API |
| Some things can be background | `[API] → response (202 Accepted)` + `[API] → [Message Queue (Kafka, SQS, or RabbitMQ)] → [Worker Service] → [Database]` — the user gets a fast acknowledgment, heavy processing happens async |
| Most things are background | `[API] → [Message Queue]` for most operations — thin synchronous API accepts and enqueues, worker services do the real processing. Good for email sending, report generation, data processing |

**Q12: "When something happens, do other parts of the system need to react?"**
`→ NEXT: Q13` | `If yes → Q15 is partially answered (event infra handles cross-service)` | `If yes → Q13 can reuse same event infra for live updates` | `If Kafka chosen → Q28 (duplicates) MANDATORY` | `DRAWS: event bus + consumer arrows`

| Answer | Draw |
|--------|------|
| No, one service handles it | `[API] → [Service] → [Database]` — no events needed, keep it simple |
| Yes, 1-2 other things react | `[Service] → [Event] → [Consumer A] + [Consumer B]` — use RabbitMQ (routing keys, simple setup) or Amazon SNS+SQS (managed, zero ops). Choose RabbitMQ when you need flexible routing patterns, choose SNS+SQS when you want zero operational burden |
| Yes, many things react (3+) | `[Service] → [Apache Kafka] → [Consumer Group A] + [B] + [C] + [D]` — use Kafka because each consumer group reads independently at its own pace, and Kafka retains messages for replay. Choose Kafka over RabbitMQ when you have 3+ consumers or need replay capability |
| Yes, and consumers need to replay/reprocess | `[Apache Kafka]` or `[Amazon Kinesis]` — durable append-only log, consumers can rewind to any offset and reprocess. Essential for rebuilding search indexes, fixing data, or adding new consumers retroactively |

**Q13: "Does the UI need live updates, or does the user refresh/poll?"**
`→ NEXT: Q14` | `If Q12 added Kafka/RabbitMQ → reuse that event stream to feed WebSocket/SSE here` | `DRAWS: WebSocket server, SSE endpoint, or nothing (poll)`

| Answer | Draw |
|--------|------|
| User refreshes the page | `[Client] → [REST or GraphQL API]` — standard request/response, simplest approach |
| Live updates needed (bidirectional, like chat) | Add `[WebSocket Server]` ← fed by Redis Pub/Sub or Kafka — because WebSocket gives full-duplex communication with low latency. Use Redis Pub/Sub to fan out events to all connected WebSocket instances |
| Live updates needed (server → client only, like dashboards) | Add `[Server-Sent Events (SSE) endpoint]` — simpler than WebSocket because it's just HTTP, has built-in auto-reconnect, and works through all proxies. Choose SSE over WebSocket when communication is one-directional |
| Near-real-time is OK (5-30 second delay acceptable) | Short polling or long polling — simplest to implement, no persistent connections needed, works everywhere. Choose this when "almost real-time" is good enough |

**Q14: "Does this system talk to external systems?"**
`→ NEXT: Q15` | `If outbound → Q27 (downstream failure) becomes critical` | `DRAWS: integration layer, circuit breaker, webhook endpoint`

| Answer | Draw |
|--------|------|
| No | No external adapters needed |
| We call them (outbound) | Add `[HTTP Client]` with `[Circuit Breaker + Retry with exponential backoff]` — use Polly (.NET), Resilience4j (Java), or tenacity (Python). Circuit breaker prevents your system from hanging when their API is down |
| They call us (inbound) | Add `[Webhook Endpoint]` — verify payload signature (HMAC-SHA256) to confirm sender identity, use an idempotency key to handle duplicate deliveries. Respond 200 quickly, process the payload asynchronously via a queue |
| Both directions | Add `[Integration Layer]` — inbound: webhook receiver + signature verification + queue for processing. Outbound: HTTP client + circuit breaker + retry + Dead Letter Queue for persistent failures |

**Q15: "Can an operation span multiple services? What if one fails halfway?"**
`→ NEXT: Q16 (API layer)` | `SKIP if Q12 said "no events needed" AND only one service` | `If saga chosen → Q28 (idempotency) MANDATORY` | `DRAWS: saga flow, outbox table, or consistency arrows`

| Answer | Draw |
|--------|------|
| No, each operation is within one service | No distributed transaction needed — use a normal database transaction |
| Yes, and we must roll back on failure | `[Saga Pattern]`: each service executes a local transaction and publishes an event; if a downstream step fails, previous services execute compensating actions (e.g., refund payment). Implement as choreography (services react to events independently — simpler) or orchestration (a central Saga coordinator tells each service what to do — easier to monitor). Use a message broker (Kafka, RabbitMQ) to deliver the events between steps |
| Yes, but brief inconsistency is OK | `[Eventual Consistency]`: Service A writes and publishes an event, Service B consumes and updates its own data later — no saga overhead needed. The system is temporarily inconsistent for milliseconds to seconds. Implement by publishing domain events to Kafka or RabbitMQ after each local write |
| Yes, and we can't afford to lose the event | Add `[Transactional Outbox]`: write the event to an outbox table in the same database transaction as the data change, then a separate process (poller or Debezium CDC) publishes from the outbox to the message broker. This guarantees the event is published if and only if the data was committed |
| Yes, and it involves money or safety | Use a synchronous call with an idempotency key — the caller retries with the same key until it succeeds, and the receiver deduplicates. No eventual consistency; the caller blocks until confirmed |

---

### Phase 4 — Choose the API Layer

**Q16: "How many backend services will there be?"**
`→ NEXT: Q17` | `If 1 service → SKIP Q18 (no internal comms), Q33 is answered (monolith), Q35 is answered` | `If 10+ → Q33 is answered (microservices)` | `DRAWS: gateway or load balancer box`

| Answer | Draw |
|--------|------|
| One (monolith or modular monolith) | `[Client] → [API]` — no gateway needed, route directly. Implement as a single deployable with clear internal module boundaries so you can split later |
| 2-5 services | `[Client] → [Load Balancer (Nginx, HAProxy, or cloud ALB)] → [Service A / B / C]` — the load balancer routes by URL path (e.g., `/users` → User Service, `/orders` → Order Service). Implement with path-based routing rules |
| Many (10+) | `[Client] → [API Gateway (Kong, AWS API Gateway, Envoy, or a custom GraphQL gateway)]` — centralize authentication, rate limiting, request routing, and protocol translation in one place. Without a gateway, every service reimplements auth and rate limiting |

**Q17: "Do different clients need different data from the same endpoint?"**
`→ NEXT: Q18` | `DRAWS: REST, GraphQL, or BFF label on the API box`

| Answer | Draw |
|--------|------|
| No, same shape for everyone | `[REST API]` — fixed endpoints with JSON responses. Implement with OpenAPI/Swagger for documentation. Choose REST when the API surface is simple and cacheable (HTTP GET + ETag) |
| Yes, web needs more, mobile needs less | `[GraphQL API]` — client specifies exactly which fields it needs in each query, eliminating over-fetching. Implement with Apollo Server (Node.js), HotChocolate (.NET), or Strawberry (Python). Alternatively, use `[Backend-for-Frontend (BFF)]` — one dedicated API per client type (web BFF, mobile BFF), each returning only what that client needs |

**Q18: "Do services need to call each other internally?"**
`→ NEXT: Q19 (scaling)` | `SKIP if Q16 said 1 service` | `If Q12 already added async events → this only adds the sync arrows` | `DRAWS: gRPC arrows between services`

| Answer | Draw |
|--------|------|
| No, each service is independent | No internal arrows between services — each service has its own database and API |
| Yes, synchronously (need immediate response) | `[Service A] → [gRPC] → [Service B]` — choose gRPC because it uses binary Protocol Buffers (10x smaller than JSON), HTTP/2 multiplexing, and generates typed client code from .proto files so a field change causes a compile error, not a runtime crash. Use REST between services only if the team is unfamiliar with gRPC |
| Yes, asynchronously (fire and forget) | `[Service A] → [Message Broker] → [Service B]` — already covered if Q12 said yes. The same Kafka/RabbitMQ infrastructure handles both cross-service events and async processing |
| Both synchronous and asynchronous | Draw both arrows: solid line for synchronous gRPC calls (when caller needs data back), dashed line for asynchronous events (when caller doesn't wait). Example: Service A calls Service B via gRPC to get user profile (sync), and publishes "OrderCreated" event to Kafka for Service C to process later (async) |

---

### Phase 5 — Add Scaling & Caching

**Q19: "How many concurrent users / requests per second?"**
`→ NEXT: Q20` | `SKIP if Q7 already gave clear volume numbers and you drew scaling components` | `DRAWS: LB, auto-scaler, sharding, CDN, rate limiter`

| Answer | Draw |
|--------|------|
| <100 requests per second | Single instance + single database. No special scaling needed. Deploy as one container behind a simple reverse proxy (Nginx or cloud load balancer) |
| 100-1,000 requests per second | Add `[Load Balancer]` (Nginx, AWS ALB, or Kubernetes Ingress) distributing to 2-5 stateless API instances. Add `[Redis]` as a read-through cache for frequently accessed data. Implement the Horizontal Scaling pattern — services must be stateless (no in-memory sessions) |
| 1,000-10,000 requests per second | Add `[Auto-scaling]` (Kubernetes HPA scaling on CPU at 75% target, or AWS Auto Scaling Groups). Add `[Redis]` for caching + `[Database Read Replicas]` for read distribution. Implement the Cache-Aside pattern and the Database Replication pattern |
| 10,000+ requests per second | Add `[CDN]` (CloudFront, CloudFlare) for static content + `[Database Sharding]` (partition by tenant or user ID) + `[Kafka with worker consumers]` for async processing + `[Rate Limiter]` (Redis-based token bucket) to protect backends. Implement the Sharding pattern, the Queue-Based Load Leveling pattern, and the Throttling pattern |
| 100,000+ requests per second | Multi-region deployment + edge compute (CloudFlare Workers, Lambda@Edge) + aggressive caching at every layer + database sharding + async processing everywhere. Implement the Multi-Region Active-Active pattern with GeoDNS routing |

**Q20: "Is there static content (images, files, JS/CSS)?"**

| Answer | Draw |
|--------|------|
| No, all dynamic | No CDN needed for content |
| Yes | Add `[CDN]` (CloudFront, CloudFlare, Akamai) in front. `[Object Storage]` (S3, GCS, Blob) behind. Versioned URLs |

**Q21: "Do users upload files?"**

| Answer | Draw |
|--------|------|
| No | Skip |
| Yes, small files (<10MB) | `[Client] → [API] → [Object Storage]` — proxy through API is OK |
| Yes, large files | `[Client] → [API: get pre-signed URL] → [Direct upload to Object Storage]` → `[Event] → [Workers: scan, thumbnail, metadata]` |

**Q22: "Does traffic spike or is it steady?"**
`→ NEXT: Q23 (security)` | `SKIP if Q7 already added queue for write-heavy (queue handles spikes)` | `DRAWS: auto-scaler, queue buffer`

| Answer | Draw |
|--------|------|
| Steady | Fixed instance count, basic auto-scaling |
| Spiky (time of day) | `[Auto-scaler]` with CPU/memory target — scale up/down |
| Very spiky (unpredictable) | Add `[Queue]` to buffer spikes + `[Event-driven scaler]` on queue depth |

---

### Phase 6 — Add Security

**Q23: "How do users authenticate?"**
`→ NEXT: Q24` | `Use Q3's user types → each type may need different auth here` | `DRAWS: identity provider, JWT flow, API key validation`

| Answer | Draw |
|--------|------|
| Username + password (web app) | `[Identity Provider]` → `[JWT/Session tokens]` → `[API validates]` |
| OAuth / social login (Google, GitHub) | `[OAuth2 + OIDC Provider]` → Authorization Code + PKCE → `[JWT]` |
| API keys (machine-to-machine) | `[API Gateway]` validates key, rate limits per key |
| Internal services only | `[mTLS]` between services, or `[Service Account / Pod Identity]` |
| No auth needed (public API) | `[Rate Limiter]` at minimum — still need abuse protection |

**Q24: "Are there different permission levels?"**
`→ NEXT: Q25` | `If Q4 said multi-tenant → "tenant-scoped" answer is mandatory here` | `DRAWS: RBAC layer, policy engine, or tenant filter`

| Answer | Draw |
|--------|------|
| No, all users can do everything | Simple auth check, no authorization layer |
| Yes, roles (admin, user, viewer) | Add `[RBAC]` — roles in token claims, checked at each service |
| Yes, resource-level (own data only) | Add `[Resource ownership check]` — every query checks user owns the resource |
| Yes, tenant-scoped | Add `tenant_id` in token. Every DB query filtered. Every service checks |
| Complex / policy-based | Add `[Policy Engine]` (OPA, Casbin, Cedar) — externalized authorization rules |

**Q25: "Where do secrets (API keys, DB passwords) live?"**
`→ NEXT: Q26 (resilience)` | `DRAWS: secrets manager box`

| Answer | Draw |
|--------|------|
| In code / config files | **Fix this** — move to a secrets manager |
| In environment variables | Better, but visible in process listings. Move to mounted files |
| In a secrets manager | `[Secrets Manager]` (Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager) → injected at runtime |

---

### Phase 7 — Add Resilience

**Q26: "What if the database is down?"**
`→ NEXT: Q27` | `SKIP if Q7 already added Redis cache (cache IS the read fallback)` | `DRAWS: fallback paths`

| Answer | Draw |
|--------|------|
| System can be down too | No special handling needed |
| Must still serve reads | Implement the **Graceful Degradation pattern**: add `[Redis]` as a cache fallback — when the database is unreachable, return the last cached version. Implement by wrapping database calls in a try-catch that falls back to the cache on failure |
| Must still accept writes | Implement the **Queue-Based Load Leveling pattern**: add `[Apache Kafka or Amazon SQS]` — the API writes to the queue and returns 202 Accepted. A worker drains the queue when the database recovers. No writes lost |
| Must never go down | Implement the **Active-Passive Failover pattern**: use a multi-availability-zone database (Amazon RDS Multi-AZ, or PostgreSQL + Patroni for automatic failover) + Redis cache for read fallback + message queue for write buffering |

**Q27: "What if a downstream service is slow or down?"**

| Answer | Draw |
|--------|------|
| Show error to user | Add a `[Timeout]` (2-5 seconds) on every external call — bare minimum resilience. Implement with HTTP client timeout configuration. Without this, one slow service holds threads indefinitely and your service becomes unresponsive too |
| Don't let it cascade | Implement the **Circuit Breaker pattern**: after N consecutive failures (e.g., 5 in 30 seconds), the circuit opens and all calls fail immediately for a cooldown period (e.g., 60 seconds), then a few test requests check if the service recovered. Implement with Polly (.NET), Resilience4j (Java), or a service mesh sidecar (Istio, Linkerd) |
| Show degraded data instead | Implement the **Graceful Degradation pattern**: when the circuit breaker is open, return a cached or default response instead of an error. Example: if the recommendation service is down, show popular items instead of personalized ones. Implement with a fallback handler in the circuit breaker configuration |
| All of the above (best practice) | Implement the full **Resilience Stack**: `[Timeout]` on every call + `[Retry with exponential backoff + jitter]` (3 retries at 1 second, 2 seconds, 4 seconds + random offset to prevent thundering herd) + `[Circuit Breaker]` (open after 5 failures) + `[Fallback response]`. Apply this as cross-cutting middleware to every outbound HTTP and gRPC call |

**Q28: "Can the same request arrive twice?"**
`→ NEXT: Q29` | `MANDATORY if Q11 chose async or Q12 chose Kafka (at-least-once = duplicates are inevitable)` | `SKIP if system is fully synchronous with no queues` | `DRAWS: idempotency key or dedup table`

| Answer | Draw |
|--------|------|
| Doesn't matter (read-only operations) | No special handling — reads are naturally idempotent |
| Yes, and duplicates are dangerous (payments, orders) | Implement the **Idempotency Key pattern**: the client generates a UUID and sends it with each request in an `Idempotency-Key` header. The server stores processed keys in a database table with a unique constraint and returns the cached result for duplicate keys. If the key already exists, return the previous response without re-executing |
| Yes, for async message consumers | Implement **Idempotent Consumers**: store processed message IDs in a deduplication table — before processing, check if the message ID exists; if yes, skip it. Alternatively, design operations to be naturally idempotent: use SET (always same result) instead of INCREMENT (accumulates), use UPSERT instead of INSERT |

**Q29: "What if async processing fails?"**
`→ NEXT: Q30 (observability)` | `MANDATORY if Q11 chose async or Q12 added event consumers` | `SKIP if system is fully synchronous` | `DRAWS: DLQ box, retry arrows`

| Answer | Draw |
|--------|------|
| Best effort, retries are enough | Implement `[Retry with exponential backoff]` — 3 attempts with 1 second, 2 second, 4 second delays plus random jitter to prevent all consumers retrying at the same time |
| Must not lose the message | Implement the **Dead Letter Queue pattern**: after N failed retries, move the message to a separate Dead Letter Queue (a dedicated Kafka topic, an SQS Dead Letter Queue, or a RabbitMQ dead-letter exchange). Build a dashboard to inspect failed messages and replay them after fixing the issue. Set up an alert when DLQ depth is greater than zero |
| Must complete eventually (critical business operation) | Implement the **Transactional Outbox pattern** for guaranteed event publishing (see Q15) combined with the **Dead Letter Queue pattern** for consumer failures. Add monitoring alerts on DLQ depth and outbox table growth. The combination guarantees the event is published and will eventually be processed successfully |

---

### Phase 8 — Add Observability & Operations

**Q30: "How do we know if the system is healthy?"**
→ Always draw this side-layer:

```
All Services → [OTel SDK] → [Collector]
                                  |
                    ┌─────────────┼─────────────┐
                    ↓             ↓             ↓
              [Traces]      [Metrics]      [Logs]
              (Tempo)       (Prometheus)   (Loki)
                    └─────────────┼─────────────┘
                                  ↓
                            [Grafana] → [Alerts]
```

**Q31: "How does code get to production?"**
→ Always draw the deploy pipeline:

```
[Git Push] → [Build + Test + Security Scan] → [Quality Gate]
    → [Container Registry] → [Dev] → [Staging] → [Prod]
```

**Q32: "How do we deploy without downtime?"**

| Answer | Draw |
|--------|------|
| Downtime is OK | Simple deploy — stop old, start new. Acceptable for internal tools or dev environments |
| Zero downtime required | Implement the **Rolling Update pattern**: deploy new version one instance at a time with `maxUnavailable: 0` (never remove an old instance before the new one is healthy). Use readiness probes to verify the new instance can serve traffic before routing to it. Add a preStop hook (5 second sleep) to drain in-flight requests before shutdown |
| Need instant rollback | Implement the **Blue-Green Deployment pattern**: maintain two identical environments (Blue = current, Green = new). Deploy and test on Green, then switch the load balancer to point at Green. Rollback = switch back to Blue instantly. Costs 2x resources but gives instant rollback |
| Risky change, gradual rollout | Implement the **Canary Deployment pattern**: route 5% of traffic to the new version using weighted routing at the load balancer or ingress controller (Nginx, Envoy, Istio). Monitor error rates and latency. If healthy, increase to 25%, 50%, 100%. If unhealthy, route 100% back to the old version |

---

### Phase 9 — Decide on Architectural Patterns

**Q33: "Should this be a monolith or microservices?"**

| Answer | Draw |
|--------|------|
| Small team (2-5 developers), unclear domain boundaries | **Modular Monolith** — one deployable with clear internal module boundaries (separate folders, interfaces between modules). You can split into microservices later when boundaries are proven. Implement by enforcing module boundaries with dependency rules (no circular dependencies, modules communicate via interfaces) |
| Multiple teams, clear domain boundaries, independent release cycles needed | **Microservices** — each service owns its domain, database, and deployment pipeline. Implement by aligning service boundaries with business domains (Domain-Driven Design bounded contexts). Each service communicates via APIs or events, never direct database access |
| Existing monolith, gradual extraction | **Strangler Fig pattern** — extract one bounded context at a time into a new service. Route traffic via a reverse proxy: old paths → monolith, extracted paths → new service. Share the database initially, evolve to database-per-service as data ownership becomes clear |

**Q34: "How should data flow through the system?"**

| Answer | Draw |
|--------|------|
| Simple request/response, no side effects | **Layered Architecture**: `[Controller] → [Service Layer] → [Repository] → [Database]`. Standard three-tier. Each layer depends only on the layer below |
| Complex domain logic, many business rules | **Clean Architecture / Hexagonal Architecture**: `[API Layer] → [Application Core (use cases, domain models)] → [Infrastructure (database, messaging)]`. The core has no dependencies on infrastructure — infrastructure implements interfaces defined by the core. Enables testing business logic without a database |
| Different optimization needs for reads and writes | **CQRS (Command Query Responsibility Segregation)**: separate the write path (commands → domain logic → primary database) from the read path (queries → denormalized read store or cache). Implement by having write operations update the primary database and publish events that update a separate read-optimized store |
| Need audit trail, undo, or temporal queries | **Event Sourcing**: store events (facts that happened) instead of current state. Rebuild current state by replaying events. Implement with an event store (EventStoreDB, or a Kafka topic with infinite retention). Natural pairing with CQRS — events drive read model projections |

**Q35: "How should services be organized?"**

| Answer | Draw |
|--------|------|
| Data that changes together should live together | **Domain-Driven Design bounded contexts** — group entities by business domain, not by technical layer. Example: User + Profile + Preferences = User Service (they change together). Orders + LineItems + Payments = Order Service. If two entities always change together, they belong in the same service. If they change independently, separate them |
| Some services are more important than others | **Service Tiers**: Tier 1 (critical path: auth, payments) gets more replicas, stricter SLAs, dedicated resources. Tier 2 (important but not critical: search, recommendations) gets standard resources with graceful degradation. Tier 3 (background: analytics, reports) runs on lower-priority resources and can tolerate delays |

---

### Phase 10 — Validate Your Design

Before you stop drawing, check these:

| Check | Ask yourself | If the answer is no, add... |
|-------|-------------|----------------|
| **Single point of failure?** | Is there any box that, if it dies, everything dies? | Multiple instances behind a load balancer. Multi-availability-zone deployment. Database replicas with automatic failover |
| **Bottleneck?** | Is there one box that gets all the load? | Cache in front of hot reads (Redis). Queue to buffer writes (Kafka, SQS). Split the service into smaller services if it does too many things |
| **Data loss?** | If this box crashes mid-operation, do we lose data? | Database replication. Message queue persistence (Kafka retains messages on disk). Transactional Outbox pattern for guaranteed event delivery |
| **Security?** | Can an unauthenticated user reach the database? | Authentication at the API gateway. Authorization (RBAC) at each service. Network policies blocking direct database access from outside |
| **Debugging?** | If a request fails, how do I find where and why? | Distributed tracing (OpenTelemetry → Jaeger/Tempo). Structured logs with trace ID correlation (→ Loki/ELK). Metrics dashboards (Prometheus → Grafana) |
| **Cost?** | Am I adding components the system doesn't need yet? | Remove unnecessary complexity. A cache is wasted if you have 100 users. A message queue is wasted if everything is synchronous. Start simple, add when you have data showing a bottleneck |
| **Consistency?** | Can two users see conflicting data? Is that OK? | If it's OK for a few seconds → eventual consistency via events. If it's never OK → single database transaction or synchronous saga with compensating actions |
| **Scalability?** | If traffic doubles tomorrow, does anything break? | Every service should be stateless (no in-memory state). State lives in databases, caches, or queues. Stateless services scale horizontally by adding instances |

---


## Scenario Dashboard

### Classic System Design — Likely Asked

|                                                                                                                                                                                                                         |                                                                                                                                                                                                                         |                                                                                                                                                                                                                         |                                                                                                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <div style="background:rgba(249,115,22,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**NOTIFICATION SYSTEM**</span> <br> [[#Communication Picker\|Kafka]] → Router → [[#Scenario Templates\|Email/Push/SMS]] · [[#Resilience\|DLQ]] · [[#Multi-Tenancy\|Per-tenant rate limit]] <br> *Why Kafka: fan-out to many consumers. Why DLQ: delivery can fail, need retry without blocking. Priority queues for urgent vs marketing.*</div> | <div style="background:rgba(249,115,22,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**REAL-TIME DASHBOARD**</span> <br> [[#Communication Picker\|Kafka/Streams]] → [[#Storage Picker\|Redis]](hot) + [[#Storage Picker\|SQL]](cold) · [[#Communication Picker\|WebSocket]] to browser · [[#Scaling\|Pre-aggregate]] <br> *Why split hot/cold: Redis for latest state (sub-ms), SQL for historical queries. Pre-aggregate in consumer, not at query time.*</div> | <div style="background:rgba(249,115,22,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**API GATEWAY**</span> <br> [[#Security Stack\|JWT validation]] · [[#Resilience\|Rate limiting]] · [[#Comparisons\|REST vs GraphQL vs gRPC]] routing · [[#Observability\|OTel]] injection <br> *Why gateway: single entry, centralize auth+rate limit. GraphQL gateway lets clients pick fields. gRPC behind gateway for internal.*</div> | <div style="background:rgba(249,115,22,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**CHAT SYSTEM**</span> <br> [[#Communication Picker\|WebSocket]] connections · [[#Storage Picker\|MongoDB]] message store · [[#Storage Picker\|Redis]] presence/typing · Group [[#Communication Picker\|fan-out]] <br> *Why WebSocket: full-duplex, low latency. Why MongoDB: messages are document-shaped, flexible, horizontal scaling.*</div> |
| <div style="background:rgba(249,115,22,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**JOB / WORKFLOW SCHEDULER**</span> <br> [[#Kubernetes\|CronJob]]/KEDA triggers · [[#Consistency\|Distributed lock]] (Redis) · [[#Problem → Pattern\|Saga]] for multi-step · State in [[#Storage Picker\|SQL]] <br> *Why distributed lock: prevent duplicate execution across instances. Why SQL: workflow state needs ACID (state machine transitions).*</div> | <div style="background:rgba(249,115,22,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**RATE LIMITER**</span> <br> Token bucket / Sliding window · [[#Storage Picker\|Redis]] for distributed state · [[#Multi-Tenancy\|Per-tenant rules]] · 429 response <br> *Why Redis: atomic operations (INCR+EXPIRE), sub-ms, shared across all API instances. Token bucket allows bursts, sliding window is more accurate.*</div> | <div style="background:rgba(249,115,22,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**SEARCH PLATFORM**</span> <br> [[#Problem → Pattern\|CDC]] → Indexer → [[#Storage Picker\|Elasticsearch]] · [[#Storage Picker\|Redis]] autocomplete · [[#Consistency\|Eventual consistency]] <br> *Why ES: inverted index for full-text, relevance scoring, aggregations. Why CDC: keep index in sync without coupling. Eventual consistency OK for search.*</div> | <div style="background:rgba(249,115,22,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**URL SHORTENER**</span> <br> Base62 ID · [[#Storage Picker\|Redis]] cache (100:1 read/write) · [[#Storage Picker\|SQL]] persistence · [[#Communication Picker\|Kafka]] → analytics <br> *Why Redis: 100:1 read ratio, hot URLs cached. Why Kafka for analytics: every redirect → event → aggregate clicks, referrers, geo async.*</div> |
| <div style="background:rgba(59,130,246,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**FILE UPLOAD PIPELINE**</span> <br> Pre-signed URL → [[#AWS ↔ Azure\|S3]] direct upload · [[#Communication Picker\|Kafka]] event → [[#Scaling\|Workers]] (scan, thumb, meta) · [[#Caching Layer\|CDN]] download <br> *Why pre-signed: never proxy large files through API (memory, timeout). Why async workers: scan/resize can take seconds, don't block upload response.*</div> | <div style="background:rgba(59,130,246,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**ORDER FLOW (SAGA)**</span> <br> [[#Problem → Pattern\|Saga]] over 2PC · [[#Problem → Pattern\|Outbox]] for guaranteed delivery · [[#Problem → Pattern\|Idempotency]] keys · [[#Resilience\|Compensating actions]] <br> *Why Saga: no distributed locks, each service does local tx + event. Why Outbox: event in same DB transaction, guarantees at-least-once.*</div> | <div style="background:rgba(59,130,246,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**CI/CD PIPELINE**</span> <br> [[#CI/CD Pipeline\|Build→Test→Scan→Gate]] · [[#IaC\|Terraform]] for infra · [[#Kubernetes\|Kustomize]] for deploy · [[#Anti-Patterns\|Shared templates]] (DRY) <br> *Why shared templates: 60+ services, one change propagates everywhere. Why quality gates: catch CVEs, breaking changes before merge.*</div> | <div style="background:rgba(59,130,246,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**E-COMMERCE PLATFORM**</span> <br> [[#Storage Picker\|PostgreSQL]] catalog · [[#Storage Picker\|Redis]] cart+session · [[#Problem → Pattern\|Saga]] checkout · [[#Communication Picker\|Kafka]] order events · [[#Caching Layer\|CDN]] <br> *Why polyglot: catalog needs joins (SQL), cart is temporary (Redis), order flow spans services (Saga), product images (CDN).*</div> |

### More Classic Scenarios

|                                                                                                                                                                                                                         |                                                                                                                                                                                                                         |                                                                                                                                                                                                                         |                                                                                                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <div style="background:rgba(59,130,246,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**SOCIAL FEED / TIMELINE**</span> <br> [[#Communication Picker\|Kafka]] fan-out on post · [[#Storage Picker\|Redis]] sorted set per user · [[#Scaling\|Pre-compute]] feed · [[#Caching Layer\|Cache-aside]] <br> *Why fan-out-on-write: pre-build feed at post time (fast reads). Why Redis sorted set: chronological ordering with O(log N) insert.*</div> | <div style="background:rgba(59,130,246,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**PAYMENT SYSTEM**</span> <br> [[#Consistency\|Strong consistency]] · [[#Problem → Pattern\|Idempotency]] keys · [[#Problem → Pattern\|Outbox]] · [[#Resilience\|Retry + DLQ]] · PCI compliance <br> *Why strong consistency: money can't be eventually consistent. Why idempotency: retried charge must not double-bill. Outbox guarantees event delivery.*</div> | <div style="background:rgba(59,130,246,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**CONFIG / FEATURE FLAG SVC**</span> <br> [[#Storage Picker\|Redis]] for fast reads · [[#Communication Picker\|SSE]] for live updates · Per-tenant overrides · Audit log · A/B % rollout <br> *Why Redis: every request checks flags (must be sub-ms). Why SSE: push flag changes to running services without restart.*</div> | <div style="background:rgba(59,130,246,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**LOGGING / LOG AGGREGATION**</span> <br> [[#Communication Picker\|Kafka]] as log bus · [[#Observability\|Loki/ELK]] storage · [[#Storage Picker\|S3]] archive · Retention policies · Structured JSON <br> *Why Kafka: buffer log spikes, decouple producers from consumers. Why Loki over ELK: cheaper (labels-only indexing), native Grafana.*</div> |
| <div style="background:rgba(34,197,94,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**LEADERBOARD / RANKING**</span> <br> [[#Storage Picker\|Redis]] sorted set (ZADD/ZRANK) · [[#Scaling\|Read replicas]] · [[#Caching Layer\|Cache-aside]] for top-N · Periodic snapshot to SQL <br> *Why Redis sorted set: O(log N) insert and O(1) rank lookup. Purpose-built data structure for rankings.*</div> | <div style="background:rgba(34,197,94,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**EMAIL DELIVERY SYSTEM**</span> <br> [[#Communication Picker\|Kafka]] ingest · Rate control (ISP throttling) · Bounce/complaint handling · [[#Resilience\|DLQ]] · Reputation tracking <br> *Why Kafka: buffer millions of emails, process at rate ISPs allow. Why DLQ: bounces and failures need separate retry logic.*</div> | <div style="background:rgba(34,197,94,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**ANALYTICS / EVENT TRACKING**</span> <br> [[#Communication Picker\|Kafka]] event ingestion · [[#Scaling\|Batch writers]] → data warehouse · [[#Storage Picker\|Redis]] real-time counters · [[#Caching Layer\|Pre-aggregation]] <br> *Why Kafka: high-throughput ingestion (1M+ msg/s). Why batch: aggregate before write to warehouse (cost, efficiency).*</div> | <div style="background:rgba(34,197,94,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**CONTENT MGMT (CMS)**</span> <br> [[#Storage Picker\|PostgreSQL]] content + versions · [[#Storage Picker\|S3]] media assets · [[#Caching Layer\|CDN]] delivery · [[#Communication Picker\|Webhook]] publish events <br> *Why SQL: content has relations (author, category, tags, versions). Why CDN: static rendered pages cached globally.*</div> |
| <div style="background:rgba(34,197,94,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**IoT DATA PIPELINE**</span> <br> [[#Communication Picker\|Kafka]] high-throughput ingest · [[#Storage Picker\|TimescaleDB]] time-series · [[#Scaling\|KEDA]] workers · [[#Resilience\|Backpressure]] · Edge processing <br> *Why Kafka: millions of device events/sec. Why TimescaleDB: time-bucketed compression, downsampling, retention policies built-in.*</div> | <div style="background:rgba(34,197,94,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**VIDEO STREAMING**</span> <br> [[#Storage Picker\|S3]] raw storage · Transcoding workers ([[#Scaling\|KEDA]]) · [[#Caching Layer\|CDN]] for delivery · Adaptive bitrate · [[#Storage Picker\|Redis]] view counts <br> *Why CDN: video is bandwidth-heavy, edge caching critical. Why KEDA: scale transcoding workers on queue depth, scale to zero when idle.*</div> | <div style="background:rgba(34,197,94,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**RECOMMENDATION ENGINE**</span> <br> [[#Communication Picker\|Kafka]] user events · Batch ML pipeline · [[#Storage Picker\|Redis]] serving cache · [[#Resilience\|Graceful degradation]] (fallback to popular) <br> *Why batch ML: recommendations don't need real-time retraining. Why Redis cache: pre-computed recs served sub-ms. Fallback if ML service is down.*</div> | <div style="background:rgba(34,197,94,0.12);padding:8px;border-radius:8px"><span style="font-size:1.3em">**DISTRIBUTED CONFIG / SERVICE REGISTRY**</span> <br> [[#Kubernetes\|K8s DNS]] for discovery · [[#Storage Picker\|Redis]]/etcd for config · [[#Communication Picker\|SSE]] push updates · Health-based routing <br> *Why K8s DNS: built-in service discovery, no Consul/Eureka needed. Why etcd: strong consistency for config, used by K8s itself.*</div> |

### Architecture Discussion Topics — Quick Scan

|                                                                                                                                                                                                                         |                                                                                                                                                                                                                         |                                                                                                                                                                                                                         |                                                                                                                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**How to split a monolith?** <br> [[#Migration Checklist\|Strangler fig]] · [[#Consistency\|DB strategy]] · [[#Communication Picker\|Events]]</div> | <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**Data consistency across svcs?** <br> [[#Consistency\|Eventual]] · [[#Problem → Pattern\|Saga]] · [[#Problem → Pattern\|Outbox]] · [[#Scaling\|CQRS]]</div> | <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**Request path browser → DB?** <br> [[#Caching Layer\|CDN]] → LB → [[#Kubernetes\|Ingress]] → [[#Security Stack\|GW]] → Svc → [[#Caching Layer\|Cache]] → DB</div> | <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**High availability?** <br> Multi-AZ · [[#Resilience\|Health checks + CB]] · [[#Kubernetes\|HPA + PDB]] · [[#Kubernetes\|Rolling update]]</div> |
| <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**Auth in microservices?** <br> [[#Security Stack\|OAuth2+OIDC · JWT · mTLS · Pod identity · Tenant scoping]]</div> | <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**CI/CD for 50+ services?** <br> [[#CI/CD Pipeline\|Shared templates · Quality gates · Breaking change CI]] · [[#Numbers\|DORA]]</div> | <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**Monitor distributed system?** <br> [[#Observability\|OTel → Traces + Logs + Metrics · Trace ID correlation]]</div> | <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**Secrets in K8s?** <br> [[#Security Stack\|Key Vault CSI · Pod identity]] · [[#Kubernetes\|NetworkPolicy · RBAC]]</div> |
| <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**Sync vs async?** <br> [[#Comparisons\|gRPC]] when need response · [[#Comparisons\|Kafka]] when fire-and-forget/fan-out</div> | <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**Handle traffic spike?** <br> [[#Scaling\|Queue buffers · HPA/KEDA]] · [[#Caching Layer\|Cache absorbs]] · [[#Resilience\|CB protects]]</div> | <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**SQL vs NoSQL?** <br> [[#Comparisons\|ACID vs flexibility · Joins vs nesting · Vertical vs horizontal]]</div> | <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**Zero-downtime deploy?** <br> [[#Kubernetes\|Rolling(maxUnavail:0) · Readiness · PDB]] · [[#Deployment Strategies\|Canary · Flags]]</div> |
| <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**Database per service?** <br> [[#Consistency\|Start shared → evolve]] · [[#Problem → Pattern\|Events for sync]] · [[#Anti-Patterns\|No shared DB]]</div> | <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**How to handle failures?** <br> [[#Resilience\|Timeout · Retry · CB · Bulkhead · DLQ · Graceful degradation]]</div> | <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**Caching strategy?** <br> [[#Caching Layer\|CDN for static · Redis cache-aside · TTL + event invalidation]]</div> | <div style="background:rgba(168,85,247,0.12);padding:8px;border-radius:8px">**Rebuild from scratch?** <br> [[#Anti-Patterns\|Modular monolith first]] · [[#Observability\|OTel day 1]] · [[#CI/CD Pipeline\|Testcontainers day 1]]</div> |

---

## Problem → Pattern

> [!example|no-icon] Stale data across services → **Eventual Consistency** — accept delay, converge
> Kafka/RabbitMQ events, consumers update own data. Brief window of inconsistency OK for dashboards, feeds, analytics.

> [!example|no-icon] Atomic op across 2+ services → **Saga** — local tx + events + compensating actions
> Choreography (2-3 steps, simple) or Orchestration (complex, central coordinator). Each step idempotent.

> [!example|no-icon] Guaranteed event after DB write → **Outbox** — event in outbox table, same DB transaction
> Separate process publishes from outbox. At-least-once delivery without distributed transactions.

> [!example|no-icon] Read model ≠ write model → **CQRS** — separate paths, optimize each
> Write side: domain logic. Read side: denormalized projection. Only where read/write genuinely diverge.

> [!example|no-icon] Full history / audit / time travel → **Event Sourcing** — store events, derive state
> Powerful for workflows, finance. Overkill for simple CRUD. Natural pairing with CQRS.

> [!example|no-icon] Migrating monolith → **Strangler Fig** — route traffic gradually, old + new coexist
> Reverse proxy routes: old requests → monolith, migrated → new service. Every step reversible.

> [!example|no-icon] One slow service kills everything → **Circuit Breaker** — fail fast after N failures
> Closed → Open (after 5 fails/30s) → Half-open (test after 60s). Polly in .NET.

> [!example|no-icon] One dependency saturates threads → **Bulkhead** — isolated pools per dependency
> 20 threads for Service A, 20 for B. A being slow doesn't affect B.

> [!example|no-icon] Cache stampede → **Jittered TTL + lock** — stale-while-revalidate
> First request acquires lock and refreshes. Others serve stale. Jitter prevents synchronized expiry.

> [!example|no-icon] Same message processed twice → **Idempotency** — dedup table or natural idempotency
> Idempotency key (UUID from client), dedup table, or design ops to be naturally idempotent (SET vs INCREMENT).

> [!example|no-icon] Retry storm after outage → **Exponential backoff + jitter** — 1s, 2s, 4s + random
> Without jitter: 1000 clients retry at same time. With: spread out. Max 3 retries. Combine with circuit breaker.

> [!example|no-icon] Data to search/analytics → **CDC** — stream DB changes as events
> DB changelog → indexer workers → Elasticsearch. Full re-index nightly + incremental via events.

> [!example|no-icon] Deploying risky changes → **Canary / Feature Flag** — small %, toggle on/off
> Canary: route 5% traffic to new version, monitor, increase. Flag: deploy code OFF, enable gradually.

---

## Communication Picker

### Client → API

| Need | Tool | What it is and how it works | When to choose and why | How to implement |
|------|------|-----------------------------|----------------------|------------------|
| Simple create/read/update/delete operations | **REST** | Each URL represents a resource (`/users/123`). Uses standard HTTP methods: GET (read), POST (create), PUT (update), DELETE (remove). Returns JSON. Stateless — each request is independent | When your API has predictable, resource-oriented endpoints and you want native HTTP caching (GET requests cached via ETag/Last-Modified headers). Simplest for external partners who just want to `curl` your API | Define resources and endpoints with OpenAPI/Swagger. Use proper HTTP status codes (200 OK, 201 Created, 404 Not Found, 409 Conflict). Add versioning via URL path (`/v1/users`) or headers |
| Frontend needs flexible queries (different pages need different fields) | **GraphQL** | Single endpoint (`/graphql`) that accepts a query specifying exactly which fields the client wants. The server returns only those fields. Eliminates over-fetching (getting 50 fields when you need 3) and under-fetching (needing 5 REST calls to build one page) | When you have multiple client types (web, mobile, admin) that need different data shapes from the same entities. When reducing network round-trips matters (mobile on slow connections). Not for simple CRUD or external partners | Use Apollo Server (Node.js), HotChocolate (.NET), or Strawberry (Python). Define a schema with types and resolvers. Add query depth limiting (max 5 levels) and complexity analysis to prevent abuse. Disable introspection in production |
| Real-time bidirectional communication (chat, collaborative editing) | **WebSocket** | Upgrades an HTTP connection to a persistent, full-duplex TCP connection. Both client and server can send messages at any time without waiting for a request. Low latency because the connection stays open — no HTTP overhead per message | When the server needs to push data AND the client needs to send data in real-time. Chat systems, live collaboration, gaming. Not for one-way updates (use Server-Sent Events instead — simpler) | Open a WebSocket connection from the client (`new WebSocket('wss://...')`). On the server, manage connections in a connection manager. Use Redis Pub/Sub to broadcast messages across multiple server instances (because each user connects to one specific server, but messages need to reach all servers) |
| Server pushes updates to the client (dashboards, notifications, live feeds) | **Server-Sent Events (SSE)** | A one-way HTTP connection where the server sends events to the client. The client opens a standard HTTP request, the server holds it open and sends text events as they happen. The browser automatically reconnects if the connection drops | When you only need server → client communication. Simpler than WebSocket: it's just HTTP, works through all proxies and load balancers, has built-in auto-reconnect. Use for dashboards, notification feeds, live status updates | Server sends `Content-Type: text/event-stream` and writes `data: {...}\n\n` for each event. Client uses `new EventSource('/events')`. Feed events from Redis Pub/Sub or Kafka consumer into the SSE stream |
| External system needs to be notified when something happens | **Webhook (HTTP POST callback)** | Your system sends an HTTP POST request to a URL registered by the external system whenever an event occurs. The external system processes the payload. Reverse of a normal API call — you call them, not the other way around | When external partners need to react to events in your system (e.g., "notify Slack when a ticket is created"). The external system registers a callback URL, you POST to it. They don't need to poll your API | Store registered webhook URLs in your database. When an event occurs, POST the payload with an HMAC-SHA256 signature header so the receiver can verify it came from you. Send asynchronously via a queue (not inline) — if their server is slow, it shouldn't block your operation. Retry with exponential backoff on failure |
| User uploads large files (images, documents, video) | **Pre-signed URL + direct upload to object storage** | Your API generates a temporary, signed URL that grants the client permission to upload directly to S3/Blob Storage. The client uploads the file directly to storage without going through your API server. After upload, an event triggers processing (virus scan, thumbnail generation) | When files are larger than a few megabytes. Proxying large files through your API ties up server memory and threads for the duration of the upload. Pre-signed URLs offload this entirely to the storage service, which is built for it | Client calls your API: `POST /uploads` → API generates a pre-signed URL with `PutObject` permission (expires in 15 minutes) → returns URL to client → client uploads directly to S3/Blob → S3 triggers an event (S3 Event Notification or EventBridge) → worker processes the file (virus scan with ClamAV, thumbnail generation with ImageMagick, metadata extraction) → updates database status to "ready" |

### Service ↔ Service (Internal)

| Need | Tool | What it is and how it works | When to choose and why | How to implement |
|------|------|-----------------------------|----------------------|------------------|
| Synchronous call — caller needs a response immediately | **gRPC** | A framework for making remote function calls between services using binary Protocol Buffers (protobuf) over HTTP/2. You define the service contract in a `.proto` file, and a code generator creates typed client and server code in your language. 10x smaller payloads than JSON, multiplexed connections, and compile-time type safety | When services call each other frequently and need fast, reliable, typed communication. A field change in the `.proto` file causes a compile error in the consumer, not a runtime crash weeks later. Not for browser clients (needs a gRPC-Web proxy). Choose over REST for internal calls because it's faster and type-safe | Define service contracts in `.proto` files organized by service and version (`users/v1/users.proto`). Generate client libraries and publish as packages (NuGet, npm, pip). Add deadline propagation — every gRPC call should have a timeout so a slow service doesn't hang the caller forever. Run backward compatibility checks in CI (using `buf breaking`) to catch breaking changes before merge |
| Asynchronous events — multiple services need to react, events need replay | **Apache Kafka** | A distributed, durable, append-only event log. Producers write events to topics. Topics are split into partitions for parallelism. Consumer groups read from partitions independently at their own pace. Events are retained for a configurable period (days, weeks, or forever) and can be replayed from any offset | When 3+ services need to react to the same event (fan-out). When consumers need to replay/reprocess old events (rebuilding a search index, fixing a bug, adding a new consumer). When ordering matters (events for the same entity must be processed in order). Choose over RabbitMQ when you need durability, replay, or many independent consumers | Produce events to named topics (e.g., `orders.created`). Use the entity ID as the partition key — all events for the same entity go to the same partition, guaranteeing order. Each consuming service has its own consumer group with its own offset tracking. Set retention based on replay needs (7 days default, or infinite for event sourcing). Add a Dead Letter Topic for events that fail processing after N retries |
| Asynchronous commands — one specific service needs to process a task | **RabbitMQ** | A message broker with exchanges, queues, and bindings. Producers publish to an exchange with a routing key. The exchange routes the message to matching queues based on binding rules. Consumers pull from queues and acknowledge (ack) or reject (nack) messages. Rejected messages go to a Dead Letter Queue | When you need flexible routing (e.g., `VehicleState.Energy.*` routes to the energy monitor, `VehicleState.#` routes to the catch-all). When you need request-reply patterns. When messages should be consumed by exactly one consumer (competing consumers pattern). Choose over Kafka when routing logic matters more than replay or fan-out | Declare exchanges (topic type for pattern matching, direct for exact routing, fanout for broadcast). Bind queues to exchanges with routing keys. Consumers acknowledge messages after successful processing — unacked messages are redelivered. Configure a Dead Letter Exchange for messages that fail after N retries. Use quorum queues (Raft-based replication) for durability in production |
| Simple async queue — zero operational burden, just need to decouple | **Amazon SQS (Simple Queue Service)** | A fully managed message queue. You create a queue, send messages, and receive messages. AWS handles scaling, availability, and durability. No clusters to manage, no brokers to monitor. Pay per message (very cheap). Built-in Dead Letter Queue support | When you want async processing without the operational cost of running Kafka or RabbitMQ clusters. When you don't need replay, complex routing, or multi-consumer fan-out. When you're on AWS and want a "just works" queue. Choose over Kafka when simplicity and zero ops matter more than features | Create a queue in AWS. Producer: `sqs.sendMessage()`. Consumer: `sqs.receiveMessage()` in a polling loop, process, then `sqs.deleteMessage()`. Configure a Dead Letter Queue — after 3 failed processing attempts, the message moves to the DLQ automatically. For fan-out, combine with SNS: publish to an SNS topic, each SQS queue subscribes and gets its own copy |

---

## Storage Picker

### Database

| Need | Tool | What it is and how it works | When to choose and why | Key concepts to know |
|------|------|-----------------------------|----------------------|----------------------|
| Relational data with transactions, joins, and constraints | **PostgreSQL** | An open-source relational database. Stores data in tables with typed columns, enforces relationships with foreign keys, supports complex joins across tables, and provides full ACID transactions. Also supports JSON columns for semi-structured data | When your data is naturally relational (users have orders, orders have line items, products belong to categories). When you need joins, complex queries, or multi-table transactions. The most feature-rich open-source database — choose over MySQL for advanced features (JSON, array columns, CTEs, window functions) | Indexes (B-tree for equality/range, GIN for JSON/full-text), explain plans for query optimization, connection pooling (PgBouncer), read replicas for scaling reads, partitioning for large tables, VACUUM for dead row cleanup |
| Relational data in a Microsoft/.NET ecosystem | **Microsoft SQL Server** | Microsoft's relational database. Deep integration with .NET, Visual Studio, and Azure. Enterprise licensing with advanced features (Always On availability groups, column store indexes, in-memory OLTP) | When the team and infrastructure are Microsoft-oriented. When using Dapper or Entity Framework — both have excellent SQL Server support. When you need enterprise features like Always On or when the existing infrastructure is SQL Server | Dapper for high-performance reads (raw SQL, no ORM overhead), Entity Framework for complex domain operations (change tracking, migrations), SqlBulkCopy for batch inserts (handles thousands of writes per second), query plan analysis with SQL Server Management Studio |
| Document-shaped data with flexible schema | **MongoDB** | A document database that stores data as JSON-like documents (BSON). Each document can have different fields — no schema migrations needed. Documents can contain nested objects and arrays. Supports multi-document ACID transactions (with replica set) | When your data varies per record (different vehicle types have different telemetry fields). When you need rapid iteration — add fields without schema migrations. When data is naturally nested (a product with variants, specs, and images all in one document). Choose over SQL when you rarely need joins and your data is "document-shaped" | Document design (embed vs reference: embed data that's always read together, reference data that changes independently), compound indexes, the aggregation pipeline for complex queries, replica sets for high availability, sharding for horizontal scaling |
| Sub-millisecond lookups, caching, counters, and rich data structures | **Redis** | An in-memory data store supporting strings, hashes, lists, sets, sorted sets, streams, and pub/sub. All operations are atomic and execute in microseconds. Data can be persisted to disk but is primarily in-memory | When you need a cache layer between your API and database (cache-aside pattern). When you need real-time data structures: sorted sets for leaderboards, streams for event logs, pub/sub for broadcasting, hashes for session storage. Choose over Memcached because Redis supports persistence, more data types, pub/sub, and Lua scripting | Cache-aside pattern (check cache → miss → query DB → write to cache with TTL), eviction policies (volatile-ttl for cache workloads, noeviction for streams), Sentinel for automatic failover (3 sentinels monitor primary, promote replica in ~5 seconds if primary fails), Redis Cluster for horizontal sharding |
| Full-text search with relevance scoring and faceted filtering | **Elasticsearch** (or OpenSearch) | A distributed search engine based on Apache Lucene. Builds an inverted index — for every word, it knows which documents contain it. Supports fuzzy matching, synonym expansion, relevance scoring (TF-IDF/BM25), aggregations, and faceted filtering | When users need to search by text and expect ranked results (not just exact matches). When you need autocomplete, "did you mean?" suggestions, or faceted navigation (filter by category + price range + rating). Choose Elasticsearch for search, not as a primary database — sync from your main database via events or CDC | Index documents with field mappings (text fields for full-text search, keyword fields for exact match). Sync data from the primary database using Change Data Capture (Debezium) or application-level events. Use edge-ngram analyzer for autocomplete. Run a nightly full re-index as a safety net. Accept that the search index is eventually consistent — it lags behind the primary database by milliseconds to seconds |
| Time-series data (IoT metrics, sensor readings, logs, financial ticks) | **TimescaleDB** or **InfluxDB** | TimescaleDB is a PostgreSQL extension optimized for time-series: automatic time-based partitioning, compression (10-20x), downsampling (aggregate old data to save space), and retention policies (auto-delete data older than N days). InfluxDB is a purpose-built time-series database with its own query language | When data is append-mostly with a timestamp as the primary dimension. When you need efficient queries like "average temperature per hour for the last 30 days" or "max CPU usage per 5-minute window". Choose TimescaleDB if you already use PostgreSQL (it's an extension). Choose InfluxDB for a dedicated time-series stack | Hypertable partitioning (automatic chunking by time), continuous aggregates (pre-computed rollups that update automatically), retention policies (drop data older than 90 days), compression policies (compress chunks older than 7 days) |
| Graph relationships (social networks, recommendation engines, knowledge graphs) | **Neo4j** or **Amazon Neptune** | A graph database that stores nodes (entities) and edges (relationships) as first-class concepts. Queries traverse relationships directly without joins. Cypher query language (Neo4j) or Gremlin (Neptune) for pattern matching across relationships | When relationships are the core of your data model (friends-of-friends, shortest path, who-bought-what-also-bought). When relationship traversal depth is variable and unpredictable. Choose over SQL when recursive CTEs become too slow or complex (typically at depth 3+) | Nodes with labels and properties, edges with types and properties, Cypher queries for pattern matching (e.g., `MATCH (u:User)-[:BOUGHT]->(p:Product)<-[:BOUGHT]-(other:User) RETURN other`), index on frequently queried properties |
| Binary files: images, videos, documents, backups | **Amazon S3** / **Azure Blob Storage** / **Google Cloud Storage** | Object storage — stores files as objects in buckets/containers. Each object has a key (path), the binary data, and metadata. Designed for durability (99.999999999%), cheap storage, and high throughput. Not a database — no queries, no indexes, just store and retrieve by key | When your system handles any binary content. Never store large files in a database (expensive, slows down backups, limits scalability). Object storage integrates with CDN for global delivery, has lifecycle policies (move to cold storage after 90 days), and supports pre-signed URLs for secure direct upload/download | Upload via SDK or pre-signed URL, organize with key prefixes (`/tenant-123/uploads/2024/01/image.jpg`), set lifecycle rules (move to Glacier after 90 days, delete after 1 year), enable versioning for audit/recovery, serve via CDN (CloudFront distribution pointing at the bucket) |
| Massive write throughput with linear horizontal scaling | **Apache Cassandra** or **Amazon DynamoDB** | Cassandra: a distributed wide-column store designed for high write throughput across multiple data centers. No single point of failure — every node can accept writes. DynamoDB: AWS's fully managed key-value/document store with automatic scaling, single-digit millisecond latency, and pay-per-request pricing | When write volume exceeds what a single relational database can handle (100K+ writes/second). When you need multi-datacenter replication with no downtime. Choose Cassandra if you want control and can manage the cluster. Choose DynamoDB if you want zero operational burden and are on AWS | Cassandra: design tables around your query patterns (denormalize, one table per query), choose partition keys that distribute data evenly, use replication factor 3 for durability. DynamoDB: design with partition key + sort key, use single-table design for related entities, enable auto-scaling or on-demand capacity mode |

### Caching Layer

| Need | Tool | What it is and how it works | When to choose and why | How to implement |
|------|------|-----------------------------|----------------------|------------------|
| Static assets (images, CSS, JavaScript, fonts) cached globally | **CDN (Content Delivery Network)** — CloudFront, CloudFlare, Akamai | A network of edge servers worldwide that cache and serve static content from the location closest to the user. First request goes to the origin server; all subsequent requests for the same file are served from the edge cache | When your application serves static files to users in multiple geographic regions. The CDN handles 90%+ of static traffic, so your origin server barely gets hit. Use versioned filenames (`app.a3b2c1.js`) so deploying a new version doesn't require cache purging — the filename changes | Point your domain's static asset subdomain to the CDN. Set `Cache-Control: public, max-age=31536000` on versioned assets (cache forever — the filename changes on redeploy). Set `Cache-Control: no-cache` on `index.html` so the browser always fetches the latest version that references the new asset filenames |
| Application data read frequently (user profiles, product details, config) | **Redis with cache-aside pattern** | The application checks Redis first. On cache hit: return cached data (sub-millisecond). On cache miss: query the database, store the result in Redis with a TTL, return the data. Redis serves as a fast read-through layer in front of the database | When the same data is read repeatedly (product page viewed 1000 times, user profile fetched on every request). The cache absorbs reads, reducing database load by 90%+. Choose cache-aside over write-through because it's simpler and only caches data that's actually requested | On read: `GET cache_key` → if exists, return it. If not, query DB, then `SET cache_key value EX 300` (5-minute TTL). On write: update DB, then delete the cache key (next read will repopulate). Use consistent key naming: `user:{id}:profile`, `product:{id}:details`. Set TTL on every cached value — never cache without expiration |
| User sessions shared across multiple server instances | **Redis with TTL** | Store session data (user ID, roles, preferences, CSRF token) in Redis with an expiration time. Every server instance reads/writes to the same Redis, so it doesn't matter which server handles the request | When you have multiple API server instances behind a load balancer. Without shared session storage, a user logged in on Server A gets a "not authenticated" error if their next request goes to Server B. Redis makes servers stateless — any instance can handle any user | On login: generate a session ID (UUID), store session data in Redis with `SET session:{id} {json} EX 1800` (30-minute TTL). Set the session ID as an HttpOnly, Secure, SameSite cookie. On each request: read the session from Redis using the cookie value. On logout: delete from Redis |
| Expensive aggregations or report data that doesn't change often | **Materialized View** (database-level or application-level) | A pre-computed query result stored as a table or cache entry. Instead of running an expensive aggregation query on every dashboard load, the result is computed once (on write or on schedule) and served instantly on read | When you have dashboard queries that aggregate millions of rows (total sales by region, ticket counts by status, average response time). Computing on every request is slow and wasteful. Pre-compute the result when data changes or on a schedule | Database-level: PostgreSQL `CREATE MATERIALIZED VIEW stats AS SELECT ...`, refresh with `REFRESH MATERIALIZED VIEW CONCURRENTLY stats` on a schedule (every 5 minutes) or triggered by data changes. Application-level: a background worker computes aggregations and stores results in Redis. The dashboard reads from Redis — instant response |
| HTTP responses that are identical for all users (public pages, API responses) | **Reverse Proxy cache** — Nginx, Varnish, or CDN | A reverse proxy sits in front of your API and caches complete HTTP responses. If the same URL is requested again within the TTL, the proxy returns the cached response without forwarding the request to the backend | When you have public endpoints that return the same data for all users (product listing, homepage, status page). Offloads the backend completely for cached responses. Not for user-specific data (unless you cache per-user with Vary headers) | Configure Nginx with `proxy_cache_path` and `proxy_cache_valid 200 60s`. Add `Cache-Control: public, max-age=60` headers from your API. The proxy caches the response for 60 seconds. Use `Vary: Authorization` if different responses per user |
| Browser cache — avoid network requests entirely for unchanged resources | **HTTP Cache-Control headers** | The browser stores responses locally based on `Cache-Control` headers. On subsequent requests for the same URL, the browser uses the local copy without making a network request at all. Zero latency, zero server load for cached resources | For all static assets (already handled by CDN, but browser cache is the first layer checked), and for API responses that rarely change (feature flags, configuration). Use `ETag` headers for conditional revalidation — the browser sends `If-None-Match`, server returns 304 Not Modified if unchanged (no body transferred) | Set `Cache-Control: public, max-age=31536000, immutable` on versioned static assets. Set `Cache-Control: private, max-age=60` on user-specific API responses. Use `ETag` headers on API responses — generate from content hash, return 304 if unchanged |

---

## Scaling

| Bottleneck                                        | Strategy (Pattern)                                  | Tool                                                                                                                           | How to implement                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Too many reads — database is slow under read load | **Read Replica pattern** + **Cache-Aside pattern**  | Database read replicas (RDS Read Replica, PostgreSQL streaming replication) + Redis                                            | Route write queries to the primary database. Route read queries to read replicas. Add Redis in front for the hottest data (cache-aside with TTL). The combination reduces primary database load by 90%+                                                                                                                                              |
| Too many writes — single database can't keep up   | **Sharding pattern** (horizontal partitioning)      | Database-level sharding by tenant ID, user ID, or geography. Or application-level routing to separate database instances       | Choose a shard key that distributes writes evenly. Tenant ID is common for SaaS (each tenant's data lives on one shard). Hash-based sharding for even distribution. Range-based sharding for time-series data. Avoid cross-shard queries — they're expensive                                                                                         |
| CPU spikes — API pods running hot under load      | **Horizontal Pod Autoscaler (HPA)**                 | Kubernetes HPA                                                                                                                 | Configure HPA with `targetCPUUtilizationPercentage: 75`. When average CPU across pods exceeds 75%, HPA adds pods. When it drops below, HPA removes pods. Requires stateless services (no in-memory state) — state must live in database, cache, or queue                                                                                             |
| Message queue growing — consumers can't keep up   | **Event-Driven Autoscaling**                        | KEDA (Kubernetes Event-Driven Autoscaling)                                                                                     | KEDA monitors external metrics (Kafka consumer lag, SQS queue depth, RabbitMQ queue length). When the metric exceeds a threshold, KEDA scales up worker pods. When the queue is empty, KEDA scales to zero (saving cost). More responsive than CPU-based HPA for queue-processing workloads                                                          |
| Read and write need different optimization        | **CQRS (Command Query Responsibility Segregation)** | Separate write path (commands → domain logic → primary database) and read path (queries → denormalized read store)             | Write operations go through the domain model and store in the normalized primary database. After each write, publish an event that updates a denormalized read store (Redis, a read-optimized database table, or Elasticsearch). Read operations hit the fast read store. The read store is eventually consistent with the write store               |
| Spiky traffic overwhelms the system during peak   | **Queue-Based Load Leveling pattern**               | Apache Kafka, Amazon SQS, or RabbitMQ as a buffer                                                                              | Instead of processing requests synchronously (where a spike overwhelms the backend), the API enqueues requests and returns 202 Accepted. Worker services consume from the queue at a steady rate the backend can handle. The queue absorbs the spike. Combine with KEDA to auto-scale workers based on queue depth                                   |
| Users in multiple regions experience high latency | **Multi-Region Deployment** + **CDN**               | CDN (CloudFront, CloudFlare) for static content, multi-region database replicas, GeoDNS (Route 53, CloudFlare DNS) for routing | Deploy the application in 2-3 regions. CDN serves static assets from the nearest edge. GeoDNS routes users to the nearest application deployment. Database: either read replicas per region (writes go to primary region) or active-active with conflict resolution. Start with CDN + single region, add regions only when latency data justifies it |
| Stateful service can't scale horizontally         | **Externalize State pattern**                       | Move state from in-memory to Redis (sessions, locks), database (persistent state), or message queue (pending work)             | Identify what state the service holds in memory (sessions, caches, locks, uploaded files in progress). Move each piece to the appropriate external store. Once the service is stateless, it can be scaled horizontally by adding instances — any instance can handle any request                                                                     |

---

## Consistency

| Scenario | Consistency Level | Pattern | How it works | When to choose |
|----------|------------------|---------|--------------|----------------|
| All operations within one service and one database | **Strong consistency** | Database transaction | Wrap multiple operations in a single database transaction. Either all succeed or all fail (atomicity). The database guarantees isolation from concurrent transactions. Standard approach for any single-service operation | Always use for operations within one service — there's no reason not to. It's the simplest and most reliable option |
| Multiple services need to stay in sync, but a few seconds of delay is acceptable | **Eventual consistency** | Event-driven with consumers | Service A writes to its database and publishes an event (e.g., "OrderCreated"). Service B consumes the event and updates its own database. There's a window (milliseconds to seconds) where A and B have different views of the data. Eventually they converge | When the business logic tolerates brief inconsistency. Dashboards, search indexes, activity feeds, analytics — users don't notice a 2-second delay. This covers 90% of cross-service data synchronization needs |
| Multiple services must coordinate, and failures must roll back previous steps | **Saga** | Choreography (each service reacts to events) or Orchestration (a coordinator directs the flow) | A sequence of local transactions across services, each publishing an event on success. If a step fails, compensating actions undo previous steps (e.g., refund the payment if inventory reservation fails). Each step must be idempotent | When an operation spans 2+ services and partial completion is unacceptable (order processing: charge payment → reserve inventory → schedule shipping). Use choreography for simple flows (2-3 steps). Use orchestration when the flow is complex or you need visibility into the saga state |
| A database write must also publish an event, and neither can be lost | **Guaranteed delivery** | Transactional Outbox | Write the data change AND the event to an outbox table in the same database transaction. A separate process (a poller or Change Data Capture with Debezium) reads from the outbox and publishes to the message broker. The event is guaranteed to be published if and only if the data was committed | When you need reliable event publishing without distributed transactions. Without the outbox, a crash between "commit to DB" and "publish to Kafka" means the event is lost. The outbox eliminates this gap |
| A user must see their own changes immediately after writing | **Read-your-writes** (Session consistency) | Sticky routing or optimistic UI | Option 1: Route the user's reads to the same database node that handled their write (sticky sessions or read-from-primary for N seconds after a write). Option 2: Optimistic UI — the frontend shows the change immediately (before the server confirms) and reconciles on the next fetch | When eventual consistency causes confusing user experience — the user updates their profile but sees the old version on page refresh. Most important for user-facing operations where the person who made the change is looking at the result |

**Rule of thumb:** Choose **strong consistency** when money, safety, or data integrity is at stake (payments, inventory, commands). Choose **eventual consistency** when brief staleness is acceptable and simplicity matters (feeds, dashboards, search, analytics).

---

## Security Stack

| Layer | What it protects against | Tool | Why this tool | How to implement |
|-------|-------------------------|------|---------------|-----------------|
| **Edge** | Distributed Denial of Service (DDoS) attacks, bot traffic, common web exploits (SQL injection, cross-site scripting at the HTTP level) | CloudFlare, AWS Shield, AWS WAF (Web Application Firewall) | CloudFlare is the cheapest and easiest — just point your DNS to CloudFlare and it proxies all traffic, filtering attacks at the edge before they reach your servers. AWS Shield is included free with ALB and provides basic DDoS protection. AWS WAF lets you write rules to block specific attack patterns | Put CloudFlare or a WAF in front of your load balancer as the first layer traffic hits. Configure rate limiting rules (e.g., max 100 requests per second per IP). Enable managed rulesets for OWASP Top 10 attacks |
| **Transport** | Eavesdropping, man-in-the-middle attacks, data interception on the network | TLS (Transport Layer Security) for all external traffic, mTLS (mutual TLS) for service-to-service | TLS encrypts all data in transit so network sniffers see only encrypted bytes. mTLS adds client certificate verification — both sides prove their identity, preventing unauthorized services from calling your internal APIs | External: terminate TLS at the load balancer or ingress controller using Let's Encrypt certificates (free, auto-renewing via cert-manager in Kubernetes). Internal: configure mTLS between services using a service mesh (Istio, Linkerd) or Kubernetes network policies with certificate-based identity |
| **Identity** | Unauthorized access — someone calling your API without being logged in | OAuth2 + OpenID Connect (OIDC) for the authentication protocol, JWT (JSON Web Tokens) as the token format | OAuth2 + OIDC is the industry standard for web authentication — every identity provider supports it (Auth0, Okta, Azure AD, Google, Keycloak). JWT is stateless — the token itself contains user claims, so the API verifies the signature without a database lookup, which is fast and scalable | Use an identity provider (Auth0, Okta, Keycloak, or AWS Cognito) to handle login flows. The provider issues a JWT containing user ID, roles, and tenant ID. Your API gateway validates the JWT signature on every request using the provider's public key. Short-lived access tokens (15 minutes) + long-lived refresh tokens (7 days) |
| **Authorization** | Users doing things they shouldn't — accessing other users' data, performing admin actions without admin rights | Role-Based Access Control (RBAC) checked at each service, plus resource ownership checks | RBAC is simple and covers most cases — assign roles (admin, editor, viewer) and check the role before allowing an action. Resource ownership checks prevent horizontal privilege escalation (user A accessing user B's data) | Store roles in the JWT claims. Each service reads the role from the token and checks it against the required permission for the endpoint using policy-based middleware (e.g., `[Authorize(Policy = "AdminOnly")]` in .NET, or a middleware function). For resource ownership: every database query includes `WHERE user_id = @requesting_user_id` |
| **Multi-tenant** | Data leakage between tenants — one customer seeing another customer's data | Tenant ID in the JWT, tenant-scoped database queries, per-tenant rate limiting | Tenant isolation is the most critical security concern in a SaaS application. A single missing `WHERE tenant_id = @tenant` clause means data leakage. Defense in depth: enforce at the API gateway, at each service, and at the database level | Add `tenant_id` as a claim in the JWT. The API gateway extracts it and passes it to services. Every database query filters by tenant_id — enforce this with a base repository class or query interceptor so developers can't accidentally skip it. Add integration tests that verify cross-tenant queries return empty results |
| **Secrets** | Leaked credentials — database passwords, API keys, encryption keys exposed in source code or environment variables | AWS Secrets Manager, Azure Key Vault, HashiCorp Vault, Google Cloud Secret Manager | A secrets manager stores credentials encrypted, controls access with IAM policies, provides audit logs of who accessed what, and supports automatic rotation. Secrets in code or Git history are the #1 cause of production breaches | Store all credentials in the secrets manager. In Kubernetes, use the CSI Secrets Store Driver to mount secrets as files inside pods — the application reads the password from a file path, never from an environment variable (environment variables are visible in `kubectl describe pod`). For cloud-to-cloud access, use pod identity (AWS IRSA, Azure Workload Identity) so pods authenticate without any stored credentials |
| **Data** | Data theft if an attacker gains access to the storage layer (database files, disk snapshots, backups) | AWS KMS (Key Management Service), Azure Key Vault, Google Cloud KMS for key management; database-level transparent encryption | Encryption at rest ensures that even if someone steals a hard drive or a database backup, the data is unreadable without the encryption key. KMS manages the keys — you never handle raw encryption keys in your code | Enable transparent data encryption (TDE) on your database — RDS, Azure SQL, and Google Cloud SQL all support it with one setting. For sensitive fields (credit card numbers, personal data), use application-level field encryption with keys from KMS so that even database administrators can't read the plaintext |
| **Pipeline** | Deploying code with known vulnerabilities, leaked secrets in commits, vulnerable base images | Static Application Security Testing (SAST): SonarQube or Semgrep. Software Composition Analysis (SCA): Snyk or Dependabot. Container scanning: Trivy or Grype. Secret detection: git-secrets or detect-secrets | Catching vulnerabilities at build time costs 5 minutes to fix. The same vulnerability found in a penetration test costs days. Automated scanning in CI/CD makes security checks as routine as running tests | Add scanning stages to your CI/CD pipeline: (1) SAST scans source code for security patterns — block merge if SQL concatenation or hardcoded credentials are found. (2) SCA checks package dependencies against CVE databases — block build on critical CVEs. (3) Trivy scans the Docker image for OS and library vulnerabilities — block push to registry if critical vulnerabilities exist. (4) Pre-commit hook scans for secret patterns (connection strings, API keys) — block push before it reaches Git |
| **Network** | Lateral movement — an attacker who compromises one service accessing everything else in the network | Kubernetes NetworkPolicy (default deny + explicit allowlists), namespace isolation, Cilium for advanced Layer 7 policies | Default-deny network policies ensure that even if a service is compromised, it can only reach the specific services it's allowed to talk to — not the entire network. This limits the blast radius of any breach | Set a default-deny NetworkPolicy in each Kubernetes namespace — all ingress and egress blocked unless explicitly allowed. Then add specific allow rules: "Service A can talk to Service B on port 8080", "All pods can reach DNS", "Monitoring can scrape all pods on the metrics port". Use Cilium if you need Layer 7 rules (e.g., "allow HTTP GET but block HTTP DELETE") |

### Auth Flows

| Flow | When to use | How it works |
|------|-------------|--------------|
| **Authorization Code + PKCE** | Users logging in from a browser (SPA) or mobile app | The client generates a random `code_verifier`, hashes it to create a `code_challenge`, and sends the challenge with the auth request. After login, the authorization server returns a code. The client exchanges the code + original `code_verifier` for tokens. The server verifies the hash matches. This prevents an attacker who intercepts the code from using it (they don't have the verifier). Required for SPAs because they can't safely store a client_secret |
| **Client Credentials** | Machine-to-machine authentication — one service calling another, or a backend calling an external API | No user involved. The service authenticates with its own client_id and client_secret (stored in a secrets manager, never in code). The identity provider returns an access token. Simple and secure for backend-to-backend calls |
| **JWT (stateless tokens)** | API authentication — validating who is calling your API on every request | The identity provider issues a signed JWT containing claims (user_id, roles, tenant_id, expiration). The API verifies the signature using the provider's public key — no database lookup needed. Fast, scalable, but cannot be revoked before expiration (use short TTL + refresh tokens to mitigate) |
| **mTLS (mutual TLS)** | Service-to-service communication inside a cluster where no user context is needed | Both the client service and server service present TLS certificates and verify each other. Handled at the infrastructure level by a service mesh (Istio, Linkerd) or Kubernetes network configuration. No application code changes needed — the mesh sidecar handles certificate rotation and verification automatically |
| **Pod Identity (IRSA / Workload Identity)** | A Kubernetes pod accessing cloud services (S3, RDS, Secrets Manager) without storing any credentials | The pod's Kubernetes service account is federated with the cloud provider's identity system (AWS IAM via IRSA, Azure AD via Workload Identity). The pod receives temporary credentials that rotate automatically. No API keys, no passwords, no secrets to manage or leak |

---

## Observability

| Signal | What question it answers | Tool | How the tool works | Key method |
|--------|------------------------|------|--------------------|------------|
| **Metrics** | "What is happening right now?" — request rates, error counts, latency percentiles, CPU/memory usage | **Prometheus** collects metrics by scraping `/metrics` endpoints on each service every 15 seconds. **Grafana Mimir** stores metrics long-term in object storage (S3) for months instead of days | Prometheus uses PromQL for querying. Mimir is a drop-in replacement for Prometheus storage that scales horizontally | **RED method** per service: **R**ate (requests/second), **E**rrors (error percentage), **D**uration (latency at p50/p95/p99). Alert when error rate >5% over 5 minutes, not on a single error |
| **Logs** | "Why did it happen?" — the error message, stack trace, input that caused the failure | **Grafana Loki** stores logs indexed by labels only (namespace, service, pod) — much cheaper than full-text indexing. **ELK stack** (Elasticsearch + Logstash + Kibana) indexes every word — more powerful search but more expensive | Loki: Promtail agent collects logs from pods and ships to Loki. Query with LogQL in Grafana. ELK: Logstash collects and transforms, Elasticsearch stores and indexes, Kibana visualizes | Include the **trace ID** in every log line. Click a log entry in Grafana → jump to the full distributed trace in Tempo |
| **Traces** | "Where did it happen?" — which service was slow, which database query took long, across all 10+ services in the request path | **Grafana Tempo** or **Jaeger** store distributed traces. Tempo uses object storage (cheap at scale). Jaeger uses Elasticsearch or Cassandra | A trace is a tree of spans. Each span = one operation (HTTP call, DB query). Shows: API Gateway 5ms → User Service 50ms → Database 45ms. You instantly see where the time went | **OpenTelemetry (OTel)** SDK auto-instruments HTTP, gRPC, database, and message broker calls. Each request gets a unique trace ID propagated via W3C Trace Context headers. No manual instrumentation needed for basic tracing |
| **Profiling** | "Where is CPU or memory being spent inside a single service?" — unlike tracing (inter-service), profiling shows intra-service hotspots | **Grafana Pyroscope** or **Datadog Continuous Profiler** continuously sample CPU stack traces and memory allocations from running services | Produces flamegraphs showing which functions consume the most resources. Often reveals surprises: JSON serialization, regex evaluation, or excessive logging consuming 40% of CPU | Attach as a library or sidecar. Look at the flamegraph to find the widest bar (most CPU time). No performance overhead when not actively viewing |

**Alerting rule of thumb:** Alert on rates and trends, not individual events. "Error rate >5% for 5 minutes" is actionable. "One 500 error occurred" is noise that leads to alert fatigue.

---

## Comparisons

Covered in detail above in the Communication Picker and Storage Picker sections with full tool explanations, when-to-choose reasoning, and implementation guidance.

---

## Kubernetes

Covered in detail above in the Scaling section (Horizontal Pod Autoscaler, KEDA, Pod Disruption Budget) and in the Questions Phase 8 (deployment strategies).

Quick reference for Kubernetes object selection:

| Need | Kubernetes Object | How it works |
|------|-------------------|--------------|
| Run N replicas of a long-running service | **Deployment** | You declare the container image and replica count. Kubernetes keeps that many pods running, restarts crashed pods, and handles rolling updates (new version deployed one pod at a time with zero downtime) |
| Run one instance on every node in the cluster | **DaemonSet** | Kubernetes automatically schedules one pod per node. When a new node joins, it gets a pod. Used for log collectors (Promtail, Fluentd), monitoring agents (Grafana Alloy), time synchronization (Chrony NTP), network plugins |
| Run a batch task to completion then stop | **Job** | Creates a pod that runs until it exits successfully (exit code 0). If it fails, the Job retries (configurable `backoffLimit`). Used for data migrations, database seeding, one-off imports, report generation |
| Run a task on a recurring schedule | **CronJob** | Creates a new Job on a cron schedule (e.g., `"0 3 * * *"` = every day at 3 AM). Each run is a separate Job. Used for nightly cleanup, periodic data sync, scheduled report generation. Set `concurrencyPolicy: Forbid` to prevent overlapping runs |
| Stable internal network endpoint for a set of pods | **Service (ClusterIP)** | Creates a virtual IP and DNS name (e.g., `user-service.default.svc.cluster.local`) that load-balances across all healthy pods matching a label selector. Other services call this DNS name — Kubernetes handles routing |
| Route external HTTP/HTTPS traffic into the cluster | **Ingress** (standard) or **HTTPProxy** (Contour) | An Ingress Controller (Nginx, Contour/Envoy, Traefik) reads Ingress rules and configures routing. Maps hostnames and URL paths to internal Services. Handles TLS termination using certificates from cert-manager (Let's Encrypt) |
| Store non-sensitive configuration | **ConfigMap** | Key-value data that pods read as environment variables or mounted files. Used for feature flags, database hostnames, log levels. Changes require pod restart unless the app watches for file changes |
| Store sensitive configuration (passwords, API keys) | **Secret** + external vault via **CSI Secrets Store Driver** | For production: the CSI driver mounts secrets from an external vault (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault) as files inside the pod. The app reads from a file path. Never use environment variables for secrets — visible in `kubectl describe pod` |
| Automatically scale pods based on CPU or memory usage | **Horizontal Pod Autoscaler (HPA)** | Monitors average CPU/memory across pods every 15 seconds. When average exceeds the target (e.g., 75% CPU), HPA increases replica count. When it drops, HPA decreases. Set `minReplicas` and `maxReplicas` to bound scaling. Requires stateless services |
| Automatically scale pods based on queue depth or external metrics | **KEDA (Kubernetes Event-Driven Autoscaling)** | Extends Kubernetes with ScaledObject resources. Monitors external metrics: Kafka consumer lag, SQS queue depth, RabbitMQ queue length, custom Prometheus queries. Scales pods proportionally to the backlog. Can scale to zero when idle (HPA cannot). More responsive than HPA for queue-processing workloads |
| Prevent too many pods from being killed during maintenance | **Pod Disruption Budget (PDB)** | Limits how many pods Kubernetes can voluntarily terminate at once during node drains, cluster upgrades, or autoscaler scale-downs. Example: `minAvailable: 2` ensures at least 2 pods are always running. Without PDB, a node drain could kill all replicas of a service simultaneously |
| Control which pods can communicate with each other | **NetworkPolicy** | Firewall rules at the pod level. Default Kubernetes: all pods can talk to all pods. NetworkPolicy adds default-deny rules and explicit allowlists. "Only the API pod can reach the database pod on port 5432." Requires a network plugin that supports policies (Calico, Cilium, Weave) |
| Manage different configurations per environment (dev, staging, prod) | **Kustomize** | Template-free YAML customization. Define a base `deployment.yaml` with common config, then create overlays for each environment with patches (different replica counts, resource limits, image tags). No templating language — just YAML patches. Built into kubectl: `kubectl apply -k overlays/prod/` |
| Deploy complex third-party software packages | **Helm** | A package manager for Kubernetes. Helm Charts bundle YAML templates, default values, and documentation into versioned, reusable packages. Used for complex third-party tools (Prometheus stack, Nginx Ingress, Cilium, cert-manager). Pin chart versions for reproducibility. Use Kustomize for your own simpler applications |

### Deployment Strategies

| Strategy | Zero downtime? | Rollback speed | Resource cost | How it works | When to use |
|----------|:---:|:---:|:---:|-------------|-------------|
| **Rolling Update** | Yes | Slow (re-roll) | Low (+1 pod) | Replace pods one at a time: start new pod → wait for readiness probe to pass → remove old pod. `maxUnavailable: 0` ensures no pod is removed before its replacement is healthy. Add a `preStop` hook (5-second sleep) to drain in-flight requests before shutdown | Default strategy for most services. Use for all standard deployments |
| **Blue-Green** | Yes | Instant | High (2x resources) | Run two identical environments (Blue = current, Green = new). Deploy to Green, run smoke tests. Switch the load balancer from Blue to Green. Rollback = switch back to Blue instantly | When you need instant rollback capability for critical services. When you can afford running double infrastructure during deployment |
| **Canary** | Yes | Fast (reroute) | Low (+1 pod) | Deploy the new version to a small number of pods and route a small percentage of traffic (5%) to them via weighted routing at the ingress controller. Monitor error rates and latency. If healthy, increase to 25%, 50%, 100%. If not, route 100% back to old | When deploying risky changes (new database, major refactor). When you want data-driven confidence before full rollout |
| **Feature Flag** | Yes | Instant (toggle) | None | Deploy the code to production with the feature behind a flag set to OFF. Enable for internal users first, then 1% of users, then 10%, then 100%. If problems arise, flip the flag OFF — no deployment needed | When you want to decouple deployment from release. When you want to test with real production traffic. When you need instant kill-switch capability |

---

## Resilience

Covered in detail above in the Questions Phase 7 (Q26-Q29) with full implementation guidance per pattern.

---

## Multi-Tenancy

Covered in detail above with full isolation levels, implementation guidance, and solutions for noisy neighbor, data leakage, feature differences, and GDPR data residency.

---

## Migration Checklist

> [!todo|no-icon] Monolith → Microservices
> 1. **Extract first**: stateless, well-understood, low-risk, high K8s value
> 2. **Route traffic**: reverse proxy → old to monolith, new to K8s (strangler fig)
> 3. **Database**: shared DB initially → evolve to DB-per-service
> 4. **Communication**: events for async, API for sync between old+new
> 5. **CI/CD**: automated pipeline for every new service from day one
> 6. **Observability**: OTel in new, unified logging across old+new
> 7. **Rollback**: proxy switches back, DB changes backward-compatible
> 8. **Team**: pair on first service, show value, don't lecture

---

## CI/CD Pipeline

> [!info|no-icon] Pipeline Stages
> | Stage | Catches | Tool |
> |-------|---------|------|
> | Build | Syntax, missing dep | dotnet build, Docker |
> | Unit test | Logic bugs | xUnit |
> | Integration test | Schema mismatch, config | Testcontainers |
> | SAST | SQL injection, hardcoded secrets | SonarQube, Semgrep |
> | SCA | Known CVEs | Snyk, Dependabot |
> | Container scan | Image vulns | Trivy |
> | Breaking change | Removed field, type change | buf breaking, GraphQL diff |
> | Quality gate | All above pass | Pipeline decision |
> | Deploy staging | Integration failure | Kustomize + kubectl |
> | Deploy prod | — | Manual approval / canary |

---

## IaC

> [!note|no-icon] Tool Picker
> | Tool | Lang | Multi-cloud | Best for |
> |------|------|:-----------:|---------|
> | Terraform | HCL | Yes | Cloud infra, agnostic |
> | Pulumi | Python/TS/Go/C# | Yes | Complex logic |
> | CloudFormation | YAML | AWS only | Pure AWS |
> | CDK | Python/TS | AWS only | AWS + real language |
> | Ansible | YAML | Yes | Config mgmt, not infra lifecycle |

---

## AWS ↔ Azure

> [!abstract|no-icon] Service Map
> | Concept | AWS | Azure |
> |---------|-----|-------|
> | Kubernetes | EKS | AKS |
> | Registry | ECR | ACR |
> | Object storage | S3 | Blob Storage |
> | Relational DB | RDS | Azure SQL |
> | Cache | ElastiCache | Azure Cache for Redis |
> | Queue | SQS | Azure Queue |
> | Streaming | MSK | Event Hubs |
> | Secrets | Secrets Manager | Key Vault |
> | DNS | Route 53 | Azure DNS |
> | CDN | CloudFront | Azure CDN |
> | IAM | IAM + IRSA | Entra + Workload Identity |
> | IaC | CFN / Terraform | Bicep / Terraform |
> | Monitoring | CloudWatch + X-Ray | App Insights |
> | LB (L7) | ALB | App Gateway |
> | Serverless | Lambda | Azure Functions |

---

## Numbers

> [!tip|no-icon] Latency & Throughput
> | Op | Time | | Resource | Throughput |
> |----|------|-|----------|-----------|
> | Redis GET | 0.5 ms | | Redis | 100K ops/s |
> | DB query | 1-5 ms | | Postgres | 5-20K qps |
> | Same-region RTT | 0.5 ms | | Kafka partition | ~10K msg/s |
> | Cross-region RTT | 50-150 ms | | Kafka cluster | 1M+ msg/s |
> | S3 GET | 50-200 ms | | Web server | 1-10K rps |
>
> **Storage** = `writes/day * size * retention` | **Instances** = `RPS / per_instance` + 30% | **Cache** target 90-99% hit

---

## Anti-Patterns

| Anti-pattern | What it looks like | Why it's bad | Concrete example | How to fix |
|-------------|-------------------|-------------|-----------------|------------|
| **Distributed monolith** | Services are deployed separately but can't be released independently. Deploying Service A always requires deploying Service B at the same time | You have all the complexity of microservices (network calls, distributed debugging, deployment coordination) with none of the benefits (independent releases, independent scaling) | Service A and Service B share a data model library. Changing a field in the shared library requires rebuilding, testing, and deploying both services simultaneously. If either deployment fails, both must be rolled back | Remove shared data model libraries — each service owns its own models. Replace synchronous call chains with asynchronous events where the caller doesn't need an immediate response. If two services always change together, merge them into one service |
| **Shared database** | Two or more services read from and write to the same database tables directly, bypassing each other's APIs | A schema change made by one service breaks the other service's queries. You can't scale, migrate, or tune the database for one service without impacting all services sharing it. Coupling at the data layer defeats the purpose of separate services | User Service adds a `middle_name` column to the `users` table and changes an index. Order Service, which also queries `users` directly, slows down because its queries used the old index. Neither team knew about the dependency until production | Each service gets its own database. If Order Service needs user data, it either calls User Service via API (synchronous), or subscribes to `UserUpdated` events from Kafka and maintains its own local copy of the user fields it needs (eventual consistency) |
| **Chatty services** | Rendering one page or completing one operation requires 10-15 sequential synchronous calls between services | Latency accumulates: 10 calls at 50ms each = 500ms minimum. Any one service being slow makes everything slow. Failure probability increases with each call: 99% uptime per service × 10 services = 90% effective uptime | The product detail page calls User Service, then Product Service, then Pricing Service, then Inventory Service, then Review Service, then Recommendation Service — all sequentially before responding to the user | Use GraphQL to fetch from multiple services in one request (parallel resolution). Use the Backend-for-Frontend (BFF) pattern to aggregate server-side. Pre-compute combined views using CQRS read models. Merge services that are always called together — they may not be truly separate domains |
| **No API versioning** | API fields are renamed or removed without warning. Consumers discover breaking changes through runtime errors in production | Consumers can't trust the API. Every deployment is a potential breaking change. Teams become afraid to evolve APIs because they don't know who depends on what | Profile Service renames `name` to `full_name`. Five consuming services now get null for `name` and display "Hello, null" to users. The change wasn't caught until customers reported the issue | Use additive-only changes: add new fields freely, mark old fields as deprecated, remove only after confirming all consumers have migrated. Run backward compatibility checks in CI: `buf breaking` for gRPC protobuf, schema comparison for GraphQL, OpenAPI diff for REST APIs |
| **God service** | One service handles too many unrelated responsibilities. It has hundreds of endpoints, a massive codebase, and every team needs to modify it for their features | Every team is blocked by the same service and its deployment queue. Merge conflicts are constant. A bug in the billing logic can crash the user registration flow because they run in the same process. The codebase is too large for anyone to fully understand | A "Platform Service" handles user management, billing, notifications, reporting, admin panel, and integrations — 200+ endpoints, 50,000 lines of code, owned by nobody and modified by everybody. Three teams edit the same files every sprint | Decompose using Domain-Driven Design bounded contexts. Identify distinct business domains (User Management, Billing, Notifications) and extract each into its own service with its own database and deployment pipeline. Start with the domain that has the clearest boundary and changes most independently |
| **Missing timeouts** | External calls (HTTP, gRPC, database) have no timeout configured. If a downstream service hangs, the calling service's threads are held indefinitely | One slow or hung downstream cascades to all callers. Threads and connections are held indefinitely, exhausting pools. Eventually your entire system becomes unresponsive because all threads are waiting on one dead service | Order Service calls Payment Gateway with no timeout. The payment gateway has a network issue and never responds. Order Service's 200 threads are all blocked waiting. No new orders can be processed. Users see errors on the frontend. The issue was in the payment gateway, but your system is the one that's down | Set a timeout on every external call: 2 seconds for internal service-to-service calls, 5 seconds for external third-party APIs. Combine with retry (for transient failures) and circuit breaker (to stop calling after repeated failures). In .NET: `HttpClient.Timeout = TimeSpan.FromSeconds(2)`. In Java: `RestTemplate.setReadTimeout(2000)` |
| **Liveness probe checks database** | The Kubernetes liveness probe makes a database query to verify health. If the database has any latency spike, all pods fail the liveness check and Kubernetes kills them simultaneously | One 5-second database blip (during a failover, index rebuild, or connection pool exhaustion) causes Kubernetes to kill all pods at once. The system goes from "database is slow" to "everything is completely down" — a much worse outcome than the original issue | Database has a 5-second latency spike during an automatic failover. Liveness probes on all 20 pods time out. Kubernetes kills all 20 pods and starts 20 new ones. The 20 new pods all connect to the database simultaneously during startup, overwhelming it further. System is fully down for minutes instead of having slow queries for 5 seconds | Liveness probe should check only if the application process is responsive: "Can you respond to a simple HTTP request?" Never check database, cache, or external service health in liveness. Put dependency checks in the readiness probe instead — a failed readiness probe removes the pod from the load balancer without killing it, allowing it to recover when the database comes back |
| **Over-engineering on day one** | Building infrastructure for 10 million users when you have 100. Microservices for a 3-person team. Kubernetes for a single-container application | Months spent building infrastructure instead of features. Complexity slows development and debugging. Operational costs far exceed what the traffic requires. Every feature takes 5x longer because of inter-service coordination, distributed tracing setup, and infrastructure maintenance | A 3-person startup builds 12 microservices, a Kubernetes cluster, Kafka, Redis, Elasticsearch, and a service mesh for a product with 50 beta users. Every feature requires changes across 3 services. The Kafka cluster costs $500/month and processes 100 messages per day. The team spends more time on infrastructure than on the product | Start with a modular monolith: one deployable application with clear internal module boundaries that can be split later. Use a managed database (RDS, Cloud SQL). Use SQS if you need async processing. Deploy as a single container on a simple platform (ECS, App Runner, or a single Kubernetes Deployment). Add complexity only when you have concrete data showing a bottleneck. Design for 10x current load, plan for 100x, but build for 1x |

---

## Scenario Templates

> [!example|no-icon] SaaS Multi-Tenant Platform
> ```
> [Client] → [CDN] → [LB] → [API GW (auth + tenant routing)]
>                                    |
>                  ┌─────────────────┼─────────────────┐
>                  ↓                 ↓                  ↓
>          [Service A]       [Service B]        [Service C]
>                  ↓                 ↓                  ↓
>          [Tenant DB]      [Redis Cache]       [Kafka → Workers]
> ```
> Tenant isolation: shared DB + tenant_id (start) → DB-per-tenant (evolve). Rate limit per tenant. Feature flags per tenant. GDPR: region-specific deploy.

> [!example|no-icon] Monolith → K8s Migration
> ```
> Phase 1:  [Users] → [Proxy] → [Monolith] | [New K8s Svc] → [Shared DB]
> Phase 2:  [Users] → [API GW] → [Svc A][Svc B][Svc C] → [DB A][DB B][DB C]
>                                         ↕ [Kafka]
> ```
> Strangler fig. Stateless first. Shared DB → DB-per-service. CI/CD + OTel from day one.

> [!example|no-icon] Real-Time Dashboard
> ```
> [Sources] → [Ingestion] → [Kafka/Redis Streams]
>                                  |
>                      ┌───────────┼───────────┐
>                      ↓           ↓           ↓
>               [RT Consumer] [Batch Writer] [Alerts]
>                [Redis]       [SQL/TSDB]    [Notify]
>                [WebSocket]   [REST API]
>                      └───────────┘ → [Dashboard]
> ```
> Hot path (Redis) vs cold path (SQL). Backpressure via queue. Pre-aggregate in consumers.

> [!example|no-icon] Notification / Automation
> ```
> [Triggers: user action, cron, webhook, event]
>       → [Kafka] → [Router] → [Email|Push|SMS] → [Provider]
>                                     ↓
>                              [Delivery DB + DLQ]
> ```
> Priority queues (urgent vs marketing). Rate limit per user. Templates with tenant branding. Retry + DLQ.

> [!example|no-icon] Auth & Authorization
> ```
> [Client] → [API GW: JWT validation] → [Service: RBAC + resource check]
>                   ↑                              ↑
>         [IdP: OAuth2+OIDC]            [Policy engine: tenant-scoped]
> ```
> PKCE for SPAs. JWT: 15min access + 7d refresh. Service-to-service: mTLS or pod identity. tenant_id on every query.

> [!example|no-icon] Saga (Order Flow)
> ```
> [Order Svc] → OrderCreated → [Payment Svc] → PaymentCharged
>     → [Inventory Svc] → StockReserved → [Shipping] → [Notification]
>     Failure at any step → compensating events roll back previous steps
> ```
> Saga over 2PC. Choreography (simple) or orchestration (complex). Every step idempotent. Outbox for guaranteed delivery.

> [!example|no-icon] CI/CD Pipeline
> ```
> [Git Push] → [Build + Test + Security Scan] → [Quality Gate]
>     → [Registry] → [Dev(auto)] → [Staging(smoke)] → [Prod(approval)]
> ```
> Shared workflow templates. Breaking change detection. DORA metrics. Feature env cleanup on branch delete.

> [!example|no-icon] File Upload Pipeline
> ```
> [Client] → [API: pre-signed URL] → [Direct upload to S3]
>     → [Event] → [Scan|Thumbnail|Metadata workers] → [DB: status=ready] → [CDN]
> ```
> Never proxy large files. Chunked upload with resume. Async processing via workers.

> [!example|no-icon] Search Platform
> ```
> [Data changes] → [CDC/Events] → [Indexer] → [Elasticsearch]
> [Client] → [API] → [Search Svc] → [ES: query+filter+aggregate]
>                                    [Redis: autocomplete, popular queries]
> ```
> Eventual consistency (index lags). Full re-index nightly + incremental. Edge-ngram for autocomplete.

> [!example|no-icon] URL Shortener
> ```
> [Client] → [LB] → [API] → Write:[SQL] | Read:[Redis cache] | Analytics:[Kafka→DB]
> ```
> 100:1 read/write. Base62 ID. TTL expiration. Every redirect → Kafka event → aggregate clicks.

---

## Phrases That Show Depth

> [!quote|no-icon] Replace generic with specific
> | Don't say | Say instead |
> |-----------|-------------|
> | "Use a database" | "PostgreSQL for ACID, but MongoDB if schema varies" |
> | "Add a cache" | "Cache-aside with Redis, TTL 60s, event-based invalidation" |
> | "Use a queue" | "Kafka for fan-out, partition by entity ID for ordering" |
> | "Scale it" | "HPA at 75% CPU for API, KEDA on queue depth for workers" |
> | "Make it secure" | "JWT at gateway, RBAC per service, tenant_id on every query, mTLS inside cluster" |
> | "Monitor it" | "OTel traces + structured logs correlated by trace ID, RED metrics, rate-based alerts" |

---

## Possible Interview Scenarios — What Niclas Might Ask

> [!danger|no-icon] Lime-Specific (Most Likely)
> These align directly with Lime's product (help desk, sales, marketing automation) and their K8s+AWS migration.
>
> | # | Scenario | Why they'd ask | Key components |
> |---|----------|---------------|----------------|
> | 1 | **"Design our platform migration from monolith to K8s on AWS"** | Their #1 initiative — they want to see if you've done this | Strangler fig, reverse proxy, shared DB → DB-per-service, CI/CD from day one, OTel |
> | 2 | **"Design a multi-tenant SaaS help desk system"** | Their core product | Tenant isolation (shared DB + tenant_id), ticket routing, assignment engine, SLA tracking, notification per channel |
> | 3 | **"Design a marketing automation pipeline"** | Part of their product suite | Event triggers, audience segmentation, campaign scheduler, template engine, delivery tracking, A/B testing |
> | 4 | **"Design how we'd handle customer communication across channels"** | Help desk + sales = omnichannel | Unified inbox, channel adapters (email, chat, phone), conversation threading, routing rules, agent assignment |
> | 5 | **"How would you set up the infrastructure for a new service on AWS?"** | They're building from scratch on AWS | EKS cluster, Terraform, CI/CD pipeline, secrets management, observability, networking |

> [!warning|no-icon] Classic System Design (Likely)
> Standard questions that test architectural thinking. Any of these could come up.
>
> | # | Scenario | Core architecture |
> |---|----------|-------------------|
> | 6 | **"Design a notification system"** | Event bus → router → channel adapters (email/push/SMS) → delivery tracking + DLQ + rate limiting |
> | 7 | **"Design a real-time dashboard"** | Data sources → Kafka/Streams → hot path (Redis+WebSocket) + cold path (SQL+REST) |
> | 8 | **"Design a task/ticket management system"** | CRUD API + state machine (open→assigned→in-progress→resolved) + assignment rules + SLA timer + search |
> | 9 | **"Design an API gateway for microservices"** | Auth (JWT), rate limiting, routing, protocol translation, aggregation, observability |
> | 10 | **"Design a chat system"** | WebSocket connections, message persistence, presence (online/offline), delivery receipts, fan-out to group members |
> | 11 | **"Design a job scheduler / workflow engine"** | Cron-based triggers, DAG execution, retry policies, state persistence, distributed locking, dead letter |
> | 12 | **"Design a rate limiter"** | Token bucket or sliding window, Redis for distributed state, per-tenant and per-endpoint rules, 429 responses |
> | 13 | **"Design a URL shortener"** | Base62 ID, Redis cache (read-heavy), SQL persistence, analytics via Kafka, TTL expiration |
> | 14 | **"Design a file storage service"** | Pre-signed URLs → S3 direct upload → event → async workers (scan, thumbnail, metadata) → CDN |
> | 15 | **"Design a search system"** | CDC/events → indexer workers → Elasticsearch, autocomplete via Redis, eventual consistency |

> [!tip|no-icon] Architecture Discussion Questions (Very Likely for 1-hour format)
> Niclas might not give a full "design X" prompt. He might ask open-ended architecture questions and expect you to draw while explaining.
>
> | # | Question | What to draw / discuss |
> |---|----------|----------------------|
> | 16 | **"How would you split a monolith into services?"** | Bounded contexts, strangler fig, database strategy, event-driven communication |
> | 17 | **"How do you handle data consistency across microservices?"** | Eventual consistency, saga, outbox pattern, CQRS — draw the event flow |
> | 18 | **"Walk me through a request from browser to database"** | CDN → LB → ingress → API gateway → service → cache → DB, with auth and observability at each step |
> | 19 | **"How do you design for high availability?"** | Multi-AZ, health checks, circuit breakers, graceful degradation, auto-scaling, PDB |
> | 20 | **"How do you handle authentication in a microservices setup?"** | OAuth2+OIDC at gateway, JWT propagation, service-to-service mTLS, tenant-scoped claims |
> | 21 | **"How do you approach CI/CD for 50+ services?"** | Shared workflow templates, quality gates, breaking change detection, feature envs, DORA metrics |
> | 22 | **"How do you monitor and debug a distributed system?"** | OTel → traces (Tempo) + logs (Loki) + metrics (Prometheus) → Grafana, trace ID correlation |
> | 23 | **"What's your approach to database design in microservices?"** | DB-per-service, polyglot persistence (SQL vs Mongo vs Redis), eventual consistency via events |
> | 24 | **"How do you handle secrets and security in K8s?"** | Key Vault CSI, pod identity (IRSA), network policies (default deny), RBAC, image scanning |
> | 25 | **"When would you choose sync vs async communication?"** | Sync (gRPC) when caller needs response now. Async (Kafka) when fire-and-forget, fan-out, or decoupling |
> | 26 | **"How do you handle a traffic spike?"** | Queue buffers requests, HPA/KEDA scales pods, cache absorbs reads, circuit breaker protects downstream |
> | 27 | **"What trade-offs do you consider when choosing between SQL and NoSQL?"** | ACID vs flexibility, joins vs nesting, schema rigidity vs evolution, vertical vs horizontal scaling |
> | 28 | **"How do you handle multi-tenancy?"** | Tenant_id column (start) vs DB-per-tenant (compliance). Rate limit per tenant. Feature flags. GDPR residency. |
> | 29 | **"How would you design a zero-downtime deployment?"** | Rolling update (maxUnavailable:0), readiness probes, preStop hook, PDB, feature flags |
> | 30 | **"What would you do differently if you had to rebuild your current system from scratch?"** | Modular monolith first, split when boundaries are clear. OTel from day one. Testcontainers from day one. |

---

---

## Glossary — Abbreviations Used in This Document

### Core Concepts

| Abbreviation | Full Name | What it is / How it works |
|---|---|---|
| **API** | Application Programming Interface | A contract that defines how software components talk to each other. In web systems, usually means HTTP endpoints that accept requests and return JSON responses. REST APIs use standard HTTP methods (GET, POST, PUT, DELETE) |
| **REST** | Representational State Transfer | An API style where each URL represents a resource (e.g., `/users/123`). Uses standard HTTP methods and status codes. Stateless — each request contains all needed information. Easy to cache with HTTP headers |
| **GraphQL** | Graph Query Language | An API style where the client writes a query specifying exactly which fields it wants, and the server returns only those fields. Single endpoint instead of many REST endpoints. Eliminates over-fetching and under-fetching |
| **gRPC** | Google Remote Procedure Call | A framework for calling functions on a remote service as if they were local. Uses binary Protocol Buffers (protobuf) instead of JSON — smaller payloads, faster serialization. Runs over HTTP/2 for multiplexing. Generates typed client code from `.proto` definition files |
| **CRUD** | Create, Read, Update, Delete | The four basic database operations. A "CRUD API" is a simple API that just creates, reads, updates, and deletes records with no complex business logic |
| **ACID** | Atomicity, Consistency, Isolation, Durability | Four guarantees of a reliable database transaction. **Atomicity**: all operations succeed or all fail (no partial writes). **Consistency**: data stays valid after the transaction. **Isolation**: concurrent transactions don't interfere. **Durability**: committed data survives a crash |

### Architecture Patterns

| Abbreviation | Full Name | What it is / How it works |
|---|---|---|
| **CQRS** | Command Query Responsibility Segregation | A pattern that uses separate models for reading and writing data. The write side (commands) goes through domain logic to a primary database. The read side (queries) reads from a denormalized view optimized for fast queries. Use when read and write patterns are very different — e.g., dashboard reads 100x more than it writes |
| **CDC** | Change Data Capture | A technique that captures every change (insert, update, delete) in a database and streams it as an event. Tools like Debezium read the database's transaction log and publish changes to Kafka. Use to keep a search index or cache in sync with the database without modifying application code |
| **DDD** | Domain-Driven Design | A software design approach that structures code around business domains. Each domain gets a "bounded context" — a clear boundary with its own data, language, and rules. In microservices, each bounded context often maps to one service |
| **BFF** | Backend for Frontend | A pattern where each client type (web, mobile, admin) gets its own dedicated backend API that returns exactly the data that client needs. Avoids a "one size fits none" API. Alternative to GraphQL for solving the over-fetching problem |
| **DRY** | Don't Repeat Yourself | A principle: every piece of knowledge should have a single source of truth. In the context of CI/CD, it means shared pipeline templates so 60 services don't each have their own copy of the build logic |

### Infrastructure & Scaling

| Abbreviation | Full Name | What it is / How it works |
|---|---|---|
| **CDN** | Content Delivery Network | A global network of servers that caches static content (images, CSS, JavaScript) at locations close to users. When a user in Europe requests an image, the CDN serves it from a European server instead of the origin in the US. Reduces latency and offloads the origin server. Examples: CloudFront, CloudFlare, Akamai |
| **LB** | Load Balancer | A component that distributes incoming requests across multiple server instances. If one server is down, the LB routes to healthy ones. L4 (Layer 4) load balancers route by IP/port. L7 (Layer 7) load balancers can inspect HTTP content and route by URL path, headers, or cookies. Examples: Nginx, HAProxy, AWS ALB |
| **ALB** | Application Load Balancer | AWS's Layer 7 load balancer. Routes HTTP requests by URL path, host header, or query parameters. Supports WebSocket and gRPC. Use for web applications and APIs |
| **DNS** | Domain Name System | The system that translates domain names (e.g., `api.example.com`) to IP addresses. GeoDNS returns different IPs based on the user's geographic location, routing them to the nearest data center |
| **HPA** | Horizontal Pod Autoscaler | A Kubernetes feature that automatically adds or removes pod instances based on CPU usage, memory usage, or custom metrics. Example: if CPU exceeds 75% for 5 minutes, add another pod. If CPU drops below 30%, remove a pod |
| **KEDA** | Kubernetes Event-Driven Autoscaling | An extension to Kubernetes that scales based on external metrics like message queue depth. Example: if there are 1000 messages in the Kafka topic, spin up 10 worker pods. If the queue is empty, scale to zero pods (saving cost) |
| **PDB** | Pod Disruption Budget | A Kubernetes setting that limits how many pods can be taken down simultaneously during maintenance (node upgrades, drains). Example: `minAvailable: 2` ensures at least 2 pods are always running even during a node drain |
| **CSI** | Container Storage Interface | A standard interface for mounting external storage into containers. In the context of secrets: the CSI Secrets Store Driver mounts secrets from a vault (like AWS Secrets Manager) as files inside the pod, so the application reads secrets from a file path instead of environment variables |
| **TTL** | Time to Live | An expiration time on a cached value or database record. After the TTL expires, the value is automatically deleted or refreshed. Example: cache a user profile with TTL of 5 minutes — after 5 minutes, the next request fetches fresh data from the database |
| **AZ** | Availability Zone | A physically separate data center within a cloud region. Running in multiple AZs means if one data center loses power or network, the system continues in the other AZs. Example: AWS `us-east-1a`, `us-east-1b`, `us-east-1c` are three AZs in the `us-east-1` region |
| **IaC** | Infrastructure as Code | Managing cloud infrastructure (servers, databases, networks) through code files instead of clicking in a web console. Benefits: version control, code review, reproducibility. Tools: Terraform, Pulumi, CloudFormation |

### Security

| Abbreviation | Full Name | What it is / How it works |
|---|---|---|
| **JWT** | JSON Web Token | A signed token containing user claims (user ID, roles, tenant ID) encoded as JSON. The API gateway or service verifies the signature using a public key — no database lookup needed. Stateless authentication: the token itself contains everything needed to identify and authorize the user |
| **OIDC** | OpenID Connect | A layer on top of OAuth2 that adds user identity. OAuth2 alone only gives authorization (access tokens). OIDC adds an ID token that contains who the user is (name, email). Used for "Login with Google" flows |
| **PKCE** | Proof Key for Code Exchange | A security extension for OAuth2 that protects against authorization code interception attacks. The client generates a random secret (code_verifier), hashes it, and sends the hash with the auth request. The server verifies the original secret when exchanging the code for tokens. Required for SPAs and mobile apps because they can't safely store a client_secret |
| **RBAC** | Role-Based Access Control | An authorization model where users are assigned roles (admin, editor, viewer), and each role has a set of permissions. The system checks the user's role before allowing an action. Example: only users with the "admin" role can delete other users |
| **mTLS** | Mutual Transport Layer Security | A two-way TLS authentication where both the client and server verify each other's certificates. Normal TLS only verifies the server. mTLS ensures that only authorized services can call each other — used for service-to-service communication inside a cluster |
| **IRSA** | IAM Roles for Service Accounts | An AWS feature that lets a Kubernetes pod assume an AWS IAM role without storing any credentials. The pod's Kubernetes service account is federated with AWS IAM. The pod can access AWS services (S3, RDS, Secrets Manager) using temporary credentials that rotate automatically |
| **HMAC** | Hash-Based Message Authentication Code | A technique to verify that a message hasn't been tampered with. The sender computes a hash of the message using a shared secret key and attaches it. The receiver recomputes the hash and compares. Used for webhook signature verification — confirms the webhook really came from the expected sender |
| **GDPR** | General Data Protection Regulation | EU regulation requiring data residency (personal data stored in the EU), right to deletion, consent management, and audit trails. Affects architecture: may need multi-region deployment with data pinned to specific regions |
| **SLA** | Service Level Agreement | A commitment to a certain level of availability or performance. Example: 99.9% SLA means the system can be down for at most 8.7 hours per year. Drives architecture decisions about redundancy, failover, and monitoring |
| **CVE** | Common Vulnerabilities and Exposures | A publicly known security vulnerability with a unique ID (e.g., CVE-2021-44228 is Log4Shell). Dependency scanning tools check your packages against CVE databases and fail the build if a critical vulnerability is found |
| **SAST** | Static Application Security Testing | Analyzing source code for security vulnerabilities without running it. Finds SQL injection patterns, hardcoded secrets, insecure deserialization. Tools: SonarQube, Semgrep, CodeQL |
| **SCA** | Software Composition Analysis | Scanning your project's dependencies (npm packages, NuGet packages, Python packages) against known vulnerability databases. Finds vulnerable library versions. Tools: Snyk, Dependabot, OWASP Dependency-Check |

### Messaging & Events

| Abbreviation | Full Name                   | What it is / How it works                                                                                                                                                                                                                                                                     |
| ------------ | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **DLQ**      | Dead Letter Queue           | A separate queue where messages that failed processing after N retries are moved. Instead of retrying forever (blocking the queue) or dropping the message (losing data), the failed message is parked in the DLQ for inspection and manual replay. Every production async system needs one   |
| **SSE**      | Server-Sent Events          | A simple protocol for one-way server-to-client push over HTTP. The server holds the connection open and sends events as they happen. The browser auto-reconnects if the connection drops. Simpler than WebSocket when you only need server → client communication (dashboards, notifications) |
| **SNS**      | Simple Notification Service | An AWS managed pub/sub service. You publish a message to a topic, and SNS delivers it to all subscribers (SQS queues, Lambda functions, HTTP endpoints). Use SNS + SQS together for fan-out: one event published to SNS, multiple SQS queues each get a copy                                  |
| **SQS**      | Simple Queue Service        | An AWS managed message queue. Zero operational burden — no clusters to manage, auto-scales, built-in DLQ, pay per message. Use for simple async processing where you don't need Kafka's replay, ordering, or multi-consumer features                                                          |
| **FIFO**     | First In, First Out         | A queue ordering guarantee — messages are processed in the exact order they were sent. Amazon SQS offers FIFO queues as an option. Kafka guarantees FIFO ordering within a single partition                                                                                                   |

### Observability

| Abbreviation | Full Name | What it is / How it works |
|---|---|---|
| **OTel** | OpenTelemetry | A vendor-neutral open standard for instrumenting applications to produce traces, metrics, and logs. You add the OTel SDK to your service, and it automatically captures HTTP requests, database calls, and message processing as spans in a trace. Data is exported to backends like Jaeger, Tempo, Prometheus, or Datadog |
| **ELK** | Elasticsearch + Logstash + Kibana | A log aggregation stack. Logstash collects and transforms logs, Elasticsearch stores and indexes them (full-text searchable), Kibana visualizes them. Alternative: Grafana Loki (cheaper — indexes labels only, not full text) |
| **DORA** | DevOps Research and Assessment | Four metrics that measure software delivery performance: **Deployment Frequency** (how often you deploy), **Lead Time for Changes** (commit → production), **Change Failure Rate** (% of deploys that cause incidents), **Time to Restore** (incident → resolution). Used to benchmark and improve engineering health |
| **RPS** | Requests Per Second | The number of HTTP requests hitting your API per second. Key metric for capacity planning: if each instance handles 500 RPS and you expect 2000 RPS, you need at least 4 instances + headroom |

### Pipeline & Development

| Abbreviation | Full Name | What it is / How it works |
|---|---|---|
| **CI** | Continuous Integration | Automatically building, testing, and scanning code on every push or pull request. The pipeline runs unit tests, integration tests, security scans, and produces a build artifact (container image). Catches bugs before they reach production |
| **CD** | Continuous Delivery / Continuous Deployment | Continuous Delivery: automatically deploying to staging after CI passes, with a manual approval gate before production. Continuous Deployment: automatically deploying to production without manual approval — requires high confidence in tests |
| **ORM** | Object-Relational Mapping | A library that maps database tables to programming language objects (classes). Entity Framework (.NET), Hibernate (Java), SQLAlchemy (Python). Generates SQL from code. Convenient but can produce slow queries — use raw SQL (Dapper) for performance-critical reads |
| **SDK** | Software Development Kit | A library or package that provides pre-built functions for interacting with a service. Example: the AWS SDK lets you call S3, SQS, and RDS from your code without writing raw HTTP requests |
| **CDK** | Cloud Development Kit | AWS CDK: define cloud infrastructure using real programming languages (TypeScript, Python, Java) instead of YAML. The CDK generates CloudFormation templates under the hood |
| **HCL** | HashiCorp Configuration Language | The declarative language used by Terraform to define infrastructure. Looks like JSON but simpler and more readable. Example: `resource "aws_s3_bucket" "my_bucket" { bucket = "my-app-data" }` |
| **CFN** | CloudFormation | AWS's infrastructure-as-code service. Define infrastructure in YAML or JSON templates. AWS-only (no multi-cloud). Free to use — you pay for the resources it creates |

### Networking & Protocols

| Abbreviation | Full Name | What it is / How it works |
|---|---|---|
| **TLS** | Transport Layer Security | Encrypts data in transit between client and server (HTTPS). Prevents eavesdropping and tampering. A certificate proves the server's identity. Let's Encrypt provides free auto-renewing certificates |
| **DNS** | Domain Name System | Translates domain names (`api.example.com`) to IP addresses. The first step of every web request. GeoDNS returns different IPs based on user location for multi-region routing |
| **IAM** | Identity and Access Management | Cloud provider's system for controlling who can do what. AWS IAM defines users, roles, and policies. Example: "This role can read from S3 bucket X and write to SQS queue Y but nothing else" (principle of least privilege) |
| **WAF** | Web Application Firewall | Inspects incoming HTTP requests and blocks common attacks: SQL injection, cross-site scripting (XSS), request flooding. Sits at the edge (CloudFlare, AWS WAF) before traffic reaches your application |
| **SPA** | Single Page Application | A web application that loads a single HTML page and dynamically updates content via JavaScript (React, Vue, Angular). The entire frontend runs in the browser, calling APIs for data. Relevant for auth: SPAs can't safely store a client_secret, so they use PKCE |
| **RTT** | Round-Trip Time | The time for a network packet to travel from source to destination and back. Same-region RTT: ~0.5ms. Cross-region RTT: 50-150ms. Cross-continent RTT: 100-300ms. Directly impacts perceived latency |
| **CPU** | Central Processing Unit | The processor that executes your code. In the context of scaling: when CPU usage is high, you either optimize code, add more instances (horizontal scaling), or use a bigger instance (vertical scaling) |
| **SMS** | Short Message Service | Text messages sent to mobile phones. In system design, one of the notification channels (alongside email and push notifications). Typically sent via third-party providers (Twilio, AWS SNS) |

### Data & Storage

| Abbreviation | Full Name | What it is / How it works |
|---|---|---|
| **DB** | Database | A system for storing, organizing, and querying data. Relational databases (PostgreSQL, MySQL) store data in tables. Document databases (MongoDB) store JSON-like documents. Key-value stores (Redis) store simple key-value pairs |
| **BSON** | Binary JSON | MongoDB's binary representation of JSON documents. Supports additional types that JSON doesn't (dates, binary data, ObjectId). More efficient to parse and store than text JSON |
| **KMS** | Key Management Service | A cloud service for creating, storing, and managing encryption keys. AWS KMS, Azure Key Vault, Google Cloud KMS. You never handle raw keys in your code — the KMS encrypts and decrypts data using keys it manages. Used for database encryption at rest and field-level encryption |
| **TDE** | Transparent Data Encryption | Database-level encryption that encrypts data files on disk automatically without application code changes. All major managed databases support it (RDS, Azure SQL, Cloud SQL). Protects against physical disk theft or unauthorized backup access |
| **MSK** | Managed Streaming for Apache Kafka | AWS's fully managed Kafka service. AWS handles broker provisioning, patching, and cluster scaling. You configure topics, partitions, and retention. Same Kafka API as self-hosted, but with reduced operational burden |
| **ML** | Machine Learning | Algorithms that learn patterns from data to make predictions. In system design context: ML models are typically trained offline (batch pipeline) and served via a prediction API. Cache predictions in Redis for fast serving |
| **OLTP** | Online Transaction Processing | Database workloads focused on many small, fast transactions (reads and writes). Example: an e-commerce checkout, a ticket creation. Contrasted with OLAP (Online Analytical Processing) which focuses on complex queries over large datasets for reporting |

### Security (additional)

| Abbreviation | Full Name | What it is / How it works |
|---|---|---|
| **OWASP** | Open Web Application Security Project | A nonprofit that publishes the OWASP Top 10 — the 10 most critical web application security risks (injection, broken auth, XSS, CSRF, etc.). Pen-testing firms and compliance frameworks reference it. If your app is vulnerable to something in the Top 10, it's a serious gap |
| **PCI** | Payment Card Industry (PCI DSS = Data Security Standard) | Compliance requirements for handling credit card data. Requires encryption of cardholder data, network segmentation, access control, audit logging, and regular vulnerability scanning. Affects architecture: card data may need a separate isolated service |
| **CSRF** | Cross-Site Request Forgery | An attack where a malicious website tricks a user's browser into making an unintended request to your site (using the user's cookies). Prevented with anti-forgery tokens and `SameSite` cookie attribute |
| **OPA** | Open Policy Agent | A general-purpose policy engine. You write authorization rules in Rego language, and OPA evaluates them at runtime. Used when RBAC is too simple — e.g., "users can edit documents only if they're in the same department AND the document isn't locked" |
| **UI** | User Interface | The visual part of the application that users interact with (web page, mobile app, admin panel). In system design, UI = the client that calls your API |
| **ID** | Identifier | A unique value that identifies a record (user ID, order ID, tenant ID). Can be auto-increment integers (simple, sequential), UUIDs (globally unique, no coordination needed), or Snowflake IDs (time-sortable, unique across nodes) |

### Cloud Services

| Abbreviation | Full Name | What it is |
|---|---|---|
| **EKS** | Elastic Kubernetes Service | AWS's managed Kubernetes. AWS handles the control plane; you manage worker nodes and deployments |
| **AKS** | Azure Kubernetes Service | Azure's managed Kubernetes. Same concept as EKS but on Azure |
| **ECR** | Elastic Container Registry | AWS's Docker image registry. You push container images here; Kubernetes pulls from here |
| **ACR** | Azure Container Registry | Azure's Docker image registry |
| **RDS** | Relational Database Service | AWS's managed relational database. Supports PostgreSQL, MySQL, MS SQL, Oracle. Handles backups, patching, replication, failover |
| **GCS** | Google Cloud Storage | Google Cloud's object storage (equivalent to AWS S3 or Azure Blob Storage) |
| **GCP** | Google Cloud Platform | Google's cloud computing platform. Third major cloud after AWS and Azure. Services include GKE (Kubernetes), Cloud SQL (databases), GCS (storage), Pub/Sub (messaging) |


*[[00-dashboard|Back to Dashboard]]*
