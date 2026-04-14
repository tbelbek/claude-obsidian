---
tags:
  - interview-kit
  - interview-kit/agile
up: [[13-pillar-agile]]
---

*[[00-dashboard|Home]] > [[13-pillar-agile|Agile]] > VOLVO CARS*

# VOLVO CARS — Agile in Regulated Environments

At Volvo, the challenge was running Agile inside a heavily regulated environment. Automotive embedded software has [[ref-automotive-compliance#Compliance in Agile|compliance]] requirements — documentation, [[ref-automotive-compliance#Traceability|traceability]], [[ref-automotive-compliance#Traceability|audit trails]] — that don't naturally fit a 2-week sprint cadence.

What I owned long-term was making compliance and agility work together. The [[ref-automotive-compliance#ISO 26262 — Functional Safety|regulatory]] team wanted full documentation before any release. The dev team wanted to ship frequently. I [[ag-compliance|automated documentation generation]] via ZUUL CI — the post-merge pipeline generated compliance artifacts from Cynosure StateDB queries and Ansible playbook outputs — in the release pipeline — test reports, traceability matrices, change logs — all machine-generated as build artifacts. Dev team shipped as often as the pipeline allowed. Regulatory team got better docs than manual Word documents.

I also wrote technical docs that met Volvo's strict regulatory requirements — this wasn't optional. I coordinated between regulatory, QA, and test to make sure the pipeline served all three departments.

## Key Experiences
- [[ag-compliance|COMPLIANCE — regulatory wanted docs first, automated in pipeline]]

## Sorulursa

> [!faq]- "Did this approach scale to other teams at Volvo?"
> Other teams saw what we were doing and started asking about it. The pipeline-generated docs were more consistent and more complete than manual ones. I don't know if they fully adopted it after I left, but the approach was proven and documented.

---

*[[00-dashboard|Home]] > [[13-pillar-agile|Agile]]*
