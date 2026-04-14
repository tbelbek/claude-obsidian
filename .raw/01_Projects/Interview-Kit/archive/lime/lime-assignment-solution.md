---
tags:
  - interview-kit
  - interview-kit/lime
up: "[[company-lime]]"
---

*[[company-lime]]*

# Email Marketing SaaS — System Design Solution

---

## Step 1: Clarify Requirements (ask these first)

### What I know from the assignment

- Multi-tenant SaaS — multiple customers share the system
- Users: authenticated tenant users + external partners via public API
- Core features: templates, campaigns, recipient lists, send/schedule, image upload, statistics
- External SMTP provider handles actual sending + tracking (we receive webhooks)
- Scale: millions of recipients per campaign, 100M+ interaction events
- Future: other channels beyond email (SMS, push, etc.)

### Questions I would ask Niclas

1. "How many tenants? Tens, hundreds, thousands?" → drives tenant isolation strategy
2. "What's the peak send rate? 1M emails in 1 hour or spread over days?" → drives queue sizing
3. "Do users need real-time statistics or is a few minutes delay OK?" → drives stats architecture
4. "What's the availability target? Can we have maintenance windows?" → drives redundancy
5. "Is there an existing system or is this greenfield?" → drives migration approach
6. "How many team members will develop this?" → drives monolith vs microservices

### My assumptions (if "you decide")

- Hundreds of tenants, some sending millions, most sending thousands
- Peak: 10M emails/hour for the largest campaigns
- Statistics: near-real-time (1-2 minute delay acceptable for dashboards)
- 99.9% availability (no scheduled downtime)
- Greenfield — new system
- Multiple teams — microservices appropriate

---

## Step 2: High-Level Architecture (the main diagram)

```
                           ┌──────────────────────────────────────────────┐
                           │              EXTERNAL                        │
                           │                                              │
  [Tenant Users]           │   [External SMTP Provider]                   │
  [Partner API]            │     (SendGrid/Mailgun/SES)                   │
       │                   │        │              │                      │
       │                   │   sends emails    reports back               │
       │                   │        │         (webhooks)                  │
       │                   └────────│──────────────│──────────────────────┘
       │                            │              │
       ▼                            │              ▼
┌─────────────┐                     │    ┌──────────────────┐
│  CloudFront │                     │    │ Webhook Ingestion │
│    (CDN)    │                     │    │    Endpoint       │
└──────┬──────┘                     │    │ (verify signature │
       │                            │    │  return 200 fast) │
       ▼                            │    └────────┬─────────┘
┌─────────────┐                     │             │
│     ALB     │                     │             ▼
│ (Load Bal.) │                     │    ┌──────────────────┐
└──────┬──────┘                     │    │   Kafka Topic:   │
       │                            │    │   webhook.events  │
       ▼                            │    └────────┬─────────┘
┌─────────────────┐                 │             │
│   API Gateway   │                 │             ▼
│ (auth, tenant   │                 │    ┌──────────────────┐
│  routing, rate  │                 │    │  Event Processor  │
│  limiting)      │                 │    │   Workers (KEDA)  │
└──┬───┬───┬──────┘                 │    │ (parse, enrich,   │
   │   │   │                        │    │  store in Stats   │
   │   │   │                        │    │  DB, update       │
   ▼   ▼   ▼                        │    │  campaign status) │
┌────┐┌────┐┌──────────┐            │    └────────┬─────────┘
│Cam-││List││ Template  │            │             │
│pai-││Mgmt││ Service   │            │             ▼
│gn  ││Svc ││           │            │    ┌──────────────────┐
│Svc ││    ││           │            │    │   Stats Service   │
└──┬─┘└──┬─┘└────┬─────┘            │    │  (query stats,    │
   │     │       │                   │    │   aggregations,   │
   │     │       │                   │    │   dashboards)     │
   │     │       │                   │    └────────┬─────────┘
   │     │       │                   │             │
   ▼     ▼       ▼                   │             ▼
┌──────────────────────┐             │    ┌──────────────────┐
│    PostgreSQL        │             │    │  TimescaleDB /   │
│  (campaigns, lists,  │             │    │  ClickHouse      │
│   templates, tenants,│             │    │  (100M+ events,  │
│   users, schedules)  │             │    │   time-series    │
└──────────────────────┘             │    │   aggregations)  │
                                     │    └──────────────────┘
   ┌───────────────┐                 │
   │  Scheduler    │                 │
   │  Service      │─────────────────┘
   │ (cron checks  │     sends via SMTP provider
   │  pending      │
   │  send-outs,   │
   │  triggers     │
   │  Send Worker) │
   └───────┬───────┘
           │
           ▼
   ┌───────────────┐
   │  Send Worker   │
   │  (KEDA-scaled) │
   │  batch sends   │
   │  to SMTP API   │
   └───────────────┘


Supporting services:

   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
   │     Redis     │    │      S3       │    │   Secrets     │
   │  (cache,      │    │  (images,     │    │   Manager     │
   │   sessions,   │    │   files,      │    │  (API keys,   │
   │   rate limit) │    │   exports)    │    │   SMTP creds) │
   └───────────────┘    └───────────────┘    └───────────────┘

   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
   │  Tenant Admin │    │  OpenTelemetry│    │  Grafana      │
   │  Service      │    │  → Tempo      │    │  Dashboards   │
   │ (onboard,     │    │  → Prometheus │    │  + Alerts     │
   │  delete,      │    │  → Loki       │    │               │
   │  configure)   │    └───────────────┘    └───────────────┘
   └───────────────┘
```

