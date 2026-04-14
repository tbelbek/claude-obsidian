---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# DORA Metrics — Quick Reference

> [!info] How I've used it: Built DORA dashboards in Grafana at KocSistem. Tracked all four metrics, reported monthly to leadership. Used data to justify automation investments. Lead time insight (4 days, mostly manual approvals) changed how we handled deployment gates.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Deployment Frequency\|deploy frequency]] | weekly→daily at KocSistem, measures delivery tempo | [[#Lead Time for Changes\|lead time]] | 4 days → mostly manual approvals, changed gate strategy |
| [[#Change Failure Rate\|change failure rate]] | <15% target, caught by automated testing | [[#Mean Time to Restore (MTTR)\|MTTR]] | <1 hour target, automated rollback helps |
| [[#Key Insights\|key insights]] | data justified automation investments, monthly reports | | |

## HOW WE USED IT

At KocSistem, I [[ref-dora#HOW WE USED IT|built DORA metric dashboards]] in Grafana and reported monthly to leadership. The metrics drove concrete decisions about pipeline investments.

**What I built:**
- Grafana dashboards tracking all four metrics with weekly and monthly trend lines
- Custom pipeline step that recorded the oldest commit SHA in each deployment — this is how I calculated lead time (deployment timestamp minus oldest commit timestamp)
- Change failure rate definition: any deployment requiring a follow-up within 24 hours counts as a failure — pragmatic, consistent, debated for weeks before the team agreed
- Rate-based alerting: pipeline failure rate > 20% in rolling hour → Slack notification. Per-build notifications failed — team ignored them within a week

**How it drove decisions:**
- First dashboard showed 4-day average lead time — mostly manual approval bottlenecks, not technical issues. That data point justified automating non-production approval gates
- Showed leadership: "we spend 40% of our time on manual deployments and incident response. If we automate, that time goes back to feature development." Charts going in the right direction ended the debate
- Tracked improvement over time: weekly → daily deployments, lead time 4 days → under 1 day for non-production

**Where we ended up:** Solidly "high performer" on the DORA scale — daily deployments, ~2-day lead time for production (approval gates), ~10% change failure rate. Not elite, but a massive improvement from where we started.

---

## The Four Metrics

### What DORA Metrics Are
DORA metrics are four key measurements of software delivery performance, developed by the DevOps Research and Assessment team: Deployment Frequency, Lead Time for Changes, Change Failure Rate, and Mean Time to Restore. Elite teams deploy on demand, have lead times under an hour, change failure rate under 15%, and restore service in under an hour. These metrics correlate with organizational performance — they're not vanity metrics, they predict actual business outcomes.

### Deployment Frequency
- **What** — How often you deploy to production. Elite teams: multiple times per day.
- **How I measured** — Count successful production deployments per week from pipeline logs.

### Lead Time for Changes
- **What** — Time from first commit to production deployment.
- **How I measured** — Pipeline step records oldest commit SHA in each deployment. Lead time = deployment timestamp - oldest commit timestamp.
- **Our result** — 4 days average, mostly manual approval bottlenecks.

### Change Failure Rate
- **What** — Percentage of deployments that cause an incident or require a rollback/hotfix.
- **How I measured** — Any deployment requiring a follow-up within 24 hours counts as a failure. Pragmatic, consistent.

### Mean Time to Restore (MTTR)
- **What** — Time from incident detection to resolution.
- **How I measured** — From incident tracking system: time between incident opened and incident resolved.

## Key Insights

- From the **Accelerate** book by Nicole Forsgren, Jez Humble, Gene Kim. Research across thousands of organizations.
- Speed and stability are NOT trade-offs — the best teams are both fast and reliable.
- Elite performers: multiple deploys/day, <1hr lead time, <15% failure rate, <1hr MTTR.
- **Rate-based alerting** — [[ref-dora#HOW WE USED IT|Per-build notifications failed (team ignored them in a week)]]. Switched to 20% failure rate threshold in rolling hour.

## Sorulursa

> [!faq]- "How do you use DORA metrics without creating pressure?"
> Track trends, not individual numbers. A single sprint with low deployment frequency doesn't matter — a 3-month downward trend does. Share metrics openly with the team, not as a report card but as a conversation: "our lead time went up this month, what changed?" The team owns the metrics, leadership sees the trends.

> [!faq]- "What do you do when DORA metrics show problems?"
> Dig into the data. If lead time is high, is it build time, test time, or approval time? If change failure rate is high, are we shipping untested code or is our test coverage insufficient? The metrics tell you something is wrong — the diagnosis requires understanding the pipeline and the team's workflow.

## Also relevant to

- [[ls-initiative]] — Building monitoring as a side project led to DORA metrics work
- [[ls-vision]] — DORA metrics were part of the roadmap I owned as Technology Manager
- [[12-pillar-leadership|Leadership Pillar]] — Using data to justify infrastructure investments

---

*[[00-dashboard]]*
