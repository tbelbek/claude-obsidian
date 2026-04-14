---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Web Architecture & Infrastructure — Quick Reference

> [!tip] How web systems are built at scale. CDN, load balancing, reverse proxy, edge computing, DNS routing, caching layers, API gateways.

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#CDN (Content Delivery Network)\|CDN]] | edge cache, reduce latency, DDoS protection | [[#Load Balancing\|load balancing]] | round-robin, least-conn, L4 vs L7 |
| [[#Reverse Proxy\|reverse proxy]] | SSL termination, caching, request routing | [[#API Gateway Pattern\|API gateway]] | federated GraphQL gateway at Combination |
| [[#Caching Layers\|caching layers]] | browser→CDN→reverse proxy→app→DB cache | [[#DNS & Routing\|DNS routing]] | GeoDNS, failover, weighted routing |
| [[#Edge Computing\|edge computing]] | CloudFlare Workers, serverless at edge, sub-ms | | |

---

### What Web Architecture Is

Web architecture is how you structure the layers between a user's browser and your backend services — CDN for static assets, load balancers for traffic distribution, reverse proxies for SSL/caching, API gateways for routing, and caching layers at every level. Understanding these layers is essential for designing systems that are fast, reliable, and scalable. Most performance and availability improvements come from the infrastructure layer, not the application code.

## CDN (Content Delivery Network)

**Q: What is a CDN and why use it?**
A: A network of edge servers distributed globally that cache and serve content close to users. Benefits: reduced latency (serve from nearest PoP), offload origin server (less traffic hits your backend), DDoS protection, improved availability. Without CDN, every request travels to your origin server regardless of user location.

**Q: How does CDN caching work?**
A: CDN respects HTTP cache headers (`Cache-Control`, `Expires`, `ETag`, `Last-Modified`). Origin sets TTL via `Cache-Control: max-age=3600`. CDN stores the response at edge. Subsequent requests for the same resource are served from edge cache until TTL expires. On expiry, CDN revalidates with origin (conditional GET with `If-None-Match` / `If-Modified-Since`). You can also force purge/invalidation from CDN dashboard or API.

**Q: CDN for static assets vs APIs — what's different?**
A: Static assets (JS, CSS, images, fonts): aggressive caching with long TTL, versioned filenames (`app.abc123.js`) for instant invalidation. APIs: usually pass-through (no caching) because responses are dynamic and user-specific. Exception: public read-heavy API responses can be cached at edge with short TTL. Edge compute (CloudFlare Workers) can add logic at CDN layer for APIs.

**Q: What are CloudFlare Workers and how is edge computing used?**
A: CloudFlare Workers run JavaScript/WASM at CDN edge locations worldwide. Code executes in the PoP closest to the user, not in your origin data center. Use cases: request routing, A/B testing, auth validation, response transformation. At Combination: we use CloudFlare Workers for GraphQL routing in E2E tests — requests are intercepted and routed at the edge before reaching the gateway.

**Q: What are CDN cache invalidation strategies?**
A: (1) Purge by URL — invalidate a specific cached resource. (2) Purge by cache tag — tag responses with logical groups, purge all resources with that tag. (3) Versioned URLs — change the filename/query param (`v=2`), so the old cached version is never requested again. (4) Short TTL + stale-while-revalidate — serve stale content while fetching fresh in background. Versioned URLs are the most reliable because you never need to purge.

---

## Load Balancing

**Q: What is the difference between Layer 4 and Layer 7 load balancing?**
A: Layer 4 (Transport/TCP): routes based on IP and port. Fast, no content inspection. Cannot make routing decisions based on HTTP headers, URL path, cookies. Layer 7 (Application/HTTP): inspects HTTP content. Can route based on URL path (`/api` to backend A, `/static` to backend B), headers, cookies. More flexible but slightly more overhead. Most modern load balancers operate at L7.

**Q: What are the common load balancing algorithms?**
A: **Round-robin** — distribute requests sequentially across servers. Simple, works when servers are equal. **Least connections** — send to server with fewest active connections. Better when request processing times vary. **IP hash** — hash client IP to pick server. Same client always hits same server (poor man's sticky sessions). **Weighted** — assign weight to each server. Heavier servers get more traffic. Useful during rolling deploys or mixed hardware.

**Q: How do health checks and failover work?**
A: LB periodically sends health check requests to backends (HTTP GET to `/health`). If a backend fails N consecutive checks, LB marks it unhealthy and stops routing traffic to it. When backend recovers and passes checks again, LB adds it back. Two types: **active** (LB probes backends) and **passive** (LB observes real traffic for errors/timeouts). Failover = automatic rerouting to healthy backends when one fails.

**Q: When are sticky sessions needed, and when are they harmful?**
A: Needed: when server holds session state in memory (legacy apps), WebSocket connections (must stay on same server), file upload with chunked transfer. Harmful: prevents even load distribution, makes scaling harder (can't just add servers), makes failover worse (if sticky server dies, user loses session). Better solution: externalize session state to Redis/DB so any server can handle any request.

**Q: How does load balancing work in Kubernetes?**
A: **Service** (L4) — ClusterIP provides internal load balancing via kube-proxy/iptables. Round-robin across pods. **Ingress** (L7) — Ingress controller (Nginx, Traefik, Contour) handles HTTP routing, SSL termination, path-based routing. **External LB** — cloud provider's load balancer (ALB, NLB) for traffic from outside the cluster. At Combination: we use Contour (Envoy-based) as our Ingress controller.

---

## Reverse Proxy

**Q: What does a reverse proxy do?**
A: Sits between clients and backend servers. Responsibilities: **SSL termination** (decrypt HTTPS, forward HTTP internally), **compression** (gzip/brotli responses), **caching** (cache responses to reduce backend load), **routing** (direct requests to different backends based on path/host), **rate limiting** (protect backends from abuse), **security** (hide backend topology, add security headers). Clients only see the proxy, never the backends directly.

**Q: Nginx vs Traefik vs Envoy — when to use which?**
A: **Nginx** — battle-tested, great for static serving, simple reverse proxy. Config-file based, reload for changes. Good for: traditional deployments, static sites. **Traefik** — built for containers/K8s, auto-discovers services, automatic Let's Encrypt. Good for: Docker/K8s environments needing auto-config. **Envoy** — L7 proxy designed for service mesh, advanced observability, gRPC-native. Good for: service mesh (Istio/Linkerd sidecar), complex routing, high-performance microservices.

**Q: How does an API Gateway act as a reverse proxy?**
A: API Gateway is a specialized reverse proxy for APIs. Beyond basic proxying, it handles: auth (JWT validation, API keys), rate limiting per client, request/response transformation, protocol translation (REST to gRPC), aggregation (combine multiple backend calls). At Combination: our GraphQL gateway is effectively an API gateway — it receives all client GraphQL queries and routes them to 60+ backend services.

**Q: What is Contour and how is it used at Combination?**
A: Contour is an Envoy-based Ingress controller for Kubernetes. It translates K8s Ingress/HTTPProxy resources into Envoy configuration. Benefits over Nginx Ingress: better performance, dynamic config updates without reload, advanced traffic management (weighted routing, rate limiting, retries). At Combination: Contour handles all inbound HTTP traffic to our K8s clusters, managing SSL termination and routing to services.

---

## Caching Layers

**Q: What are the layers of caching in a web architecture?**
A: From closest to user to closest to data: (1) **Browser cache** — HTTP cache headers, Service Worker cache. (2) **CDN cache** — edge servers cache static assets and cacheable responses. (3) **API gateway/reverse proxy cache** — cache frequent API responses. (4) **Application cache** — Redis/Memcached for computed data, session data, frequently accessed objects. (5) **Database cache** — query cache, buffer pool, materialized views. Each layer reduces load on the layer behind it.

**Q: What are write-through, write-behind, and cache-aside patterns?**
A: **Cache-aside (lazy loading)** — app checks cache first. On miss, reads from DB, writes to cache, returns. Most common pattern. **Write-through** — app writes to cache, cache synchronously writes to DB. Ensures cache is always current but adds write latency. **Write-behind (write-back)** — app writes to cache, cache asynchronously writes to DB later. Fast writes but risk of data loss if cache crashes before persisting. At Combination: we primarily use cache-aside with Redis.

**Q: How do you handle cache invalidation?**
A: (1) **TTL-based** — set expiry time, accept staleness within TTL window. Simple but imprecise. (2) **Event-based** — when data changes, publish event that triggers cache invalidation. Precise but requires event infrastructure. (3) **Versioned keys** — include version/hash in cache key (`user:123:v5`), increment on change. Old entries expire naturally. Best practice: combine short TTL with event-based invalidation for critical data.

**Q: What is cache stampede and how do you prevent it?**
A: When a popular cache entry expires, many concurrent requests all miss cache simultaneously and hit the database. Prevention: (1) **Locking** — first request acquires lock and refreshes cache, others wait. (2) **Background refresh** — refresh cache before expiry using a background job. (3) **Stale-while-revalidate** — serve stale data immediately, refresh in background. (4) **Jittered TTL** — add random offset to TTL so entries don't all expire at once.

---

## DNS & Routing

**Q: How does DNS resolution work end to end?**
A: (1) Browser checks its DNS cache. (2) OS checks its DNS cache. (3) Query goes to configured resolver (ISP or public like 8.8.8.8). (4) Resolver checks its cache. On miss: (5) Resolver asks root name servers ("who handles .com?"). (6) Root responds with TLD server. (7) Resolver asks TLD server ("who handles example.com?"). (8) TLD responds with authoritative name server. (9) Resolver asks authoritative server for the IP. (10) Response flows back, each layer caches per TTL.

**Q: What is DNS-based load balancing?**
A: DNS server returns different IPs for the same domain. **GeoDNS** — return IP of nearest data center based on client's geographic location. **Weighted DNS** — distribute traffic by returning different IPs with configured weights. **Round-robin DNS** — rotate through a list of IPs. Limitations: DNS caching means changes are slow to propagate, no health checking (can return IPs of dead servers), clients may cache and ignore TTL.

**Q: Why aren't DNS changes instant?**
A: DNS responses are cached at every level (browser, OS, resolver) with a TTL. Even if you update the authoritative record, cached entries persist until their TTL expires. Common TTLs range from 60 seconds to 24 hours. Best practice: lower TTL before planned changes, wait for old TTL to expire, make the change, then raise TTL back. Some clients (Java, some browsers) ignore TTL and cache longer.

**Q: How is DNS managed at Combination?**
A: CloudFlare DNS managed via CDeploy (our internal deployment tool). Infrastructure-as-code approach: DNS records are defined in configuration, CDeploy applies changes to CloudFlare. This gives us version control, audit trail, and automated DNS management as part of deployments. CloudFlare also provides DDoS protection and CDN at the DNS layer.

---

## API Gateway Pattern

**Q: What does an API Gateway do?**
A: Single entry point for all client requests. Responsibilities: **Routing** — direct requests to appropriate microservices. **Authentication/Authorization** — validate JWT tokens, API keys before requests reach services. **Rate limiting** — protect services from abuse. **Request transformation** — modify headers, body, query params. **Protocol translation** — REST to gRPC, HTTP to WebSocket. **Aggregation** — combine responses from multiple services into one. **Observability** — centralized logging, metrics, tracing.

**Q: How does the GraphQL gateway work as an API gateway at Combination?**
A: Our GraphQL gateway (Apollo Federation) acts as the API gateway for all client-facing traffic. 60+ microservices expose their own GraphQL subgraphs. The gateway composes them into a single unified schema. Clients send one query, gateway resolves it across multiple services. This gives us: single endpoint for clients, type-safe API contract, automatic query planning, centralized auth and rate limiting. It is the north-south traffic entry point.

**Q: What is the difference between an API Gateway and a Service Mesh?**
A: **API Gateway** — handles **north-south** traffic (external clients to internal services). One centralized component. Focuses on: auth, rate limiting, protocol translation, client-facing concerns. **Service Mesh** — handles **east-west** traffic (service-to-service communication). Sidecar proxy on every service. Focuses on: mTLS, retries, circuit breaking, observability between services. They complement each other. At Combination: GraphQL gateway for north-south, service mesh patterns via Polly/direct for east-west.

**Q: What is the BFF (Backend for Frontend) pattern?**
A: Create separate API surfaces optimized for each client type. A mobile BFF returns minimal data (bandwidth-conscious), a web BFF returns richer payloads, a third-party BFF returns stable/versioned APIs. Each BFF aggregates and transforms backend service responses for its specific client. Prevents a single API from becoming a "one size fits none" compromise. GraphQL partially solves this — clients request exactly what they need — reducing the need for separate BFFs.

---

## Edge Computing

**Q: What is edge computing in the context of web architecture?**
A: Running application code at CDN edge locations, physically close to users (100+ locations worldwide instead of 1-3 data centers). Code executes in the PoP nearest to the requesting user. Sub-millisecond cold starts (V8 isolates, not containers). Benefits: ultra-low latency, reduced origin load, ability to personalize/transform responses at the edge.

**Q: What are the major edge computing platforms?**
A: **CloudFlare Workers** — V8 isolates, 200+ locations, Workers KV for storage, Durable Objects for state. **AWS Lambda@Edge** — runs at CloudFront edge, triggered by CDN events (viewer request, origin request). **Vercel Edge Functions** — built on CloudFlare Workers, integrated with Next.js. **Deno Deploy** — globally distributed V8 isolates. **Fastly Compute@Edge** — WASM-based, very fast cold starts.

**Q: What are practical use cases for edge computing?**
A: **A/B testing** — route users to variants at edge without hitting origin. **Geo-routing** — redirect users to region-specific content/services. **Auth validation** — validate JWT at edge, reject unauthorized requests before they reach origin. **Response transformation** — modify HTML/JSON at edge (inject headers, rewrite URLs, personalize content). **Bot detection** — filter bot traffic at edge. **API rate limiting** — enforce rate limits at edge to protect origin.

**Q: How does Combination use CloudFlare Workers?**
A: At Combination, CloudFlare Workers are used for GraphQL routing in E2E tests. The Workers intercept requests at the edge and route them appropriately before they reach the GraphQL gateway. This enables testing routing logic in a production-like environment without modifying the gateway itself. Edge computing provides the flexibility to add routing rules, transformations, and test instrumentation without deploying changes to the core infrastructure.

---

## Sorulursa (Interview Q&A)

> [!question] "How do you design a system for global users?"
> Start with DNS-based routing (GeoDNS via CloudFlare) to direct users to nearest region. CDN for static assets with aggressive caching. Edge computing for personalization and auth validation at the edge. Multi-region deployment for low-latency API access. Database replication with read replicas in each region. Eventual consistency between regions is usually acceptable for most data. For critical operations: route to primary region and accept slightly higher latency. Monitor latency percentiles per region, not just averages.

> [!question] "CDN vs application cache (Redis) — when do you use which?"
> CDN caches HTTP responses at the edge for public, cacheable content — same response for many users. Best for: static assets, public API responses, HTML pages. Application cache (Redis) caches computed data inside your infrastructure — for data that varies per user, requires auth, or needs complex invalidation. Best for: session data, user-specific query results, expensive computations, rate limiting counters. Use both: CDN reduces traffic to your servers, Redis reduces load on your database.

> [!question] "How does your GraphQL gateway work as an API gateway?"
> Apollo Federation gateway composes 60+ service subgraphs into a unified schema. Clients send a single GraphQL query to one endpoint. Gateway creates a query plan, resolves data from relevant services in parallel where possible, and returns the combined response. It handles auth (JWT validation), rate limiting, and query complexity analysis. Benefits: strong typing across services, no over-fetching (clients request exactly what they need), single network round-trip for complex queries that span multiple services.

> [!question] "How do you handle cache invalidation at scale?"
> Multi-layer approach: (1) Versioned URLs for static assets (never need to invalidate). (2) Short TTL (30-60s) for API responses cached at CDN — accept brief staleness. (3) Event-based invalidation for application cache — when data changes, publish event that clears relevant Redis keys. (4) Cache-aside pattern so stale cache entries are naturally refreshed on next read. (5) For critical data: skip cache or use very short TTL. The hardest part is knowing what to invalidate — we use cache tags and entity-based keys (`user:123:profile`) to make invalidation targeted.

> [!question] "Explain the request path from user to database in your architecture"
> (1) User's browser resolves DNS via CloudFlare. (2) Request hits CloudFlare CDN — if cached, returns immediately. (3) If not cached, request goes to CloudFlare Workers (edge compute for routing/auth). (4) Request reaches K8s cluster, hits Contour (Envoy-based Ingress controller) for SSL termination and L7 routing. (5) Routed to GraphQL gateway pod. (6) Gateway validates auth, creates query plan, calls relevant microservices via internal K8s Service (L4 load balancing). (7) Microservice checks Redis cache. On miss, queries MongoDB. (8) Response flows back: service to gateway (aggregated), gateway to CDN (cached if appropriate), CDN to user.
