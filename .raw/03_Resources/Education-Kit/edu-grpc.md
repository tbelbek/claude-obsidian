---
tags:
  - education-kit
---
# gRPC — Knowledge Base
> [!info] High-performance RPC framework using Protocol Buffers for binary serialization and HTTP/2 for transport — covering proto files, versioning, streaming, error handling, and comparisons with REST and GraphQL.

---

## Key Concepts

### What gRPC Is
gRPC is a high-performance RPC framework by Google that uses Protocol Buffers for binary serialization and HTTP/2 for transport. Services define their API in .proto files, and the tooling generates typed client/server code in any language. Best for: service-to-service communication in microservices where performance matters — smaller payloads than JSON, compile-time type safety, and built-in streaming support.

### Protocol Buffers
- **Proto files** — Schema definition language. Defines services, methods, and message types.
- **Code generation** — Compiler generates typed client/server stubs from proto files. Available for C#, Java, Python, Go, etc.
- **Binary format** — Much smaller than JSON. Faster serialization/deserialization. Not human-readable.

### Versioning
- **Versioned protos** — v1, v2, v3 directories per service. Old versions kept for backward compatibility.
- **Breaking changes** — Adding fields is safe. Removing/renaming fields breaks clients. CI detects this.
- **Client SDKs** — Each service can publish a package with generated client code. Consumers reference the package, not the proto files directly.

### When to Use
- **Service-to-service** — Fast, typed, binary. No JSON overhead.
- **Streaming** — gRPC supports server streaming, client streaming, and bidirectional streaming.
- **NOT for browsers** — Browsers can't make gRPC calls directly. Use GraphQL or REST for frontend. gRPC-Web exists but adds complexity.

### vs REST vs GraphQL
- **gRPC** — Fastest. Typed. Binary. Best for internal service calls.
- **REST** — Simplest. HTTP caching. Best for external APIs.
- **GraphQL** — Most flexible. Client picks data shape. Best for frontends with varying data needs.

### Error Handling
- **Status codes** — gRPC has its own status codes (OK, NOT_FOUND, INTERNAL, DEADLINE_EXCEEDED, etc.). Mapped to HTTP status codes when going through gRPC-Web gateway.
- **Deadlines** — Every gRPC call should have a deadline. If the server doesn't respond in time, the client gets DEADLINE_EXCEEDED. Prevents cascading timeouts.
- **Retry policies** — gRPC supports built-in retry with backoff. Configure per-method: which status codes to retry, max attempts, backoff multiplier.

---

## Sorulursa

> [!faq]- "How do you handle backward compatibility with gRPC?"
> Proto rules: never remove a field, never change a field number, never rename a message type. Adding new fields is always safe — old clients ignore unknown fields. Enforce this with `buf breaking` in CI — it compares the PR's proto files against the base branch and fails if any backward-incompatible change is detected. This catches problems before code review even starts.

> [!faq]- "How do you debug gRPC calls?"
> grpcurl for manual testing (like curl for gRPC). Distributed tracing (OpenTelemetry) to see the full call chain across services. gRPC interceptors for logging request/response metadata. Each gRPC call should have a correlation ID that flows through the entire call chain.

> [!faq]- "gRPC vs REST for external APIs — why not gRPC everywhere?"
> gRPC requires proto definitions and code generation on the client side. External partners (third-party integrations) expect REST — they want to hit an endpoint with curl, not install a protobuf compiler. For internal service-to-service, gRPC is faster and type-safe. For external APIs, REST is simpler and more accessible.
