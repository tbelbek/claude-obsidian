---
tags:
  - education-kit
---

# Web Fundamentals — Education Kit

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
DNS maps domain names to IP addresses. In Kubernetes, CoreDNS handles internal service discovery — services get DNS names like `my-service.my-namespace.svc.cluster.local`. Externally, DNS can be used for load balancing (round-robin A records, weighted routing), blue-green deployments (swapping DNS records), and failover. DNS TTL matters — too long and failover is slow, too short and DNS load increases.

### Q9: How does connection pooling work at the HTTP level?
HTTP/1.1 introduced `Connection: keep-alive` to reuse TCP connections across multiple requests, avoiding the overhead of TCP+TLS handshake per request. HTTP clients and servers maintain a pool of open connections. In microservices, each service maintains connection pools to its dependencies — misconfigured pool sizes cause connection exhaustion under load or wasted resources when oversized. HttpClient in .NET should be reused (singleton or via IHttpClientFactory) because creating new instances per request exhausts sockets.

### Q9b: What is a reverse proxy and how does it differ from a load balancer?
Reverse proxy sits in front of servers, handles client requests on their behalf — SSL termination, caching, compression, request routing. A load balancer distributes traffic across multiple server instances. In practice they overlap — nginx, Traefik, and cloud load balancers do both. In Kubernetes, the Ingress controller acts as both reverse proxy and load balancer.

### Q9c: Explain connection pooling — why does it matter?
Opening a TCP connection is expensive (handshake, TLS negotiation). Connection pooling reuses open connections across requests. HTTP: `Keep-Alive` header reuses TCP connections. Database: connection pools (e.g., default pool sizes in most frameworks). Monitor active connections to avoid exhaustion under load.

### Q9d: What is the difference between synchronous and asynchronous HTTP communication?
Synchronous: client sends request, waits for response, blocks until complete. Simple but thread-blocking. Asynchronous: client sends request, continues other work, handles response when it arrives. In microservices, sync (REST/gRPC) for request-response patterns, async (Kafka/RabbitMQ) for fire-and-forget or event-driven patterns.

---

## SSL/TLS & Security

### Q10: Explain the TLS handshake process.
In TLS 1.2: ClientHello (supported cipher suites, random) -> ServerHello (chosen cipher, random, server certificate) -> client verifies certificate chain against trusted CAs -> client generates pre-master secret, encrypts with server's public key -> both derive session keys -> Finished messages confirm. TLS 1.3 simplifies this to a single round-trip (1-RTT) or even zero round-trips (0-RTT for resumed sessions). The result is a shared symmetric key used for data encryption (AES-GCM typically).

### Q11: What is a certificate chain and what happens when a certificate expires?
A certificate chain goes: leaf (server) cert -> intermediate CA -> root CA. The browser trusts root CAs in its trust store and validates the chain. When a cert expires, clients reject the TLS handshake — total outage for HTTPS traffic. Prevention: use cert-manager in Kubernetes with Let's Encrypt for automatic renewal. Monitor cert expiry with alerts.

### Q12: What is mutual TLS (mTLS) and when would you use it?
In standard TLS, only the server presents a certificate. In mTLS, both client and server present certificates and verify each other. This provides strong service-to-service authentication in microservices — you know exactly which service is calling you. Service meshes like Istio and Linkerd automate mTLS between pods. Use for zero-trust networking.

### Q13: Explain HTTPS redirect and HSTS.
HTTPS redirect: server returns 301/302 from HTTP to HTTPS URL. But the first request is still plaintext (vulnerable to MITM). HSTS header tells the browser to only use HTTPS for this domain for a specified time. HSTS preload lists eliminate even the first insecure request.

### Q14: Walk through the OWASP Top 10 vulnerabilities relevant to backend APIs.
Injection (SQL, NoSQL, command) — use parameterized queries. Broken Authentication — weak passwords, missing rate limiting. Sensitive Data Exposure — not encrypting data at rest/in transit. Broken Access Control — IDOR, missing authorization checks. Security Misconfiguration — default credentials, verbose errors in production. SSRF — user-controlled URLs hitting internal services. In microservices, each service is an attack surface — defense in depth matters.

