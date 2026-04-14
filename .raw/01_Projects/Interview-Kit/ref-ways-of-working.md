---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Ways of Working — How I Plan, Work, and Measure Success

> [!tip] Behavioral and process questions: "How do you approach a new project?", "How do you prioritize?", "What does success look like?" These come up in every interview, usually from the hiring manager or team lead.

---

## Cheatsheet — Quick Scan

### My Core Principles
| Principle           | One-liner                                                                                          | Deep dive                                |
| ------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| **Problem-solving** | **DRIVE:** Define → Reduce → Implement → Validate → Evolve                                         | [[#The DRIVE Framework]]                 |
| **Planning**        | Understand why → break down → risk first → prototype risky parts → define done                     | [[#How I Plan]]                          |
| **Prioritizing**    | Blocking someone? → now. Production issue? → drop everything. High impact low effort? → next.      | [[#How I Prioritize]]                    |
| **Working style**   | IC: deep work mornings, async default. Lead: mornings code, afternoons people.                     | [[#How I Work Day-to-Day]]               |
| **Leadership**      | Lead by doing, measure with data, let results speak. No mandates.                                  | [[#How I Lead]]                          |
| **Stakeholders**    | Their language, not mine. Show working software, not slides. Trade-offs explicit.                  | [[#How I Communicate With Stakeholders]] |
| **Disagreements**   | Data first. Can't measure? Pilot for 2 sprints. Style? Defer to linter.                            | [[#How I Handle Disagreements]]          |
| **Failure**         | Own it. Blameless post-mortem. Fix the system, not the symptom.                                    | [[#How I Handle Failure]]                |
| **Success**         | Ships on time + tests pass + no incidents first week + team is growing                             | [[#What Success Looks Like]]             |
| **Growing others**  | 1:1s (they talk, I listen). Pair sessions (show thinking, not just mistakes). Stretch assignments. | [[#How I Grow Others]]                   |
| **Good team**       | Autonomy + accountability, data over opinions, sustainable pace, engineers own decisions.            | [[#What Makes a Good Team For Me]]       |

### What Makes a Good Team For Me

> [!tip] "What kind of team do you work best in?" / "What's your ideal work environment?"

A good team for me has these qualities:
- **Autonomy with accountability** — engineers own their decisions and their outcomes. No one asks permission for every PR, but everyone owns what they ship.
- **Data over opinions** — disagreements are settled with experiments, metrics, and evidence — not hierarchy or who talks loudest. At KocSistem, I [[ls-conflict|resolved a deployment freeze debate]] with a 6-week data experiment instead of arguing.
- **Sustainable pace** — quality comes from focus, not overtime. Deadline-driven cultures produce technical debt and burnout. The best teams I've been on shipped faster *because* they didn't rush.
- **Engineers talk to the problem** — I want access to the "why" behind features, not just Jira tickets. At KocSistem, [[ag-alignment|sprint goals]] worked because we understood the business context behind every story.
- **Continuous improvement is real** — retros produce actual changes, not just complaints. [[ag-accountability|Two action items per retro, each with an owner and a deadline, reviewed next retro.]]
- **Clean code is a shared value** — [[ref-code-review#HOW WE SET IT UP|code review]] is meaningful feedback, not rubber stamps. Formatting debates are for linters, reviews are for logic, security, and edge cases.
- **Learning is part of the job** — new tools and domains are expected. When I joined Volvo, I had [[ref-ways-of-working#Uncertainty — New Domain|zero embedded experience]] — I became sole pipeline owner in 2 months because the team gave me space to learn.

What I bring to that team: I take ownership before being asked, I measure before I argue, and I make the people around me better through pairing, reviews, and honest feedback.

### My Key Numbers
| Metric | Value | Where |
|--------|-------|-------|
| SLA breach reduction | **60%** | KocSistem |
| Bug rate reduction | **55%** | KocSistem |
| Release frequency | **2x** (weekly→daily) | KocSistem |
| Agile maturity | **3.1→3.7** | KocSistem |
| Pen-test findings | **Zero** (3 quarters) | KocSistem |
| QA cycle reduction | **30%** | Volvo |
| Compliance findings | **Zero** (all releases) | Volvo |
| Build time | **40→15 min** | Volvo |
| API response fix | **3s→200ms** | Combination |
| Docker images | **800→80MB** | Combination |
| Build caching fix | **10→2 min** | Combination |
| Dashboard fix | **frozen→sub-second** | KocSistem |
| Deployments per day | **multiple** (was weekly) | KocSistem |
| Team size led | **25 engineers** | KocSistem |
| Promotions | **2 in 4 years** | KocSistem |

### Story Quick-Pick
| They ask about... | Say this story | Backup |
|-------------------|---------------|--------|
| Conflict | [[ref-star-stories#Conflict — Deployment Freeze]] | [[ref-star-stories#Conflict — Skeptical Developer]] |
| Failure | [[ref-star-stories#Failure — RabbitMQ Split-Brain]] | [[ref-star-stories#Failure — Terraform State Corruption]] |
| Leadership | [[ref-star-stories#Leadership — CI/CD Pilot]] | [[ref-star-stories#Leadership — Quarter Planning]] |
| Hard problem | [[ref-star-stories#Problem-Solving — DevOps From Zero]] | [[ref-star-stories#Problem-Solving — GPS Scaling]] |
| Pressure | [[ref-star-stories#Pressure — Production Line]] | |
| Initiative | [[ref-star-stories#Initiative — Observability]] | [[ref-star-stories#Initiative — Cross-Team Testing]] |
| Difficult person | [[ref-star-stories#Collaboration — Third-Party Integration]] | |
| Adaptability | [[ref-star-stories#Adaptability — GraphQL Migration]] | [[ref-star-stories#Adaptability — Stepping Up as PO]] |
| Mentoring | [[ref-star-stories#Mentoring — Junior to Mid]] | |
| Feedback | [[ref-star-stories#Feedback — Code Review Culture]] | [[ref-star-stories#Receiving Feedback — Management Style]] |
| Prioritization | [[ref-star-stories#Prioritization — Roadmap Trade-offs]] | |
| Stakeholders | [[ref-star-stories#Stakeholders — Mid-Sprint Changes]] | |
| Cross-team | [[ref-star-stories#Cross-Team — Department Alignment]] | |
| Uncertainty | [[ref-star-stories#Uncertainty — New Domain]] | |
| Customer focus | [[ref-star-stories#Customer Focus — Client Adaptation]] | |
| Proudest | [[ref-star-stories#Proud — Full Transformation Arc at KocSistem]] | [[ref-star-stories#Proud — Monitoring POC That Changed Everything]] |
| Proudest technical | [[ref-star-stories#Proud — Zero Compliance Findings at Volvo]] | [[ref-star-stories#Proud — GraphQL Migration Without Breaking Anyone]] |

---

## The DRIVE Framework

> [!tip] Works for ANY question — technical, non-technical, system design, behavioral, debugging, architecture, people problems. Use when you're not sure how to start.

### **D**efine → **R**educe → **I**mplement → **V**alidate → **E**volve

**D — Define the problem.**
- Don't jump to solutions. Ask: what's the real problem? what's the context? who's affected? what does success look like?
- Technical: "The endpoint is slow" → slow for who? how slow? since when? what changed?
- Non-technical: "The team isn't delivering" → what's blocking? is it capacity, motivation, unclear requirements, or bad process?
- ← *At Volvo, the production line bug — I didn't debug remotely. I drove to the facility because I needed to understand the actual hardware conditions.*

**R — Reduce to small pieces.**
- Split the big problem into small, testable pieces. Each piece should be independently verifiable.
- Technical: "Migrate to GraphQL" → (1) pick one endpoint, (2) build resolver, (3) test with frontend, (4) measure, (5) expand
- Non-technical: "Improve team process" → (1) measure current pain, (2) fix standups, (3) fix retros, (4) add sprint goals, (5) measure again
- ← *At KocSistem, DevOps from zero — I didn't try to change everything at once. One app, one pipeline, prove it works, expand.*

**I — Implement the smallest useful thing first.**
- Start with what gives you the most information or the most impact. Don't plan forever.
- Technical: Build a POC/prototype for the riskiest part. If it works, you have confidence. If it doesn't, you've learned cheaply.
- Non-technical: Pilot with one team for 2 sprints. Low risk, clear exit criteria.
- ← *At KocSistem, monitoring POC — weekends, one dashboard, showed it to the lead. That single action started the entire transformation.*

**V — Validate with data.**
- Measure the outcome, not just the output. "We shipped it" is output. "Response time dropped from 3s to 200ms" is outcome.
- Technical: Check metrics, run tests, compare before/after. Don't declare victory based on feelings.
- Non-technical: Track the numbers — deployment frequency, bug rate, team satisfaction. Data beats opinions.
- ← *At KocSistem, DORA dashboards — I didn't just build CI/CD and hope. I measured deployment frequency, lead time, failure rate monthly.*

**E — Evolve from what you learned.**
- Every problem teaches something. Document it if it's worth sharing.
- Technical: blameless post-mortem after incidents. What did we not know? What should we change?
- Non-technical: retro action items after process changes. What worked? What didn't?
- ← *After the RabbitMQ split-brain at Toyota — post-mortem led to chaos testing. After Terraform state corruption — led to mandatory locking.*

### How to Use DRIVE in Interviews

**When asked a technical question you're not sure about:**
> "I'd DRIVE through this. First, **Define** — what are the constraints? Then **Reduce** to the key pieces. **Implement** — I'd start with the riskiest part as a prototype. **Validate** by measuring. **Evolve** — apply what I learned to the next iteration."

**When asked a behavioral question:**
> STAR maps to DRIVE: **S**ituation = **D**efine the problem. **T**ask = what needed to change. **A**ction = **R**educe + **I**mplement. **R**esult = **V**alidate + **E**volve.

**When asked "how would you design X?":**
> "Let me DRIVE this. **Define** — what are we optimizing for? **Reduce** — sketch the main components. **Implement** — for the riskiest part, I'd prototype or reference similar experience. **Validate** — measure success by [metric]. **Evolve** — here are the trade-offs and what I'd watch for."

**When you genuinely don't know:**
> "I haven't used that tool, but I'd DRIVE it: **Define** the problem it solves, **Reduce** to what I need to learn, **Implement** a small POC, **Validate** it works in our context, **Evolve** from there. That's how I learned embedded systems at Volvo — zero experience, productive in 2 months."

---

## How I Plan

**Starting a new feature/project:**
1. **Understand the why** — What problem are we solving? Who benefits? What does success look like? I ask stakeholders, not assume.
2. **Break it down** — Large tasks into small, deliverable pieces. Each piece should be demo-able. If a task takes more than 3 days, it's too big — break it further.
3. **Identify risks early** — What could go wrong? Dependencies on other teams? New technology I haven't used? Performance unknowns? I address these first, not last.
4. **Prototype the risky parts** — Build a POC for the uncertain parts before committing to a plan. At Combination, I built a GraphQL side project for a week before proposing the migration to the team.
5. **Define "done"** — Not just "code works" but: tests pass, code reviewed, deployed to staging, documentation updated, breaking changes communicated.

**Starting at a new company:**
- First 2 weeks: listen, read code, understand architecture. No big changes.
- First month: fix something small that annoys the team — a slow pipeline, a flaky test, a missing dashboard. Build trust through action.
- First quarter: propose one meaningful improvement based on what I've learned. Data-driven, not opinion-driven.
- ← *this is exactly what I did at KocSistem — built monitoring POC in the first months, led to promotion*

## How I Work Day-to-Day

**As an IC (Individual Contributor):**
- Morning: check dashboards (pipeline health, service metrics), review PRs, unblock anyone waiting on me.
- Core hours: deep work — feature development, debugging, architecture exploration. Minimize meetings.
- End of day: push code, update tickets, leave notes for tomorrow.
- ← *at Combination and Toyota, this is my daily rhythm*

**As a Tech Lead / Manager:**
- Morning: technical work (code, reviews, architecture). Protected block — no meetings before noon.
- Afternoon: people work (1:1s, planning, stakeholder sync, unblocking).
- ← *I learned this split at KocSistem — without protecting morning time, coding never happened*

**Communication style:**
- Default to async (Slack, PR comments, docs) unless it's urgent or complex.
- For complex discussions: 15-minute call > 10 emails.
- Status updates: show working software, not slide decks.
- ← *at KocSistem, I replaced status reports with live sprint demos — stakeholders stopped micromanaging*

## How I Prioritize

**Framework:**
1. **Is it blocking someone?** → Do it now. Unblocking a teammate for 30 minutes is worth more than 3 hours of my own coding.
2. **Is it a production issue?** → Drop everything. Fix it, then post-mortem.
3. **Is it high impact, low effort?** → Next in queue. Quick wins build momentum.
4. **Is it high impact, high effort?** → Plan it, break it down, schedule it.
5. **Is it low impact?** → Backlog. Maybe never.

**When everything is "urgent":**
- Ask: "If we could only do one thing this week, what would it be?"
- Make trade-offs explicit: "We can do X or Y, not both. Which matters more?"
- ← *this is how I handled mid-sprint priority changes at KocSistem — sprint goals forced the conversation*

## What Success Looks Like

**For a feature:**
- Ships on time (or we communicated early if it won't)
- Tests cover the important paths
- No incidents in the first week after deployment
- Users/stakeholders got what they needed, not just what they asked for

**For a team:**
- Deploys daily with confidence
- Bugs caught in review/CI, not in production
- Team members growing — juniors becoming mids, mids becoming seniors
- Ceremonies produce decisions, not just fill calendars
- ← *at KocSistem: SLA -60%, bugs -55%, 2x releases, Agile 3.1→3.7 — these were my success metrics*

**For myself:**
- I made the team better, not just shipped my own code
- I left things cleaner than I found them
- I said "I don't know" when I didn't, and went and learned it

## How I Handle Disagreements

- **Technical disagreements** — Data first. "Let's measure and decide" not "I think X is better." If we can't measure, try both for a sprint and compare. ← *the deployment freeze debate at KocSistem — 6-week experiment, data decided*
- **Process disagreements** — Pilot it. "Can we try this for 2 sprints and evaluate?" Low risk, clear exit criteria. ← *how I introduced CI/CD — volunteered our team for the pilot*
- **Priority disagreements** — Make trade-offs visible. "We can't do both. Which one moves the needle more?" With data, not opinions.

## How I Lead

**My leadership style:**
- Hands-on + data-driven. I don't tell people what to do — I show the data, propose a direction, and let results speak. If I'm wrong, the data shows that too. ← *at KocSistem, I presented deployment pain as "am I seeing this right?" not "here's what's wrong"*
- I lead by doing, not by delegating the hard stuff. When I proposed CI/CD at KocSistem, I volunteered our team, fixed flaky tests myself, and was online at 6 AM for the first deploys. The team saw me taking the risk first.
- I protect my team's time. If stakeholders want status updates, I give them demos of working software — not meetings where developers explain what they did this week.

**What I've led:**
- 25 engineers at KocSistem (Technology Manager) — technical roadmap, DevOps, security, architecture, Agile
- DevOps transformation from zero — weekly to daily deploys, org-wide in 6 months
- Cross-department coordination at Volvo — sole owner of the pipeline between 3+ departments
- Cross-team test framework at Toyota — built something for my team that other teams adopted

**How I make decisions:**
- Small decisions: just decide, move fast. If it's easily reversible, don't waste time debating.
- Medium decisions: discuss with the team, get input, decide within the day.
- Large decisions (architecture, technology choice): data + prototype + team buy-in. A week of investigation is worth it to avoid a year of regret.
- ← *the GraphQL migration was a large decision — I built a POC for a week, paired with a skeptic, proved the value, then scaled*

## How I Communicate With Stakeholders

**Translating technical to business:**
- Never say "we need to refactor the codebase." Say "right now, adding a feature takes 2 weeks because of technical debt. If we invest 3 sprints in cleanup, new features take 3 days."
- Frame everything in business impact: time saved, incidents prevented, revenue risk, customer experience.
- ← *at KocSistem, I showed leadership "we spend 40% of our time firefighting — here's a chart showing it decreasing after we added monitoring." They approved the investment immediately.*

**Talking to product owners / non-technical stakeholders:**
- Use their language, not yours. "The system will be faster" not "we're optimizing database queries with covering indexes."
- Show, don't tell. Live demos every sprint — when stakeholders see working software, they trust the team and stop micromanaging.
- Make trade-offs explicit. "We can ship feature A by Friday or feature A + B by next Wednesday. Which matters more?" They can't prioritize if they don't see the trade-off.
- ← *at KocSistem, I acted as Product Owner for the HR platform — I learned to bridge the gap between what stakeholders want and what's technically feasible*

**Talking to executives / leadership:**
- Numbers, not stories. "SLA breaches down 60%, release frequency doubled, zero security findings." That's what they care about.
- One slide, not ten. If you need 10 slides to make your point, your point isn't clear.
- Propose solutions, not problems. "Here's what's broken" is useless without "here's how I'd fix it and what it costs."
- ← *at KocSistem, my monthly DORA metrics report to leadership was 4 numbers and their trends. Charts going in the right direction ended every debate.*

**Managing expectations:**
- Communicate early, not late. If a deadline is going to slip, say it at 50% progress — not at 95%.
- Never promise what you can't deliver. Under-promise, over-deliver. If I think something takes 5 days, I say a week.
- When someone asks "is this possible?" — my answer is "yes, here are the trade-offs." Everything is possible; the question is what it costs.

**Handling difficult conversations:**
- With a senior developer who resists change: listen first, acknowledge their experience, propose a data-driven experiment. ← *deployment freeze debate — 6-week experiment, he became an advocate*
- With a defensive external partner: go in person, lead with questions not demands, build trust through consistency. ← *Toyota third-party integration — "help me understand what went wrong before"*
- With a manager who wants everything "urgent": make trade-offs explicit. "If everything is priority 1, nothing is. Which three things matter most this sprint?" ← *sprint goals at KocSistem solved this*

## How I Handle Failure

- **Own it** — "I made a mistake, here's what I learned, here's what I'm doing differently." No blame-shifting.
- **Post-mortem** — Blameless. "What did we not know?" not "Who screwed up?" ← *RabbitMQ split-brain at Toyota — ran a blameless post-mortem, team started reporting problems earlier*
- **Prevent recurrence** — Fix the system, not just the symptom. Add a test, add monitoring, add a runbook. ← *after the Terraform state corruption — added locking, it never happened again*

## How I Grow Others

- **1:1s** — Weekly 30 minutes. "What's blocking you? What do you want to learn? How can I help?" The best 1:1s are the ones where they talk more than I do.
- **Code reviews** — Real feedback, not rubber stamps. Explain why, not just what. ← *at KocSistem, I set the review standard by writing detailed reviews on every PR until the team matched*
- **Stretch assignments** — Give people work slightly beyond their comfort zone. Support them but don't do it for them.
- **Visibility** — When someone does great work, credit them publicly. When something fails, take responsibility as the lead.

## Sorulursa

> [!faq]- "How do you approach a project you've never done before?"
> Research first: understand the domain, read existing code, talk to people who've done similar things. Then prototype the riskiest part — the thing I'm least sure about. If the prototype works, I have confidence. If it doesn't, I've learned early and cheaply. At Combination, I spent a week building a GraphQL side project before proposing the migration. At KocSistem, I learned monitoring tools on weekends before building the POC.

> [!faq]- "How do you handle tight deadlines?"
> Scope down, not cut corners. "What's the smallest version of this that delivers value?" Ship that, then iterate. I never skip tests or reviews to meet a deadline — that creates more work later. If the deadline is genuinely impossible, I communicate early: "We can deliver X by the deadline, or X+Y with one more week. Which do you prefer?"

> [!faq]- "What's your biggest weakness?"
> I sometimes dig too deep into technical problems when delegating would be more effective. I've gotten better at this — at KocSistem I learned that unblocking 25 engineers is more impactful than solving one problem myself. But the instinct to "just fix it" is still there. I manage it by asking: "Am I the only person who can solve this, or am I just the fastest?"

> [!faq]- "Where do you see yourself in 5 years?"
> Leading a platform or infrastructure team — the kind of role where I set technical direction, mentor engineers, and still stay close enough to the code to make good decisions. Something like a Staff Engineer or Engineering Manager — technical leadership with people impact. I don't want to be in meetings all day, and I don't want to be an IC who only ships their own features.

> [!faq]- "Why are you looking for a new role?"
> I want to work on systems where my experience with microservices at scale, CI/CD, and team leadership has the most impact. I'm looking for a team that values both technical depth and engineering culture — where building the right thing and building it right both matter.

> [!faq]- "What questions do you have for us?"
> I always ask: "What does the team's deployment pipeline look like today?" (tells me DevOps maturity), "What's the biggest technical challenge you're facing?" (tells me what I'd work on), "How is the team organized?" (tells me the culture). See [[02-questions]] for the full list.

> [!faq]- "How do you communicate with non-technical stakeholders?"
> Their language, not mine. "This change reduces page load from 3 seconds to 200 milliseconds" instead of "we optimized the N+1 GraphQL resolver with DataLoader batching." I show working software in demos, not technical slides. I frame investments in business terms: "3 sprints of cleanup = feature delivery 4x faster." And I make trade-offs explicit: "Feature A by Friday or A+B by Wednesday — which matters more?"

> [!faq]- "How do you build trust with a new team?"
> Listen first, act second. First 2 weeks: 1:1s with everyone, understand pain points, learn the codebase. Then fix one thing the team has been complaining about — a slow pipeline, a flaky test, a missing dashboard. Small action builds more trust than big promises. At KocSistem, my monitoring POC was that first action — the team saw I understood their pain and did something about it.

> [!faq]- "How do you handle a situation where you disagree with your manager?"
> I present my perspective with data, not opinions. "Here's what I see in the metrics, here's my recommendation, here's the risk if we don't." If they still disagree, I ask them to explain their reasoning — maybe they have context I don't. If after that I still disagree on a reversible decision, I commit and execute their way. If it's irreversible and I believe it's harmful, I escalate clearly: "I want to flag that I see significant risk here. Can we discuss with [person with more context]?"

> [!faq]- "Describe your leadership style in one sentence."
> I lead by doing first, measuring second, and letting results speak — not by giving orders or pulling rank.

---
---

# Behavioral Stories — STAR Format

> [!tip] Her story'nin yaninda hangi soruya cevap verdigi var. Ayni story'yi iki kez kullanma. Bir soru icin birden fazla story varsa, interview akisina gore sec.

## Quick Lookup

| Soru turu | Story | Company | Yedek story |
|-----------|-------|---------|-------------|
| Conflict with teammate | [[ref-star-stories#Conflict — Deployment Freeze]] | KocSistem | [[ref-star-stories#Conflict — Skeptical Developer]] |
| Failure / mistake | [[ref-star-stories#Failure — RabbitMQ Split-Brain]] | Toyota | [[ref-star-stories#Failure — Terraform State Corruption]] |
| Leadership without authority | [[ref-star-stories#Leadership — CI/CD Pilot]] | KocSistem | [[ref-star-stories#Leadership — Quarter Planning]] |
| Complex problem | [[ref-star-stories#Problem-Solving — DevOps From Zero]] | KocSistem | [[ref-star-stories#Problem-Solving — GPS Scaling]] |
| Under pressure | [[ref-star-stories#Pressure — Production Line]] | Volvo | |
| Above and beyond | [[ref-star-stories#Initiative — Observability]] | KocSistem | [[ref-star-stories#Initiative — Cross-Team Testing]] |
| Difficult person | [[ref-star-stories#Collaboration — Third-Party Integration]] | Toyota | |
| Adaptability / change | [[ref-star-stories#Adaptability — GraphQL Migration]] | Combination | [[ref-star-stories#Adaptability — Stepping Up as PO]] |
| Mentoring / growing others | [[ref-star-stories#Mentoring — Junior to Mid]] | KocSistem | |
| Giving feedback | [[ref-star-stories#Feedback — Code Review Culture]] | KocSistem | |
| Receiving feedback | [[ref-star-stories#Receiving Feedback — Management Style]] | KocSistem | |
| Prioritization | [[ref-star-stories#Prioritization — Roadmap Trade-offs]] | KocSistem | |
| Stakeholder management | [[ref-star-stories#Stakeholders — Mid-Sprint Changes]] | KocSistem | |
| Cross-team collaboration | [[ref-star-stories#Cross-Team — Department Alignment]] | Volvo | [[ref-star-stories#Initiative — Cross-Team Testing]] |
| Risk / uncertainty | [[ref-star-stories#Uncertainty — New Domain]] | Volvo | |
| Customer focus | [[ref-star-stories#Customer Focus — Client Adaptation]] | KocSistem | |
| Time management | [[ref-star-stories#Time Management — Code vs People]] | KocSistem | |
| Influence / persuasion | [[ref-star-stories#Influence — Data-Driven Pitch]] | KocSistem | |
| **Proudest achievement** | [[ref-star-stories#Proud — Full Transformation Arc at KocSistem]] | KocSistem | [[ref-star-stories#Proud — Monitoring POC That Changed Everything]] |
| **Proudest technical** | [[ref-star-stories#Proud — Zero Compliance Findings at Volvo]] | Volvo | [[ref-star-stories#Proud — GraphQL Migration Without Breaking Anyone]] |
| **Big project success** | [[ref-star-stories#Proud — 2019 IDC Award]] | KocSistem | |
| **Critical impact** | [[ref-star-stories#Proud — Production Line Saved]] | Volvo | |
| **Impact beyond role** | [[ref-star-stories#Proud — Cross-Team Testing Impact at Toyota]] | Toyota | [[ref-star-stories#Proud — Stepping In When Nobody Else Would]] |


---

> [!tip] All 24 STAR stories and 8 success stories have been moved to [[ref-star-stories|STAR Stories]] for easier navigation.

---

*[[00-dashboard]]*