---

## Step 3: Service-by-Service Breakdown

### Services and their responsibilities

| Service | Responsibility | Database | Communication |
|---------|---------------|----------|---------------|
| **API Gateway** | Auth (JWT validation), tenant routing, rate limiting per tenant, public API access control | — | Routes to all backend services |
| **Campaign Service** | Create/edit campaigns, link to templates + lists, manage send-out state machine (draft → scheduled → sending → sent) | PostgreSQL (campaigns table, tenant_id scoped) | Reads templates and lists. Publishes `CampaignScheduled` event to Kafka |
| **List Management Service** | CRUD for recipient lists, import CSV, manage unsubscribes and bounced addresses | PostgreSQL (lists, recipients tables) | Receives bounce events from Event Processor to auto-unsubscribe |
| **Template Service** | Create/edit email templates with variable placeholders, version management | PostgreSQL (templates table) | Called by Send Worker to render emails |
| **Scheduler Service** | Checks for campaigns scheduled to send at a specific time, triggers the send process | PostgreSQL (reads scheduled campaigns) | Publishes `SendOutTriggered` event to Kafka when it's time |
| **Send Worker** | Batches recipients, renders templates with recipient data, calls external SMTP API | — (reads from PostgreSQL + Template Service) | Consumes `SendOutTriggered` from Kafka, calls SMTP provider API in batches |
| **Webhook Ingestion** | Receives webhooks from SMTP provider, validates signature, returns 200 immediately, enqueues event | — | Publishes raw webhook to Kafka `webhook.events` topic |
| **Event Processor** | Consumes webhook events, parses/enriches, stores in Stats DB, updates campaign delivery status, flags bounces | TimescaleDB / ClickHouse | Consumes from Kafka, writes to Stats DB, updates PostgreSQL campaign status |
| **Stats Service** | Queries statistics for dashboards — sends, deliveries, opens, clicks, bounces per campaign/list/time | TimescaleDB / ClickHouse (read) | REST/GraphQL API for the frontend dashboard |
| **Tenant Admin Service** | Onboard new tenants (create DB records, configure SMTP, allocate resources), delete tenants (cascade delete all data) | PostgreSQL (tenants, plans, billing) | Internal only — called by admin panel |

---

## Step 4: How Services Communicate

