---
tags:
  - interview-kit
  - interview-kit/reference
up: "[[00-dashboard]]"
---

*[[00-dashboard]]*

# Web Architecture — Advanced Senior Interview Questions

> [!tip] Deep-dive questions beyond basics. Covers API paradigms, protocols, auth flows, networking, caching, observability, event-driven patterns, and serialization. Cross-reference with [[ref-web-fundamentals]], [[ref-graphql]], [[ref-grpc]], [[ref-observability-stack]].

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Q1: Deep compare GraphQL vs REST vs gRPC -- when does each shine and what are the trade-offs?\|GraphQL vs REST vs gRPC]] | GraphQL=client flexibility, REST=simplicity, gRPC=perf | [[#Q2: When would you use a hybrid API stack? Give a real architecture example.\|hybrid API stack]] | REST public, GraphQL frontend, gRPC internal |
| [[#Q3: Explain the WebSocket handshake and frame protocol in detail.\|WebSocket handshake]] | HTTP Upgrade 101, binary frames, ping/pong | [[#Q4: How do you scale WebSocket connections across multiple server instances?\|scaling WebSockets]] | sticky sessions, Redis pub/sub, message broker |
| [[#Q5: Walk through the OAuth 2.0 Authorization Code flow with PKCE step by step.\|OAuth2 + PKCE]] | code_verifier hashed, no client_secret needed | [[#Q6: How does OpenID Connect layer on top of OAuth 2.0? What is the difference?\|OIDC vs OAuth]] | OIDC adds ID token (JWT) for authentication |
| [[#Q7: What is a service mesh and when do you need one?\|service mesh]] | sidecar proxies handle mTLS, routing, observability | [[#Q8: Compare Istio vs Linkerd -- architecture, philosophy, and trade-offs.\|Istio vs Linkerd]] | Istio=feature-rich/complex, Linkerd=simple/light |
| [[#Q9: Compare the major rate limiting algorithms -- token bucket, leaky bucket, fixed window, sliding window.\|rate limiting algos]] | token bucket=bursty, leaky=smooth, sliding=accurate | [[#Q10: How do you implement distributed rate limiting across multiple server instances?\|distributed rate limit]] | Redis + Lua atomic scripts, sliding window log |
| [[#Q11: Explain how database connection pooling works internally.\|connection pooling]] | min/max size, idle timeout, leak detection | [[#Q12: How do you diagnose and fix connection pool exhaustion?\|pool exhaustion]] | slow queries hold connections, monitor active count |
| [[#Q13: What are the main CDN cache invalidation strategies and their trade-offs?\|CDN invalidation]] | TTL, purge API, surrogate keys, stale-while | [[#Q14: How does HTTP/3 with QUIC work? Why was it needed?\|HTTP/3 QUIC]] | UDP-based, 0-RTT, no head-of-line blocking |
| [[#Q15: Explain zero-trust networking principles and why the perimeter model failed.\|zero trust]] | never trust, always verify, least privilege | [[#Q16: How do you implement zero trust for backend microservices?\|zero trust impl]] | mTLS, SPIFFE/SPIRE, policy engines |
| [[#Q17: What is OpenTelemetry and how does distributed tracing work end-to-end?\|OTel tracing]] | traces > spans > context propagation via W3C headers | [[#Q18: How do you implement effective observability? What is the relationship between metrics, logs, and traces?\|observability strategy]] | metrics+logs+traces correlated, SLO-driven alerts |
| [[#Q19: Compare the major event-driven architecture patterns -- event sourcing, CQRS, saga, outbox.\|EDA patterns]] | event sourcing, CQRS, saga, outbox pattern | [[#Q20: How do you guarantee exactly-once processing in an event-driven system?\|exactly-once]] | idempotent consumers + deduplication table |
| [[#Q21: Compare Protobuf vs Avro vs MessagePack -- when do you use each?\|serialization formats]] | Protobuf=fast/typed, Avro=schema evolution, MsgPack=schemaless | [[#Q22: When do you choose which serialization format?\|when to use which]] | gRPC=Protobuf, Kafka=Avro, cache=MsgPack |

---

## 1 -- API Paradigms: GraphQL vs REST vs gRPC

### Q1: Deep compare GraphQL vs REST vs gRPC -- when does each shine and what are the trade-offs?

| Dimension | REST | GraphQL | gRPC |
|-----------|------|---------|------|
| **Transport** | HTTP/1.1 or HTTP/2 | HTTP (single POST endpoint) | HTTP/2 (binary framing) |
| **Data format** | JSON (typically) | JSON | Protocol Buffers (binary) |
| **Contract** | OpenAPI / Swagger | Schema (SDL) | .proto files |
| **Versioning** | URL (/v1, /v2) or headers | No versioning -- additive changes, deprecate fields | Package versioning in proto (v1, v2) |
| **Overfetching** | Common (fixed response shape) | Eliminated (client specifies fields) | Minimal (typed messages) |
| **Underfetching** | Requires multiple round-trips | Single query fetches related data | Requires multiple RPC calls |
| **Streaming** | SSE, chunked transfer | Subscriptions (WebSocket) | Bidirectional streaming native |
| **Browser support** | Full | Full (over HTTP POST) | Limited (needs grpc-web proxy) |
| **Performance** | Moderate | Moderate (parsing overhead) | Highest (binary, HTTP/2, multiplexing) |
| **Caching** | Native HTTP caching (GET + ETag) | Hard (POST only, need persisted queries) | No HTTP caching (custom needed) |
| **Learning curve** | Low | Medium | Medium-High |
| **Best for** | Public APIs, simple CRUD | Frontend-driven APIs, mobile (bandwidth) | Service-to-service, low-latency internal |

**Key interview insight**: In 2025, hybrid stacks are the norm. REST for public/partner APIs (simplicity, cacheability), GraphQL for client-facing BFFs (frontend flexibility, reduce round-trips on mobile), gRPC for internal service-to-service (performance, strong typing, streaming). The decision is not "pick one" -- it's "where does each fit."

### Q2: When would you use a hybrid API stack? Give a real architecture example.

A typical modern architecture uses all three. The **API gateway** exposes REST endpoints for external partners. The **BFF (Backend-for-Frontend)** exposes a GraphQL endpoint that aggregates data from multiple internal services. Internal services communicate via **gRPC** for performance and type safety. Example flow: Mobile app --> GraphQL BFF --> gRPC to OrderService + ProductService + UserService. Each layer chosen for its strengths: GraphQL reduces mobile round-trips, gRPC gives fast binary internal calls. The BFF pattern also decouples frontend evolution from backend service changes.

---

## 2 -- WebSocket Protocol Deep Dive

### Q3: Explain the WebSocket handshake and frame protocol in detail.

**Handshake**: Client sends an HTTP/1.1 GET request with `Upgrade: websocket`, `Connection: Upgrade`, `Sec-WebSocket-Key` (base64 random), and `Sec-WebSocket-Version: 13`. Server responds with HTTP 101 Switching Protocols, `Sec-WebSocket-Accept` (SHA-1 hash of key + magic GUID). After this, the connection upgrades from HTTP to a persistent, full-duplex TCP connection.

**Frame protocol**: Data is sent in frames with an opcode (0x1 text, 0x2 binary, 0x8 close, 0x9 ping, 0xA pong), payload length (7 bits, or 16/64 bits for larger), masking key (client-to-server frames must be masked), and payload. Control frames (ping/pong/close) can be interleaved with data frames. The ping/pong mechanism serves as a heartbeat to detect dead connections.

**Key differences from HTTP**: No request/response cycle -- either side can send at any time. No headers per message (low overhead). Connection is stateful and persistent.

### Q4: How do you scale WebSocket connections across multiple server instances?

WebSockets are stateful -- a connection is tied to a specific server instance. Scaling strategies:

1. **Sticky sessions**: Load balancer routes a client to the same backend (by IP or cookie). Simple but limits failover.
2. **Redis Pub/Sub or message broker**: When Server A needs to push to a client on Server B, it publishes to Redis; Server B subscribes and forwards. This decouples message routing from connection ownership.
3. **Dedicated WebSocket gateway**: A service (e.g., Socket.IO with Redis adapter, or a custom gateway) manages all WS connections. Backend services publish events to the gateway via message queue.
4. **Connection state externalization**: Store connection metadata (user ID, server ID) in Redis. On reconnect, route to any server that can restore state.
5. **Horizontal scaling limits**: Each server can handle ~50K-100K concurrent connections (OS file descriptor limits). Plan capacity accordingly.

**Security considerations**: Validate the `Origin` header to prevent cross-site WebSocket hijacking. Implement per-connection rate limiting. Use `wss://` (TLS). Authenticate during the handshake (token in query param or first message). Set idle timeouts and max message size.

---

## 3 -- OAuth 2.0 / OpenID Connect

### Q5: Walk through the OAuth 2.0 Authorization Code flow with PKCE step by step.

PKCE (Proof Key for Code Exchange) is the recommended flow for all clients (SPAs, mobile, server-side) as of OAuth 2.1.

1. **Client generates code_verifier**: Random string (43-128 chars). Kept secret on client.
2. **Client computes code_challenge**: `BASE64URL(SHA256(code_verifier))`. Method = S256.
3. **Authorization request**: Client redirects user to authorization server with `response_type=code`, `client_id`, `redirect_uri`, `scope`, `state` (CSRF protection), `code_challenge`, `code_challenge_method=S256`.
4. **User authenticates and consents** at the authorization server.
5. **Authorization server redirects** back to `redirect_uri` with `code` and `state`.
6. **Client validates state** matches what it sent (prevents CSRF).
7. **Token exchange**: Client sends POST to token endpoint with `grant_type=authorization_code`, `code`, `redirect_uri`, `client_id`, `code_verifier`.
8. **Authorization server verifies**: Hashes `code_verifier`, compares with stored `code_challenge`. If match, issues `access_token`, `refresh_token`, and optionally `id_token`.

**Why PKCE matters**: Without it, an attacker who intercepts the authorization code (mobile deep link, browser history) can exchange it for tokens. With PKCE, they also need the `code_verifier` which never left the client. This replaces the need for `client_secret` in public clients.

### Q6: How does OpenID Connect layer on top of OAuth 2.0? What is the difference?

**OAuth 2.0** is an **authorization** framework -- it answers "what can this client access on my behalf?" It issues access tokens but says nothing about who the user is.

**OpenID Connect (OIDC)** is an **authentication** layer built on top of OAuth 2.0. It adds:
- **ID Token**: A JWT containing claims about the user (sub, name, email, iat, exp, iss, aud). Signed by the identity provider.
- **UserInfo endpoint**: A protected resource returning user profile information.
- **Standard scopes**: `openid` (required), `profile`, `email`, `address`, `phone`.
- **Discovery document**: `/.well-known/openid-configuration` returns all endpoints, supported flows, and signing keys.

**In practice**: When your app needs to know WHO the user is, use OIDC (get the ID token). When your API needs to know WHAT the user can do, use OAuth 2.0 (validate the access token's scopes/claims). Most modern identity providers (Entra ID, Auth0, Keycloak) implement both together.

**Other OAuth 2.0 flows**:
- **Client Credentials**: Machine-to-machine, no user involved. Service authenticates with client_id + client_secret, gets access_token directly.
- **Device Authorization (Device Code)**: For devices without a browser (smart TVs, CLI tools). Device shows a code, user enters it on another device.
- **Refresh Token**: Exchange refresh_token for new access_token without re-authenticating the user. Refresh tokens should be rotated on use.

---

## 4 -- Service Mesh (Istio, Linkerd)

### Q7: What is a service mesh and when do you need one?

A service mesh is a **dedicated infrastructure layer** that handles service-to-service communication. It works by injecting a **sidecar proxy** (e.g., Envoy) into each pod. All traffic flows through the proxy transparently -- the application code doesn't change.

**What it provides**:
- **mTLS everywhere**: Automatic mutual TLS between services without application changes.
- **Traffic management**: Canary deployments, traffic splitting, retries, timeouts, circuit breaking.
- **Observability**: Automatic metrics (latency, error rates, throughput), distributed tracing, access logs -- all without instrumentation code.
- **Policy enforcement**: Authorization policies (which service can call which), rate limiting.

**When you need one**: When you have 10+ microservices and cross-cutting concerns (security, observability, traffic control) are becoming painful to implement in each service. When you need mTLS without changing application code. When you want consistent retry/timeout policies across all services.

**When you don't need one**: Small number of services (< 5-10). The added complexity (sidecar resource usage, debugging difficulty, operational overhead) outweighs benefits. A simpler solution (library-based service mesh like Dapr, or just configuring your ingress controller) may suffice.

### Q8: Compare Istio vs Linkerd -- architecture, philosophy, and trade-offs.

| Dimension | Istio | Linkerd |
|-----------|-------|---------|
| **Proxy** | Envoy (C++, feature-rich) | linkerd2-proxy (Rust, purpose-built) |
| **Philosophy** | Enterprise-first, comprehensive features | Simplicity-first, minimal overhead |
| **Resource usage** | Higher (Envoy sidecar ~50-100MB RAM) | Lower (~10-20MB RAM per proxy) |
| **Configuration** | Thousands of options, CRDs | Deliberately limited, sensible defaults |
| **mTLS** | Manual or auto, configurable | On by default, zero-config |
| **Traffic management** | VirtualService, DestinationRule (powerful but complex) | TrafficSplit, ServiceProfile (simpler) |
| **Multi-cluster** | Supported (complex setup) | Supported (simpler model) |
| **Observability** | Prometheus, Jaeger, Kiali integration | Built-in dashboard, Prometheus metrics |
| **WASM extensibility** | Yes (Envoy WASM filters) | No |
| **CNCF status** | Graduated (2023) | Graduated (2024) |
| **Best for** | Large enterprises needing fine-grained control | Teams wanting simple, low-overhead mesh |

**Interview insight**: Istio graduated CNCF in 2023 and introduced **ambient mesh** (ztunnel) as an alternative to sidecars -- a per-node proxy that handles L4 (mTLS) without sidecars, with optional L7 waypoint proxies. This reduces resource overhead significantly. Linkerd countered with its ultra-lightweight Rust proxy and simpler operational model. The choice depends on organizational complexity and team capacity to manage the mesh.

---

## 5 -- API Rate Limiting Algorithms

### Q9: Compare the major rate limiting algorithms -- token bucket, leaky bucket, fixed window, sliding window.

**Token Bucket**: A bucket holds tokens (max = burst capacity). Tokens are added at a fixed rate. Each request consumes one token. If bucket is empty, request is rejected. **Allows bursts** up to bucket size while maintaining average rate. Used by Stripe, AWS. Simple, memory-efficient (2 values: token count + last refill timestamp).

**Leaky Bucket**: Requests enter a queue (bucket). Processed at a fixed rate (the "leak"). If queue is full, new requests are dropped. **Smooths out bursts** -- output rate is always constant. Good for APIs that need steady throughput (e.g., payment processing). Essentially a FIFO queue with fixed processing rate.

**Fixed Window**: Count requests in fixed time windows (e.g., 100 req/minute). Reset counter at window boundary. **Problem**: Burst at window edges -- 100 requests at 0:59 + 100 at 1:00 = 200 in 2 seconds. Simple but inaccurate at boundaries.

**Sliding Window Log**: Store timestamp of every request. Count requests in the last N seconds. Precise but **memory-intensive** (stores every timestamp). O(n) per check.

**Sliding Window Counter**: Hybrid of fixed window + sliding window. Uses weighted count: `current_window_count * overlap_percentage + previous_window_count * (1 - overlap_percentage)`. Memory-efficient (two counters), smooth, no boundary burst problem. **Best general-purpose choice**.

| Algorithm | Burst handling | Memory | Accuracy | Complexity |
|-----------|---------------|--------|----------|------------|
| Token Bucket | Allows bursts | O(1) | Good | Low |
| Leaky Bucket | Smooths bursts | O(1) | Good | Low |
| Fixed Window | Edge bursts | O(1) | Poor at edges | Lowest |
| Sliding Window Log | No bursts | O(n) | Exact | Medium |
| Sliding Window Counter | Controlled | O(1) | Very good | Medium |

### Q10: How do you implement distributed rate limiting across multiple server instances?

Single-server rate limiting breaks when you have multiple instances. Solutions:

1. **Centralized store (Redis)**: Store counters in Redis. Use Lua scripts for atomic check-and-increment. `MULTI/EXEC` or `EVALSHA` to avoid race conditions. **Trade-off**: Added latency per request (network hop to Redis), Redis becomes a SPOF.
2. **Sliding window with Redis sorted sets**: `ZADD` timestamp, `ZREMRANGEBYSCORE` old entries, `ZCARD` to count. Precise but more memory.
3. **Local + sync**: Each instance maintains local counters, periodically syncs to central store. Allows slight over-limit but avoids Redis latency on every request.
4. **API Gateway level**: Let the gateway (Kong, Envoy, AWS API Gateway) handle rate limiting. They have built-in distributed rate limiting with Redis/DynamoDB backends.

**Headers to return**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`. Return 429 Too Many Requests with `Retry-After` header.

---

## 6 -- Database Connection Pooling

### Q11: Explain how database connection pooling works internally.

A connection pool maintains a set of pre-established database connections. Instead of opening/closing connections per request (expensive: TCP handshake + auth + SSL = 20-50ms), the application **borrows** a connection, uses it, and **returns** it.

**Key parameters**:
- **Min pool size**: Connections kept open even when idle. Avoids cold-start latency.
- **Max pool size**: Upper limit. Requests beyond this wait in a queue or get rejected. Typical: 10-20 per instance for OLTP.
- **Idle timeout**: Close connections idle longer than N seconds to free database resources.
- **Max lifetime**: Close connections after N minutes regardless of use (handles database-side connection limits, DNS changes, credential rotation).
- **Connection validation**: Test before borrowing (e.g., `SELECT 1`) or rely on TCP keepalive. HikariCP uses `connectionTestQuery` or JDBC4 `isValid()`.
- **Leak detection**: Alert if a connection is not returned within N seconds.

**Sizing formula (from HikariCP)**: `pool_size = (core_count * 2) + effective_spindle_count`. For SSDs, often 10-20 per instance is sufficient. More connections != more throughput -- too many causes context switching and lock contention on the database.

### Q12: How do you diagnose and fix connection pool exhaustion?

**Symptoms**: Requests hang, then timeout. Latency spikes but database CPU is low. Error: "Cannot acquire connection from pool" or "Connection pool exhausted."

**Root causes**:
1. **Connection leaks**: Code borrows a connection but never returns it (missing `using`/`try-with-resources`, exception path skips cleanup). Fix: enable leak detection (HikariCP `leakDetectionThreshold`), use language-level resource management.
2. **Slow queries**: Queries take too long, holding connections. 20 connections + 5-second queries = max 4 req/sec. Fix: optimize queries, add indexes, set query timeout.
3. **Transaction scope too large**: Business logic inside a transaction (calling external APIs while holding a connection). Fix: minimize transaction scope.
4. **Pool too small for load**: More concurrent requests than pool size. Fix: increase pool size (but check database max_connections first). If 10 instances * 20 pool = 200 connections hitting a database that supports 100 max, you're still stuck.
5. **External dependency blocking**: Connection held while waiting for another service. Fix: move external calls outside the connection scope.

**Monitoring**: Track pool active/idle/waiting counts, connection wait time, connection usage duration. Alert on wait time > 1s and active count near max.

---

## 7 -- CDN Cache Invalidation Strategies

### Q13: What are the main CDN cache invalidation strategies and their trade-offs?

**Why it's hard**: Phil Karlton's quote -- "There are only two hard things in computer science: cache invalidation and naming things." CDN caches are distributed globally, invalidation must propagate to all edge nodes.

**Strategies**:

1. **TTL-based expiration**: Set `Cache-Control: max-age=3600`. Content expires after TTL. Simple, predictable. **Trade-off**: Stale data during TTL window. Short TTL = more origin hits. Long TTL = longer staleness.

2. **Purge/Ban API**: CDN provides API to invalidate specific URLs or patterns. Cloudflare `Purge by URL`, Fastly `Purge by surrogate key`. **Trade-off**: Propagation takes seconds-minutes across global PoPs. Need to integrate into deployment pipeline.

3. **Surrogate keys (cache tags)**: Tag cached objects with logical keys (e.g., `product-123`, `category-electronics`). Invalidate all objects matching a tag. **Best for**: Complex invalidation (update a product -> purge all pages showing that product). Supported by Fastly, Cloudflare, Varnish.

4. **Stale-while-revalidate**: `Cache-Control: max-age=60, stale-while-revalidate=300`. Serve stale content immediately while fetching fresh content in the background. User gets fast response, eventual freshness. **Best for**: Content that can tolerate brief staleness.

5. **Versioned URLs**: Append hash or version to URL (`/styles.abc123.css`). New deploy = new URL = CDN treats it as new object. Old URL stays cached (harmless). **Best for**: Static assets (JS, CSS, images). Cannot work for API responses.

6. **Origin-managed invalidation**: Origin server sends `Cache-Control: no-cache` (always revalidate with origin) or `must-revalidate`. With `ETag` / `If-None-Match`, CDN revalidates but avoids re-downloading if content unchanged (304). **Trade-off**: Every request hits origin for validation.

**Interview answer**: For APIs, use short TTL + stale-while-revalidate. For static assets, use versioned URLs (cache forever). For dynamic content tied to business events, use surrogate key purging triggered by domain events.

---

## 8 -- HTTP/3 and QUIC

### Q14: How does HTTP/3 with QUIC work? Why was it needed?

**The problem with HTTP/2 over TCP**: HTTP/2 multiplexes streams over a single TCP connection. If one TCP packet is lost, ALL streams are blocked until retransmission (TCP head-of-line blocking). TLS handshake adds 1-2 round trips on top of TCP handshake.

**QUIC solves this**:
- **Built on UDP**: QUIC is a transport protocol running over UDP. It reimplements reliability, congestion control, and flow control at the application layer.
- **Independent streams**: Each QUIC stream is independent. Packet loss on one stream doesn't block others. True multiplexing.
- **Integrated TLS 1.3**: Crypto handshake is part of the QUIC handshake. Connection setup in 1 RTT (vs 2-3 RTT for TCP + TLS). **0-RTT** for returning clients (send data in the first packet using cached keys).
- **Connection migration**: QUIC connections are identified by a Connection ID, not the 4-tuple (src IP, dst IP, src port, dst port). When a mobile device switches from Wi-Fi to cellular, the connection survives.
- **Improved loss recovery**: Per-packet sequence numbers (no TCP ambiguity), more accurate RTT estimation, better congestion control.

**Adoption status**: Google (YouTube, Search), Meta (Facebook, Instagram), Cloudflare (entire network). ~30% of web traffic uses QUIC as of 2025.

**Backend implications**: Most backends still serve HTTP/2. QUIC terminates at the CDN/load balancer edge. Between LB and origin, HTTP/2 or gRPC is used. NGINX and Caddy have experimental QUIC support. For service-to-service, gRPC over HTTP/2 remains dominant.

---

## 9 -- Zero-Trust Networking

### Q15: Explain zero-trust networking principles and why the perimeter model failed.

**Traditional (perimeter) model**: "Castle and moat" -- hard shell (firewall) protecting a trusted internal network. Once inside, everything is trusted. **Failed because**: VPNs extend the perimeter to remote workers, lateral movement after breach is trivial, cloud/hybrid deployments have no clear perimeter, insider threats exist.

**Zero-trust principles**:
1. **Never trust, always verify**: Every request must be authenticated and authorized, even from "internal" networks.
2. **Least privilege**: Grant minimum permissions needed. Just-in-time access, not permanent roles.
3. **Assume breach**: Design as if the attacker is already inside. Limit blast radius.
4. **Micro-segmentation**: Network divided into small zones. Each service-to-service call is authorized independently.
5. **Continuous verification**: Not just at login -- re-evaluate trust continuously based on device health, location, behavior anomalies.

### Q16: How do you implement zero trust for backend microservices?

1. **mTLS everywhere**: Every service has a certificate. Both client and server authenticate. No plaintext internal traffic. Use a service mesh (Istio/Linkerd) to automate certificate management and rotation.
2. **SPIFFE/SPIRE**: SPIFFE (Secure Production Identity Framework for Everyone) provides workload identities. SPIRE is the implementation. Each workload gets a SVID (SPIFFE Verifiable Identity Document). Identity is tied to workload attributes, not network location.
3. **Policy engines**: OPA (Open Policy Agent) or Istio AuthorizationPolicy to define which service can call which endpoint. Policies are code, version-controlled, auditable.
4. **No implicit trust from network location**: Being in the same VPC or Kubernetes namespace does not grant access. Every call carries identity and is authorized.
5. **Short-lived credentials**: Certificates valid for hours, not years. Auto-rotated. No long-lived API keys.
6. **Encrypted at rest and in transit**: All data encrypted. All traffic encrypted (mTLS).
7. **Centralized logging and monitoring**: Every access decision is logged. Anomaly detection on access patterns.

---

## 10 -- Observability (OpenTelemetry, Distributed Tracing)

### Q17: What is OpenTelemetry and how does distributed tracing work end-to-end?

**OpenTelemetry (OTel)** is a CNCF project providing a vendor-neutral standard for instrumenting, generating, collecting, and exporting telemetry data -- **traces, metrics, and logs**.

**Distributed tracing flow**:
1. A request enters Service A. OTel SDK creates a **trace** (unique `traceId`) and a root **span** (operation name, start time, attributes).
2. Service A calls Service B. OTel **injects** the trace context into HTTP headers using W3C `traceparent` format: `00-{traceId}-{spanId}-{flags}`.
3. Service B **extracts** the context from headers, creates a **child span** linked to the parent via `parentSpanId`.
4. Each span records: operation name, start/end time, status (OK/ERROR), attributes (http.method, db.statement), events (logs within span context).
5. Spans are exported to a **collector** (OTel Collector), which processes (batching, sampling, enrichment) and exports to a backend (Jaeger, Tempo, Zipkin, Datadog).
6. The backend assembles spans into a complete trace, visualized as a waterfall/Gantt chart.

**Sampling strategies**: Head-based (decide at trace start -- e.g., sample 1%), tail-based (decide after trace completes -- keep traces with errors or high latency), adaptive (adjust rate based on traffic).

### Q18: How do you implement effective observability? What is the relationship between metrics, logs, and traces?

**Three pillars, correlated**:
- **Metrics**: Aggregated numbers over time (request count, p99 latency, error rate, saturation). Cheap to store, good for alerting and dashboards. Tools: Prometheus, Datadog.
- **Logs**: Discrete events with context. Expensive at scale. Structured logging (JSON) with `traceId` and `spanId` enables correlation. Tools: Loki, ELK.
- **Traces**: End-to-end request journey across services. Expensive but invaluable for debugging distributed systems. Tools: Tempo, Jaeger.

**Correlation is the key**: A metric alert fires (p99 latency spike). Click through to **exemplar traces** showing slow requests. From a trace span, jump to **correlated logs** for that exact operation (matched by traceId). This is the "drill-down" that makes observability actionable.

**OTel Collector architecture**: Services export to OTel Collector (receiver -> processor -> exporter pipeline). Collector handles batching, retry, sampling, attribute enrichment. Decouples application from backend vendor -- change backend without changing application code.

**SLO-driven alerting**: Define SLOs (e.g., 99.9% of requests < 500ms). Alert on burn rate (how fast you're consuming error budget), not on individual threshold breaches. Multi-window burn rate alerts reduce noise while catching real issues.

---

## 11 -- Event-Driven Architecture Patterns

### Q19: Compare the major event-driven architecture patterns -- event sourcing, CQRS, saga, outbox.

**Event Sourcing**: Store the complete sequence of **immutable events** as the source of truth (OrderCreated, ItemAdded, OrderPaid). Current state is derived by replaying events. **Benefits**: Full audit trail, temporal queries ("state at time T"), easy debugging. **Challenges**: Event schema evolution, read performance (need projections/snapshots), eventual consistency.

**CQRS (Command Query Responsibility Segregation)**: Separate the write model (handles commands, emits events) from the read model (denormalized views optimized for queries). The write side ensures business invariants; the read side is eventually consistent but fast. **Often paired with event sourcing** but they are independent patterns.

**Saga Pattern**: Manages distributed transactions across services without 2PC. Two flavors:
- **Choreography**: Each service listens for events and reacts. Service A emits OrderCreated, Service B listens and reserves inventory, emits InventoryReserved, Service C listens and charges payment. Compensating events on failure (InventoryReleased). Simple but hard to track.
- **Orchestration**: A saga orchestrator explicitly calls each step and handles compensation. Easier to understand and debug. More coupling to the orchestrator.

**Outbox Pattern**: Solves dual-write problem (write to DB + publish event). Write business data AND the event to the same database in one ACID transaction (to an "outbox" table). A separate process (CDC with Debezium, or polling) reads the outbox and publishes to the message broker. Guarantees **at-least-once** event delivery without distributed transactions.

### Q20: How do you guarantee exactly-once processing in an event-driven system?

True exactly-once delivery is impossible in distributed systems. The practical approach is **at-least-once delivery + idempotent consumers**.

**Implementation**:
1. **Producer**: Use the outbox pattern for reliable publishing. Include a unique `eventId` in every event.
2. **Consumer**: Before processing, check if `eventId` exists in a **deduplication table** (or processed_events table). If yes, skip. If no, process and insert `eventId` in the same transaction as the business operation.
3. **Idempotency by design**: Operations that are naturally idempotent (SET balance = 100) don't need deduplication. Operations that aren't (INCREMENT balance by 10) need the dedup check.
4. **Message broker guarantees**: Kafka provides exactly-once semantics within a single cluster using idempotent producers + transactional consumers. But cross-system, you still need application-level idempotency.

**Ordering guarantees**: Use partition keys (e.g., orderId) to ensure events for the same entity are processed in order within a partition. Cross-partition ordering requires timestamps or sequence numbers.

---

## 12 -- Data Serialization Formats

### Q21: Compare Protobuf vs Avro vs MessagePack -- when do you use each?

| Dimension | Protocol Buffers | Apache Avro | MessagePack |
|-----------|-----------------|-------------|-------------|
| **Schema** | Required (.proto files) | Required (JSON schema) | Schema-less |
| **Encoding** | Binary, field tags | Binary, schema must be available to reader | Binary (like compact JSON) |
| **Schema evolution** | Good (field numbers, add/remove optional fields) | Excellent (reader/writer schema resolution) | N/A (no schema) |
| **Code generation** | Required (protoc compiler) | Optional (can use generic reader) | Not needed |
| **Performance** | Fastest serialization/deserialization | Slower than Protobuf (schema resolution overhead) | Fast (no schema overhead) |
| **Message size** | Smallest (field tags + varints) | Small (no field names in binary) | Small (compact binary JSON) |
| **Self-describing** | No (need .proto to decode) | Yes (schema can be embedded) | Yes (like JSON but binary) |
| **Language support** | Excellent (C++, Java, Go, C#, Python, etc.) | Good (Java-centric, other langs via libraries) | Excellent (40+ languages) |
| **Ecosystem** | gRPC, Google Cloud, Buf | Kafka (Confluent Schema Registry), Hadoop, Spark | Redis, caching layers, any ad-hoc binary needs |

### Q22: When do you choose which serialization format?

**Use Protobuf when**: Building gRPC services (it's the default). Need maximum performance in service-to-service communication. Strong typing and backward/forward compatibility matter. You control both producer and consumer.

**Use Avro when**: Working with Kafka and stream processing (Confluent Schema Registry manages schema evolution). Big data pipelines (Spark, Flink, Hadoop -- Avro is a first-class citizen). Schema evolution is frequent and must be managed centrally. Need the schema embedded with the data (self-describing files).

**Use MessagePack when**: Need binary efficiency without schema management overhead. Caching serialized objects in Redis (smaller than JSON, faster to parse). Drop-in replacement for JSON where you control both sides. Schemaless flexibility is more important than contract enforcement.

**Use JSON when**: Public APIs (human-readable, universal support). Debugging ease matters more than performance. Interoperability with unknown consumers. Configuration files and small payloads.

**Interview insight**: The trend in 2025 is Protobuf for internal APIs (via gRPC and Buf), Avro for event streaming (Kafka), and JSON for external APIs. MessagePack is niche but valuable for high-throughput caching scenarios. The key is: schema-driven formats (Protobuf, Avro) catch breaking changes at build time; schema-less formats (JSON, MessagePack) push that risk to runtime.
