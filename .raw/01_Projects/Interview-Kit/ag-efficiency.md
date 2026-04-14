---
tags:
  - interview-kit
  - interview-kit/agile
up: [[ag-kocsistem]]
---

*[[00-dashboard|Home]] > [[13-pillar-agile|Agile]] > [[ag-kocsistem|KOCSISTEM]] > EFFICIENCY*

# EFFICIENCY

> [!warning] **Soru:** "How do you run effective sprints?"

At KocSistem, [[ref-agile-ceremonies#Daily Standup|standups]] were 25 people in a room, each giving a status update nobody listened to. 30 minutes every morning. Retros were skipped or turned into complaint sessions — people vented, felt better, nothing changed. The point of ceremonies is outcomes, not compliance — and we were getting neither. Sprint planning was guesswork — teams committed to work without understanding scope, then either cut corners or carried over half the sprint.

I fixed standups first. Broke them into team-level meetings — 5-6 people, focused on blockers, not status updates. If your update is "I'm still working on the same thing," you don't need to say it. 30 minutes became 8.

For retros, I added a simple rule: every retro produces exactly 2 action items, each with an owner and a deadline. Next retro starts by reviewing those items. If we didn't complete them, we talk about why before raising new issues. It took three sprints, but once people saw that problems actually got fixed, they started taking retros seriously.

For planning, I introduced planning poker. Not because story points are precise — they're not. But the conversation during estimation is valuable. "Why do you think this is an 8 when I said 3?" often reveals that one person knows about a dependency or risk that nobody else is aware of.

I bring this up under Agile because ceremonies exist to produce outcomes — if they're not helping the team make decisions and remove blockers, they're just overhead.

## Sorulursa

> [!faq]- "How did the team react to smaller standups?"
> Some people felt left out — they liked knowing what everyone was doing. I set up a shared Slack channel where teams posted a one-line daily update. People who wanted the big picture could read it there. The standup meeting was for blockers only.

> [!faq]- "What if teams can't fill 2 action items from a retro?"
> Then the sprint went well and we do a shorter retro. But in my experience, there are always at least 2 things worth improving. Sometimes they're small — "let's update the readme" or "let's add a test for that edge case." Small improvements add up.

> [!faq]- "What does the Scrum Guide say about standups?"
> The Scrum Guide says the Daily Scrum should be 15 minutes max and is for the developers, not for reporting to management. It's about synchronization and planning for the next 24 hours. Most teams turn it into a status meeting because that's what they're used to. Jeff Sutherland (co-creator of Scrum) says in his book "Scrum: The Art of Doing Twice the Work in Half the Time" that the daily should answer one question: "what's in the way?" Everything else can be async.

> [!faq]- "How do you handle remote standups?"
> Same rules — blockers only, keep it short. We used a simple Slack bot: each person posts their blocker (or "no blockers") before 9:30. If there's something to discuss, we do a 10-minute call. If not, we skip the call. Remote standups tend to be faster because there's less social chat, but you lose some spontaneous problem-solving. We compensated with a weekly informal coffee chat.

---

*[[00-dashboard|Home]] > [[13-pillar-agile|Agile]] > [[ag-kocsistem|KOCSISTEM]]*
