---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Agile Leadership — Quick Reference

> [!info] How I've used it: Led 25 engineers at KocSistem with OKRs, servant leadership, blameless post-mortems. Built psychological safety through data-driven decisions and accountability without blame. Registered Scrum Master.

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#OKRs (Objectives and Key Results)\|OKRs]] | quarterly, 4 dimensions, tracked monthly as conversation | [[#Servant Leadership\|servant leadership]] | volunteered for CI/CD pilot, removed obstacles for 25 engineers |
| [[#Blameless Post-Mortems\|blameless post-mortem]] | "what did we not know?" — after RabbitMQ split-brain | [[#Psychological Safety\|psychological safety]] | people report problems early instead of hiding them |
| [[#Data-Driven Decision Making\|data-driven]] | DORA dashboards, "am I seeing this right?" not mandates | [[#Change Management\|change management]] | Kotter's model: urgency→coalition→quick wins→culture |
| [[#Mentoring & 1:1s\|1:1s]] | weekly 30min: "what's blocking you? what to learn?" | | |

## HOW WE USED IT

**OKRs:** At KocSistem as Technology Manager — quarterly OKRs across 4 dimensions. Example: Objective "Improve release reliability" → KR1 "Change failure rate below 15%" → KR2 "MTTR under 1 hour" → KR3 "Zero pen-test findings." Each objective framed as pain the team felt, not management goals. Tracked monthly with the team as a conversation: "we're at X, what's blocking us from Y?"

**Servant Leadership:** At KocSistem as Dev Lead — [[ls-ownership|volunteered our team for the CI/CD pilot]], fixed flaky tests myself, online at 6 AM for first deploys. Didn't mandate change — showed it works. The most impactful thing a tech manager does isn't write code — it's [[ls-balance|remove obstacles for 25 others]].

**Blameless Post-Mortems:** After the [[sd-rabbitmq-splitbrain|RabbitMQ split-brain at Toyota]] — ran a post-mortem focused on "what did we not know?" and "what should we change?" — not "who screwed up?" Built psychological safety — people started reporting problems early instead of hiding them.

**Data-Driven Decisions:** [[ls-transformation|Measured deployment pain with data]], presented as "am I seeing this right?" not "here's what's wrong." [[ref-dora#HOW WE USED IT|DORA dashboards]] made pipeline health visible. [[ls-conflict|6-week experiment]] settled the deployment freeze debate — data decided, not opinions.

**Mentoring:** Weekly 30-minute 1:1s with direct reports. Format: "What's blocking you? What do you want to learn? How can I help?" Best 1:1s are the ones where the direct report does most of the talking.

**Change Management:** [[ls-transformation|Kotter's model in practice]]: created urgency (showed the data), built coalition (pilot team), quick wins (daily deploys in 3 weeks), anchored in culture (org-wide in 6 months). Change fails when you skip the urgency step — if people don't feel the pain, they don't see the need.

---

## Key Concepts

### What Agile Leadership Is
Agile Leadership is leading through influence, data, and service — not authority and mandates. It means removing blockers instead of assigning tasks, measuring outcomes instead of activity, creating psychological safety so people report problems early, and using frameworks (OKRs, blameless post-mortems, data-driven decisions) to align teams without micromanaging. The hardest part isn't the framework — it's consistently modeling the behavior you expect from others.

### OKRs (Objectives and Key Results)
- **What** — Goal-setting framework. Objective = what you want to achieve. Key Results = how you measure it.
- **How I used it** — Quarterly OKRs for the technical roadmap at KocSistem. Example: Objective: "Improve release reliability" → KR1: "Change failure rate below 15%" → KR2: "MTTR under 1 hour" → KR3: "Zero pen-test findings."
- **Key insight** — Frame objectives as pain the team feels, not management goals. "Let's measure commit-to-production time" resonates more than "implement DevSecOps metrics."
- **Reference** — Measure What Matters by John Doerr.

### Servant Leadership
- **What** — The leader serves the team by removing blockers and creating conditions for success. Not "I tell you what to do" but "what's in your way?"
- **How I used it** — At KocSistem as Dev Lead, I [[ls-ownership|volunteered our team for the CI/CD pilot]], fixed flaky tests myself, and was online at 6 AM. I didn't mandate change — I showed it works.
- **Key insight** — The most impactful thing a tech manager does isn't write code — it's [[ls-balance|remove obstacles for 25 others]].
- **Reference** — Robert Greenleaf's Servant Leadership concept. Netflix culture doc: "lead by context, not control."

### Blameless Post-Mortems
- **What** — After an incident, analyze what happened and what to change — without blaming individuals. Humans make mistakes; systems should prevent those mistakes from causing outages.
- **How I used it** — After the [[sd-rabbitmq-splitbrain|RabbitMQ split-brain at Toyota]], I ran a post-mortem focused on "what did we not know?" and "what should we change?" — not "who screwed up?"
- **Key insight** — If people fear blame, they hide mistakes. If they feel safe, they report problems early — when they're still small.
- **Reference** — John Allspaw (Etsy), Google SRE Book.

### Psychological Safety
- **What** — Team members feel safe to take risks, make mistakes, and speak up without fear of punishment.
- **How I used it** — At KocSistem, I [[ls-conflict|proposed a data experiment instead of overruling a senior developer]]. The team saw decisions were fair because they were based on evidence. At Toyota, [[ag-resilience|the RabbitMQ incident post-mortem]] built safety by showing failures were learning opportunities.
- **Key insight** — Teams with high psychological safety learn faster and perform better.
- **Reference** — Amy Edmondson's research at Harvard.

### Data-Driven Decision Making
- **What** — Use data instead of opinions to make decisions. Removes politics from disagreements.
- **How I used it** — [[ls-transformation|Measured deployment pain with data]], presented as "am I seeing this right?" not "here's what's wrong." [[ref-dora#HOW WE USED IT|DORA dashboards]] made pipeline health visible. [[ls-conflict|6-week experiment]] settled the deployment freeze debate.
- **Key insight** — Data speaks louder than opinions. Leaders don't argue with charts that go in the right direction.
- **Reference** — Crucial Conversations (shared pool of meaning).

### Mentoring & 1:1s
- **What** — Regular one-on-one meetings with each team member. Not status updates — career development, blockers, feedback.
- **How I used it** — Weekly 30-minute 1:1s with direct reports at KocSistem. Format: "What's blocking you? What do you want to learn? How can I help?"
- **Key insight** — The best 1:1s are the ones where the direct report does most of the talking. Your job is to listen and unblock.
- **Reference** — The Manager's Path by Camille Fournier.

### Change Management
- **What** — How to drive organizational change without mandate or authority.
- **How I used it** — [[ls-transformation|Kotter's 8-step model]]: create urgency (data), build coalition (pilot team), quick wins (daily deploys in 3 weeks), anchor in culture (org-wide in 6 months).
- **Key insight** — Change fails when you skip the urgency step. If people don't feel the pain, they don't see the need.
- **Reference** — John Kotter's Leading Change.

## Sorulursa

> [!faq]- "How do you handle underperformers?"
> Direct conversations, early. Talk in 1:1 — "I've noticed X, what's going on?" Usually it's a tooling problem, unclear requirements, or a personal issue. Remove the blocker first. If it's a genuine skill gap, set clear expectations with a timeline and check weekly. Never let performance issues fester — unfair to the person and the team.

> [!faq]- "How do you build trust with a new team?"
> Listen first, act second. First 2 weeks: mostly 1:1s, understanding the pain points, learning the codebase. First quick win: fix something that's been annoying the team for months — a flaky test, a slow pipeline, a bad process. Actions build trust faster than words.

> [!faq]- "How do you balance team autonomy with alignment?"
> Three things: clear OKRs (everyone knows what we're building toward), team-level sprint autonomy (each team owns their sprint), and shared infrastructure (pipeline templates, coding standards, architecture decisions). Teams decide how to build, leadership decides what to build.

---

*[[00-dashboard]]*