### Q15: How do you prevent CSRF attacks in a backend API?
CSRF exploits cookies being automatically sent. For server-rendered apps: anti-CSRF tokens. For SPAs: SameSite cookie attribute (Strict or Lax). If using token-based auth (Bearer tokens in headers), CSRF is not a concern because the browser does not automatically attach Authorization headers.

### Q16: What is CORS and how do you configure it for a backend API?
CORS controls which origins can call your API from a browser. The browser sends a preflight OPTIONS request for non-simple requests. Configure `Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers`. In microservices, configure CORS at the API gateway level. Be specific with allowed origins in production.

### Q16b: What happens when an SSL certificate expires? How do you fix it?
Browsers show a security warning and refuse to connect. APIs return SSL errors. Fix: renew the certificate, install the new cert on the server/load balancer, verify with `openssl s_client`. Prevention: cert-manager in K8s auto-renews and deploys certs. Monitor cert expiry with alerts.

### Q16c: What is certificate pinning and when should you use it?
Certificate pinning hardcodes the expected certificate (or public key) in the client. Prevents MITM attacks even if a CA is compromised. Used in mobile apps and high-security APIs. Downside: cert rotation requires client update.

---

## REST API Design

### Q17: What are the principles of good REST API resource naming?
Use nouns, not verbs: `/orders` not `/getOrders`. Use plurals: `/users/123` not `/user/123`. Nest for relationships: `/users/123/orders`. Use hyphens for readability. Avoid deep nesting (max 2-3 levels). Keep URLs lowercase. Actions that do not map to CRUD can use sub-resources: `POST /orders/123/cancel`.

### Q18: Compare offset-based vs cursor-based pagination.
Offset-based (`?page=3&pageSize=20`): simple, allows jumping to any page, but breaks when data changes between requests. Performance degrades on large offsets. Cursor-based (`?cursor=eyJpZCI6MTIzfQ&limit=20`): uses an opaque token, stable under concurrent writes, consistently fast. Cursor-based is strongly preferred in high-throughput services with real-time data.

### Q19: How do you design API error responses?
Use a consistent structure across all services. Include: machine-readable error code, human-readable message, field-level details, and correlation/trace ID for debugging. Use RFC 7807 (Problem Details for HTTP APIs) as a standard.

### Q20: What are the common API versioning strategies?
URL path versioning (`/api/v1/users`): most common, easy to route. Header versioning: cleaner URLs but harder to test. Query parameter: Azure's approach. URL versioning wins for simplicity. Version only on breaking changes — adding fields does not need a new version.

### Q21: How do you implement rate limiting in an API?
Common algorithms: Token Bucket (allows bursts), Sliding Window (smoother). Return 429 Too Many Requests with `Retry-After` header. In microservices, rate limiting is typically at the API gateway level. For distributed rate limiting across instances, use Redis (atomic INCR with TTL). Different limits for different endpoints.

### Q22: What are idempotency keys and why do they matter?
A unique identifier (usually UUID) sent by the client with a request. The server stores the key with the result. If the same key is sent again, the server returns the stored result. Critical for payment APIs, order creation, any non-idempotent operation where retries could cause duplicates.

### Q23: What is HATEOAS and is it practical?
HATEOAS means API responses include links to related actions and resources. In theory, clients discover the API dynamically. In practice, very few APIs implement full HATEOAS. However, including pagination links and self links is widely adopted and genuinely useful.

### Q23b: How do you design error responses in a REST API?
Consistent format across all endpoints. Include: error code (machine-readable), message (human-readable), details (field-level validation errors), request ID (for debugging). Never expose stack traces in production.

### Q23c: How do you handle API versioning in practice?
URL path (`/v1/users`) is simplest and most common. In GraphQL, no versioning — deprecate fields with `@deprecated`. In gRPC, versioned proto directories (v1/, v2/).

---

## Authentication & Authorization

### Q24: Explain JWT structure and how validation works.
A JWT has three base64url-encoded parts: Header (algorithm, type) . Payload (claims — sub, exp, iat, iss, custom claims) . Signature (HMAC or RSA/ECDSA sign of header+payload). Validation: decode header, verify signature, check `exp`, `iss`, `aud`. Never store sensitive data in JWT payload — it is base64, not encrypted.

### Q25: Describe OAuth2 flows and when to use each.
Authorization Code flow (with PKCE): for web/mobile apps — most secure for user-facing apps. Client Credentials flow: for service-to-service communication — no user involved. Implicit flow: deprecated. Resource Owner Password: only for trusted first-party apps. In microservices, Client Credentials for inter-service, Authorization Code + PKCE for user-facing APIs.

