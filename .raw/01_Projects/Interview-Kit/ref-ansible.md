---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Ansible — Quick Reference

> [!info] How I've used it: At Volvo, Ansible playbooks orchestrated test execution against CSP emulators — setting up emulator environments, running test campaigns, collecting results, and tearing down. Also used for image packing, validation, and code quality checks.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Playbooks\|playbooks]] | YAML tasks, idempotent, emulator setup at Volvo | [[#Inventory\|inventory]] | host groups, dynamic inventory, target selection |
| [[#Integration with CI\|CI integration]] | ZUUL triggers Ansible for test campaigns | [[#vs Shell Scripts\|vs shell scripts]] | idempotent, structured, error handling built in |
| [[#Error Handling & Idempotency\|idempotency]] | run twice = same result, safe re-runs | [[#What I Automated at Volvo\|at Volvo]] | emulator setup, test execution, image packing, teardown |

## HOW WE USED IT

At Volvo, I used Ansible to automate the test and validation side of the release pipeline. The playbooks handled:
- **Emulator setup** — spinning up CSP (Core System Platform) emulators for integration testing
- **Test execution** — running test campaigns against flashed firmware on emulators
- **Image packing and validation** — assembling and verifying build artifacts
- **Code quality checks** — shellcheck for bash scripts, flake8/mypy for Python

The CI system (ZUUL) triggered Ansible playbooks as part of the check and gate pipelines. When a developer pushed a patchset, ZUUL ran the build, then Ansible took over for the test phase — setting up the right emulator configuration, flashing the build, executing the test suite, and collecting results.

---

## Key Concepts

### Playbooks
- **What** — YAML files describing a sequence of tasks to execute on target hosts. Declarative — you describe the desired state, Ansible figures out how to get there.
- **Roles** — Reusable bundles of tasks, handlers, and variables. We had roles for "setup emulator", "run tests", "collect results", "teardown".
- **Handlers** — Tasks that run only when triggered by a change. Example: restart emulator only if the firmware was re-flashed.

### Inventory
- **What** — List of target hosts. Can be static (file) or dynamic (API query).
- **At Volvo** — Our inventory was the set of available CSP emulators. Each emulator had different capabilities (hardware variant, available ECUs). The playbook picked the right emulator based on the build target.

### Integration with CI
- **ZUUL + Ansible** — ZUUL defined the pipeline stages, Ansible executed the test stages. ZUUL passed build artifacts and parameters to the playbook, Ansible returned test results.
- **Idempotency** — Playbooks could be re-run safely. If an emulator was already set up from a previous failed run, the setup steps would skip. Only test execution would re-run.

### vs Shell Scripts
- **Why Ansible over bash** — Ansible is declarative, idempotent, and handles errors better than bash scripts. A 200-line bash script with error handling becomes a 30-line playbook. Also, Ansible has built-in support for parallel execution across multiple targets.

### Error Handling & Idempotency
- **Idempotent tasks** — Running a playbook twice produces the same result. If the emulator is already set up, the setup tasks skip. Only test execution re-runs.
- **Error handling** — `block/rescue/always` for try/catch/finally semantics. Failed tasks can trigger cleanup (teardown emulator, release rig) instead of leaving resources hanging.
- **Retries** — `retries` and `delay` parameters for tasks that might fail transiently (network calls, service startups).

### What I Automated at Volvo
- **Emulator setup** — CSP emulator provisioning, firmware flashing, network configuration
- **Test campaigns** — Running test suites against flashed firmware, collecting pass/fail results
- **Image packing** — Assembling build artifacts into deployable images, validating checksums
- **Code quality** — shellcheck for bash scripts, flake8/mypy for Python code, integrated into ZUUL check pipeline
- **Cleanup** — Releasing emulator rigs after test completion, cleaning up temporary files

---

## Sorulursa

> [!faq]- "Why Ansible instead of just shell scripts?"
> Ansible is declarative, idempotent, and handles errors gracefully. A 200-line bash script with proper error handling, cleanup, and retry logic becomes a 30-line playbook. Also, Ansible has built-in support for parallel execution — running tests on 5 emulators simultaneously is one config change, not rewriting the script.

> [!faq]- "How did Ansible fit into the ZUUL CI pipeline?"
> ZUUL defined the pipeline stages (check, gate, post-merge). For test stages, ZUUL triggered Ansible playbooks, passing build artifacts and target configuration as variables. Ansible executed the tests, collected results, and returned them to ZUUL. If tests failed, ZUUL marked the Gerrit change as Verified -1.

> [!faq]- "Could you replace Ansible with something else?"
> For the test orchestration use case, you could use plain Python scripts or even Makefile targets. But Ansible's inventory system (knowing which emulators are available and their capabilities) and idempotency (safe to re-run after a partial failure) made it the right fit. For infrastructure provisioning, Terraform would be better. Ansible is best for configuration management and orchestration tasks.

---

*[[00-dashboard]]*
