---
tags:
  - education-kit
---

# Agile Ceremonies — Education Kit

## What Agile Ceremonies Are

Agile ceremonies are the recurring meetings that structure a Scrum sprint — standup, planning, review, retrospective. They exist to create alignment, visibility, and continuous improvement. The value isn't in the ceremony itself but in what it produces: standups surface blockers, planning creates shared commitment, reviews give stakeholders visibility, retros drive actual change. When ceremonies become ritual without outcomes, they're waste.

## Daily Standup

- **Purpose** — Synchronize on blockers, not give status reports. Scrum Guide says 15 min max.
- **Anti-pattern** — 25 people, 30 minutes, nobody listening. Fix: small teams (5-6 people), blockers only.
- **Best practice** — Break large teams into team-level standups. Remote teams can use async updates + short call only if blockers exist.
- **Format** — "What's blocking you?" is the only required question. If nothing changed since yesterday, don't waste everyone's time.

## Sprint Planning

- **Sprint goal** — One sentence describing what this sprint delivers. Protects scope from mid-sprint changes. Mid-sprint request doesn't serve the goal? Goes to backlog. Genuinely urgent? Conversation about what to drop.
- **Planning poker** — Not for precision. The conversation surfaces hidden risks. "Why is this an 8 when I said 3?" reveals hidden dependencies.
- **Story points** — Relative complexity, not time. A story that takes a senior 2 hours and a junior 2 days is the same complexity.
- **Velocity** — Average story points per sprint. Use for forecasting, not for pressure. Track trends, challenge padding — always hitting 100% means you're not being challenged.
- **Reference stories** — Pin completed stories as calibration points to fix point inflation.

## Retrospective

- **Purpose** — Inspect and adapt. What to improve next sprint.
- **Anti-pattern** — Complain, feel better, change nothing. Fix: 2 action items per retro, each with owner and deadline. Review at next retro.
- **Formats** — Rotate between Start/Stop/Continue, 4Ls, Sailboat to prevent staleness.
- **Key insight** — After 3 sprints of actually fixing problems, teams stop treating retros as a waste of time.

## Sprint Review / Demo

- **Purpose** — Show working software to stakeholders. Get real feedback.
- **Anti-pattern** — Slides and screenshots. Fix: live working software, clickable demo.
- **Impact** — When stakeholders see working software every 2 weeks, they stop micromanaging because they have visibility.

## Definition of Done

- **Standard** — Code reviewed, tests passing, deployed to staging.
- **Safety-critical** — Add: integration tests, test report archived, safety checklist signed off.
- **Regulated** — Add: compliance documentation generated in pipeline.
- **Rule** — If DoD is too expensive, automate parts or reduce sprint scope. Never pretend it doesn't exist.

## Scrum Roles

- **Product Owner** — Owns the backlog. Prioritizes by business value. Protects sprint scope.
- **Scrum Master** — Facilitates ceremonies, removes impediments, coaches the team. Tool, not identity.
- **Cross-functional team** — Developers, testers, domain experts in the same sprint. No handoffs.

## Scrum vs Kanban

- **Scrum** — Fixed-length sprints (1-4 weeks), sprint planning, daily standup, sprint review, retrospective. Prescribed roles (PO, SM, Dev Team). Commitment to sprint scope. Best when: work can be planned in chunks, team needs rhythm and predictability.
- **Kanban** — Continuous flow, no sprints. WIP limits control throughput. Pull-based — new work starts when capacity opens. No prescribed roles or ceremonies. Best when: work arrives unpredictably (support, ops), or team needs flexibility without sprint commitments.
- **Scrumban** — Scrum structure (sprints, standups) with Kanban mechanics (WIP limits, flow metrics). Many teams evolve here naturally — keep the ceremonies that work, add WIP limits to prevent overload.

---

## Common Questions

**"How do you handle a team that resists Agile ceremonies?"**
Don't force it. Measure the pain first — how long do deployments take, how many bugs escape, how much time is spent in meetings vs coding. Then show the data and propose one change at a time. Start with standups (easiest win). Once the team sees that one ceremony actually helped, they're more open to fixing the others. Change works when people feel the benefit, not when you lecture them about the Scrum Guide.

**"How do you make retros produce real change?"**
Two rules: (1) Every retro produces exactly 2 action items with an owner and a deadline. (2) Next retro starts by reviewing those items. If you didn't complete them, discuss why before raising new issues.

**"Sprint goals — how do you write a good one?"**
One sentence, outcome-oriented. "Users can check out with Apple Pay" not "complete tickets 123-128." A good sprint goal answers: "If we only deliver one thing this sprint, what should it be?"

**"How do you handle Definition of Done in different contexts?"**
Standard DoD for web apps: code reviewed, tests passing, deployed to staging. For safety-critical software: add integration tests, test reports, safety checklists. For regulated environments: add compliance documentation generated in the pipeline. The DoD should match the risk level.
