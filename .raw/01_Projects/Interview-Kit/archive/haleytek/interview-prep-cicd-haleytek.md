# CI/CD Engineer Interview Prep Script

## Opening (2-3 dk)

> I've been in software engineering for over 10 years, and for the last 4-5 years my work has been heavily centered on CI/CD, release engineering, and DevOps infrastructure.
>
> The most directly relevant experience is my time at **Volvo Cars** as a **Software Factory Engineer**. I was responsible for the release pipeline infrastructure for embedded automotive software — safety-critical systems where a broken build isn't just an inconvenience, it can block an entire vehicle program. I built and maintained release pipelines using **Gerrit** for code review with automated triggers, wrote the automation layer in **Python** on **Linux**, and cut the overall QA and gating cycle time by 30%. Every release I shipped had zero compliance findings.
>
> Before that, at **KoçSistem**, I drove a full **DevOps transformation** — from zero CI/CD to fully automated pipelines on **Azure DevOps** for 10+ applications. I set up quality gates, security scanning, standardized Git workflows, and we measured everything with **DORA metrics**. The results were concrete: 55% fewer bugs in releases, doubled deployment frequency, zero pen test findings, and DevSecOps Four Key Metrics at 75%.
>
> Right now at **Combination AB**, I work daily with **Kubernetes, Docker, Azure DevOps, and GitHub Actions** — building CI/CD for .NET 9 microservices with REST, GraphQL, and gRPC endpoints.

---

## Deep Dive: CI/CD Pipeline Architecture

