# Session 10 — Full interview simulation

---


## Q1: Development workflow from scratch
**Your answer:** Plan, analyze effects, ask stakeholders, sketch diagram, basic tests, implement slice by slice, iterate tests+code, small commits, ADR for decisions, self-review, full build+test, PR.
**Grade: A** — Structured, senior-level, proactively addressed the big-commit in PoC.

## Q2: Cast null to value type / Nullable<T>
**Your answer:** "Compile error. Use Nullable<T> or int?. HasValue to check. Null-coalescing for default."
**Grade: A** — Four correct answers, precise, no hesitation.

---

## Q3: Why SQL Server instead of appsettings.json for 9 rows?
**Your answer:** "Project requirement — runtime updates without restart."
**Grade: B+** — Correct primary reason. Could add: unique constraints, transactions, persistence across deployments, auditability.

## Q4: IEnumerable vs IReadOnlyCollection as parameter
**Your answer:** "IEnumerable has modification methods" — WRONG. IEnumerable only has GetEnumerator (iteration).
**Grade: D** — Confused IEnumerable (iteration only) with ICollection (Add/Remove). Two separate branches: mutable (IEnumerable→ICollection→IList) and read-only (IEnumerable→IReadOnlyCollection→IReadOnlyList). IEnumerable is the base of BOTH — no mutation. This was covered before. Must memorize.

---

## Q5: Trade-off between quality and speed
**Your answer:** "Used EnsureCreated for speed, know I need migrations later. Technical debt borrowed."
**Grade: B** — Right example. Add: what speed bought (focus on business logic + tests), how mitigated (documented known risk).

## Q6: Middleware in ASP.NET Core
**Your answer:** "Chain of handlers, onion model, first registered = outermost. next() triggers next layer."
**Grade: B+** — Good onion analogy, correct registration order. Needed coaching on response path: response travels back outward through same layers in reverse. Request IN, response OUT.

---

## Q7: Repository handles both data access and caching — separate class?
**Your answer (first):** "Cache is too small." — not a principle.
**Your answer (after coaching):** "Decorator pattern — CachedTollRulesRepository wraps plain repo. Both implement ITollRulesRepository. Service doesn't know about caching. Extract when cache logic grows beyond simple GetOrCreate."
**Grade: B** — Needed coaching but delivered the pattern name and extraction trigger. Key: Decorator pattern, not "too small."

---

## Q8: string vs StringBuilder
**Your answer:** "String creates copy on every modification. StringBuilder is mutable buffer, operates in place. Small ops → string. Loops/dynamic → StringBuilder."
**Grade: A-** — Correct distinction, correct switching rule. Needed initial coaching but delivered clean.

---

## Q9: DORA metrics
**Your answer:** "Four metrics: deployment frequency, lead time, change failure rate, MTTR. Important for agile gating. Used at KocSistem — decreased 4 days to 1 day by reducing deploy sizes which reduced failures and approval bottlenecks."
**Grade: A-** — Named all four, tied to own experience, explained the mechanism (smaller deploys → less risk → faster approvals).

---

## Q10: builder.Host vs builder.Services vs builder.Configuration
**Your answer:** "Services = what gets injected. Host = infrastructure before DI. Configuration = read from appsettings. Serilog on Host because it replaces the whole logging pipeline."
**Grade: A-** — Correct distinction, correct Serilog reasoning. Needed coaching but delivered clean.

---

## Q11: ExecuteDeleteAsync — what SQL, why not load-then-delete?
**Your answer:** "ExecuteDeleteAsync runs DELETE WHERE directly, no load. Load-then-delete does SELECT first then individual DELETEs."
**Grade: B+** — Correct mechanism. Could add: "single round-trip, constant memory vs N+1 statements and loading all rows into memory."

---

