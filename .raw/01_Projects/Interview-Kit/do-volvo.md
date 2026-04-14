---
tags:
  - interview-kit
  - interview-kit/devops
up: [[11-pillar-devops]]
---

*[[00-dashboard|Home]] > [[11-pillar-devops|DevOps]] > VOLVO CARS*

# VOLVO CARS — DevOps

I was a Software Factory Engineer at Volvo Cars. My job was owning the release pipeline for embedded automotive software — from code push to a tested, gated, [[ref-automotive-compliance#Compliance in Agile|compliance]]-checked release on target hardware.

## Tools I Used Here
| Tool | Ref | Tool | Ref |
|------|-----|------|-----|
| [[ref-gerrit\|Gerrit]] | maintained instance, triggers | [[ref-ansible\|Ansible]] | test orchestration, emulators |
| [[ref-docker\|Docker]] | build containers per target | [[ref-automotive-compliance\|Compliance]] | ISO 26262, automated docs |

This was safety-critical embedded software running on QNX, Linux, and Android Automotive — the kind where a bad release can block an entire vehicle program. I built and maintained the full pipeline: build with Cynosure — Volvo's internal product tracking system with StateDB for product instances and a message bus for build events — [[ref-cicd-security#Scanning Types|static analysis]], unit tests, hardware-in-the-loop testing on actual ECU hardware — test execution was orchestrated with [[ref-ansible#Integration with CI|Ansible playbooks]] — setting up CSP emulators, flashing firmware, running test suites, and collecting results —, [[ref-automotive-compliance#ISO 26262 — Functional Safety|regulatory]] gate checks, and staged rollout. Everything auditable.

What I owned long-term was the [[ref-gerrit#Change-Based Workflow|Gerrit]] infrastructure and the build orchestration. I maintained the [[ref-gerrit#HOW WE USED IT|Gerrit instance]] — project configs, [[ref-gerrit#Access Control|access control]], labels, [[ref-gerrit#Labels & Review|submit rules]] — and wrote the Python trigger daemon using ZUUL CI — with pipelines for check, gate, post-merge, deploy, and periodic-nightly builds — that connected Gerrit events to the build system. I also wrote the [[do-cynosure-parallel|build orchestration layer]] that managed parallel builds across multiple hardware targets, including VBF (Vehicle Boot File) image building for ARM QNX targets. I maintained Ansible playbooks for test execution against CSP emulators, and wrote manifest management scripts that queried the ZUUL REST API and updated module versions automatically.

I coordinated between three departments that didn't naturally talk to each other — regulatory, QA, and test. Wrote technical documentation that met Volvo's strict compliance requirements. Mentored teammates and helped new joiners get up to speed.

Over 18 months, I cut the QA gating cycle by 30% and shipped multiple releases with zero compliance findings.

## Tools Used
| | | |
|---|---|---|
| [[ref-gerrit\|Gerrit]] | [[ref-ansible\|Ansible]] | [[ref-docker\|Docker]] |
| [[ref-automotive-compliance\|ISO 26262]] | [[ref-python\|Python]] | [[ref-cicd-security\|CI/CD Security]] |

## Key Challenges
- [[ref-gerrit#HOW WE USED IT|GERRIT — Triggers — SSH silent drops, heartbeat daemon, dedup -30%]]
- [[do-cynosure-parallel|CYNOSURE — Parallelization — 40dk→15dk, OOM on naive, batched by resource]]
- [[ref-ansible#Integration with CI|ANSIBLE — Test Orchestration — CSP emulator setup, test campaigns, result collection]]

## Sorulursa

> [!faq]- "What was your biggest long-term contribution at Volvo?"
> The trigger system and the build orchestration. Both were things I built from scratch and maintained for the entire time I was there. When I left, the team was still using them daily. The trigger daemon handled thousands of events per week reliably, and the build orchestration cut build times by more than half. Those weren't one-time fixes — they were systems I designed, built, monitored, and improved over 18 months.

> [!faq]- "How did you work across three departments?"
> Regular face-to-face syncs. Regulatory cared about documentation and [[ref-automotive-compliance#Traceability|audit trail]]s. QA cared about test coverage and [[ref-automotive-compliance#Traceability|traceability]]. Test cared about hardware access and test execution. I built the pipeline to serve all three — automated docs for regulatory, coverage reports for QA, rig scheduling for test. Each department got what they needed from the same pipeline run.

---

*[[00-dashboard|Home]] > [[11-pillar-devops|DevOps]]*
