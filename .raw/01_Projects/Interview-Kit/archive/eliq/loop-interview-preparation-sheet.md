---
tags:
  - interview-kit
  - interview-kit/eliq
up: "[[Loop interview schema and schedule]]"
---

# Loop Interview — Full Preparation Guide

> **Location:** Stora Badhusgatan 18-20
> **Format:** 3 x 45-min back-to-back, behavioral + technical
> **Method:** STAR — 1-2 examples per principle, go deep into the how and why
> **Panel:** Olof (CTO), Doug (Head of Embedded Energy), Vilius (Senior Engineering Manager)
> **Key:** They are a fact-driven team. Specificity is everything. Numbers, tradeoffs, alternatives considered, lessons learned.

---

## Delivery Rules

- **"I" not "we"** — "the team did X, **I** did Y specifically"
- **Numbers always** — 30%, 55%, 60%, 7x, 25 engineers, 3.1 to 3.7, 800 to 80MB
- **Don't volunteer detail** — give the STAR, let them pull the thread
- **Honest on gaps** — "haven't used X, but understand the model — here's what's similar in my experience"
- **STAR discipline** — never skip the Result, always quantify the outcome
- **3-4 min per story** — leaves room for follow-ups and 3-4 stories per 45-min session
- **Don't reuse stories** — if two interviewers ask about the same principle, use a different example

---

## Story Index — Quick Scan

| Principle | Story | D (Situation) | R (Task) | I (Action) | V (Result) | E (Lesson) |
|-----------|-------|---------------|----------|------------|------------|------------|
| **1 — Customer & Ownership** | GPS Warehouse — KocSistem | Live view and history were strangling each other through the same pipe | Reads and writes fighting for the same rows — two concerns tangled into one path | Fast store for live, database for history — split them apart; Hot backup with automatic failover — no human needed; Reject bad data loudly at entry | Frozen → sub-second, 50→500+ trucks, IDC Award | One codebase, four clients — rules in config, not code |
| **1 — Customer & Ownership** | Leading Without Authority — KocSistem | Weekly big-batch releases causing SLA breaches — no mandate, no budget | Show the pain as data, not a complaint — "am I reading this right?"; Low-risk pilot: one team, two sprints | Nobody believes in a change you're not willing to try yourself — volunteer first; Day 2 something broke — caught in 3 min, rolled back in 5 | Weekly → daily deploys in 3 weeks, SLA -60% | Mandated changes get compliance, not ownership — pilot gets conviction |
| **1 — Customer & Ownership** | Stepping In as PO — Combination AB | PO left mid-quarter, no one driving priorities — leadership vacuum | Said it explicitly: "I'm not the PO, but someone needs to drive this"; Asked: "If we can only do 3 things, what are they?" | Shared the plan before the quarter started — early sign-off reduced misalignment risk | All planned tasks completed, first time ever | Imperfect action beats no action — a documented starting point beats a blank page |
| **1 — Customer & Ownership** | Third-Party Turnaround — Toyota | He wasn't difficult — he'd been burned by previous partners | Root cause was relational, not technical — stop emailing, go in person | Start with read-only access: no risk to him, trust starts building; Advance notice before every change, credit his team publicly | Dynamic reversed, referred another division | Full trust in 6 weeks — tone is invisible over text |
| **2 — Dive Deep** | RabbitMQ Split-Brain — Toyota | Default behavior was "keep going" — both sides diverged, messages vanished; Test environment had no real network — we never saw partition behavior | Trust the trace, not the health check — cluster said "healthy" while messages were dropping | Pause, don't guess — frozen forklift is safe, dropped command is not; Don't confirm until it's safe — majority of nodes must write first | Zero silent message loss, failure testing in every build | Break it on purpose, in the pipeline — failure tests caught 2 more edge cases in the first month |
| **2 — Dive Deep** | GraphQL Migration — Combination AB | Each service is an expert, the gateway is the coordinator — 5-6 requests per page, each service called independently | Don't make a hundred phone calls when one will do — batch lookups, not one per item | Lock the menu, not just the food — pre-register valid queries; Deprecate, don't delete — let consumers migrate at their pace; Pair with the biggest skeptic first | 5-6 requests per page → 1, zero breaking changes, 6 months | Move caching closer to the data — single endpoint breaks HTTP caching |
| **2 — Dive Deep** | Terraform State Corruption — KocSistem | Two pipelines wrote simultaneously — tracking file and reality diverged | Reconciled by hand: re-register what exists, remove what doesn't — took a full day | A checkout system for the tracking file — one writer at a time, always; Split the tracking file per environment | Never happened again, policy for every new project | The tracking file contains sensitive data — treat it like a secret, not a config |
| **2 — Dive Deep** | Build Parallelization — Volvo Cars | Ran everything in parallel on day 1 — server ran out of memory and crashed | The bottleneck was linking, not compiling — can't distribute, only schedule smarter; Know your heavyweights before you schedule | Measured peak memory per target, designed execution order around that; Each target in its own isolated environment — incompatible compilers can't conflict | 40 → 15 min, QA cycle -30%, zero compliance failures | Skip what hasn't changed — no point rebuilding an untouched module |
| **3 — Invent & Simplify** | Docker Optimization — Combination AB | Images included the full compiler — no purpose in production, pure bloat; Registry tripled in 3 months | Don't ship the factory with the product — separate build environment from runtime | Put slow stuff first, fast stuff last — dependencies before code, cache does the rest; One shared template for 60+ services — single fix benefits everyone | 800 → 80MB, 10 → 2 min build time | Dependencies rarely change, code changes every commit — ordering unlocks caching |
| **3 — Invent & Simplify** | Ceremony Reform — KocSistem | 25 people in a standup — nobody was listening to anyone | Standups are for blockers, retros are for decisions — not reporting, not venting | Groups of 5-6, blockers only; Exactly 2 retro action items, each with a named owner and deadline; Next retro starts by reviewing last retro | 30 min standup → 8 min, retros produced real changes | Took 3 sprints to stick — by then, people saw problems actually getting fixed |
| **3 — Invent & Simplify** | Monitoring POC — KocSistem | Nobody asked me to — I learned the tools on my own time and built the POC | Three signals cover 80% of problems: request volume, error rate, response time | Showed it to my lead: "Here's what our services look like right now"; Made it routine — mentioned the dashboard every standup | Hours → minutes to detect, led to promotion to Dev Lead | Filling gaps nobody assigned is how you move from IC to leadership |
| **3 — Invent & Simplify** | Meeting Audit — KocSistem | Meetings producing no decisions — everyone attending, nothing changing | One test: what decision did this meeting produce? None → cancel or fix it | Cancelled a weekly sync — nobody missed it; Reviews became live demos — stakeholders could click and give feedback | Fewer meetings, every surviving one produced a decision | When people saw their feedback in the product, they started attending |
| **4 — Standards & Delivery** | CI/CD From Zero — KocSistem | Weekly manual deployments — copying to servers and hoping; No pipelines, no metrics | Four numbers tell you if delivery is improving: frequency, speed, failure rate, recovery time; Start with the most painful app, prove it works, expand | Shared pipeline building blocks — add security scanning once, it applies everywhere; Same artifact promotes through environments; Infrastructure as code | 7x deploy frequency, zero downtime cloud migration, zero pen-test findings 3 quarters | Frequency alone is gameable — pair it with failure rate so gaming has a cost |
| **4 — Standards & Delivery** | Safety-Critical DoD — Toyota | "Story isn't done until DoD is met" — pushed back every time, no exceptions; Overhead was 2 full days per story | Automate the mechanical, keep the human judgment — don't confuse strict with manual | Test execution, report generation, coverage checks — all automated; Design review, risk assessment — kept manual because they need judgment | Overhead 2 days → half a day, zero safety incidents | Zero defects escaping made the overhead feel justified, not arbitrary |
| **4 — Standards & Delivery** | Automated Compliance — Volvo Cars | Regulatory teams don't care how docs are produced — only that they're accurate and complete | Pipeline reconstructed the chain: requirement → code change → test — automatically | Machine-generated docs were more complete than manual ones; Ran both in parallel for two releases — side-by-side comparison was the proof | Zero compliance findings, 18 months | Automated traceability depends on clean inputs — pipeline rejects commits without ticket links |
| **4 — Standards & Delivery** | First-Year Roadmap — KocSistem | "Implement DevSecOps metrics" is abstract — "find the bottleneck from commit to production" is real | Every goal tied to pain the team already felt — not "leadership wants a number" | 3-4 objectives, 2-3 measurable key results each — tracked monthly, adjusted quarterly; Security scanning in every build | Agile 3.1→3.7, deploys 2x, zero pen-test findings | Agile maturity tracked as a team conversation, not a management metric |
| **5 — Earn Trust** | RabbitMQ — What I Got Wrong — Toyota | We'd read the docs and thought we understood — we didn't; Test environment had no real network — we never saw how it actually breaks | Reading docs is not understanding — understanding comes from testing failure | Added "what are the failure modes?" as a required question before any prod deployment; Ran a workshop: deliberately caused failures and practiced recovering | Chaos testing standard, team started reporting problems earlier | Blameless post-mortem: "what didn't we know?" not "who screwed up?" |
| **5 — Earn Trust** | Deployment Freeze Conflict — KocSistem | He was right to worry — his concern came from a real Friday outage | Didn't overrule him — pulling rank wins the argument, loses the trust; Proposed 6 weeks of data: "let's let the evidence decide" | Data showed the problem was what was in releases, not when they went out; Shared the data with him first, privately | He became the strongest daily deployment advocate | Built the pre-deployment checklist together — shared ownership meant real compliance |
| **5 — Earn Trust** | Production Line Emergency — Volvo Cars | Production line stopped — embedded bug, physical hardware | Drive there — embedded bugs need physical access, remote debugging would have been guessing; First hour: reproduce reliably before touching anything | Two components initializing in parallel, stepping on each other — made startup deterministic; Test on a spare unit first, then roll out one unit at a time | Production line never stopped | After the fix: change the test environment so the same surprise can't happen again |
| **5 — Earn Trust** | Not Delegating Well — KocSistem | IC habits that got me promoted were making me a bottleneck as a lead; A team member told me directly: "you're doing things I should be doing" | Speed on a single task doesn't matter if it creates a dependency on you | Moved from "I'll decide" to "what do you think? walk me through your reasoning"; Set up review rotation — my reviews became the exception | Team moved faster, developer became a collaborator | Delegated tasks I could do faster — team needed the reps, not my speed |

---

## The DRIVE Framework

> Works for ANY question — technical, non-technical, system design, behavioral, debugging, architecture, people problems.

**D**efine → **R**educe → **I**mplement → **V**alidate → **E**volve

**D — Define** is the Situation: what's the real problem, who's affected, what does success look like. **R — Reduce** maps to the Task: split the problem into small, independently verifiable pieces. **I — Implement** is the Action: start with the riskiest or most impactful part, POC before committing. **V — Validate** is the Result: measure outcomes, not just outputs — data beats feelings. **E — Evolve** is the Lesson: what changed permanently, what did the system learn.

Use this as a thinking backbone. It doesn't need to be announced — just let the structure guide the narrative.

---

# PRINCIPLE 1: Customer & Ownership

> *"How does your code solve a user problem? Show us you never say 'that's not my job.'"*

---

## Story A: GPS Warehouse Scaling — KocSistem

**Situation (Define):** I built a GPS-based warehouse management system for enterprise logistics clients — Arcelik, Beko, Bosch, Aygaz. Real-time truck tracking inside warehouses. The system worked fine with 50 trucks. The client signed three more warehouses — suddenly 500+ trucks, 250 GPS writes per second. The SQL Server dashboard froze. Users couldn't see truck positions. The entire value proposition — real-time visibility — was gone.

**Task (Reduce):** Make the system handle 10x load without rewriting everything. Clients were already onboarding. I broke the problem down: the bottleneck was that every GPS write went directly to SQL Server, and the dashboard queried the same table. Reads and writes were fighting for the same rows. Two separate concerns — real-time display and historical storage — were tangled into one data path.

**Action (Implement):** The core insight was that the live view and the historical record are two different things being forced to share the same pipe — and they were strangling each other. I split them apart.

```
╔═════════════════════ BEFORE ═══════════════════════╗
║                                                    ║
║  ┌────────────┐  250 w/s   ┌────────────────┐     ║
║  │ GPS Device │───────────▶│                │     ║
║  └────────────┘            │   SQL Server   │     ║
║                            │  (single DB)   │     ║
║  ┌────────────┐  reads     │                │     ║
║  │ Dashboard  │───────────▶│                │     ║
║  └────────────┘            └────────────────┘     ║
║                                                    ║
║  ⚡ reads + writes on same table = FROZEN           ║
╚════════════════════════════════════════════════════╝

╔══════════════════════ AFTER ═══════════════════════╗
║                                                    ║
║  ┌────────────┐         ┌─────────────────┐        ║
║  │ GPS Device │────────▶│  Redis (in-mem) │        ║
║  └────────────┘         │ latest pos only │        ║
║                         └───┬─────────┬───┘        ║
║                             │         │            ║
║                    read     │         │ batch 30s  ║
║                 ◀───────────┘         │            ║
║  ┌────────────┐ sub-sec               ▼            ║
║  │ Dashboard  │             ┌─────────────────┐    ║
║  └────────────┘             │   SQL Server    │    ║
║                             │  history only   │    ║
║                             └─────────────────┘    ║
║                                                    ║
║  ┌─────────┐ sync ┌─────────┐ sync ┌─────────┐    ║
║  │ Primary │◀────▶│ Replica │◀────▶│ Replica │    ║
║  └─────────┘      └─────────┘      └─────────┘    ║
║          auto-failover (majority vote)             ║
╚════════════════════════════════════════════════════╝
```

The live view got its own fast, in-memory store (Redis) that held only the latest position per truck and could answer in under a second. The historical record continued going to the database, but in batches every 30 seconds instead of on every GPS ping. The database was no longer competing with itself — live reads went one way, historical writes went another.

