---
tags:
  - interview-kit
  - interview-kit/devops
up: [[do-kocsistem]]
---

*[[00-dashboard|Home]] > [[11-pillar-devops|DevOps]] > [[do-kocsistem|KOCSISTEM]] > TERRAFORM — State Corruption*

# TERRAFORM — State Corruption

> [!warning] **Soru:** "Terraform experience?" / "Infrastructure challenges?"

At KocSistem, two developers ran `terraform apply` at almost the same time. This is what happens when the foundation of [[ref-terraform#State Management|infrastructure as code]] — state management — breaks down. This was early on — I hadn't set up state locking yet. Both runs tried to write to the state file at the same time, and it ended up broken. Some resources were tracked in state but didn't exist in Azure. Others existed in Azure but weren't in state. Some had wrong IDs.

I couldn't just run `terraform apply` again — it would try to create resources that already existed and fail. I had to fix it by hand: compare what Terraform thought existed with what actually existed in Azure, use `terraform import` for resources missing from state, and `terraform state rm` for entries pointing to nothing. It took most of a day.

After that, I set up state locking on Azure Blob Storage. When one pipeline is running `terraform apply`, the state file is locked and no other pipeline can touch it. Non-negotiable from that point on.

This sits in my DevOps experience because infrastructure as code only works if the state is reliable — when the foundation breaks, everything built on top of it becomes untrustworthy.

## Sorulursa

> [!faq]- "How does Terraform state locking work on Azure?"
> You store the state file in an Azure Blob Storage container with lease-based locking. When Terraform starts an operation, it takes a lease on the blob. If another process tries to start, it sees the lease and waits or fails. You set this up in the backend configuration — storage account name, container name, key, and `use_microsoft_entra_id` or access key for auth.

> [!faq]- "How did you find which resources were broken?"
> I ran `terraform plan` and looked at what it wanted to create or destroy. Then I checked the Azure Portal to see if those resources actually existed or not. For each mismatch: if the resource existed but wasn't in state, I ran `terraform import`. If it was in state but didn't exist, I ran `terraform state rm`. Tedious but straightforward.

> [!faq]- "How do you prevent this from happening again?"
> State locking is the main thing. But I also set up a rule: never run `terraform apply` locally. All applies go through the pipeline, which has a mutex on the state. If you need to test, run `terraform plan` locally — that's read-only and safe.

> [!faq]- "Technical: Terraform state internals"
> Terraform state is a JSON file that maps your HCL resources to real infrastructure IDs. When you run `terraform plan`, it reads state, queries the cloud provider, and computes the diff. The state file contains sensitive data (resource IDs, sometimes outputs with secrets), so it should be encrypted at rest and access-controlled. HashiCorp's documentation recommends remote backends for any team setup. Azure Blob Storage with lease-based locking is one option; Terraform Cloud and S3+DynamoDB are others. The key concept is that state is the source of truth — if state and reality diverge, Terraform gets confused.

> [!faq]- "What about Terraform workspaces vs separate state files?"
> We used workspaces — one state file per environment (dev, staging, prod) within the same configuration. The alternative is separate directories with separate state files, which gives more isolation but more code duplication. HashiCorp's Terraform Up & Running by Yevgeniy Brikman discusses both approaches. Workspaces worked for us because our environments were structurally identical — only the variable values differed.

> [!faq]- "How do you handle Terraform at scale — many resources, many teams?"
> We used modules to keep things manageable. Each module was a self-contained unit (e.g., "standard web app" = App Service + SQL + Key Vault + monitoring). Teams composed modules instead of writing raw resources. For cross-team coordination, we used a naming convention and tag policy enforced by Azure Policy. State was split per project — no single giant state file. This follows the principle from the Terraform documentation: "one state file per blast radius."

---

*[[00-dashboard|Home]] > [[11-pillar-devops|DevOps]] > [[do-kocsistem|KOCSISTEM]]*
