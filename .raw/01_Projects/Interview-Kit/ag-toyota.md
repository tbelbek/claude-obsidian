---
tags:
  - interview-kit
  - interview-kit/agile
up: [[13-pillar-agile]]
---

*[[00-dashboard|Home]] > [[13-pillar-agile|Agile]] > TOYOTA MATERIAL HANDLING*

# TOYOTA MATERIAL HANDLING — Safety-Critical Agile

At Toyota, I worked in a [[ref-agile-ceremonies#Scrum Roles|cross-functional]] Agile team on T-ONE — developers, testers, and domain experts in the same sprint, building software that controlled autonomous forklifts. Sprint discipline wasn't optional here — a missed test or skipped review could mean a collision on the warehouse floor.

What I owned long-term was the quality bar. I pushed for a strict [[ref-agile-ceremonies#Definition of Done|Definition of Done]] that went beyond the usual — [[ag-quality|integration tests on simulated fleet scenarios using [[ref-texttest#What TextTest Is|TextTest]] framework with BDD-style acceptance tests, test reports archived, safety review checklist signed off]]. When developers wanted to skip the checklist or push it to the next sprint, I pushed back every time. Over time, I [[ag-quality|automated the heavy parts]] — integrated with the Docker Compose test stacks that spun up RabbitMQ, MongoDB, and service containers for isolated testing — and brought the overhead from 2 days to half a day per story.

I also owned estimation quality. [[ag-calibration|Point inflation]] had made [[ref-agile-ceremonies#Sprint Planning|story points]] useless — everything was a 13. I brought in reference stories and made [[ref-agile-ceremonies#Sprint Planning|planning poker]] a real conversation instead of a formality.

The [[ag-resilience|RabbitMQ split-brain incident]] happened here too. It changed how the whole team thought about production readiness — we added failure mode testing to our sprint DoD for any work involving distributed components.

## Key Experiences
- [[ag-quality|QUALITY — safety checklist +2 days per story, automated to half day]]
- [[ag-calibration|CALIBRATION — point inflation, recalibrated with reference stories]]
- [[ag-resilience|RESILIENCE — docs != understanding, deep-dived partition handling, never again]]

## Sorulursa

> [!faq]- "How is Agile different in safety-critical vs regular software?"
> The definition of done is heavier. In a web app, "done" means code reviewed and tests passing. In forklift software, "done" includes safety review, archived test reports, and integration tests against simulated fleet scenarios. You can't skip it. The trade-off is fewer features per sprint, but zero defects escaping to production. In this domain, that trade-off is always worth it.

---

*[[00-dashboard|Home]] > [[13-pillar-agile|Agile]]*
