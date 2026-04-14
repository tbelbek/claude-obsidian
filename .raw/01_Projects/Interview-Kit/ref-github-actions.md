---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# GitHub Actions — Quick Reference

> [!info] How I've used it: At Combination, GitHub Actions is the primary CI/CD platform for 60+ microservices. Reusable workflows from a shared library (DevEnv-GitHub-Workflows). Breaking change detection for gRPC protos and GraphQL schemas. Build, test, deploy, cleanup workflows.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Reusable Workflows\|reusable workflows]] | shared library, DevEnv-GitHub-Workflows, 60+ services | [[#Breaking Change Detection\|breaking changes]] | buf breaking for gRPC, schema diff for GraphQL |
| [[#Environment Deployments\|environments]] | feature→staging→prod, cleanup on branch delete | [[#NuGet Package Publishing\|NuGet publishing]] | auto-version, push to registry on merge |
| [[#HOW WE USE IT\|workflow types]] | build, check, deploy, cleanup, breaking, publish, iac | [[#GitHub Actions vs Azure DevOps vs Jenkins\|vs AzDO vs Jenkins]] | GHA=GitHub-native, AzDO=enterprise, Jenkins=flexible |

## HOW WE USE IT

At Combination (KSD), every microservice has GitHub Actions workflows:
- **build.yml** — Compile, test, build container image
- **check.yml** — Code quality checks
- **deploy.yml** — Deploy to Kubernetes environments (feature, staging, production)
- **cleanup_deploy.yml** — Resource cleanup after feature branch deletion
- **breaking.yml** — Breaking change detection for gRPC proto files and GraphQL schemas
- **publish_nuget.yml** — NuGet package publishing for shared libraries
- **iac.yml** — Infrastructure-as-Code deployment

All workflows reference reusable workflows from a shared library: `Keep-Social-Dev/DevEnv-GitHub-Workflows/.github/workflows/`.

---

## Key Concepts

### What GitHub Actions Is
GitHub Actions is a CI/CD platform built into GitHub — workflows defined in YAML that run on push, PR, schedule, or manual trigger. It uses a marketplace of community-built actions for common tasks (checkout, build, deploy, scan) and supports matrix builds, reusable workflows, and environment-specific deployments. Best for: teams on GitHub that want CI/CD without a separate platform, with easy setup and strong community ecosystem.

### Reusable Workflows
- **What** — Shared workflow definitions that multiple repos can call. Like Azure DevOps templates but native to GitHub.
- **How** — `uses: org/repo/.github/workflows/build.yml@main` in your workflow file. Pass inputs and secrets.
- **Why** — DRY principle for CI/CD. Change the shared workflow, every repo gets the update. At Combination, 60+ repos share the same build/deploy workflows.

### Breaking Change Detection
- **gRPC protos** — CI checks if proto file changes are backward-compatible (no removed fields, no renamed messages). Prevents a service from breaking its consumers.
- **GraphQL schemas** — Same principle. Schema changes checked for backward compatibility before merge.
- **How** — Dedicated `breaking.yml` workflow runs on PRs that touch proto or schema files. Fails the PR if incompatible changes detected.

### Environment Deployments
- **Feature environments** — Each PR can deploy to a temporary environment for testing. Cleaned up on PR close.
- **Staging/Production** — Deployment workflows with environment protection rules (required reviewers, wait timers).
- **Cleanup** — `cleanup_deploy.yml` tears down feature environments when the branch is deleted.

### NuGet Package Publishing
- **Shared libraries** — Common packages (RabbitMQ client, MongoDB extensions, domain models) published as NuGet packages.
- **Workflow** — Version bump → build → test → publish to private NuGet feed. Other services reference packages by version.

### GitHub Actions vs Azure DevOps vs Jenkins
- **GitHub Actions** — YAML workflows, tight GitHub integration, marketplace for actions, matrix builds, reusable workflows. Free for public repos. Best when: code is on GitHub, team wants simple config, needs community actions. *(we use this at Combination for 60+ services with shared reusable workflows)*
- **Azure DevOps** — YAML pipelines, template system, service connections, approval gates, Azure integration. Better enterprise features (audit, compliance, fine-grained permissions). Best when: code is on Azure Repos or enterprise needs full ALM (boards, repos, pipelines, artifacts in one place). *(we used this at KocSistem — shared YAML templates across 25+ projects)*
- **Jenkins** — Self-hosted, Groovy-based Jenkinsfile, plugin ecosystem. Maximum flexibility but high maintenance burden. Best when: complex custom workflows, on-premise requirements, existing Jenkins infrastructure.
- **Key differences** — GitHub Actions: easiest setup, best for GitHub-native teams. Azure DevOps: best enterprise features, approval workflows. Jenkins: most flexible, highest maintenance cost. All three support YAML-based pipeline-as-code.

## Sorulursa

> [!faq]- "GitHub Actions vs Azure DevOps — which do you prefer?"
> GitHub Actions has a better developer experience — tighter integration with the repo, better marketplace, easier to read workflow files. Azure DevOps has more mature approval gates and environment management. At Combination, we're gradually moving everything to GitHub Actions. For new projects, I'd pick GitHub Actions. For enterprise environments with complex approval workflows, Azure DevOps still has an edge.

> [!faq]- "How do you handle secrets in GitHub Actions?"
> GitHub repository secrets and environment secrets. For more sensitive secrets, we use Azure Key Vault with OIDC federation — the workflow authenticates to Azure without storing credentials, then pulls secrets from Key Vault. No long-lived tokens.

> [!faq]- "How does the breaking change detection work technically?"
> For gRPC: we use `buf breaking` which compares the current proto files against the base branch and flags backward-incompatible changes (removed fields, changed field numbers, renamed messages). For GraphQL: HotChocolate's schema comparison tool checks if the new schema is backward-compatible with the published one in the SchemaRegistry.

---

*[[00-dashboard]]*
