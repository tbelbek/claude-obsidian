---
tags:
  - interview-kit
  - interview-kit/leadership
up: [[12-pillar-leadership]]
---

*[[00-dashboard|Home]] > [[12-pillar-leadership|Leadership & Soft Skills]] > VOLVO CARS*

# VOLVO CARS — Solo Ownership Across Departments

At Volvo, I was the only person responsible for the entire teams-to-car release pipeline. There was no DevOps team, no platform team — just me. I built and maintained everything from the moment a developer pushed code to the moment software landed on vehicle hardware.

That meant I was the single point of contact between multiple departments that didn't naturally talk to each other. Development teams writing software, QA running test campaigns, the test department managing hardware-in-the-loop rigs, and the [[ref-automotive-compliance#ISO 26262 — Functional Safety|regulatory]] team checking [[ref-automotive-compliance#Compliance in Agile|compliance]] documentation. Each group had different priorities — developers wanted fast feedback, QA wanted coverage, test wanted rig availability, regulatory wanted [[ref-automotive-compliance#Traceability|audit trail]]s. I had to understand all of them and build a pipeline that served everyone without anyone waiting on anyone else.

When something broke in the pipeline, there was no one to escalate to. I debugged it, fixed it, and got things moving again. When departments disagreed on process, I was the one who found the middle ground. When a new joiner needed to understand the release flow, I was the one who explained it and mentored them through their first release.

The [[ls-composure|production line crisis]] — driving to the facility at night to fix a race condition — was one night. The real leadership at Volvo was owning the entire delivery chain solo for 18 months, keeping 3+ departments aligned, and making sure every release met automotive compliance standards. Cut the QA cycle by 30%, zero compliance findings across all releases.

## Key Experiences
- [[ls-composure|COMPOSURE — race condition at night, drove to facility, line never stopped]]

## Sorulursa

> [!faq]- "How did you handle being the single point of failure?"
> I documented everything — the pipeline architecture, the [[ref-gerrit#Change-Based Workflow|Gerrit]] config, the trigger daemon, the build orchestration. I wrote runbooks for common issues. I mentored teammates on the basics so they could handle simple pipeline problems when I was on vacation. The goal was to reduce the bus factor from 1 to at least 2-3 people who understood the system, even if I was the primary owner.

> [!faq]- "How did you debug pipeline issues when you were the only person?"
> Systematic approach. First: check the ZUUL build log — which stage failed and what was the error message. Most issues fell into a few categories: (1) Gerrit trigger didn't fire — check the daemon heartbeat log, reconnect if needed, re-queue missed changes. (2) Build failed on a specific target — check the Cynosure output for that target, usually a missing dependency or toolchain version mismatch. (3) HIL test rig unavailable — check rig status, restart if needed, re-queue the test. (4) Regulatory gate failed — check which criterion wasn't met, usually a missing test report or coverage below threshold. I had runbooks for each category. When something genuinely new happened, I'd investigate, fix it, document the fix, and add it to the runbook. Over 18 months, the runbook covered 95% of issues.

> [!faq]- "How did you manage priorities across departments?"
> Regular face-to-face syncs with each group. Short — 15 minutes, once a week. I'd ask "what's blocking you from the pipeline side?" and work through the list. When two departments had conflicting needs (e.g., regulatory wanted slower releases for review, dev wanted faster releases for feedback), I found technical solutions — like automated compliance docs that gave regulatory what they needed without slowing down dev.

---

*[[00-dashboard|Home]] > [[12-pillar-leadership|Leadership & Soft Skills]]*
