---
tags:
  - interview-kit
  - interview-kit/agile
up: [[ag-toyota]]
---

*[[00-dashboard|Home]] > [[13-pillar-agile|Agile]] > [[ag-toyota|TOYOTA MATERIAL HANDLING]] > QUALITY*

# QUALITY

> [!warning] **Soru:** "How do you handle quality in Agile?" / "Definition of Done?"

At Toyota, we were building software that controlled autonomous forklifts. A bug in a web app means a bad user experience. A bug in forklift software means a potential collision. When software controls physical machines, quality standards can't be negotiated. Sprint discipline wasn't optional.

Our definition of done went beyond the usual "code reviewed, tests passing." We added: integration tests against simulated fleet scenarios passed, test report generated and archived, documentation updated, and a safety review checklist signed off.

This made sprints feel slow at first. Developers would "finish" a story in 3 days, but the safety checklist and test report took another 2 days. The temptation was to push those steps to the next sprint — "it's done, we just need sign-off." I pushed back on this every time. A story isn't done until it meets the full definition of done. If the DoD is too expensive, we either automate parts of it or reduce sprint scope. We don't pretend it doesn't exist.

Over time, we automated the test report generation and parts of the safety checklist. The overhead went from 2 days to about half a day per story.

I bring this up under Agile because Definition of Done is where Agile meets reality — in safety-critical software, you can't negotiate on quality, you can only automate to make it sustainable.

## Sorulursa

> [!faq]- "How did you automate the safety checklist?"
> Not all of it — some parts required human judgment. But the mechanical parts (test coverage above threshold, no open critical bugs, all required test scenarios executed) were automated as pipeline checks. The remaining items were a short form that took 30 minutes instead of a full day.

> [!faq]- "How did the team feel about the strict DoD?"
> Frustrated at first — they felt it slowed them down. But after a few sprints without any defects escaping to production, they understood. When you work on safety-critical software, cutting corners on quality isn't an option. Better to ship fewer features cleanly than ship more features with risk.

> [!faq]- "What's the theory behind strict Definition of Done?"
> The Scrum Guide says the Definition of Done creates transparency — everyone knows what "done" means. In safety-critical domains, IEC 61508 (functional safety standard) and ISO 26262 (automotive safety) require documented verification at each stage. Our DoD was basically the intersection of Scrum's "done" and the safety standard's verification requirements. The challenge is keeping the DoD achievable within a sprint — if it's too heavy, nothing gets "done" and the team loses motivation.

> [!faq]- "How do you balance safety requirements with sprint velocity?"
> Automate everything you can. Manual safety checks are expensive but necessary — so minimize them by automating the mechanical parts (test execution, report generation, coverage checks). What's left should be human judgment calls (design review, risk assessment). At Toyota, we got the manual overhead from 2 days to half a day by automating test reports and coverage checks. The remaining half day was genuinely valuable human review.

---

*[[00-dashboard|Home]] > [[13-pillar-agile|Agile]] > [[ag-toyota|TOYOTA MATERIAL HANDLING]]*
