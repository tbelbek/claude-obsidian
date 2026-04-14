---
tags:
  - education-kit
---

# Web Architecture — Advanced Education Kit

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

**Key insight**: Hybrid stacks are the norm. REST for public/partner APIs (simplicity, cacheability), GraphQL for client-facing BFFs (frontend flexibility, reduce round-trips on mobile), gRPC for internal service-to-service (performance, strong typing, streaming).

### Q2: When would you use a hybrid API stack?

A typical modern architecture uses all three. The API gateway exposes REST for external partners. The BFF exposes GraphQL that aggregates from internal services. Internal services communicate via gRPC. Each layer chosen for its strengths.

---

## 2 -- WebSocket Protocol Deep Dive

### Q3: Explain the WebSocket handshake and frame protocol in detail.

**Handshake**: Client sends HTTP/1.1 GET with `Upgrade: websocket`, `Connection: Upgrade`, `Sec-WebSocket-Key`. Server responds with HTTP 101 Switching Protocols. After this, the connection upgrades to persistent, full-duplex TCP.

**Frame protocol**: Data is sent in frames with opcode (text, binary, close, ping, pong), payload length, masking key, and payload. Ping/pong serves as heartbeat.

### Q4: How do you scale WebSocket connections across multiple server instances?

Strategies: (1) Sticky sessions. (2) Redis Pub/Sub or message broker for cross-instance messaging. (3) Dedicated WebSocket gateway. (4) Connection state externalization in Redis. (5) Plan for ~50K-100K concurrent connections per server.

**Security**: Validate Origin header, per-connection rate limiting, use `wss://`, authenticate during handshake, set idle timeouts and max message size.

---

## 3 -- OAuth 2.0 / OpenID Connect

### Q5: Walk through OAuth 2.0 Authorization Code flow with PKCE step by step.

1. Client generates `code_verifier` (random string, kept secret).
2. Client computes `code_challenge` = `BASE64URL(SHA256(code_verifier))`.
3. Authorization request with `response_type=code`, `code_challenge`, `code_challenge_method=S256`.
4. User authenticates and consents.
5. Authorization server redirects back with `code` and `state`.
6. Client validates `state` matches.
7. Token exchange with `code` and `code_verifier`.
8. Server verifies hash match, issues tokens.

**Why PKCE matters**: Prevents intercepted authorization codes from being exchanged for tokens without the `code_verifier`.

### Q6: How does OpenID Connect layer on top of OAuth 2.0?

OAuth 2.0 is **authorization** ("what can this client access?"). OIDC adds **authentication** ("who is the user?") with ID Token (JWT with user claims), UserInfo endpoint, standard scopes (`openid`, `profile`, `email`), and discovery document.

**Other flows**: Client Credentials (machine-to-machine), Device Authorization (devices without browser), Refresh Token (rotate on use).

---

## 4 -- Service Mesh

### Q7: What is a service mesh and when do you need one?

A dedicated infrastructure layer with sidecar proxies handling: mTLS everywhere, traffic management (canary, splitting, retries), observability (automatic metrics, tracing), and policy enforcement. Need one when: 10+ microservices with cross-cutting concerns becoming painful. Don't need one when: small number of services where the complexity outweighs benefits.

### Q8: Compare Istio vs Linkerd.

| Dimension | Istio | Linkerd |
|-----------|-------|---------|
| Proxy | Envoy (C++, feature-rich) | linkerd2-proxy (Rust, purpose-built) |
| Philosophy | Enterprise-first, comprehensive | Simplicity-first, minimal overhead |
| Resource usage | Higher (~50-100MB RAM) | Lower (~10-20MB RAM) |
| Configuration | Thousands of options | Deliberately limited, sensible defaults |
| mTLS | Manual or auto, configurable | On by default, zero-config |

---

## 5 -- API Rate Limiting Algorithms

### Q9: Compare the major rate limiting algorithms.

| Algorithm | Burst handling | Memory | Accuracy | Complexity |
|-----------|---------------|--------|----------|------------|
| Token Bucket | Allows bursts | O(1) | Good | Low |
| Leaky Bucket | Smooths bursts | O(1) | Good | Low |
| Fixed Window | Edge bursts | O(1) | Poor at edges | Lowest |
| Sliding Window Log | No bursts | O(n) | Exact | Medium |
| Sliding Window Counter | Controlled | O(1) | Very good | Medium |