For reliability, I set up a small cluster with automatic failover — think of it as a hot backup that takes over immediately if the primary dies, without any human intervention required. I kept all nodes holding the same data rather than splitting it across them, because the dataset was small enough to fit on one machine. Splitting the data would have added routing and rebalancing complexity for zero practical benefit. I also added a check at the entry point: if a GPS device sent a message in an unexpected shape, the system would reject it immediately with a clear error rather than quietly writing garbled data to storage.

The system was built so each client's rules — warehouse boundaries, truck types, compliance logic — lived in configuration rather than code. One codebase served all four clients. Onboarding a new client meant updating config, not writing new software.

**Result (Validate + Evolve):** Dashboard went from frozen to sub-second. System scaled from 50 to 500+ trucks. Same architecture handled all four client warehouses. Project won the 2019 IDC Award and a Customer Satisfaction Award. Onboarding new clients went from months to weeks.

**Tradeoffs, risks & alternatives:** I considered Kafka, but it would have meant a new cluster, new ops burden, and new team knowledge for a problem Redis already solved — we already had Redis in the stack. Kafka makes sense when you need strict ordering guarantees or multiple independent consumer groups for the same event stream, neither of which applied here. I also considered just scaling up SQL Server vertically, but that would have delayed the problem without fixing it — the fundamental issue was reads and writes competing on the same table, not hardware capacity. A full CQRS split with a separate read database was also on the table, but it was too heavy for the timeline; Redis gave the same read/write separation with minimal code changes.

The main risk with the in-memory store is that if a background worker crashes mid-batch, it might reprocess the same positions twice. I handled this by making the database write idempotent — writing the same position twice produces the same result as writing it once, so replays are safe. The other risk was automatic failover misfiring during a brief network hiccup and promoting a standby unnecessarily, but with three nodes and a majority vote requirement, that kind of false trigger was unlikely.

**Lesson:** Load calculations need to happen before choosing an architecture, not after the first outage. The simplest solution that fits the constraints is usually the right one.

**Likely follow-ups:**
- *"How did you migrate to Redis without downtime?"* — Ran both paths in parallel: GPS writes went to Redis AND SQL Server simultaneously for a week. Dashboard switched to reading from Redis once we confirmed data parity. If Redis had a problem, the dashboard could fall back to SQL Server. Zero downtime, fully reversible.
- *"What happens if Redis goes down?"* — Redis was clustered with automatic failover (3 nodes, majority vote). If the primary died, a replica promoted within seconds. In the unlikely event all Redis nodes failed, GPS writes would still go to SQL Server — the dashboard would be slower but not dead. We never needed this fallback in production.
- *"Why not just add a read replica to SQL Server instead?"* — A read replica solves the contention problem but doesn't solve the latency problem. SQL Server's replication lag meant the dashboard would still show stale positions. Redis gave sub-millisecond reads for the latest position — a read replica would have been seconds behind under load.
- *"How did you handle the transition with four different clients?"* — All four used the same codebase. Client-specific rules (warehouse boundaries, truck types, compliance logic) lived in configuration, not code. The architecture change was transparent to clients — they didn't need to change anything on their side.
- *"What would you do differently today?"* — I'd add proper capacity planning from day one — load-test with projected traffic before the first client onboards. The fix was straightforward, but we shouldn't have needed to discover the bottleneck in production.

> **TR:** Anlık konum ve geçmiş kayıt aynı veritabanını paylaşıyordu, birbirini boğuyordu. İkisini ayırdım: anlık konumlar için hızlı bellek deposu, geçmiş için veritabanı. Sistem 50 kamyondan 500+ kamyona ölçeklendi, IDC ödülü kazandı.

---

## Story B: Leading Without Authority — KocSistem

**Situation (Define):** I was a Dev Lead. The team was stuck on weekly releases — big, risky deployments. Every release was fire-fighting. SLA breaches were climbing. Developers built locally, copied to servers, and hoped. Nobody had assigned CI/CD as a project. There was no mandate from management and no budget allocated.

**Task (Reduce):** I broke this into a testable experiment: could daily automated deployments work for one team, over two sprints, with measurable outcomes? Rather than proposing an org-wide change, I proposed a low-risk pilot.

**Action (Implement):** I started by measuring the pain with data — deployment times, failure rates, how much time was spent in meetings vs coding. Presented the data to the team as "am I reading this right?" not "here's what's wrong." Then I volunteered our own team for the pilot — nobody believes in a change you're not willing to try yourself.

I did the unglamorous work: fixed flaky tests personally — mostly tests that were timing-dependent, written to just wait a fixed amount of time and hope the system caught up, rather than actually checking whether it had. I rewrote those to actively wait for the expected state before moving on. Wrote documentation nobody asked for. Was online at 6 AM for the first automated deployments. Pair-programmed with the most skeptical developers — demonstrated, didn't mandate.

On the second day, a config mismatch between staging and production caused a service to start with wrong connection strings. Caught it in 3 minutes because monitoring was part of the pilot, rolled back in under 5 minutes. Under the old weekly process, this would have been hours of guessing. The incident actually proved the value — faster detection, faster rollback.

**Result (Validate + Evolve):** Weekly to daily in 3 weeks for our team. Others saw it working, asked for the same. Six months later, the whole organization shifted. SLA breaches dropped 60%. Two developers never fully bought in but didn't block it — the results were too clear. Over time, as the old manual process was simply gone, they adapted.

**Tradeoffs, risks & alternatives:** I could have gone top-down — as Dev Lead I had the authority to mandate the change. But mandated changes get compliance, not ownership. People follow the process when you're watching and revert when you're not. By going through a pilot and letting the team see it work, the adoption became self-sustaining. The downside of the pilot approach is that it's slower — the org-wide shift took 6 months instead of potentially a few weeks. I accepted that trade because the alternative was adoption without conviction.

The risk of going first with our own team was that any failures would be visible and could be used as evidence against the approach. I mitigated that by setting up monitoring before the first deploy, so when something did go wrong on day 2, we had data and a fast rollback — and it became the best argument for the approach.

**Lesson:** Real ownership means seeing a problem and taking responsibility without being asked. The pilot approach works because "let me try this with one team for two sprints" is hard to say no to — if it fails, you go back; if it works, you have proof.

**Likely follow-ups:**
- *"What if the pilot had failed?"* — I had a revert plan from day one: if failure rates increased or team velocity dropped after two sprints, we'd go back to manual deployments and I'd present the data on what went wrong. A failed pilot with data is still useful — it tells you what to fix before the next attempt.
- *"How did you handle the two developers who never fully bought in?"* — I didn't force the issue. They followed the process because the automation was there — they didn't have to love it to use it. Over time, as the manual process simply no longer existed, they adapted. Not everyone needs to be an advocate; they just need to not block.
- *"How did you measure success?"* — Three numbers: deployment frequency (weekly → daily), time to recover from a failed deployment (hours → minutes), and SLA breach rate (tracked monthly). I presented these at the end of each sprint during the pilot so the data was visible, not hidden in a report.
- *"Didn't management eventually mandate CI/CD anyway?"* — Yes, but 6 months after we'd already proven it. By then, our team's results were the evidence used to justify the mandate. The difference: teams that adopt from conviction maintain the practice; teams that comply with a mandate often revert when oversight drops.

> **TR:** Haftalık release döngüsü SLA ihlallerine yol açıyordu ama değiştirme yetkim yoktu. Kendi ekibimi pilot olarak önerdim, acıyı veriyle gösterdim, zorlamadım. Haftadan güne geçtik, SLA ihlalleri %60 azaldı.

---

## Story C: Stepping In as PO and Tech Lead — Combination AB

**Situation (Define):** Both the tech lead and the product owner were unavailable during quarter planning. Priorities weren't set, scope wasn't defined, no commitments made. The team was about to stall.

**Task (Reduce):** Prevent a leadership vacuum from derailing the quarter. I scoped it as: get stakeholder priorities, map them to technical dependencies, run planning with the team, and document every decision for the returning leads.

**Action (Implement):** I didn't wait for someone to assign the role. Told the team explicitly: "I'm not the PO or the tech lead, but someone needs to drive this. I'll do it, and when they're back we'll adjust."

*Stakeholder alignment:* I set up 30-minute one-on-ones with each key stakeholder — product, business, and the engineers who had context on previous commitments. My opening question in every meeting: "If we can only deliver 3 things this quarter and everything else slips, what are they?" That framing forces real prioritization — "everything is critical" is not an answer you can plan around. I heard different answers from different people, wrote them all down, and looked for the overlap. Items that multiple stakeholders independently named as essential became the non-negotiables.

*Technical dependency mapping:* I sat with the engineering team and drew a dependency graph on a whiteboard — what blocks what? Some items couldn't start until others were done. That gave me ordering constraints independent of business priority. Then I combined the two lists: items that were both high-priority business value and unblocked the most downstream technical work went first.

*Priority framework:* High business impact, low effort first. When two items had similar weight, one tiebreaker: which one frees up the most other work if done first? I wrote this reasoning down explicitly — not just the final priority order, but why each item landed where it did. The returning leads needed to audit the logic, not just the outcome.

*Planning sessions:* I ran two sessions with the full team. In the first, I presented the priority order and the dependency map — not as "here's what we're doing" but as "here's what I think, tell me what I'm missing." Engineers flagged two dependencies I hadn't caught. I adjusted on the spot. In the second session we sized the work and set sprint milestones. I left buffer in the plan — never plan at 100% utilization.

*Pre-emptive transparency:* Before the quarter started, I shared the plan with the returning leads in writing: what we're doing, why this order, what assumptions I made, and what I'd want them to override if they disagreed. That way, when they returned, there were no surprises — they could review asynchronously and flag issues before we were too far in.

**Result (Validate + Evolve):** All planned tasks completed before the quarter ended — a first. PO and tech lead reviewed when they returned, approved the direction. No surprises because everything was documented.

**Tradeoffs, risks & alternatives:** The main risk of stepping in without domain expertise was making wrong priority calls. I mitigated this by asking stakeholders directly instead of guessing, and by sharing the draft plan before the quarter started to get early sign-off. The alternative — waiting for the leads to return or escalating to management — would have left the team idle for days and put the quarter at risk. Even if the returning leads disagreed with some choices, a documented starting point is better than a blank page.

**Lesson:** Leadership isn't a title. Imperfect action beats no action. The key is transparency about the role you're filling and documenting your reasoning so others can adjust.

**Likely follow-ups:**
- *"What if the returning PO disagreed with your priorities?"* — That's exactly why I documented the reasoning, not just the outcome. If they disagreed, they could see which assumptions to challenge. I also shared the plan before the quarter started specifically so they could override before we were committed. I'd rather be corrected early than validated late.
- *"Did you have domain expertise for the prioritization?"* — No, and I didn't pretend to. That's why I asked stakeholders "if we can only do 3 things" instead of deciding myself. My value was in the process — mapping dependencies, structuring the plan, running the sessions — not in knowing the product better than the PO.
- *"How did you handle scope creep during the quarter?"* — Anything new went through the same test: does it outrank something already on the list? If yes, what gets bumped? I didn't say no to new requests — I said "yes, and here's what it displaces." That kept decisions visible and honest.
- *"Wasn't this risky for your career? What if things went badly?"* — Yes. If the quarter had failed, I'd have been the person who stepped into a role they weren't qualified for. I accepted that risk because the alternative — a stalled team with no direction — was certain failure. A documented attempt that partially works is better than no attempt at all.

> **TR:** PO ve tech lead çeyrek planlaması sırasında yoktu, ekip durma noktasına gelmişti. Rolü açıkça üstlendim, paydaşlarla bire bir konuştum, teknik bağımlılıkları haritaladım, her kararı belgeledim. İlk kez tüm planlanan işler tamamlandı.

---

## Story D: Third-Party Partner Turnaround — Toyota

**Situation (Define):** A third-party logistics system integration at Toyota. Their tech lead was slow to respond, defensive, treated every request like an attack on his system. Emails went unanswered for days. The timeline was slipping.

**Task (Reduce):** I needed to understand the root cause before trying to fix the collaboration. Was it technical disagreement, capacity, or something else?

**Action (Implement):** I stopped emailing and went in person to their office. Asked questions instead of making demands: "Help me understand what went wrong before with previous partners." He opened up — previous teams had pushed changes without notice, broken things, blamed his team. He wasn't difficult; he'd been burned.

I proposed a trust-building approach: start with read-only access only so there was no risk to him, give advance notice before any changes, shared daily communication channel, and credited his team publicly when things worked. Email is easy to ignore and hard to read tone — in person, you can have a real conversation. The first real shift happened within 2-3 weeks. Full trust — where he proactively suggested improvements — took about 6 weeks. The key was consistency: every change got advance notice, every success got public credit for his team.

**Result (Validate + Evolve):** Within weeks, the dynamic changed completely. He started proactively suggesting improvements. Eventually referred another division to work with us.

**Tradeoffs, risks & alternatives:** Escalating to managers with formal SLAs would have been the faster path to enforced response times, but it would have created compliance without trust — an adversarial dynamic that makes long-term integration harder. Working around the partner entirely was also an option, but we'd have lost domain knowledge and the integration quality would have suffered.

The risk of the in-person approach was that it required time and might not have addressed the real root cause. If it hadn't worked, I would have escalated to propose a joint working agreement with documented SLAs. But the in-person approach worked because the root cause was relational, not technical — he felt disrespected by previous partners, not incapable of delivering.

**Lesson:** Build trust with external teams by starting small and giving before asking. Trust builds through consistent small actions, not grand gestures.

