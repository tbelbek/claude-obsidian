---
tags:
  - interview-kit
  - interview-kit/leadership
up: [[ls-kocsistem]]
---

*[[00-dashboard|Home]] > [[12-pillar-leadership|Leadership & Soft Skills]] > [[ls-kocsistem|KOCSISTEM]] > TRANSFORMATION*

# TRANSFORMATION

> [!warning] **Soru:** "How do you drive change?" / "Tell me about a transformation you led"

At KocSistem, the team was doing "push and pray" releases. I learned early that driving change through data and leading by example beats mandating it every time. Weekly at best, sometimes biweekly. Manual deployments, no automated tests gating the release, no rollback plan. When something broke, everyone scrambled.

I didn't walk in and say "we're doing CI/CD now." I started by measuring the pain. Tracked deployment times, failure rates, and how much time the team spent in meetings vs actually coding. Then I showed the data to the team — not as "here's what's wrong" but as "am I reading this right?"

I proposed a pilot: one team, two sprints, daily deployments with automated checks. I volunteered our team. I pair-programmed with the biggest skeptics, fixed flaky tests myself, and was online at 6 AM for the first automated deploys. The pilot team went from weekly to daily in 3 weeks. Other teams saw it working and asked for the same setup. Six months later, the whole organization had shifted.

I bring this up under leadership because driving organizational change is a leadership problem, not a technical one — the tools were the easy part, getting people to trust them was the real work.

## Sorulursa

> [!faq]- "Why did you volunteer your own team?"
> Because nobody believes in a change you're not willing to make yourself. If I'd asked another team to be the guinea pig, the pushback would've been 10x. By going first, I showed it was safe and I was putting my own reputation on the line.

> [!faq]- "What did the skeptics say?"
> The main objection was "we'll break production more often." I showed data that most production incidents were caused by big, risky releases — not frequent small ones. Smaller changes are easier to test, easier to review, and easier to roll back. After they saw the first two weeks of daily deploys with zero incidents, they got it.

> [!faq]- "What was the hardest part?"
> The cultural shift. Some developers had been deploying the same way for years. Automation felt like a threat — "is this replacing me?" I had to show them it was freeing them from boring work, not replacing them. Once they stopped spending Friday afternoons on manual deployments, they came around.

> [!faq]- "What does the research say about organizational change?"
> [[ref-agile-leadership#Change Management|Kotter's model]] (8-step model for change) is the classic framework: create urgency, build a coalition, form a vision, communicate, empower action, create quick wins, build on change, anchor in culture. I didn't follow it formally, but looking back, I did most of these steps naturally. The "pilot with quick wins" approach maps directly to Kotter's model. The key insight from the research: change fails when you skip the urgency step. If people don't feel the pain, they don't see the need for change. That's why I started by measuring and showing the data.

> [!faq]- "How do you sustain change after the initial excitement?"
> Two things: metrics and ownership. Once the pilot worked, I set up dashboards showing deployment frequency and failure rate. The team could see their own progress. And I made sure people owned parts of the pipeline — this person owns the build template, that person owns the deployment scripts. When people own something, they maintain it. When "the DevOps guy" owns everything, it falls apart when that person leaves.

## Also relevant to

- [[do-azdevops-zero]] — The technical side of the same transformation: Azure DevOps pipelines, Terraform, DORA metrics
- [[11-pillar-devops|DevOps Pillar]] — CI/CD from zero implementation details

---

*[[00-dashboard|Home]] > [[12-pillar-leadership|Leadership & Soft Skills]] > [[ls-kocsistem|KOCSISTEM]]*
