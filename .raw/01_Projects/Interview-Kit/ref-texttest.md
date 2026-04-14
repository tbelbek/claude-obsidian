---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# TextTest — Quick Reference

> [!info] How I've used it: At Toyota, TextTest was the acceptance testing framework for T-ONE. BDD-style feature-driven test suites. Fleet simulation with multiple AGV types (SEW Palletrunner, Kollmorgen, Toyota forklifts). Integrated with Docker Compose test stacks.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#What TextTest Is\|TextTest]] | BDD acceptance testing, text-based expected output diffs | [[#Fleet Simulation\|fleet simulation]] | multiple AGV types, warehouse scenarios, parallel execution |
| [[#Integration with CI/CD\|CI integration]] | Docker Compose stacks, automated test campaigns | [[#Why TextTest Over Other Frameworks\|why TextTest]] | domain-specific, non-developer authoring, fleet sim support |
| [[#Cross-Team Impact\|cross-team]] | test framework used by 3 teams, I maintained shared infra | | |

## HOW WE USED IT

At Toyota, I built and maintained the TextTest-based acceptance testing framework for T-ONE. The test suites covered full system scenarios — fleet behavior with different AGV types, warehouse layouts, and load patterns. Tests ran against Docker Compose stacks that spun up the full service mesh (RabbitMQ, MongoDB, application services).

I became the go-to person for testing strategy across multiple teams — [[ls-toyota|helping other teams set up their own simulation environments]] and integration tests.

## Cross-Team Impact

My official role at Toyota was backend development on T-ONE. But the test frameworks I built had a bigger impact than any single feature. It started when I created fleet simulation tests for my own team — TextTest scenarios that spun up Docker Compose stacks with RabbitMQ, MongoDB, and the full service mesh, then simulated hundreds of forklifts.

Other teams saw what these could do in a demo and started asking for help. I ended up supporting multiple teams across Toyota Material Handling — helping them set up their own TextTest environments, write fleet simulation scenarios for their specific AGV types, and integrate the test suites into their CI pipelines. Over time, I became the go-to person for testing strategy across the organization.

This wasn't in my job description. But the need was real — teams that had no integration tests before were now catching bugs before staging. My manager saw it as a multiplier, not a distraction. The cross-team visibility also helped me write better backend code because I understood how different parts of the system interacted.

---

## Key Concepts

### What TextTest Is
- **Text-based acceptance testing** — Tests define expected behavior as text-based scenarios. Compare actual output against expected output.
- **BDD-style** — Feature files describe behavior in domain language. "Given a warehouse with 5 forklifts, when a transport is requested, then the nearest available forklift is assigned."
- **Language-agnostic** — TextTest runs any executable and compares its output. Works with Python, Java, C#, or any command-line tool.

### Fleet Simulation
- **What** — Simulate hundreds of autonomous vehicles in a virtual warehouse. Test routing algorithms, collision avoidance, job assignment logic.
- **AGV types** — SEW Palletrunner, Kollmorgen Forklift, Toyota forklifts. Each type has different capabilities, speeds, and turning radii. Tests verify behavior across all types.
- **Scenarios** — Different warehouse layouts, different load patterns (peak hour rush, steady state, single vehicle breakdown). Tests verify the system handles each gracefully.

### Integration with CI/CD
- **Docker Compose test stacks** — Full test environment: RabbitMQ, MongoDB, application services, fleet simulator. Tests run against a realistic system, not mocks.
- **Test data management** — Pre-configured warehouse layouts, vehicle configs, and test scenarios loaded before each test run.
- **Result comparison** — TextTest compares actual output files against approved baselines. Any difference = test failure with a clear diff.

### Why TextTest Over Other Frameworks
- **Approval-based testing** — Instead of writing assertions, you approve the output once and TextTest detects any change. Good for complex systems where writing granular assertions for every field is impractical.
- **Visual diffs** — When a test fails, TextTest shows a diff of expected vs actual. Easy to see what changed.
- **Batch execution** — Run hundreds of scenarios in parallel. Integrated with CI for automated regression detection.

## Sorulursa

> [!faq]- "Why TextTest instead of standard unit/integration test frameworks?"
> Unit tests verify individual components. TextTest verifies the whole system end-to-end. For autonomous forklifts, you can't unit-test routing algorithms in isolation — you need a simulated warehouse with multiple vehicles, obstacles, and concurrent tasks. TextTest's approval-based model is perfect for this: run the scenario, check the output matches the expected behavior.

> [!faq]- "How did you handle flaky tests in fleet simulation?"
> Timing-dependent tests were the biggest challenge. We added tolerances for time-sensitive assertions and used deterministic scheduling in the simulator. For truly non-deterministic scenarios (network delays, concurrent vehicle decisions), we ran the test multiple times and checked for consistency rather than exact match.

---

*[[00-dashboard]]*
