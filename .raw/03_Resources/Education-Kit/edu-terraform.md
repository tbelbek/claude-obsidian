---
tags:
  - education-kit
---

# Terraform — Education Kit

## Key Concepts

### What Terraform Is
Terraform is an Infrastructure-as-Code tool by HashiCorp that lets you define cloud resources (VMs, networks, databases, K8s clusters) in declarative HCL files. You describe the desired state, Terraform figures out what to create, change, or destroy. It is cloud-agnostic — same tool for Azure, AWS, GCP — and tracks everything in a state file so it knows what it manages. Best for: provisioning and managing cloud infrastructure reproducibly, with plan/apply workflow that shows exactly what will change before making any changes.

### State Management
- **State file** — JSON mapping of your HCL resources to real infrastructure IDs. Source of truth for Terraform.
- **Remote state** — Store state in a shared backend (Azure Blob Storage, S3, Terraform Cloud) instead of locally. Required for team use. Prevents state corruption that happens when two developers run apply simultaneously.
- **State locking** — Prevents two people running `apply` at the same time. Uses lease-based locking on the backend. Without locking, simultaneous applies can corrupt state and require manual recovery with `terraform import` and `state rm`.
- **State drift** — When reality diverges from state because someone changed infrastructure manually. Set up scheduled plan checks (e.g., nightly) to catch drift early.
- **terraform import** — Bring existing resources into state management without recreating them.
- **terraform state rm** — Remove a resource from state without destroying it in the cloud.

### Plan/Apply Workflow
Plan/apply is Terraform's two-step workflow: first show what will change (plan), then make the changes (apply). This separation is critical — you review infrastructure changes the same way you review code in a PR. Never apply without reviewing the plan.

- **terraform plan** — Read-only diff between desired state and actual state. Safe to run anytime. Makes infrastructure changes reviewable — the PR shows exactly what will be created, changed, or destroyed before anyone approves.
- **terraform apply** — Makes the changes. Should only run from a saved plan file in CI/CD, not ad-hoc.
- **Plan-as-PR-comment** — Post the plan output on the pull request so reviewers see exactly what infrastructure changes the code will produce before approving.
- **Manual approval gate** — Between plan and apply, especially for production. Prevents accidental changes.

### Modules
- **Root module** — The main Terraform config that calls child modules.
- **Child modules** — Reusable building blocks (e.g., "standard web app" = App Service + SQL + Key Vault + monitoring).
- **Module versioning** — Pin module versions so upstream changes do not break your infrastructure.
- **Feature flags** — Boolean variables like `enable_sql`, `enable_redis` to make modules flexible without forking. Solves the rigid module problem where a first version assumes every app needs the same resources.

### Workspaces vs Separate State
- **Workspaces** — Same config, different state per environment (dev/staging/prod). Simpler but less isolation.
- **Separate directories** — Different directories per environment with their own state. More isolation but more duplication.
- **Best practice** — One state file per blast radius. Do not put 100 resources in one state file.

### Common Pitfalls
- Running `apply` without locking — state corruption
- Portal/console changes without importing — drift
- Rigid modules that assume every app needs the same resources
- Not pinning provider versions — surprise breaking changes on `init`

### Terraform vs Pulumi vs CloudFormation
- **Terraform (HCL)** — Declarative, cloud-agnostic, huge provider ecosystem. State file as source of truth. Plan before apply. Mature, well-documented, large community.
- **Pulumi** — Real programming languages (Python, TypeScript, Go, C#) instead of HCL. Better for complex logic (loops, conditionals, abstractions). State managed by Pulumi Cloud or self-hosted backend. Growing ecosystem but smaller community than Terraform.
- **CloudFormation** — AWS-only, JSON/YAML, tightly integrated with AWS services. No state file management (AWS manages it). Free. But: vendor lock-in, verbose syntax, slow rollbacks, no multi-cloud.
- **When to choose** — Terraform: multi-cloud or team knows HCL. Pulumi: team prefers real programming languages and needs complex logic. CloudFormation: pure AWS shop that wants zero external dependencies.

### Terraform vs Ansible
- **Different jobs** — Terraform provisions infrastructure (create VMs, networks, databases, K8s clusters). Ansible configures what is already running (install packages, deploy apps, run scripts on servers). Terraform is "what should exist", Ansible is "what should be installed/configured on existing machines".
- **Declarative vs Procedural** — Terraform is fully declarative (describe desired state, it figures out how). Ansible playbooks are procedural (ordered list of tasks), though individual modules are idempotent.
- **State** — Terraform tracks state (knows what it created, can diff and update). Ansible is stateless (runs tasks every time, relies on idempotency to avoid duplicate changes).
- **When to use both** — Terraform creates the infrastructure (clusters, networking). Ansible configures test environments, runs deployment campaigns, sets up application stacks. Different layers, complementary tools.
- **Overlap** — Terraform can run scripts via `local-exec`/`remote-exec`, Ansible can create cloud resources via modules. But each is better at its primary job. Do not use Terraform to configure software, do not use Ansible to manage cloud infrastructure lifecycle.

## Sorulursa

> [!faq]- "Why Terraform instead of Pulumi or CloudFormation?"
> Terraform is cloud-agnostic — same tool for Azure, AWS, GCP. CloudFormation is AWS-only. Pulumi uses real programming languages which is nice but adds complexity — Terraform's declarative HCL is simpler for infrastructure that does not need loops and conditionals. Terraform skills transfer if you ever go multi-cloud.

> [!faq]- "How do you structure Terraform for a team?"
> One state file per blast radius — never put everything in one giant state. Shared modules for common patterns (standard web app, standard database). Remote state with locking on day one. Plan/apply separation in CI/CD — never apply without reviewing the plan. And a rule: no portal/console changes. Everything through code.