**Sliding Window Counter** is the best general-purpose choice.

### Q10: How do you implement distributed rate limiting?

Solutions: (1) Centralized Redis with Lua scripts for atomic operations. (2) Sliding window with Redis sorted sets. (3) Local counters + periodic sync. (4) API Gateway level (Kong, Envoy).

Return headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`. Return 429 with `Retry-After`.

---

## 6 -- Database Connection Pooling

### Q11: How does connection pooling work internally?

Key parameters: min/max pool size, idle timeout, max lifetime, connection validation, leak detection. Sizing: `pool_size = (core_count * 2) + effective_spindle_count`. More connections != more throughput.

### Q12: How do you diagnose and fix connection pool exhaustion?

Root causes: connection leaks (missing `using`), slow queries holding connections, large transaction scope, pool too small, external dependency blocking. Monitor: pool active/idle/waiting counts, connection wait time.

---

## 7 -- CDN Cache Invalidation

### Q13: Main strategies and trade-offs.

1. **TTL-based**: Simple, predictable. Trade-off: stale data during TTL window.
2. **Purge/Ban API**: Invalidate specific URLs or patterns. Propagation takes seconds-minutes.
3. **Surrogate keys**: Tag objects, invalidate by tag. Best for complex invalidation.
4. **Stale-while-revalidate**: Serve stale, fetch fresh in background.
5. **Versioned URLs**: Hash in filename. Best for static assets.
6. **Origin-managed**: `Cache-Control: no-cache` with ETag for revalidation.

For APIs: short TTL + stale-while-revalidate. For static assets: versioned URLs. For business events: surrogate key purging.

---

## 8 -- HTTP/3 and QUIC

### Q14: How does HTTP/3 with QUIC work?

QUIC solves HTTP/2's head-of-line blocking over TCP. Built on UDP with independent streams, integrated TLS 1.3, 0-RTT for returning clients, and connection migration (survives Wi-Fi to cellular switch). ~30% of web traffic uses QUIC as of 2025.

---

## 9 -- Zero-Trust Networking

### Q15: Principles and why the perimeter model failed.

1. Never trust, always verify.
2. Least privilege.
3. Assume breach.
4. Micro-segmentation.
5. Continuous verification.

### Q16: Implementation for microservices.

mTLS everywhere, SPIFFE/SPIRE for workload identities, OPA for policy enforcement, no implicit trust from network location, short-lived credentials, encrypted at rest and in transit, centralized logging.

---

## 10 -- Observability (OpenTelemetry)

### Q17: Distributed tracing end-to-end.

OTel creates traces with spans. Context propagated via W3C `traceparent` headers. Spans exported to collector, then to backend (Jaeger, Tempo). Sampling: head-based, tail-based, or adaptive.

### Q18: Relationship between metrics, logs, and traces.

Metrics for alerting and dashboards (cheap). Logs for discrete events (expensive at scale). Traces for request journeys (invaluable for debugging). **Correlation is the key**: metric alert -> exemplar traces -> correlated logs. SLO-driven alerting on burn rate.

---

## 11 -- Event-Driven Architecture Patterns

### Q19: Event sourcing, CQRS, saga, outbox.

**Event Sourcing**: Store immutable events as source of truth. Replay to derive state.
**CQRS**: Separate write model from read model.
**Saga**: Choreography (decentralized events) or Orchestration (central coordinator) for distributed transactions.
**Outbox Pattern**: Write business data + event in same transaction. Separate process publishes from outbox to broker.

### Q20: Exactly-once processing.

True exactly-once is impossible. Use at-least-once delivery + idempotent consumers. Include unique `eventId`, check deduplication table before processing. Kafka provides exactly-once within a single cluster.

---

## 12 -- Data Serialization Formats

### Q21: Protobuf vs Avro vs MessagePack.

| Dimension | Protobuf | Avro | MessagePack |
|-----------|---------|------|-------------|
| Schema | Required (.proto) | Required (JSON) | Schema-less |
| Performance | Fastest | Slower (schema resolution) | Fast |
| Schema evolution | Good | Excellent | N/A |
| Best for | gRPC, internal APIs | Kafka, big data | Redis, caching |

### Q22: When to choose which.

Protobuf: gRPC services, maximum performance. Avro: Kafka and stream processing. MessagePack: caching without schema overhead. JSON: public APIs, human-readability.
