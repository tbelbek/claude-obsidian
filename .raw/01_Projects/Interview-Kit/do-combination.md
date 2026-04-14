---
tags:
  - interview-kit
  - interview-kit/devops
up: [[11-pillar-devops]]
---

*[[00-dashboard|Home]] > [[11-pillar-devops|DevOps]] > COMBINATION AB*

# COMBINATION AB — DevOps

At Combination, I own the CI/CD pipelines and container infrastructure for our .NET 9 microservices. Each service has its own pipeline in [[ref-github-actions#Reusable Workflows|GitHub Actions]] with reusable workflows from a shared workflow library (DevEnv-GitHub-Workflows) — build, test, scan, push image, deploy. CI includes [[ref-grpc#Versioning|breaking change]] detection for gRPC proto files and GraphQL schemas.

## Tools I Use Here
| Tool | Ref | Tool | Ref |
|------|-----|------|-----|
| [[ref-docker\|Docker]] | multi-stage, .commons, ACR | [[ref-kubernetes\|Kubernetes]] | probes, HPA, Kustomize |
| [[ref-github-actions\|GitHub Actions]] | reusable workflows | [[ref-terraform\|Terraform]] | AKS infrastructure |
| [[ref-cdeploy\|CDeploy]] | Python deployment framework | [[ref-observability-stack\|OTel/Tempo/Loki]] | traces, logs, metrics |

What I own long-term here is the [[ref-docker#Multi-Stage Builds|Docker]] and [[ref-kubernetes#Configuration|Kubernetes]] layer. I standardized a `.commons/Dockerfile` pattern across all 60+ services, restructured them as [[ref-docker#HOW WE USE IT|multi-stage builds]], set up [[ref-kubernetes#HOW WE USE IT|health probes]] for every service, and manage the Azure Container Registry with retention policies. I use [[ref-kubernetes#Configuration|Kustomize]] for Kubernetes deployment [[ref-kubernetes#Configuration|overlays]] — base configs with dev/staging/prod overrides. Terraform manages the underlying AKS cluster infrastructure (GP-IaC-K8s-AKS, GP-IaC-AKS) — provisioning, networking, and [[ref-kubernetes#Configuration|Helm]] chart deployments. Before I set up the cleanup rules, registry storage tripled in 3 months — nobody was deleting old images.

I also maintain the [[ref-cdeploy#What CDeploy Manages|Python CDeploy framework]] for infrastructure automation — managing AKS clusters, CloudFlare DNS, Kubernetes resources, Kafka topics, and GraphQL schema configuration. The team deploys multiple times a day, and I make sure the pipeline stays fast and reliable. When something slows down — a build taking 10 minutes instead of 2 — I'm the one who digs in and fixes it.

## Key Challenges
- [[ref-docker#HOW WE USE IT|DOCKER — Caching — COPY order broke layers, 10min→2min]]
- [[ref-kubernetes#HOW WE USE IT|K8S — Health Probes — 45s startup → restart loop, startup probe fix]]

## Sorulursa

> [!faq]- "What's your long-term goal for the CI/CD setup here?"
> We're gradually moving from Azure DevOps to GitHub Actions for a better developer experience. I'm also working on standardizing the Kubernetes deployment configs — right now each service has slightly different probe settings and [[ref-kubernetes#Resource Management|resource limits]]. I want a baseline template that covers 80% of cases, with overrides for services that need something different.

---

*[[00-dashboard|Home]] > [[11-pillar-devops|DevOps]]*
