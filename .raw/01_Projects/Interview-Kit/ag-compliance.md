---
tags:
  - interview-kit
  - interview-kit/agile
up: [[ag-volvo]]
---

*[[00-dashboard|Home]] > [[13-pillar-agile|Agile]] > [[ag-volvo|VOLVO CARS]] > COMPLIANCE*

# COMPLIANCE

> [!warning] **Soru:** "How do you do Agile in regulated environments?"

At Volvo, the [[ref-automotive-compliance#Compliance in Agile|compliance]] regulatory team wanted full documentation before any release — test reports, traceability matrices, change logs. The development team wanted to ship frequently. These two goals seemed like they couldn't both work at the same time. But regulations and agility can work together if you automate the paperwork.

The key insight was that the regulatory team didn't care how the documentation was produced — they cared that it was accurate and complete. So I automated it. Every release pipeline generated the compliance artifacts as part of the build: test reports pulled from test results, traceability matrices generated from commit history and ticket links, change logs assembled from merge messages.

The dev team could ship as often as the pipeline allowed. The regulatory team got consistent, machine-generated documentation that was more accurate than the manually-written Word documents they were used to. Both sides were happy.

This sits in my Agile experience because the biggest blocker to Agile in regulated environments is the assumption that compliance requires manual work — once you automate it, the constraint disappears.

## Sorulursa

> [!faq]- "How did you generate traceability matrices?"
> Each commit message included a ticket reference. The pipeline script parsed the commit log since the last release, extracted ticket IDs, queried the bug tracker for details, and assembled a matrix: requirement → ticket → commit → test result. All automated, generated fresh for every release.

> [!faq]- "Did the regulatory team trust automated documentation?"
> Not at first. I ran both in parallel for two releases — manual docs and automated docs. When the regulatory team compared them and found the automated ones were more complete (they didn't miss anything like humans sometimes do), they switched. Consistency won them over.

> [!faq]- "What automotive standards apply here?"
> ISO 26262 is the functional safety standard for automotive — it defines safety integrity levels (ASIL A through D) and requires documentation at each development phase. ASPICE (Automotive SPICE) is the process assessment model. At Volvo, we had to meet both. The key requirement is traceability: you must trace from requirements → design → implementation → test → verification. Automating this traceability in the pipeline meant we could prove compliance at any time, not just at audit time.

> [!faq]- "How did you convince the regulatory team to trust automation?"
> I ran both approaches in parallel for two releases. The regulatory team compared manual and automated documentation side by side. The automated docs were more complete (they caught everything, humans sometimes miss items) and more consistent (same format every time). Once they saw the quality was equal or better, they agreed to switch. Trust was built through evidence, not arguments.

## Also relevant to

- [[do-volvo]] — The pipeline where compliance automation was built
- [[11-pillar-devops|DevOps Pillar]] — Gerrit triggers, Cynosure builds, regulatory gating in the pipeline

---

*[[00-dashboard|Home]] > [[13-pillar-agile|Agile]] > [[ag-volvo|VOLVO CARS]]*
