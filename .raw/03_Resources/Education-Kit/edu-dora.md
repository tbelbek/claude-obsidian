---
tags:
  - education-kit
---

# DORA Metrics — Education Kit

## What DORA Metrics Are

DORA metrics are four key measurements of software delivery performance, developed by the DevOps Research and Assessment team: Deployment Frequency, Lead Time for Changes, Change Failure Rate, and Mean Time to Restore. Elite teams deploy on demand, have lead times under an hour, change failure rate under 15%, and restore service in under an hour. These metrics correlate with organizational performance — they're not vanity metrics, they predict actual business outcomes.

## The Four Metrics

### Deployment Frequency
- **What** — How often you deploy to production. Elite teams: multiple times per day.
- **How to measure** — Count successful production deployments per week from pipeline logs.

### Lead Time for Changes
- **What** — Time from first commit to production deployment.
- **How to measure** — Record the oldest commit SHA in each deployment. Lead time = deployment timestamp minus oldest commit timestamp.
- **Key insight** — Often the bottleneck is manual approvals, not technical build time.

### Change Failure Rate
- **What** — Percentage of deployments that cause an incident or require a rollback/hotfix.
- **How to measure** — Define consistently (e.g., any deployment requiring a follow-up within 24 hours counts as a failure). Pragmatic, consistent definitions matter more than perfection.

### Mean Time to Restore (MTTR)
- **What** — Time from incident detection to resolution.
- **How to measure** — From incident tracking system: time between incident opened and incident resolved.

## Key Insights

- From the **Accelerate** book by Nicole Forsgren, Jez Humble, Gene Kim. Research across thousands of organizations.
- Speed and stability are NOT trade-offs — the best teams are both fast and reliable.
- Elite performers: multiple deploys/day, <1hr lead time, <15% failure rate, <1hr MTTR.
- **Rate-based alerting** works better than per-build notifications. Teams often ignore per-build notifications within a week. Switch to threshold-based alerting (e.g., 20% failure rate in a rolling hour).

---

## Common Questions

**"How do you use DORA metrics without creating pressure?"**
Track trends, not individual numbers. A single sprint with low deployment frequency doesn't matter — a 3-month downward trend does. Share metrics openly with the team, not as a report card but as a conversation: "our lead time went up this month, what changed?" The team owns the metrics, leadership sees the trends.

**"What do you do when DORA metrics show problems?"**
Dig into the data. If lead time is high, is it build time, test time, or approval time? If change failure rate is high, are you shipping untested code or is test coverage insufficient? The metrics tell you something is wrong — the diagnosis requires understanding the pipeline and the team's workflow.
