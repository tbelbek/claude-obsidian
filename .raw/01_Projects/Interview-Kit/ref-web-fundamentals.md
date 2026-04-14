---
tags:
  - interview-kit
  - interview-kit/reference
up: "[[00-dashboard]]"
---

*[[00-dashboard]]*

# Web Fundamentals — Senior Interview Questions

> [!tip] Backend web fundamentals. Not framework-specific — these apply whether you use .NET, Node, Python, or Go.

## Quick Scan — Ctrl+F This


| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Q1: What happens when you type a URL in the browser and press Enter?\|HTTP lifecycle]] | DNS→TCP→TLS→HTTP→response | [[#Q2: Explain HTTP methods and their idempotency guarantees.\|HTTP methods]] | GET=safe, POST=create, PUT=replace |
| [[#Q3: When do you use each HTTP status code? Walk through the important ones.\|status codes]] | 200/201/400/401/403/404/500/502/503 | [[#Q4: Explain the key HTTP headers a backend developer should know.\|key headers]] | Content-Type, Auth, Cache-Control, ETag |
| [[#Q5: What is the difference between HTTP/1.1, HTTP/2, and HTTP/3?\|HTTP/2 vs HTTP/3]] | H2=multiplexed/TCP, H3=QUIC/UDP | [[#Q6: Compare WebSockets, Server-Sent Events (SSE), and long polling.\|WebSocket vs SSE]] | WS=bidirectional, SSE=server→client |
| [[#Q9b: What is a reverse proxy and how does it differ from a load balancer?\|reverse proxy vs LB]] | proxy=SSL/cache, LB=distribute | [[#Q9c: Explain connection pooling — why does it matter?\|connection pooling]] | reuse TCP, avoid handshake overhead |
| [[#Q10: Explain the TLS handshake process.\|TLS handshake]] | cert exchange→key agree→symmetric | [[#Q16b: What happens when an SSL certificate expires? How do you fix it?\|cert expired]] | renew+install, cert-manager automates |
| [[#Q12: What is mutual TLS (mTLS) and when would you use it?\|mTLS]] | both sides authenticate with certs | [[#Q14: Walk through the OWASP Top 10 vulnerabilities relevant to backend APIs.\|OWASP Top 10]] | injection, XSS, CSRF, broken auth |
| [[#Q17: What are the principles of good REST API resource naming?\|REST naming]] | nouns not verbs, plural, hierarchical | [[#Q18: Compare offset-based vs cursor-based pagination.\|pagination]] | offset=simple, cursor=stable+fast |
| [[#Q23c: How do you handle API versioning in practice?\|API versioning]] | URL /v1 simplest, GraphQL=no versions | [[#Q29b: How does JWT validation work step by step?\|JWT validation]] | split→verify sig→check exp/iss/aud |
| [[#Q29c: How do you handle inter-service authentication in microservices?\|inter-service auth]] | mTLS, service tokens, workload identity | [[#Q30: Explain HTTP caching mechanisms (Cache-Control, ETag, Last-Modified).\|HTTP caching]] | Cache-Control, ETag, 304 Not Modified |
| [[#Q34b: What is cache stampede and how do you prevent it?\|cache stampede]] | lock, background refresh, stale-while | [[#Q35: When do you choose SQL vs NoSQL?\|SQL vs NoSQL]] | SQL=fixed+ACID, NoSQL=flexible+scale |
| [[#Q36: What is the N+1 query problem and how do you solve it?\|N+1 problem]] | loop of queries→one JOIN or batch | [[#Q38: What is the difference between ACID and BASE?\|ACID vs BASE]] | ACID=strong, BASE=eventually consistent |
| [[#Q45c: What is the difference between horizontal and vertical scaling?\|horizontal vs vertical]] | vertical=bigger, horizontal=more machines | [[#Q45b: What is backpressure and how do you implement it?\|backpressure]] | bounded queues, rate limiting |
| [[#Q46: Compare blue-green, canary, and rolling deployments.\|blue-green vs canary]] | BG=switch, canary=gradual % | [[#Q50: Explain the circuit breaker pattern.\|circuit breaker]] | open/half-open/closed, fail fast |

---

## HTTP & Networking

### Q1: What happens when you type a URL in the browser and press Enter?
DNS resolution (recursive lookup: browser cache, OS cache, resolver, root/TLD/authoritative nameservers) resolves domain to IP. TCP three-way handshake (SYN/SYN-ACK/ACK) establishes connection. If HTTPS, TLS handshake follows (certificate exchange, key agreement, symmetric key derived). HTTP request is sent, server processes it, HTTP response returns with status code, headers, and body. Each step can fail independently — DNS timeout, TCP refused, TLS cert invalid, HTTP 5xx.

### Q2: Explain HTTP methods and their idempotency guarantees.
GET retrieves a resource (safe, idempotent). POST creates a resource or triggers a process (neither safe nor idempotent). PUT replaces a resource entirely (idempotent — calling it twice yields the same state). PATCH partially updates a resource (not guaranteed idempotent by spec, but often implemented as such). DELETE removes a resource (idempotent — deleting twice results in the same state, though the second call may return 404). In microservices, idempotency matters hugely because network retries are inevitable — if your POST isn't idempotent, you need idempotency keys.

### Q3: When do you use each HTTP status code? Walk through the important ones.
2xx success: 200 OK (general success), 201 Created (resource created, include Location header), 204 No Content (success but no body, common for DELETE). 3xx redirect: 301 Moved Permanently (SEO redirect, browser caches it), 302 Found (temporary redirect). 4xx client errors: 400 Bad Request (malformed syntax), 401 Unauthorized (actually means unauthenticated — no valid credentials), 403 Forbidden (authenticated but not authorized), 404 Not Found, 409 Conflict (e.g., duplicate resource or version conflict), 422 Unprocessable Entity (valid syntax but semantic errors — validation failures), 429 Too Many Requests (rate limited, include Retry-After header). 5xx server errors: 500 Internal Server Error (unhandled exception), 502 Bad Gateway (upstream service returned invalid response), 503 Service Unavailable (overloaded or in maintenance, include Retry-After).

### Q4: Explain the key HTTP headers a backend developer should know.
`Content-Type` tells the receiver the media type (application/json, multipart/form-data). `Accept` tells the server what the client wants back (content negotiation). `Authorization` carries credentials (Bearer token, Basic base64). `Cache-Control` directs caching behavior (max-age, no-cache, no-store, private, public). `ETag` is a version identifier for a resource — the server sends it, the client sends it back in `If-None-Match` for conditional requests (304 Not Modified saves bandwidth). CORS headers (`Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`) control cross-origin access — in microservices behind an API gateway, CORS is typically handled at the gateway level, not in each service.

### Q5: What is the difference between HTTP/1.1, HTTP/2, and HTTP/3?
HTTP/1.1 uses text-based protocol with one request per TCP connection (or pipelining, which was poorly supported). HTTP/2 introduced binary framing, multiplexing (multiple requests over a single TCP connection), header compression (HPACK), and server push. HTTP/3 replaces TCP with QUIC (UDP-based), eliminating head-of-line blocking at the transport layer and reducing connection setup time (0-RTT). For backend APIs behind a load balancer, HTTP/2 between client and LB is common; between LB and services, HTTP/2 or gRPC is increasingly used.

### Q6: Compare WebSockets, Server-Sent Events (SSE), and long polling.
Long polling: client sends request, server holds it open until data is available, responds, client immediately reconnects. Simple but wasteful (connection overhead per message). SSE: server pushes events over a single HTTP connection (text/event-stream). Unidirectional (server to client), auto-reconnects, works with HTTP/2. Great for notifications, live feeds. WebSockets: full-duplex, bidirectional communication over a single TCP connection after an HTTP upgrade handshake. Use for chat, real-time collaboration, gaming. In a microservices architecture, WebSockets require sticky sessions or a pub/sub backbone (Redis, Kafka) to fan out messages across instances.

### Q7: Explain cookies vs tokens for session management.
Cookies are automatically sent by the browser with every request to the domain (HttpOnly, Secure, SameSite flags for security). They are stateful if they contain a session ID pointing to server-side state, or stateless if they contain a signed JWT. Tokens (typically JWTs in Authorization header) are explicitly attached by client code — they work well for APIs consumed by mobile apps and SPAs and are inherently cross-domain. Cookies are vulnerable to CSRF (mitigated by SameSite, CSRF tokens); tokens in localStorage are vulnerable to XSS. In microservices, token-based auth is dominant because services are stateless and need to validate tokens independently.

### Q8: What is DNS and how does resolution work in a cloud-native context?
DNS maps domain names to IP addresses. In Kubernetes, CoreDNS handles internal service discovery — services get DNS names like `my-service.my-namespace.svc.cluster.local`. Externally, DNS can be used for load balancing (round-robin A records, weighted routing in Route53/Cloud DNS), blue-green deployments (swapping DNS records), and failover. DNS TTL matters — too long and failover is slow, too short and DNS load increases. In a 60+ service architecture, internal service discovery via DNS (or service mesh) is critical for decoupling services from specific IPs.

### Q9: How does connection pooling work at the HTTP level?
HTTP/1.1 introduced `Connection: keep-alive` to reuse TCP connections across multiple requests, avoiding the overhead of TCP+TLS handshake per request. HTTP clients and servers maintain a pool of open connections. In microservices, each service maintains connection pools to its dependencies — misconfigured pool sizes cause connection exhaustion under load or wasted resources when oversized. HttpClient in .NET, for example, should be reused (singleton or via IHttpClientFactory) because creating new instances per request exhausts sockets (socket exhaustion / SNAT port exhaustion).

### Q9b: What is a reverse proxy and how does it differ from a load balancer?
Reverse proxy sits in front of servers, handles client requests on their behalf — SSL termination, caching, compression, request routing. A load balancer distributes traffic across multiple server instances. In practice they overlap — nginx, Traefik, and cloud load balancers do both. In our K8s setup, the Ingress controller (Contour) acts as both reverse proxy and load balancer.

### Q9c: Explain connection pooling — why does it matter?
Opening a TCP connection is expensive (handshake, TLS negotiation). Connection pooling reuses open connections across requests. HTTP: `Keep-Alive` header reuses TCP connections. Database: connection pool (e.g., SqlConnection pool in .NET defaults to 100). At KocSistem, 500+ trucks overwhelmed the default pool size — we had to increase it and monitor active connections.

### Q9d: What is the difference between synchronous and asynchronous HTTP communication?
Synchronous: client sends request, waits for response, blocks until complete. Simple but thread-blocking. Asynchronous: client sends request, continues other work, handles response when it arrives. In microservices, sync (REST/gRPC) for request-response patterns, async (Kafka/RabbitMQ) for fire-and-forget or event-driven patterns. At Combination: gRPC for sync service-to-service, Kafka for async domain events.

---

## SSL/TLS & Security

### Q10: Explain the TLS handshake process.
In TLS 1.2: ClientHello (supported cipher suites, random) → ServerHello (chosen cipher, random, server certificate) → client verifies certificate chain against trusted CAs → client generates pre-master secret, encrypts with server's public key → both derive session keys → Finished messages confirm. TLS 1.3 simplifies this to a single round-trip (1-RTT) or even zero round-trips (0-RTT for resumed sessions) by combining key exchange into the first messages. The result is a shared symmetric key used for the actual data encryption (AES-GCM typically).

### Q11: What is a certificate chain and what happens when a certificate expires?
A certificate chain goes: leaf (server) cert → intermediate CA → root CA. The browser trusts root CAs in its trust store and validates the chain. When a cert expires, clients reject the TLS handshake — your API returns nothing, just connection failures. In production, this means total outage for HTTPS traffic. Fix: replace the cert. Prevent: use cert-manager in Kubernetes with Let's Encrypt for automatic renewal (90-day certs, auto-renewed at 60 days). Monitor cert expiry with alerts (e.g., Prometheus blackbox exporter checks TLS expiry).

### Q12: What is mutual TLS (mTLS) and when would you use it?
In standard TLS, only the server presents a certificate. In mTLS, both client and server present certificates and verify each other. This provides strong service-to-service authentication in microservices — you know exactly which service is calling you, not just that the connection is encrypted. Service meshes like Istio and Linkerd automate mTLS between pods, handling certificate rotation transparently. Use mTLS for zero-trust networking where you cannot rely on network perimeter security alone.

### Q13: Explain HTTPS redirect and HSTS.
HTTPS redirect: server returns 301/302 from HTTP to HTTPS URL. But the first request is still plaintext (vulnerable to MITM). HSTS (HTTP Strict Transport Security) fixes this — the `Strict-Transport-Security` header tells the browser to only use HTTPS for this domain for a specified time (max-age). After the first visit, the browser never makes an HTTP request to that domain. HSTS preload lists go further — browsers ship with a list of domains that should always use HTTPS, eliminating even the first insecure request.

### Q14: Walk through the OWASP Top 10 vulnerabilities relevant to backend APIs.
Injection (SQL, NoSQL, command) — use parameterized queries, never concatenate user input. Broken Authentication — weak passwords, missing rate limiting on login, exposing session IDs. Sensitive Data Exposure — not encrypting data at rest/in transit, logging PII. Broken Access Control — IDOR (accessing /api/users/123 when you are user 456), missing authorization checks. Security Misconfiguration — default credentials, open cloud storage buckets, verbose error messages in production. SSRF (Server-Side Request Forgery) — user-controlled URLs that the server fetches, potentially hitting internal services. In microservices, each service is an attack surface — defense in depth matters.

### Q15: How do you prevent CSRF attacks in a backend API?
CSRF exploits the browser automatically sending cookies with requests. For traditional server-rendered apps: use anti-CSRF tokens (server generates a token, embeds it in forms, validates it on submission). For SPAs calling APIs: use SameSite cookie attribute (Strict or Lax), which prevents cookies from being sent on cross-site requests. If your API uses token-based auth (Bearer tokens in headers), CSRF is not a concern because the browser does not automatically attach Authorization headers. In microservices behind an API gateway, CSRF protection typically lives at the gateway or BFF (Backend-for-Frontend) layer.

### Q16: What is CORS and how do you configure it for a backend API?
CORS (Cross-Origin Resource Sharing) controls which origins can call your API from a browser. The browser sends a preflight OPTIONS request for non-simple requests. The server responds with `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers`. Common mistake: setting `Access-Control-Allow-Origin: *` with credentials — this is not allowed by browsers. In microservices, configure CORS at the API gateway level (e.g., Kong, NGINX, Azure API Management) rather than in every service. Be specific with allowed origins in production.

### Q16b: What happens when an SSL certificate expires? How do you fix it?
Browsers show a security warning and refuse to connect. APIs return SSL errors. Fix: (1) Renew the certificate — Let's Encrypt auto-renews, enterprise CAs require manual request. (2) Install the new cert on the server/load balancer. (3) Verify with `openssl s_client`. Prevention: cert-manager in K8s auto-renews and deploys certs. Monitor cert expiry with alerts (< 30 days = warning, < 7 days = critical). At Combination, cert-manager handles this automatically in K8s.

### Q16c: What is certificate pinning and when should you use it?
Certificate pinning hardcodes the expected certificate (or public key) in the client. If the server presents a different cert (even a valid one), the connection is rejected. Prevents MITM attacks even if a CA is compromised. Used in mobile apps and high-security APIs. Downside: cert rotation requires client update. In most web APIs, standard TLS validation is sufficient.

---

## REST API Design

### Q17: What are the principles of good REST API resource naming?
Use nouns, not verbs: `/orders` not `/getOrders`. Use plurals: `/users/123` not `/user/123`. Nest for relationships: `/users/123/orders`. Use hyphens for readability: `/order-items` not `/orderItems`. Avoid deep nesting (max 2-3 levels) — beyond that, use filtering: `/orders?userId=123` instead of `/users/123/departments/456/orders`. Keep URLs lowercase. Actions that do not map to CRUD can use sub-resources: `POST /orders/123/cancel` rather than inventing a verb-based URL.

### Q18: Compare offset-based vs cursor-based pagination.
Offset-based (`?page=3&pageSize=20` or `?offset=40&limit=20`): simple, allows jumping to any page, but breaks when data is inserted or deleted between requests (items shift, causing duplicates or missed items). Performance degrades on large offsets (database still scans skipped rows). Cursor-based (`?cursor=eyJpZCI6MTIzfQ&limit=20`): uses an opaque token (typically encoded last-seen ID + sort field) — stable under concurrent writes, consistently fast regardless of position. In high-throughput microservices with real-time data, cursor-based pagination is strongly preferred. Return `nextCursor` in response metadata.

### Q19: How do you design API error responses?
Use a consistent structure across all services: `{ "error": { "code": "VALIDATION_ERROR", "message": "Human-readable message", "details": [{ "field": "email", "reason": "Invalid format" }], "traceId": "abc-123" } }`. Always include a machine-readable error code (not just HTTP status). Include a correlation/trace ID for debugging across services. Never expose stack traces or internal details in production. Use RFC 7807 (Problem Details for HTTP APIs) as a standard: `application/problem+json` with `type`, `title`, `status`, `detail`, `instance` fields.

### Q20: What are the common API versioning strategies?
URL path versioning (`/api/v1/users`): most common, easy to route, but clutters URLs. Header versioning (`Accept: application/vnd.myapi.v2+json`): cleaner URLs but harder to test (cannot just paste a URL). Query parameter (`?api-version=2024-01-15`): Azure's approach, date-based versions. In practice, URL versioning wins for simplicity. Version when you make breaking changes (removing fields, changing types, renaming). Non-breaking changes (adding fields) do not need a new version. Run multiple versions simultaneously, deprecate old versions with sunset headers and migration guides.

### Q21: How do you implement rate limiting in an API?
Common algorithms: Token Bucket (tokens replenish at a fixed rate, each request consumes a token — allows bursts), Sliding Window (count requests in a rolling time window — smoother). Return 429 Too Many Requests with `Retry-After` header and `X-RateLimit-Remaining`, `X-RateLimit-Limit`, `X-RateLimit-Reset` headers. In microservices, rate limiting is typically at the API gateway level (per client/API key). For distributed rate limiting across multiple gateway instances, use Redis (atomic INCR with TTL). Different limits for different endpoints — writes are more expensive than reads.

### Q22: What are idempotency keys and why do they matter?
An idempotency key is a unique identifier (usually UUID) sent by the client in a header (`Idempotency-Key: uuid`). The server stores the key with the result of the first request. If the same key is sent again (e.g., network retry), the server returns the stored result instead of processing again. Critical for payment APIs, order creation, any non-idempotent operation where retries could cause duplicates. Store keys in Redis with a TTL (e.g., 24 hours). Stripe, PayPal, and most payment APIs use this pattern extensively.

### Q23: What is HATEOAS and is it practical?
HATEOAS (Hypermedia As The Engine Of Application State) means API responses include links to related actions and resources: `{ "order": { "id": 123, "status": "pending", "_links": { "cancel": "/orders/123/cancel", "pay": "/orders/123/pay" } } }`. In theory, clients discover the API dynamically. In practice, very few APIs implement full HATEOAS — most clients are tightly coupled to the API anyway. However, including pagination links (`next`, `prev`) and self links is widely adopted and genuinely useful.

### Q23b: How do you design error responses in a REST API?
Consistent format across all endpoints. Include: error code (machine-readable), message (human-readable), details (field-level validation errors), request ID (for debugging). Example: `{"error": "VALIDATION_FAILED", "message": "Invalid input", "details": [{"field": "email", "issue": "not a valid email"}], "requestId": "abc-123"}`. Never expose stack traces or internal details in production.

### Q23c: How do you handle API versioning in practice?
Three approaches: URL path (`/v1/users`), header (`Accept: application/vnd.api.v2+json`), query parameter (`?version=2`). URL path is simplest and most common. In GraphQL, no versioning — deprecate fields with `@deprecated`. In gRPC, versioned proto directories (v1/, v2/). At Combination: REST uses URL versioning for external partners, GraphQL avoids it entirely.

---

## Authentication & Authorization

### Q24: Explain JWT structure and how validation works.
A JWT has three base64url-encoded parts separated by dots: Header (algorithm, type) . Payload (claims — sub, exp, iat, iss, custom claims like roles) . Signature (HMAC or RSA/ECDSA sign of header+payload). Validation: decode header to get algorithm, verify signature using the secret (HMAC) or public key (RSA/ECDSA), check `exp` (expiration), `iss` (issuer), `aud` (audience). In microservices, the API gateway or each service validates the JWT independently using the identity provider's public key (fetched from JWKS endpoint). Never store sensitive data in JWT payload — it is base64, not encrypted.

### Q25: Describe OAuth2 flows and when to use each.
Authorization Code flow (with PKCE): for web/mobile apps — user redirects to auth server, gets authorization code, exchanges it for tokens. Most secure for user-facing apps. Client Credentials flow: for service-to-service communication — no user involved, the service authenticates with client ID/secret and gets an access token. Implicit flow: deprecated — tokens in URL fragment, vulnerable to interception. Resource Owner Password: user gives credentials directly to the app — only for trusted first-party apps. In microservices, Client Credentials is used for inter-service calls, Authorization Code + PKCE for user-facing APIs.

### Q26: Compare API keys vs OAuth tokens.
API keys are simple strings, typically long-lived, identifying a client application (not a user). Easy to implement but risky — if leaked, they give full access until rotated. No standard for scoping or expiry. OAuth tokens (access tokens) are short-lived, scoped (read:users, write:orders), revocable, tied to a specific user+application combination. Use API keys for server-to-server integrations with trusted partners (always over HTTPS, never in URLs). Use OAuth tokens for user-delegated access and when you need fine-grained permissions.

### Q27: Explain session-based vs token-based authentication.
Session-based: server creates a session on login, stores it (in memory, Redis, or database), sends a session ID cookie to the client. Every request sends the cookie, server looks up the session. Requires shared session store for horizontal scaling. Token-based: server issues a signed token (JWT) on login, client stores it and sends it in the Authorization header. Server validates the token without any lookup (stateless). Scales horizontally without shared state. Downside: cannot revoke a JWT before expiry without a blacklist (which reintroduces state). In practice, use short-lived access tokens (15 min) + refresh tokens (stored securely, revocable).

### Q28: What is the difference between RBAC and ABAC?
RBAC (Role-Based Access Control): users have roles (admin, editor, viewer), permissions are assigned to roles. Simple, widely used, but can lead to role explosion when you need fine-grained rules. ABAC (Attribute-Based Access Control): policies evaluate attributes of the user, resource, action, and environment (e.g., "users in department=engineering can edit documents where classification=internal during business hours"). More flexible, handles complex scenarios. In microservices, RBAC is common for coarse-grained checks (is this user an admin?), while ABAC via a policy engine (OPA/Rego, Cedar) handles fine-grained authorization.

### Q29: How do you secure inter-service communication in a microservices architecture?
Layer 1: Network isolation (VPC, network policies in K8s — only allow traffic between known services). Layer 2: mTLS for transport security (service mesh handles this). Layer 3: Service-to-service auth tokens (OAuth2 Client Credentials, or JWT propagation with audience validation). Layer 4: Authorization — each service validates that the calling service has permission for the specific operation. Do not rely on any single layer. In practice, a service mesh (Istio/Linkerd) handles mTLS and network policy, while application-level JWT validation handles authorization.

### Q29b: How does JWT validation work step by step?
(1) Extract token from `Authorization: Bearer <token>` header. (2) Split into header.payload.signature (base64-encoded, dot-separated). (3) Verify signature using the signing key (symmetric HMAC or asymmetric RSA/ECDSA). (4) Check claims: `exp` (not expired), `iss` (trusted issuer), `aud` (correct audience), `nbf` (not before). (5) If all pass, trust the claims in the payload. Common mistake: not checking `exp` — expired tokens should be rejected.

### Q29c: How do you handle inter-service authentication in microservices?
Options: (1) Mutual TLS (mTLS) — each service has a certificate, services authenticate each other at the transport level. (2) Service account tokens — each service gets a JWT signed by a trusted authority, passed in headers. (3) K8s service accounts with OIDC federation — pods authenticate to external services via workload identity. At Combination, we use Azure Workload Identity — pods get tokens without stored credentials.

---

## Caching

### Q30: Explain HTTP caching mechanisms (Cache-Control, ETag, Last-Modified).
`Cache-Control: max-age=3600` tells the client/proxy to cache the response for 3600 seconds without revalidation. `no-cache` means always revalidate (still caches, but checks before using). `no-store` means never cache at all. `ETag` is a fingerprint — client sends `If-None-Match: "etag"` on next request, server returns 304 Not Modified if unchanged (saves bandwidth, not round-trip). `Last-Modified` / `If-Modified-Since` is the date-based equivalent. `private` means only browser can cache (not CDN/proxy), `public` allows shared caches. In APIs, use ETags for resources that change unpredictably and max-age for static or slowly-changing data.

### Q31: When and how do you use Redis for caching in microservices?
Use Redis for: frequently read, rarely changing data (user profiles, configuration, feature flags), computed results (aggregations, leaderboards), session storage, rate limiting counters. Pattern: check Redis first, on miss query database, write to Redis with TTL. Use appropriate data structures — Strings for simple K/V, Hashes for objects, Sorted Sets for leaderboards/ranked data. Set TTLs always (avoid unbounded memory growth). In a multi-service architecture, Redis acts as a shared cache layer, but be careful about cache coherence — each service should own its cache namespace.

### Q32: What is cache invalidation and why is it hard?
"There are only two hard things in CS: cache invalidation and naming things." The problem: when the source data changes, cached copies become stale. Strategies: TTL-based (let it expire — simple, eventual consistency), event-driven (publish a change event, subscribers invalidate their cache — more complex but faster consistency), write-through (update cache and DB simultaneously), write-behind (update cache, async write to DB — risk of data loss). In microservices, event-driven invalidation via Kafka/RabbitMQ is common — when the orders service updates an order, it publishes an event, and any service caching order data invalidates it.

### Q33: What is a cache stampede and how do you prevent it?
Cache stampede (thundering herd): a popular cache key expires, and hundreds of concurrent requests all miss the cache simultaneously, all hit the database, potentially overloading it. Prevention: lock-based recomputation (first request acquires a distributed lock, others wait or get stale data), probabilistic early recomputation (randomly refresh before expiry), stale-while-revalidate (serve stale data while refreshing in background), never-expire with async refresh. In high-traffic services, cache stampede on a hot key can take down your database — always plan for it.

### Q34: How does CDN caching work and when do you use it for APIs?
A CDN (CloudFront, Cloudflare, Akamai) caches responses at edge locations close to users, reducing latency. For APIs: cache GET responses for public, stable data (product catalogs, configuration). Use `Cache-Control` and `Vary` headers to control what gets cached. `Vary: Authorization` means different cache entries per auth token (usually means "do not cache"). CDN caching is excellent for read-heavy, public APIs. For authenticated/personalized APIs, CDN is used primarily for TLS termination and DDoS protection, not caching.

### Q34b: What is cache stampede and how do you prevent it?
When a cache entry expires, many requests hit the database simultaneously to rebuild it. Fixes: (1) Lock — first request acquires a lock, rebuilds cache, others wait. (2) Background refresh — refresh cache before it expires so it's never empty. (3) Stale-while-revalidate — serve stale data while refreshing in the background. At KocSistem, we used background refresh for the truck dashboard — a scheduled task updated each truck's position in cache every few seconds.

---

## Database & Data

### Q35: When do you choose SQL vs NoSQL?
SQL (PostgreSQL, SQL Server): strong consistency, complex queries with joins, transactions (ACID), well-understood schema, relationships between entities. Use for: financial data, orders, user accounts — anything where correctness matters. NoSQL (MongoDB, DynamoDB, Cosmos DB): flexible schema, horizontal scaling, high write throughput, denormalized data. Use for: event logs, product catalogs, content management, IoT telemetry. In microservices, each service picks the right database for its domain — the orders service might use PostgreSQL while the analytics service uses ClickHouse and the session store uses Redis.

### Q36: What is the N+1 query problem and how do you solve it?
N+1 occurs when you query a list of N items, then make N additional queries to fetch related data for each item. Example: fetch 100 orders (1 query), then fetch customer for each order (100 queries). Solution: eager loading/joins (`SELECT * FROM orders JOIN customers`), batch loading (`WHERE customer_id IN (1,2,3,...)`), or DataLoader pattern (batches individual lookups within a request). ORMs like Entity Framework, Hibernate, and SQLAlchemy all support eager loading. Always check your ORM's generated SQL — the N+1 problem is the most common performance issue in data access layers.

### Q37: Explain database indexing — when and how to use indexes.
An index is a data structure (typically B-tree) that speeds up lookups at the cost of slower writes and extra storage. Index columns used in WHERE, JOIN, and ORDER BY clauses. Composite indexes follow the leftmost prefix rule — an index on (A, B, C) helps queries filtering on A, A+B, or A+B+C, but not B alone. Covering indexes include all columns needed by the query, avoiding table lookups. Too many indexes slow down writes (every INSERT/UPDATE must update all indexes). Use EXPLAIN/EXPLAIN ANALYZE to verify index usage. In high-throughput microservices, missing indexes are the number one cause of slow API responses.

### Q38: What is the difference between ACID and BASE?
ACID (Atomicity, Consistency, Isolation, Durability): traditional relational databases guarantee all-or-nothing transactions, consistent state, isolated concurrent operations, and durable writes. BASE (Basically Available, Soft state, Eventually consistent): distributed NoSQL databases trade strong consistency for availability and partition tolerance (CAP theorem). In practice, microservices often use ACID within a single service's database but BASE across services — the Saga pattern coordinates multi-service transactions with eventual consistency and compensating actions rather than distributed two-phase commit.

### Q39: What is connection pooling and why does it matter?
Creating a database connection is expensive (TCP handshake, TLS, authentication, protocol negotiation — 50-200ms). Connection pooling maintains a pool of pre-established connections that are reused across requests. Most frameworks have built-in pooling (HikariCP for Java, Npgsql for .NET, pgBouncer for PostgreSQL). Configure min/max pool size based on load — too few connections cause request queuing, too many exhaust database limits. In Kubernetes with many pod replicas, each pod has its own pool — 50 pods x 20 connections = 1000 database connections. Use PgBouncer or similar proxy to multiplex.

### Q40: Explain eventual consistency and its implications for microservices.
In a distributed system, eventual consistency means that after a write, all replicas will converge to the same state given enough time, but reads may temporarily return stale data. Implications: you might create an order and not immediately see it in the order list (read from a different replica). Design for it: use read-your-own-writes consistency (route the user's reads to the same replica that handled their write), show optimistic UI updates, design idempotent consumers. In event-driven microservices, eventual consistency is the norm — the order service publishes an event, the inventory service processes it asynchronously.

---

## Scalability

### Q41: Compare horizontal vs vertical scaling.
Vertical scaling (scale up): add more CPU/RAM to a single machine. Simple, no code changes, but has a ceiling (hardware limits) and single point of failure. Horizontal scaling (scale out): add more instances behind a load balancer. Requires stateless services (no local state — use external stores for sessions, files, cache). In Kubernetes, horizontal scaling is native (HPA — Horizontal Pod Autoscaler scales based on CPU, memory, or custom metrics). Microservices are designed for horizontal scaling — each service scales independently based on its own demand.

### Q42: What load balancing strategies exist and when do you use each?
Round Robin: distribute requests evenly — simple, works when instances are equal. Weighted Round Robin: assign more traffic to stronger instances. Least Connections: route to the instance with fewest active connections — good for long-lived requests. IP Hash / Consistent Hashing: route the same client to the same instance — use for sticky sessions (but prefer stateless services). In Kubernetes, kube-proxy does L4 (TCP) load balancing by default. For L7 (HTTP) routing (path-based, header-based), use an Ingress controller (NGINX, Traefik) or service mesh. gRPC requires L7 load balancing because HTTP/2 multiplexes over one connection.

### Q43: Why must services be stateless for scalability?
Stateless means no request-scoped data stored in the service instance's memory between requests. If a service stores session data locally, requests must be routed to the same instance (sticky sessions) — this prevents effective load balancing, complicates scaling, and causes data loss when instances restart. Move state externally: sessions to Redis, files to object storage (S3/Azure Blob), cache to Redis/Memcached. Stateless services can be freely killed, restarted, and scaled — Kubernetes assumes pods are disposable.

### Q44: Explain service discovery in a microservices architecture.
Services need to find each other without hardcoded IPs. Client-side discovery: the client queries a service registry (Consul, Eureka) and picks an instance. Server-side discovery: the client calls a load balancer/DNS name that routes to an available instance. In Kubernetes, server-side discovery is built in — Services get stable DNS names and kube-proxy handles routing to pods. For external service discovery (across clusters or clouds), use Consul, AWS Cloud Map, or DNS-based approaches. Service meshes add another layer — Envoy sidecars handle discovery and routing transparently.

### Q45: What are common rate limiting patterns at scale?
Local rate limiting: per-instance counters — simple but inconsistent across instances (10 instances x 100 req/s limit = 1000 req/s effective). Global rate limiting: centralized counter in Redis — consistent but adds latency per request. Distributed rate limiting: each instance tracks locally and syncs periodically with a central store — compromise between consistency and performance. Algorithms: Token Bucket (bursty traffic allowed), Leaky Bucket (smooths traffic to constant rate), Fixed Window (simple but allows 2x burst at window boundaries), Sliding Window (most accurate). Apply different limits by tier: free (100 req/min), pro (1000 req/min), enterprise (custom).

### Q45b: What is backpressure and how do you implement it?
When a producer generates work faster than a consumer can process it. Without backpressure, the consumer's queue grows until it runs out of memory. Fixes: (1) Bounded queues — producer blocks when queue is full (Channel<T> in .NET with BoundedChannelOptions). (2) Rate limiting on the producer side. (3) Consumer-driven pull instead of producer-driven push. Kafka handles this naturally — consumers read at their own pace.

### Q45c: What is the difference between horizontal and vertical scaling?
Vertical: bigger machine (more CPU, RAM). Simple but has a ceiling and requires downtime. Horizontal: more machines behind a load balancer. No ceiling in theory, requires stateless services. In K8s, horizontal scaling is native (HPA adds pods), vertical scaling is manual (change resource limits). At Combination, we use HPA — services auto-scale during peak hours and scale down overnight.

---

## DevOps & Deployment

### Q46: Compare blue-green, canary, and rolling deployments.
Blue-green: run two identical environments — blue (current) and green (new). Switch traffic all at once (DNS or load balancer). Instant rollback by switching back. Downside: double the infrastructure during deployment. Canary: route a small percentage of traffic (1-5%) to the new version, monitor metrics, gradually increase. Catches issues before full rollout. Rolling: Kubernetes default — replace pods one at a time (maxSurge, maxUnavailable). No extra infrastructure but rollback is slower (must roll forward or back). In practice, canary with automated rollback (based on error rate / latency) via Flagger or Argo Rollouts is the safest for microservices.

### Q47: What are health checks and why do you need different types?
Liveness probe: "Is the process alive?" If it fails, Kubernetes restarts the pod. Should check if the app is running, not dependencies (otherwise a database outage restarts all pods, making things worse). Readiness probe: "Can this instance serve traffic?" If it fails, the pod is removed from the Service endpoints (no traffic routed to it). Should check dependencies (database connection, required config loaded). Startup probe: "Has the app finished starting?" Prevents liveness probe from killing slow-starting apps. Pattern: `/health/live` (liveness), `/health/ready` (readiness), `/health/startup` (startup).

### Q48: What is graceful shutdown and why does it matter?
When a pod is terminated, Kubernetes sends SIGTERM, then waits (terminationGracePeriodSeconds, default 30s), then sends SIGKILL. Graceful shutdown means: stop accepting new requests, finish processing in-flight requests, close database connections, flush logs/metrics, then exit. Without it, in-flight requests get dropped (users see errors). In .NET, use `IHostApplicationLifetime.ApplicationStopping`. Also important: Kubernetes removes the pod from endpoints when SIGTERM is sent, but there is a propagation delay — add a small shutdown delay (e.g., 5 seconds) before stopping the server to allow endpoint updates to propagate.

### Q49: How do feature flags work and when do you use them?
Feature flags (LaunchDarkly, Unleash, Azure App Configuration) let you enable/disable features at runtime without deploying. Use for: gradual rollouts (enable for 10% of users), A/B testing, kill switches (disable a problematic feature instantly), trunk-based development (merge incomplete features behind flags). Implementation: simple boolean flags, percentage-based rollouts, user-segment targeting. Clean up flags after features are fully rolled out — stale flags become technical debt. In microservices, feature flags decouple deployment from release — you deploy daily but release features when ready.

### Q50: Explain the circuit breaker pattern.
When a downstream service is failing, continuing to call it wastes resources and increases latency. Circuit breaker: Closed (requests pass through, failures counted) → Open (after failure threshold, all requests fail immediately with a fallback — no calls to downstream) → Half-Open (after a timeout, allow a test request — if it succeeds, close the circuit; if it fails, reopen). Libraries: Polly (.NET), Resilience4j (Java), Hystrix (deprecated). In microservices with 60+ services, circuit breakers prevent cascading failures — one failing service should not take down the entire system. Combine with retries (with exponential backoff + jitter) and timeouts.

---

## Sorulursa

> [!faq]- "Explain what happens when an HTTP request leaves the browser"
> DNS resolves the domain to an IP (recursive lookup through cache layers → resolver → root → TLD → authoritative). TCP three-way handshake establishes connection (SYN, SYN-ACK, ACK). If HTTPS, TLS handshake follows (certificate exchange, key agreement, derive symmetric key). HTTP request goes over the encrypted channel — method, path, headers, body. Server processes it — routing, middleware, handler, database queries. Response comes back with status code, headers, body. Browser renders. Each step can fail independently — DNS timeout, TCP refused, cert invalid, 5xx error.

> [!faq]- "How do you debug a slow API endpoint?"
> Systematic: (1) Check application metrics — which endpoint, what latency percentile (p50 vs p99 tells different stories). (2) Distributed trace — follow the request through all services, find the slow span. (3) Database: check query execution plan, look for table scans, N+1 queries. (4) Network: check if the latency is in the service or between services. (5) Memory/CPU: check if the service is resource-constrained. At Combination, I fixed a 3-second endpoint by finding an N+1 in the GraphQL resolver — the trace showed 11 database calls that should have been 2.

> [!faq]- "How do you handle rate limiting in a microservices architecture?"
> Multiple layers: (1) API gateway — global rate limits per client/API key. (2) Per-service — protect downstream dependencies from overload. (3) Per-endpoint — different limits for read vs write operations. Implementation: token bucket or sliding window algorithm. Return 429 with Retry-After header. In K8s, the Ingress controller can handle basic rate limiting. For advanced scenarios, a dedicated rate limiting service (Redis-based counter).

> [!faq]- "SQL vs NoSQL — how do you choose?"
> SQL when: fixed schema, complex relationships, ACID transactions, complex queries with JOINs. NoSQL when: flexible schema (different fields per record), high write throughput, horizontal scaling, document-oriented data. At Toyota: MongoDB for vehicle state (each vehicle type has different telemetry), PostgreSQL for user accounts. At KocSistem: SQL Server for transactional data, Redis for real-time streaming. Often use both — polyglot persistence.

> [!faq]- "How do you design for high availability?"
> No single points of failure. Multiple instances behind a load balancer. Database replicas for read scaling and failover. Health checks so the load balancer routes around unhealthy instances. Circuit breakers to prevent cascading failures. Graceful degradation — return cached data when a dependency is down. Auto-scaling (K8s HPA) to handle traffic spikes. Chaos testing to verify resilience. At Combination: K8s rolling updates with readiness probes, Redis Sentinel for cache failover, Kafka replication for message durability.
