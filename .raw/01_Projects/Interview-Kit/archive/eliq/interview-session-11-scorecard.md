# Session 11 — Coding focus + DevOps sprinkle

---


## Q1: What does IEnumerable give you?
**Your answer:** "Count only" — WRONG (4th time).
**Grade: F** — IEnumerable gives GetEnumerator() ONLY. foreach. Nothing else. Count comes from IReadOnlyCollection or ICollection. MUST memorize this.

---

## Q2: Thread vs Task
**Your answer:** "Task runs on thread pool, framework manages it. Thread is manual management."
**Grade: A-** — Correct distinction. Add: Task integrates with async/await, Thread doesn't.

## Q3: What are generics?
**Your answer:** "Placeholder for type-safe reusable classes. List<T> works with any type safely. Examples: Task, IReadOnlyCollection, Func."
**Grade: B+** — Needed initial coaching on the concept but delivered clean explanation with project examples.

---

## Q4: Biggest Docker problem you solved
**Your answer:** "High build times. Multi-stage builds (SDK→runtime) reduced images from 800MB to 80MB. Reordered layers — package restore first (cached), source copy last (changes often). Docker invalidates cache downward so keeping changing parts low matters."
**Grade: A** — Concrete problem, specific technique (layer ordering + multi-stage), measurable result (800→80MB). Real experience from 60+ services.

---

## Q5: What's a delegate? Func vs Action?
**Your answer:** "Delegation of function to other parts. Action = no return. Func = returns value. Used in fee band and year config updates."
**Grade: B** — Got the Action/Func distinction and project example. Imprecise on delegate definition — it's a type-safe method pointer (variable that stores a function), not "delegation." But correct usage example.

---

## Q6: Test pyramid — what and how does your project map?
**Your answer:** "Unit-integration-blackbox-smoke. Cheapest at bottom, expensive at top. Catch errors early and cheap. My project: 79 unit, 48 blackbox, smoke script."
**Grade: B+** — Correct shape and reasoning. Needed coaching on "why pyramid" but delivered clean: "catch errors early and cheap."

---

## Q7: Access modifiers — private, protected, internal, public
**Your answer:** "private = class only. internal = same assembly. public = everywhere. protected = needed coaching."
**Grade: B-** — 3 of 4 correct. protected = class + subclasses ("private but my children can see it"). Also: protected internal (subclass OR same assembly), private protected (subclass AND same assembly).

---

## Q8: Adding Redis — what would you store and how?
**Your answer (first):** "All the DB in Redis" — wrong, Redis is cache not primary DB.
**Your answer (after coaching):** "Replace IMemoryCache with Redis cache implementation. SQL stays as source of truth."
**Grade: C+** — Needed coaching. Initial instinct was wrong (Redis as DB replacement). Corrected to cache replacement. Know: Redis = distributed cache, SQL = durable source. L1/L2 pattern for optimization.

---

## Q9: LINQ — what is it, two syntaxes?
**Your answer:** "Query language of C#. Method syntax (fluent) and query syntax (SQL-like). I use method syntax — more methods, better chaining, works with async EF Core. Query syntax better for complex joins which I don't have."
**Grade: A-** — Correct definitions, correct preference with reasoning. Needed coaching on "why not query" but delivered clean answer.

---

## Q10: TollService — too many responsibilities?
**Your answer:** "Those are done by different functions/engines. Orchestration is the business flow — one responsibility."
**Grade: A-** — Correct SRP defense: orchestration = one responsibility. Steps delegated to engine/repo/validator. TollService wires them in order. One reason to change: if the flow changes.

---

## Q11: Extension methods — what and where?
**Your answer:** "Method you can use with the type of that class. Exception handler uses it on app start."
**Grade: B** — Correct concept and one example. Missed FeeBandMappingExtensions (ToFeeBand, ToFeeBandResponse extending IFeeBandShape). Know: static method with `this` keyword on first parameter. Adds methods to types without modifying them.

---

## Q12: Docker image vs container
**Your answer:** "Image is blueprint, container is isolated running instance with env vars and config."
**Grade: A** — Clean, correct, concise.

---

## Q13: ref vs out vs in parameters
**Your answer:** "ref = pass by reference. out = must assign inside method, compile error if not. in = read-only pass."
**Grade: B+** — All three correct. Typo "painter" for "pointer" but meaning was clear.

---

## Q14: Liskov Substitution Principle
**Your answer:** "Subclass substitutable for parent. TollRulesRepository and InMemoryRulesRepository both implement the interface — swap without behavior change. If one throws unexpected exception, that violates Liskov."
**Grade: A-** — Correct definition, correct usage example, correct violation scenario. Initially said "siblings" but corrected to parent-child.

---

## Q15: Database indexes — types, when do they hurt?
**Your answer:** "Phonebook of data. Clustered = table data. Non-clustered = separate structure. Hurts on: long types, write-heavy tables (must maintain indexes), low-selectivity columns (boolean — doesn't narrow search)."
**Grade: B+** — Good analogy, correct types, correct hurt scenarios. Needed coaching on write-heavy but delivered clean after.

---

## Session 11 Summary

| Grade | Count | Questions |
|---|---|---|
| A / A- | 5 | Q2, Q4, Q9, Q12, Q14 |
| B / B+ | 6 | Q3, Q5, Q6, Q7, Q11, Q13, Q15 |
| C+ | 1 | Q8 |
| F | 1 | Q1 |

### Session 11 Average: B+

### Overall Trend
R1: C+ → R2: C+ → Mix: B → S3: A- → S4: A- → S5: B- → S6: B+/A- → S7: B+ → S8: B+ → S9: B → S10: B+ → **S11: B+**

### Persistent weakness
IEnumerable = GetEnumerator ONLY. 4th wrong answer. This WILL come up in the real interview.

### Strengths this session
- Docker experience with real numbers (800→80MB) — A
- SRP defense of TollService (orchestration = single responsibility) — A-
- Liskov with correct example and violation — A-
- LINQ syntax preference with reasoning — A-