> At Volvo, the pipeline wasn't a simple build-test-deploy. Embedded automotive software has a completely different pipeline topology:
>
> **Build stage** — The build system was **Cynosure** (Volvo's internal build framework). I wrote Python wrappers that configured the build environment, pulled the correct toolchain versions, set target-specific compiler flags, and kicked off parallel builds for multiple hardware targets. If a build variant failed, the pipeline had to report exactly which target and which commit broke it — not just "build failed."
>
> **Test stage** — Unit tests ran in the pipeline, but the real challenge was integration testing against **hardware-in-the-loop (HIL)** setups. I set up the pipeline to reserve HIL rigs, flash the built firmware, run the test suite, collect results, and release the rig — all automated. If a rig was busy, the pipeline queued and retried rather than failing.
>
> **Gating stage** — Every release had to pass a formal gate: static analysis clean, test coverage above threshold, no open critical bugs, regulatory documentation generated and attached. I automated the gate check as a Python script that pulled data from multiple sources (test reports, bug tracker, analysis tools) and produced a go/no-go verdict with a full audit trail.
>
> **Release stage** — Once gated, the release was packaged, signed, and pushed to the artifact repository with full traceability — you could trace any binary back to the exact commit, build configuration, and test results.
>
> The key design principle was treating the pipeline as a **state machine** — each stage had explicit entry criteria, exit criteria, and rollback behavior. The pipeline config itself was version-controlled and reviewed through the same Gerrit workflow as the product code.

---

## Gerrit Workflow & Triggers

> At Volvo, **Gerrit** was the core of our code review and CI trigger system. I didn't just use it — I was involved in maintaining the Gerrit instance and configuring the trigger integrations.
>
> **Setup & configuration** — Our Gerrit was running on a dedicated Linux server. I managed project configurations (project.config), set up access control rules per repository — who can push, who can submit, which groups can bypass review for automation accounts. I configured **label definitions** (Verified, Code-Review) with custom score ranges and set up submit rules to enforce that both labels had to pass before a change could be merged.
>
> **Gerrit triggers** — We had webhook-based triggers that fired on specific Gerrit events: `patchset-created`, `change-merged`, `comment-added`. When a developer pushed a new patchset, the trigger kicked off the verification pipeline automatically. The pipeline ran the build + tests, and then posted the result back to Gerrit as a `Verified +1` or `Verified -1` label via Gerrit's REST API. I wrote the integration script that did this — it authenticated with an API token, posted the review, and included a link to the build log so reviewers could see exactly what passed or failed.
>
> **Practical challenges I solved:**
>
> - **Flaky triggers** — Sometimes the webhook would fire but the pipeline wouldn't start. I added a retry mechanism and a dead-letter log so we could audit missed triggers.
> - **Multi-repo dependencies** — Some changes needed to land across multiple repos simultaneously. I configured Gerrit topic-based submissions so related changes across repos could be reviewed and submitted together.
> - **Rebase conflicts** — In a high-velocity team, patchsets would go stale. I set up auto-rebase in Gerrit so that when a dependency merged, downstream changes would automatically rebase and re-trigger verification.
> - **Access control for service accounts** — The CI system needed a service account that could post reviews and fetch code. I configured this with minimal permissions — read access + label permissions only, no submit rights — following the principle of least privilege.

---

## Containerization & Kubernetes

> At Combination, I work with **Docker and Kubernetes** daily. Some concrete things I've done:
>
> **Docker** — I've written multi-stage Dockerfiles for .NET 9 services: first stage builds with the SDK image, second stage runs on the slim ASP.NET runtime image. This keeps production images around 80-100MB instead of 800MB+. I've debugged layer caching issues where a misplaced `COPY` invalidated the cache and made builds take 10 minutes instead of 2. I've also set up `.dockerignore` properly — I've seen pipelines fail because someone accidentally included `node_modules` or `.git` in the build context.
>
> **Kubernetes** — I've configured deployments with proper health probes (liveness, readiness, startup), resource requests and limits, and rolling update strategies. For CI/CD pipelines specifically, I understand the model of running build tasks as **Kubernetes pods** — each build gets its own pod with the right tools, runs in isolation, and the pod is cleaned up afterward. This gives you dynamic scaling (cluster autoscaler spins up nodes when the build queue grows) and strong isolation between builds.
>
> **Azure Container Registry** — I've set up ACR, configured image retention policies to avoid storage bloat, and integrated it with pipelines so that every merge to main produces a tagged image pushed to the registry with the commit SHA and semantic version.
>
> **Tekton** — I haven't used Tekton in production, but I understand the architecture: Tasks and Pipelines are Kubernetes CRDs, each step runs as a container in a pod, and workspaces map to PVCs for sharing data between steps. Coming from Azure DevOps YAML pipelines, the concepts map directly — the main shift is that Tekton is cluster-native, so you're managing pipelines with `kubectl` and they benefit from Kubernetes scheduling, resource management, and RBAC natively.

---

## Infrastructure as Code — Terraform

> At KoçSistem, I owned the infrastructure direction. I've worked with **Terraform** for provisioning Azure resources — resource groups, App Services, SQL databases, Key Vault instances, and networking.
>
> **State management** — I've configured remote state backends on Azure Blob Storage with state locking to prevent concurrent modifications. I've also dealt with state drift — when someone manually changes a resource in the portal, `terraform plan` catches it, and you have to decide whether to import the change or revert it.
>
> **In CI/CD pipelines** — I've set up Terraform as a pipeline stage: `terraform init` → `terraform plan` (saved to a file) → manual approval gate → `terraform apply` (from the saved plan). The plan output is posted as a comment on the pull request so reviewers can see exactly what infrastructure changes the code will produce before approving.
>
> **Module structure** — I've organized Terraform code into reusable modules — one module for a "standard web app" that provisions App Service + SQL + Key Vault + monitoring, parameterized per environment (dev/staging/prod). This way, spinning up a new environment is a single module call with different variables.

---

## Observability Stack

> I've worked with **Prometheus and Grafana** for monitoring — but more importantly, I understand how observability fits into CI/CD.
>
> **Pipeline observability** — At KoçSistem, I tracked **DORA metrics**: deployment frequency, lead time for changes, change failure rate, and mean time to restore. These weren't vanity metrics — I reported them to leadership and used them to justify infrastructure investments. Getting these to 75% implementation was one of my key achievements as Technology Manager.
>
> **Application observability** — I'm familiar with the **OpenTelemetry** instrumentation model: add OTel SDKs to your services, configure exporters, and route telemetry to backends. The stack here — **Tempo for distributed traces, Loki for log aggregation, InfluxDB for metrics, Grafana for visualization** — is a well-known pattern. The OTel Collector sits in the middle, receiving data from services and routing it to the right backend.
>
> **Practical experience** — I've set up Grafana dashboards for tracking build times, test pass rates, and deployment success rates. I've also configured alerting — if the pipeline failure rate spikes above a threshold, the team gets notified before it becomes a bottleneck.

---

## Security in CI/CD

> At KoçSistem, I was responsible for the security posture of all applications. We achieved **zero penetration test findings**, which means security was embedded in the pipeline, not bolted on afterward.
>
> **Pipeline security practices I've implemented:**
>
> - **Dependency scanning** — Every build runs a dependency check. If a critical CVE is found in a transitive dependency, the build fails with a clear message pointing to the vulnerable package and the recommended fix version.
> - **Static analysis** — Code quality and security rules enforced at build time. SonarQube-style quality gates that block merges if new code introduces security hotspots.
> - **Secrets management** — I've used **Azure Key Vault** integrated into pipelines — secrets are pulled at runtime via service connections, never hardcoded in YAML or environment variables. The pattern is the same as **HashiCorp Vault with AppRole auth**: the pipeline authenticates, gets a short-lived token, retrieves secrets, and they exist only in memory during the build.
> - **Image scanning** — Container images are scanned before being pushed to the registry. If a critical vulnerability is found in the base image, the pipeline fails and the team is notified to update the Dockerfile.
> - **Network policies** — Build pods in Kubernetes should have restricted network access — they only need to reach the source repo, artifact registry, and test environments. No outbound internet access unless explicitly allowed.

---

## Messaging & Data (Redis, RabbitMQ, PostgreSQL)

> I've worked with both **Redis** and **RabbitMQ** in production.
>
> **RabbitMQ** — At Toyota Material Handling, our microservices communicated via RabbitMQ. I've configured exchanges, queues, and bindings. In a CI/CD context, I've set up pipeline stages that spin up a RabbitMQ container for integration testing — the test suite publishes messages and verifies that consumers process them correctly, then the container is torn down.
>
> **Redis** — At KoçSistem, I worked with Redis for caching and session management. In pipelines, I've used Redis as a shared cache for build artifacts between stages — faster than pulling from blob storage for frequently accessed dependencies.
>
> **PostgreSQL** — I've set up database migration stages in pipelines — the pipeline runs migrations against a test database, runs integration tests, and only if everything passes does the migration get applied to staging/production. This prevents broken migrations from reaching environments where rollback is painful.

---

## Airflow (Workflow Orchestration)

> I haven't used **Apache Airflow** directly, but at Volvo I built what was essentially the same thing — a workflow orchestration system for release pipelines in Python.
>
> I understand Airflow's model: DAGs define task dependencies, the scheduler triggers tasks based on dependencies and schedules, and there's a UI for monitoring and manual intervention. In a CI/CD context, Airflow makes sense for orchestrating complex release workflows that go beyond what a simple pipeline can express — things like: "run nightly builds, then fan out integration tests across 5 hardware targets, then aggregate results, then generate a release report, then notify the release manager."
>
> The Python foundation means I could get productive with Airflow quickly — writing DAGs, custom operators, and hooking them into existing CI/CD infrastructure.

---

## Kapanış

> What I bring is not just tool experience — it's the discipline of building CI/CD in **safety-critical environments**. At Volvo, a broken pipeline didn't just slow down developers, it could delay an entire vehicle program with regulatory implications. That taught me to treat pipelines as production systems — they need monitoring, they need tests, they need runbooks, and they need someone who understands both the tooling and the domain.
>
> I've also led DevOps transformations from zero — I know what it takes to get a team from "we deploy manually" to "we deploy 10 times a day with confidence." And my management experience means I can communicate pipeline health and infrastructure needs in business terms, not just technical jargon.

---

## Quick Reference: Zayif Noktalarda Strateji

| Soru | Cevap Stratejisi |
|------|-------------------|
| "Have you used Tekton?" | "Not in production, but I understand the CRD model — Tasks, Pipelines, Workspaces. It maps well to Azure DevOps YAML stages. I'd need a sprint to get fluent, not a quarter." |
| "How about Airflow?" | "I built similar orchestration at Volvo in Python. Airflow's DAG model formalizes what I was doing manually. I'd focus on learning the operator ecosystem and scheduler tuning." |
| "Traefik / OAuth2 Proxy?" | "I've configured reverse proxies and auth layers, but not these specific tools. The pattern is the same — route traffic, terminate TLS, enforce auth before hitting the service." |
| "InfluxDB vs Prometheus?" | "Prometheus is pull-based, InfluxDB is push-based. InfluxDB handles high-cardinality time-series data better. Both feed into Grafana. I've used Prometheus; InfluxDB's InfluxQL/Flux query language would be new." |
| Bilmedigin bir sey | "I haven't worked with that directly — I'd want to look at your setup and docs before giving you a confident answer. But here's how I'd approach learning it: [concrete plan]." |