### Q26: Compare API keys vs OAuth tokens.
API keys are simple, long-lived strings identifying a client application. OAuth tokens are short-lived, scoped, revocable, and tied to a specific user+application combination. Use API keys for server-to-server with trusted partners. Use OAuth tokens for user-delegated access with fine-grained permissions.

### Q27: Explain session-based vs token-based authentication.
Session-based: server stores session state, sends session ID cookie. Requires shared session store for scaling. Token-based: server issues signed token (JWT), client sends in Authorization header. Stateless, scales horizontally. Downside: cannot revoke a JWT before expiry without a blacklist. Use short-lived access tokens + refresh tokens.

### Q28: What is the difference between RBAC and ABAC?
RBAC: users have roles, permissions are assigned to roles. Simple but can lead to role explosion. ABAC: policies evaluate attributes of user, resource, action, and environment. More flexible for complex scenarios.

### Q29: How do you secure inter-service communication?
Layer 1: Network isolation (VPC, K8s network policies). Layer 2: mTLS. Layer 3: Service-to-service auth tokens (OAuth2 Client Credentials, or JWT propagation). Layer 4: Authorization per service. Do not rely on any single layer.

### Q29b: How does JWT validation work step by step?
(1) Extract token from `Authorization: Bearer <token>` header. (2) Split into header.payload.signature. (3) Verify signature using the signing key. (4) Check claims: `exp`, `iss`, `aud`, `nbf`. (5) If all pass, trust the claims.

### Q29c: How do you handle inter-service authentication in microservices?
Options: (1) Mutual TLS — services authenticate each other at transport level. (2) Service account tokens — each service gets a JWT signed by a trusted authority. (3) K8s service accounts with OIDC federation — pods authenticate via workload identity.

---

## Caching

### Q30: Explain HTTP caching mechanisms (Cache-Control, ETag, Last-Modified).
`Cache-Control: max-age=3600` tells the client/proxy to cache for 3600 seconds. `no-cache` means always revalidate. `no-store` means never cache. `ETag` is a fingerprint for conditional requests (304 Not Modified). `private` means only browser can cache, `public` allows shared caches.

### Q31: When and how do you use Redis for caching in microservices?
Use Redis for: frequently read, rarely changing data, computed results, session storage, rate limiting counters. Pattern: check Redis first, on miss query database, write to Redis with TTL. Set TTLs always. Each service should own its cache namespace.

### Q32: What is cache invalidation and why is it hard?
When source data changes, cached copies become stale. Strategies: TTL-based (let it expire), event-driven (publish change event, invalidate cache), write-through (update cache and DB simultaneously), write-behind (update cache, async write to DB).

### Q33: What is a cache stampede and how do you prevent it?
A popular cache key expires, hundreds of concurrent requests all miss cache, all hit the database. Prevention: lock-based recomputation, probabilistic early recomputation, stale-while-revalidate, never-expire with async refresh.

### Q34: How does CDN caching work and when do you use it for APIs?
CDN caches responses at edge locations. For APIs: cache GET responses for public, stable data. CDN caching is excellent for read-heavy, public APIs. For authenticated APIs, CDN is used primarily for TLS termination and DDoS protection.

### Q34b: What is cache stampede and how do you prevent it?
When a cache entry expires, many requests hit the database simultaneously. Fixes: (1) Lock, (2) Background refresh, (3) Stale-while-revalidate.

---

## Database & Data

### Q35: When do you choose SQL vs NoSQL?
SQL: strong consistency, complex queries with joins, ACID transactions, well-understood schema. NoSQL: flexible schema, horizontal scaling, high write throughput, denormalized data. In microservices, each service picks the right database for its domain.

### Q36: What is the N+1 query problem and how do you solve it?
N+1 occurs when you query N items, then make N additional queries to fetch related data. Solution: eager loading/joins, batch loading, or DataLoader pattern. Always check your ORM's generated SQL.

### Q37: Explain database indexing — when and how to use indexes.
An index speeds up lookups at the cost of slower writes and extra storage. Composite indexes follow the leftmost prefix rule. Covering indexes avoid table lookups. Too many indexes slow writes. Use EXPLAIN to verify index usage.

