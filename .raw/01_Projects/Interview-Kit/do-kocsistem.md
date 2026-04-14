---
tags:
  - interview-kit
  - interview-kit/devops
up: [[11-pillar-devops]]
---

*[[00-dashboard|Home]] > [[11-pillar-devops|DevOps]] > KOCSISTEM*

# KOCSISTEM — DevOps

I built KocSistem's DevOps practice from nothing. When I became Dev Lead, there was no CI/CD, no code review process, no branching strategy, no infrastructure as code. Developers built locally and copied files to servers. When production broke, we guessed.

## Tools I Used Here
| Tool | Ref | Tool | Ref |
|------|-----|------|-----|
| [[ref-azure-devops\|Azure DevOps]] | shared YAML templates | [[ref-terraform\|Terraform]] | state mgmt, drift detection |
| [[ref-cicd-security\|CI/CD Security]] | shift-left, zero pen-test | [[ref-dora\|DORA Metrics]] | 4 metrics, Grafana dashboards |
| [[ref-grafana-prometheus\|Grafana]] | RED/USE, rate-based alerting | [[ref-code-review\|Code Review]] | built from scratch |

Over two years (as Dev Lead then Technology Manager), I owned the entire DevOps stack. I built [[do-azdevops-zero|Azure DevOps pipelines]] with shared YAML templates, set up [[ref-terraform#State Management|Terraform]] for infrastructure, integrated [[ref-cicd-security#HOW WE USED IT|security scanning]] into every build, and tracked everything with [[ref-dora#HOW WE USED IT|DORA metrics]] in [[ref-grafana-prometheus#Grafana|Grafana]].

What I owned long-term was the pipeline platform and the security posture. The shared template repo I created meant onboarding a new app to CI/CD took hours instead of days. When I needed to add a security scan across all 10+ projects, I changed one template. The [[ref-cicd-security#HOW WE USED IT|pre-push hooks]] I set up caught real secrets in the first week. After three quarters of zero [[ref-cicd-security#Quality Gates|pen-test]] findings, the security team started sending other teams to copy our setup.

I also owned the infrastructure automation. [[do-terraform-state|Terraform state management]], [[do-terraform-drift|drift detection]], and the discipline of making infrastructure changes through code, not through the Azure Portal. That discipline didn't come for free — I had to earn it through incidents and fixes.

Results: weekly to daily deployments (7x), SLA breaches down 60%, bugs down 55%, zero pen-test findings, DevSecOps 4 Key Metrics at 75%.

## Tools Used
| | | |
|---|---|---|
| [[ref-azure-devops\|Azure DevOps]] | [[ref-terraform\|Terraform]] | [[ref-grafana-prometheus\|Grafana]] |
| [[ref-dora\|DORA Metrics]] | [[ref-cicd-security\|CI/CD Security]] | [[ref-code-review\|Code Review]] |

## Key Challenges
- [[do-terraform-state|TERRAFORM — State Corruption — 2 devs simultaneous apply, day-long fix]]
- [[do-terraform-drift|TERRAFORM — Drift — portal changes during incidents, nightly plan check]]
- [[ref-cicd-security#HOW WE USED IT|AZURE DEVOPS — Pipeline Gates — dep scanning backlash, zero pen-test 3 quarters]]
- [[ref-dora#HOW WE USED IT|GRAFANA — DORA Metrics — lead time gap, alert fatigue → rate-based]]
- [[do-azdevops-zero|AZURE DEVOPS — From Zero — no CI/CD → full pipelines, weekly→daily 7x]]

## Sorulursa

> [!faq]- "What lasted after you left?"
> The shared template repo, the Terraform setup, the [[ref-dora#Deployment Frequency|DORA]] dashboards, and the security scanning pipeline. I documented everything and made sure multiple people on the team could maintain it. The pre-push hooks and the nightly drift checks were still running when I checked in with former colleagues months later.

> [!faq]- "How did you balance building DevOps with your other responsibilities?"
> As Dev Lead, DevOps was maybe 40% of my time — the rest was team management and architecture. As Technology Manager, it shifted to 20% hands-on DevOps and 80% roadmap and people. By then the foundations were solid and the team could maintain them. I focused on metrics and improvements rather than building from scratch.

---

*[[00-dashboard|Home]] > [[11-pillar-devops|DevOps]]*
