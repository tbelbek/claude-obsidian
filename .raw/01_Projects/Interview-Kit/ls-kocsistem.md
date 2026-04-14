---
tags:
  - interview-kit
  - interview-kit/leadership
up: [[12-pillar-leadership]]
---

*[[00-dashboard|Home]] > [[12-pillar-leadership|Leadership & Soft Skills]] > KOCSISTEM*

# KOCSISTEM — Leadership Journey

KocSistem is one of Turkey's largest IT services companies — part of the Koc Group, the country's biggest industrial conglomerate. I spent 4 years there, growing through three roles. Each one taught me something different about leadership, and together they gave me the full arc: from individual contributor who sees a gap and fills it, to team lead who changes how a team works, to manager who owns the direction for 25 engineers.

---

## Senior Software Developer (Mar 2018 – Feb 2020)

I was hired to write backend code for a GPS-based warehouse management system. The technical work was interesting — .NET Core, Redis, Elasticsearch, RabbitMQ, consulting for major clients like Arcelik, Beko, Bosch, Aygaz. But the leadership story starts here because I kept running into the same problem: **no production visibility**. When something broke, we spent hours guessing. There was no monitoring, no dashboards, no alerts.

Nobody asked me to fix this. I wasn't hired for infrastructure. But I was tired of wasting 3 hours tracking down bugs that proper metrics would surface in 3 minutes. So I [[ls-initiative|spent weekends learning monitoring tools, built a proof-of-concept]] — [[ref-grafana-prometheus#Prometheus|Prometheus]] for metrics, [[ref-grafana-prometheus#Grafana|Grafana]] for dashboards, basic latency and error rate tracking. Showed it to my lead. His reaction: "Why don't we have this already?"

I got approval to deploy it properly. Wrote alert rules, set up dashboards, documented everything. The hard part wasn't the tech — it was [[ls-growth|getting the team to actually use it]]. I started every [[ref-agile-ceremonies#Daily Standup|standup]] with "here's what the dashboard showed overnight." After a few weeks where we caught issues before users reported them, people started checking on their own. Detection time went from hours to minutes. It became the template for every new service.

That initiative — seeing a problem nobody assigned to me, solving it, and making it stick — is what led to my **promotion to Dev Lead**.

---

## Software Development Lead (Mar 2020 – Jul 2021)

As Dev Lead, I owned the team's day-to-day: planning, [[ref-agile-leadership#Mentoring & 1:1s|1:1s]], technical direction, architecture decisions. But the biggest job was changing how the team worked.

When I took over, the team was doing **"push and pray" releases** — manual deployments, weekly at best, no automated tests, no rollback plan. When something broke, everyone scrambled. Developers didn't trust automation because they'd never seen it work.