### Q38: What is the difference between ACID and BASE?
ACID (Atomicity, Consistency, Isolation, Durability): strong transactional guarantees. BASE (Basically Available, Soft state, Eventually consistent): trade strong consistency for availability. Microservices often use ACID within a single service but BASE across services.

### Q39: What is connection pooling and why does it matter?
Creating a database connection is expensive (50-200ms). Connection pooling reuses pre-established connections. Configure min/max pool size based on load. In Kubernetes with many pod replicas, total connections add up quickly — use a connection proxy to multiplex.

### Q40: Explain eventual consistency and its implications for microservices.
After a write, all replicas will converge eventually, but reads may temporarily return stale data. Design for it: read-your-own-writes consistency, optimistic UI updates, idempotent consumers.

---

## Scalability

### Q41: Compare horizontal vs vertical scaling.
Vertical: add more CPU/RAM (simple, has a ceiling). Horizontal: add more instances (requires stateless services). Kubernetes makes horizontal scaling native via HPA.

### Q42: What load balancing strategies exist?
Round Robin: distribute evenly. Weighted Round Robin: more traffic to stronger instances. Least Connections: route to least busy. IP Hash: sticky sessions. gRPC requires L7 load balancing because HTTP/2 multiplexes over one connection.

### Q43: Why must services be stateless for scalability?
Stateless services can be freely killed, restarted, and scaled. Move state externally: sessions to Redis, files to object storage, cache to Redis/Memcached.

### Q44: Explain service discovery in a microservices architecture.
Client-side discovery: client queries a registry and picks an instance. Server-side discovery: client calls a DNS name/load balancer that routes to an available instance. In Kubernetes, server-side discovery is built in.

### Q45: What are common rate limiting patterns at scale?
Local rate limiting: per-instance counters. Global rate limiting: centralized counter in Redis. Algorithms: Token Bucket, Leaky Bucket, Fixed Window, Sliding Window.

### Q45b: What is backpressure and how do you implement it?
When a producer generates work faster than a consumer can process it. Fixes: bounded queues, rate limiting on the producer side, consumer-driven pull instead of producer-driven push.

### Q45c: What is the difference between horizontal and vertical scaling?
Vertical: bigger machine (has a ceiling, may require downtime). Horizontal: more machines behind a load balancer (requires stateless services).

---

## DevOps & Deployment

### Q46: Compare blue-green, canary, and rolling deployments.
Blue-green: switch traffic all at once between two environments. Instant rollback. Canary: route small percentage to new version, monitor, gradually increase. Rolling: replace pods one at a time — Kubernetes default.

### Q47: What are health checks and why do you need different types?
Liveness: "Is the process alive?" Should not check dependencies. Readiness: "Can it serve traffic?" Should check dependencies. Startup: "Has it finished starting?"

### Q48: What is graceful shutdown and why does it matter?
Stop accepting new requests, finish in-flight requests, close connections, flush logs, then exit. Without it, in-flight requests get dropped. Add a small shutdown delay to allow endpoint updates to propagate.

### Q49: How do feature flags work and when do you use them?
Enable/disable features at runtime without deploying. Use for: gradual rollouts, A/B testing, kill switches, trunk-based development. Clean up flags after features are fully rolled out.

### Q50: Explain the circuit breaker pattern.
When a downstream service is failing, stop calling it. Three states: Closed -> Open (after failures) -> Half-Open (test request). Combine with retries and timeouts. Prevents cascading failures.

---

## Common Questions

**"Explain what happens when an HTTP request leaves the browser"**
DNS resolves domain to IP. TCP three-way handshake. TLS handshake if HTTPS. HTTP request sent. Server processes. Response returns. Each step can fail independently.

**"How do you debug a slow API endpoint?"**
Check application metrics (which endpoint, what percentile). Distributed trace — follow the request. Database: check execution plan. Network: latency between services. Memory/CPU: resource constraints.

**"SQL vs NoSQL — how do you choose?"**
SQL when: fixed schema, complex relationships, ACID transactions. NoSQL when: flexible schema, high write throughput, horizontal scaling. Often use both — polyglot persistence.

**"How do you design for high availability?"**
No single points of failure. Multiple instances behind a load balancer. Database replicas. Health checks. Circuit breakers. Graceful degradation. Auto-scaling. Chaos testing.
