---
tags:
  - interview-kit
  - interview-kit/devops
up: [[do-kocsistem]]
---

*[[00-dashboard|Home]] > [[11-pillar-devops|DevOps]] > [[do-kocsistem|KOCSISTEM]] > AZURE DEVOPS — From Zero*

# AZURE DEVOPS — From Zero

> [!warning] **Soru:** "Tell me about a complex problem you solved"

When I joined KocSistem as Dev Lead, there was no CI/CD. The team had never had a delivery platform — I needed to build one from nothing. Developers built locally, copied files to a server, and prayed. When something broke in production, we'd get a message saying "system is slow" and spend hours guessing what went wrong because there was no visibility.

I built everything from scratch on Azure DevOps. Created a shared template repository so each project's pipeline was just 15-20 lines referencing common build, test, and deploy stages. Set up Terraform for infrastructure instead of clicking through the Azure Portal. Added Prometheus and Grafana so we could actually see what was happening in production. Wrote runbooks that people actually used.

We went from weekly deployments to daily — 7x more frequent, with fewer rollbacks. Did a cloud migration for all apps with zero downtime and zero incidents. Mean time to detect issues dropped from hours to minutes.

This sits in my DevOps experience because building a delivery platform from scratch for a team that had nothing is the most complete DevOps challenge — you have to solve tooling, culture, and process all at once.

## Sorulursa

> [!faq]- "How did you approach it without disrupting ongoing work?"
> I didn't try to change everything at once. Started with one application — the one with the most deployment pain. Built the pipeline for that, showed it works, then moved to the next. Each new project was easier because the templates were already there. Teams saw the first team deploying daily and asked for the same setup.

> [!faq]- "How were the shared templates structured?"
> A separate Git repo called `pipeline-templates`. Inside: YAML templates for common stages — dotnet-build, dotnet-test, docker-build, deploy-to-k8s. Each template was parameterized: project path, .NET version, target environment. A project's pipeline file just referenced the templates and passed in its specific values. When I needed to add security scanning across all projects, I updated the template once.

> [!faq]- "How did you handle the cultural change?"
> Data first. I tracked deployment times, failure rates, and time spent in meetings vs coding. Showed the numbers as "am I seeing this right?" not "here's what's wrong." Then a pilot — one team, two sprints, daily deployments with automated checks. I volunteered our team, fixed flaky tests myself, was online at 6 AM for the first deploys. When it worked, other teams asked how.

> [!faq]- "Technical: Pipeline template patterns"
> Azure DevOps supports template references across repositories — similar to GitHub Actions reusable workflows. The pattern: a central `pipeline-templates` repo with YAML templates for common stages (build, test, scan, deploy). Each project's `azure-pipelines.yml` references these templates with `resources.repositories` and passes project-specific parameters. This is the DRY principle applied to CI/CD. When you need to change something across all projects (add a new scan, update a .NET version), you change it once in the template repo. The Azure DevOps documentation calls this "template expressions" — conditional logic, loops, and parameter types make templates flexible enough for most projects.

> [!faq]- "How did you handle environment-specific deployments?"
> Multi-stage pipeline: build → deploy to dev (automatic) → deploy to staging (automatic) → deploy to prod (manual approval). Each stage used the same Docker image but different environment variables and connection strings pulled from Azure Key Vault. The approval gate for production was a manual check in Azure DevOps — specific people had to click approve, and the pipeline showed them a summary of what was about to be deployed (image tag, commit list, test results).

> [!faq]- "How does this compare to GitOps approaches like [[ref-terraform#Common Pitfalls|ArgoCD]]?"
> Azure DevOps pipelines are push-based — the pipeline pushes changes to the target environment. ArgoCD is pull-based — it watches a Git repo and pulls the desired state. Pull-based is more resilient to pipeline failures and gives better audit trails. If I were setting it up today for Kubernetes workloads, I'd probably use ArgoCD or Flux. But at KocSistem we were deploying to Azure App Services and AKS, and Azure DevOps was already there. Pragmatic choice — use what you have.

## Also relevant to

- [[ls-transformation]] — The leadership/cultural change side of the same transformation
- [[ls-ownership]] — How I took ownership without a mandate
- [[12-pillar-leadership|Leadership Pillar]] — Driving change, data-first pitch, pilot approach

---

*[[00-dashboard|Home]] > [[11-pillar-devops|DevOps]] > [[do-kocsistem|KOCSISTEM]]*
