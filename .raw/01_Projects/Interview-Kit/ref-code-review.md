---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Code Review — Quick Reference

> [!info] How I've used it: At KocSistem, established code review culture from scratch — the team went from no reviews to mandatory PRs with quality gates. At Toyota, gave meaningful reviews in a safety-critical system. At Combination, reviews across 60+ services with breaking change detection.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#"Review This Code" — My Checklist\|my checklist]] | security→correctness→performance→maintainability→tests→API | [[#"Review This Code" — My Checklist\|security first]] | injection, auth, secrets, data exposure, deserialization |
| [[#What Makes a Good Review\|good review]] | logic not style, questions not commands, review tests too | [[#Quality Gates in CI\|quality gates]] | build+tests+static analysis+coverage must pass before merge |
| [[#Review Flow\|turnaround]] | 4 hours target, don't block someone for a day | [[#Branch Strategy\|branch strategy]] | feature branches, protected main, release branches |
| [[#Common Anti-Patterns I Flag\|anti-patterns]] | catch empty, SELECT *, no tests, hardcoded secrets | [[#Code Review at Scale (60+ services)\|at scale (60+)]] | PR templates, CODEOWNERS, automated quality gates |

## HOW WE SET IT UP

When I became Dev Lead, there was no code review process. Developers pushed directly to main. No pull requests, no reviews, no quality checks. I set up the entire system:

**The technical setup:**
- Moved from "push to main" to a proper branching strategy — feature branches, pull requests, protected main branch.
- Required at least one approval before merge. For critical paths (auth, data access, API changes), required two.
- Added automated quality gates in the CI pipeline — build must pass, tests must pass, static analysis must pass before the PR can be merged.
- Set up PR templates with a checklist: "Tests added? Documentation updated? Breaking changes noted?"

**The cultural setup (harder than the technical):**
- First few weeks, reviews were rubber stamps — "LGTM" with no comments. I started writing detailed reviews myself on every PR to set the standard. Line-by-line comments explaining why something could be improved, not just that it should be.
- Made it clear: a review is not a judgment of the developer, it's a conversation about the code. "Have you considered X?" is better than "This is wrong."
- Paired the most resistant developers with me on their first reviewed PRs. Once they got useful feedback that actually improved their code, they bought in.
- Set a turnaround expectation: reviews should be done within 4 hours. If a PR sits for a day, the author can ping the reviewer. No PR should block someone for more than a day.

**What changed:**
- Bug rate in new releases dropped 55%. Most bugs were caught in review, not in production.
- Knowledge sharing improved — developers learned from each other's code instead of working in silos.
- Junior developers grew faster because they got real feedback, not just "approved."
- SLA breach rate dropped 60% — fewer bugs reaching production meant fewer emergency fixes.

---

## Key Concepts

### "Review This Code" — My Checklist

When someone opens a PR or an interviewer puts code on screen and says "review this," I go through these in order:

**1. Security (first, always):**
- Input validation — is user input sanitized? SQL injection, XSS, path traversal?
- Authentication/authorization — does this endpoint check who's calling? Is the user allowed to do this?
- Secrets — any hardcoded credentials, API keys, connection strings?
- Data exposure — does the response leak data the caller shouldn't see? (e.g., returning password hashes, internal IDs)
- Deserialization — is untrusted data being deserialized without validation?

**2. Correctness:**
- Does the code do what the PR description says it does?
- Edge cases — what happens with null, empty, zero, negative, very large, duplicate, concurrent?
- Error handling — what happens when it fails? Is there a try/catch? Does it fail silently or loudly?
- Race conditions — is shared state being modified without locking? Are there async operations that could interleave?
- Off-by-one errors — loop boundaries, array indexing, pagination

**3. Performance:**
- N+1 queries — is there a loop making database calls? Should it be a JOIN or batch?
- Unbounded queries — `SELECT *` without WHERE or LIMIT on a large table?
- Memory leaks — is a disposable resource (connection, stream, file handle) being created but not disposed?
- Unnecessary computation — is the same thing calculated multiple times when it could be cached?
- Large payloads — is the API returning more data than the consumer needs?

**4. Maintainability:**
- Naming — do variable/function/class names tell you what they do?
- Single responsibility — does one function do one thing, or is it a 200-line god method?
- Duplication — is the same logic copied in multiple places? Should it be extracted?
- Magic numbers/strings — are there unexplained constants? Should they be named?
- Complexity — can a nested if/else be simplified? Is there a simpler approach?

**5. Tests:**
- Are there tests for the new behavior?
- Do tests cover the happy path AND the error/edge cases?
- Are the assertions checking the right thing? (not just "it doesn't throw")
- Are the tests independent? (not relying on execution order or shared state)
- If this is a bug fix, is there a regression test?

**6. API/Contract:**
- Is this a breaking change for consumers? Field removed, type changed, endpoint renamed?
- Is the API versioned correctly?
- Are error responses consistent with existing endpoints? (same format, same status codes)
- Is the response shape documented?

### What Makes a Good Review
- **Focus on logic, not style** — Formatting is for linters. Reviews focus on correctness, security, edge cases.
- **Ask questions, don't command** — "Have you considered what happens when X is null?" is better than "Add a null check." Helps the author think, not just comply.
- **Review the tests too** — If tests don't cover the new behavior, the code isn't done.
- **Small PRs** — Large PRs get rubber-stamped. Keep under 200 lines. One feature, one PR.
- **Read the PR description first** — Understand intent before reading code. If the description is missing, that's the first comment.
- **Check the diff, not just the new code** — Did the change break something that was working? Did it remove something important?

### Quality Gates in CI
- **Build must pass** — A broken build should never be mergeable.
- **Tests must pass** — All unit, component, integration. No "skip because flaky" — fix the flaky test.
- **Static analysis** — Block on critical/high. Suppress false positives via version-controlled suppression file (requires review to change). *(we used SonarQube-style gates at KocSistem)*
- **Coverage check** — Not a hard percentage. "No new code without tests" is the rule. *(enforced via review, not metrics)*
- **Breaking change detection** — gRPC proto and GraphQL schema compatibility checked automatically. *(we used this at Combination to protect 60+ services from cascading breaks)*

### Review Flow
- **Author** — Creates PR, writes description (what and why), adds reviewers, responds to feedback.
- **Reviewer** — Reads description first, then diff. Comments with questions or suggestions. Approves or requests changes.
- **Turnaround** — 4 hours target. Longer than a day blocks delivery.
- **Approval** — One approval for standard changes. Two for critical paths (auth, payment, data migrations, infrastructure).
- **Walkthrough** — For large PRs that can't be split, author schedules 15-minute walkthrough before review. Cuts review time in half.

### Branch Strategy
- **Feature branches** — One branch per feature/bugfix. Named descriptively (`feature/add-graphql-subscriptions`, `fix/redis-connection-timeout`).
- **Protected main** — No direct pushes. All changes go through PR + review + CI.
- **Release branches** — Feature branches merge to main, main merges to release when ready.

### Code Review at Scale (60+ services)
- **Consistent standards** — Same expectations across all services. PR templates, quality gates, linting rules shared via pipeline template repo.
- **Breaking change detection** — CI handles proto/schema compatibility. Reviewer focuses on logic, not backward compatibility.
- **CODEOWNERS** — GitHub CODEOWNERS ensures the right people review critical paths. API changes → API team. Infrastructure → platform team.
- **Automated formatting** — No style debates. Linters and formatters run pre-commit or in CI. Reviewers never comment on formatting.

### Common Anti-Patterns I Flag

| What I See | What I Say |
|------------|-----------|
| `catch (Exception) { }` | "Swallowing exceptions hides bugs. Log the error or let it propagate." |
| `SELECT * FROM users` | "Do we need all columns? What happens with 1M rows? Consider pagination." |
| No tests on new feature | "How do we know this works? What happens when X is null?" |
| 300+ line PR | "Can we split this? Hard to review effectively at this size." |
| Hardcoded connection string | "This needs to come from config/Key Vault, not the source code." |
| Nested if/else 5 levels deep | "Can we simplify? Early returns or guard clauses?" |
| `Thread.Sleep(5000)` | "Why the wait? Is there a race condition we should fix properly?" |
| `// TODO: fix later` | "Can we create a ticket for this so it doesn't get lost?" |
| No error handling on external call | "What happens when this API is down or returns 500?" |

## Sorulursa

> [!faq]- "Walk me through how you'd review this code" (interview scenario)
> I start by reading the context — what is this code supposed to do? Then I scan for security first (input validation, auth, secrets), then correctness (edge cases, null handling, error paths), then performance (N+1, unbounded queries, resource leaks), then maintainability (naming, complexity, duplication), then tests (coverage, assertions, regression). I don't try to find everything in one pass — I do focused passes by category. I comment with questions ("what happens when X is null?") rather than commands ("add a null check").

> [!faq]- "How do you handle developers who resist code review?"
> Show the value, don't mandate. At KocSistem, first month was rough. I paired with resistant developers, gave useful feedback that caught real bugs, showed before/after bug rates. When they saw reviews catching issues they would've spent hours debugging in production, they came around. The key: make the review helpful, not painful.

> [!faq]- "How do you keep reviews from becoming a bottleneck?"
> Small PRs, 4-hour turnaround expectation, enough reviewers per team. If a PR is urgent, tag multiple reviewers — whoever's available picks it up. For large PRs: 15-minute walkthrough before review. Cuts review time in half.

> [!faq]- "How do you review code in a language/domain you're not expert in?"
> Focus on structure, not syntax. Is the logic clear? Are there edge cases? Are tests covering the right scenarios? Is error handling complete? You don't need to be an expert to spot a missing null check, an untested error path, or a function doing too many things.

> [!faq]- "What's the difference between reviewing at 25-person team vs 60+ services?"
> At KocSistem (25 people), I set expectations personally. At Combination (60+ services), it's systems — PR templates, CODEOWNERS, automated quality gates, shared linting rules. You can't personally review every PR across 60 services, so you build the system that does it.

> [!faq]- "How do you handle disagreements in code review?"
> If it's about style — defer to the linter/formatter. If it's about approach — ask "what problem does this solve?" and discuss trade-offs. If we can't agree, we timebox it: try one approach for a sprint, measure, decide. Never block a PR over a preference — only over correctness or security.

> [!faq]- "What do you do when you find a security issue in review?"
> Flag it immediately, don't approve. Explain the risk clearly — "this allows SQL injection because user input is concatenated into the query." Suggest the fix — "use parameterized queries instead." If it's already in production, escalate alongside the review — don't wait for the PR to be fixed before alerting the team.

---

*[[00-dashboard]]*
