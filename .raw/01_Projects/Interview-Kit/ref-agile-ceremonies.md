---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Agile Ceremonies — Quick Reference

> [!info] How I've used it: Reformed all ceremonies at KocSistem (standups 30→8min, retros with accountability, sprint goals, live demos). Strict DoD at Toyota for safety-critical software. Registered Scrum Master.

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Daily Standup\|standup]] | 30→8min, team-level, blockers only | [[#Sprint Planning\|sprint planning]] | reference stories, planning poker, calibrate points |
| [[#Retrospective\|retro]] | 2 action items with owner+deadline, review next retro | [[#Sprint Review / Demo\|sprint review]] | live demos to stakeholders every 2 weeks |
| [[#Definition of Done\|Definition of Done]] | tests+report+safety checklist at Toyota | [[#Scrum Roles\|Scrum roles]] | Registered Scrum Master, reformed all ceremonies |
| [[#HOW WE USED IT\|velocity]] | challenge sprint padding, track trends | [[#HOW WE USED IT\|meeting audit]] | "what decision did this produce?" — fix or cancel |
| [[#Scrum vs Kanban\|Scrum vs Kanban]] | Scrum=sprints+roles, Kanban=flow+WIP limits | | |

## HOW WE USED IT

**At KocSistem (25 engineers, Technology Manager):**
- [[ag-efficiency|Standups]]: broke 25-person, 30-minute status meetings into team-level (5-6 people), blockers only. 30 min → 8 min. Remote teams used async Slack updates + call only if blockers
- [[ag-accountability|Retros]]: 2 action items per retro, each with owner and deadline. Next retro starts by reviewing them. After 3 sprints of actually fixing problems, team started taking retros seriously
- [[ag-alignment|Sprint goals]]: one sentence per sprint. Mid-sprint request doesn't serve the goal → backlog. Genuinely urgent → conversation about what we drop
- [[ag-calibration|Planning poker]]: fixed estimation by introducing reference stories. "Why is this an 8 when I said 3?" surfaces hidden dependencies
- [[ag-ambition|Velocity]]: challenged sprint padding — always hitting 100% means you're not being challenged. Tracked trends, normalized occasional misses
- [[ag-outcomes|Meeting audit]]: "what decision did this meeting produce?" If nothing → fix or cancel
- Live demos for stakeholders — working software every 2 weeks. Stopped micromanaging because they had visibility

**At Toyota (safety-critical, cross-functional):**
- [[ag-quality|Strict DoD]]: integration tests on simulated fleet + test report archived + safety checklist signed off. Automated mechanical parts — 2 days overhead → half day
- [[ag-calibration|Reference stories]]: fixed point inflation (everything was a 13) by pinning 5 completed stories as calibration points

**At Volvo (regulated automotive):**
- [[ag-compliance|Automated compliance docs]]: test reports, traceability matrices, change logs generated in the pipeline — not manual Word documents. Regulatory team got better docs, dev team shipped faster

---

## Key Concepts

### What Agile Ceremonies Are
Agile ceremonies are the recurring meetings that structure a Scrum sprint — standup, planning, review, retrospective. They exist to create alignment, visibility, and continuous improvement. The value isn't in the ceremony itself but in what it produces: standups surface blockers, planning creates shared commitment, reviews give stakeholders visibility, retros drive actual change. When ceremonies become ritual without outcomes, they're waste — I've reformed every one of these at KocSistem.

### Daily Standup
- **Purpose** — Synchronize on blockers, not give status reports. Scrum Guide says 15 min max.
- **Anti-pattern** — 25 people, 30 minutes, nobody listening. [[ag-discipline|Fix: small teams, blockers only]].
- **At KocSistem** — I broke 25-person standups into team-level (5-6 people), blockers only. 30 minutes → 8 minutes. Remote teams used async Slack updates + short call only if blockers existed.
- **Remote** — Async Slack updates + short call only if there's something to discuss.

### Sprint Planning
- **Sprint goal** — One sentence describing what this sprint delivers. [[ag-alignment|Protects scope from mid-sprint changes]].
- **Planning poker** — Not for precision. The conversation surfaces hidden risks. "Why is this an 8 when I said 3?" [[ag-calibration|Reference stories for calibration]].
- **Story points** — Relative complexity, not time. A story that takes a senior 2 hours and a junior 2 days is the same complexity.
- **Velocity** — Average story points per sprint. Use for forecasting, not for pressure. [[ag-ambition|Track trends, challenge padding]].
- **At Toyota** — I fixed estimation by introducing reference stories and planning poker. Point inflation (everything was a 13) disappeared when the team had concrete examples to compare against.

### Retrospective
- **Purpose** — Inspect and adapt. What to improve next sprint.
- **Anti-pattern** — Complain, feel better, change nothing. [[ag-accountability|Fix: 2 action items, owner + deadline, review at next retro]].
- **Formats** — Rotate between Start/Stop/Continue, 4Ls, Sailboat to prevent staleness.
- **At KocSistem** — 2 action items per retro, owner + deadline. Reviewed at next retro. After 3 sprints of actually fixing problems, the team stopped treating retros as a waste of time.

### Sprint Review / Demo
- **Purpose** — Show working software to stakeholders. Get real feedback.
- **Anti-pattern** — Slides and screenshots. [[ag-alignment|Fix: live working software, clickable demo]].
- **Impact** — When stakeholders see working software every 2 weeks, they stop micromanaging.

### Definition of Done
- **Standard** — Code reviewed, tests passing, deployed to staging.
- **Safety-critical** — Add: integration tests, test report archived, safety checklist signed off. [[ag-quality|Automate the mechanical parts]].
- **Rule** — If DoD is too expensive, automate parts or reduce sprint scope. Never pretend it doesn't exist.
- **At Toyota** — Extended DoD for safety-critical: integration tests on simulated fleet + test report archived + safety checklist signed off. Automated the mechanical parts, brought overhead from 2 days to half a day per story.

### Scrum Roles
- **Product Owner** — Owns the backlog. Prioritizes by business value. Protects sprint scope.
- **Scrum Master** — Facilitates ceremonies, removes impediments, coaches the team. Tool, not identity.
- **Cross-functional team** — Developers, testers, domain experts in the same sprint. No handoffs.

---

### Scrum vs Kanban
- **Scrum** — Fixed-length sprints (1-4 weeks), sprint planning, daily standup, sprint review, retrospective. Prescribed roles (PO, SM, Dev Team). Commitment to sprint scope. Best when: work can be planned in chunks, team needs rhythm and predictability. *(we used Scrum at KocSistem and Toyota — sprint goals gave us scope protection)*
- **Kanban** — Continuous flow, no sprints. WIP limits control throughput. Pull-based — new work starts when capacity opens. No prescribed roles or ceremonies (though most teams keep standups). Best when: work arrives unpredictably (support, ops), or team needs flexibility without sprint commitments.
- **Scrumban** — Scrum structure (sprints, standups) with Kanban mechanics (WIP limits, flow metrics). Many teams evolve here naturally — keep the ceremonies that work, add WIP limits to prevent overload.
- **My experience** — Used Scrum at KocSistem (needed structure to fix chaos), Toyota (safety-critical needed sprint discipline), and Combination. Kanban would fit better for pure ops/support teams where work is unpredictable.

## Sorulursa

> [!faq]- "How do you handle a team that resists Agile ceremonies?"
> I don't force it. I measure the pain first — how long do deployments take, how many bugs escape, how much time is spent in meetings vs coding. Then I show the data and propose one change at a time. At KocSistem, I started with standups (easiest win — 30 min to 8 min, everyone noticed). Once the team saw that one ceremony actually helped, they were more open to fixing the others. Change works when people feel the benefit, not when you lecture them about the Scrum Guide.

> [!faq]- "What's your standup format?"
> Three questions, but only if relevant: "What's blocking you?" is the only required one. "What did you do?" and "What will you do?" are optional — if nothing changed since yesterday, don't waste everyone's time. Blockers get assigned immediately — "who can help with this?" If nobody can, I take it. 8 minutes max for a team of 6.

> [!faq]- "How do you make retros produce real change?"
> Two rules: (1) Every retro produces exactly 2 action items with an owner and a deadline. (2) Next retro starts by reviewing those items. If we didn't complete them, we discuss why before raising new issues. After 3 sprints of actually fixing problems, people started coming to retros with specific, actionable suggestions instead of vague complaints.

> [!faq]- "How do you handle Definition of Done in different contexts?"
> Standard DoD for web apps: code reviewed, tests passing, deployed to staging. For safety-critical (Toyota): add integration tests on simulated fleet, test report archived, safety checklist signed off. For regulated (Volvo): add compliance documentation generated in pipeline. The DoD should match the risk level — don't over-engineer for a CRUD app, don't under-engineer for forklift software.

> [!faq]- "Sprint goals — how do you write a good one?"
> One sentence, outcome-oriented. "Users can check out with Apple Pay" not "complete tickets 123-128." A good sprint goal answers: "If we only deliver one thing this sprint, what should it be?" Everything else in the sprint supports the goal or is secondary. When a new request comes in mid-sprint, the question becomes: "Does this serve the sprint goal?"

---

*[[00-dashboard]]*
