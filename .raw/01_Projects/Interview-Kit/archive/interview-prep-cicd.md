---
tags:
  - interview-kit
  - interview-kit/company
---

# CI/CD Engineer Interview Preparation — Haleytek

*[[interview-kit/00-dashboard]] | [[interview-kit/01-script]] | [[interview-kit/ref-ways-of-working#Behavioral Stories — STAR Format|Stories]]*

**Target Role:** CI/CD Engineer
**Format:** Short intro (5 min) + Q&A. Detail sections linked below — only dive in if asked.

---

## Quick Reference — Last Minute Scan

| Must Mention | Key Phrase |
|--------------|------------|
| **Experience** | 10+ years, CI/CD pipelines, release engineering, DevOps transformation |
| **Current** | Combination AB — K8s, Docker, Azure DevOps, GitHub Actions |
| **Key Role** | Volvo Cars — Software Factory Engineer, Gerrit, embedded release pipelines |
| **Key Wins** | 30% QA cycle cut, 2x release frequency, zero compliance findings, zero pen-test findings |
| **Industries** | Automotive embedded (Volvo), industrial automation (Toyota), enterprise (KoçSistem) |

---

## The Script — Compact Version (5 min)

> "I've been in software engineering for over 10 years. The last 4-5 years, my focus has been CI/CD, release engineering, and DevOps infrastructure.
>
> Most relevant is my time at **Volvo Cars** as a **Software Factory Engineer**. I built and maintained release pipelines for embedded automotive software — safety-critical systems where a broken build can block an entire vehicle program. I worked hands-on with **Gerrit** — not just as a user but maintaining the instance, configuring trigger integrations, writing the Python automation that connected Gerrit events to our build system and posted verification results back. I automated the QA gating process and cut the release cycle time by 30%. Every release shipped with zero compliance findings. *(Detail istenirse: [[#Gerrit Deep Dive]] | [[#Pipeline Architecture Deep Dive]])*
>
> Before that, at **KoçSistem**, I drove a DevOps transformation from zero — no CI/CD, no code review, no branching strategy. I built **Azure DevOps pipelines** with shared YAML templates, integrated **security scanning** and quality gates, set up **Terraform** for infrastructure, and tracked everything with **DORA metrics**. Results: 55% fewer bugs, doubled deployment frequency, zero pen-test findings. *(Detail istenirse: [[#Terraform Deep Dive]] | [[#Security Deep Dive]] | [[#Observability Deep Dive]])*
>
> Currently at **Combination AB**, I work daily with **Kubernetes and Docker** — multi-stage builds, health probes, rolling updates, ACR image management — and maintain CI/CD pipelines in Azure DevOps and GitHub Actions for .NET 9 microservices. *(Detail istenirse: [[#Docker & Kubernetes Deep Dive]])*
>
> I've also worked with **RabbitMQ** at Toyota for real-time messaging in autonomous forklift orchestration, and **Redis** and **PostgreSQL** in pipeline contexts — integration testing with sidecar containers, database migration stages. *(Detail istenirse: [[#Messaging & Data Deep Dive]])*"

### Closing (30 sec)

> "What I bring is the discipline of building CI/CD in environments where reliability is non-negotiable. I treat pipelines as production systems — they need monitoring, tests, and runbooks. And I've done it both from scratch and at scale."

---

## Weak Spots — Honest Answers

| Topic | Answer |
|-------|--------|
| "Have you used Tekton?" | "Not in production, but I understand the CRD model — Tasks, Pipelines, Workspaces. It maps to Azure DevOps YAML stages. I'd need a sprint to get fluent, not a quarter." |
| "How about Airflow?" | "I built similar workflow orchestration at Volvo in Python. Airflow formalizes that with DAGs and operators. I'd focus on the operator ecosystem and scheduler tuning." |
| "Traefik / OAuth2 Proxy?" | "I've configured reverse proxies and auth layers, but not these specific tools. The pattern is the same — route traffic, terminate TLS, enforce auth." |
| "InfluxDB vs Prometheus?" | "Prometheus is pull-based, InfluxDB is push-based with better high-cardinality support. Both feed Grafana. I've used Prometheus; InfluxDB's query language would be new." |
| Something unknown | "I haven't worked with that directly — I'd want to see your setup before giving a confident answer. But here's how I'd approach learning it..." |

---

## Questions to Ask Them — Pick 2-3

- "How is the Tekton pipeline structured — shared task catalog or fully custom per team?"
- "What does the Gerrit trigger flow look like — webhook-based or stream-events?"
- "How do you measure pipeline health — DORA metrics or something else?"
- "What's the current biggest bottleneck in the release cycle?"
- "How is the CI/CD team organized — embedded in product teams or a platform team?"
- "What does a typical week look like for this role?"

---

## Behavioral Stories — Quick Reference

| If they ask... | Use this story |
|----------------|----------------|
| Conflict with teammate | [[#Conflict / Disagreement]] |
| Failure / mistake | [[#Failure / Lesson Learned]] |
| Complex problem | [[#Complex Technical Problem]] |
| Pressure / deadline | [[#Delivering Under Pressure]] |
| Above and beyond | [[#Going Above and Beyond]] |

---
---

# DETAIL SECTIONS — Sadece Sorulursa

*Asagidaki bolumler intro'da degindigin konularin detaylari. Interview sirasinda sorulursa buraya bak, sorulmazsa atlat.*

---

## Pipeline Architecture Deep Dive

### What I Did

> "At Volvo, the pipeline wasn't a simple build-test-deploy. Embedded automotive software has multiple hardware targets — QNX ARM, Linux x86, Android Automotive. I wrote a Python orchestration layer that read a manifest listing all targets, set up the correct cross-compilation toolchain for each, kicked off the build via Cynosure — Volvo's internal build framework — and then parsed the output into structured reports. Each target ran in its own Docker container with the toolchain pre-installed, so builds were reproducible across servers."

### Where We Struggled

> "The first version ran all targets sequentially — 40+ minutes for a full build. Developers were waiting nearly an hour for verification. I tried parallelizing naively — just spawn all at once — but we hit resource limits. Some targets needed a lot of memory for linking, and running them all in parallel caused OOM kills. The fix was batching by resource requirements: lighter targets in parallel first, heavier ones after. Brought total build time down to about 15 minutes."

### KocSistem — Template Approach

> "At KocSistem, I built a shared YAML template repository. Each project's pipeline was 15-20 lines referencing shared templates."

### Where We Struggled

> "Getting teams to adopt was harder than writing the templates. One team had a custom bash script they'd maintained for years. I had to sit down with them, understand their script step by step, prove the template could handle each piece, and migrate one app as a pilot. When they saw it working, they migrated the rest voluntarily. Lesson: you can't just build a better tool and expect people to switch."

---

## Gerrit Deep Dive

### What I Did

> "At Volvo, I managed Gerrit project configurations — `project.config` in the `refs/meta/config` branch. Set up access control per repo: who can push, who can review, who can submit. Configured label definitions — Verified and Code-Review — with custom score ranges and submit rules requiring both labels before merge. For release branches, I blocked direct pushes entirely.
>
> I wrote a Python daemon that connected to Gerrit's stream-events SSH interface, listening in real time. On `patchset-created`, it extracted the project name, change number, and patchset ref, kicked off the build, and after completion posted `Verified +1` or `-1` back via REST API with a link to the build log. It also handled 'recheck' comments to re-trigger builds."

### Where We Struggled

> "The stream-events SSH connection dropped silently — Gerrit restarts, network blips, no error, just silence. Builds stopped triggering and nobody noticed until a developer complained their change sat unverified for two hours. I added a heartbeat check — ping every 30 seconds, reconnect on failure. On reconnect, query Gerrit's REST API for unverified changes in the last hour and re-queue them. Added a dead-letter log and a dashboard showing trigger events per hour — flat line means something's wrong.
>
> Another issue: duplicate builds. Gerrit fires events for internal operations like auto-rebases, not just developer pushes. We were burning build capacity for nothing. Fixed by deduplicating on change ID plus patchset number and filtering service account events. Build queue dropped 30% overnight.
>
> Third: multi-repo changes. Automotive embedded often requires changes across repos simultaneously — API change in platform, client update in application. Verification ran them independently and one would fail. Solution was Gerrit topic-based submissions. But getting developers to use topics was its own challenge — I added a check that warned when a change touched cross-repo interfaces without a topic."

---

## Docker & Kubernetes Deep Dive

### What I Did

> "I restructured Dockerfiles as multi-stage builds — SDK image for building, slim runtime image for production. Images went from 800MB+ to 80-100MB. For Kubernetes, I configured three types of health probes: startup (for services with slow init), readiness (for rolling updates), and liveness (for hung processes). Set resource requests based on steady-state metrics and limits based on peak observed usage."

### Where We Struggled

> "Health probes were surprisingly tricky. One service loaded a large cache on startup — 45 seconds. Kubernetes killed it during startup because the liveness probe was checking before the service was ready. Infinite restart loop. We didn't have startup probes configured. Once I added a startup probe with a generous initial delay and made liveness only start after startup succeeded, it worked. Lesson: always understand a service's init behavior before setting probe values.
>
> Resource limits bit us too. We set memory limits tight to pack more pods per node. Under normal load, fine. During peak, one service got OOMKilled during GC spikes. Pod restarts, loses cache, rebuilds from DB, slow during rebuild, causes upstream timeouts. Cascading failure. Had to study actual memory profiles in Grafana and set limits with GC headroom, not just steady-state.
>
> Registry storage tripled in three months before we noticed — every build pushed an image, nobody cleaned up. Set up retention policies, but had to coordinate with teams about long-lived feature branches first. After the initial cleanup, automated it."

---

## Terraform Deep Dive

### What I Did

> "Separated `plan` from `apply` in the pipeline. Plan output posted as a PR comment so reviewers see exactly what changes. Apply only from the saved plan file. Remote state on Azure Blob Storage with locking."

### Where We Struggled

> "The state corruption incident: two developers ran `terraform apply` simultaneously. State ended up broken — some resources tracked, others not, some with wrong IDs. Couldn't just run apply again — it would try to recreate existing resources. Had to manually reconcile: compare Terraform state with actual Azure resources, `terraform import` for missing entries, `terraform state rm` for phantom ones. Took most of a day. After that, state locking was non-negotiable.
>
> Portal changes were a constant battle. People made quick changes during incidents — understandable but created drift. Nightly drift detection helped, but the real fix was making Terraform changes fast enough. If scaling up is a one-variable PR that applies in 10 minutes, people stop going to the portal.
>
> Module rigidity: first version assumed every app needed SQL. Some only used Redis. Refactoring to feature flags (`enable_sql`, `enable_redis`) broke state references — had to run `terraform state mv` for every environment. Painful. Now I design modules for flexibility from the start."

---

## Observability Deep Dive

### What I Did

> "Built DORA metric dashboards in Grafana: deployment frequency, lead time, change failure rate, MTTR. Reported to leadership monthly. Also set up pipeline health dashboards — build duration trends, failure rates, slowest stages."

### Where We Struggled

> "Getting accurate DORA data was harder than expected. Deployment frequency was easy. Lead time required correlating Git commit timestamps with deployment timestamps — our pipeline didn't track that initially. Had to add a step recording the oldest commit SHA in each deployment. Change failure rate was debated — does a hotfix 30 minutes later count? We settled on: any deployment requiring a follow-up within 24 hours counts as a failure. Not perfect, but consistent. First time I showed leadership, they were surprised our lead time was 4 days — mostly manual approval bottlenecks. That data point alone justified automating non-production approvals.
>
> Alerting: first attempt sent a notification for every build failure. Team ignored them within a week. Switched to rate-based alerting — 20% failure rate in a rolling hour. Noise dropped, team started paying attention again."

---

## Security Deep Dive

### What I Did

> "At KocSistem, went from quarterly pen-test findings to three consecutive quarters of zero findings."

### Where We Struggled

> "Dependency scanning wasn't popular. Developers complained their builds failed for 'something they didn't even change.' Had to explain the vulnerability was already there, the pipeline just made it visible.
>
> Static analysis needed two weeks of rule calibration. Too many false positives and developers bypass the system. Too few and you miss real issues. Added custom rules for patterns specific to our codebase — like our specific ORM usage patterns that could lead to SQL injection.
>
> Secrets migration was the scariest. Secrets scattered everywhere — config files, pipeline variables, some hardcoded. Couldn't rip them all out at once. Did it service by service: identify secrets, create Key Vault entries, update application, test in staging, deploy, then clean Git history with `git filter-branch` — which required the entire team to re-clone. First week after adding the pre-push secret scanning hook, it blocked 4 pushes with real secrets. That alone justified the effort."

---

## Messaging & Data Deep Dive

### What I Did

> "At Toyota, set up RabbitMQ sidecar containers in the pipeline for integration testing. After the split-brain incident, added a chaos step that kills RabbitMQ mid-test to verify reconnection logic."

### Where We Struggled

> "The sidecar RabbitMQ was flaky. Health check said ready, but the management plugin wasn't fully initialized. Tests failed with 'connection refused' — we thought it was a network issue. Spent two days tracking it down. The health check was checking if the port was open, not if RabbitMQ was ready for AMQP connections. Changed to an actual AMQP connection check. Fixed 10% of our pipeline failures.
>
> Database migration testing: staging snapshots took 20 minutes. Developers hated it. Tried smaller datasets, but data-dependent migrations (like adding NOT NULL columns to large tables) would pass in the pipeline and fail in staging. Compromise: a 'representative subset' snapshot refreshed weekly — small enough to copy quickly, large enough to catch data-dependent issues."

---

## Behavioral Stories — Full STAR Format

### Conflict / Disagreement

**S:** At KocSistem, a senior developer wanted a monthly "deployment freeze." He'd been burned by a Friday outage.

**T:** Resolve without alienating him while maintaining deployment momentum.

**A:** Asked him to stay 15 minutes. Acknowledged his experience, proposed an experiment: track every deployment failure and check if a freeze would have prevented it. After 6 weeks, data showed incidents were from config drift and missing tests — things a freeze wouldn't catch. Built a pre-deployment checklist and automated rollback together.

**R:** He became an advocate for daily deployments. Incident rate dropped because we shipped smaller changes.

---

### Failure / Lesson Learned

**S:** At Toyota, responsible for RabbitMQ messaging for autonomous forklifts. Went to production with a 3-node cluster.

**T:** Ensure reliable message delivery for real-time forklift commands.

**A:** Didn't fully account for network partitions. A blip caused split-brain. Messages got lost. Forklifts waited for commands that never came.

**R:** No equipment damaged, but lost productivity. Deep-dived into partition handling, built monitoring, documented recovery, started chaos tests. Never happened again.

---

### Complex Technical Problem

**S:** At KocSistem, no CI/CD, no production visibility. Manual deployments, hours of guessing.

**T:** Transform deployment without disrupting ongoing work.

**A:** Built pipelines from scratch on Azure DevOps. Terraform for IaC. Prometheus and Grafana for visibility. Wrote runbooks.

**R:** Weekly to daily releases (7x). Cloud migration with zero downtime. Mean time to detect: hours to minutes.

---

### Delivering Under Pressure

**S:** At Volvo, a bug causing intermittent failures in embedded software. They were considering stopping the production line.

**T:** Fix or workaround. Stopping production was the nuclear option.

**A:** Drove to facility with one engineer. Isolated it — race condition in initialization. Wrote patch with deterministic startup, verified on spare unit, rolled out carefully.

**R:** Production line never stopped. Patch held until next maintenance window. Pushed for better test/production parity.

---

### Going Above and Beyond

**S:** At KocSistem, hired as backend developer. No production visibility.

**T:** Not my job, but tired of debugging blind.

**A:** Learned monitoring tools on my own time. Built POC, demoed to lead, deployed properly, wrote alerts and dashboards.

**R:** Detection time: hours to minutes. Became the template for every new service. Led to my promotion.

---

## Setup Scenarios — "How Would You Set Up...?"

*Bunlar da sorulursa kullan. Daha teknik, adim adim.*

### Scenario 1: Pipeline from Scratch

> Build → Test (sidecars for deps) → Security scan → Push image (SHA + semver tag) → Deploy (staging auto, prod manual approval + smoke tests + auto-rollback). Pipeline definition version-controlled and reviewed like application code.

### Scenario 2: Gerrit + CI Triggers

> Install on Linux VM → configure `gerrit.config` (auth, SMTP) → create projects with submit rules → service account with minimal permissions → stream-events listener → fetch patchset ref → build → post Verified label via REST API. Handle: webhook failures (retry + dead-letter), duplicates (dedup on change+patchset), slow clones (partial clone).

### Scenario 3: K8s Build Runners

> Dedicated namespace with resource quotas → autoscaling node pool → each build = one pod → init containers for workspace setup → PVC for dependency cache → Kaniko instead of Docker-in-Docker (no privileged mode) → RBAC with minimal permissions → TTL cleanup for completed pods → log collection before deletion.

### Scenario 4: Vault for Secrets

> Deploy via Helm (HA mode) → AppRole auth per pipeline → short-lived tokens (15 min TTL) → secrets as env vars at runtime only → dynamic secrets for DB credentials (Vault creates temp user, auto-revokes) → audit logging for every access. Same pattern as Azure Key Vault, which I've implemented.

### Scenario 5: Pipeline Observability

> Metrics via Prometheus pushgateway → Logs to Loki (structured, with pipeline ID/stage/branch) → Traces with OTel (each pipeline stage = span) → Grafana dashboards: pipeline health, DORA metrics, resource usage → Alerts: rate-based (not per-failure), production deploy failure pages on-call.

### Scenario 6: Flaky Pipeline Debugging

> Classify (test vs infra vs timing) → data (last 50 builds, resource metrics, exact error) → common fixes: Dockerfile layer order, wait-for-it scripts, registry mirrors, test quarantine, resource requests → prevention: retry with limits, trend alerting, flaky test rate as a metric.

---

## Delivery Tips

1. **Lead with Volvo** — strongest overlap with automotive CI/CD
2. **Use numbers** — 30%, 55%, 60%, 7x
3. **Say "I" not "we"**
4. **Be honest about gaps** — model understanding + learning speed
5. **Don't volunteer detail** — let them ask, then go to the relevant deep dive section
6. **Hook, don't lecture** — drop a one-liner that shows depth, wait for the follow-up

---

*Created: 2026-03-26*
*Based on experience at: Combination AB, Toyota Material Handling, Volvo Cars, KocSistem, Antasya*
