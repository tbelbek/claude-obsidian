---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Automotive Compliance — Quick Reference

> [!info] How I've used it: Built compliance automation at Volvo. Auto-generated test reports, traceability matrices, change logs in the pipeline. Zero compliance findings. Coordinated between regulatory, QA, and test departments.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#ISO 26262 — Functional Safety\|ISO 26262]] | functional safety, ASIL levels, hazard analysis | [[#ASPICE — Automotive SPICE\|ASPICE]] | process maturity, traceability, work products |
| [[#Traceability\|traceability]] | requirement→design→code→test, auto-generated matrices | [[#Compliance in Agile\|agile compliance]] | DoD includes compliance artifacts, pipeline generates |
| [[#At Volvo — Practical Setup\|at Volvo]] | zero findings, auto test reports, change logs in CI | | |

## HOW WE USED IT

At Volvo, I [[ag-compliance|automated compliance documentation]] in the release pipeline. Every release had to meet ISO 26262 and ASPICE requirements — documentation, traceability, audit trails.

**What I automated:**
- Test reports generated from test results — pulled pass/fail data, coverage metrics, and test execution logs into a formatted report
- Traceability matrices from commit history and ticket links — pipeline script parsed commit messages for JIRA IDs, queried the bug tracker for requirement links, assembled matrix: requirement → ticket → commit → test result
- Change logs from merge messages — assembled automatically per release with affected components and risk assessment
- Gate check script — Python script that pulled data from test reports, bug tracker, and analysis tools. Produced a go/no-go verdict with full audit trail. Pipeline wouldn't advance without explicit validation

**How I proved it works:**
- Ran manual and automated docs in parallel for 2 releases. Regulatory team compared them side by side. Automated ones were more complete — machines don't forget items. More consistent — same format every time
- After they switched, any auditor could trace a binary to: exact commit → build configuration → test results → requirements it implements

**What it meant for the team:**
- Dev team shipped as frequently as the pipeline allowed — no waiting for someone to write Word documents
- Regulatory team got better documentation than before — and it was available immediately after every build, not days later
- Zero compliance findings across all releases I shipped — the gate check caught issues before they reached the release

---

## Key Standards

### ISO 26262 — Functional Safety
- **What** — International standard for functional safety of electrical/electronic systems in road vehicles.
- **ASIL levels** — A (lowest risk) to D (highest). Determines required documentation depth and testing rigor.
- **Key requirement** — Traceability from requirements → design → implementation → test → verification. Every decision documented.

### ASPICE — Automotive SPICE
- **What** — Process assessment model for automotive software development. Evaluates maturity of development processes.
- **Levels** — 0 (incomplete) to 5 (optimizing). Most automotive OEMs require level 2-3.
- **Focus areas** — Requirements management, design, implementation, testing, configuration management.

### Traceability
- **What** — Ability to trace any binary back to: exact commit, build configuration, test results, requirements it implements.
- **How I automated it** — Pipeline script parsed commit log for ticket references, queried bug tracker for details, assembled matrix: requirement → ticket → commit → test result.
- **Why it matters** — During an audit, you must prove that every requirement was implemented and tested. Without traceability, you can't.

### Compliance in Agile
- **Challenge** — Compliance docs don't fit naturally into 2-week sprints. Regulatory wants full docs before release. Dev wants to ship frequently.
- **Solution** — [[ag-compliance|Automate doc generation in the pipeline]]. Ship as often as pipeline allows. Compliance artifacts generated automatically.
- **Key insight** — Regulatory teams don't care how docs are produced. They care that they're accurate and complete.

### At Volvo — Practical Setup
- **Pipeline-generated docs** — Every release pipeline run produced: test report (from test results), traceability matrix (from commit-to-ticket mapping), change log (from merge messages). All as build artifacts, not manual Word documents.
- **Parallel validation** — Ran manual and automated docs in parallel for 2 releases. Regulatory team compared them side by side. Automated ones were more complete — machines don't forget items.
- **Audit readiness** — Any auditor could trace a binary to: exact commit → build configuration → test results → requirements it implements. All queryable from the pipeline outputs.
- **Cross-department coordination** — Regulatory cared about audit trails, QA cared about coverage, Test cared about rig availability. I built the pipeline to serve all three from a single run.

## Sorulursa

> [!faq]- "How did you generate traceability matrices automatically?"
> Each commit message included a ticket reference (JIRA ID). The pipeline script parsed the commit log since the last release, extracted ticket IDs, queried the bug tracker for requirement links, and assembled the matrix: requirement → ticket → commit → test result. All automated, generated fresh for every release. The first time took a week to set up; after that it was zero effort per release.

> [!faq]- "How did you convince the regulatory team to trust automated documentation?"
> Evidence. I ran both approaches for two releases — manual and automated. The regulatory team compared them. The automated docs were more complete (machines don't skip items) and more consistent (same format every time). Once they saw the quality was equal or better, they switched. Trust was built through proof, not promises.

> [!faq]- "What happens when an audit finds a gap in traceability?"
> At Volvo, we never had this happen — zero compliance findings across all my releases. But the system was designed for it: if a requirement had no linked test, the gate check would flag it before the release. The pipeline wouldn't produce a "pass" verdict until every requirement had a traced implementation and test result. Prevention, not detection.

> [!faq]- "How does ISO 26262 affect day-to-day development?"
> It adds rigor to testing and documentation, but doesn't change how you write code. The main impact: every change needs a traceable path from requirement to test. In practice, this means writing good commit messages (reference the ticket), having good test coverage, and generating the documentation automatically. If your pipeline handles it, developers barely notice the compliance overhead.

---

*[[00-dashboard]]*
