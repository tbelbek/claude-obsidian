---
tags:
  - interview-kit
  - interview-kit/leadership
up: [[ls-volvo]]
---

*[[00-dashboard|Home]] > [[12-pillar-leadership|Leadership & Soft Skills]] > [[ls-volvo|VOLVO CARS]] > COMPOSURE*

# COMPOSURE

> [!warning] **Soru:** "Tell me about delivering under pressure"

At Volvo, a bug made it through testing — on-and-off failures in embedded software. Got called late — they were thinking about stopping the production line. In automotive, that costs a ton of money per hour.

Staying calm and systematic when the stakes are highest was the only option. I had a choice: try to debug remotely or drive to the facility. I chose to go — embedded hardware issues need physical access. Brought one other engineer. We spent the first hour just trying to reproduce the issue reliably. It only happened under specific startup timing conditions that our test environment didn't create.

Once we could reproduce it, we found the root cause quickly — a race condition in the initialization sequence. Two components were starting in parallel and occasionally stepped on each other. Wrote a patch that made the startup deterministic — component A finishes before component B starts. Tested it on a spare unit first, then rolled it out to production units one by one while monitoring each one.

The production line never stopped. The patch held until the proper fix at the next maintenance window. After that, I pushed hard for making our test environments match production timing more closely so we wouldn't get surprised like this again.

I bring this up under leadership because high-pressure moments reveal whether you can stay systematic or whether you panic — and the team watches how you handle it.

## Sorulursa

> [!faq]- "Why did you choose to drive there instead of debugging remotely?"
> Because embedded systems are physical. The bug only showed up under specific hardware timing conditions. Remote debugging would've been guessing — I needed to see the actual hardware, connect a debugger, and reproduce the exact conditions. The drive was worth it.

> [!faq]- "How did you test the patch safely?"
> We had a spare unit that wasn't in the production line. Flashed the patch there first, ran it for 30 minutes under the same conditions that triggered the bug. When it was stable, we rolled it out to production units one at a time — not all at once. If any unit showed issues, we could revert just that one.

> [!faq]- "What did you change about the test environment afterward?"
> The test environment had all components starting sequentially with fixed delays. Production had them starting in parallel based on hardware readiness signals, which introduced variable timing. I pushed for a test configuration that matched production startup behavior — parallel starts with realistic timing variation. This would have caught the race condition before it reached production.

> [!faq]- "How do you stay calm in high-pressure situations?"
> Practice and preparation. If you've dealt with incidents before and you have a mental framework, the pressure doesn't paralyze you. My framework: (1) reproduce the problem, (2) isolate the root cause, (3) test the fix safely before applying to production, (4) monitor after deployment. The Google SRE book calls this "managing incidents" — having a structured approach means you don't waste time panicking. The most important thing is not to rush the fix into production without testing — that usually makes things worse.

> [!faq]- "What's your incident response process?"
> Declare the incident, assign roles (incident commander, communicator, debugger), set up a communication channel, work the problem systematically. After resolution: write a [[ref-agile-leadership#Blameless Post-Mortems|blameless post-mortem]], identify action items, follow up. The key word is "blameless" — the goal is to learn, not to punish. The Etsy engineering team popularized this approach, and Google's SRE book formalized it. At Volvo, we didn't have formal incident management, but I followed these principles informally — especially the "test before deploying the fix" part, which saved us that night.

## Also relevant to

- [[11-pillar-devops|DevOps Pillar]] — The embedded release pipeline context that led to this incident
- [[do-volvo]] — Volvo DevOps setup: Gerrit, Cynosure, HIL testing

---

*[[00-dashboard|Home]] > [[12-pillar-leadership|Leadership & Soft Skills]] > [[ls-volvo|VOLVO CARS]]*
