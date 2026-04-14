---
tags:
  - interview-kit
  - interview-kit/company
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Lime Technologies — Senior Cloud-Focused Software Engineer

## Skill Matrix — Lime vs My Experience

| Lime Needs              | My Match                                            | Preview                                                                                                                                                                                                                                                                                                                                                               |
| ----------------------- | --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **C#**                  | 10yr, .NET 9, microservices, 95 interview Qs        | [[ref-csharp#Q6. What happens under the hood when you `await` a Task?\|Async]] · [[ref-csharp#Q17. Explain the three DI service lifetimes in ASP.NET Core.\|DI]] · [[ref-csharp#Q51. What are `FrozenDictionary` and `FrozenSet` and how do they differ from `ReadOnlyDictionary`?\|.NET 9]] · [[ref-csharp#Q35. How does the middleware pipeline work?\|Middleware]] |
| **Kubernetes**          | 60+ svc AKS, custom probes, HPA, Kustomize          | [[ref-kubernetes#What Kubernetes Is\|What K8s Is]] · [[ref-kubernetes#Health Probes\|Probes]] · [[ref-kubernetes#Resource Management\|HPA/KEDA]] · [[ref-kubernetes#Deployment Strategies\|Rolling/PDB]] · [[ref-kubernetes#Docker vs Kubernetes\|vs Docker]]                                                                                                         |
| **AWS migration**       | Azure→AWS: K8s=K8s, TF=TF, patterns transfer        | [[ref-terraform#What Terraform Is\|Terraform]] · [[ref-terraform#Terraform vs Pulumi vs CloudFormation\|vs Pulumi/CFN]] · [[ref-docker#What Docker Is\|Docker]] · [[ref-docker#Multi-Stage Builds\|Multi-Stage]]                                                                                                                                                      |
| **CI/CD**               | GH Actions 60+ svc + AzDO from scratch              | [[ref-github-actions#What GitHub Actions Is\|GH Actions]] · [[ref-github-actions#Reusable Workflows\|Reusable]] · [[ref-github-actions#GitHub Actions vs Azure DevOps vs Jenkins\|vs AzDO/Jenkins]] · [[ref-cicd-security#What CI/CD Security Is\|DevSecOps]]                                                                                                         |
| **MS SQL**              | GPS 250w/s, SqlBulkCopy, Dapper+EF                  | [[ref-sql-databases#What SQL Databases Are\|SQL]] · [[ref-sql-databases#Dapper vs Entity Framework\|Dapper vs EF]] · [[ref-sql-databases#SQL Performance Analysis — My Approach\|Perf Analysis]]                                                                                                                                                                      |
| **Redis**               | Streams, Sentinel, cache-aside, GPS scaling         | [[ref-redis#What Redis Is\|What Redis Is]] · [[ref-redis#Redis Streams (What I Used)\|Streams]] · [[ref-redis#Sentinel (High Availability)\|Sentinel]] · [[ref-redis#Caching Patterns\|Cache-Aside]]                                                                                                                                                                  |
| **Vue / TypeScript**    | Backend-first, frontend understanding               | [[ref-frontend-frameworks#Vue Composition API\|Vue]] · [[ref-frontend-frameworks#TypeScript for Frontend\|TypeScript]] · [[ref-frontend-frameworks#SSR vs CSR vs SSG vs ISR\|SSR/CSR]]                                                                                                                                                                                |
| **Architecture**        | GraphQL migration, DDD/CQRS, 60+ microservices      | [[ref-microservices#What Microservices Are\|Microservices]] · [[ref-microservices#Microservices vs Monolith\|vs Monolith]] · [[ref-design-patterns#What Design Patterns Are\|Patterns]] · [[ref-ddd-cqrs#What DDD and CQRS Are\|DDD/CQRS]]                                                                                                                            |
| **Testing**             | Test pyramid, Testcontainers, E2E, breaking changes | [[ref-testing-strategy#What a Testing Strategy Is\|Strategy]] · [[ref-testing-strategy#Testcontainers\|Testcontainers]] · [[ref-testing-strategy#Unit vs Integration vs E2E — When to Use Which\|Unit vs Int vs E2E]] · [[ref-testing-strategy#Mocking vs Real Dependencies\|Mock vs Real]]                                                                           |
| **ShapeUp**             | Scrum Master certified, reformed ceremonies         | [[ref-agile-ceremonies#What Agile Ceremonies Are\|Ceremonies]] · [[ref-agile-ceremonies#Scrum vs Kanban\|Scrum vs Kanban]] · [[ref-agile-leadership#What Agile Leadership Is\|Leadership]]                                                                                                                                                                            |
| **SaaS / Multi-tenant** | KocSistem: 4 enterprise clients, config-driven      | [[ref-web-architecture#What Web Architecture Is\|Web Arch]] · [[ref-performance#What Performance Profiling Is\|Performance]] · [[ref-owasp-security#How I Applied This\|Security]]                                                                                                                                                                                    |
| **Observability**       | OTel, Tempo, Loki, Grafana, DORA metrics            | [[ref-observability-stack#What Observability Is\|OTel Stack]] · [[ref-grafana-prometheus#Prometheus\|Prometheus]] · [[ref-dora#What DORA Metrics Are\|DORA]]                                                                                                                                                                                                          |
| **Code review**         | Built from scratch, quality gates, at scale         | [[ref-code-review#"Review This Code" — My Checklist\|Checklist]] · [[ref-code-review#Quality Gates in CI\|Gates]] · [[ref-code-review#Common Anti-Patterns I Flag\|Anti-Patterns]]                                                                                                                                                                                    |
| **Leadership**          | 25 engineers, DevOps transform, data-driven         | [[ref-ways-of-working#The DRIVE Framework\|DRIVE]] · [[ref-ways-of-working#How I Lead\|How I Lead]] · [[ref-ways-of-working#Conflict — Deployment Freeze\|Conflict]] · [[ref-ways-of-working#Leadership — CI/CD Pilot\|CI/CD Pilot]]                                                                                                                                  |
|                         |                                                     |                                                                                                                                                                                                                                                                                                                                                                       |
[[14-ref-overview]]
---

## Job Summary

| | |
|---|---|
| **Company** | Lime Technologies (listed, founded 1990, 9 offices, 6 countries, ~20% annual growth since 2000) |
| **Role** | Senior Cloud-Focused Software Engineer |
| **Location** | Gothenburg (also Lund, Stockholm) |
| **Product** | Automation & communication platform — help desk, sales, marketing automation |
| **Big move** | Migrating components to **Kubernetes on AWS** — joining from the start |
| **Methodology** | **ShapeUp** (not Scrum — appetite-based, 6-week cycles, cooldown periods) |
| **Stack** | C#, Vue, TypeScript, MS SQL, Redis |
| **Nice-to-have** | AWS, SaaS hosting, CI/CD (GitHub Actions, Azure DevOps), architecture experience |

---

## My Overlap — What to Highlight

### Perfect Match ✓
| Their need | My experience | Where to find it |
|-----------|---------------|-------------------|
| **C#** | 10 years, .NET 9, microservices | [[ref-csharp]] |
| **Kubernetes** | 60+ services, Kustomize, custom health checks, HPA | [[ref-kubernetes]] |
| **CI/CD (GitHub Actions, Azure DevOps)** | Built from zero at KocSistem, 60+ services at Combination | [[ref-github-actions]], [[ref-azure-devops]] |
| **Redis** | Streams, caching, Sentinel at KocSistem | [[ref-redis]] |
| **MS SQL** | GPS tracking system, Dapper, EF, SqlBulkCopy | [[ref-sql-databases]] |
| **Architecture ownership** | GraphQL migration, microservices platform, DDD/CQRS | [[ref-design-patterns]], [[ref-microservices]] |
| **Automated testing** | Test pyramid, Testcontainers, E2E, breaking change detection | [[ref-testing-strategy]] |
| **Cloud migration** | Building K8s infrastructure at Combination (AKS), Terraform | [[ref-kubernetes]], [[ref-terraform]] |
| **Cross-functional collaboration** | PO experience, stakeholder management, 25 engineers | [[ref-ways-of-working]] |

### Strong Match — Need to Frame
| Their need | My angle | Notes |
|-----------|---------|-------|
| **AWS** | I work on Azure (AKS, Key Vault, ACR, Blob Storage). K8s is K8s regardless of cloud. Terraform skills transfer. Services like S3/Blob, RDS/SQL, ElastiCache/Redis are conceptually the same. | Be honest: "I've worked on Azure, but K8s, Terraform, and the container/IaC patterns are cloud-agnostic. I'd need a sprint to learn AWS-specific services, not a quarter." |
| **Vue / TypeScript** | I'm a backend engineer. I've done MVC frontends, Blazor, and I understand frontend architectures. Not a Vue expert but can contribute. | Frame as: "I'm backend-first but I've worked with frontend teams closely — I understand the contract between backend and frontend. I can pick up Vue." |
| **SaaS hosting** | I've built and operated microservices that serve many customers — multi-tenant experience at KocSistem (4 enterprise clients, config-driven tenancy). | Frame as: "I've built multi-tenant systems — one codebase, different configs per customer. SaaS hosting patterns (tenant isolation, feature flags, rolling deployments) are familiar." |
| **ShapeUp** | I know Scrum well (Scrum Master certified). ShapeUp is different — appetite-based, 6-week cycles, no sprints. | Read up before interview. Key difference: fixed time + variable scope (vs Scrum's fixed scope + variable time). Cooldown periods for tech debt. Pitches instead of backlog items. |

### Gap — Be Honest
| Their need | My situation | How to address |
|-----------|-------------|----------------|
| **AWS specific** | Azure experience, not AWS | "K8s is K8s. Terraform is Terraform. I'd learn EKS/S3/RDS specifics quickly. The patterns transfer." |
| **Vue.js** | No Vue experience | "I'm backend-focused. I can learn Vue, but my value is in the cloud/K8s/C# side." |

---

## Migration & Transformation — Anticipated Questions

> [!tip] Lime'ın en büyük projesi K8s+AWS dönüşümü. Bu konuda deep-dive soruları gelecek.

| Question                                 | My Answer                                                                                                                                                                                                                                                                                                                                                              | Ref                                                                 |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **Migration Strategy**                   |                                                                                                                                                                                                                                                                                                                                                                        |                                                                     |
| How would you approach migrating to K8s? | [[ref-microservices#Decomposition\|Strangler fig]] — don't rewrite, migrate piece by piece. Start with clearest boundary, lowest risk. Old system keeps running. At Combination, I [[sd-graphql-migration\|migrated REST→GraphQL]] over 6 months, zero breaking changes — same principle.                                                                              | [[ref-microservices#Decomposition\|Strangler Fig]]                  |
| Which services to migrate first?         | (1) Stateless — no data migration, (2) well-understood — fewer surprises, (3) low-risk — not payment on day one, (4) high-value — benefits from K8s autoscaling. At KocSistem, I [[do-azdevops-zero\|started CI/CD pilot]] with our own team — low risk, high visibility.                                                                                              | [[do-azdevops-zero\|CI/CD From Zero]]                               |
| How to run old + new in parallel?        | Reverse proxy routes traffic. Old requests → legacy, migrated → K8s. Share DB initially, evolve to events. At Combination, [[ref-graphql#Federation (HotChocolate Fusion)\|federated gateway]] routes to both old REST and new GraphQL — clients see one API.                                                                                                          | [[ref-graphql#Federation (HotChocolate Fusion)\|Federation]]        |
| **Containerization & Infra**             |                                                                                                                                                                                                                                                                                                                                                                        |                                                                     |
| How to containerize a legacy .NET app?   | [[ref-docker#Multi-Stage Builds\|Multi-stage Dockerfile]] (SDK→build, runtime→run). Externalize config. Add [[ref-kubernetes#Health Probes\|health probes]]. Handle SIGTERM graceful shutdown. At Combination, [[ref-docker#At Combination — Practical Setup\|.commons pattern]] — one template, 60+ services.                                                         | [[ref-docker#Multi-Stage Builds\|Multi-Stage]]                      |
| K8s from scratch on AWS?                 | [[ref-terraform#What Terraform Is\|Terraform]] for EKS/VPC/IAM. [[ref-kubernetes#Configuration\|Kustomize]] for app deployments (base + overlays). At Combination, GP-IaC-K8s-AKS repos. EKS vs AKS = different details, same patterns.                                                                                                                                | [[ref-terraform#HOW WE USE IT\|Terraform Setup]]                    |
| Secrets in K8s?                          | Never Git, never hardcoded. [[ref-kubernetes#Configuration\|Key Vault via CSI]] (Azure) / Secrets Manager + External Secrets (AWS). [[ref-cicd-security#Secrets Management\|At KocSistem, migrated to Key Vault, cleaned Git history]].                                                                                                                                | [[ref-cicd-security#Secrets Management\|Secrets]]                   |
| **CI/CD for Migration**                  |                                                                                                                                                                                                                                                                                                                                                                        |                                                                     |
| CI/CD for migrating platform?            | Both old + new get pipelines. New K8s services get [[ref-github-actions#Reusable Workflows\|reusable workflows]] — build→test→containerize→deploy from day one. At Combination, shared library for 60+ services. At KocSistem, [[do-azdevops-zero\|shared YAML templates]] = every project got pipelines automatically.                                                | [[ref-github-actions#Reusable Workflows\|Reusable Workflows]]       |
| Quality during migration?                | [[ref-testing-strategy#Testcontainers\|Testcontainers]] for real DB tests. [[ref-testing-strategy#Breaking Change Detection\|Breaking change detection]] in CI. [[ref-kubernetes#Deployment Strategies\|Rolling updates]] with readiness probes — unhealthy version never gets traffic.                                                                                | [[ref-testing-strategy#Mocking vs Real Dependencies\|Mock vs Real]] |
| **Database**                             |                                                                                                                                                                                                                                                                                                                                                                        |                                                                     |
| DB migration to microservices?           | Start shared DB (pragmatic), evolve to [[ref-microservices#Data Management\|database-per-service]]. Split service first, keep same DB. Then move data ownership gradually. Use [[ref-kafka#What Kafka Is\|events]] for sync during transition.                                                                                                                         | [[ref-microservices#Data Management\|Data Management]]              |
| MS SQL on K8s or managed?                | Managed (AWS RDS). Don't run DBs in K8s — managed handles backups, patching, failover. K8s = stateless workloads. At Combination, DBs on managed services, not in cluster.                                                                                                                                                                                             | [[ref-sql-databases#What SQL Databases Are\|SQL Databases]]         |
| **Observability**                        |                                                                                                                                                                                                                                                                                                                                                                        |                                                                     |
| Monitoring during migration?             | [[ref-observability-stack#OpenTelemetry (OTel)\|OTel]] in new services from day one. Unified logging ([[ref-observability-stack#Grafana Loki (Log Aggregation)\|Loki]]) + tracing ([[ref-observability-stack#Grafana Tempo (Distributed Tracing)\|Tempo]]) across old+new. [[ref-dora#What DORA Metrics Are\|DORA metrics]] to measure if migration improves delivery. | [[ref-observability-stack#The Full Data Flow\|Data Flow]]           |
| Rollback strategy?                       | Every step reversible. Proxy switches traffic back instantly. DB changes backward-compatible. [[ref-kubernetes#Deployment Strategies\|K8s auto-rollback]] on failed health checks. Feature flags for gradual enable.                                                                                                                                                   | [[ref-kubernetes#Deployment Strategies\|Rolling/PDB]]               |
| **Team & Culture**                       |                                                                                                                                                                                                                                                                                                                                                                        |                                                                     |
| Team new to K8s?                         | [[ls-transformation\|Same as KocSistem DevOps transform]]: start small, pair on first service, show value (zero-downtime, auto-recovery). First win visible and quick. Don't lecture — demonstrate.                                                                                                                                                                    | [[ls-transformation\|Transformation]]                               |
| Migration vs features?                   | ShapeUp cooldowns for migration steps, 6-week cycles for features. Or 70/30 split. At KocSistem, [[ls-transformation\|transformation alongside delivery]]. Migration should make features faster, not compete.                                                                                                                                                         | [[ref-agile-ceremonies#Scrum vs Kanban\|Scrum vs Kanban]]           |

---

## Questions I'd Ask Them

### Technical
- "What does the current architecture look like before the K8s migration? Monolith, microservices, or something in between?"
- "What's driving the move to K8s on AWS? Scale, cost, deployment speed, or all three?"
- "How far along is the K8s migration? Are you starting from zero or is there existing infrastructure?"
- "What does the CI/CD pipeline look like today? GitHub Actions? How do you deploy currently?"
- "How do you handle multi-tenancy in the SaaS platform? Shared database? Separate databases per tenant?"

### Process
- "You mention ShapeUp — how long have you been using it? What does a typical 6-week cycle look like?"
- "How does the cooldown period work? Is that where tech debt gets addressed?"
- "How much architectural autonomy does a senior engineer have?"

### Team
- "How big is the team I'd be joining? What's the backend/frontend split?"
- "How does cross-functional collaboration work in practice — do engineers talk to customers directly?"
- "What does on-call look like?"

---

## Interview Script — Lime-Specific

### Opening — Who I Am (1 min)
> "Hi, I'm Tughan Belbek. I live in Gothenburg with my family — my wife and my 4-year-old daughter. We moved here in 2022 from Turkey. I've been working as a software engineer for over **10 years**, building apps from the start till the end is exactly what I've been doing.
>
> My career covers four areas that all come together for this role: **[[10-pillar-software-dev|software development]]**, **[[11-pillar-devops|DevOps and infrastructure]]**, **[[12-pillar-leadership|technical leadership]]**, and **[[13-pillar-agile|Agile process]]**. Most of my career has been in environments where systems had to work — autonomous forklifts at Toyota, embedded automotive at Volvo, enterprise platforms with strict SLAs at KocSistem."

### Combination AB — Current Role (2 min)
> "I'm currently a **Senior Software Engineer** at **[[sd-combination|Combination AB]]** — a social gaming platform with **60+ .NET 9 microservices**. I own the API layer and the infrastructure side.
>
> On the **software side**: we use three API styles — [[ref-graphql#HOW WE USE IT|GraphQL]] for internal frontends (I [[sd-graphql-migration|led the migration from REST to GraphQL]] — 6 months, zero breaking changes), [[ref-grpc#HOW WE USE IT|gRPC]] for service-to-service (100+ proto files, typed client SDKs, [[ref-testing-strategy#Breaking Change Detection|breaking change detection]] in CI), and [[ref-rest#HOW WE USE IT|REST]] for external partners. When an endpoint is slow, I dig into query plans and resolver patterns — I [[ref-graphql#DataLoader & N+1 Problem|fixed an N+1 in GraphQL]] that dropped response time from 3 seconds to 200ms.
>
> On the **DevOps side**: I own the [[ref-kubernetes#HOW WE USE IT|Kubernetes deployment configs]] for all services — custom [[ref-kubernetes#Health Probes|health probes]] (we had a service stuck in restart loops until I added a startup probe), [[ref-kubernetes#Resource Management|HPA autoscaling]], [[ref-kubernetes#Configuration|Kustomize overlays]] for dev/staging/prod. I manage the [[ref-terraform#HOW WE USE IT|Terraform infrastructure]] for AKS — Cilium for networking, Contour for ingress, Chrony for time sync. I [[ref-docker#HOW WE USE IT|restructured all Dockerfiles]] as multi-stage builds — images from 800MB to 80MB, build times from 10 minutes to 2. Every service is instrumented with [[ref-observability-stack#OpenTelemetry (OTel)|OpenTelemetry]] — traces to Tempo, logs to Loki.
>
> On the **testing side**: I standardized the [[ref-testing-strategy#HOW WE TEST|test strategy across 60+ services]] — [[ref-testing-strategy#Testcontainers|Testcontainers]] with real MongoDB (we switched from mocks after mocked tests passed but production broke), E2E tests in both C# and TypeScript, and schema compatibility checks for gRPC protos and GraphQL."

### Toyota Material Handling — Distributed Real-Time Systems (1 min)
> "Before Combination, I was a **Senior Software Engineer** at **[[sd-toyota|Toyota Material Handling]]** — working on **T-ONE**, the platform that controls autonomous forklifts in warehouses. Backend in **.NET 8** with [[ref-ddd-cqrs#HOW WE USED IT|DDD/CQRS patterns]] — 30+ microservices, each owning a domain (Vehicles, Transport, Missions, Workflows). Fleet state in [[ref-mongodb#HOW WE USED IT|MongoDB]] with a custom extensions NuGet package, real-time commands via [[ref-rabbitmq#HOW WE USED IT|RabbitMQ]] with typed publishers and consumers.
>
> I dealt with a [[sd-rabbitmq-splitbrain|RabbitMQ split-brain in production]] — network partition split the cluster, messages got lost, forklifts stopped. That taught me more about distributed systems than any book. After that, I added chaos tests to the CI pipeline.
>
> I also maintained the **[[ref-texttest#HOW WE USED IT|Python TextTest framework]]** for fleet simulation — scenarios with 50, 100, 200 forklifts running simultaneously. Three other teams adopted the framework I maintained."

### Volvo Cars — Embedded Release Pipeline (1 min)
> "At **[[do-volvo|Volvo Cars]]**, I was a **Software Factory Engineer** — sole owner of the release pipeline for embedded automotive software. Build, [[ref-cicd-security#Scanning Types|static analysis]], unit tests, hardware-in-the-loop testing on actual ECU hardware, [[ref-automotive-compliance#ISO 26262 — Functional Safety|regulatory gate checks]], staged rollout. All on Linux with Python automation and ZUUL CI.
>
> I maintained the [[ref-gerrit#HOW WE USED IT|Gerrit instance]] and wrote the Python trigger daemon connecting Gerrit events to the build system — solved silent SSH drops and cut duplicate builds by 30%. I [[do-cynosure-parallel|parallelized the build orchestration]] across QNX, Linux, and Android Automotive targets — build time from 40 minutes to 15. Three departments, one pipeline, one person responsible. Zero [[ref-automotive-compliance#HOW WE USED IT|compliance findings]]."

### KocSistem — DevOps Transformation & Leadership (2 min)
> "At **[[do-kocsistem|KocSistem]]**, I had three roles over 4 years: **Senior Developer**, **Dev Lead**, and **Technology Manager**.
>
> As a Senior Dev, I built a **GPS-based warehouse management system** for clients like Arcelik, Beko, and Bosch. [[sd-redis-scaling|500+ trucks sending GPS every 2 seconds overwhelmed SQL Server]] — I split the architecture with [[ref-redis#HOW WE USED IT|Redis Streams]] for real-time display + batch writes to SQL for history. That project won the **2019 IDC Award**. I also [[ls-initiative|built monitoring from scratch]] because I was tired of debugging blind — detection went from hours to minutes. That initiative [[ls-growth|led to my promotion to Dev Lead]].
>
> As Dev Lead, I [[ls-transformation|drove a DevOps transformation]] — the team was doing push-and-pray weekly releases. I measured the pain with [[ref-dora#HOW WE USED IT|DORA metrics]], proposed a [[ls-ownership|pilot with our own team]], and was online at 6 AM for the first automated deploys. Weekly to daily in 3 weeks, org-wide in 6 months. I [[do-azdevops-zero|built Azure DevOps pipelines]] with [[ref-azure-devops#Template System|shared YAML templates]], set up [[ref-terraform#State Management|Terraform with remote state]] (learned state locking [[do-terraform-state|the hard way]]), and integrated [[ref-cicd-security#HOW WE USED IT|security scanning]] into every build. SLA breaches down **60%**, bugs down **55%**, zero pen-test findings 3 quarters.
>
> As Technology Manager, I led **25 engineers**, owned the technical roadmap, and [[ls-balance|split my time between coding and managing]]. I [[ls-conflict|resolved a deployment freeze conflict]] with a 6-week data experiment — data decided, not opinions. I'm a **Registered [[ref-agile-ceremonies#Scrum Roles|Scrum Master]]** and took Agile maturity from **3.1 to 3.7** — [[ag-efficiency|standups from 30 to 8 minutes]], [[ag-accountability|retros with real action items]], [[ag-alignment|sprint goals]] to protect scope."

### Why Lime (1 min)
> "Four things:
>
> **Technically** — you're moving to Kubernetes on AWS, and I get to help build that from the start. That's where I'm strongest — I've done exactly this at Combination and KocSistem.
>
> **Product** — automation platforms need to be reliable and scalable. That's what I care about — systems where uptime matters and performance is visible to customers.
>
> **Process** — ShapeUp with stable cycles, no artificial deadlines, 'best tool for the problem.' I've seen what [[ls-transformation|deadline-driven cultures]] do to quality, and I've seen how much better things get when teams have space to do things right.
>
> **Culture** — cross-functional teams, clean code focus, engineer autonomy. I work best in environments where [[ref-agile-leadership#Data-Driven Decision Making|decisions are made with data]], people [[ls-ownership|own their work]], and [[ref-code-review#HOW WE SET IT UP|quality is a habit]], not a gate."

### The Migration Question (they'll ask)
> "I've done this before — different scale, different cloud, same pattern. At Combination, I set up K8s infrastructure with [[ref-terraform#What Terraform Is|Terraform]] and [[ref-kubernetes#Configuration|Kustomize]]. At KocSistem, I took a team from [[do-azdevops-zero|zero automation to daily deployments]] in 6 months.
>
> My approach: [[ref-microservices#Decomposition|strangler fig]] — migrate piece by piece, never big bang. Start stateless, low-risk, high-value. Set up [[ref-github-actions#Reusable Workflows|CI/CD]] early so every migrated service gets automated build/test/deploy from day one.
>
> The people side matters just as much — if the team is new to K8s, I'd pair with them on the first service. Show the value, don't lecture. At KocSistem, the [[ls-transformation|transformation worked]] because I started with a pilot, not a mandate."

### The AWS Question (they'll ask)
> "I've been on Azure — AKS, Key Vault, ACR, Blob Storage, Terraform. Kubernetes is Kubernetes regardless of cloud. Terraform works the same. I'd need to learn EKS, S3, RDS, IAM specifics — the 'which button' details, not the 'how to think about it' part. A sprint to get productive, not a quarter."

### The Vue Question (they might ask)
> "I'm backend-first — C#, microservices, infrastructure. I've worked closely with frontend teams and I understand the contract: API design, data shapes, how frontend performance depends on backend response shapes. I can learn Vue, but my biggest value is cloud/K8s/C#."

### The ShapeUp Question (they might ask)
> "I know the principles — fixed time, variable scope, appetite-based betting, cooldowns. Different from [[ref-agile-ceremonies#Scrum vs Kanban|Scrum]] where you fix scope and flex time. I've done both. ShapeUp cooldowns are especially interesting for a migration — infrastructure progress without competing with feature work."

### Closing
> "What ties everything together: I've been in environments where cutting corners has real consequences — stopped forklifts, delayed vehicle programs, breached SLAs. That taught me to think about the full chain: **code → pipeline → team → process**.
>
> This K8s migration at Lime — building cloud infrastructure from the start, with a product team that values quality and sustainability — that's exactly where I want to be."

---

## Salary Benchmark

Based on the research: Senior SWE in Gothenburg, 10+ years, cloud/K8s focus.
- **Your current:** 67,000 SEK/month
- **Market range:** 60,000–75,000 for Gothenburg senior
- **Your ask:** 67,000–72,000 (at or above current, justified by K8s + architecture + leadership experience)
- **Lime context:** Listed company, stable growth, Gothenburg office. Likely pays market rate, not startup-level. 67k is realistic.

---

## What I Expect From the Company

### Technically
- **Real migration ownership** — not just executing someone else's plan. I want to influence architecture decisions, not just implement tickets.
- **Infrastructure-as-code** — Terraform or equivalent for everything. No portal clicking, no manual deployments.
- **CI/CD from day one** — every migrated service gets automated pipelines immediately. No "we'll add CI later."
- **Testing culture** — real tests with real dependencies ([[ref-testing-strategy#Testcontainers\|Testcontainers]]), not mocks that pass while production breaks.
- **Observability built-in** — [[ref-observability-stack#OpenTelemetry (OTel)\|OpenTelemetry]], centralized logging, distributed tracing. Not "we'll add monitoring later."
- **Code review as standard** — [[ref-code-review#What Makes a Good Review\|meaningful reviews]], not rubber stamps.

### Culturally
- **Autonomy with accountability** — senior means owning decisions and outcomes, not asking permission for every PR.
- **Data over opinions** — disagreements settled with [[ref-agile-leadership#Data-Driven Decision Making\|experiments and metrics]], not hierarchy.
- **Sustainable pace** — ShapeUp's "no deadlines" promise matters. I've seen what [[ls-transformation\|deadline-driven cultures]] do to quality.
- **Learning is part of the job** — AWS is new to me, and I expect time to learn it properly, not "figure it out in your spare time."
- **Engineers talk to the problem** — I want access to the "why" behind features, not just Jira tickets. At KocSistem, [[ag-alignment\|sprint goals]] worked because we understood the business context.
- **Clean code is non-negotiable** — their JD says "clean/maintainable code focused" — I want to see that in practice, not just on paper.

---

## Prep Checklist

- [ ] Read about ShapeUp methodology (basecamp.com/shapeup)
- [ ] Review AWS vs Azure mapping: EKS/AKS, S3/Blob, RDS/SQL, ElastiCache/Redis, IAM/Entra
- [ ] Review [[ref-kubernetes#What Kubernetes Is\|Kubernetes]] — Combination setup, migration angles
- [ ] Review [[ref-terraform#What Terraform Is\|Terraform]] — cloud-agnostic IaC story
- [ ] Review [[ref-redis#What Redis Is\|Redis]] — caching patterns, Sentinel
- [ ] Review [[ref-sql-databases#What SQL Databases Are\|SQL Server]] — performance, Dapper vs EF
- [ ] Review [[ref-testing-strategy#What a Testing Strategy Is\|Testing]] — pyramid, Testcontainers
- [ ] Review [[ref-ways-of-working#The DRIVE Framework\|Ways of Working]] — DRIVE, leadership stories
- [ ] Review [[ref-csharp#Q6. What happens under the hood when you `await` a Task?\|C# Async]] — DI, modern features
- [ ] Prepare 3 STAR stories: [[ref-ways-of-working#Leadership — CI/CD Pilot\|CI/CD Pilot]], [[ref-ways-of-working#Proud — Full Transformation Arc at KocSistem\|KocSistem Arc]], [[ref-ways-of-working#Uncertainty — New Domain\|New Domain]]

---

*[[00-dashboard\|Dashboard]]*