```
Synchronous (REST/gRPC — when caller needs a response):
  [API Gateway] → [Campaign Service]       GET /campaigns, POST /campaigns
  [API Gateway] → [List Management]        GET /lists, POST /lists, POST /lists/import
  [API Gateway] → [Template Service]       GET /templates, POST /templates
  [API Gateway] → [Stats Service]          GET /campaigns/:id/stats
  [API Gateway] → [Tenant Admin Service]   POST /tenants (admin only)
  [Send Worker] → [Template Service]       GET /templates/:id/render (with recipient data)
  [Send Worker] → [SMTP Provider API]      POST /send (batch of emails)

Asynchronous (Kafka events — fire-and-forget, multiple consumers):
  [Campaign Service]    → Kafka: campaign.scheduled     → [Scheduler Service] picks up
  [Scheduler Service]   → Kafka: sendout.triggered      → [Send Worker] starts sending
  [Send Worker]         → Kafka: sendout.progress        → [Campaign Service] updates status
  [Webhook Ingestion]   → Kafka: webhook.events          → [Event Processor] stores stats
  [Event Processor]     → Kafka: recipient.bounced       → [List Management] auto-unsubscribes
  [Event Processor]     → Kafka: campaign.stats.updated  → [Stats Service] refreshes cache

Why Kafka (not SQS or RabbitMQ):
  - 100M+ webhook events need high-throughput durable log
  - Multiple consumers per event (stats + list update + campaign status all react)
  - Need replay capability (rebuild stats if something goes wrong)
  - Partition by campaign_id for ordering (events for same campaign processed in order)
```

---

## Step 5: Detailed Design Decisions

### Data Storage

| Data | Store | Why |
|------|-------|-----|
| Tenants, users, campaigns, templates, lists, recipients, schedules | **PostgreSQL** (RDS Multi-AZ) | Relational data with foreign keys (campaign belongs to tenant, uses template, targets list). ACID transactions for schedule + status updates. tenant_id on every table |
| 100M+ interaction events (sends, deliveries, opens, clicks, bounces) | **TimescaleDB** (or ClickHouse) | Time-series data: append-only, queried by time range. TimescaleDB: automatic time-based partitioning, compression (10-20x), continuous aggregates for pre-computed dashboard stats. ClickHouse: even faster for analytical queries at 100M+ scale |
| Session data, rate limiting counters, campaign send progress | **Redis** (ElastiCache) | Sub-ms reads for rate limiting (every API request checks the limit). Cache campaign stats that are queried frequently. Track send progress (sent: 500,000 / 1,000,000) |
| Images and file uploads used in campaigns | **S3** + CloudFront CDN | Images may be served to millions of email recipients. S3 stores the files, CloudFront CDN caches globally. Pre-signed URLs for upload, public CDN URL for serving in emails |
| SMTP credentials, API keys, secrets | **AWS Secrets Manager** | Never in code, never in env vars. CSI driver mounts as files in K8s pods |

### Multi-Tenancy

```
Strategy: shared database with tenant_id column on every table.
Why: hundreds of tenants, most are small. DB-per-tenant at this scale = hundreds of databases to manage.

Implementation:
  - tenant_id in JWT claims, extracted at API Gateway
  - every service receives tenant_id in the request context
  - every database query: WHERE tenant_id = @tenant_id AND ...
  - enforced at the data access layer (base repository), not in controllers
  - integration tests verify cross-tenant access returns zero results

Rate limiting per tenant:
  - Redis token bucket per tenant: INCR tenant:{id}:requests EX 60
  - large tenants get higher limits (configured in tenant settings)
  - prevents one tenant's bulk send from degrading the platform for others

Noisy neighbor protection:
  - separate Kafka partitions are not per-tenant (would limit parallelism)
  - instead: rate limit the SMTP API calls per tenant (max emails/hour)
  - large campaigns are sent in batches with controlled throughput
```

### Scheduling Send-Outs