**Likely follow-ups:**
- *"How long until you would have escalated if in-person didn't work?"* — I gave it 2-3 weeks. If there was no shift in responsiveness after consistent in-person effort, I'd have proposed a joint working agreement with documented SLAs and escalation paths. But escalation was the last resort — it signals "I couldn't solve this," and it creates an adversarial dynamic that's hard to undo.
- *"How did you maintain the relationship long-term?"* — Consistency. Advance notice before every change, credit to his team after every success, and never surprising him. When we had issues on our side, I told him first, before he could discover it himself. Trust is maintained by the same behaviors that built it.
- *"What if the root cause had been technical incompetence, not trust?"* — Then the read-only phase would have revealed it — we'd have seen gaps in their system's documentation, testing, or architecture. In that case, I'd have shifted from trust-building to knowledge sharing and offered to pair on the integration. The approach adapts once you understand the real root cause.
- *"How do you distinguish between a difficult person and a burned person?"* — Ask about their history. "Help me understand what went wrong before" is a diagnostic question. A difficult person gives vague complaints or blames everyone. A burned person gives specific incidents with specific actors. His answers were specific — he named what previous partners had done. That told me the problem was recoverable.

> **TR:** Dış partner zor görünüyordu ama aslında önceki ekiplerce hayal kırıklığına uğratılmıştı. E-postayı bırakıp yüz yüze gittim, küçük güven adımları attım. 6 haftada tam işbirliğine dönüştü.

---

# PRINCIPLE 2: Dive Deep

> *"Be ready to explain the technical why behind your architectural choices with data and solid judgment."*

---

## Story A: RabbitMQ Split-Brain — Toyota

**Situation (Define):** Toyota Material Handling, T-ONE system — autonomous forklifts in warehouses. 30+ microservices, .NET 8, RabbitMQ for real-time messaging. A lost message means a forklift stops on the warehouse floor. A temporary network blip caused our 3-node RabbitMQ cluster to partition. Each side thought the other was dead. Messages got lost. Forklifts waited for commands that never came.

The root cause: by default, the messaging cluster was configured to ignore a network split — meaning if the nodes lost sight of each other, each side would keep accepting messages independently and the two halves would diverge. We'd never caught this in testing because our test environment had all the nodes running on the same machine, so there was never a real network between them to split.

```
╔═══════════ BEFORE — "ignore" (default) ════════════╗
║                                                    ║
║        ┌────────┐  ⚡ SPLIT  ┌────────┬────────┐   ║
║        │ Node A │─── ✕ ─────│ Node B │ Node C │   ║
║        └───┬────┘           └───┬────┴────────┘   ║
║            │                    │                  ║
║            ▼                    ▼                  ║
║       ┌──────────┐         ┌──────────┐           ║
║       │ Queue v1 │         │ Queue v2 │           ║
║       │ accepts  │         │ accepts  │           ║
║       │ msgs     │         │ msgs     │           ║
║       └────┬─────┘         └────┬─────┘           ║
║            │                    │                  ║
║            └──── reconnect ─────┘                  ║
║                     ▼                              ║
║         ⚡ CONFLICT: which version wins?            ║
║         → loser's msgs silently discarded          ║
╚════════════════════════════════════════════════════╝
```

**Task (Reduce):** I broke the fix into: diagnose and reconcile the immediate damage, change how the cluster behaves during a network split, upgrade to a queue type with stronger guarantees, prevent recurrence through failure testing, and improve visibility for future incidents.

**Action (Implement):** I reconciled the queues by hand — comparing what the system believed existed against what was actually running, re-registering the ones that had gone out of sync, and removing the ghost entries that pointed to nothing.

*Network split behavior — "pause, don't guess":* When two halves of a cluster lose contact, each side has to decide what to do. The default was "keep going" — both sides kept accepting messages independently, so by the time they reconnected, they had conflicting versions of reality. I changed it to: the smaller side freezes until it can rejoin the majority. You lose availability on that side temporarily, but you don't lose data. The alternative — automatically picking a winner and discarding the other side's messages — restores availability faster but silently throws messages away. For forklifts, a frozen forklift waiting for a command is safe. A silently dropped command to a moving one is not.

*How I implemented it:* One config line in `rabbitmq.conf`: `cluster_partition_handling = pause_minority`. RabbitMQ counts votes — a node is "minority" if it can't see a quorum (more than half) of the cluster. In a 3-node cluster, that means a lone node that loses sight of the other two pauses all queue operations and stops accepting new connections until it can rejoin. The majority side keeps running normally.

```
╔═══════════ AFTER — pause_minority ═════════════════╗
║                                                    ║
║        ┌────────┐  ⚡ SPLIT  ┌────────┬────────┐   ║
║        │ Node A │─── ✕ ─────│ Node B │ Node C │   ║
║        └───┬────┘           └───┬────┴───┬────┘   ║
║            │                    │        │         ║
║            ▼                    ▼        ▼         ║
║       ┌──────────┐         ┌─────────────────┐    ║
║       │ ⏸ PAUSED │         │ MAJORITY (2/3)  │    ║
║       │ minority │         │ ✅ keeps running  │    ║
║       │ (1 node) │         │ ✅ accepts msgs   │    ║
║       │ no msgs  │         │ ✅ single reality │    ║
║       └────┬─────┘         └────────┬────────┘    ║
║            │                        │              ║
║            │     network heals      │              ║
║            └────────▶ sync ◀────────┘              ║
║                       ▼                            ║
║           ✅ single reality restored                ║
╚════════════════════════════════════════════════════╝
```

*Queue guarantees — "don't confirm until it's safe":* The old queue type (classic mirrored queues) would tell the sender "got it" as soon as the main node had the message, then copy it to backup nodes in the background. If the main node crashed before the copy finished, the message was gone but the sender didn't know. I switched to quorum queues, which use the Raft consensus protocol — they only confirm once a majority of replicas have physically written the message to disk. Slower per message, but the confirmation actually means something.

```
╔════════ Classic Mirrored Queue (old) ══════════════╗
║                                                    ║
║  ┌──────────┐         ┌────────┐                   ║
║  │ Producer │────────▶│ Node A │                   ║
║  └────┬─────┘         └───┬────┘                   ║
║       ▲                   │ async copy             ║
║       │                   ▼                        ║
║       │  ack!        ┌─────────┐                   ║
║       │ (immediate)  │ Node B  │  (maybe later)    ║
║       └──────────────│ Node C  │                   ║
║                      └─────────┘                   ║
║                                                    ║
║  ⚡ Node A crashes before copy completes            ║
║  → message LOST, producer thinks it's safe         ║
╚════════════════════════════════════════════════════╝

╔════════ Quorum Queue — Raft (new) ═════════════════╗
║                                                    ║
║  ┌──────────┐         ┌────────┐                   ║
║  │ Producer │────────▶│ Node A │──┐                ║
║  └──────────┘         └────────┘  │ replicate      ║
║                                   ▼                ║
║                       ┌────────┐ ┌────────┐        ║
║                       │ Node B │ │ Node C │        ║
║                       └───┬────┘ └───┬────┘        ║
║                           │          │             ║
║              wait: 2 of 3 must write to disk       ║
║                           │          │             ║
║                           ▼          ▼             ║
║                     ┌──────────────────┐           ║
║                     │  majority wrote  │           ║
║                     │  → ack! to prod  │           ║
║                     └──────────────────┘           ║
║                                                    ║
║  ✅ ack sent AFTER majority write to disk           ║
║  → crash-safe, guaranteed durable                  ║
╚════════════════════════════════════════════════════╝
```

*Failure testing — "break it on purpose, in the pipeline":* We built chaos tests using Toxiproxy to introduce real network conditions — killing nodes mid-send, severing connections between them, adding latency. These ran automatically in a separate pipeline stage on every merge. The goal was to find failure modes before production did. This caught two edge cases we hadn't anticipated: one where a node restart silently dropped in-flight messages, and one where a crash during handoff caused the same message to be processed twice. I handled the second by making storage writes idempotent — same input always produces the same result, regardless of how many times it runs.

*Visibility — "trust the trace, not the health check":* The cluster's own dashboard showed all nodes as healthy even during a partition — it used internal peer connections, not actual queue health. We added OpenTelemetry spans at every send and receive point. If a message was sent but not confirmed within a deadline, it appeared as a gap in our trace dashboard. The system's self-reported health said everything was fine; our traces told the truth.

**Result (Validate + Evolve):** No more silent message loss. Chaos tests caught two more edge cases the first month. Changed the team's mindset — "how does this break?" became part of code reviews, not just "does this work?"

**Tradeoffs, risks & alternatives:** I considered migrating to Kafka, which provides stronger ordering and partition tolerance by design. But migrating 30+ services mid-project was too risky and disruptive — we'd have needed new infrastructure, new operational knowledge, and a service-by-service rewrite. We fixed the configuration and added chaos tests instead.

The tradeoff of pausing the minority side is that during a real network split, part of the cluster becomes temporarily unavailable. For this domain that was acceptable — a brief pause is recoverable; a silently dropped command to a moving forklift is not. The automatic recovery option would have kept things available, but by discarding messages on the losing side, which was a worse outcome here.

**Likely follow-ups:**
- *"What if the minority never comes back?"* — The paused node stays paused indefinitely. An operator has to manually intervene to either restart it or remove it from the cluster. We added alerting so any paused node would page within 60 seconds.
- *"What if the two sides are exactly equal in size — 1 vs 1 in a 2-node cluster?"* — We ran 3 nodes specifically to avoid this. In a 2-node setup there's no clear majority. With 3, a single isolated node is always the minority.
- *"How did you know which messages were lost after the incident?"* — We didn't, definitively. The services that sent commands had their own retry logic — if a forklift didn't acknowledge within a timeout, it would re-send. That gave us at-least-once delivery, not exactly-once. The quorum queue switch + idempotent writes made the re-send safe.
- *"Why not just use acknowledgments and retry from the start?"* — We had acknowledgments, but the cluster itself was confirming receipt before ensuring durability. The sender thought the message was safe, so no retry was triggered. The problem was the false confirmation, not the retry logic.

**Lesson:** Reading documentation is not the same as understanding how distributed systems break. Test environments need to model real network conditions. Understanding only comes from testing failure modes, not just the happy path.

> **TR:** Ağ bölünmesinde küme iki tarafa ayrıldı, mesajlar sessizce kayboldu. "Tahmin etme, dondur" ilkesiyle küçük tarafı bekleyecek şekilde yapılandırdım; mesajlar çoğunluk yazmadan onaylanmıyor. Sessiz mesaj kaybı sıfırlandı, chaos testi her build'in parçası oldu.

---

## Story B: GraphQL Migration — Combination AB

**Situation (Define):** 60+ .NET 9 microservices. Three API styles: GraphQL for internal frontends, gRPC for service-to-service, REST for external partners. The REST API was causing problems — mobile needed 3 fields, web needed 20. Frontend was making 5-6 requests per page with massive over-fetching. Every new UI feature required a backend endpoint change.

**Task (Reduce):** Migrate to GraphQL without breaking any existing consumer. I broke this into: learn GraphQL hands-on first, prove it works for one endpoint, get team buy-in through working code, then scale gradually.

**Action (Implement):** I wasn't a GraphQL expert when I started, so I built a side project first to hit the pain points myself before proposing anything to the team. Then I proposed a gradual approach: new features built in GraphQL alongside existing REST. No big-bang migration. REST stays until consumers migrate naturally.

I paired with the most skeptical developer on the first production resolver. When the frontend went from five requests to one and he saw it himself, he changed his mind — adoption spread organically from there.

```
╔═════════════════ BEFORE (REST) ════════════════════╗
║                                                    ║
║  ┌────────┐  GET /orders     ┌───────────────┐    ║
║  │        │─────────────────▶│ Order Service │    ║
║  │        │                  └───────────────┘    ║
║  │        │  GET /customers/1 ┌──────────────┐    ║
║  │ Client │─────────────────▶│ Customer Svc │    ║
║  │        │  GET /customers/2 ├──────────────┤    ║
║  │        │─────────────────▶│ Customer Svc │    ║
║  │        │                  └──────────────┘    ║
║  │        │  GET /products/1  ┌──────────────┐    ║
║  │        │─────────────────▶│ Product Svc  │    ║
║  └────────┘                  └──────────────┘    ║
║                                                    ║
║  ⚡ 5-6 requests per page  ⚡ N+1 per related item  ║
╚════════════════════════════════════════════════════╝

╔═══════════ AFTER (GraphQL Federation) ═════════════╗
║                                                    ║
║  ┌────────┐  1 query   ┌──────────────┐            ║
║  │ Client │───────────▶│   Gateway    │            ║
║  └────────┘            │ (Apollo Fed) │            ║
║                        └──┬─────┬──┬──┘            ║
║                           │     │  │               ║
║                     ┌─────┘     │  └──────┐        ║
║                     ▼           ▼         ▼        ║
║              ┌───────────┐ ┌─────────┐ ┌─────────┐ ║
║              │  Orders   │ │Customer │ │ Product │ ║
║              │  Service  │ │ Service │ │ Service │ ║
║              │(owns its  │ │(batched)│ │(batched)│ ║
║              │ fields)   │ │         │ │         │ ║
║              └───────────┘ └─────────┘ └─────────┘ ║
║                                                    ║
║  ✅ 1 request  ✅ batched lookups  ✅ no N+1         ║
╚════════════════════════════════════════════════════╝
```

*Federation — "each service is an expert, the gateway is the coordinator":* Rather than one big API that knows everything, each service published its own slice of the data contract — just the part it owns. A gateway layer composed all those slices into a single entry point. When a client asks for an order and the customer behind it, the gateway knows which service to ask for each piece and stitches the answer together. The client asks one question; the routing is invisible to it.

*The N+1 problem — "don't make a hundred phone calls when one will do":* A common trap with this kind of API is that fetching a list of 50 orders, each with a customer, would trigger 50 separate database lookups for the customer — one per item. I fixed this by batching: instead of resolving each item immediately, the system collects all the pending lookups and fires a single query for all of them at once. One database call instead of fifty.

*Security — "lock the menu, not just the food":* I limited how deeply nested a query could go, so clients couldn't construct requests that would cascade into thousands of database calls. I pre-registered all valid queries at build time — in production, clients send a short fingerprint instead of the full query text, and the server only executes queries it already knows about. Anything not on the list is rejected. Permissions are checked where data is fetched, not at the door — everyone sees the same API shape, but what comes back depends on your role.

