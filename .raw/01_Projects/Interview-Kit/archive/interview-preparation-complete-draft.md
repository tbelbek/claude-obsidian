# Interview Preparation — Tughan Belbek (Generic)

*Senior Software Engineer · DevOps Lead · Technology Manager · Registered Scrum Master*

**Format:** Short intro (5 min) + Q&A. Four expertise pillars: Software Development, DevOps, Leadership, Agile.
**Location:** Gothenburg

---

## Quick Reference — Last Minute Scan

| Must Mention | Key Phrase |
|--------------|------------|
| **Experience** | 10+ years across software dev, DevOps, and team leadership |
| **Current** | Combination AB — .NET 9 microservices, K8s, GraphQL/gRPC, CI/CD |
| **Dev** | .NET ecosystem (10 years), distributed systems, RabbitMQ, Redis, PostgreSQL |
| **DevOps** | CI/CD from scratch, Terraform, Docker/K8s, Gerrit, DORA metrics, zero pen-test findings |
| **Leadership** | 25 engineers, DevOps transformation, Scrum Master |
| **Agile** | Registered Scrum Master, maturity 3.1→3.7, cross-functional teams, sprint ceremonies |
| **Industries** | Automotive (Volvo), industrial automation (Toyota), enterprise (KocSistem) |

### Bottom Line (Memorize)
> "I've spent 10 years across four areas that usually live in different people: I write production backend code, I build the pipelines that ship it, I've led the teams that do both, and I've shaped the Agile processes that keep them aligned. That combination means I can see problems end-to-end — from a flaky test to a broken deploy to a team that's stuck in ceremony without outcomes."

---

## The Script — Compact Version (5 min)