```
"How can scheduling of send-outs be handled?"

Option chosen: Scheduler Service polling + Kafka event

Flow:
  1. User creates campaign, sets send_date = "2024-01-15 09:00 UTC"
     Campaign Service writes to PostgreSQL: status = 'scheduled', send_at = timestamp

  2. Scheduler Service runs every 60 seconds (Kubernetes CronJob or Deployment with timer)
     Query: SELECT * FROM campaigns WHERE status = 'scheduled' AND send_at <= NOW()
     For each: publish SendOutTriggered event to Kafka, update status = 'sending'

  3. Send Worker consumes SendOutTriggered
     - Loads recipient list from List Management Service
     - Batches recipients (1000 per batch)
     - For each batch:
       - Renders template for each recipient (merge variables: name, email, etc.)
       - Calls SMTP provider API with the batch
       - Publishes progress event (sent: 5000 / 100000)
     - When all batches complete: publishes SendOutCompleted event

  4. Campaign Service consumes SendOutCompleted → updates status = 'sent'

Why this approach:
  - Scheduler is simple (poll every 60s, idempotent — skips already-sending campaigns)
  - Kafka decouples scheduling from sending (Scheduler doesn't wait for send to finish)
  - Send Workers auto-scale via KEDA on Kafka consumer lag
  - If a Send Worker crashes mid-batch, Kafka redelivers unacked messages
  - Idempotency: each batch has a batch_id, SMTP provider deduplicates by message-id

Alternative considered: database-level pg_cron or AWS EventBridge scheduler
  Rejected: less flexible, harder to monitor, tighter coupling to cloud provider

Campaign state machine:
  draft → scheduled → sending → sent
                   → paused (user can pause mid-send)
                   → failed (SMTP provider error, retry or manual intervention)
```

### Webhook Ingestion (100M+ events)

```
"External SMTP provider reports bounces, deliveries, clicks, opens via webhooks"

Flow:
  1. SMTP provider sends HTTP POST to our webhook endpoint
     Contains: event_type (delivered/bounced/opened/clicked), message_id, recipient, timestamp, metadata

  2. Webhook Ingestion endpoint:
     - Verifies signature (HMAC-SHA256 with shared secret) → reject if invalid
     - Returns 200 OK immediately (< 100ms response time — SMTP providers retry on slow responses)
     - Publishes the raw event to Kafka topic: webhook.events
     - Partition key: campaign_id (all events for same campaign go to same partition → ordered)

  3. Event Processor Workers (KEDA-scaled on Kafka consumer lag):
     - Consumes from Kafka
     - Parses the event (normalize format across SMTP providers — future-proofing for multi-channel)
     - Enriches: look up campaign_id, tenant_id from message_id
     - Writes to TimescaleDB/ClickHouse:
       INSERT INTO events (tenant_id, campaign_id, recipient, event_type, timestamp, metadata)
     - Side effects per event type:
       ├── delivered → increment campaign delivered count (Redis counter)
       ├── bounced → publish recipient.bounced event → List Management auto-unsubscribes
       ├── opened → increment campaign opened count
       ├── clicked → increment campaign clicked count, record which link
       └── complaint/spam → publish recipient.complained → List Management + alert tenant

  4. Stats Service reads from TimescaleDB for dashboard queries:
     - "Show me opens over time for campaign X" → time-bucketed query
     - "Show me bounce rate per list" → aggregation query
     - Pre-computed via TimescaleDB continuous aggregates (hourly/daily rollups)

Why this approach:
  - Webhook endpoint is thin and fast (returns 200 in < 100ms, no processing)
  - Kafka buffers spikes (a campaign sending 1M emails → 1M+ webhook events in minutes)
  - Event Processors scale independently from the webhook endpoint
  - KEDA scales processors on consumer lag: 100K pending events → 10 workers, 0 events → 0 workers
  - TimescaleDB handles 100M+ events with time-based partitioning and compression
  - Idempotent consumers: event_id (from SMTP provider) stored in dedup table, skip duplicates
```

### Future Multi-Channel Support

```
"Have in mind that we potentially want to start sending through other channels"

Design for extensibility — Channel Adapter pattern:

Current:
  [Send Worker] → [Email Adapter] → [SMTP Provider API]

Future:
  [Send Worker] → [Channel Router (by campaign.channel_type)]
                    ├── [Email Adapter]  → [SMTP Provider API]
                    ├── [SMS Adapter]    → [Twilio API]
                    ├── [Push Adapter]   → [FCM / APNs]
                    └── [WhatsApp Adapter] → [WhatsApp Business API]

What this means for the current design:
  - Campaign table has a channel_type column (default: 'email')
  - Template Service supports channel-specific templates (email HTML, SMS text, push payload)
  - Webhook Ingestion is already per-channel (different endpoint or different parser per provider)
  - Event Processor normalizes events to a common format:
    { tenant_id, campaign_id, channel, recipient, event_type, timestamp }
  - Stats Service queries are channel-agnostic (filter by channel in the WHERE clause)

  No architecture changes needed — just add a new adapter and template type per channel.
```

