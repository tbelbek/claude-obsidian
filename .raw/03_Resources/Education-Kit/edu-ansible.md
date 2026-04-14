---
tags:
  - education-kit
---

# Ansible — Education Kit

## Key Concepts

### What Ansible Is

Ansible is an agentless automation tool for configuration management, application deployment, and task orchestration. It uses SSH to connect to target hosts and executes tasks defined in YAML playbooks. No agent installation required on managed nodes — just Python and SSH. Ansible is idempotent by design: running a playbook twice produces the same result. Best for: configuring servers, deploying applications, orchestrating multi-step workflows across multiple machines, and automating repetitive operations tasks.

### Playbooks
- **What** — YAML files describing a sequence of tasks to execute on target hosts. Declarative — you describe the desired state, Ansible figures out how to get there.
- **Roles** — Reusable bundles of tasks, handlers, and variables. Roles let you organize common automation patterns (e.g., "setup environment", "run tests", "collect results", "teardown").
- **Handlers** — Tasks that run only when triggered by a change. Example: restart a service only if its configuration file was modified.

### Inventory
- **What** — List of target hosts. Can be static (file) or dynamic (API query).
- **Host groups** — Organize hosts by function or capability. Playbooks can target specific groups.
- **Dynamic inventory** — Query an API (cloud provider, CMDB) to discover hosts at runtime. Useful when hosts are ephemeral or change frequently.

### Integration with CI
- **CI + Ansible** — CI systems define the pipeline stages, Ansible executes specific stages (e.g., test orchestration, deployment). The CI system passes build artifacts and parameters to the playbook, Ansible returns results.
- **Idempotency in CI** — Playbooks can be re-run safely. If the environment is already set up from a previous failed run, the setup steps skip. Only the actual work (test execution, deployment) re-runs.

### vs Shell Scripts
- **Why Ansible over bash** — Ansible is declarative, idempotent, and handles errors better than bash scripts. A 200-line bash script with error handling becomes a 30-line playbook. Also, Ansible has built-in support for parallel execution across multiple targets — running tasks on many hosts simultaneously is one config change, not rewriting the script.

### Error Handling & Idempotency
- **Idempotent tasks** — Running a playbook twice produces the same result. If the environment is already set up, the setup tasks skip.
- **Error handling** — `block/rescue/always` for try/catch/finally semantics. Failed tasks can trigger cleanup (release resources, teardown environments) instead of leaving resources hanging.
- **Retries** — `retries` and `delay` parameters for tasks that might fail transiently (network calls, service startups).

## Sorulursa

> [!faq]- "Why Ansible instead of just shell scripts?"
> Ansible is declarative, idempotent, and handles errors gracefully. A 200-line bash script with proper error handling, cleanup, and retry logic becomes a 30-line playbook. Also, Ansible has built-in support for parallel execution — running tasks on multiple hosts simultaneously is one config change, not rewriting the script.

> [!faq]- "How does Ansible fit into a CI pipeline?"
> The CI system defines the pipeline stages (check, gate, post-merge). For orchestration stages, the CI triggers Ansible playbooks, passing build artifacts and target configuration as variables. Ansible executes the tasks, collects results, and returns them to the CI system.

> [!faq]- "Could you replace Ansible with something else?"
> For orchestration tasks, you could use plain Python scripts or Makefile targets. But Ansible's inventory system (knowing which hosts are available and their capabilities) and idempotency (safe to re-run after a partial failure) make it the right fit. For infrastructure provisioning, Terraform would be better. Ansible is best for configuration management and orchestration tasks.