*Versioning — "deprecate, don't delete":* Instead of creating new URL paths for each API version and maintaining multiple versions forever, I marked old fields as deprecated and let consumers migrate at their own pace. The build pipeline would fail if anyone tried to remove a field without going through that deprecation step first — no accidental breaking changes.

*Caching — "move it closer to the data, not the edge":* Traditional APIs let you cache responses at the network level because the URL uniquely identifies the request. With a single endpoint that accepts arbitrary queries, that doesn't work. I cached at the data layer instead — frequently-read results stored close to where they're computed, not at the network boundary.

**Result (Validate + Evolve):** 6-month migration, zero breaking changes. Frontend went from 5-6 requests per page to 1. Team adopted it organically after seeing it work.

**Tradeoffs, risks & alternatives:** BFF (Backend for Frontend) was an option — one backend per client type. But that creates duplication across BFFs and coordination overhead that grows with every new client type. GraphQL federation gives each client exactly what it needs from a single endpoint without duplication. REST with sparse fieldsets was also possible but adds complexity to every endpoint and doesn't solve the "one endpoint per UI view" problem fundamentally.

The big-bang approach — rewriting everything at once — would have been cleaner to reason about but too risky with 60+ services and live consumers. The gradual approach meant maintaining two API surfaces during the transition, which added cognitive overhead, but it meant zero breaking changes and a reversible path.

GraphQL does add backend complexity: resolver design, N+1 awareness, query cost analysis. The bet was that this backend complexity pays for itself in frontend simplicity and eliminated the constant "add a new endpoint for this new view" cycle.

**Lesson:** The best way to introduce a new technology is to pair with the biggest skeptic on the first real implementation. Working code convinces faster than presentations.

**Likely follow-ups:**
- *"How did you handle authentication across federated services?"* — Permissions are checked where data is fetched, not at the gateway. The gateway forwards the user's identity token to each service. Each service decides independently what to return based on that identity. This means the gateway doesn't need to know business rules — it just routes. A service returning customer data checks "can this user see this customer?" on its own.
- *"What about monitoring — how do you find slow resolvers?"* — Each resolver is instrumented with timing metrics. The gateway traces the full query execution showing which service took how long. When a query is slow, the trace tells you which subgraph is the bottleneck. We set alerting thresholds per resolver — if a resolver that normally takes 20ms starts taking 200ms, it pages.
- *"How did you prevent the N+1 problem from coming back as new developers joined?"* — DataLoader is part of the project template. Every new resolver gets it by default. We also added a query cost analyzer that estimates the number of downstream calls for any query — if the cost exceeds a threshold, the query is rejected before execution. New developers can't accidentally ship an N+1 because the pipeline catches it.
- *"What was the learning curve for the team?"* — Steep for the first 2 weeks. Resolver thinking is different from REST controller thinking. I pair-programmed the first 3 resolvers with different developers to spread knowledge. After about a month, the team was self-sufficient. The side project I built before proposing it meant I could answer "how do I…?" questions immediately instead of both of us guessing.
- *"Why Apollo Federation specifically and not schema stitching?"* — Schema stitching centralizes the schema composition — the gateway has to know about every type. Federation lets each service declare its own types and the gateway discovers them. That means teams can deploy their service independently without touching the gateway config. For 60+ services, that independence is essential.

> **TR:** 60+ servis, sayfada 5-6 ayrı istek, aşırı veri çekme. Federation mimarisine geçtim, N+1 sorununu toplu sorgularla çözdüm, yavaş yavaş geçiş yaptım. Tek istekle sayfa, sıfır kırılma, 6 ayda tamamlandı.

---

## Story C: Terraform State Corruption — KocSistem

**Situation (Define):** Two developers ran our infrastructure tool simultaneously with no concurrency protection. Both tried to write to the same shared file that tracks what infrastructure exists — and they corrupted it. The result was a mismatch between what the system believed it had created and what was actually running in the cloud. Some things existed in the cloud but weren't tracked. Others were tracked but didn't exist. Trying to run the tool again would attempt to create things that were already there and fail.

**Task (Reduce):** Fix the immediate corruption by reconciling the tracking file against reality, then prevent recurrence by adding locking, and separate state by environment.

**Action (Implement):** Fixed by hand — went through the cloud console and compared it against what the tracking file said. Re-registered resources that existed but weren't recorded. Removed tracking entries that pointed to nothing. Took most of a day.

```
╔══════════════════ BEFORE ══════════════════════════╗
║                                                    ║
║  ┌────────────┐                                    ║
║  │ Pipeline A │──┐                                 ║
║  └────────────┘  │  simultaneous  ┌─────────────┐  ║
║                  ├───────────────▶│ State File  │  ║
║  ┌────────────┐  │      write     │ (shared)    │  ║
║  │ Pipeline B │──┘                └──────┬──────┘  ║
║  └────────────┘                          │         ║
║                                  ⚡ CORRUPT         ║
║                                  state ≠ reality   ║
║                                  next run fails    ║
╚════════════════════════════════════════════════════╝

╔══════════════════ AFTER ═══════════════════════════╗
║                                                    ║
║  ┌────────────┐ ┌──────┐ ┌───────┐ ┌──────────┐   ║
║  │ Pipeline A │▶│ LOCK │▶│ WRITE │▶│ RELEASE  │   ║
║  └────────────┘ └──────┘ └───────┘ └──────────┘   ║
║                                                    ║
║  ┌────────────┐ ┌──────┐                           ║
║  │ Pipeline B │▶│ WAIT │─ ─ ─ ─ ─ ▶ (its turn)   ║
║  └────────────┘ └──────┘                           ║
║                 (blob lease)                       ║
║                                                    ║
║  ┌───────────┐  ┌───────────┐  ┌───────────┐      ║
║  │ dev/state │  │ stg/state │  │prod/state │      ║
║  └───────────┘  └───────────┘  └───────────┘      ║
║       ✅ isolated per environment                   ║
╚════════════════════════════════════════════════════╝
```

*The fix — "a checkout system for the tracking file":* Think of it like a library book. Before anyone can take it out and write in it, they check it out. While it's checked out, nobody else can touch it. When they're done, they return it. I implemented exactly that: Terraform's remote state backend with state locking — the state file lives in cloud storage (Azure Blob in our case), and locking is handled via a lease on the blob. Any pipeline that wants to apply changes has to acquire the blob lease first. The moment a pipeline holds it, every other pipeline trying to do the same thing will wait or fail fast with a clear error. Separated the state file by environment too — dev, staging, and production each got their own container — so a mistake in one couldn't bleed into another.

**Result (Validate + Evolve):** Never happened again. State locking became non-negotiable for every new project.

**Tradeoffs, risks & alternatives:** There are managed services that handle this locking and collaboration out of the box, with additional features like policy enforcement and cost estimation. But they require budget and add an external dependency. Using cloud storage we already had access to was free and sufficient. I'd reach for a managed service when multiple independent teams are making changes to the same infrastructure and need more than just concurrency protection.

The choice to use environment-level isolation within the same storage setup, rather than completely separate storage per environment, is a trade-off between simplicity and blast radius. Shared storage is easier to manage but means a misconfiguration could theoretically affect all environments. Fully separate storage per environment would have given more isolation, but the added overhead wasn't worth it for our team size.

**Lesson:** The tracking file for infrastructure contains sensitive data — resource IDs, sometimes credentials. It needs to be encrypted, access-controlled, and never modified by more than one process at a time. An early mistake that became a permanent policy.

**Likely follow-ups:**
- *"How do you handle infrastructure drift — when someone changes something in the console manually?"* — We added a drift detection step that runs nightly. It compares what the tool thinks exists against what's actually running in the cloud. If there's a mismatch, it creates an alert. The rule is: if you changed it manually, you either import the change into the tool or revert it. No silent drift allowed.
- *"How did you manage Terraform modules across multiple teams?"* — Shared modules lived in a versioned repository. Teams referenced a specific version. Upgrading was opt-in per team — you bump the version when you're ready. This prevented a single module change from breaking everyone simultaneously. We also ran automated validation on module changes before they could be published.
- *"What about secrets in the state file?"* — The state file was encrypted at rest in Azure Blob Storage, access-controlled via RBAC — only the pipeline service principals could read it. Developers couldn't access the raw state file directly. For values that shouldn't be in state at all (like database passwords), we referenced them from a secrets vault at deploy time instead of inlining them.
- *"Why not use Terraform Cloud or Spacelift?"* — Cost and dependency. We were a small team — 2-3 people touching infrastructure. The managed services add value when you have 10+ teams with approval workflows, cost governance, and audit requirements. For us, blob storage locking was sufficient. If the team had grown, I'd have revisited.

> **TR:** İki pipeline eş zamanlı yazdı, altyapı takip dosyası gerçeklikten saptı. Elle uzlaştırdım, sonra ortam başına ayrı dosyaya geçip kilit ekledim. Bir daha yaşanmadı, her yeni projeye standart oldu.

---

## Story D: Build Parallelization — Volvo Cars

**Situation (Define):** Embedded automotive software, multiple build targets: QNX ARM, Linux x86, Android Automotive. Safety-critical — a bad release blocks the vehicle program. Build orchestration ran sequentially. 40+ minutes for a full build. Developers waited an hour for verification feedback.

**Task (Reduce):** Cut build time without compromising safety checks. I broke this into: profile resource usage per target, design a smart batching strategy, and skip unchanged modules.

**Action (Implement):** First tried running everything in parallel — the build server ran out of memory and crashed after one day. Some build targets need a lot of memory during the final assembly phase — the step where all the compiled pieces get joined into a single deployable binary. Running all of them simultaneously was like opening every app on your phone at once: everything grinds to a halt.

```
╔════════ NAIVE — day 1, failed ═════════════════════╗
║                                                    ║
║  t=0 ┌──────────────┐ ┌───────────┐ ┌───────────┐ ║
║      │ QNX ARM 12GB │ │Linux x86  │ │Android 6G │ ║
║      │              │ │       8G  │ │           │ ║
║      └──────┬───────┘ └─────┬─────┘ └─────┬─────┘ ║
║             │               │              │       ║
║             └───────┐       │       ┌──────┘       ║
║                     ▼       ▼       ▼              ║
║              ⚡ 26GB total = OOM CRASH               ║
╚════════════════════════════════════════════════════╝

╔════════ PROFILED — smart scheduling ═══════════════╗
║                                                    ║
║  t=0  ┌───────────┐  ┌───────────┐                ║
║       │Linux x86  │  │Android 6G │  (14GB — fits) ║
║       │       8G  │  │           │                 ║
║       └─────┬─────┘  └─────┬─────┘                ║
║             ▼              ▼                       ║
║  t=8  ┌──────────────────────────┐                 ║
║       │     QNX ARM 12GB         │  (runs alone)   ║
║       └────────────┬─────────────┘                 ║
║                    ▼                               ║
║  t=15 ✅ DONE (was 40 min)                          ║
║                                                    ║
║  ┌────────────────────────────────────────┐        ║
║  │ Each target in own Docker container    │        ║
║  │ → compilers can't conflict             │        ║
║  ├────────────────────────────────────────┤        ║
║  │ Hash inputs vs last build              │        ║
║  │ → unchanged targets skip entirely      │        ║
║  └────────────────────────────────────────┘        ║
╚════════════════════════════════════════════════════╝
```

