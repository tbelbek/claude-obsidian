---
tags:
  - education-kit
---

# CI/CD Security — Education Kit

## Key Concepts

### What CI/CD Security Is
CI/CD Security (DevSecOps) is the practice of embedding security checks into every stage of the build and deployment pipeline — not as a gate at the end, but as automated feedback throughout. Dependency scanning catches vulnerable packages, static analysis finds code-level vulnerabilities, secret detection prevents credentials from reaching Git, and quality gates block deployments that do not meet security thresholds. The goal: make security as automatic as running tests.

### Shift-Left Security
- **Concept** — Move security checks earlier in the development lifecycle. From pen-test, to CI pipeline, to pre-commit.
- **Why** — A vulnerability caught at build time takes 5 minutes to fix. Same vulnerability found in pen-test takes days.
- **OWASP DevSecOps** — Guidelines for integrating security into CI/CD.

### Scanning Types
- **Dependency scanning** — Check packages against known vulnerability databases (NVD — National Vulnerability Database). Tools: OWASP Dependency-Check, Snyk, Dependabot.
- **Static analysis (SAST)** — Analyze source code for security patterns (SQL injection, XSS, hardcoded credentials). Tools: SonarQube, Semgrep.
- **Container image scanning** — Check Docker images for OS and app-level vulnerabilities. Tools: Trivy, Grype.
- **Secret detection** — Scan code and commits for credentials, API keys, connection strings. Tools: git-secrets, detect-secrets, custom regex hooks.

### Quality Gates
- **What** — Build fails if security findings exceed threshold. Critical = block. Medium = warn. Low = log.
- **Tuning** — Spend time calibrating rules to avoid false positive fatigue while catching real issues. Takes effort upfront but pays off in developer trust.
- **Suppression file** — Version-controlled list of reviewed false positives. Requires PR review to change — not a free pass, but a tracked risk.

### Secrets Management
- **Never in code** — Connection strings, API keys must not be in config files or Git history.
- **Key Vault** — Use a secrets manager (Azure Key Vault, HashiCorp Vault). Pipeline pulls secrets at runtime via service connections.
- **Pre-push hook** — Regex patterns for common secret formats. Rejects push before it reaches the server.
- **git filter-branch** — Clean secrets from Git history if they were previously committed. Requires team re-clone.

## Sorulursa

> [!faq]- "How do you balance security scanning with developer velocity?"
> Fast feedback. Dependency scans run in parallel with the build — they do not add to the critical path. Static analysis runs on the diff only, not the entire codebase — much faster. Container scanning happens after the image is built, before push — adds ~30 seconds. The total security overhead is under 2 minutes per build. If it took 10 minutes, developers would find ways around it.

> [!faq]- "How do you handle a critical vulnerability in a dependency you can't upgrade?"
> Document it in the suppression file with an explanation, set a deadline for the upgrade, and add a compensating control (WAF rule, input validation, network policy). The suppression file is version-controlled and reviewed — it is not a free pass, it is a tracked risk with a plan.

> [!faq]- "How do you handle cultural resistance to security scanning?"
> Developers may complain that builds fail for issues they did not introduce. Explain that the vulnerability was already there — the pipeline just made it visible. For static analysis, spend time tuning rules — suppress noisy ones, keep the ones that catch real issues (SQL concatenation, hardcoded credentials, missing input validation). The key is reducing false positives so developers trust the tool instead of working around it.

> [!faq]- "What is the ROI of shift-left security?"
> Before shift-left: periodic pen-test findings, days to reproduce and fix each one, re-test cycle. After: findings caught at build time and fixed in minutes. The scanning overhead is under 2 minutes per build — trivial compared to the cost of fixing vulnerabilities found in production.