> "Hi, I'm Tughan Belbek. I've been working as a software engineer for over 10 years, and my career has covered four areas that I think complement each other well: **software development**, **DevOps and infrastructure**, **technical leadership**, and **Agile process**. I live here in Gothenburg with permanent residence.
>
> On the **software development** side — I've been shipping production .NET services for 10 years, currently on .NET 9 at Combination AB. Microservices with GraphQL and gRPC, containerized and running on Kubernetes. Before that, at Toyota I worked on T-ONE — their autonomous forklift orchestration platform — where I dealt with real-time messaging over RabbitMQ, and the kind of failure modes you only learn about in production. *(Detay: [[#Software Development Deep Dive]])*
>
> On the **DevOps** side — at Volvo Cars I was a Software Factory Engineer, building release pipelines for embedded automotive software with Gerrit, Python automation, and strict regulatory gating. At KocSistem, I built CI/CD from zero for 10+ applications — Azure DevOps pipelines, Terraform for infrastructure, security scanning baked into every build. I tracked DORA metrics and used them to justify infrastructure investments to leadership. Currently I maintain pipelines in Azure DevOps and GitHub Actions daily. *(Detay: [[#DevOps Deep Dive]])*
>
> On the **leadership** side — at KocSistem I grew from Senior Developer to Technology Manager, leading 25 engineers. I owned the technical roadmap and was hands-on enough to pair-program with junior devs while also presenting to the board. *(Detay: [[#Leadership Deep Dive]])*
>
> On the **Agile** side — I'm a registered Scrum Master and I've led Agile transformations in teams that were either doing waterfall or doing Agile in name only. At KocSistem I took Agile maturity from 3.1 to 3.7 out of 4 — not by adding more ceremonies, but by making the existing ones actually useful. At Toyota I worked in a cross-functional Agile team on safety-critical software where sprint discipline wasn't optional. I care more about outcomes than certifications, but the certification helped me have credibility when pushing for change. *(Detay: [[#Agile Deep Dive]])*
>
> What ties these four together: I've been in environments where systems had to work — autonomous forklifts, automotive embedded, enterprise platforms with strict SLAs. That taught me to think about the full chain: the code, the pipeline that ships it, the team that maintains it, and the process that keeps them aligned."

### Why This Company (30 sec)
> "I'm selective about where I apply. You're building systems that need to balance speed with reliability — that's the exact problem I've been working on for 10 years across all four of those areas."

### Closing (30 sec)
> "I close gaps — between code and delivery, between teams, between 'working' and 'reliable.' I'd be interested in bringing that here."

---

## Behavioral Stories — Quick Reference

| If they ask... | Use this story |
|----------------|----------------|
| Conflict with teammate | [[#Conflict — Deployment Freeze Debate]] |
| Failure / mistake | [[#Failure — RabbitMQ Split-Brain]] |
| Leadership without authority | [[#Leadership — CI/CD Pilot Adoption]] |
| Complex problem | [[#Problem-Solving — DevOps From Zero]] |
| Pressure / deadline | [[#Pressure — Volvo Production Line]] |
| Above and beyond | [[#Initiative — Observability From Scratch]] |
| Difficult person | [[#Collaboration — Third-Party Integration]] |
| Adaptability / change | [[#Adaptability — REST to GraphQL]] |

---

## Questions to Ask Them — Pick 2-3

- "What does the current architecture look like?"
- "What's the biggest technical challenge you're facing right now?"
- "How do you handle observability and incident response?"
- "How is the engineering team organized?"
- "What's the on-call situation like?"
- "How do you balance moving fast with reliability?"

---

## Delivery Tips

1. **Say "I" not "we"** — "the team did X, I did Y"
2. **Be specific** — "we cut release time from weekly to daily" not "we improved things"
3. **Don't volunteer detail** — let them ask, then go to the relevant deep dive
4. **Don't reuse stories** — if you used RabbitMQ for "failure," use Volvo for "pressure"
5. **Match the pillar to the question** — if they ask about architecture, lead with dev. If process, lead with DevOps. If people, lead with leadership.

---
---

# PILLAR 1: SOFTWARE DEVELOPMENT — Detay

## Software Development Deep Dive

### Combination AB — .NET 9 Microservices (Current)

> "I'm building microservices in .NET 9 — REST, GraphQL, and gRPC depending on what fits the use case. GraphQL for frontend-driven queries where the client needs flexibility in what data it fetches. gRPC for service-to-service communication where performance matters. REST for external APIs where simplicity and discoverability are more important than optimization.
>
> I profile backend services when something's slow. Not just 'add a cache' — I look at the actual query plans, the serialization overhead, the network round-trips. Recently we had an endpoint that took 3 seconds. Everyone assumed it was the database. Turned out it was N+1 queries hidden behind a GraphQL resolver that looked innocent. Fixed the data loader pattern, response time dropped to 200ms."

### Where We Struggled — GraphQL Migration

> "We decided to move from REST to GraphQL. Half the backend team was skeptical — we'd invested years in REST conventions. I volunteered as migration lead even though I wasn't a GraphQL expert.
>
> I spent a week building a side project, hit every pain point, documented them. The biggest risk was doing a big-bang migration and breaking existing clients. I proposed a gradual approach: GraphQL alongside REST for new features first, prove the value, then migrate existing endpoints one by one.
>
> The turning point was pairing with the most skeptical developer. We built the first production resolver together. When he saw the frontend team's reaction — one request instead of five, exactly the data they needed — he flipped. We migrated most of the API surface in 6 months. Zero breaking changes for existing clients."

---

### Toyota — Distributed Systems & Messaging

> "At Toyota Material Handling, I worked on T-ONE — the autonomous forklift orchestration platform. Backend in .NET 8, MongoDB for persistence, RabbitMQ for real-time coordination between forklifts and the central system.
>
> This wasn't a typical web app. Messages had to arrive reliably and in order. A forklift waiting for a command that never comes is expensive — and potentially dangerous. I built Python test frameworks that simulated fleet scenarios and caught regressions before they reached production."

### Where We Struggled — Split-Brain

> "I went to production with a RabbitMQ 3-node cluster thinking I understood clustering from the docs. A temporary network blip caused split-brain — the cluster partitioned, each side thought the other was dead, and messages got lost. Forklifts waited for commands that never came. I spent hours manually reconciling queues while operations was breathing down my neck.
>
> No equipment damaged, but lost productivity. That taught me the difference between reading documentation and understanding failure modes. I deep-dived into RabbitMQ partition handling strategies, built proper cluster health monitoring, documented recovery procedures, and started running chaos engineering tests — intentionally killing nodes to verify reconnection logic. Never had that issue again."

---

### KocSistem — Enterprise Backend & Architecture

> "At KocSistem as Senior Developer, I built a GPS-based warehouse management system — card access, production band audit, truck tracing. .NET Core, Redis for caching, Elasticsearch for search, RabbitMQ for async processing. Consulted for major clients: Arcelik, Beko, Bosch Siemens, Aygaz.
>
> The project won the 2019 IDC Award and a Customer Satisfaction Award in Turkey. I also contributed reusable modules to KocSistem's company-wide project framework."

### Where We Struggled — Performance at Scale

> "The GPS tracking system worked fine in testing with 50 trucks. In production with 500+ trucks, the real-time tracking dashboard froze. Every truck was sending GPS coordinates every 2 seconds, and we were writing each one directly to SQL Server.
>
> The fix was a pipeline: GPS data went into Redis as a stream first — the dashboard read from Redis for real-time display, and a background worker batch-inserted into SQL every 30 seconds for historical queries. Dashboard went from unusable to sub-second response. Taught me that the architecture that works at 50 users is often completely wrong at 500."

---

### Antasya — Embedded & IoT

> "Built public transport software in C# and C++ for Istanbul's public transport agency (IETT). Delivered an AVL (Automatic Vehicle Location) solution deployed across the city's fleet. Also worked on Android 4.4 embedded devices for in-vehicle digital signage. Researched the Green Stop Project — E-Ink displays with solar-powered embedded PCs in transit stops."

---
---

# PILLAR 2: DEVOPS — Detay

## DevOps Deep Dive

### Volvo Cars — Embedded Release Pipelines & Gerrit

> "As Software Factory Engineer, I built and maintained release pipelines for embedded automotive software. The pipeline wasn't build-test-deploy — it was build, static analysis, unit tests, hardware-in-the-loop integration tests, regulatory gate check, staged rollout. Each stage had strict pass/fail criteria and everything had to be auditable.
>
> I wrote the automation layer in Python on Linux. The build system was Cynosure — Volvo's internal framework — with multiple hardware targets: QNX ARM, Linux x86, Android Automotive. I wrote an orchestration layer that set up the correct cross-compilation toolchain per target, kicked off builds, parsed results into structured reports, and notified the team with exactly which target and component failed.
>
> Gerrit was the core of our code review and CI trigger system. I maintained the instance — project configurations, access control rules, label definitions (Verified, Code-Review), submit rules. I wrote a Python daemon that listened to Gerrit's stream-events, triggered verification builds on patchset-created, and posted Verified +1/-1 back via REST API with build log links."

### Where We Struggled — Gerrit Triggers

> "The stream-events SSH connection dropped silently — Gerrit restarts, network blips, no error. Builds stopped triggering and nobody noticed until a developer complained their change sat unverified for two hours.
>
> I added a heartbeat check every 30 seconds, automatic reconnect on failure, and a catch-up query on reconnect — poll Gerrit REST API for unverified changes in the last hour and re-queue them. Added a dead-letter log and a dashboard showing trigger events per hour — flat line means something's broken.
>
> Another issue: duplicate builds from internal Gerrit operations like auto-rebases. Fixed by deduplicating on change ID plus patchset number. Build queue dropped 30% overnight.
>
> Third: multi-repo changes in automotive embedded. A platform API change and its client update needed to land together. Changes verified independently would fail. I configured Gerrit topic-based submissions and added a check that warned when cross-repo interfaces changed without a topic."

### Where We Struggled — Build Parallelization

> "First version of the orchestration ran all targets sequentially — 40+ minutes. Developers waited nearly an hour for verification. I tried naive parallelism — spawn all at once — but heavy targets caused OOM kills during linking. Fixed by batching targets by resource requirements: light ones in parallel first, heavy ones after. Build time dropped to ~15 minutes."

---

### KocSistem — DevOps Transformation From Zero

> "When I became Dev Lead, there were no CI/CD pipelines, no code review standards, no branching strategy. I built everything on Azure DevOps: shared YAML template repository for common stages, parameterized per project. Each project's pipeline was 15-20 lines referencing shared templates.
>
> Integrated security scanning — dependency checks, static analysis with quality gates, secrets migrated from config files to Azure Key Vault. Added a pre-push Git hook that blocked commits containing secret patterns — first week it blocked 4 pushes with real secrets.
>
> Set up Terraform for infrastructure. Separated plan from apply in the pipeline — plan output posted as PR comment, apply only from saved plan after manual approval. Remote state on Azure Blob Storage with locking.
>
> Tracked DORA metrics in Grafana: deployment frequency, lead time, change failure rate, MTTR. Reported monthly to leadership."

### Where We Struggled — State Corruption

> "Two developers ran `terraform apply` simultaneously before I had locking enabled. State ended up broken — some resources tracked, others not, some with wrong IDs. Couldn't just re-apply — it would recreate existing resources. Had to manually reconcile: compare Terraform state with actual Azure resources, `terraform import` for missing entries, `terraform state rm` for phantoms. Took most of a day. After that, state locking was non-negotiable."

### Where We Struggled — Portal Drift

> "People made quick changes through the Azure Portal during incidents — understandable, but created drift. I set up nightly `terraform plan` that alerted on any drift. But the real fix was making Terraform changes fast enough. Once scaling up was a one-variable PR that applied in 10 minutes, people stopped going to the portal."

### Where We Struggled — Template Adoption

> "Building shared pipeline templates was the easy part. Getting teams to use them was hard. One team had a custom bash script they'd maintained for years. I sat down with them, understood their script step by step, proved the template handled each piece, and migrated one app as a pilot. When they saw it working and realized they didn't have to maintain that script anymore, they migrated the rest. You can't just build a better tool and expect people to switch."

### Where We Struggled — Security Pushback

> "Dependency scanning wasn't popular. Developers complained their builds failed for 'something they didn't even change.' I had to explain the vulnerability was already there — the pipeline just made it visible. Static analysis needed two weeks of rule calibration to avoid false positive fatigue. And the secrets migration was the scariest — secrets scattered in config files, pipeline variables, some hardcoded. Did it service by service, then cleaned Git history with `git filter-branch`, which meant the entire team had to re-clone.
>
> After three consecutive quarters of zero pen-test findings, the security team stopped treating us as a risk and started asking other teams to adopt our setup."

### Where We Struggled — Observability

> "Getting accurate DORA data was harder than expected. Lead time required correlating Git commit timestamps with deployment timestamps — our pipeline didn't track that. Had to add a step recording the oldest commit SHA per deployment. Change failure rate definition was debated for weeks — we settled on 'any deployment requiring a follow-up within 24 hours.'
>
> Alerting: first version sent a notification per build failure. Team ignored them within a week. Switched to rate-based alerting — 20% failure rate in a rolling hour window. Noise dropped, team started paying attention again."

---

### Combination AB — Current CI/CD

> "Maintaining CI/CD pipelines in Azure DevOps and GitHub Actions for .NET 9 microservices. Multi-stage Docker builds — SDK image for building, slim runtime for production. Images from 800MB+ down to 80-100MB. ACR with retention policies. Kubernetes deployments with proper health probes and rolling updates."

### Where We Struggled — Docker Caching

> "Builds were taking 10 minutes instead of 2. The issue was Docker layer caching — `COPY . .` early in the Dockerfile invalidated the cache on every change, even when dependencies hadn't changed. Reordered: copy project files first, restore dependencies, then copy source. Expensive restore step now cached unless you actually change a dependency."

### Where We Struggled — K8s Health Probes

> "One service loaded a large cache on startup — 45 seconds. Kubernetes killed it because the liveness probe fired before the service was ready. Infinite restart loop. We didn't have startup probes configured. Added a startup probe with generous initial delay, liveness only starts after startup succeeds. Lesson: always understand a service's init behavior before setting probe values."

---
---

# PILLAR 3: LEADERSHIP — Detay

## Leadership Deep Dive

### KocSistem — Technology Manager (25 engineers)

> "Managed 25 engineers. Owned the technical roadmap: DevOps, security posture, architecture direction, Agile process improvements. Also acted as Product Owner for the HR employee experience platform. Mentored engineers at every level — junior to senior. Ran and spoke at internal tech events."

### Where We Struggled — Balancing Code and Management

> "Half my time was coding, half was planning, 1:1s, roadmapping, and unblocking people. Some days I'd start a code review and not finish it until the next day because of meetings.
>
> I learned to protect my coding time — blocked mornings for technical work, afternoons for people work. And I learned that the most impactful thing a tech manager can do isn't write code — it's remove obstacles that prevent 25 other people from writing code. A roadblock I clear in 30 minutes might unblock a week of work for someone else."

### Results
> "Hit all first-year roadmap targets. DevSecOps 4 Key Metrics at 75%. Agile maturity from 3.1 to 3.7. Doubled release frequency. Zero pen-test findings."

---

### KocSistem — Dev Lead (CI/CD Transformation)

> "Led the dev team day-to-day: planning, 1:1s, technical direction, architectural decisions. Pushed through a DevOps transformation the team was overdue for."

### Where We Struggled — Cultural Resistance

> "The team was doing 'push and pray' releases. I measured the pain first: deployment times, failure rates, time in ceremonies vs coding. Presented data as 'am I seeing this right?' — not 'here's what's wrong.'
>
> Proposed a pilot: one team, 2 sprints, daily deployments with automated checks. Volunteered our team, pair-programmed with skeptics, fixed flaky tests myself, was online at 6 AM for first deploys. Pilot went weekly to daily in 3 weeks. Other teams asked how. Six months later, org-wide shift.
>
> The hardest part was the cultural shift. Some developers had been deploying the same way for years. They didn't trust automation. I had to let them see it work — not tell them it would."

### Results
> "Git workflow overhauled. SLA breach rate down 60%. CI/CD live for all apps. Bug rate in new releases dropped 55%. User satisfaction up 50%."

---

### KocSistem — Initiative & Growth

> "Started as a Senior Developer. We were flying blind in production. I wasn't hired to do infrastructure — I was hired to write backend code. But I was tired of spending 3 hours tracking down bugs that proper metrics would surface in 3 minutes."

### Where We Struggled — Getting Buy-In

> "I spent weekends learning monitoring tools. Built a POC showing our services' latency, memory, error rates. Demoed to my lead — his reaction was 'why don't we have this already?'
>
> The struggle was getting the team to actually look at dashboards. I started every standup with 'here's what the dashboard showed overnight.' After a few weeks where we caught issues before users reported them, the team started checking on their own. It became the template for every new service — monitoring first, not afterthought.
>
> That initiative led to my promotion to Dev Lead."

---

### Conflict Management — Deployment Freeze Debate

> "A senior developer wanted a monthly deployment freeze — he'd been burned by a Friday outage. Team of 25 was divided. I asked him to stay 15 minutes after a meeting. Acknowledged his experience, proposed an experiment: track every deployment failure for 6 weeks and check if a freeze would have prevented it.
>
> Data showed incidents came from config drift and missing tests — things a freeze wouldn't catch. We built a pre-deployment checklist and automated rollback together. He became an advocate for daily deployments."

---

### Working With Difficult People — Toyota Integration

> "Integrating with a third-party logistics system at Toyota. Their tech lead was defensive — burned by previous integrations. Stopped emailing. Went in person. Brought questions not demands: 'Help me understand what went wrong before.'
>
> He opened up — previous partners broke promises, pushed changes without notice, blamed his team. I proposed: start read-only, give notice on changes, shared daily channel. Publicly credited his team when things worked. He became a genuine partner — proactively suggested optimizations, referred us to another division."

---
---

# PILLAR 4: AGILE — Detay

## Agile Deep Dive

### KocSistem — Agile Transformation (Technology Manager)

> "When I took over as Technology Manager, the team was doing Agile in name only. They had sprints and standups, but the sprints had no clear goals, the standups were status reports that took 30 minutes, and retrospectives were either skipped or turned into complaint sessions with no follow-up. Agile maturity was measured at 3.1 out of 4 — which sounds decent, but when I looked at the breakdown, velocity was unpredictable, sprint commitments were missed regularly, and stakeholders had no visibility into what the team was actually delivering."

### Where We Struggled — Making Ceremonies Useful

> "The first thing I changed was standups. They were 25 people in a room giving updates nobody listened to. I broke them into team-level standups — 5-6 people, focused on blockers, not status. If your update is 'I'm still working on the same thing,' you don't need to say it. Standups went from 30 minutes to 8.
>
> Retrospectives were harder. The team was used to complaining without follow-through. I introduced a rule: every retro produces exactly 2 action items, each with an owner and a deadline. Next retro starts by reviewing last retro's action items. If we didn't complete them, we had to talk about why before raising new issues. At first people resisted — 'this is too rigid.' But after three sprints where actual problems got fixed because someone was accountable, the team started taking retros seriously.
>
> Sprint planning was the biggest fight. Teams were committing to work without understanding scope, then either cutting corners or carrying over half the sprint. I pushed for story point estimation with planning poker — not because I believe in the precision of story points, but because the conversation during estimation surfaces risks and unknowns that people wouldn't mention otherwise. 'Why do you think this is an 8 when I said 3?' often reveals that one person knows about a dependency the other doesn't."

### Where We Struggled — Agile With Stakeholders

> "Engineering-side Agile was one thing. Getting stakeholders to play along was another. Product owners would change priorities mid-sprint, add 'urgent' items that weren't urgent, and then ask why the sprint commitment wasn't met. I introduced sprint goals — a single sentence describing what this sprint delivers. If a new request didn't serve the sprint goal, it went to the backlog. If it was genuinely urgent, we'd have a conversation about what we drop in exchange.
>
> I also started sharing sprint demos with stakeholders — not just screenshots or reports, but live working software. When they could see what was shipped every two weeks, they stopped micromanaging because they had visibility. The trust went up, the mid-sprint interruptions went down."

### Results
> "Agile maturity from 3.1 to 3.7 out of 4. Sprint velocity became predictable within 10% variance. Stakeholder satisfaction improved because they had visibility. Team morale improved because ceremonies felt useful instead of wasteful."

---

### Toyota — Cross-Functional Agile on Safety-Critical Software

> "At Toyota Material Handling, the T-ONE team was cross-functional — developers, testers, domain experts — working in sprints on software that controlled autonomous forklifts. Sprint discipline wasn't optional here because a missed test or a skipped review could mean a forklift collision."

### Where We Struggled — Definition of Done in Safety-Critical

> "The standard definition of done — code reviewed, tests passing, deployed to staging — wasn't enough. We had to include: integration tests against simulated fleet scenarios passed, test report generated and archived, documentation updated, and a safety review checklist signed off.
>
> This made sprints feel slow at first. Developers would 'finish' a story in 3 days but the safety checklist took another 2. The temptation was to push the checklist to the next sprint — 'it's done, we just need sign-off.' I pushed back hard on this. A story isn't done until it meets the full definition of done. If the definition of done takes too long, we need to either automate parts of it or reduce sprint scope — not pretend it doesn't exist.
>
> Over time, we automated the test report generation and parts of the safety checklist, which brought the overhead from 2 days to about half a day per story."

---

### Volvo — Agile in Regulated Environments

> "At Volvo, the challenge was running Agile processes within a heavily regulated environment. Automotive embedded software has compliance requirements — documentation, traceability, audit trails — that don't naturally fit into a 2-week sprint cadence."

### Where We Struggled — Compliance vs Agility

> "The regulatory team wanted full documentation before any release. The development team wanted to ship frequently. These goals seemed contradictory. The compromise was: we automated the documentation generation. Every release pipeline produced compliance artifacts automatically — test reports, traceability matrices, change logs — as part of the build, not as a separate manual process.
>
> This meant the team could ship as frequently as the pipeline allowed while still meeting every compliance requirement. The regulatory team was happy because the documentation was consistent and machine-generated. The development team was happy because they didn't have to spend days writing Word documents."

---

### Scrum Master Certification — Practical Value

> "I'm a registered Scrum Master. I'll be honest — I got the certification because I needed credibility when pushing for change at KocSistem. Engineers don't like being told to change their process by someone without credentials. The certification gave me the authority to say 'this is how it should work' and have people listen.
>
> But the real value wasn't the certification itself — it was the framework for having difficult conversations. When a product owner wants to change priorities mid-sprint, you need a principled response, not just 'I don't think we should.' 'The Scrum framework says we protect sprint scope' is stronger than 'I'd prefer not to.' It's a tool, not an identity."

---

### Agile Anti-Patterns I've Fixed

> "Over the years I've seen the same anti-patterns across companies:
>
> **Zombie standups** — 25 people, 30 minutes, nobody listening. Fix: break into small teams, focus on blockers only, timebox to 10 minutes.
>
> **Retros without follow-through** — complain, feel better, change nothing. Fix: 2 action items per retro, each with an owner, review at next retro before raising new items.
>
> **Sprint padding** — team takes less work than they can handle to always 'succeed.' Fix: track velocity over time, challenge teams to stretch, normalize that missing a commitment occasionally is healthy.
>
> **Agile theater** — all the ceremonies, none of the outcomes. Fix: ask 'what decision did this meeting produce?' If the answer is nothing, either fix the meeting or cancel it.
>
> **Story point inflation** — everything is a 13. Fix: recalibrate with reference stories, make estimation a conversation not a formality."

---
---

# BEHAVIORAL STORIES — Full STAR Format

## Conflict — Deployment Freeze Debate

**S:** At KocSistem, senior developer wanted monthly deployment freeze. Burned by Friday outage. Team divided.

**T:** Resolve without alienating him while keeping momentum toward daily deployments.

**A:** Asked him to stay 15 minutes. Acknowledged his experience. Proposed experiment: track every failure, check if freeze would have prevented it. After 6 weeks, data showed config drift and missing tests — not deployment timing. Built pre-deployment checklist and automated rollback together.

**R:** He became advocate for daily deployments. Incident rate dropped — smaller changes = fewer surprises.

---

## Failure — RabbitMQ Split-Brain

**S:** At Toyota, responsible for RabbitMQ messaging for T-ONE. 3-node cluster in production.

**T:** Ensure reliable message delivery for real-time forklift commands.

**A:** Didn't account for network partitions. Blip caused split-brain. Messages lost. Forklifts waited.

**R:** No equipment damaged, lost productivity. Deep-dived into partition handling, built monitoring, documented recovery, started chaos tests. Never happened again.

---

## Leadership — CI/CD Pilot Adoption

**S:** Joined KocSistem as Tech Lead. Team stuck — weekly releases, hours of ceremonies.

**T:** Change how we worked without mandating it.

**A:** Measured pain with data. Presented as "am I seeing this right?" Proposed pilot: one team, 2 sprints, daily deploys. Volunteered our team, fixed flaky tests myself, online at 6 AM for first deploys.

**R:** Weekly to daily in 3 weeks. Other teams asked how. Six months later, org-wide. SLA breaches down 60%.

---

## Problem-Solving — DevOps From Zero

**S:** At KocSistem, no CI/CD, no production visibility. Manual deployments, hours of guessing.

**T:** Transform deployment without disrupting ongoing work.

**A:** Built pipelines from scratch on Azure DevOps. Terraform for IaC. Prometheus and Grafana for visibility. Runbooks.

**R:** Weekly to daily (7x). Cloud migration with zero downtime. Detection time: hours to minutes.

---

## Pressure — Volvo Production Line

**S:** Bug causing intermittent embedded failures. Production line stop being considered.

**T:** Fix or workaround. Stopping production was the nuclear option.

**A:** Drove to facility with one engineer. Isolated race condition in initialization. Tested patch on spare unit. Rolled out carefully.

**R:** Production line never stopped. Patch held. Pushed for better test/production parity.

---

## Initiative — Observability From Scratch

**S:** At KocSistem, hired as backend developer. No production visibility.

**T:** Not my job, but tired of debugging blind.

**A:** Learned monitoring on my own time. Built POC, demoed to lead, deployed properly. Wrote alerts and dashboards.

**R:** Detection time: hours to minutes. Template for every new service. Led to promotion.

---

## Collaboration — Third-Party Integration

**S:** Toyota, integrating with third-party logistics. Their tech lead was defensive — burned by previous integrations.

**T:** Get integration working without relationship turning toxic.

**A:** Went in person. Questions not demands. Proposed: start read-only, give notice on changes, shared channel. Credited his team publicly.

**R:** Shipped on time. He became a partner — proactively suggested optimizations.

---

## Adaptability — REST to GraphQL

**S:** At Combination, decided to move from REST to GraphQL. Half the backend team skeptical.

**T:** Learn GraphQL deeply enough to guide migration while keeping team motivated.

**A:** Volunteered as lead. Built side project, documented pain points. Gradual approach — GraphQL alongside REST. Paired with most skeptical dev.

**R:** Migrated most of API surface in 6 months. Zero breaking changes. Frontend velocity up. Skeptics became proponents.

---

*Created: 2026-03-24 | Updated: 2026-03-26*
*Based on experience at: Combination AB, Toyota Material Handling, Volvo Cars, KocSistem, Antasya*
