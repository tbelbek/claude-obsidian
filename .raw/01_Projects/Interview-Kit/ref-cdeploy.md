---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# CDeploy — Quick Reference

> [!info] How I've used it: At Combination, CDeploy is the Python framework for deployment orchestration — managing Azure AKS clusters, CloudFlare DNS, Kubernetes resources, Kafka topics, and GraphQL schema management. I maintain and extend it as part of my infrastructure automation work.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#What CDeploy Manages\|what it manages]] | AKS, DNS, K8s resources, Kafka topics, GraphQL schemas | [[#Architecture\|architecture]] | Python CLI, YAML config, idempotent operations |
| [[#Why a Custom Framework\|why custom]] | Azure/CloudFlare/K8s/Kafka in one tool, not 4 separate | | |

## HOW WE USE IT

At Combination, CDeploy (`DevEnv-CDeploy`) is the central infrastructure automation framework. It's a Python application that orchestrates everything outside of the application code itself — cluster provisioning, DNS management, deployment workflows, and topic management.

I maintain and extend CDeploy as part of my day-to-day work. When a new service needs a Kafka topic, a CloudFlare DNS entry, or a Kubernetes namespace configured, it goes through CDeploy — not manual clicks in the Azure Portal.

---

## Key Concepts

### What CDeploy Manages
- **Azure AKS** — Cluster provisioning, node pool configuration, networking. The `cdeploy/azure/` module handles Azure API calls for AKS, storage accounts, Key Vault, and other Azure resources.
- **Kubernetes** — Namespace creation, resource quotas, RBAC policies, Helm chart deployments. The `cdeploy/kubernetes/` module wraps kubectl and Helm CLI operations.
- **CloudFlare** — DNS record management and CloudFlare Workers deployment. The `cdeploy/cloudflare/` module handles DNS entries for service endpoints.
- **Kafka** — Topic creation, partition configuration, retention policies. The `cdeploy/kafka.py` module manages Kafka topic lifecycle.
- **GraphQL** — Schema management and federation configuration. The `cdeploy/graphql.py` module coordinates with the GP-GraphQL-SchemaRegistry.
- **GitHub** — Repository and workflow management. The `cdeploy/github/` module handles GitHub API interactions.

### Architecture
- **CLI wrappers** — CDeploy wraps command-line tools (kubectl, helm, docker, terraform) in Python functions with error handling, retries, and structured output.
- **Templates** — Deployment templates for common patterns (new service setup, environment creation, DNS configuration).
- **Environment configs** — `environments.py` manages environment-specific settings (dev/staging/prod) with consistent naming.
- **Resource definitions** — `resources.py` defines infrastructure resources declaratively — CDeploy figures out how to create or update them.

### Why a Custom Framework
- **Consistency** — 60+ microservices need consistent infrastructure. CDeploy ensures every service gets the same namespace structure, resource quotas, and DNS configuration.
- **Speed** — Setting up a new service environment (Kubernetes namespace, Kafka topics, DNS, monitoring) takes one CDeploy command instead of 30 minutes of portal clicking.
- **Auditability** — All infrastructure changes go through CDeploy, which logs every action. No mystery changes from someone clicking in the Azure Portal.

## Sorulursa

> [!faq]- "Why a custom Python framework instead of Terraform for everything?"
> Terraform handles the infrastructure layer (AKS cluster, networking, storage). CDeploy handles the application layer on top — Kubernetes resources, Kafka topics, DNS entries, schema registry. Terraform is declarative and great for infrastructure that changes rarely. CDeploy is imperative and great for the operational tasks that happen daily — deploying a new service, creating a topic, updating DNS. They complement each other.

> [!faq]- "How is CDeploy structured technically?"
> Python package with submodules per integration (azure/, cloudflare/, github/, kubernetes/). CLI wrappers for external tools. A central `resources.py` for declarative resource definitions and `environments.py` for environment configs. Templates for common operations. Each module has its own error handling and retry logic. The framework is version-controlled and shared across all 60+ services.

> [!faq]- "Could this be replaced with Helm charts or Kustomize?"
> Helm and Kustomize handle Kubernetes resources, but CDeploy does more — it also manages Azure resources, CloudFlare DNS, Kafka topics, and GraphQL schemas. You'd need Helm + a Terraform module + a DNS management tool + a Kafka topic manager to replace what CDeploy does in one framework. For a platform with 60+ services, having one tool that handles all of it is more maintainable.

---

*[[00-dashboard]]*