### Image and File Uploads

```
Flow:
  1. User clicks "upload image" in the campaign editor
  2. Frontend calls POST /uploads → API returns a pre-signed S3 URL (expires in 15 minutes)
  3. Frontend uploads directly to S3 using the pre-signed URL (never goes through our API)
  4. S3 event notification → small worker validates the file (size check, virus scan with ClamAV)
  5. Campaign stores the S3 URL as the image reference
  6. When email is sent, the image URL points to CloudFront CDN:
     https://cdn.emailplatform.com/tenant-123/campaigns/456/hero.jpg
  7. CloudFront caches the image globally — millions of email opens hit CDN, not S3

Why pre-signed URL:
  - Campaign images can be large (5-10 MB per image, multiple images per campaign)
  - Proxying through the API wastes memory and threads
  - Direct S3 upload handles any file size without API server involvement

Tenant isolation:
  - S3 key prefix: /tenant-{id}/campaigns/{campaign-id}/{filename}
  - Pre-signed URL is scoped to the tenant's prefix (can't upload to another tenant's path)
  - CDN serves any public image (images in emails must be public), but the S3 bucket is private
```

---

## Step 6: Tenant Administration

```
"Explain how the service could be administered — setting up new customers and deleting them"

═══ ONBOARDING A NEW TENANT ═══════════════════════════════

Trigger: admin creates tenant via Tenant Admin Service (internal admin panel or API)

Steps:
  1. Create tenant record in PostgreSQL
     INSERT INTO tenants (id, name, plan, smtp_config, rate_limits, created_at)
     
  2. Create admin user for the tenant
     INSERT INTO users (id, tenant_id, email, role='admin')
     Send welcome email with login link (password reset flow)
     
  3. Configure SMTP provider for the tenant
     - Create sender domain / sender identity in the SMTP provider (SendGrid verified sender)
     - Store SMTP credentials in Secrets Manager under tenant's namespace
     - Verify domain (DNS records: SPF, DKIM, DMARC)
     
  4. Set rate limits based on plan
     - Free: 1,000 emails/month, 1 list, 1 user
     - Pro: 100,000 emails/month, unlimited lists, 5 users
     - Enterprise: custom limits, dedicated sending IP, SLA
     Store limits in tenant config (PostgreSQL + cached in Redis)
     
  5. Create S3 prefix for tenant's files
     - No action needed — S3 prefix is created on first upload (lazy creation)
     - Pre-signed URLs are scoped to /tenant-{id}/ automatically

  6. Verification: run automated health check
     - Can the tenant's user log in?
     - Can they create a template?
     - Can they send a test email?
     
  Duration: < 5 minutes (automated). DNS verification: up to 48 hours (external dependency).


═══ DELETING A TENANT ═════════════════════════════════════

Trigger: admin initiates tenant deletion (requires confirmation + grace period)

Steps:
  1. Soft-delete: mark tenant as deleted, disable login
     UPDATE tenants SET status = 'deleted', deleted_at = NOW() WHERE id = @tenant_id
     All API requests for this tenant return 403 immediately (checked at API Gateway)
     
  2. Grace period: 30 days (in case of accidental deletion or customer wants to return)
     Tenant data still exists but is inaccessible
     
  3. After grace period: hard-delete pipeline
     ├── Delete all campaigns, templates, lists, recipients WHERE tenant_id = @id
     ├── Delete all events from TimescaleDB WHERE tenant_id = @id
     ├── Delete all files from S3 under /tenant-{id}/ prefix (S3 batch delete)
     ├── Delete all Redis keys matching tenant:{id}:*
     ├── Delete tenant record from PostgreSQL
     ├── Remove SMTP sender identity from provider
     ├── Remove secrets from Secrets Manager
     └── Audit log: record who initiated deletion, when, what was deleted
     
  4. GDPR compliance:
     - Right to deletion: all personal data (recipient emails, names) must be removed
     - Audit log of the deletion itself is retained (proves we complied)
     - Backups: tenant data in backups expires naturally with backup retention policy (30 days)
       After 30 days, the tenant's data is gone from backups too
```

