---
tags:
  - education-kit
---

# Education Catalog — Software Engineering Knowledge Base

> [!tip] Generic bilgi kataloğu. Şirket spesifik değil, saf konsept ve araç bilgisi. Interview kit'teki ref dosyalarından türetilmiş, deneyim referansları çıkarılmış.

## Skill Map

| | | | |
|---|---|---|---|
| <span style="font-size:1.3em">**BACKEND & API**</span> | <span style="font-size:1.3em">**DATA & MESSAGING**</span> | <span style="font-size:1.3em">**INFRA & DEVOPS**</span> | <span style="font-size:1.3em">**PRACTICES & SOFT SKILLS**</span> |
| [[edu-csharp\|C# / .NET]] | [[edu-kafka\|Kafka]] | [[edu-docker\|Docker]] | [[edu-microservices\|Microservice Patterns]] |
| [[edu-python\|Python]] | [[edu-rabbitmq\|RabbitMQ]] | [[edu-kubernetes\|Kubernetes]] | [[edu-design-patterns\|Design Patterns]] |
| [[edu-graphql\|GraphQL]] | [[edu-mongodb\|MongoDB]] | [[edu-terraform\|Terraform]] | [[edu-distributed-systems\|Distributed Systems]] |
| [[edu-grpc\|gRPC]] | [[edu-sql\|SQL Databases]] | [[edu-github-actions\|GitHub Actions]] | [[edu-testing\|Testing Strategy]] |
| [[edu-rest\|REST APIs]] | [[edu-redis\|Redis]] | [[edu-azure-devops\|Azure DevOps]] | [[edu-code-review\|Code Review]] |
| [[edu-ddd-cqrs\|DDD & CQRS]] | [[edu-elasticsearch\|Elasticsearch]] | [[edu-ansible\|Ansible]] | [[edu-agile\|Agile & Scrum]] |
| [[edu-web-fundamentals\|Web Fundamentals]] | | [[edu-cicd-security\|CI/CD Security]] | [[edu-leadership\|Technical Leadership]] |
| [[edu-web-advanced\|Web Advanced]] | | [[edu-observability\|Observability (OTel)]] | [[edu-system-design\|System Design]] |
| [[edu-frontend\|Frontend Frameworks]] | | [[edu-grafana\|Grafana & Prometheus]] | [[edu-estimation\|Back-of-Envelope Estimation]] |
| [[edu-owasp\|Application Security]] | | [[edu-dora\|DORA Metrics]] | [[edu-performance\|Performance Profiling]] |

---

## Topic Detail

### Backend & API

| Topic | Key Concepts | Level |
|-------|-------------|-------|
| **[[edu-csharp\|C# / .NET]]** | Async/await, DI lifetimes, LINQ, GC, records, pattern matching, Span\<T\>, source generators, Minimal APIs, EF Core, gRPC in .NET, SignalR, background services | Advanced |
| **[[edu-python\|Python]]** | Dict internals, GIL, decorators, generators, asyncio, metaclasses, typing, pytest, packaging, match/case, CLI tools | Advanced |
| **[[edu-graphql\|GraphQL]]** | Schema, resolvers, federation, DataLoader, N+1, persisted queries, depth limiting, introspection, versioning | Advanced |
| **[[edu-grpc\|gRPC]]** | Protocol Buffers, HTTP/2, streaming, versioning, breaking changes, interceptors, deadlines, vs REST vs GraphQL | Intermediate |
| **[[edu-rest\|REST APIs]]** | Resource design, HTTP methods, idempotency, versioning, caching, rate limiting, HATEOAS, OpenAPI | Intermediate |
| **[[edu-ddd-cqrs\|DDD & CQRS]]** | Bounded contexts, aggregates, domain events, CQRS, clean architecture, repository pattern, event sourcing | Advanced |
| **[[edu-web-fundamentals\|Web Fundamentals]]** | HTTP lifecycle, TLS, status codes, headers, WebSocket, SSE, JWT, OAuth, pagination, caching, CORS | Intermediate |
| **[[edu-web-advanced\|Web Advanced]]** | OAuth2/OIDC, service mesh, rate limiting algorithms, connection pooling, CDN invalidation, HTTP/3 QUIC, zero trust, event-driven patterns, serialization formats | Advanced |
| **[[edu-frontend\|Frontend Frameworks]]** | React hooks/RSC/Next.js, Angular signals, Vue Composition, Blazor, SSR/CSR/SSG, state management, Core Web Vitals, Playwright, micro-frontends, Web Components | Intermediate |
| **[[edu-owasp\|Application Security]]** | OWASP Top 10, injection, XSS, CSRF, SSRF, broken auth, cryptographic failures, security logging, deserialization | Intermediate |

### Data & Messaging

| Topic | Key Concepts | Level |
|-------|-------------|-------|
| **[[edu-kafka\|Kafka]]** | Topics, partitions, consumer groups, offsets, replication, exactly-once, vs RabbitMQ, schema evolution | Advanced |
| **[[edu-rabbitmq\|RabbitMQ]]** | Exchanges, queues, bindings, routing keys, clustering, split-brain, quorum queues, consumer patterns, chaos testing | Advanced |
| **[[edu-mongodb\|MongoDB]]** | Document model, BSON, transactions, indexes, aggregation pipeline, replica sets, sharding, vs SQL, vs PostgreSQL | Intermediate |
| **[[edu-sql\|SQL Databases]]** | ACID, indexing, execution plans, connection pooling, bulk operations, migrations, Dapper vs EF, query optimization | Intermediate |
| **[[edu-redis\|Redis]]** | Data structures, Streams, pub/sub, caching patterns, Sentinel, eviction policies, persistence (RDB/AOF), vs Memcached | Intermediate |
| **[[edu-elasticsearch\|Elasticsearch]]** | Index/shard model, full-text search, analyzers, aggregations, bulk API, index lifecycle, vs SQL LIKE | Intermediate |

### Infrastructure & DevOps

| Topic | Key Concepts | Level |
|-------|-------------|-------|
| **[[edu-docker\|Docker]]** | Containers vs VMs, multi-stage builds, layer caching, .dockerignore, ENTRYPOINT vs CMD, image tagging, Kaniko, vs K8s | Intermediate |
| **[[edu-kubernetes\|Kubernetes]]** | Pod/Deployment/Service, health probes, resource requests/limits, HPA/KEDA, rolling updates, PDB, Kustomize vs Helm, Cilium, secrets, RBAC | Advanced |
| **[[edu-terraform\|Terraform]]** | HCL, state management, plan/apply, modules, workspaces, drift detection, vs Pulumi vs CloudFormation, vs Ansible | Intermediate |
| **[[edu-github-actions\|GitHub Actions]]** | Workflows, actions, reusable workflows, matrix builds, environments, secrets, vs Azure DevOps vs Jenkins | Intermediate |
| **[[edu-azure-devops\|Azure DevOps]]** | YAML pipelines, templates, service connections, approval gates, vs GitHub Actions | Intermediate |
| **[[edu-ansible\|Ansible]]** | Playbooks, inventory, idempotency, roles, CI integration, vs shell scripts, vs Terraform | Beginner |
| **[[edu-cicd-security\|CI/CD Security]]** | Shift-left, dependency scanning, SAST, secret detection, quality gates, secrets management | Intermediate |
| **[[edu-observability\|Observability (OTel)]]** | OpenTelemetry, distributed tracing, Tempo, Loki, Alloy, three pillars (metrics/logs/traces), vs monitoring | Advanced |
| **[[edu-grafana\|Grafana & Prometheus]]** | Pull-based metrics, PromQL, dashboards, RED/USE methods, alerting, DORA integration | Intermediate |
| **[[edu-dora\|DORA Metrics]]** | Deployment frequency, lead time, change failure rate, MTTR, elite vs low performers | Beginner |

### Practices & Soft Skills

| Topic | Key Concepts | Level |
|-------|-------------|-------|
| **[[edu-microservices\|Microservice Patterns]]** | Sync vs async, database per service, saga, circuit breaker, service discovery, decomposition, vs monolith, anti-patterns | Advanced |
| **[[edu-design-patterns\|Design Patterns]]** | Repository, Factory, Strategy, Observer, Decorator, CQRS, Mediator, composition vs inheritance, anti-patterns | Intermediate |
| **[[edu-distributed-systems\|Distributed Systems]]** | CAP theorem, consistency models, Raft consensus, saga vs 2PC, idempotency, split-brain, vector clocks | Advanced |
| **[[edu-testing\|Testing Strategy]]** | Test pyramid, unit vs integration vs E2E, Testcontainers, mocking vs real, WebApplicationFactory, breaking change detection | Intermediate |
| **[[edu-code-review\|Code Review]]** | Review checklist (security→correctness→performance→maintainability→tests), quality gates, branch strategy, anti-patterns | Intermediate |
| **[[edu-agile\|Agile & Scrum]]** | Standup, planning, retro, review, DoD, Scrum roles, Scrum vs Kanban, ceremony optimization | Intermediate |
| **[[edu-leadership\|Technical Leadership]]** | OKRs, servant leadership, blameless post-mortems, psychological safety, data-driven decisions, change management, mentoring | Advanced |
| **[[edu-system-design\|System Design]]** | 5-step framework, requirements clarification, high-level design, deep dive, trade-offs, capacity planning | Advanced |
| **[[edu-estimation\|Back-of-Envelope Estimation]]** | QPS formula, storage formula, reference numbers, powers of 2, time conversions, worked examples | Intermediate |
| **[[edu-performance\|Performance Profiling]]** | .NET profiling tools, N+1 queries, memory leaks, GC pressure, database performance, API performance | Intermediate |

---

## Learning Path Suggestions

### Junior → Mid Backend Engineer
1. [[edu-csharp\|C#/.NET fundamentals]] → [[edu-rest\|REST API design]] → [[edu-sql\|SQL basics]]
2. [[edu-docker\|Docker]] → [[edu-testing\|Testing strategy]] → [[edu-code-review\|Code review]]
3. [[edu-web-fundamentals\|Web fundamentals]] → [[edu-owasp\|Security basics]] → [[edu-design-patterns\|Design patterns]]

### Mid → Senior Backend Engineer
1. [[edu-microservices\|Microservice patterns]] → [[edu-distributed-systems\|Distributed systems]] → [[edu-kafka\|Kafka]] or [[edu-rabbitmq\|RabbitMQ]]
2. [[edu-kubernetes\|Kubernetes]] → [[edu-terraform\|Terraform]] → [[edu-observability\|Observability]]
3. [[edu-graphql\|GraphQL]] or [[edu-grpc\|gRPC]] → [[edu-ddd-cqrs\|DDD/CQRS]] → [[edu-system-design\|System design]]
4. [[edu-performance\|Performance]] → [[edu-cicd-security\|CI/CD security]] → [[edu-dora\|DORA metrics]]

### Senior → Staff / Tech Lead
1. [[edu-leadership\|Technical leadership]] → [[edu-agile\|Agile practices]] → [[edu-estimation\|Estimation]]
2. [[edu-system-design\|System design]] → [[edu-distributed-systems\|Distributed systems]] → [[edu-web-advanced\|Web advanced]]
3. [[edu-microservices\|Microservices vs monolith]] → [[edu-design-patterns\|Architectural patterns]] → [[edu-performance\|Performance at scale]]

---

## Status Tracker

| Topic | Status | Notes |
|-------|--------|-------|
| C# / .NET | 🟢 Strong | 10yr, 95 questions covered |
| Python | 🟢 Strong | 95 questions covered |
| GraphQL | 🟢 Strong | Federation, DataLoader, migration |
| gRPC | 🟢 Strong | 100+ protos, versioning |
| REST | 🟢 Strong | 10yr, design principles |
| Kafka | 🟡 Good | Core model, vs RabbitMQ |
| RabbitMQ | 🟢 Strong | Split-brain experience |
| MongoDB | 🟢 Strong | Custom extensions, transactions |
| SQL | 🟢 Strong | Performance tuning, bulk ops |
| Redis | 🟢 Strong | Streams, Sentinel, scaling |
| Docker | 🟢 Strong | Multi-stage, layer caching |
| Kubernetes | 🟢 Strong | 60+ svc, custom probes, HPA |
| Terraform | 🟢 Strong | State mgmt, drift, modules |
| GitHub Actions | 🟢 Strong | Reusable workflows, 60+ svc |
| Observability | 🟡 Good | OTel, Tempo, Loki stack |
| Testing | 🟢 Strong | Testcontainers, E2E, breaking |
| Microservices | 🟢 Strong | 60+ svc architecture |
| Distributed Systems | 🟡 Good | CAP, split-brain experience |
| System Design | 🟡 Good | Framework + practice problems |
| Frontend | 🟡 Learning | React/Vue/Angular concepts |
| DDD/CQRS | 🟢 Strong | 30+ svc at Toyota |
| Leadership | 🟢 Strong | 25 engineers, transformation |
