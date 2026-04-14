---
tags:
  - education-kit
---

# Azure DevOps — Education Kit

## Key Concepts

### What Azure DevOps Is

Azure DevOps is Microsoft's all-in-one DevOps platform — repos, CI/CD pipelines, boards, artifacts, and test plans in a single service. It is the enterprise-grade alternative to GitHub for teams that need fine-grained access control, approval workflows, and Azure integration. Best for organizations already in the Microsoft ecosystem.

### YAML Pipelines
- **What** — Pipeline-as-code in YAML. Version-controlled, reviewable, templatable.
- **Multi-stage** — Separate stages for build, test, scan, deploy. Each stage can have approval gates.
- **Triggers** — Branch triggers (`trigger: [main, release/*]`), PR triggers, scheduled triggers.

### Template System
- **What** — Reusable YAML templates across projects. A shared template repo that all pipelines reference.
- **How** — `resources.repositories` to reference the template repo, then `template:` to call specific templates with parameters.
- **Why** — Change once, propagate everywhere. Adding security scanning to many projects = one template change.

### Service Connections
- **What** — Secure connections to external services (Azure, Docker registries, Key Vault). No credentials in YAML.
- **Key Vault integration** — Pipeline pulls secrets at runtime via service connection. Secrets exist only in memory during the build.

### Approval Gates
- **What** — Manual or automated checks before a stage runs. Production deployments require specific people to approve.
- **Environment approvals** — Tied to deployment environments (dev, staging, prod). Different approvers per environment.

### Azure Blob Storage (for Terraform)
- **Remote state backend** — Terraform state stored in Azure Blob Storage with lease-based locking.
- **Artifact storage** — Build artifacts (test reports, packages) stored in Azure Storage for downstream stages.

## Sorulursa

> [!faq]- "Why Azure DevOps instead of Jenkins or GitHub Actions?"
> It depends on what is already available. Azure DevOps is a pragmatic choice when Microsoft licensing is in place. The YAML template system is powerful enough for most needs, and the service connection model makes secrets management clean. If starting fresh today with K8s workloads, GitHub Actions may be a better fit, but using what is available is often the right call.

> [!faq]- "How do you structure shared templates?"
> A separate Git repo for pipeline templates. Inside: YAML templates for common stages — dotnet-build, dotnet-test, docker-build, deploy-to-k8s. Each template is parameterized: project path, .NET version, target environment. A project's pipeline file becomes 15-20 lines referencing templates and passing parameters.

> [!faq]- "How do you handle secrets in pipelines?"
> Key Vault with service connections. The pipeline authenticates to Key Vault via a service principal, pulls secrets at runtime, and they exist only as environment variables during that build step. Never in YAML, never in logs. Add a pre-push hook that blocks commits containing secret patterns for an extra layer of protection.
