---
tags:
  - interview-kit
  - interview-kit/devops
up: [[do-kocsistem]]
---

*[[00-dashboard|Home]] > [[11-pillar-devops|DevOps]] > [[do-kocsistem|KOCSISTEM]] > TERRAFORM — Drift*

# TERRAFORM — Drift

> [!warning] **Soru:** "How do you prevent config drift?"

People kept making changes through the Azure Portal — especially during incidents when someone needed to scale up a service fast. I understood the motivation, but it meant what was defined in code and what was actually running in Azure were drifting apart. Next time someone ran `terraform plan`, it would show unexpected diffs and nobody knew if they were safe to apply or not.

I set up a nightly pipeline that ran `terraform plan` and alerted the team if there was any drift. That helped us catch changes within 24 hours. But the real fix was making Terraform changes fast enough that people didn't feel the need to go to the portal. If scaling up a service is a one-variable PR that gets applied in 10 minutes, the portal becomes unnecessary. Once we got there, drift almost disappeared.

I bring this up under DevOps because drift is the silent killer of [[ref-terraform#Common Pitfalls|infrastructure as code]] — if reality and code diverge, you lose the main benefit of IaC.

## Sorulursa

> [!faq]- "How did the nightly drift check work?"
> A scheduled pipeline ran `terraform plan` against every environment. If the plan showed any changes (exit code 2), it posted a message to our Slack channel with the diff. Someone would look at it the next morning and either import the change or revert it in the portal.

> [!faq]- "What if the portal change was intentional?"
> Then we'd import it into Terraform state and update the Terraform code to match. The point wasn't to prevent all manual changes — sometimes you need to act fast during an incident. The point was to make sure Terraform and reality stayed in sync afterward.

> [!faq]- "How did you make Terraform changes fast?"
> Template-based. Each environment had a var file with just the knobs — instance count, SKU, feature flags. Changing one variable, opening a PR, getting it approved, and running apply took about 10 minutes total. Compare that to clicking through the portal, which takes about the same time but doesn't leave a record.

> [!faq]- "Technical: Infrastructure drift detection approaches"
> There are several ways to detect drift: scheduled `terraform plan` (what we did), cloud-native tools like Azure Policy or AWS Config, or third-party tools like Driftctl or env0. Terraform plan is the simplest — it compares state with reality and shows the diff. The limitation is that it only checks resources Terraform manages — if someone creates a new resource manually, Terraform doesn't know about it. For that, you need a cloud inventory tool. The CNCF's guidelines on GitOps recommend treating infrastructure drift like a bug — detect it, alert on it, fix it.

> [!faq]- "What's the [[ref-terraform#Common Pitfalls|GitOps]] approach to preventing drift?"
> GitOps (as described by Weaveworks and the Argo project) says all changes should go through Git. The Git repo is the source of truth, and a reconciliation loop continuously applies the desired state. ArgoCD does this for Kubernetes; for cloud infrastructure, tools like Atlantis or Spacelift do it for Terraform. We didn't go full GitOps at KocSistem, but we followed the principle: Terraform code in Git, plan on PR, apply through pipeline only. The nightly drift check was our manual reconciliation loop.

---

*[[00-dashboard|Home]] > [[11-pillar-devops|DevOps]] > [[do-kocsistem|KOCSISTEM]]*