---

## Step 7: Monitoring and Troubleshooting

```
"Explain how the service could be monitored and troubleshooted by us"

═══ MONITORING STACK ══════════════════════════════════════

  [All Services + OpenTelemetry SDK]
       ├── traces  → Tempo (or Jaeger)
       ├── metrics → Prometheus → Grafana
       └── logs    → Loki (or ELK) → Grafana

  All signals correlated by trace ID.
  Click a metric spike → see the traces → click a trace → see the logs.

═══ KEY DASHBOARDS ════════════════════════════════════════

  1. Platform Health Dashboard
     - Request rate, error rate, latency (p50, p95, p99) per service
     - Kafka consumer lag per topic (webhook.events, sendout.triggered)
     - Database connections, CPU, disk usage
     - Redis memory usage, hit rate, eviction rate
     - Pod count, restarts, OOMKills per service
     
  2. Send-Out Dashboard
     - Active send-outs: which campaigns are currently sending
     - Send rate: emails/second per tenant and total
     - Queue depth: how many batches are waiting to be sent
     - SMTP provider response codes: 200s, 429s (rate limited), 500s
     - Progress: sent / total per campaign
     
  3. Webhook Ingestion Dashboard
     - Webhook events received per second (total and per event type)
     - Processing lag: time from webhook received to event stored in Stats DB
     - Event Processor consumer lag (Kafka lag metric)
     - Signature verification failures (possible attack or misconfigured provider)
     - DLQ depth (events that failed processing)
     
  4. Tenant Dashboard (per-tenant view)
     - Emails sent this month vs plan limit
     - Bounce rate (alert if > 5% — reputation risk)
     - Complaint/spam rate (alert if > 0.1% — provider may suspend)
     - API usage per tenant (rate limiting effectiveness)
     
  5. Cost Dashboard
     - SMTP provider cost (per email sent)
     - AWS infra cost (per service: compute, database, S3, CDN bandwidth)
     - Cost per tenant (for billing and plan enforcement)

═══ ALERTING ══════════════════════════════════════════════

  | Alert | Condition | Action |
  |-------|-----------|--------|
  | Error rate spike | Error rate > 5% for 5 minutes | Page on-call, check error flow |
  | Webhook lag | Kafka consumer lag > 100K events | Scale Event Processors, check for poison messages |
  | Send stalled | Campaign in 'sending' state > 1 hour without progress | Check Send Workers, SMTP provider status |
  | Bounce rate high | Tenant bounce rate > 5% | Notify tenant, pause sending (reputation protection) |
  | Complaint rate | Tenant spam complaint rate > 0.1% | Auto-pause tenant, alert team |
  | DLQ not empty | DLQ depth > 0 for > 5 minutes | Investigate failed messages, fix and replay |
  | Database disk | Disk usage > 80% | Increase volume, check retention policies |
  | Certificate expiry | TLS cert expires in < 14 days | Check cert-manager, renew |

═══ TROUBLESHOOTING FLOWS ═════════════════════════════════

  "Emails not being delivered"
   1. Check campaign status in PostgreSQL → is it 'sending' or stuck?
   2. Check Send Worker logs → are they running? any errors calling SMTP API?
   3. Check SMTP provider dashboard → are they accepting our sends?
   4. Check Kafka topic sendout.triggered → was the event published?
   5. Check SMTP provider for bounces → is the recipient list clean?

  "Statistics not updating"
   1. Check Webhook Ingestion → are webhooks arriving? (request count metric)
   2. Check signature verification → are webhooks being rejected? (401 rate)
   3. Check Kafka topic webhook.events → are events being published?
   4. Check Event Processor consumer lag → are processors running? keeping up?
   5. Check DLQ → are events failing processing? (parsing error, DB error)
   6. Check TimescaleDB → is the Stats DB reachable? disk full?

  "User can't log in"
   1. Check API Gateway → is it routing correctly? tenant exists?
   2. Check identity provider (Auth0/Keycloak) → is it up?
   3. Check JWT token → expired? wrong tenant? wrong role?
   4. Check tenant status → is the tenant soft-deleted or suspended?
```

