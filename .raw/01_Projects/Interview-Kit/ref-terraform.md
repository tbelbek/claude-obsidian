---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Terraform — Quick Reference

> [!info] How I've used it: Currently at Combination managing Azure AKS infrastructure with Terraform (GP-IaC-K8s-AKS, GP-IaC-AKS). Previously built Terraform IaC at KocSistem from scratch — remote state, plan/apply in CI/CD, dealt with state corruption and drift.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#State Management\|state file]] | JSON mapping HCL→real infra, source of truth | [[#State Management\|remote state]] | Azure Blob/S3, required for teams, lease-based locking |
| [[#State Management\|state locking]] | prevents simultaneous apply, learned the hard way | [[#State Management\|state drift]] | reality diverges from code, nightly plan catches it |
| [[#Plan/Apply Workflow\|plan/apply]] | plan=read-only diff, apply=make changes, separate in CI | [[#Plan/Apply Workflow\|plan-as-PR-comment]] | reviewers see infra changes before approving |
| [[#Modules\|modules]] | reusable building blocks, feature flags for flexibility | [[#Workspaces vs Separate State\|workspaces]] | same config, different state per env (dev/staging/prod) |
| [[#HOW WE USE IT\|what we provision]] | AKS, Cilium, Chrono, Contour, Key Vault, ACR, DNS | [[#Terraform vs Pulumi vs CloudFormation\|vs Pulumi/CFN]] | TF=cloud-agnostic+HCL, Pulumi=real langs, CFN=AWS-only |
| [[#Terraform vs Ansible\|vs Ansible]] | TF=provision infra, Ansible=configure+deploy on machines | | |

## HOW WE USE IT

At Combination, I manage the Azure AKS cluster infrastructure with Terraform — the GP-IaC-K8s-AKS and GP-IaC-AKS repositories handle cluster provisioning, networking, Helm chart deployments (Cilium for CNI, Chrony for time sync), and Azure resource management. Kustomize handles the application-level deployment overlays on top.

At KocSistem, I built Terraform from scratch — Azure resources, remote state on Blob Storage, plan/apply in CI/CD pipelines. I dealt with [[do-terraform-state|state corruption]] and [[do-terraform-drift|drift detection]].

**What we provision with Terraform at Combination (GP-IaC-K8s-AKS + GP-IaC-AKS):**
- **AKS cluster** — node pools, VM sizes, autoscaling config, K8s version ← *the foundation — everything runs on this*
- **Azure networking** — VNet, subnets, NSGs, private endpoints ← *isolates the cluster from public internet*
- **Cilium (CNI)** — deployed via Helm chart in Terraform ← *replaces Azure CNI for better network policies and eBPF performance*
- **Chrony (NTP)** — deployed via Helm chart as DaemonSet ← *consistent timestamps across nodes for log correlation and tracing*
- **Contour (Ingress)** — Envoy-based ingress controller with HPA, PDB, NetworkPolicy ← *L7 routing, TLS termination, rate limiting*
- **Nginx (Ingress)** — secondary/fallback ingress ← *compatibility for legacy routes*
- **CloudFlare WARP** — Zero Trust networking ← *secure cluster access without VPN*
- **External DNS** — auto-manages Azure DNS records from K8s resources ← *no manual DNS updates when services change*
- **Feature Cleanup** — utility chart for cleaning up feature branch deployments ← *auto-deletes temporary environments*
- **Azure Key Vault** — secrets store, accessed by pods via CSI driver ← *secrets never stored in K8s, never in Git*
- **Azure Container Registry (ACR)** — image registry with retention policies ← *every service pushes images here, K8s pulls from here*
- **Azure Monitor** — cluster-level metrics and diagnostics ← *AKS health, node status, API server metrics*

**What we built at KocSistem:**
- [[do-terraform-state|State locking after a corruption incident]] ← *two devs applied at the same time, broke state, took a day to fix*
- [[do-terraform-drift|Nightly drift detection pipeline]] ← *caught portal changes within 24 hours instead of weeks*
- Shared modules for standard app stacks ← *one module = App Service + SQL + Key Vault + monitoring*
- Plan/apply separation in Azure DevOps pipelines ← *plan as PR comment, apply only after approval*

---

## Key Concepts

### What Terraform Is
Terraform is an Infrastructure-as-Code tool by HashiCorp that lets you define cloud resources (VMs, networks, databases, K8s clusters) in declarative HCL files. You describe the desired state, Terraform figures out what to create, change, or destroy. It's cloud-agnostic — same tool for Azure, AWS, GCP — and tracks everything in a state file so it knows what it manages. Best for: provisioning and managing cloud infrastructure reproducibly, with plan/apply workflow that shows exactly what will change before making any changes.

### State Management
- **State file** — JSON mapping of your HCL resources to real infrastructure IDs. Source of truth for Terraform.
- **Remote state** — Store state in a shared backend (Azure Blob Storage, S3, Terraform Cloud) instead of locally. Required for team use. *(we used this to prevent the state corruption that happened when two developers ran apply simultaneously at KocSistem)*
- **State locking** — Prevents two people running `apply` at the same time. Uses lease-based locking on the backend. [[do-terraform-state|I learned this the hard way]]. *(we learned this the hard way — two simultaneous applies corrupted state, took a full day to fix by hand with terraform import and state rm)*
- **State drift** — When reality diverges from state because someone changed infrastructure manually. [[do-terraform-drift|I set up nightly plan checks to catch this]].
- **terraform import** — Bring existing resources into state management without recreating them.
- **terraform state rm** — Remove a resource from state without destroying it in the cloud.

### Plan/Apply Workflow
Plan/apply is Terraform's two-step workflow: first show what will change (plan), then make the changes (apply). This separation is critical — you review infrastructure changes the same way you review code in a PR. Never apply without reviewing the plan.

- **terraform plan** — Read-only diff between desired state and actual state. Safe to run anytime. *(we used this to make infrastructure changes reviewable at KocSistem — the PR shows exactly what will be created, changed, or destroyed before anyone approves)*
- **terraform apply** — Makes the changes. Should only run from a saved plan file in CI/CD, not ad-hoc.
- **Plan-as-PR-comment** — Post the plan output on the pull request so reviewers see exactly what infrastructure changes the code will produce before approving.
- **Manual approval gate** — Between plan and apply, especially for production. Prevents accidental changes.

### Modules
- **Root module** — The main Terraform config that calls child modules.
- **Child modules** — Reusable building blocks (e.g., "standard web app" = App Service + SQL + Key Vault + monitoring).
- **Module versioning** — Pin module versions so upstream changes don't break your infrastructure.
- **Feature flags** — Boolean variables like `enable_sql`, `enable_redis` to make modules flexible without forking. *(we used this to solve the rigid module problem at KocSistem — first version assumed every app needed SQL, but some only used Redis. Feature flags made modules flexible without forking)*

### Workspaces vs Separate State
- **Workspaces** — Same config, different state per environment (dev/staging/prod). Simpler but less isolation.
- **Separate directories** — Different directories per environment with their own state. More isolation but more duplication.
- **Best practice** — One state file per blast radius. Don't put 100 resources in one state file.

### Common Pitfalls
- Running `apply` without locking → state corruption
- Portal changes without importing → drift
- Rigid modules that assume every app needs the same resources
- Not pinning provider versions → surprise breaking changes on `init`

### Terraform vs Pulumi vs CloudFormation
- **Terraform (HCL)** — Declarative, cloud-agnostic, huge provider ecosystem. State file as source of truth. Plan before apply. Mature, well-documented, large community. *(we use this at Combination and KocSistem — skills transfer across clouds)*
- **Pulumi** — Real programming languages (Python, TypeScript, Go, C#) instead of HCL. Better for complex logic (loops, conditionals, abstractions). State managed by Pulumi Cloud or self-hosted backend. Growing ecosystem but smaller community than Terraform.
- **CloudFormation** — AWS-only, JSON/YAML, tightly integrated with AWS services. No state file management (AWS manages it). Free. But: vendor lock-in, verbose syntax, slow rollbacks, no multi-cloud.
- **When to choose** — Terraform: multi-cloud or team knows HCL. Pulumi: team prefers real programming languages and needs complex logic. CloudFormation: pure AWS shop that wants zero external dependencies. *(I chose Terraform because it's cloud-agnostic and the declarative model fits infrastructure well — you don't need loops and conditionals for most infra)*

### Terraform vs Ansible
- **Different jobs** — Terraform provisions infrastructure (create VMs, networks, databases, K8s clusters). Ansible configures what's already running (install packages, deploy apps, run scripts on servers). Terraform is "what should exist", Ansible is "what should be installed/configured on existing machines".
- **Declarative vs Procedural** — Terraform is fully declarative (describe desired state, it figures out how). Ansible playbooks are procedural (ordered list of tasks), though individual modules are idempotent.
- **State** — Terraform tracks state (knows what it created, can diff and update). Ansible is stateless (runs tasks every time, relies on idempotency to avoid duplicate changes).
- **When to use both** — Terraform creates the AKS cluster and networking. Ansible configures test environments, runs deployment campaigns, sets up emulator stacks. *(at Combination we use Terraform for infra, at Volvo we used Ansible for test orchestration — different layers, complementary tools)*
- **Overlap** — Terraform can run scripts via `local-exec`/`remote-exec`, Ansible can create cloud resources via modules. But each is better at its primary job. Don't use Terraform to configure software, don't use Ansible to manage cloud infrastructure lifecycle.

## Sorulursa

> [!faq]- "Why Terraform instead of Pulumi or CloudFormation?"
> Terraform is cloud-agnostic — same tool for Azure, AWS, GCP. CloudFormation is AWS-only. Pulumi uses real programming languages which is nice but adds complexity — Terraform's declarative HCL is simpler for infrastructure that doesn't need loops and conditionals. At KocSistem and Combination, we're Azure-only, but Terraform skills transfer if we ever go multi-cloud.

> [!faq]- "How do you structure Terraform for a team?"
> One state file per blast radius — never put everything in one giant state. Shared modules for common patterns (standard web app, standard database). Remote state with locking on day one. Plan/apply separation in CI/CD — never apply without reviewing the plan. And a rule: no Portal changes. Everything through code.

---

*[[00-dashboard]]*
