---
tags:
  - education-kit
---

# Agile Leadership — Education Kit

## What Agile Leadership Is

Agile Leadership is leading through influence, data, and service — not authority and mandates. It means removing blockers instead of assigning tasks, measuring outcomes instead of activity, creating psychological safety so people report problems early, and using frameworks (OKRs, blameless post-mortems, data-driven decisions) to align teams without micromanaging. The hardest part isn't the framework — it's consistently modeling the behavior you expect from others.

## OKRs (Objectives and Key Results)

- **What** — Goal-setting framework. Objective = what you want to achieve. Key Results = how you measure it.
- **Example** — Objective: "Improve release reliability" -> KR1: "Change failure rate below 15%" -> KR2: "MTTR under 1 hour" -> KR3: "Zero pen-test findings."
- **Key insight** — Frame objectives as pain the team feels, not management goals. "Let's measure commit-to-production time" resonates more than "implement DevSecOps metrics."
- **Reference** — Measure What Matters by John Doerr.

## Servant Leadership

- **What** — The leader serves the team by removing blockers and creating conditions for success. Not "I tell you what to do" but "what's in your way?"
- **Key insight** — The most impactful thing a tech manager does isn't write code — it's remove obstacles for the team.
- **Reference** — Robert Greenleaf's Servant Leadership concept. Netflix culture doc: "lead by context, not control."

## Blameless Post-Mortems

- **What** — After an incident, analyze what happened and what to change — without blaming individuals. Humans make mistakes; systems should prevent those mistakes from causing outages.
- **Key insight** — If people fear blame, they hide mistakes. If they feel safe, they report problems early — when they're still small.
- **Reference** — John Allspaw (Etsy), Google SRE Book.

## Psychological Safety

- **What** — Team members feel safe to take risks, make mistakes, and speak up without fear of punishment.
- **Key insight** — Teams with high psychological safety learn faster and perform better. Data experiments and evidence-based decisions build safety by showing that decisions are fair.
- **Reference** — Amy Edmondson's research at Harvard.

## Data-Driven Decision Making

- **What** — Use data instead of opinions to make decisions. Removes politics from disagreements.
- **Key insight** — Data speaks louder than opinions. Present findings as "am I seeing this right?" not "here's what's wrong." DORA dashboards make pipeline health visible. Time-boxed experiments settle debates — data decides, not opinions.
- **Reference** — Crucial Conversations (shared pool of meaning).

## Mentoring & 1:1s

- **What** — Regular one-on-one meetings with each team member. Not status updates — career development, blockers, feedback.
- **Format** — Weekly 30 minutes: "What's blocking you? What do you want to learn? How can I help?"
- **Key insight** — The best 1:1s are the ones where the direct report does most of the talking. Your job is to listen and unblock.
- **Reference** — The Manager's Path by Camille Fournier.

## Change Management

- **What** — How to drive organizational change without mandate or authority.
- **Framework** — Kotter's 8-step model: create urgency (data), build coalition (pilot team), quick wins (visible improvements in weeks), anchor in culture (org-wide adoption over months).
- **Key insight** — Change fails when you skip the urgency step. If people don't feel the pain, they don't see the need.
- **Reference** — John Kotter's Leading Change.

---

## Common Questions

**"How do you handle underperformers?"**
Direct conversations, early. Talk in 1:1 — "I've noticed X, what's going on?" Usually it's a tooling problem, unclear requirements, or a personal issue. Remove the blocker first. If it's a genuine skill gap, set clear expectations with a timeline and check weekly. Never let performance issues fester — unfair to the person and the team.

**"How do you build trust with a new team?"**
Listen first, act second. First 2 weeks: mostly 1:1s, understanding the pain points, learning the codebase. First quick win: fix something that's been annoying the team for months — a flaky test, a slow pipeline, a bad process. Actions build trust faster than words.

**"How do you balance team autonomy with alignment?"**
Three things: clear OKRs (everyone knows what we're building toward), team-level sprint autonomy (each team owns their sprint), and shared infrastructure (pipeline templates, coding standards, architecture decisions). Teams decide how to build, leadership decides what to build.
