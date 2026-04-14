---
tags:
  - education-kit
---

# Application Security (OWASP) — Education Kit

## OWASP Top 10 — Overview

### Q1. What is the OWASP Top 10 and why does it matter?
The OWASP Top 10 is a regularly updated list of the most critical web application security risks, maintained by the Open Web Application Security Project. It matters because it serves as a baseline standard for security awareness — most pen-test firms and compliance frameworks (PCI-DSS, ISO 27001) reference it directly. If your app is vulnerable to something in the Top 10, you have no excuse.

### Q2. Name the current OWASP Top 10 categories (2021).
A01: Broken Access Control, A02: Cryptographic Failures, A03: Injection, A04: Insecure Design, A05: Security Misconfiguration, A06: Vulnerable and Outdated Components, A07: Identification and Authentication Failures, A08: Software and Data Integrity Failures, A09: Security Logging and Monitoring Failures, A10: Server-Side Request Forgery (SSRF).

---

## Injection Attacks

### Q3. What is SQL injection and how does it work?
SQL injection occurs when user input is concatenated directly into a SQL query string, allowing an attacker to alter the query logic. Example: `SELECT * FROM users WHERE name = '' OR '1'='1'` — the injected `OR '1'='1'` makes the WHERE clause always true, returning all rows. It can lead to data exfiltration, data modification, or even OS command execution.

### Q4. How do you prevent SQL injection?
Use parameterized queries (prepared statements) — always. In .NET: `command.Parameters.AddWithValue("@name", userInput)` or use an ORM like EF Core / Dapper which parameterizes by default. Never concatenate user input into SQL strings. Defense in depth: input validation, least-privilege database accounts, WAF rules.

### Q5. What is the difference between parameterized queries and stored procedures for SQL injection prevention?
Parameterized queries separate data from code at the protocol level. Stored procedures are also safe IF they use parameters internally, but a stored procedure that concatenates input into dynamic SQL is just as vulnerable. Parameterized queries are the fundamental fix.

### Q6. What is ORM injection and can ORMs be vulnerable?
ORMs prevent injection by default because they parameterize queries. However, raw SQL methods (`FromSqlRaw`, `ExecuteSqlRaw`) are vulnerable if you concatenate input. Rule: any time you write raw SQL through an ORM, treat it with the same discipline as raw ADO.NET.

---

## Cross-Site Scripting (XSS)

### Q7. What is XSS and what are the three types?
XSS allows an attacker to inject malicious scripts into web pages viewed by other users. **Stored XSS** — payload saved in database, served to every viewer (most dangerous). **Reflected XSS** — payload in the URL, reflected in the response. **DOM-based XSS** — processed entirely client-side by JavaScript.

### Q8. How do you prevent stored XSS?
Output encoding — encode all user-supplied content when rendering in HTML. Use Content Security Policy (CSP) headers to block inline scripts. Input validation as defense in depth.

### Q9. How do you prevent reflected XSS?
Output encoding, server-side input validation, `X-Content-Type-Options: nosniff`, CSP headers, HTTP-only cookies to prevent session theft.

### Q10. What is DOM-based XSS and why is it harder to detect?
DOM-based XSS happens when JavaScript reads from an attacker-controlled source and writes to a dangerous sink (`innerHTML`, `eval`) without sanitization. It never touches the server, so WAFs don't see it. Prevention: use `textContent` instead of `innerHTML`, avoid `eval()`, sanitize with DOMPurify.

### Q11. What is Content Security Policy (CSP)?
CSP is an HTTP response header that tells the browser which sources of content are allowed. `script-src 'self'` blocks inline scripts and external domains. The strongest defense against XSS. Start with report-only mode.

---

## Cross-Site Request Forgery (CSRF)

### Q12. What is CSRF and how does it work?
CSRF tricks a logged-in user's browser into making an unintended request to a site where they're authenticated. The browser sends cookies automatically. The server can't distinguish it from a legitimate request.

### Q13. How do you prevent CSRF?
Anti-forgery tokens (synchronizer token pattern). For SPAs: `SameSite=Strict` or `SameSite=Lax` cookie attribute. Double-submit cookie pattern for stateless APIs.

### Q14. Does SameSite cookie attribute eliminate the need for CSRF tokens?
`SameSite=Lax` significantly reduces CSRF risk but isn't a complete replacement — older browsers may not support it and subdomain attacks can bypass it. Use both SameSite cookies AND anti-forgery tokens.

---

## Broken Access Control (A01)

### Q15. What is broken access control and why is it #1 on OWASP?
Users can act outside their intended permissions. It's #1 because it's the most commonly found vulnerability. Examples: IDOR, missing function-level access checks, path traversal.

### Q16. What is IDOR and how do you prevent it?
IDOR occurs when an application exposes internal object references and doesn't verify authorization. Always verify authorization server-side. Use GUIDs instead of sequential IDs to reduce enumeration risk (but this is obfuscation, not security).

### Q17. How do you implement proper authorization in a microservices architecture?
JWT claims carry roles and tenant ID. Each service validates the token AND checks authorization against its own data — never trust that another service already checked. Use policy-based authorization with resource-based checks. Every database query must include a tenant filter in multi-tenant systems.

