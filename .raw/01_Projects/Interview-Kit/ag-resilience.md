---
tags:
  - interview-kit
  - interview-kit/agile
up: [[ag-toyota]]
---

*[[00-dashboard|Home]] > [[13-pillar-agile|Agile]] > [[ag-toyota|TOYOTA MATERIAL HANDLING]] > RESILIENCE*

# RESILIENCE

> [!warning] **Soru:** "Tell me about learning from failure"

At Toyota, the RabbitMQ split-brain incident was a wake-up call for the whole team, not just me. The real learning came after the incident, not during it. We had a production incident that we could've prevented if we'd tested for network partitions. We didn't, because we assumed the clustering docs covered everything we needed to know.

After the incident, we didn't just fix the immediate problem. We changed how the team thought about production readiness. We added chaos testing to our sprint DoD for any work involving distributed components. We started asking "how does this break?" in code reviews, not just "does this work?" We wrote a post-mortem that the whole team reviewed, and added "failure mode testing" as a standard practice.

The lesson I took from it: reading docs tells you how things work. You need to test how they break. That mindset stuck with the whole team.

I bring this up under Agile because how a team handles failure defines its culture — blameless learning vs finger-pointing determines whether people report problems early or hide them.

## Sorulursa

> [!faq]- "How did the team react to the incident?"
> Some people were scared — they didn't want to touch RabbitMQ config again. I turned it into a learning opportunity: we ran a workshop where we intentionally caused failures in a test environment and practiced recovering. By the end of the session, people felt more confident, not less. Familiarity with failure modes reduces fear.

> [!faq]- "How do you prevent the same kind of mistake in new projects?"
> I always ask: "What are the failure modes of this system?" before going to production. If the team can't answer that question, we're not ready. It's become a standard checklist item for any production launch I'm involved in.

> [!faq]- "What's the concept of a blameless post-mortem?"
> The term comes from John Allspaw's work at Etsy, later formalized in the Google SRE book. The idea: after an incident, you analyze what happened and what to change — without blaming individuals. Humans make mistakes; systems should prevent those mistakes from causing outages. At Toyota, after the RabbitMQ incident, I ran a [[ref-agile-leadership#Blameless Post-Mortems|blameless post-mortem]] focused on "what did we not know?" and "what should we change?" not "who screwed up?" This built [[ref-agile-leadership#Psychological Safety|psychological safety]] — people were more willing to report problems early because they knew they wouldn't get blamed.

> [!faq]- "How does this relate to psychological safety?"
> Amy Edmondson's research at Harvard shows that teams with high psychological safety learn faster and perform better. If people are afraid of blame, they hide mistakes. If they feel safe, they report problems early — when they're still small. The blameless post-mortem is one tool for building that safety. Another is celebrating "good catches" — when someone finds a bug before it reaches production, that's worth acknowledging.

## Also relevant to

- [[sd-rabbitmq-splitbrain]] — Same incident told from the Software Dev/technical perspective: RabbitMQ clustering, partition handling, chaos testing
- [[10-pillar-software-dev|Software Dev Pillar]] — Distributed systems and messaging at Toyota

---

*[[00-dashboard|Home]] > [[13-pillar-agile|Agile]] > [[ag-toyota|TOYOTA MATERIAL HANDLING]]*
