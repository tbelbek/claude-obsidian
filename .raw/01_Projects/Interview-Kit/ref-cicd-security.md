---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# CI/CD Security — Quick Reference

> [!info] How I've used it: Embedded security scanning in every build at KocSistem. Dependency scanning, static analysis with tuned quality gates, secret detection with pre-push hooks. 3 consecutive quarters of zero pen-test findings. Migrated secrets to Azure Key Vault, cleaned Git history.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Shift-Left Security\|shift-left]] | scan in build, not after deploy, catch early | [[#Scanning Types\|scanning types]] | dependency, static analysis, secret detection |
| [[#Quality Gates\|quality gates]] | tuned thresholds, block on critical, suppress false positives | [[#Secrets Management\|secrets]] | Key Vault via CSI, git history cleaned, pre-push hooks |
| [[#HOW WE USED IT\|results]] | 3 quarters zero pen-test findings at KocSistem | | |

## HOW WE USED IT

At KocSistem, I [[ref-cicd-security#HOW WE USED IT|shifted security left]] — catching issues at build time instead of quarterly pen-test time. The pipeline failed on critical CVEs, blocked merges on security hotspots, and rejected pushes containing secret patterns.

**What I built:**
- Dependency scanning as a mandatory pipeline stage — if a library had a known critical CVE (Common Vulnerabilities and Exposures), the build failed with a clear message: which package, which CVE, what version to upgrade to
- Static analysis with SonarQube-style quality gates — new code couldn't merge if it introduced security hotspots (SQL concatenation, hardcoded credentials, missing input validation). Spent 2 weeks tuning rules to avoid false positive fatigue while catching real issues
- Secret migration from config files to Azure Key Vault — did it service by service (identify secrets, create Key Vault entries, update app, test, deploy). Then cleaned Git history with `git filter-branch` — whole team had to re-clone
- Pre-push Git hook scanning for common secret patterns (connection strings, API keys, base64 tokens). First week: blocked 4 pushes with real secrets
- Container image scanning before push to registry — critical vulnerability in base image → build fails

**Results:** 3 consecutive quarters of zero pen-test findings. Security team stopped treating us as a risk and started asking other teams to adopt our pipeline setup.

---

## Key Concepts

### What CI/CD Security Is
CI/CD Security (DevSecOps) is the practice of embedding security checks into every stage of the build and deployment pipeline — not as a gate at the end, but as automated feedback throughout. Dependency scanning catches vulnerable packages, static analysis finds code-level vulnerabilities, secret detection prevents credentials from reaching Git, and quality gates block deployments that don't meet security thresholds. The goal: make security as automatic as running tests.

### Shift-Left Security
- **Concept** — Move security checks earlier in the development lifecycle. From pen-test → to CI pipeline → to pre-commit.
- **Why** — A vulnerability caught at build time takes 5 minutes to fix. Same vulnerability found in pen-test takes days.
- **OWASP DevSecOps** — Guidelines for integrating security into CI/CD.

### Scanning Types
- **Dependency scanning** — Check packages against known vulnerability databases (NVD — National Vulnerability Database). Tools: OWASP Dependency-Check, Snyk, Dependabot.
- **Static analysis (SAST)** — Analyze source code for security patterns (SQL injection, XSS, hardcoded credentials). Tools: SonarQube, Semgrep.
- **Container image scanning** — Check Docker images for OS and app-level vulnerabilities. Tools: Trivy, Grype.
- **Secret detection** — Scan code and commits for credentials, API keys, connection strings. Tools: git-secrets, detect-secrets, custom regex hooks.

### Quality Gates
- **What** — Build fails if security findings exceed threshold. Critical = block. Medium = warn. Low = log.
- **Tuning** — [[ref-cicd-security#HOW WE USED IT|I spent 2 weeks calibrating rules]] to avoid false positive fatigue while catching real issues.
- **Suppression file** — Version-controlled list of reviewed false positives. Requires PR review to change.

### Secrets Management
- **Never in code** — Connection strings, API keys must not be in config files or Git history.
- **Key Vault** — Azure Key Vault (or HashiCorp Vault). Pipeline pulls secrets at runtime via service connections.
- **Pre-push hook** — Regex patterns for common secret formats. Rejects push before it reaches the server.
- **git filter-branch** — [[ref-cicd-security#HOW WE USED IT|Clean secrets from Git history]]. Requires team re-clone.

## Sorulursa

> [!faq]- "How do you balance security scanning with developer velocity?"
> Fast feedback. Dependency scans run in parallel with the build — they don't add to the critical path. Static analysis runs on the diff only, not the entire codebase — much faster. Container scanning happens after the image is built, before push — adds ~30 seconds. The total security overhead is under 2 minutes per build. If it took 10 minutes, developers would find ways around it.

> [!faq]- "How do you handle a critical vulnerability in a dependency you can't upgrade?"
> Document it in the suppression file with an explanation, set a deadline for the upgrade, and add a compensating control (WAF rule, input validation, network policy). The suppression file is version-controlled and reviewed — it's not a free pass, it's a tracked risk with a plan.

> [!faq]- "How did you handle the cultural resistance to security scanning?"
> Developers complained that builds failed for "something they didn't even change." I explained: the vulnerability was already there, the pipeline just made it visible. For static analysis, I spent 2 weeks tuning rules — suppressed noisy ones, kept the ones that caught real issues (SQL concatenation, hardcoded credentials, missing input validation). The key was reducing false positives so developers trusted the tool instead of working around it.

> [!faq]- "What was the ROI of shift-left security?"
> Before: quarterly pen-test findings, 2-3 days to reproduce and fix each one, re-test cycle. After: zero findings for 3 consecutive quarters. The security team stopped treating us as a risk and started asking other teams to adopt our pipeline setup. The scanning overhead was under 2 minutes per build — trivial compared to the cost of fixing vulnerabilities found in production.

---

*[[00-dashboard]]*