### Q18. What is privilege escalation and how do you prevent it?
Vertical: regular user gains admin access. Horizontal: user accesses another user's data. Prevention: deny by default, enforce authorization at every layer, audit logs for privilege changes, separate admin endpoints with additional authentication.

---

## Cryptographic Failures (A02)

### Q19. What are common cryptographic failures?
Storing passwords in plaintext or with weak hashing (MD5, SHA-1 without salt). Transmitting data without TLS. Using outdated encryption algorithms. Hardcoding encryption keys. Not rotating keys. Exposing sensitive data in logs.

### Q20. How should passwords be stored?
Use a slow, salted hashing algorithm: bcrypt, scrypt, or Argon2. Never MD5 or SHA-256 for passwords — they're fast, which means brute-force is fast. Each password gets a unique random salt.

### Q21. What is the difference between encryption and hashing?
Encryption is reversible (with the right key). Hashing is one-way. Use encryption for data you need to read back. Use hashing for data you only need to verify. Using encryption for passwords is wrong — if the key leaks, all passwords are exposed.

---

## Security Misconfiguration (A05)

### Q22. What are common security misconfigurations?
Default credentials, unnecessary services/ports open, verbose error messages, CORS set to `*`, debug endpoints enabled, missing security headers, unnecessary HTTP methods enabled.

### Q23. How do you prevent security misconfiguration?
Hardened base configurations (infrastructure as code), automated scanning, remove unused features, different credentials per environment, security headers checklist enforced via middleware.

### Q24. What security headers should every application set?
`Strict-Transport-Security` (HSTS), `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy`.

---

## Server-Side Request Forgery — SSRF (A10)

### Q25. What is SSRF and why is it dangerous?
SSRF makes the server send HTTP requests to arbitrary destinations — including internal services and metadata endpoints. Especially dangerous in cloud environments where the metadata endpoint reveals IAM credentials.

### Q26. How do you prevent SSRF?
Whitelist allowed domains/IPs, block private IP ranges, disable unnecessary URL schemes, use a dedicated egress proxy, use IMDSv2 in cloud environments.

---

## Insecure Deserialization (A08)

### Q27. What is insecure deserialization?
Deserializing untrusted data without validation, allowing arbitrary code execution or object injection. In .NET, `BinaryFormatter` is the classic example — deprecated entirely as of .NET 9.

### Q28. How do you prevent insecure deserialization?
Never deserialize untrusted data with type-flexible serializers. Use `System.Text.Json` without `TypeNameHandling`. Validate and whitelist expected types. Use signed tokens (JWT) instead of serialized objects for sessions.

---

## Identification and Authentication Failures (A07)

### Q29. What are common authentication vulnerabilities?
Weak password policies, missing brute-force protection, session IDs in URLs, not invalidating sessions on logout, missing MFA, credential stuffing.

### Q30. How do you implement secure authentication?
Strong password policy (minimum 12 chars, check against breached lists). Rate limiting on login. MFA for sensitive operations. Secure session management — random session IDs, HttpOnly + Secure + SameSite cookies, session timeout, invalidation on logout. Use established libraries — never roll your own auth.

### Q31. What is the difference between authentication and authorization?
Authentication verifies identity ("who are you?"). Authorization verifies permissions ("what can you do?"). A system can have perfect authentication but broken authorization.

---

## Security Logging and Monitoring (A09)

### Q32. What should security logging capture?
Authentication events, authorization failures, input validation failures, admin actions, data access patterns. Never log sensitive data (passwords, tokens, PII).

### Q33. What makes security monitoring effective?
Real-time alerting on suspicious patterns, centralized log aggregation (tamper-proof), retention policies for compliance, regular review.

### Q34. How do you prevent log injection?
Sanitize log input — strip or encode control characters. Use structured logging where user input is a parameter, not part of the message template.

---

## Vulnerable and Outdated Components (A06)

### Q35. How do you manage vulnerable dependencies?
Automated dependency scanning in CI pipeline. Critical CVEs fail the build. Maintain a reviewed suppression file. Regular dependency update cycles.

### Q36. What is a Software Bill of Materials (SBOM)?
A complete inventory of all components and dependencies. Essential for determining exposure when new vulnerabilities are disclosed (e.g., Log4Shell). Generate as part of build process.

---

## Common Questions

**"How do you approach application security in a team that hasn't focused on it before?"**
Start with the highest-impact, lowest-friction wins. Dependency scanning is a 30-minute pipeline addition. Pre-push hooks for secret detection take an hour. Then add SAST with tuned rules — tuning is critical because false positive fatigue makes developers ignore all findings. Show the team real findings from their own code, not theoretical threats.

**"How do you handle security in a microservices architecture differently from a monolith?"**
In a monolith, authorization is checked once at the entry point. In microservices, every service must validate the JWT and check authorization independently. Network policies restrict which services can talk to each other (zero trust). The attack surface is larger, but the blast radius of a compromise is smaller if services are properly isolated.

**"How do you stay current with security vulnerabilities?"**
OWASP updates, CVE feeds for technologies you use, post-mortems from real breaches. Automated dependency scanning catches known vulnerabilities without manual tracking. Build security into the pipeline so it's automatic.