*The fix — "know your heavyweights before you schedule":* I instrumented each build target with resource monitoring to measure actual peak memory and CPU. Built a scheduling config that expressed the dependency and resource profile for each target. The build orchestrator (we used a Makefile with GNU Make's job server for local, and Azure Pipelines stages for CI) read the config to decide what to run in parallel and in what order. Lightweight targets ran together, the heavy linker step for each platform ran sequentially after its compiler phase.

Each target also runs in its own isolated Docker container — the three platforms use incompatible compilers and toolchains, so without isolation they'd conflict with each other's environment variables and binary paths.

I also built a cache-check step: hash the inputs (source files + compiler version) before each target, compare against the stored hash from the last successful build. If unchanged, skip. This is similar to how ccache works but at the target level rather than individual compilation units.

The key insight on the bottleneck: the slow part wasn't compiling — it was the final linking step, which is inherently single-machine and can't be distributed. So more build agents wouldn't have helped; smarter scheduling was the right fix.

**Result (Validate + Evolve):** 40 minutes down to 15 minutes. QA cycle cut 30%. Developers got feedback 3x faster. Zero compliance findings — every safety gate still passed.

**Tradeoffs, risks & alternatives:** Full parallelization was the obvious first attempt and it failed immediately — proven wrong on day 1. Buying a bigger build server would have helped temporarily but left the sequential architecture intact, which was the real problem. Distributed compilation addresses compilation time but the bottleneck was linking, which is inherently single-machine, so it would have been wasted effort.

The risk of the batching approach is that resource profiles drift over time as build targets evolve. A profile that was accurate when written may not reflect reality six months later if a new target gets added or an existing one grows. I mitigated this by adding profile validation into the build config, so a target exceeding its declared resource budget would fail fast.

**Lesson:** Parallelization isn't "run everything at once." Profile the resource usage, identify the actual bottleneck, and batch accordingly.

**Likely follow-ups:**
- *"How did you validate that safety compliance wasn't broken by the new build order?"* — Every build, regardless of scheduling order, produces the same artifacts and runs the same safety test suite. The scheduling only changes when things run, not what runs. I verified this by comparing the binary outputs byte-for-byte between sequential and parallel builds for the first two weeks. Identical outputs, just faster.
- *"How did you handle flaky builds?"* — Flaky builds in an embedded context are usually environment contamination — one build target leaving state that affects the next. Docker container isolation per target eliminated that entirely. Each target gets a clean filesystem. If a build failed, it was a real failure, not a ghost from the previous run.
- *"What happens when a new build target is added?"* — The developer adds a resource profile (peak memory, estimated duration) to the config. If they don't know, the first build runs with monitoring and records the actual usage. The scheduler uses that for all subsequent runs. We also added a validation step: if a target exceeds its declared budget by more than 20%, the build fails with a clear message to update the profile.
- *"Why not use distributed compilation (distcc/Incredibuild)?"* — Distributed compilation helps the compile phase, but our bottleneck was the link phase — which is inherently single-machine. Distributing compilation across more machines would have shaved maybe 2 minutes off a 40-minute build. Smart scheduling of the link phase saved 25 minutes. We attacked the bottleneck, not the part that was already fast enough.

> **TR:** Her şeyi aynı anda çalıştırınca sunucu belleği taştı. Her hedefin tepe bellek kullanımını ölçtüm, ağır olanları sıraya koydum, değişmeyenleri atladım. 40 dakikadan 15'e, QA döngüsü %30 kısaldı.

---

# PRINCIPLE 3: Invent, Simplify & Frugal

> *"Share how you've removed complexity or optimized resources to achieve more with less."*

---

## Story A: Docker Image Optimization — Combination AB

**Situation (Define):** Docker images for .NET 9 microservices were 800MB+. Build times were 10 minutes. CI pipeline slow, developers waiting, registry storage costs climbing. Before cleanup rules, the container registry storage tripled in 3 months — nobody was deleting old images.

**Task (Reduce):** Reduce image size, cut build time via caching, standardize across 60+ services, and control registry growth.

**Action (Implement):**

```
╔════════════ BEFORE (single-stage) ═════════════════╗
║                                                    ║
║  ┌──────────────────────────────────┐              ║
║  │      FROM dotnet-sdk:9 (500MB)   │              ║
║  │  ┌────────────────────────────┐  │              ║
║  │  │ compilers, build tools,    │  │ ⚡ all this   ║
║  │  │ SDK, NuGet cache           │  │   ships to   ║
║  │  │ + app source + output      │  │   prod       ║
║  │  └────────────────────────────┘  │              ║
║  │            = 800MB               │              ║
║  └──────────────────────────────────┘              ║
╚════════════════════════════════════════════════════╝

╔════════════ AFTER (multi-stage) ═══════════════════╗
║                                                    ║
║  Stage 1 — BUILDER         Stage 2 — RUNTIME       ║
║  ┌────────────────────┐    ┌────────────────────┐  ║
║  │ FROM dotnet-sdk:9  │    │ FROM dotnet-aspnet  │  ║
║  │                    │    │      :9             │  ║
║  │ COPY *.csproj      │    │                    │  ║
║  │ RUN dotnet restore │    │ COPY --from=       │  ║
║  │ COPY .             │    │   builder /out .   │  ║
║  │ RUN dotnet build   │    │                    │  ║
║  │         ─ ─ ─ ─ output only ─ ─▶ = 80MB ✅   │  ║
║  └────────────────────┘    └────────────────────┘  ║
║  (discarded after build)   (this ships to prod)    ║
║                                                    ║
║  ┌────────────────────────────────────────────┐    ║
║  │ LAYER CACHE ORDER (key to 2-min builds):   │    ║
║  │                                            │    ║
║  │ 1. COPY *.csproj + restore  ← cached       │    ║
║  │    (slow step, deps rarely change)         │    ║
║  │                                            │    ║
║  │ 2. COPY . + build           ← rebuilt      │    ║
║  │    (fast step, code changes every commit)  │    ║
║  └────────────────────────────────────────────┘    ║
╚════════════════════════════════════════════════════╝
```

*The bloat fix — "don't ship the factory with the product":* When you build software, you need the full toolchain — compilers, build tools, SDKs. When you run it, you only need the compiled output. The images were 800MB because they were including all the build tooling that had no purpose in production. Like shipping a car to market with all the manufacturing equipment still inside it. I restructured the build so the heavy compilation step happens in a temporary environment, the output gets extracted, and only that output goes into a minimal image that has just enough to run.

*The caching fix — "put the slow stuff first, the fast stuff last":* Docker builds in layers. Once a layer is built, it's cached — if nothing in that layer changed, the build skips it. External dependencies are downloaded once and rarely change. Application code changes on every commit. By putting dependencies first and code last, the build system caches the slow part and only rebuilds the fast part. I standardized this pattern across all 60+ services with a shared template and set up automatic cleanup so old images in the registry didn't accumulate indefinitely.

**Result (Validate + Evolve):** 800MB down to 80MB. Build time from 10 minutes to 2 minutes. Registry costs stabilized.

**Tradeoffs, risks & alternatives:** There are even smaller base images available, but they use a different underlying C library than what .NET is built against, which can cause subtle runtime failures that are hard to debug. The official runtime image was small enough that the extra reduction wasn't worth the compatibility risk. The shared template is a single point of failure — a bug in it would affect all 60+ services at once. I mitigated that by versioning the template and validating it in a pipeline before rolling it out. The automatic cleanup means very old image versions require a rebuild to roll back to, but in practice rollbacks that far back never happened.

**Lesson:** Most Docker bloat comes from including the SDK in the runtime image and bad COPY order that invalidates the cache. It's a 30-minute fix per service that pays off permanently.

**Likely follow-ups:**
- *"How do you debug issues in a minimal runtime image that has no SDK?"* — Two approaches. For most issues, structured logging and distributed tracing give you enough context without needing to attach a debugger. For the rare cases that need interactive debugging, I have a debug variant of the Dockerfile that adds diagnostic tools — it's never deployed to production, only used in staging or locally. The production image stays minimal.
- *"How did you roll out the shared template to 60+ services?"* — Gradually. I migrated the 3 most-deployed services first, validated build times and image sizes, then announced it to the team with the numbers. Most teams adopted voluntarily because the results were obvious. For the remaining holdouts, I created a migration script that converted their Dockerfiles automatically. Total rollout took about 3 weeks.
- *"What about security scanning of base images?"* — The pipeline scans every image for known vulnerabilities before it leaves the build stage. We pin base image versions (e.g., `dotnet-aspnet:9.0.1`, not `:latest`) and update them monthly with a dedicated PR that runs the full test suite. An automated check alerts us if a pinned version has a new CVE.
- *"What if the shared template has a bug — doesn't that break all 60+ services?"* — Yes, that's the risk. I mitigated it by versioning the template. Services reference a specific version. A new template version is tested against 3 canary services before being promoted. Teams opt in to the upgrade explicitly — no one gets a surprise breaking change.

> **TR:** 800MB+ imajlar — derleyici üretimde boyuna taşınıyordu. Build ortamını runtime'dan ayırdım, katman sırasını önbellek için optimize ettim, tek şablon 60+ servise uyguladım. 80MB, 2 dakika build süresi.

---

## Story B: Ceremony Reform — KocSistem

**Situation (Define):** 25-person standups. Everyone gave a status update nobody listened to. 30 minutes every morning. Retros were complaint sessions — people vented, felt better, nothing changed. Two weeks later, same problems raised again.

**Task (Reduce):** Fix standups and retros separately. For standups: reduce to blockers only. For retros: add real accountability.

**Action (Implement):** Broke standups into team-level groups of 5-6 people. Focus on blockers only — if your update is "still working on the same thing," don't say it. 30 minutes became 8 minutes. People who wanted the big picture got a shared Slack channel for a one-line daily update.

For retros: added one rule — exactly 2 action items per retro, each with a specific person as owner and a specific deadline. Next retro starts by reviewing last retro's items. Didn't complete them? Talk about why before raising anything new.

**Result (Validate + Evolve):** Took three sprints to stick. By the third sprint, people saw problems actually getting fixed from retros. Started coming with concrete suggestions instead of vague complaints.

**Tradeoffs, risks & alternatives:** Smaller standups lose the "everybody knows everything" feeling. I accepted that — people who need the big picture read the Slack channel. A meeting that informs isn't worth its time cost; a meeting that unblocks is. Capping retros at 2 action items limits scope, but more items dilute ownership and nothing gets done. The risk of systemic issues being missed is handled by the "review last retro first" rule — recurring unresolved items naturally escalate.

**Lesson:** Ceremonies should produce outcomes, not compliance. A retro without follow-through is worse than no retro — it teaches people that raising issues is pointless.

**Likely follow-ups:**
- *"How did you get buy-in from people who liked the old format?"* — Some people liked the big standup because it was their only window into what other teams were doing. I addressed that with the shared Slack channel for one-line daily updates. The information was still available — just not blocking 24 other people for 30 minutes to deliver it.
- *"How do you know the ceremonies are actually working?"* — Two signals. First, sprint predictability: are we completing what we committed to? That went up. Second, retro action completion rate: are items getting done between retros? Before the change it was near zero. After, it was above 80%. If action items aren't getting done, the ceremony is broken regardless of how people feel about it.
- *"What do you do when a retro surfaces a systemic issue that can't be fixed in one sprint?"* — Break it into a sprint-sized first step. "Our deployment process is broken" is too big. "Add a smoke test to the staging deploy" is one sprint. The systemic issue stays on the radar through the "review last retro" rule — if the first step didn't help, it comes back naturally.
- *"25 people in one standup — how did that happen in the first place?"* — Organic growth. Started as one team, grew to multiple teams, nobody split the ceremonies. Nobody questioned it because "that's how we've always done it." It's a common pattern — ceremonies that worked at team size 6 don't work at 25, but nobody notices the gradual decay.

> **TR:** 25 kişilik standup kimse dinlemiyordu, retrolarda hiçbir şey değişmiyordu. 5-6 kişilik gruplara böldüm, sadece engel odaklı. Retro: 2 aksiyon, sahibi ve tarihi olan; bir sonraki retro öncekini gözden geçirerek başlar. 30 dakika → 8 dakika.

---

## Story C: Monitoring POC — KocSistem

**Situation (Define):** I was hired as a backend developer. The team had zero production visibility. Something broke, we got vague reports ("it's slow"), and spent 3 hours digging through logs manually. Nobody asked me to fix this — it wasn't in my job description.

**Task (Reduce):** Learn monitoring tools, build a minimal POC, show value to get approval, then make it routine.

**Action (Implement):** Learned monitoring tools on my own time and built a proof of concept — a set of dashboards that pulled live metrics from our services and displayed them in one place. Rather than trying to measure everything, I started with three signals per service: how many requests per second it's handling, what percentage of those are failing, and how long they take. Those three numbers tell you most of what you need to know about whether a service is healthy. I added infrastructure-level metrics — how busy the servers are, how much headroom is left — in the second iteration once the core was working.

Showed the prototype to my lead: "Here's what our services look like right now." Got approval to deploy it properly. Set up alerts that would post to the team's Slack channel when something crossed a threshold. Made it part of the daily rhythm — the first 30 seconds of standup, I'd mention what the dashboard showed overnight. By the third time someone caught an issue early because they'd looked at the dashboard themselves, the habit had formed.

**Result (Validate + Evolve):** Detection went from hours to minutes. Within weeks, catching issues before users reported them. Became standard for every service. This initiative led to my promotion to Dev Lead.

**Tradeoffs, risks & alternatives:** I could have pushed for a commercial APM from the start, which would have been more capable out of the box. But Prometheus and Grafana were free, the team had nothing, and starting with something is more important than starting with the perfect tool. A commercial tool without team buy-in would have been ignored. The risk of building on my own time was that the work might never get formalized. I mitigated that by showing the POC and getting official support before going further.

**Lesson:** Filling gaps nobody assigned is how you move from IC to leadership. Ship things that aren't your job, done well, and the recognition follows.

**Likely follow-ups:**
- *"How did you decide on alerting thresholds without historical data?"* — I started with industry defaults: error rate above 1%, latency above 2x the p50, traffic drop above 30% from the rolling average. Then tuned based on what actually triggered. The first week had false positives — I adjusted thresholds daily until the signal-to-noise ratio was useful. The goal was zero false positives per day, not zero alerts.
- *"How did you scale this to more services?"* — The three core metrics (request rate, error rate, latency) used a shared dashboard template. Adding a new service meant pointing the template at a new data source — about 10 minutes of config. Infrastructure metrics (CPU, memory, disk) came from a standard agent running on every server. The total effort to onboard a new service was under 30 minutes.
- *"What about log aggregation — dashboards alone don't tell the whole story?"* — Correct. Dashboards tell you something is wrong, logs tell you why. In the second iteration I added centralized logging with structured fields (service name, correlation ID, severity). The workflow became: dashboard alerts → click through to logs for that service and time window → find the root cause. Without that link, you're still guessing.
- *"Wasn't this a risk to your regular work — spending time on something nobody asked for?"* — Yes. I did the initial learning and POC outside work hours to avoid impacting my sprint commitments. Once I had a working prototype, I showed it to my lead and got official time allocated. The key was proving value before asking for permission — not the reverse.

> **TR:** Kimse istemeden, kendi zamanımda araçları öğrendim ve POC yaptım. İstek sayısı, hata oranı, yanıt süresi — 3 sinyal her şeyin %80'ini kapsar. Alışkanlık haline getirdim. Saatlerden dakikalara indi, bu girişim liderliğe terfi getirdi.

---

## Story D: Meeting Audit — KocSistem

**Situation (Define):** Too many meetings, no outcomes. Agile theater — going through the motions without the benefits. Standups, retros, planning, reviews all existed. Nothing was improving.

**Task (Reduce):** Apply one test to every meeting: "What decision did this meeting produce?" If the answer was "none," fix it or cancel it.

**Action (Implement):** Cancelled a weekly "team sync" that was basically a longer standup. Nobody missed it. Nothing bad happened. People got time back to actually work. Applied the same filter to sprint reviews: made them live demos with working software. Stakeholders could click, ask questions, give feedback. When they saw their feedback changing the product, they started attending regularly.

**Result (Validate + Evolve):** Fewer meetings, every surviving meeting produced a decision. Team had more time to code. Stakeholders engaged more because reviews were worth attending.

**Tradeoffs, risks & alternatives:** Cancelling meetings risks losing informal coordination. I mitigated that by keeping async channels active and ensuring the smaller, focused meetings still happened. Live demos require working software every sprint, which is a constraint — if a sprint produced nothing demo-able, the review falls flat. I addressed this by breaking stories into smaller, independently demo-able increments.

**Lesson:** If a review is boring, the format is the problem, not the audience. Show working software, not slides.

**Likely follow-ups:**
- *"What if someone disagreed with cancelling a meeting they valued?"* — I didn't cancel meetings unilaterally. I proposed: "Let's skip this one for two weeks. If anyone misses it, we bring it back." Nobody missed the weekly sync. For meetings people did value, I asked what specifically they got from it, then found a way to deliver that value in less time or asynchronously.
- *"How do you prevent meetings from creeping back?"* — A quarterly audit. Every recurring meeting gets the same test: "What decision did this produce in the last month?" If the answer is "none" for two consecutive months, it's a candidate for cancellation. The audit itself takes 15 minutes — just review the calendar with the team.
- *"Doesn't cancelling meetings hurt cross-team visibility?"* — It can. I compensated with written async updates — a Slack channel where each team posts a 2-line weekly summary. Teams that need to coordinate can read it in 2 minutes. The people who genuinely needed cross-team context were maybe 3-4 out of 25 — they shouldn't hold the other 21 hostage for that.

> **TR:** Toplantılar karar üretmiyordu. "Bu toplantı ne karar üretti?" testini uyguladım, üretemeyenleri iptal ettim. Review'ları canlı demoya çevirdim. Her hayatta kalan toplantı artık bir karar üretiyor.

---

# PRINCIPLE 4: Standards & Delivery

> *"Highlight your commitment to high-quality code, testing, and meeting deadlines despite setbacks."*

---

## Story A: Building CI/CD From Zero — KocSistem

**Situation (Define):** When I joined as Dev Lead, there was nothing. No CI/CD, no code review, no branching strategy. Developers built locally, copied files to servers. No visibility into what was deployed where. Something broke, you spent hours guessing. Weekly releases at best, sometimes biweekly. Every release was a gamble.

**Task (Reduce):** I broke the transformation into: build pipeline templates, add infrastructure as code, add observability, embed security scanning, measure with DORA metrics, and document everything.

```
╔═══════════════════ BEFORE ═════════════════════════╗
║                                                    ║
║  ┌─────┐   ┌────────┐   ┌───────────┐   ┌──────┐ ║
║  │ Dev │──▶│ Build  │──▶│Copy files │──▶│ hope │ ║
║  │     │   │locally │   │to server  │   │      │ ║
║  └─────┘   └────────┘   └───────────┘   └──────┘ ║
║                                                    ║
║  ⚡ weekly  ⚡ 2-3h manual steps  ⚡ 30% rollback    ║
╚════════════════════════════════════════════════════╝

╔═══════════════════ AFTER ══════════════════════════╗
║                                                    ║
║  ┌────────┐   ┌──────────────┐   ┌─────────────┐  ║
║  │ commit │──▶│ build + test │──▶│  security   │  ║
║  └────────┘   │ (unit tests) │   │  scan       │  ║
║               └──────────────┘   └──────┬──────┘  ║
║                                         │         ║
║                                         ▼         ║
║               ┌──────────────┐   ┌─────────────┐  ║
║               │ integration  │──▶│  package    │  ║
║               │ tests        │   │  artifact   │  ║
║               └──────────────┘   └──────┬──────┘  ║
║                                         │         ║
║  ┌──────────────────────────────────────┼───────┐ ║
║  │ SAME artifact promotes through:      │       │ ║
║  │                                      ▼       │ ║
║  │  ┌────────┐   ┌─────────┐   ┌────────────┐  │ ║
║  │  │  test  │──▶│ staging │──▶│ manual GATE│  │ ║
║  │  └────────┘   └─────────┘   └─────┬──────┘  │ ║
║  │                                    ▼         │ ║
║  │                             ┌────────────┐   │ ║
║  │                             │    prod    │   │ ║
║  │                             └────────────┘   │ ║
║  └──────────────────────────────────────────────┘ ║
║                                                    ║
║  ┌────────────────────────────────────────────┐    ║
║  │ DORA METRICS (tracked per deploy):         │    ║
║  │ freq | lead time | failure rate | MTTR     │    ║
║  └────────────────────────────────────────────┘    ║
╚════════════════════════════════════════════════════╝
```

**Action (Implement):** I built a shared library of pipeline building blocks — steps like "build and test," "package into a deployable image," "deploy to this environment" — all parameterized so any project could reference them in a few lines instead of writing everything from scratch. Every project's pipeline became essentially a configuration file that said "use these blocks, with these settings."

Infrastructure was defined as code rather than configured manually through a web console — meaning the state of the infrastructure was versioned, reviewable, and reproducible. Security scanning was embedded into every build automatically: checking dependencies for known vulnerabilities, scanning for hardcoded secrets, running static analysis. I added it once to the shared building blocks and it applied everywhere.

I measured delivery health with four numbers: how often we deployed, how long from a commit to it being in production, how often a deployment caused an incident, and how fast we recovered when it did. Those four metrics became the single source of truth for improvement conversations. Each deployment followed a promotion path — the same packaged artifact moved through test environments to production, with manual approval as the gate before anything reached customers. Wrote runbooks people actually used.

Change management: didn't change everything at once. Started with the most painful application, built the pipeline, showed it works, moved to the next. When skeptics pushed back ("you'll break production more often"), I showed data that most incidents came from big risky weekly releases, not frequent small ones.

**Result (Validate + Evolve):** Weekly to daily deployments — a 7x improvement. Fewer rollbacks. Cloud migration completed with zero downtime and zero incidents. Mean time to detect went from hours to minutes. Zero penetration test findings for three consecutive quarters. What lasted after I left: the shared pipeline library, infrastructure-as-code setup, delivery health dashboards, security scanning, and documented runbooks. Multiple people could maintain it.

**Tradeoffs, risks & alternatives:** A shared template repo is efficient but it's a single point of failure — a bad template update breaks every pipeline simultaneously. I mitigated this by versioning templates and running validation against them before rollout. Starting with the most painful application built credibility, but it also meant the first pipeline was under the most scrutiny. If it had issues, skeptics would have used it as evidence against the whole approach. I accepted that risk because the pain was visible enough that even a bumpy first attempt would be better than the status quo.

DORA metrics as proof worked well, but deployment frequency alone can be gamed by deploying empty changes. I tracked change failure rate alongside frequency so the metrics couldn't be inflated without showing the cost.

**Lesson:** The hardest part is cultural, not technical. Tools are easy. Getting people to trust automation over manual work takes data, patience, and going first.

**Likely follow-ups:**
- *"How did you handle resistance from developers used to manual deployments?"* — Two types of resistance. The "I don't trust it" crowd: I showed them the pipeline, walked through every step, and let them run it themselves in staging. Transparency builds trust. The "it's extra work" crowd: I made the pipeline the default path — the manual way was still possible but required more effort than the automated one. People take the path of least resistance.
- *"What was the rollback strategy?"* — Same artifact, previous version. Every deployment tagged the exact artifact version. Rolling back meant re-deploying the previous tag — same pipeline, same process, just a different version number. Under 5 minutes. Critically, the rollback process was tested regularly, not just documented. A rollback you've never practiced is a rollback that fails when you need it.
- *"How did you ensure security scanning didn't slow developers down?"* — Scans ran in parallel with tests, not sequentially. A dependency vulnerability scan takes 30 seconds — it doesn't add to the build time if it runs alongside the test suite. For false positives, I maintained a suppression list with documented justifications. Developers could suppress a finding with a reason, and the list was reviewed monthly.
- *"What happened when you left — did it survive?"* — Yes. That was by design. The shared pipeline library, infrastructure-as-code setup, and DORA dashboards were all owned by the team, not by me. Multiple people could maintain them. I documented the "why" behind decisions, not just the "how." When I left, nobody needed to reverse-engineer my choices.
- *"How did you pick the first application to migrate?"* — Most deployment pain. I asked the team: "Which app do you dread deploying?" Everyone named the same one. Starting with the most painful application meant the first success was the most visible. If I'd started with a low-risk app, the improvement wouldn't have been dramatic enough to convince skeptics.

> **TR:** Sıfırdan pipeline kurdum. 4 DORA metriği, paylaşımlı pipeline blokları, artifact bazlı ortam promosyonu, altyapı kod olarak. En acı çeken uygulamadan başladım. Deployment 7x arttı, 3 çeyrek boyunca sıfır pen-test bulgusu.

---

## Story B: Safety-Critical Definition of Done — Toyota

**Situation (Define):** Autonomous forklifts. A missed test isn't a bug report — it's a potential collision on the warehouse floor. Sprint discipline had to be non-negotiable, but the existing Definition of Done was vague. Developers would say "it's done, just needs sign-off" and push to the next sprint.

**Task (Reduce):** Define a strict DoD, automate mechanical checks, keep human review for what requires judgment, and make the overhead acceptable.

**Action (Implement):** Created a strict Definition of Done: code reviewed, all tests passing, integration tests simulating fleet scenarios, test report generated and archived, documentation updated, safety review checklist signed. Pushed back every time someone tried to skip: "Story isn't done until DoD is met. If it's too expensive, we automate parts or reduce scope. We don't pretend the checklist doesn't exist."

Automated mechanical checks: test execution, report generation, coverage thresholds — all checked by the pipeline. What remained manual was genuinely valuable: design review and risk assessment — things requiring human judgment. Made the manual part a short form of about 30 minutes instead of a full-day process.

**Result (Validate + Evolve):** Initially made sprints slower — developers finished code in 3 days, checklist and reports took 2 more. Team was frustrated. But after a few sprints with zero defects escaping to production, the overhead dropped from 2 extra days to half a day per story through automation. Zero safety incidents from our team.

**Tradeoffs, risks & alternatives:** The trade-off is clear: a strict DoD slows sprint velocity in the short term. In a safety-critical context, the cost of a missed defect — a forklift collision — far outweighs the cost of slower sprints. The key is that "strict DoD" doesn't mean "manual DoD." Everything that can be automated should be, so that the human review that remains is focused on judgment calls, not mechanical checks. The team frustration was real and expected — I addressed it by showing the zero-defect results, which made the overhead feel justified rather than arbitrary.

**Lesson:** In safety-critical environments, shipping fewer features cleanly is better than more features with risk. Automate everything you can so the human review that remains is focused and valuable.

**Likely follow-ups:**
- *"How did you handle pushback from developers who saw the DoD as bureaucracy?"* — I didn't argue about the principle — I showed the cost of failure. "If a forklift collides because we skipped a test, that's not a bug report, it's a safety incident." Once the team saw zero defects escaping for several sprints, the frustration faded. The overhead stopped feeling arbitrary when the results were undeniable.
- *"What did you do when a developer tried to skip the DoD under time pressure?"* — Pushed back every time. "The story isn't done until DoD is met. If we can't finish it this sprint, it moves. We don't pretend the checklist doesn't exist." I also offered an alternative: if the DoD feels too expensive, let's look at what we can automate to make it cheaper — not what we can skip.
- *"How did you balance velocity pressure from management with safety?"* — I framed it as risk management, not speed vs. safety. "We can ship faster by skipping safety checks. The expected cost of a forklift collision is X. Are we comfortable with that bet?" When the math is explicit, nobody chooses speed. I also showed that automating the DoD actually increased velocity after the initial investment.
- *"How is this different from what Eliq might need in energy systems?"* — Same principle, different domain. Energy systems have similar safety considerations — a miscalibrated meter or a failed grid integration isn't just a bug, it has real-world consequences. The approach transfers: strict quality gates, automated checks for the mechanical parts, human judgment for the complex parts, and never compromising on the checklist under time pressure.

> **TR:** Otonom forklift — bir kaçan hata çarpışma demek. "DoD'a uymayan hikaye bitmemiştir" dedim, istisna yapmadım. Mekanik olanı otomatize ettim, insan kararı gerektireni manuel tuttum. 2 günden yarım güne indi, sıfır güvenlik olayı.

---

## Story C: Automated Compliance at Volvo Cars

**Situation (Define):** Embedded automotive software. ISO 26262 functional safety, ASPICE process assessment. Regulatory requirements: documented verification at each stage, traceability from requirement to test to code. Compliance documentation was manual, slowing everything down. It felt like you couldn't ship fast and comply at the same time.

**Task (Reduce):** The key insight was that regulatory teams don't care how the docs are produced, only that they're accurate and complete. So: automate document generation from pipeline data, prove accuracy against manual, and get regulatory team buy-in.

**Action (Implement):** Built compliance automation into the release pipeline. Test reports were generated automatically from the actual test results — not written by hand after the fact. For traceability, the pipeline reconstructed the chain from requirement to code change to test: it read the history of changes since the last release, linked each change to its ticket, and assembled a complete map showing which requirement was covered by which test, through which code change. Release notes were generated from the merge history.

Machine-generated docs were more complete than manual ones — humans miss things. Ran both manual and automated in parallel for two releases to prove accuracy. Side-by-side comparison showed automated was more complete and more consistent. Regulatory team agreed to switch.

**Result (Validate + Evolve):** Regulatory team got better docs. Dev team shipped faster. 18 months, zero compliance findings.

**Tradeoffs, risks & alternatives:** The parallel run cost double the compliance work for two releases. That was the price of undeniable proof — regulatory teams trust evidence, not promises. Automated traceability depends on clean commit messages and ticket linking; garbage in, garbage out. I mitigated this by adding pipeline validation that rejects commits without ticket references. The initial investment to build the automation was significant, but after that every release got accurate compliance docs without developer overhead.

**Lesson:** Convince stakeholders with evidence, not arguments. Running in parallel was the key — they could see the quality was equal or better. Trust comes from proof.

**Likely follow-ups:**
- *"What happens when the automated docs have errors?"* — They're generated from the actual pipeline data, so an "error" in the docs means an error in the process — a missing test, an unlinked ticket. That's actually the value: the automation surfaces process gaps that manual docs would have papered over. When we did find formatting issues, we fixed the template once and every subsequent release was correct.
- *"How did you get the regulatory team to trust automated output?"* — The parallel run for two releases was key. They compared manual and automated side-by-side. The automated version was more complete — it caught traceability links that manual authors had missed. After that, their question flipped from "can we trust this?" to "why were we ever doing this by hand?"
- *"What if commit messages are garbage — doesn't the whole chain break?"* — Yes, garbage in, garbage out. That's why the pipeline rejects commits without ticket references. It's a hard gate, not a suggestion. Developers complained for the first week, then it became muscle memory. The discipline cost is low; the downstream value (automatic traceability) is high.
- *"How would you apply this to a non-automotive regulated environment?"* — The principle is universal: automate the chain from requirement to evidence. The specific regulations differ (ISO 26262 vs. GDPR vs. energy regulations), but the approach is the same — pipeline generates the proof, humans review the judgment calls. Eliq's energy domain likely has regulatory requirements around meter accuracy and grid compliance. Same pattern applies.

> **TR:** Yönetmelik ekipleri nasıl üretildiğini önemsemez, doğru ve eksiksiz olmasını ister. Pipeline gereksinim → kod → test zincirini otomatik kurdu. 2 release paralel çalıştırıp kanıtladım. 18 ay boyunca sıfır uyum bulgusu.

---

## Story D: First-Year Roadmap — KocSistem (Technology Manager)

**Situation (Define):** First year as Technology Manager, 25 engineers. Ambitious roadmap: DevSecOps adoption, Agile maturity improvement, release frequency, security posture.

**Task (Reduce):** Connected every goal to the pain the team felt. "Implement DevSecOps metrics" is abstract. "Measure time from commit to production and find the bottleneck" is something people care about. Every roadmap item framed as "make life easier," not "leadership wants a number."

**Action (Implement):** Used quarterly OKRs: 3-4 objectives, each with 2-3 measurable key results. Example: "Improve release reliability" with key results of change failure rate below 15%, MTTR under 1 hour, and zero pen-test findings. Tracked monthly, adjusted quarterly.

Security improvement: embedded scanning in CI/CD — dependency checks, static analysis, secret detection. Caught issues at build time, not quarterly pen-test time. Agile maturity tracked with a model across dimensions: sprint predictability, stakeholder visibility, team autonomy, continuous improvement. Tracked quarterly with the team as a conversation — "we're 3.1 here, what's blocking 3.5?" — not a report card.

Handling competing priorities: if something blocks daily work, it goes first. Strategic improvement can wait until next quarter. When stakeholders disagreed, I showed data: "This costs us 3 hours per week, that costs 30 minutes." Data resolves most priority debates.

**Result (Validate + Evolve):** All first-year targets hit. DevSecOps 75%. Agile maturity 3.1 to 3.7. Release frequency doubled. Zero pen-test findings.

> **TR:** Soyut hedefler yerine ekibin zaten hissettiği acılara bağlı OKR'lar kurdum. 3-4 hedef, her biri 2-3 ölçülebilir sonuçla, aylık takip. Agile olgunluğu 3.1'den 3.7'ye, deployment 2x, sıfır pen-test bulgusu.

**Tradeoffs, risks & alternatives:** OKRs can become performative if the key results aren't tied to real pain. I mitigated this by making sure every KR mapped to something the team already complained about. Agile maturity as a number risks being treated as a score to game rather than a reflection of real capability — I kept it as a team conversation rather than a management metric to avoid that. Embedding security in CI shifts findings left, which is good, but false positives slow developers. I spent time tuning rules and suppressing known false positives to keep the signal-to-noise ratio useful.

**Likely follow-ups:**
- *"How did you handle underperforming team members?"* — Direct conversation first — always 1:1, never public. "Here's what I'm seeing, here's the expectation, what's blocking you?" Most performance issues have a root cause: unclear expectations, wrong assignment, personal circumstances, or skill gaps. I matched the response to the cause. Unclear expectations: my fault, fix it. Wrong assignment: move them to work that matches their strengths. Skill gap: pair with someone strong, with a specific learning goal and timeline.
- *"How did you prioritize across 25 engineers and competing demands?"* — Everything mapped to the OKRs. If a request didn't connect to a key result, it waited. When two things connected to the same KR, the tiebreaker was: which one removes a blocker for more people? I made the priority list visible and reviewed it monthly with the team. Transparency prevents "why are we doing this?" conversations.
- *"How did you measure Agile maturity without it becoming a vanity metric?"* — I used it as a conversation starter, not a report card. The team and I would look at each dimension (predictability, autonomy, continuous improvement) and discuss: "We're at 3.1 here. What would 3.5 look like? What's stopping us?" The number was a tool for discussion, not a KPI for management. I never reported it upward as a score — only as "here's what we improved and why."
- *"How do you handle the tension between security scanning and developer velocity?"* — Tuning. Default security rules produce too many false positives. I spent the first two weeks reviewing every finding, suppressing known false positives with documented justifications, and configuring severity thresholds so only medium+ findings blocked the build. Low-severity findings were tracked but didn't break the pipeline. The goal is a useful signal, not a noisy one.

---

# PRINCIPLE 5: Earn Trust

> *"Be honest about past mistakes and what you learned. We value self-criticism over perfection."*

---

## Story A: RabbitMQ — What I Got Wrong (Toyota)

**Situation (Define):** We thought we understood RabbitMQ clustering. We'd read the docs. We had a 3-node cluster in production. But we never tested what happens when the cluster actually splits. Our test environment had all nodes on the same machine — no real network between them. When a real network blip happened, forklifts stopped.

**Task (Reduce):** After the incident: understand exactly what we missed, change testing practices, and change the team's approach to distributed systems.

**Action (Implement):** Added chaos testing to the sprint DoD for distributed components. Started asking "what are the failure modes of this system?" before any production deployment — if the team can't answer, we're not ready. Ran a workshop where we intentionally caused failures and practiced recovering. By the end, the team felt confident instead of scared. Familiarity with failure modes reduces fear. Wrote a blameless post-mortem focused on "what didn't we know?" and "what do we change?" — never "who screwed up?"

**Result (Validate + Evolve):** Chaos testing became standard. The team started reporting problems earlier because post-mortems were blameless. The mindset shift — from "does this work?" to "how does this break?" — was more valuable than the technical fix.

**Tradeoffs, risks & alternatives:** Blameless post-mortems carry the risk of avoiding accountability entirely — if nothing is ever anyone's fault, systemic problems don't get owned. I kept the focus on "what do we change?" which keeps it systemic without letting individuals off the hook for repeating the same mistake. Adding failure simulations to the build pipeline takes extra time on every build, and poorly designed simulations create noisy, unreliable tests. I mitigated this by making the failures deterministic — we'd always kill the same specific process, not introduce random chaos — so any test failure was consistently reproducible and easy to diagnose.

**Lesson:** This was humbling. We'd done the reading and thought we understood. Understanding only comes from testing failure, not from documentation.

**Likely follow-ups:**
- *"How did you run the blameless post-mortem in practice?"* — Three rules: no names in the timeline (say "the deploy step" not "Ali's deploy"), focus on "what did the system allow to happen?" not "who made the mistake," and end with exactly 3 action items with owners and deadlines. I facilitated the first few myself to set the tone. Once the team saw that honesty led to better systems instead of blame, they started volunteering information earlier.
- *"How did you get the team to adopt chaos testing — wasn't there resistance?"* — Yes, initially. "We're going to break things on purpose" sounds scary. I started with a workshop — we deliberately caused failures in a safe environment and practiced recovering. By the end, people felt confident instead of scared. Familiarity with failure modes reduces fear. After that, adding chaos tests to the pipeline was a natural next step, not a scary one.
- *"What's the difference between this story and the Dive Deep RabbitMQ story?"* — The Dive Deep version focuses on the technical fix: what I changed and why. This version focuses on what I got wrong and how I changed the team's approach afterward. Same incident, different angle. Use the Dive Deep version for "tell me about a technical challenge" and this one for "tell me about a mistake."
- *"How do you prevent this kind of blind spot in a new domain you're unfamiliar with?"* — The question I added to our process: "What are the failure modes of this system?" If the team can't answer confidently, we're not ready for production. I also insist on test environments that model real conditions — same network topology, same timing characteristics. A test environment that's too clean gives false confidence.

> **TR:** Dokümanı okuduk ve anladığımızı sandık, anlamadık. Test ortamında gerçek ağ yoktu, bölünme davranışını hiç görmedik. Blameless post-mortem yaptık, chaos testi standart oldu. Ekip sorunları daha erken raporlamaya başladı.

---

## Story B: Deployment Freeze Conflict — KocSistem

**Situation (Define):** A senior developer wanted a monthly "deployment freeze" — no releases in the last week of each month. He'd been burned by a Friday outage years back. Genuinely worried. The team of 25 was split — some agreed, others thought it was holding them back.

**Task (Reduce):** Instead of deciding who was right, I reduced it to a data collection exercise. Track every deployment failure for 6 weeks. If the data shows a freeze would have prevented most incidents, implement it. If not, find what actually would help.

**Action (Implement):** I didn't overrule him — he was a respected senior developer. Pulling rank would have won the argument but lost his trust. Asked him to stay 15 minutes after the meeting and heard him out. His concerns came from real experience. Proposed the 6-week experiment. "Let's collect data and decide based on that" is hard to argue against — and I genuinely didn't know the outcome going in. If the data showed a freeze was needed, I would have implemented it.

After 6 weeks, the data was clear: most incidents came from config drift and missing tests — not the timing of releases. The problems were about what was in the release, not when it went out. Shared the data with him first, not the team, so he wouldn't feel called out publicly. Together we built a pre-deployment checklist and set up auto-rollback.

**Result (Validate + Evolve):** He became the strongest daily deployment advocate on the team. The pre-deployment checklist caught real issues. The relationship strengthened because the resolution was collaborative, not hierarchical.

**Tradeoffs, risks & alternatives:** The 6-week experiment delayed the decision by 6 weeks. If the situation had been more urgent, that delay would have been costly. The benefit was a data-driven outcome nobody could argue with — including me if I'd been wrong. Sharing the data privately with him first carried the risk of looking like secret dealing, which I mitigated by sharing the same data with the full team immediately after. Building the checklist together was slower than mandating one, but shared ownership meant higher compliance and he was genuinely invested in it working.

**Lesson:** Resolve conflicts with data and empathy, not authority. Respect the person's experience, propose a method both sides agree to, and let the evidence decide.

**Likely follow-ups:**
- *"What if the data had supported the freeze?"* — I would have implemented it. The experiment wasn't a trick to prove him wrong — I genuinely didn't know the outcome. If the data showed that Friday releases were significantly riskier, a freeze would have been the right call. The point was to make the decision based on evidence, not opinion.
- *"How did you handle the politics — some people might see this as you undermining a senior developer?"* — Sharing the data with him first, privately, was critical. He wasn't blindsided in front of the team. When we presented together, it was "we looked at the data and here's what we found," not "I proved him wrong." The collaborative framing turned a potential conflict into a shared discovery.
- *"How do you handle a similar conflict where the other person is your manager, not a peer?"* — Same approach: propose data collection. "I think X, you think Y, let's measure for N weeks and decide based on that." It's harder to say no to data than to say no to an opinion. If my manager still overrides after seeing the data, I document my concern and comply — but I've never had that happen. Data is compelling.
- *"What was the pre-deployment checklist you built together?"* — Five items: all tests passing, no unreviewed changes, config diff reviewed, rollback plan documented, and a designated person monitoring for the first 30 minutes. Simple, but it caught real issues — twice we found config mismatches during the checklist that would have caused outages. Building it together meant he owned it as much as I did.

> **TR:** Kıdemli geliştirici aylık dondurma istedi, gerçek bir deneyimden geliyordu. Rank çekmek yerine 6 haftalık veri önerisi yaptım. Veri gösterdi ki sorun zamanlama değil, release içeriğiydi. Artık en güçlü savunucu oldu.

---

## Story C: Production Line Emergency — Volvo Cars

**Situation (Define):** Bug in embedded software — intermittent on/off failures. Got called late in the evening. If not fixed, the production line would stop. Automotive production line stoppage costs enormous money per hour.

**Task (Reduce):** Reproduce reliably, isolate root cause, test fix safely, deploy incrementally, prevent recurrence.

**Action (Implement):** I drove to the facility instead of debugging remotely — embedded hardware bugs need physical access. The bug manifested under specific startup timing that our test environment didn't create. Brought one engineer.

First hour: focused on reproducing reliably. Found it only happened with specific startup timing — two components initializing in parallel, occasionally stepping on each other. Race condition. The fix: made startup deterministic — component A finishes before B starts.

Tested on a spare unit first for 30 minutes under triggering conditions. Stable. Then rolled out to production units one at a time, monitoring each. If any issues, could revert that unit. Production line never stopped.

After the fix: pushed to make test environments match production timing. Our tests had sequential component starts with fixed delays. Production ran parallel initialization based on hardware signals with variable timing. That gap is why we missed the race condition.

**Result (Validate + Evolve):** Fix deployed, production line saved. Test environments updated to model real timing conditions.

**Tradeoffs, risks & alternatives:** Driving to the facility took time we didn't have much of, but embedded debugging is often impossible without physical access. The bug was hardware-timing-dependent — remote debugging would have been guessing. Testing on a spare unit added 30 minutes to the resolution, but deploying an untested fix directly to a production line is reckless — the cost of a bad fix is worse than 30 minutes of testing. The incremental rollout (one unit at a time) slowed full deployment, but it meant any issue was contained and instantly reversible.

**Framework under pressure:** Reproduce reliably. Isolate root cause. Test fix safely. Monitor after deployment. Post-mortem: what do we change so we catch it earlier next time?

**Lesson:** High-pressure moments reveal whether you're systematic or panicking. Don't rush a fix into production — that usually makes things worse. And change the test environment afterward so the same surprise can't happen again.

**Likely follow-ups:**
- *"How did you communicate with stakeholders during the incident?"* — One person communicated outward (the production manager), one person worked the problem (me). I gave the production manager a status update every 15 minutes: "Reproducing — estimated 30 more minutes," then "Root cause found — testing fix — 20 minutes," then "Fix tested, rolling out unit by unit." Short, factual, no guessing. Stakeholders need confidence that progress is happening, not a technical explanation.
- *"What was the total timeline from call to fix?"* — Call at ~9 PM, arrived at the facility around 10 PM, first reliable reproduction by 10:45 PM, root cause identified by 11 PM, fix tested on spare unit by 11:30 PM, full rollout completed by midnight. About 3 hours total. The first hour was reproduction — the most important and most patience-testing phase.
- *"Why didn't you debug remotely first to save time?"* — Embedded systems often have hardware-timing-dependent behavior that you can't reproduce remotely. The bug only manifested with specific startup timing from physical hardware signals. Remote debugging would have been me guessing at timing parameters without being able to observe the actual hardware behavior. Driving there cost 45 minutes; guessing remotely could have cost hours.
- *"How do you stay calm under that kind of pressure?"* — Process. I follow a fixed sequence: reproduce → isolate → test fix → deploy incrementally → monitor. Having a framework means I don't have to think about what to do next — I just follow the steps. Panic comes from not knowing what to do. A repeatable process eliminates that. I also never deploy a fix I haven't tested on a non-production unit first, no matter how urgent. That rule has never cost me more than 30 minutes, and it's prevented at least one bad fix from making things worse.

> **TR:** Gece çağrı, embedded bug, üretim hattı durma noktasında. Fiziksel erişim şarttı, fabrikaya gittim. Paralel başlatmada race condition — deterministik yaptım. Yedek birimde test ettim, birer birer devreye aldım. Hat bir daha durmadı.

---

## Story D: Not Delegating Well — KocSistem

**Situation (Define):** After being promoted to Tech Lead, I kept doing what had made me a good IC — taking on the hard technical problems myself, reviewing everything personally, making the calls on decisions. I thought I was being responsible. In practice, I was the bottleneck.

**Task (Reduce):** The team was delivering more slowly than it should have been. A team member eventually told me directly: "You're doing things I should be doing, and I'm not growing because of it." That was the moment I had to look at my behavior honestly.

**Action (Implement):** The instinct to "just do it myself" is hard to break, especially when you know you're faster on a specific problem. But speed on a single task doesn't matter if it creates a dependency that slows everything else down. I started by identifying the decisions I was making that weren't architecturally significant — things the team could and should own. For those, I moved from "I'll decide" to "what do you think? Walk me through your reasoning." It was uncomfortable at first, slower in the short term.

I stopped reviewing every pull request in detail and set up a rotation where the team reviewed each other's code. My reviews became the exception rather than the default. For tasks I knew I could do faster, I deliberately handed them to others — not because I had spare time, but because the team needed the reps. The second or third time someone handles something, they're faster and don't need me.

I also started blocking morning time for architectural and strategic work, not firefighting and reviews. That forced me to actually let go, because if I didn't delegate, the tactical work didn't get done.

**Result (Validate + Evolve):** The team started moving faster. Code review became shared ownership instead of a queue waiting on me. The developer who gave the feedback became one of my strongest collaborators. The lesson stayed with me — I now ask myself regularly: "Am I the only person who can handle this, or am I just reluctant to let go?"

**Tradeoffs, risks & alternatives:** Delegating when you know you're faster is a real cost in the short term — output drops before it grows. The risk is that quality drops too, especially early. I mitigated that by staying available for questions and doing joint reviews when something was high stakes, rather than stepping in and taking it back. There's also the risk of delegating too much too fast, leaving people without enough support. I kept 1:1s focused on "what's blocking you?" so I could course-correct before things stalled.

**Lesson:** The skills that make a good IC don't automatically make a good lead. The hardest part of the transition isn't technical — it's learning that your value comes from growing the team's capacity, not from being the best individual contributor in the room.

**Likely follow-ups:**
- *"How do you know when to step in vs. let someone struggle?"* — Two signals. If they're stuck but learning — asking good questions, making progress even if slowly — I stay out. If they're stuck and spiraling — same problem for days, frustration increasing, no new approaches — I step in. But stepping in means pairing, not taking over. "Let me look at this with you" not "let me just do it."
- *"How did you handle the quality dip during the transition?"* — It was real. The first two weeks of delegated code reviews had more things slipping through. I did spot checks — reviewed some PRs after the team reviewed them, without blocking the merge. When I found gaps, I brought them up in 1:1s as learning opportunities, not corrections. After a month, the team's review quality matched mine. They needed the reps.
- *"What's the hardest thing to delegate as a technical leader?"* — Architecture decisions. When you've been the architect, every decision feels like it needs your input. I forced myself to only weigh in on decisions that were irreversible or had cross-team impact. Everything else, the team decided and I supported. The first time they made a choice I disagreed with and it worked out, I knew the delegation was working.
- *"How do you stay technical as a manager?"* — I reserve time for hands-on work: reviewing architecture decisions, reading code during PR reviews (not rubber-stamping), and occasionally picking up a small, well-scoped task. The trap is letting management tasks eat 100% of your time. If I stop reading code, I stop being able to evaluate technical decisions — and the team loses respect for my judgment.

> **TR:** Terfi sonrası IC alışkanlıklarımı taşıdım ve darboğaz oldum. Bir ekip üyesi doğrudan söyledi. "Ben karar veririm"den "sen ne düşünüyorsun?" moduna geçtim, review rotasyonu kurdum. Ekip daha hızlı ilerledi.

---

# KEY DECISIONS — Quick Reference

The reasoning behind the architectural calls across all stories, in plain terms.

**In-memory store over a dedicated message bus (GPS scaling, KocSistem):** The tool I chose — Redis — was already running in our infrastructure. A dedicated message bus would have been more powerful, but it would have meant new infrastructure to operate, new knowledge for the team, and more moving parts — for a problem that was already solvable with what we had. The rule I apply: don't introduce a new system when an existing one fits the constraints.

**Pause over automatic recovery during a network split (RabbitMQ, Toyota):** When the cluster's nodes lost sight of each other, the question was: what should the minority do? I chose "pause and wait" over "keep going and recover automatically later." Keeping going means the two sides diverge — when they reconnect, one side's messages get discarded to resolve the conflict. For forklift commands, a paused forklift is safe. A silently discarded command is not. Always ask: which failure mode is less dangerous?

**Majority-confirmed storage over replica replication (RabbitMQ, Toyota):** The older approach confirmed a message was received as soon as the main node had it, then copied it to backups in the background. If the main node died mid-copy, the message was gone. The approach I switched to waits for confirmation from more than half the nodes before telling the sender "you're good." Slower, but you know a message is durable once confirmed. Think of it like requiring multiple witnesses to a signature instead of just one.

**Single API entry point over one backend per client (GraphQL, Combination):** The alternative — a dedicated backend per client type — means each client gets exactly what it needs, but every new client requires a new backend, and any shared logic gets duplicated. The federation approach I used lets each service own its own data while a single gateway composes it for whoever's asking. The client asks one question, the gateway figures out which services to ask, and stitches the answer together.

**Gradual alongside over full replacement (GraphQL, Combination):** Rewriting all 60+ services at once to a new API style would have been faster to complete in theory, but one breaking change could affect dozens of clients simultaneously. Running the old and new in parallel let consumers migrate at their own pace, and we could stop at any point without having broken anything. The cost was a transition period where two API surfaces needed to be maintained.

**Use what you have over a dedicated managed service (infrastructure state, KocSistem):** Cloud storage with a locking mechanism costs nothing on top of what we already paid. The managed alternative adds a richer collaboration layer — approval workflows, cost tracking, audit logs — but that's worth its cost when multiple independent teams are making changes simultaneously. For our size, it was unnecessary.

**Four delivery health numbers as the proof of improvement (CI/CD, KocSistem):** Deployment frequency, time from commit to production, incident rate per deployment, and recovery time. These four tell you whether your delivery process is actually improving or just feeling better. Frequency alone is easy to fake — you can deploy empty changes all day. Pairing it with incident rate means you can't improve one number without the other holding up.

**Three signals before everything else (observability, KocSistem):** Request volume, error rate, and response time per service. Those three numbers catch most production problems. Starting with more makes dashboards nobody reads. The discipline is adding detail only when a specific problem demands it — not in advance.

---

# Cross-Cutting Questions — Likely in Open Discussion

> These don't map to a single story. They'll come naturally in a conversational loop interview. Have a crisp answer ready.

**"Walk me through your career — why each move?"**
KocSistem: Started as backend developer, grew into Dev Lead and then Technology Manager over 25 engineers. Moved because I wanted to work on more technically challenging, safety-critical systems. → Toyota: Embedded systems, autonomous forklifts, real distributed systems problems. Moved because I wanted to scale beyond embedded and work with modern cloud-native architectures. → Volvo Cars: Embedded automotive, safety-critical at massive scale, build systems and compliance automation. → Combination AB: .NET 9 microservices, GraphQL federation, Docker optimization — the full modern cloud stack. Each move added a layer: from pure backend → distributed systems → safety-critical → cloud-native architecture.

**"Why Eliq? Why now?"**
Three things align. First, the energy domain is a real problem that matters — not another ad-tech optimization. Second, the technical challenge: IoT devices, embedded systems, data pipelines, cloud backend — that's a combination I've specifically built experience across. Third, the team size and stage: I've built engineering culture from scratch at this scale before and I know what works.

**"What's your management philosophy?"**
Three principles. First, data over opinion — every significant decision should have a measurable outcome we can check. Second, ownership over compliance — I'd rather someone do the right thing because they believe in it than because I told them to. Third, transparency — the team should always know the why behind a decision, not just the what. I don't hide context or protect people from hard truths.

**"How do you stay technical as a manager?"**
I reserve time for architecture reviews, read code in PRs (not rubber-stamp), and occasionally take on a well-scoped technical task. The rule: if I can't credibly challenge a technical decision in a design review, I've drifted too far. I also build the first version of any new process (pipeline templates, monitoring, etc.) myself before asking the team to adopt it.

**"How do you handle a technically strong person who's difficult to work with?"**
Separate the behavior from the person. "Your code reviews are technically excellent, but three people have told me they dread getting feedback from you. The tone needs to change." Specific, factual, private. If the behavior continues after two conversations, it's a performance issue regardless of technical skill — a person who makes the team slower is net negative even if their individual output is high.

**"Tell me about a time you were wrong about something important."**
The RabbitMQ split-brain incident. We read the docs and thought we understood distributed messaging. We didn't. The test environment didn't model real network conditions. When a real partition happened, forklifts stopped. I changed three things: chaos testing became standard, "what are the failure modes?" became a required question before any production deployment, and I ran a blameless post-mortem that changed the team culture from "does this work?" to "how does this break?"

**"How do you make build-vs-buy decisions?"**
Three questions. Can we build it in under a week with what we already have? Is the maintenance burden manageable with our team size? Does building it give us a meaningful advantage over buying? If all three are yes, build. If any is no, buy (or use an open-source solution). I chose Redis over Kafka because Redis was already in our stack. I chose blob storage locking over Terraform Cloud because 3 people didn't need a managed service. I'd choose differently at a different scale.

**"How would you handle the first 90 days at Eliq?"**
First 30 days: listen and observe. Read the code, understand the architecture, attend every ceremony, meet every team member 1:1. Ask "what works well?" and "what frustrates you?" — not "here's what I'd change." Days 30-60: identify the biggest pain point the team already feels and propose one concrete improvement — small, measurable, reversible. Days 60-90: deliver that improvement, show results, and use the trust earned to propose the next one. I never change processes I don't yet understand.

**"What's your experience with IoT / embedded energy systems?"**
Direct: Toyota's autonomous forklift system (30+ microservices, real-time messaging for physical hardware), Volvo's embedded automotive software (safety-critical, multi-platform builds). Adjacent: GPS warehouse tracking (250 writes/second from hardware devices, real-time dashboards). I haven't worked specifically in energy metering, but the pattern — devices sending telemetry, backend processing and storing, dashboards and analytics — is the same architecture I've built three times.

**"How do you handle mid-sprint priority changes?"**
Same test as any new request: does this outrank something already committed? If yes, what gets bumped and who needs to know? I never add without removing. If leadership says "everything is P1," I ask: "If we can only deliver one of these this sprint, which one?" That forces real prioritization. Unplanned work is tracked separately so we can show how much it costs over time — visibility creates discipline.

**"What's a hill you'd die on?"**
Automated testing in the pipeline is non-negotiable. You can debate code style, architecture patterns, tooling choices — those are contextual. But shipping without automated tests is shipping with your eyes closed. Every team I've led, that's the first thing I establish and the last thing I'd compromise on.

---

# Questions to Ask Them

Pick 2-3 total per interview. Match to conversation tone and the interviewer's role.

**For anyone:**
- "What does the current architecture look like — monolith, microservices, or somewhere in between?"
- "What's the biggest technical debt right now?"
- "What does the deployment pipeline look like today?"
- "How do you handle observability and incident response?"

**If talking to Olof (CTO):**
- "How are technical decisions made — architect, team consensus, tech lead?"
- "What's the team's relationship with the product side?"
- "Where do you see the biggest engineering challenge in the next year?"

**If talking to Doug (Head of Embedded Energy):**
- "How are infrastructure changes managed — IaC, manual, hybrid?"
- "What does the embedded energy domain look like technically — protocols, devices, data flows?"
- "What's the current biggest bottleneck in the release cycle?"

**If talking to Vilius (Senior Engineering Manager):**
- "How is the engineering team organized — squads, chapters, functional?"
- "What does a typical week look like for this role?"
- "How do you balance moving fast with reliability?"
- "How do you handle mid-sprint priority changes?"

---

# Closing Line (memorize)

> "I write production backend code, I build the pipelines that ship it, I've led the teams that do both, and I've shaped the Agile processes that keep them aligned."

---

*[[Loop interview schema and schedule]]*
