---
tags:
  - education-kit
---

# GitHub Actions — Education Kit

## Key Concepts

### What GitHub Actions Is
GitHub Actions is a CI/CD platform built into GitHub — workflows defined in YAML that run on push, PR, schedule, or manual trigger. It uses a marketplace of community-built actions for common tasks (checkout, build, deploy, scan) and supports matrix builds, reusable workflows, and environment-specific deployments. Best for: teams on GitHub that want CI/CD without a separate platform, with easy setup and strong community ecosystem.

### Reusable Workflows
- **What** — Shared workflow definitions that multiple repos can call. Like Azure DevOps templates but native to GitHub.
- **How** — `uses: org/repo/.github/workflows/build.yml@main` in your workflow file. Pass inputs and secrets.
- **Why** — DRY principle for CI/CD. Change the shared workflow, every repo gets the update. Essential when managing many services from a shared workflow library.

### Breaking Change Detection
- **gRPC protos** — CI checks if proto file changes are backward-compatible (no removed fields, no renamed messages). Prevents a service from breaking its consumers. Tools like `buf breaking` compare current proto files against the base branch.
- **GraphQL schemas** — Same principle. Schema changes checked for backward compatibility before merge.
- **How** — Dedicated workflow runs on PRs that touch proto or schema files. Fails the PR if incompatible changes detected.

### Environment Deployments
- **Feature environments** — Each PR can deploy to a temporary environment for testing. Cleaned up on PR close.
- **Staging/Production** — Deployment workflows with environment protection rules (required reviewers, wait timers).
- **Cleanup** — Cleanup workflows tear down feature environments when the branch is deleted.

### NuGet Package Publishing
- **Shared libraries** — Common packages (messaging clients, database extensions, domain models) published as NuGet packages.
- **Workflow** — Version bump, build, test, publish to private NuGet feed. Other services reference packages by version.

### GitHub Actions vs Azure DevOps vs Jenkins
- **GitHub Actions** — YAML workflows, tight GitHub integration, marketplace for actions, matrix builds, reusable workflows. Free for public repos. Best when: code is on GitHub, team wants simple config, needs community actions.
- **Azure DevOps** — YAML pipelines, template system, service connections, approval gates, Azure integration. Better enterprise features (audit, compliance, fine-grained permissions). Best when: code is on Azure Repos or enterprise needs full ALM (boards, repos, pipelines, artifacts in one place).
- **Jenkins** — Self-hosted, Groovy-based Jenkinsfile, plugin ecosystem. Maximum flexibility but high maintenance burden. Best when: complex custom workflows, on-premise requirements, existing Jenkins infrastructure.
- **Key differences** — GitHub Actions: easiest setup, best for GitHub-native teams. Azure DevOps: best enterprise features, approval workflows. Jenkins: most flexible, highest maintenance cost. All three support YAML-based pipeline-as-code.

## Sorulursa

> [!faq]- "GitHub Actions vs Azure DevOps — which do you prefer?"
> GitHub Actions has a better developer experience — tighter integration with the repo, better marketplace, easier to read workflow files. Azure DevOps has more mature approval gates and environment management. For new projects, GitHub Actions is the better starting point. For enterprise environments with complex approval workflows, Azure DevOps still has an edge.

> [!faq]- "How do you handle secrets in GitHub Actions?"
> GitHub repository secrets and environment secrets. For more sensitive secrets, use a cloud secrets manager (e.g., Azure Key Vault) with OIDC federation — the workflow authenticates without storing credentials, then pulls secrets at runtime. No long-lived tokens.

> [!faq]- "How does breaking change detection work technically?"
> For gRPC: tools like `buf breaking` compare the current proto files against the base branch and flag backward-incompatible changes (removed fields, changed field numbers, renamed messages). For GraphQL: schema comparison tools check if the new schema is backward-compatible with the published one. Both run as PR checks and block merge if incompatible changes are detected.