---

## Step 8: AWS Infrastructure

```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS Infrastructure                        │
│                                                                  │
│  [Route 53 DNS]                                                  │
│       │                                                          │
│  [CloudFront CDN] ──→ [S3: images and files]                    │
│       │                                                          │
│  [ALB (Application Load Balancer)]                               │
│       │                                                          │
│  [EKS Cluster]                                                   │
│   ├── Namespace: services                                        │
│   │    ├── API Gateway (Deployment, HPA)                         │
│   │    ├── Campaign Service (Deployment, HPA)                    │
│   │    ├── List Management Service (Deployment)                  │
│   │    ├── Template Service (Deployment)                         │
│   │    ├── Scheduler Service (Deployment, 1 replica)             │
│   │    ├── Send Worker (Deployment, KEDA-scaled)                 │
│   │    ├── Webhook Ingestion (Deployment, HPA)                   │
│   │    ├── Event Processor (Deployment, KEDA-scaled)             │
│   │    ├── Stats Service (Deployment, HPA)                       │
│   │    └── Tenant Admin Service (Deployment, 1 replica)          │
│   │                                                              │
│   └── Namespace: monitoring                                      │
│        ├── Grafana Alloy (DaemonSet — metrics + traces)          │
│        ├── Promtail (DaemonSet — log collection)                 │
│        └── kube-state-metrics                                    │
│                                                                  │
│  [Amazon MSK (Managed Kafka)]                                    │
│   Topics: webhook.events, sendout.triggered, sendout.progress,   │
│           campaign.stats.updated, recipient.bounced              │
│                                                                  │
│  [Amazon RDS PostgreSQL Multi-AZ]                                │
│   (campaigns, templates, lists, recipients, tenants, users)      │
│                                                                  │
│  [TimescaleDB on RDS or self-hosted on EKS]                     │
│   (100M+ interaction events, time-series queries)                │
│                                                                  │
│  [Amazon ElastiCache Redis]                                      │
│   (cache, sessions, rate limiting, send progress counters)       │
│                                                                  │
│  [AWS Secrets Manager]                                           │
│   (SMTP credentials, API keys, JWT signing keys)                 │
│                                                                  │
│  [Terraform] manages all of the above                            │
│  [GitHub Actions] CI/CD pipeline                                 │
│                                                                  │
│  [Grafana Cloud or self-hosted]                                  │
│   Tempo (traces) + Prometheus/Mimir (metrics) + Loki (logs)     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step 9: Summary — Key Trade-Offs

| Decision | Chose | Over | Why |
|----------|-------|------|-----|
| Shared DB + tenant_id | ✓ | DB per tenant | Simpler ops for hundreds of tenants. Evolve later if needed |
| Kafka for events | ✓ | SQS | 100M+ events, multiple consumers, need replay for stats rebuild |
| TimescaleDB for stats | ✓ | PostgreSQL | Time-series optimized: partitioning, compression, continuous aggregates for 100M+ events |
| Pre-signed URL upload | ✓ | Proxy through API | Millions of recipients view images via CDN. Large files don't touch the API server |
| Scheduler polling | ✓ | EventBridge/cron | Simpler, database is source of truth, idempotent, easy to monitor |
| Channel Adapter pattern | ✓ | Hardcoded email | Future-proof for SMS/push/WhatsApp without architecture changes |
| KEDA for workers | ✓ | Fixed replicas | Send Workers and Event Processors scale to zero when idle, scale up with Kafka lag |
| Webhook → Kafka → process | ✓ | Process inline | Return 200 fast (SMTP providers retry on slow responses), buffer spikes, scale independently |

---

*[[company-lime|Back to Lime Prep]]* · *[[system-design-reference|Reference Cards]]*
