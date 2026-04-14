---
tags:
  - interview-kit
  - interview-kit/software-dev
up: [[10-pillar-software-dev]]
---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]] > COMBINATION AB*

# COMBINATION AB — Software Development

Combination AB builds a microservices platform in .NET 9. I joined as a Senior Software Engineer in April 2025. The platform has 60+ microservices, each handling one domain — user management, billing, data processing, reporting. Everything runs on [[ref-kubernetes#Configuration|Kubernetes]] in [[ref-docker#Multi-Stage Builds|Docker]] containers, deployed multiple times a day through [[ref-github-actions#Reusable Workflows|GitHub Actions]] with reusable workflows from a shared workflow library, plus [[ref-grpc#Versioning|breaking change]] detection for [[ref-grpc#Versioning|gRPC]] protos and [[ref-graphql#Federation (HotChocolate Fusion)|GraphQL]] schemas.

## Tools I Use Here
| Tool | Ref | Tool | Ref |
|------|-----|------|-----|
| [[ref-graphql\|GraphQL]] | HotChocolate Fusion, federation | [[ref-grpc\|gRPC]] | 100+ protos, versioned APIs |
| [[ref-kafka\|Kafka]] | async events, CDeploy topics | [[ref-rest\|REST]] | external partner APIs |
| [[ref-docker\|Docker]] | multi-stage, .commons pattern | [[ref-kubernetes\|Kubernetes]] | 60+ services, Kustomize, HPA |
| [[ref-terraform\|Terraform]] | AKS, Cilium, Contour, ACR | [[ref-github-actions\|GitHub Actions]] | reusable workflows, breaking changes |
| [[ref-cdeploy\|CDeploy]] | Python deployment framework | [[ref-testing-strategy\|Testing]] | Testcontainers, E2E, breaking changes |
| [[ref-observability-stack\|OTel/Tempo/Loki]] | traces, logs, Grafana Alloy | [[ref-ai-tooling\|AI Tools]] | Cursor + Claude Code |
| [[ref-mongodb\|MongoDB]] | GP-ServiceBase integration | [[ref-code-review\|Code Review]] | PRs, CODEOWNERS, quality gates |

My day-to-day is building and maintaining these services. I write the business logic, set up the API contracts, and keep the services healthy in production. We use three API styles depending on the consumer: GraphQL for internal frontends, gRPC for [[ref-grpc#When to Use|service-to-service]] communication, and [[ref-rest#When to Use REST vs Alternatives|REST]] for external partners. [[ref-kafka#Core Model|Kafka]] handles async events between services. When I joined, everything was REST and the frontend was making too many requests per page. I [[sd-graphql-migration|led the migration to GraphQL]] and established clear rules for when to use which protocol.

I own the API layer and the thinking around it. I also own the performance side — when an endpoint is slow, I dig into query plans, serialization costs, and how [[ref-graphql#DataLoader & N+1 Problem|resolver]]s interact with the database. I profile slow services regularly and fix the actual root cause rather than just adding caches.

I also own the testing strategy across our services. Every service follows the same test pyramid — [[ref-testing-strategy#Test Pyramid|unit tests]] with xUnit and NSubstitute, [[ref-testing-strategy#Testcontainers|component tests]] with real MongoDB via Testcontainers, [[ref-testing-strategy#E2E Test Patterns|E2E tests]] in both C# (gRPC) and TypeScript (GraphQL), and [[ref-testing-strategy#Breaking Change Detection|breaking change detection]] for proto and schema compatibility. We moved from mocking databases to Testcontainers early on after mocked tests passed but production broke.

On the infrastructure side, I maintain the CI/CD pipelines, manage Docker image optimization, configure Kubernetes [[ref-kubernetes#Health Probes|health probes]], and handle container registry management. I maintain the [[ref-cdeploy#What CDeploy Manages|Python CDeploy framework]] for deployment orchestration — managing Azure AKS clusters, CloudFlare DNS, Kubernetes resources, and Kafka topics. Every service is instrumented with [[ref-observability-stack#OpenTelemetry (OTel)|OpenTelemetry]] — traces flow through [[ref-observability-stack#Grafana Alloy (Collection Agent)|Grafana Alloy]] to [[ref-observability-stack#Grafana Tempo (Distributed Tracing)|Tempo]], logs via Promtail to [[ref-observability-stack#Grafana Loki (Log Aggregation)|Loki]].

I use AI-assisted development tools daily — [[sd-ai-tools|Cursor and Claude Code]] ([[ref-ai-tooling#Workflow Integration — My Rules|workflow and rules]]). Cursor for in-editor code generation, refactoring, and test scaffolding. Claude Code for complex multi-file tasks, architecture exploration, and documentation generation. I've developed a practical sense for where AI tools actually speed you up (boilerplate, tests, repetitive patterns) vs where they slow you down (complex business logic, security-critical code, architecture decisions). The key is knowing when to trust the output and when to think for yourself.

## Key Experiences
- [[sd-graphql-migration|GRAPHQL — Migration — REST→GraphQL gradual rollout, 6 months, zero breaking changes]]
- [[sd-ai-tools|AI TOOLS — Cursor + Claude Code — daily usage, best practices, knowing when to trust vs verify]]

---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]]*
