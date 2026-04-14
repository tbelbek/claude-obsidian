---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Azure DevOps — Quick Reference

> [!info] How I've used it: Built the entire CI/CD practice at KocSistem on Azure DevOps — shared YAML templates, multi-stage pipelines, service connections to Key Vault, quality gates. Also used at Combination alongside GitHub Actions.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#YAML Pipelines\|YAML pipelines]] | multi-stage, build→test→deploy, infrastructure as code | [[#Template System\|templates]] | shared YAML templates across 25+ projects at KocSistem |
| [[#Service Connections\|service connections]] | Key Vault, Azure subscriptions, secure credential access | [[#Approval Gates\|approval gates]] | manual approvals for prod, automated for dev/staging |
| [[#Azure Blob Storage (for Terraform)\|Blob Storage]] | Terraform remote state backend with lease-based locking | | |

## HOW WE USED IT

At KocSistem, Azure DevOps was the CI/CD platform for 10+ applications. I [[do-azdevops-zero|built everything from scratch]] — shared YAML template repository, multi-stage pipelines (build → test → scan → deploy), service connections to Azure Key Vault for secrets, and approval gates for production deployments.

At Combination, some services still run on Azure DevOps while newer ones use GitHub Actions. We're gradually migrating.

---

### What Azure DevOps Is

Azure DevOps is Microsoft's all-in-one DevOps platform — repos, CI/CD pipelines, boards, artifacts, and test plans in a single service. It's the enterprise-grade alternative to GitHub for teams that need fine-grained access control, approval workflows, and Azure integration. Best for organizations already in the Microsoft ecosystem.

## Key Concepts

### YAML Pipelines
- **What** — Pipeline-as-code in YAML. Version-controlled, reviewable, templatable.
- **Multi-stage** — Separate stages for build, test, scan, deploy. Each stage can have approval gates.
- **Triggers** — Branch triggers (`trigger: [main, release/*]`), PR triggers, scheduled triggers.

### Template System
- **What** — Reusable YAML templates across projects. A shared template repo that all pipelines reference.
- **How** — `resources.repositories` to reference the template repo, then `template:` to call specific templates with parameters.
- **Why** — Change once, propagate everywhere. Adding security scanning to 10+ projects = one template change.

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
> It was already there — KocSistem had Microsoft licensing. Pragmatic choice. The YAML template system is powerful enough for most needs, and the service connection model makes secrets management clean. If starting fresh today with K8s workloads, I might pick GitHub Actions, but at the time using what was available was the right call.

> [!faq]- "How did you structure the shared templates?"
> A separate Git repo called `pipeline-templates`. Inside: YAML templates for common stages — dotnet-build, dotnet-test, docker-build, deploy-to-k8s. Each template was parameterized: project path, .NET version, target environment. A project's pipeline file was 15-20 lines referencing templates and passing parameters.

> [!faq]- "How did you handle secrets in pipelines?"
> Azure Key Vault with service connections. The pipeline authenticates to Key Vault via a service principal, pulls secrets at runtime, and they exist only as environment variables during that build step. Never in YAML, never in logs. I also added a [[ref-cicd-security#Secrets Management|pre-push hook]] that blocked commits containing secret patterns.

---

*[[00-dashboard]]*
