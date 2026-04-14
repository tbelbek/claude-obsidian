---
tags:
  - interview-kit
  - interview-kit/script
up: [[00-dashboard]]
---

# Introduction Script — 8 Minutes

> [!tip] Bunu oku, detay verme. Soru gelirse ilgili pillar'a atla.

---

## Opening (1 min)

> "Hi, I'm Tughan Belbek. I live in Gothenburg with my family, my wife and my 4 years old daughter. We moved here on 2022 from Turkey. 
> 
> I've been working as a software engineer for over **10 years**, andI was able to have some experience in four areas that I think closely related: **software development**, **DevOps and infrastructure**, **technical leadership**, and **Agile process**. I'm based here in Gothenburg with permanent residence. 
>
> Most of my career has been in many different environments and industries, autonomous forklifts at Toyota, embedded automotive software at Volvo, enterprise platforms for medical, durable goods, automotive etc. with strict SLAs at KocSistem. That background gave me the opportunity to think broadly, the code, the pipeline that ships it, the team that maintains it, and the process that keeps everyone aligned."

---

## [[10-pillar-software-dev|Software Development]] (2 min)

> "On the software development side, I've been shipping production **.NET** services for 10 years. Currently at **Combination AB** on **.NET 9** — a microservices platform with more than twenty microservices, each handling one domain. We use three API styles depending on who's calling: **GraphQL** for internal frontends, **gRPC** for [[ref-grpc#When to Use|service-to-service]], and **REST** for external partners. I [[sd-graphql-migration|led the migration from REST to GraphQL]] — gradual rollout, 6 months, zero [[ref-grpc#Versioning|breaking changes]].
>
> I own the API layer and the performance side. When an endpoint is slow, I dig into query plans, serialization costs, and how [[ref-graphql#DataLoader & N+1 Problem|resolvers]] interact with the database — not just add a cache and hope. I also use [[sd-ai-tools|Cursor and Claude Code]] daily for AI-assisted development and have built a practical workflow around where they help and [[ref-ai-tooling#Risks — Where AI Makes Things Worse|where they get in the way]].
>
> Before that, at **Toyota Material Handling**, I worked on **T-ONE** — the system that controls autonomous forklifts. Real-time messaging with **[[ref-rabbitmq#Core Model|RabbitMQ]]** — with a custom NuGet package for typed messaging — fleet state in **[[ref-mongodb#Document Model|MongoDB]]**, everything safety-critical. I maintained **Python test framework [[ref-texttest|TextTest]]** that simulated hundreds of forklifts running at once. I also dealt with a [[sd-rabbitmq-splitbrain|RabbitMQ split-brain]] in production — messages got lost, forklifts stopped, and I learned that reading 
> documentation is not the same as understanding how distributed systems break.
>
> Earlier, at **KocSistem**, I built a **GPS-based warehouse management system** for clients like Arcelik, Beko, and Bosch — real-time truck tracking that [[sd-redis-scaling|had to be rearchitected when we scaled from 50 to 500+ trucks]]. The project won the **2019 IDC Award**. And at **Antasya**, I built an [[sd-avl|AVL system]] for Istanbul's public transport fleet — C# and C++ backend tracking every bus and tram in the city, plus embedded Android devices for in-vehicle signage."

**Sorulursa:** [[10-pillar-software-dev|Software Development Pillar]]

---

## [[11-pillar-devops|DevOps]] (2 min)


> Currently at **Combination AB**, I maintain CI/CD pipelines in Azure DevOps and [[ref-github-actions#Reusable Workflows|GitHub Actions]], manage [[ref-docker#HOW WE USE IT|Docker image optimization]] — brought images from 800MB+ down to 80MB — and configure [[ref-kubernetes#HOW WE USE IT|Kubernetes deployments]] with proper [[ref-kubernetes#Health Probes|health probes]] and [[ref-kubernetes#Deployment Strategies|rolling updates]]."
> 
> Since we had a dedicated devops team on toyota, I did not do much, other than fixing the tests when pipeline is broken.
> 
> "On the DevOps side, my previous relevant experience is at **Volvo Cars** where I was a **Software Factory Engineer**. I owned the release pipeline for embedded automotive software — build, [[ref-cicd-security#Scanning Types|static analysis]], unit tests, hardware-in-the-loop testing, [[ref-automotive-compliance#ISO 26262 — Functional Safety|regulatory]] gate checks, staged rollout. All on **Linux** with **Python** automation and **ZUUL CI** pipelines. I maintained the **[[ref-gerrit#Triggers & Events|Gerrit]]** instance and wrote the [[ref-gerrit#HOW WE USED IT|trigger daemon]] that connected Gerrit events to the build system — including solving silent SSH drops and cutting duplicate builds by 30%. I also wrote the [[do-cynosure-parallel|build orchestration]] that managed parallel builds across QNX, Linux, and Android Automotive targets — brought build time from 40 minutes down to 15. Cut the QA cycle by **30%**, zero [[ref-automotive-compliance#Compliance in Agile|compliance]] findings.
>
> Before Volvo, at **KocSistem**, I [[do-azdevops-zero|built the entire DevOps practice from scratch]]. No CI/CD, no code review, no branching strategy. I built **[[ref-azure-devops#YAML Pipelines|Azure DevOps]]** pipelines with shared YAML templates, set up [[do-terraform-state|Terraform]] for infrastructure — and learned the hard way why [[ref-terraform#State Management|state locking]] is non-negotiable. Integrated [[ref-cicd-security#HOW WE USED IT|security scanning]] into every build and tracked everything with [[ref-dora#HOW WE USED IT|DORA metrics]] in **Grafana**. Weekly to **daily deployments — 7x more frequent**. **Zero [[ref-cicd-security#Quality Gates|pen-test]] findings** for three consecutive quarters.

**Sorulursa:** [[11-pillar-devops|DevOps Pillar]]

---

## [[12-pillar-leadership|Leadership]] (1.5 min)

> "On the leadership side, at **KocSistem** I grew from **Senior Developer** to **Dev Lead** to **Technology Manager** over 4 years. As Technology Manager, I led **25 engineers**, owned the technical roadmap, and [[ls-balance|split my time between coding and managing]] — mornings for technical work, afternoons for people. I [[ls-vision|hit all first-year roadmap targets]] — DevSecOps 75%, Agile 3.1→3.7, 2x releases, zero pen-test findings.
>
> As Dev Lead, I [[ls-transformation|drove a DevOps transformation]] from push-and-pray weekly releases to daily automated deployments. I didn't mandate it — I measured the pain with data, [[ls-ownership|proposed a pilot with our own team]], fixed flaky tests myself, and was online at 6 AM for the first automated deploys. **Weekly to daily in 3 weeks**, org-wide in 6 months. SLA breaches down **60%**, bugs down **55%**.
>
> I also started as the person who [[ls-initiative|built monitoring from scratch]] because I was tired of debugging blind — that initiative [[ls-growth|led to my first promotion]]. And I [[ls-conflict|resolved a conflict]] with a senior developer who wanted a deployment freeze by proposing a 6-week data experiment instead of arguing opinions.
>
> At **Toyota**, I [[ls-empathy|turned a toxic relationship]] with a third-party tech lead into a real partnership by going in person and leading with questions instead of demands. At **Volvo**, I [[ls-composure|drove to the facility at night]] to fix a race condition before they stopped the production line."

**Sorulursa:** [[12-pillar-leadership|Leadership Pillar]]

---

## [[13-pillar-agile|Agile]] (1.5 min)

> "On the Agile side, I'm a **Registered [[ref-agile-ceremonies#Scrum Roles|Scrum Master]]**. At **KocSistem**, I took Agile maturity from **3.1 to 3.7** — not by adding more ceremonies, but by making the existing ones work. [[ag-efficiency|Standups went from 30 minutes to 8]]. [[ag-accountability|Retros started producing real action items]] with owners and deadlines. I [[ag-alignment|introduced sprint goals]] so mid-sprint priority changes had to pass a filter, and started running **live demos** for stakeholders — when they saw working software every two weeks, they stopped micromanaging. I also [[ag-ambition|challenged the team to stretch]] instead of padding sprints, and [[ag-outcomes|killed meetings that didn't produce decisions]].
>
> At **Toyota**, I worked in a **[[ref-agile-ceremonies#Scrum Roles|cross-functional]]** Agile team on safety-critical forklift software. Sprint discipline wasn't optional — a missed test could mean a collision. I pushed for a [[ag-quality|strict Definition of Done]] with safety checklist sign-off and automated test reports. I also [[ag-calibration|fixed estimation]] — everything was a 13, so I brought in reference stories. The [[ag-resilience|RabbitMQ split-brain incident]] changed how the whole team thought about failure testing.
>
> At **Volvo**, I [[ag-compliance|made compliance and agility work together]] by automating regulatory documentation in the pipeline — test reports, [[ref-automotive-compliance#Traceability|traceability]] matrices, change logs — all machine-generated. Regulatory team got better docs, dev team shipped faster.
>
> At **Combination**, I [[ag-adaptability|stepped in for both the tech lead and PO]] when they were unavailable during quarter planning. Ran the planning, set priorities, kept the team aligned. We completed all planned tasks before the quarter ended."

**Sorulursa:** [[13-pillar-agile|Agile Pillar]]

---

## Closing (30 sec)

> "What ties these four areas together: I've been in environments where systems had to work and where cutting corners had real consequences — stopped forklifts, delayed vehicle programs, breached SLAs. That taught me to think about the full chain: **code → pipeline → team → process**. I close gaps — between code and delivery, between teams, between 'working' and 'reliable.' I'd be interested in bringing that here."

---

## Bottom Line (Memorize)

> "I write production backend code, I build the pipelines that ship it, I've led the teams that do both, and I've shaped the Agile processes that keep them aligned."

---

*[[00-dashboard]]*
