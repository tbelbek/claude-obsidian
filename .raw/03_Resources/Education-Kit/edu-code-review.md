---
tags:
  - education-kit
---

# Code Review — Education Kit

## Review Checklist

When reviewing code, go through these in order:

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

## What Makes a Good Review

- **Focus on logic, not style** — Formatting is for linters. Reviews focus on correctness, security, edge cases.
- **Ask questions, don't command** — "Have you considered what happens when X is null?" is better than "Add a null check." Helps the author think, not just comply.
- **Review the tests too** — If tests don't cover the new behavior, the code isn't done.
- **Small PRs** — Large PRs get rubber-stamped. Keep under 200 lines. One feature, one PR.
- **Read the PR description first** — Understand intent before reading code. If the description is missing, that's the first comment.
- **Check the diff, not just the new code** — Did the change break something that was working? Did it remove something important?

## Quality Gates in CI

- **Build must pass** — A broken build should never be mergeable.
- **Tests must pass** — All unit, component, integration. No "skip because flaky" — fix the flaky test.
- **Static analysis** — Block on critical/high. Suppress false positives via version-controlled suppression file (requires review to change).
- **Coverage check** — Not a hard percentage. "No new code without tests" is the rule.
- **Breaking change detection** — API schema compatibility checked automatically.

## Review Flow

- **Author** — Creates PR, writes description (what and why), adds reviewers, responds to feedback.
- **Reviewer** — Reads description first, then diff. Comments with questions or suggestions. Approves or requests changes.
- **Turnaround** — 4 hours target. Longer than a day blocks delivery.
- **Approval** — One approval for standard changes. Two for critical paths (auth, payment, data migrations, infrastructure).
- **Walkthrough** — For large PRs that can't be split, author schedules a 15-minute walkthrough before review. Cuts review time in half.

## Branch Strategy

- **Feature branches** — One branch per feature/bugfix. Named descriptively (`feature/add-graphql-subscriptions`, `fix/redis-connection-timeout`).
- **Protected main** — No direct pushes. All changes go through PR + review + CI.
- **Release branches** — Feature branches merge to main, main merges to release when ready.

## Code Review at Scale

- **Consistent standards** — Same expectations across all services. PR templates, quality gates, linting rules shared via pipeline template repos.
- **Breaking change detection** — CI handles schema compatibility. Reviewer focuses on logic, not backward compatibility.
- **CODEOWNERS** — Ensures the right people review critical paths. API changes go to the API team. Infrastructure goes to the platform team.
- **Automated formatting** — No style debates. Linters and formatters run pre-commit or in CI. Reviewers never comment on formatting.

## Common Anti-Patterns

| What You See | What to Say |
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

---

## Common Questions

**"Walk me through how you'd review code"**
Start by reading the context — what is this code supposed to do? Then scan for security first (input validation, auth, secrets), then correctness (edge cases, null handling, error paths), then performance (N+1, unbounded queries, resource leaks), then maintainability (naming, complexity, duplication), then tests (coverage, assertions, regression). Do focused passes by category. Comment with questions rather than commands.

**"How do you handle developers who resist code review?"**
Show the value, don't mandate. Write detailed reviews yourself on every PR to set the standard. Pair with resistant developers and give useful feedback that catches real bugs. When they see reviews catching issues they would've spent hours debugging in production, they come around. The key: make the review helpful, not painful.

**"How do you keep reviews from becoming a bottleneck?"**
Small PRs, 4-hour turnaround expectation, enough reviewers per team. If a PR is urgent, tag multiple reviewers — whoever's available picks it up. For large PRs: a short walkthrough before review cuts review time in half.

**"How do you handle disagreements in code review?"**
If it's about style — defer to the linter/formatter. If it's about approach — ask "what problem does this solve?" and discuss trade-offs. If you can't agree, timebox it: try one approach for a sprint, measure, decide. Never block a PR over a preference — only over correctness or security.