I [[ls-transformation|didn't walk in and announce "we're doing CI/CD now."]] I started by measuring the pain: deployment times, failure rates, how much time the team spent in meetings vs actually coding. Then I showed the data to the team — not as "here's what's wrong" but as "am I reading this right?" I [[ls-ownership|proposed a pilot]]: one team, two sprints, daily deployments with automated checks. I volunteered our team. I pair-programmed with the biggest skeptics, fixed flaky tests myself, and was online at 6 AM for the first automated deploys.

The pilot team went from weekly to daily in **3 weeks**. Other teams saw it working and asked for the same setup. **Six months later, the whole organization had shifted.**

I also [[ref-code-review#HOW WE SET IT UP|built the code review culture from scratch]]. The team had no PR process — developers pushed directly to main. I set up feature branches, mandatory pull requests with at least one approval, automated quality gates in CI, and PR templates. The cultural part was harder: first few weeks, reviews were rubber stamps. I started writing detailed reviews on every PR to set the standard, paired with resistant developers, and set a 4-hour turnaround expectation. Bug rate dropped 55% — most bugs caught in review, not production.

During this time I also [[ls-conflict|dealt with a conflict]] — a senior developer who wanted a monthly deployment freeze because he'd been burned by a Friday outage. Team of 25 was split. Instead of arguing, I proposed a 6-week experiment: track every failure and check if a freeze would've helped. The data showed the issues were config drift and missing tests — not deployment timing. He ended up becoming one of the strongest advocates for daily deployments.

I also overhauled the **Git workflow** — we went from everyone pushing to main to proper branching, pull requests, and code review standards. Set up **[[ref-cicd-security#Quality Gates|quality gates]]** that blocked merges if tests failed or security issues were found.

**Results:** SLA breach rate **down 60%** | CI/CD pipelines live for **all apps** | Bug rate in new releases **down 55%** | User satisfaction **up 50%**

---

## Technology Manager (Jul 2021 – Feb 2022)

As Technology Manager, I led **25 engineers** — about half my time was hands-on coding, the other half was planning, roadmapping, 1:1s, and unblocking people. The [[ls-balance|hardest part was protecting both]] — I learned to block mornings for technical work and afternoons for people work.

I owned the **technical roadmap** across four dimensions: DevOps, security posture, architecture direction, and Agile process improvements. Each one had a measurable target. I [[ls-vision|framed every roadmap item]] as "this will make your life easier" — not "leadership wants this number." DevSecOps metrics, Agile maturity, release frequency, security posture — all had clear before/after numbers.

I also acted as **[[ref-agile-ceremonies#Scrum Roles|Product Owner]]** for the HR employee experience platform — gathering requirements from business stakeholders, prioritizing the [[ref-agile-ceremonies#Sprint Planning|backlog]], making trade-off decisions. This was my first PO experience, and it later helped me at Combination when I stepped in for an absent PO.

**Mentoring** was a big part of the role. I worked with engineers at every level — pairing with juniors on their first PRs, coaching mids on technical decision-making, and giving seniors space to lead projects. I ran and spoke at **internal tech events** — both technical deep-dives and broader company meetings.

**Results:** All first-year roadmap targets **hit** | DevSecOps 4 Key Metrics **75%** | Agile maturity **3.1→3.7** | Release frequency **doubled** | **Zero [[ref-cicd-security#Quality Gates|pen-test]] findings** across all web apps

---

## The Full Arc

What makes KocSistem my strongest leadership story is the **continuity**. The monitoring I built as a Senior Dev was still running when I left as Technology Manager. The CI/CD pipelines I set up as Dev Lead, I got to measure with [[ref-dora#Deployment Frequency|DORA]] metrics as Manager. The Agile ceremonies I reformed, I got to see mature over 8 months. Not many people get to see that full transformation arc at one company — from nothing to a well-oiled machine. The changes I made as an individual contributor compounded as I moved into leadership. That's the kind of long-term ownership I care about.

## Key Experiences
- [[ls-balance|BALANCE — half code half meetings, morning/afternoon split]]
- [[ls-vision|VISION — DevSecOps 4 Key Metrics 75%, 2x release frequency]]
- [[ls-transformation|TRANSFORMATION — push-and-pray team, data-first pitch, pilot proved model]]
- [[ls-ownership|OWNERSHIP — volunteered team, weekly→daily 3 weeks, org-wide 6 months]]
- [[ls-initiative|INITIATIVE — built monitoring POC on own time, detection hours→minutes]]
- [[ls-growth|GROWTH — not my job, led to promotion to Dev Lead]]
- [[ls-conflict|CONFLICT — senior dev wanted freeze, 6-week data experiment, became advocate]]

## Sorulursa

> [!faq]- "What did 'owning the technical roadmap' look like in practice?"
> Quarterly OKRs across four dimensions. **DevOps:** CI/CD pipeline maturity, deployment frequency targets, mean time to restore. **Security:** pen-test finding targets, secret management migration, scanning coverage. **Architecture:** service decomposition decisions, technology evaluations, technical debt prioritization. **Agile:** maturity score targets, ceremony effectiveness, stakeholder satisfaction. Each dimension had 2-3 measurable key results. I tracked progress monthly with the team — not as a report card but as a conversation: "we're at X, what's blocking us from Y?" The roadmap wasn't a static document — it evolved based on what we learned each quarter. Some items got deprioritized because the pain went away, others got escalated because new problems appeared. The important thing was having clear targets and measuring against them.

> [!faq]- "Why did you stay 4 years at one company?"
> Because I kept growing. Every 12-18 months the role changed — new challenges, new responsibilities. Staying let me see the long-term impact of changes I made. The CI/CD transformation I started as Dev Lead, I got to measure and optimize as Technology Manager. You don't get that continuity if you switch jobs every year.

> [!faq]- "How did you handle the transition from IC to manager?"
> The hardest part was letting go of being the one who ships code. My output was no longer measured by my commits — it was measured by what 25 other people shipped. I had to learn that unblocking someone in a 30-minute conversation is more valuable than writing code for 3 hours. The Manager's Path by Camille Fournier helped me think about this transition.

> [!faq]- "What would you do differently?"
> I'd set up monitoring and CI/CD on day one at the Senior Dev level, not wait until I felt the pain. The monitoring POC would've been easier to build when the codebase was smaller. Also, I'd have pushed for Terraform [[ref-terraform#State Management|state locking]] from the start — the corruption incident was avoidable.

> [!faq]- "How did you handle underperformers?"
> Direct conversations, early. If someone was struggling, I'd talk to them in 1:1 — "I've noticed X, what's going on?" Usually it was a tooling problem, an unclear requirement, or a personal issue. Nine times out of ten, removing the blocker fixed the performance. The rare time it was a skill gap, I'd set clear expectations with a timeline and check in weekly. I never let performance issues fester — that's unfair to the person and to the team.

> [!faq]- "How did you keep 25 engineers aligned?"
> Three things. First, a clear technical roadmap with quarterly [[ref-agile-leadership#OKRs (Objectives and Key Results)|OKRs]] — everyone knew what we were building toward. Second, team-level autonomy with company-level alignment — each team owned their sprint, but we synced on architecture and shared templates. Third, visibility — DORA dashboards, [[ref-agile-ceremonies#Sprint Review / Demo|sprint demos]], and a weekly 15-minute leadership sync where I shared progress and blockers. No status reports — just "here's what's moving and here's what's stuck."

---

*[[00-dashboard|Home]] > [[12-pillar-leadership|Leadership & Soft Skills]]*
