---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Application Security (OWASP) — Senior Interview Questions

> [!tip] Quick review before interview. Answers are 2-3 sentences — enough to show you know it, detailed enough to survive a follow-up.

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Injection Attacks\|SQL injection]] | parameterized queries, never concatenate user input | [[#Cross-Site Scripting (XSS)\|XSS]] | encode output, CSP headers, sanitize HTML |
| [[#Cross-Site Request Forgery (CSRF)\|CSRF]] | anti-forgery tokens, SameSite cookies | [[#Identification and Authentication Failures (A07)\|broken auth]] | MFA, session timeout, password hashing (bcrypt) |
| [[#Broken Access Control (A01)\|access control]] | RBAC, deny by default, check ownership | [[#Cryptographic Failures (A02)\|crypto failures]] | use standard libs, rotate keys, encrypt at rest |
| [[#Security Misconfiguration (A05)\|misconfiguration]] | default creds, verbose errors, open ports | [[#Insecure Deserialization (A08)\|deserialization]] | never deserialize untrusted data, type allowlists |
| [[#Server-Side Request Forgery — SSRF (A10)\|SSRF]] | allowlist URLs, block internal IPs | [[#Security Logging and Monitoring (A09)\|security logging]] | audit trails, failed login alerts, tamper-proof logs |
| [[#How I Applied This\|at KocSistem]] | Key Vault, zero pen-test findings 3 quarters | | |

---

## OWASP Top 10 — Overview

### Q1. What is the OWASP Top 10 and why does it matter?
The OWASP Top 10 is a regularly updated list of the most critical web application security risks, maintained by the Open Web Application Security Project. It matters because it serves as a baseline standard for security awareness — most pen-test firms and compliance frameworks (PCI-DSS, ISO 27001) reference it directly. If your app is vulnerable to something in the Top 10, you have no excuse.

### Q2. Name the current OWASP Top 10 categories (2021).
A01: Broken Access Control, A02: Cryptographic Failures, A03: Injection, A04: Insecure Design, A05: Security Misconfiguration, A06: Vulnerable and Outdated Components, A07: Identification and Authentication Failures, A08: Software and Data Integrity Failures, A09: Security Logging and Monitoring Failures, A10: Server-Side Request Forgery (SSRF).

---

## Injection Attacks

### Q3. What is SQL injection and how does it work?
SQL injection occurs when user input is concatenated directly into a SQL query string, allowing an attacker to alter the query logic. Example: `SELECT * FROM users WHERE name = '' OR '1'='1'` — the injected `OR '1'='1'` makes the WHERE clause always true, returning all rows. It can lead to data exfiltration, data modification, or even OS command execution via `xp_cmdshell`.

### Q4. How do you prevent SQL injection?
Use parameterized queries (prepared statements) — always. In .NET: `command.Parameters.AddWithValue("@name", userInput)` or use an ORM like EF Core / Dapper which parameterizes by default. Never concatenate user input into SQL strings. Defense in depth: input validation, least-privilege database accounts, WAF rules as an additional layer.

### Q5. What is the difference between parameterized queries and stored procedures for SQL injection prevention?
Parameterized queries separate data from code at the protocol level — the database engine never interprets parameters as SQL. Stored procedures are also safe IF they use parameters internally, but a stored procedure that concatenates input into dynamic SQL (`EXEC('SELECT * FROM ' + @table)`) is just as vulnerable. Parameterized queries are the fundamental fix; stored procedures are not inherently safe.

### Q6. What is ORM injection and can ORMs be vulnerable?
ORMs like EF Core prevent injection by default because they parameterize queries. However, raw SQL methods (`FromSqlRaw`, `ExecuteSqlRaw`) are vulnerable if you concatenate input. Dapper is safe with parameterized queries but allows raw SQL by design. Rule: any time you write raw SQL through an ORM, treat it with the same discipline as writing raw ADO.NET.

---

## Cross-Site Scripting (XSS)

### Q7. What is XSS and what are the three types?
XSS allows an attacker to inject malicious scripts into web pages viewed by other users. **Stored XSS** — payload is saved in the database and served to every user who views the page (most dangerous). **Reflected XSS** — payload is in the URL/request and reflected in the response (requires victim to click a crafted link). **DOM-based XSS** — payload is processed entirely client-side by JavaScript manipulating the DOM without server involvement.

### Q8. How do you prevent stored XSS?
Output encoding — encode all user-supplied content when rendering it in HTML (`&lt;script&gt;` instead of `<script>`). In .NET, Razor does this by default with `@Model.Name`. Use `@Html.Raw()` only when you explicitly trust the content. Additionally: Content Security Policy (CSP) headers to block inline scripts, input validation as defense in depth (but never rely on it alone — encoding is the primary defense).

### Q9. How do you prevent reflected XSS?
Same output encoding principle — encode user input before reflecting it in the response. Validate and reject unexpected input server-side. Set `X-Content-Type-Options: nosniff` to prevent MIME-type sniffing. Use CSP headers to restrict script sources. HTTP-only cookies prevent session theft even if XSS succeeds.

### Q10. What is DOM-based XSS and why is it harder to detect?
DOM-based XSS happens when JavaScript reads from an attacker-controlled source (`location.hash`, `document.referrer`, `postMessage`) and writes to a dangerous sink (`innerHTML`, `eval`, `document.write`) without sanitization. It never touches the server, so server-side WAFs and logging don't see it. Prevention: use `textContent` instead of `innerHTML`, avoid `eval()`, sanitize with libraries like DOMPurify.

### Q11. What is Content Security Policy (CSP) and how does it mitigate XSS?
CSP is an HTTP response header that tells the browser which sources of content (scripts, styles, images) are allowed. `Content-Security-Policy: script-src 'self'` blocks inline scripts and scripts from external domains. It's the strongest defense against XSS because even if an attacker injects a script tag, the browser refuses to execute it. Start with report-only mode to identify violations before enforcing.

---

## Cross-Site Request Forgery (CSRF)

### Q12. What is CSRF and how does it work?
CSRF tricks a logged-in user's browser into making an unintended request to a site where they're authenticated. Example: a victim visits a malicious page containing `<img src="https://bank.com/transfer?to=attacker&amount=10000">` — the browser sends the request with the victim's cookies automatically. The server can't distinguish this from a legitimate request.

### Q13. How do you prevent CSRF?
Anti-forgery tokens (synchronizer token pattern) — the server generates a unique token per session/form, embeds it in the form, and validates it on submission. In ASP.NET Core: `[ValidateAntiForgeryToken]` attribute. For SPAs: use `SameSite=Strict` or `SameSite=Lax` cookie attribute, which prevents the browser from sending cookies on cross-origin requests. Double-submit cookie pattern is another option for stateless APIs.

### Q14. Does SameSite cookie attribute eliminate the need for CSRF tokens?
`SameSite=Lax` (default in modern browsers) blocks cross-site POST requests but allows top-level navigations (GET). `SameSite=Strict` blocks all cross-site requests. It significantly reduces CSRF risk but isn't a complete replacement — older browsers may not support it, and subdomain attacks can bypass it. Defense in depth: use both SameSite cookies AND anti-forgery tokens.

---

## Broken Access Control (A01)

### Q15. What is broken access control and why is it #1 on OWASP?
Broken access control means users can act outside their intended permissions — accessing other users' data, modifying records they shouldn't, or escalating privileges. It's #1 because it's the most commonly found vulnerability in real-world applications. Examples: IDOR (Insecure Direct Object Reference), missing function-level access checks, path traversal.

### Q16. What is IDOR and how do you prevent it?
IDOR (Insecure Direct Object Reference) occurs when an application exposes internal object references (database IDs, file paths) and doesn't verify that the requesting user is authorized to access that object. Example: `/api/orders/123` — changing to `/api/orders/124` returns another user's order. Prevention: always verify authorization server-side — check that the requesting user owns or has access to the requested resource. Use GUIDs instead of sequential IDs to reduce enumeration risk (but this is obfuscation, not security).

### Q17. How do you implement proper authorization in a microservices architecture?
JWT claims carry the user's roles and tenant ID. Each service validates the token AND checks authorization against its own data — never trust that another service already checked. Use policy-based authorization in .NET (`[Authorize(Policy = "CanEditOrder")]`) with resource-based checks. For multi-tenant systems, every database query must include a tenant filter — missing this once means data leakage.

### Q18. What is privilege escalation and how do you prevent it?
Vertical privilege escalation: a regular user gains admin access. Horizontal: a user accesses another user's data at the same privilege level. Prevention: deny by default (whitelist allowed actions, don't blacklist forbidden ones), enforce authorization at every layer (API gateway, service, database), audit logs for privilege changes, separate admin endpoints with additional authentication factors.

---

## Cryptographic Failures (A02)

### Q19. What are common cryptographic failures?
Storing passwords in plaintext or with weak hashing (MD5, SHA-1 without salt). Transmitting sensitive data without TLS. Using outdated encryption algorithms (DES, RC4). Hardcoding encryption keys in source code. Not rotating keys. Exposing sensitive data in logs or error messages.

### Q20. How should passwords be stored?
Use a slow, salted hashing algorithm designed for passwords: bcrypt, scrypt, or Argon2. Never MD5 or SHA-256 — they're fast, which means brute-force is fast. Each password gets a unique random salt. In .NET: use `Microsoft.AspNetCore.Identity` which uses PBKDF2 with 100K+ iterations by default, or use BCrypt.Net for bcrypt.

### Q21. What is the difference between encryption and hashing?
Encryption is reversible (plaintext → ciphertext → plaintext with the right key). Hashing is one-way (input → fixed-length digest, no reversal). Use encryption for data you need to read back (credit card numbers, PII at rest). Use hashing for data you only need to verify (passwords, integrity checks). Using encryption for passwords is wrong — if the key leaks, all passwords are exposed.

---

## Security Misconfiguration (A05)

### Q22. What are common security misconfigurations?
Default credentials left unchanged, unnecessary services/ports open, directory listing enabled, verbose error messages exposing stack traces in production, CORS set to `*`, debug endpoints left enabled, missing security headers (HSTS, CSP, X-Frame-Options), unnecessary HTTP methods enabled (TRACE, PUT, DELETE on static servers).

### Q23. How do you prevent security misconfiguration?
Hardened base configurations (infrastructure as code ensures consistency). Automated scanning for common misconfigurations. Remove unused features, frameworks, and dependencies. Different credentials per environment. Review and minimize CORS policies. Disable debug mode and detailed errors in production. Security headers checklist enforced via middleware.

### Q24. What security headers should every application set?
`Strict-Transport-Security` (HSTS) — force HTTPS. `Content-Security-Policy` — control allowed content sources. `X-Content-Type-Options: nosniff` — prevent MIME sniffing. `X-Frame-Options: DENY` — prevent clickjacking. `Referrer-Policy: strict-origin-when-cross-origin` — limit referrer leakage. `Permissions-Policy` — control browser features (camera, geolocation). These should be applied as default middleware, not per-endpoint.

---

## Server-Side Request Forgery — SSRF (A10)

### Q25. What is SSRF and why is it dangerous?
SSRF occurs when an attacker can make the server send HTTP requests to arbitrary destinations — including internal services, metadata endpoints, and private networks. Example: an image URL feature that fetches `http://169.254.169.254/latest/meta-data/` to steal cloud instance credentials. It's especially dangerous in cloud environments where the metadata endpoint reveals IAM credentials, and in microservice architectures where internal services trust requests from other internal services.

### Q26. How do you prevent SSRF?
Whitelist allowed domains/IPs — never let user input control the full URL. Block requests to private IP ranges (10.x, 172.16.x, 192.168.x, 169.254.x) at the application and network level. Disable unnecessary URL schemes (file://, gopher://). Use a dedicated egress proxy for outbound requests. In cloud: use IMDSv2 (requires a PUT request with a token, which SSRF attacks can't easily generate).

---

## Insecure Deserialization (A08)

### Q27. What is insecure deserialization and why is it critical?
Insecure deserialization occurs when an application deserializes untrusted data without validation, allowing an attacker to manipulate serialized objects to execute arbitrary code, inject objects, or replay sessions. In .NET, `BinaryFormatter` is the classic example — it can instantiate any type and call arbitrary methods during deserialization. Microsoft has deprecated `BinaryFormatter` entirely as of .NET 9.

### Q28. How do you prevent insecure deserialization?
Never deserialize untrusted data with type-flexible serializers (`BinaryFormatter`, `JavaScriptSerializer` with type handling). Use `System.Text.Json` or `Newtonsoft.Json` without `TypeNameHandling.Auto/All`. Validate and whitelist expected types. Use signed/encrypted tokens (JWT) instead of serialized objects for session data. Implement integrity checks (HMAC) on serialized data to detect tampering.

---

## Identification and Authentication Failures (A07)

### Q29. What are common authentication vulnerabilities?
Weak password policies (no minimum length, no complexity). Missing brute-force protection (no rate limiting, no account lockout). Session IDs in URLs. Not invalidating sessions on logout or password change. Missing multi-factor authentication for sensitive operations. Credential stuffing using leaked password databases.

### Q30. How do you implement secure authentication?
Strong password policy (minimum 12 chars, check against breached password lists). Rate limiting on login endpoints (e.g., 5 attempts per minute per IP). MFA for sensitive operations. Secure session management — random session IDs, HttpOnly + Secure + SameSite cookies, session timeout, invalidation on logout. Use established libraries (ASP.NET Identity, OAuth 2.0 / OIDC) — never roll your own auth.

### Q31. What is the difference between authentication and authorization?
Authentication verifies identity ("who are you?") — login, password, MFA, tokens. Authorization verifies permissions ("what can you do?") — roles, policies, claims. A system can have perfect authentication but broken authorization (you know exactly who the user is, but you don't check whether they're allowed to do what they're requesting).

---

## Security Logging and Monitoring (A09)

### Q32. What should security logging capture?
Authentication events (login success/failure, MFA challenges), authorization failures (403s, access denied), input validation failures (potential injection attempts), admin actions (user creation, role changes, config changes), data access patterns (bulk exports, unusual query volumes). Log enough to reconstruct an attack timeline but never log sensitive data (passwords, tokens, PII).

### Q33. What makes security monitoring effective?
Real-time alerting on suspicious patterns — burst of failed logins, access from unusual geolocations, privilege escalation attempts. Centralized log aggregation (ELK, Azure Monitor) so logs can't be tampered with on individual servers. Retention policies that meet compliance requirements (typically 90 days to 1 year). Regular review — logs that nobody reads are useless.

### Q34. How do you prevent log injection?
Log injection occurs when an attacker injects control characters (newlines, ANSI codes) into log entries to forge log lines or execute terminal exploits. Prevention: sanitize log input — strip or encode control characters. Use structured logging (Serilog, NLog with structured templates) where user input is a parameter, not part of the message template. Never log raw user input directly into the log message string.

---

## Vulnerable and Outdated Components (A06)

### Q35. How do you manage vulnerable dependencies?
Automated dependency scanning in CI pipeline (OWASP Dependency-Check, Snyk, Dependabot). Critical CVEs fail the build. Medium CVEs generate warnings with a deadline. Maintain a suppression file for reviewed false positives — version-controlled, requires PR approval. Regular dependency update cycles (weekly automated PRs for patch versions, monthly review for minor/major).

### Q36. What is a Software Bill of Materials (SBOM) and why does it matter?
SBOM is a complete inventory of all components, libraries, and dependencies in your application — including transitive dependencies. It matters because when a new vulnerability is disclosed (like Log4Shell), you need to know within minutes whether your application is affected. Generate SBOMs as part of the build process (CycloneDX, SPDX format) and store them alongside releases.

---

## How I Applied This

> [!info] Real experience across KocSistem and Combination.

**At KocSistem — shifting security left:**
- Embedded security scanning into every CI/CD pipeline — dependency scanning, SAST, container image scanning, secret detection
- Pre-push Git hooks blocked commits containing secret patterns (connection strings, API keys, base64 tokens). First week: caught 4 real secrets
- Migrated all secrets from config files and environment variables to Azure Key Vault — service by service, then cleaned Git history with `git filter-branch`
- Tuned SonarQube quality gates for 2 weeks to eliminate false positive fatigue while catching real security hotspots (SQL concatenation, hardcoded credentials, missing input validation)
- **Result: 3 consecutive quarters of zero pen-test findings.** Security team started recommending our pipeline to other teams

**At Combination — security at scale:**
- Breaking change detection in CI (`breaking.yml`) — schema changes checked for backward compatibility before merge, preventing accidental exposure of internal fields
- Container image scanning with Trivy before push to Azure Container Registry — critical vulnerability in base image blocks the build
- GraphQL introspection disabled in production — schema exposed only through the internal schema registry, not the public API
- Query depth limiting and complexity analysis to prevent GraphQL DoS attacks

---

## Sorulursa

> [!faq]- "How do you approach application security in a team that hasn't focused on it before?"
> Start with the highest-impact, lowest-friction wins. Dependency scanning is a 30-minute pipeline addition that immediately catches known CVEs. Pre-push hooks for secret detection take an hour to set up and prevent the most embarrassing breaches. Then add SAST with tuned rules — spending time on tuning is critical because false positive fatigue makes developers ignore all findings. I did this at KocSistem and the key was showing the team real findings from their own code, not theoretical threats.

> [!faq]- "What was the most critical security issue you caught before production?"
> At KocSistem, the pre-push hooks caught 4 real secrets in the first week — connection strings and API keys that would have ended up in Git history. Once a secret is in Git history, it's there forever unless you rewrite history (which requires the entire team to re-clone). Catching it before push is orders of magnitude easier than cleaning it up after.

> [!faq]- "How do you handle security in a microservices architecture differently from a monolith?"
> In a monolith, authorization is checked once at the entry point. In microservices, every service must validate the JWT and check authorization independently — you can't trust that the calling service already checked. Network policies restrict which services can talk to each other (zero trust). Secrets are per-service, not shared. The attack surface is larger (more endpoints, more network hops), but the blast radius of a compromise is smaller if services are properly isolated.

> [!faq]- "How do you stay current with security vulnerabilities and best practices?"
> OWASP updates, CVE feeds for technologies I use (.NET, Docker, Kubernetes), and post-mortems from real breaches (they teach more than any training). Automated dependency scanning catches known vulnerabilities without manual tracking. The most important habit is building security into the pipeline so it's automatic — relying on developers to remember security checks doesn't scale.

---

*[[00-dashboard]]*
