---
tags:
  - interview-kit
  - interview-kit/pillar
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Pillar: Agile

> [!info] Registered [[ref-agile-ceremonies#Scrum Roles|Scrum Master]]. Agile maturity 3.1→3.7. Safety-critical sprints on forklift software. Compliance and agility working together in automotive. Stepped in as PO and tech lead when needed.

## Quick Scan

| | | | |
|---|---|---|---|
| **[[ag-kocsistem\|KOCSISTEM]]** <br> [[ag-efficiency\|EFFICIENCY — Ceremony Reform]] · 30dk→8dk, retros with owners <br> [[ag-alignment\|ALIGNMENT — Sprint Scope]] · sprint goals, live demos built trust <br> [[ag-discipline\|DISCIPLINE — Standup Fix]] · small teams, blockers only <br> [[ag-accountability\|ACCOUNTABILITY — Retro Follow-Through]] · owner + deadline per item <br> [[ag-ambition\|AMBITION — Sprint Padding]] · challenged team to stretch <br> [[ag-outcomes\|OUTCOMES — Meeting Audit]] · "what decision?" fix or cancel <br> [[ref-agile-ceremonies#Scrum Roles\|Scrum Master]] · [[ref-agile-leadership#Servant Leadership\|Servant]] <br> [[ref-agile-leadership#Data-Driven Decision Making\|Data-Driven]] · [[ref-code-review#HOW WE SET IT UP\|Code Review]] <br> *Maturity 3.1→3.7, velocity ±10%* | **[[ag-toyota\|TOYOTA]]** <br> [[ag-quality\|QUALITY — Safety-Critical DoD]] · checklist +2 days, automated to half day <br> [[ag-calibration\|CALIBRATION — Estimation Fix]] · point inflation, reference stories <br> [[ag-resilience\|RESILIENCE — Learning from Failure]] · docs ≠ understanding <br> [[ref-testing-strategy#E2E Test Patterns\|E2E Testing]] · [[ref-texttest#What TextTest Is\|TextTest]] <br> *Automated DoD overhead* | **[[ag-volvo\|VOLVO CARS]]** <br> [[ag-compliance\|COMPLIANCE — Regulated Agile]] · automated in pipeline <br> [[do-cynosure-parallel\|CYNOSURE — Parallelization]] · 40dk→15dk, batched <br> [[ref-automotive-compliance#ISO 26262 — Functional Safety\|ISO 26262]] · [[ref-automotive-compliance#ASPICE — Automotive SPICE\|ASPICE]] <br> *Regulatory + dev both won* | **[[ag-combination\|COMBINATION AB]]** <br> [[ag-adaptability\|OWNERSHIP — Quarter Planning]] · stepped in lead+PO, completed early <br> [[sd-graphql-migration\|GRAPHQL — Migration]] · REST→GraphQL, zero breaking changes <br> *All tasks before quarter end* |

My approach to Agile is practical, not dogmatic. I care about outcomes — does the team ship working software predictably, do stakeholders have visibility, does the process help or hinder? The certification is a tool for credibility when pushing for change — not an identity. What matters is whether the team is improving. I apply [[ref-agile-leadership#Servant Leadership|servant leadership]] — removing blockers, not giving orders — and use [[ref-agile-leadership#Data-Driven Decision Making|data to settle debates]] instead of opinions.

I've applied Agile in three very different contexts. At **KocSistem**, the team was doing Agile in name only — [[ag-efficiency|standups were 30-minute status reports]], [[ag-accountability|retros produced complaints but no change]], and product owners [[ag-alignment|changed priorities mid-sprint]]. I fixed every ceremony to produce actual outcomes: standups down to 8 minutes, retros with [[ag-accountability|2 action items per session]] (owner + deadline, reviewed next retro), [[ag-alignment|sprint goals]] to protect scope, and live demos to give stakeholders visibility. I [[ag-ambition|challenged the team to stretch]] instead of padding sprints, and [[ag-outcomes|killed meetings that didn't produce decisions]]. Agile maturity went from **3.1 to 3.7**. Sprint [[ref-agile-ceremonies#Sprint Planning|velocity]] became predictable within 10% variance.

At **Toyota**, Agile wasn't optional — it was safety-critical. The T-ONE team built software that controls autonomous forklifts. A missed test or skipped review could mean a collision. I pushed for a strict [[ag-quality|Definition of Done]] with safety checklist sign-off, automated [[ref-testing-strategy#E2E Test Patterns|test reports]], and integration tests on simulated fleet scenarios using [[ref-texttest#What TextTest Is|TextTest]]. Developers resisted the overhead (2 extra days per story), but I automated the mechanical parts — [[ag-quality|overhead dropped from 2 days to half a day]]. I also [[ag-calibration|fixed estimation]] — everything was a 13, so I brought in reference stories. The [[ag-resilience|RabbitMQ split-brain incident]] changed how the whole team thought about failure testing.

At **Volvo**, the challenge was making [[ag-compliance|compliance and agility work together]]. Automotive embedded has [[ref-automotive-compliance#ISO 26262 — Functional Safety|documentation requirements]] (ISO 26262, ASPICE) that don't fit naturally into 2-week sprints. I automated documentation generation in the pipeline — test reports, traceability matrices, change logs — so the regulatory team got better docs than their manual process, and the dev team shipped as often as the pipeline allowed.

At **Combination**, I [[ag-adaptability|stepped in for both the tech lead and PO]] when they were unavailable during quarter planning. Ran the planning, set priorities, kept the team aligned. We completed all planned tasks before the quarter ended — a first.

I'm a **Registered [[ref-agile-ceremonies#Scrum Roles|Scrum Master]]**. The real value isn't the certification — it's the framework for hard conversations. "Scrum says we protect sprint scope" is stronger than "I'd prefer not to."

---

### [[ag-combination|COMBINATION AB]] — [[ag-adaptability|Stepped in as PO + tech lead]]. Quarter planning, all tasks completed early.

### [[ag-toyota|TOYOTA MATERIAL HANDLING]] — [[ag-quality|Safety-critical DoD]], [[ag-calibration|estimation fix]], [[ag-resilience|learning from failure]].

### [[ag-volvo|VOLVO CARS]] — [[ag-compliance|Compliance automated in pipeline]]. Regulatory + dev both won.

### [[ag-kocsistem|KOCSISTEM]] — [[ag-efficiency|Ceremonies reformed]] (standups 30→8min), [[ag-alignment|sprint goals]], [[ag-accountability|retro accountability]], [[ag-discipline|standup fix]], [[ag-ambition|sprint padding challenged]], [[ag-outcomes|meetings audited]]. I also [[ref-code-review#HOW WE SET IT UP|established code review culture]] as part of the Agile transformation. Maturity **3.1→3.7**.

---

**Related:** [[10-pillar-software-dev]] | [[11-pillar-devops]] | [[12-pillar-leadership]]

*[[00-dashboard]]*