## Q12: throw expression in ?? — how does that work?
**Your answer:** "Throws when null. Yes you can throw in an expression. Since C# 12?"
**Grade: B** — Correct behavior. Wrong version: throw expressions were introduced in C# 7 (not 12). Know: before C# 7, throw was statement-only. Now it's an expression usable in ??, ?:, and lambdas.

---

## Q13: Stuck and how you unblocked
**Your answer:** "Stuck testing with real SQL. Removed integration tests, created blackbox tests with Testcontainers."
**Grade: B** — Good problem-solution story. Add: "Evaluated in-memory provider but it doesn't test real SQL translation. Testcontainers gave me real SQL Server with zero infra setup."

---

## Q14: Task<T> vs ActionResult<T> — why different controllers?
**Your answer:** "Intention was unifying but calculation API surface can't change. ActionResult returns status, Task can't. All errors go through centralized handler."
**Grade: B+** — Correct technical distinction and practical reasoning. Key: TollFee always 200-or-throw. Config GET needs 404 decision in controller.

---

## Q15: WHERE vs HAVING in SQL
**Your answer:** "WHERE before GROUP BY, HAVING after. HAVING can use SUM/COUNT, WHERE can't."
**Grade: A-** — Correct distinction. Needed initial coaching but delivered clean.

---

## Q16: LEFT JOIN vs INNER JOIN — do you use joins?
**Your answer:** "Left join brings left + overlap, inner only overlap. No joins in my project."
**Grade: B** — Correct definitions. Needed coaching on why no joins: tables are independent, queried separately by year, combined in C# code.

---

## Q17: IDisposable — what, when, does your code implement it?
**Your answer:** "For unmanaged resources — connections, file handles. Dispose releases them. My classes managed by DI, don't need it. Use using/await using for disposal."
**Grade: B+** — Correct definition, correct that DI handles it. Needed coaching on using vs await using: using = sync Dispose(), await using = async DisposeAsync() (releases thread during cleanup).

---

## Q18: internal vs public — why internal for FeeBandClockFormat?
**Coaching provided:** internal = visible within assembly only. FeeBandClockFormat is implementation detail. Public would add to API surface = maintenance burden. Internal = free to change.
**Grade: F (needed coaching)** — Must know: internal = same assembly only. Public = API surface. Implementation details should be internal.

---

## Q19: git merge vs git rebase
**Your answer:** "Merge creates merge commit. Rebase aligns history from target. Prefer rebase for cleaner history. Don't rebase when lots of overlapping conflicts."
**Grade: B+** — Correct distinction and preference. Add: never rebase shared/pushed commits — rewrites history, forces team re-sync.

---

## Q20: .NET vs .NET Framework — can your project run on Framework?
**Your answer:** "Framework was predecessor, project can't run on it. Different setup, .NET Core came after 4.7.2."
**Grade: B** — Correct that it can't run. Add key distinction: Framework = Windows-only, .NET = cross-platform (your Docker runs on Linux). Framework = maintenance mode, .NET = all new features.

---

## Session 10 Summary

| Grade | Count | Questions |
|---|---|---|
| A / A- | 3 | Q1, Q2, Q15 |
| B / B+ | 12 | Q3, Q5, Q6, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q17, Q19, Q20 |
| D / F | 3 | Q4, Q7, Q18 |

### Session 10 Average: B+

### Key weaknesses this session
- IEnumerable still confused with ICollection (Q4) — THIRD TIME. Must memorize: IEnumerable = iteration ONLY.
- internal vs public (Q18) — didn't know. Now documented.
- Decorator pattern (Q7) — needed coaching. "Too small" is not a principle.

### Key strengths
- Workflow explanation (A)
- Nullable types (A)
- DORA metrics with personal story (A-)
- SQL knowledge (WHERE/HAVING, JOIN types)
- Good practical reasoning throughout

### Overall Trend
Round 1: C+ → Round 2: C+ → Mixed: B → S3: A- → S4: A- → S5: B- → S6: B+/A- → S7: B+ → S8: B+ → S9: B → **S10: B+**
