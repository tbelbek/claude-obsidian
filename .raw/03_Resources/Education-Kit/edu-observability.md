---
tags:
  - education-kit
---

# Observability Stack (Tempo, Loki, OpenTelemetry) — Education Kit

## Key Concepts

### What Observability Is

Observability is the ability to understand the internal state of a system by examining its external outputs — metrics, logs, and traces. Unlike monitoring, which answers predefined questions ("Is CPU above 80%?"), observability lets you ask arbitrary questions about system behavior ("Why was this specific request slow?" "What changed between yesterday and today?"). It is essential for debugging complex distributed systems where failures are unpredictable.

### OpenTelemetry (OTel)
- **What** — Vendor-neutral standard for instrumenting applications. Produces traces, metrics, and logs in a common format (OTLP).
- **Traces** — Each HTTP/gRPC request creates a trace with spans for each operation (database call, external API call, message publish). Traces flow from services through a collection agent to a tracing backend.
- **Metrics** — Request rate, latency histograms, error counters, custom business metrics. Exported via OTLP to a metrics backend.
- **Auto-instrumentation** — OTel SDK automatically instruments common frameworks (ASP.NET Core, HttpClient, gRPC, database drivers). No manual span creation needed for basic operations.
- **Configuration** — Services export telemetry via environment variables (`OTEL_EXPORTER_OTLP_ENDPOINT`) pointing to a collection agent.

### Grafana Tempo (Distributed Tracing)
- **What** — Distributed tracing backend by Grafana. Stores and queries traces. Like Jaeger but designed for massive scale with object storage (S3, Azure Blob).
- **How it fits** — Services emit traces via OTel, a collection agent receives them, Tempo stores them, Grafana visualizes them.
- **Use case** — "This request took 3 seconds — why?" Open the trace, see each span: 50ms in the service, 2.8s waiting for a downstream call, 150ms in the database. Now you know where to optimize.
- **TraceID correlation** — Each request gets a trace ID that flows through all services. Logs include the trace ID so you can jump from a log line to the full trace.
- **vs Jaeger** — Both store distributed traces. Jaeger uses Elasticsearch or Cassandra for storage — good but expensive at scale. Tempo uses object storage — much cheaper for high-volume trace data.

### Grafana Loki (Log Aggregation)
- **What** — Log aggregation system by Grafana. Like Elasticsearch but designed to be cheaper and simpler — indexes labels only, not full text.
- **How it works** — A log shipper (Promtail or Alloy) tails container logs, adds labels (namespace, pod, container), and ships to Loki.
- **Querying** — LogQL query language in Grafana. Filter by labels: `{namespace="production", app="my-service"} |= "error"`.
- **Correlation** — Logs include trace IDs from OTel. Click a log line in Grafana and jump to the full trace in Tempo.
- **Cost efficiency** — Because Loki indexes only labels (not full text), storage grows much slower than with Elasticsearch. Set retention per label — production logs kept longer, debug logs shorter.

### Grafana Alloy (Collection Agent)
- **What** — Grafana's unified collection agent (successor to Grafana Agent). Scrapes Prometheus metrics, receives OTel traces, collects cloud metrics.
- **Why Alloy instead of raw Prometheus** — Alloy can receive OTel data natively. Prometheus cannot receive traces. Alloy replaces both Prometheus scraper and OTel Collector in one agent.
- **Deployment** — Typically runs as a DaemonSet in Kubernetes (one per node for metrics scraping), with additional instances for cloud metrics and cluster events.

### The Full Data Flow
```
Service (app + OTel SDK)
  → metrics + traces → Collection Agent (e.g., Grafana Alloy)
  → logs → Log Shipper (Promtail/Alloy) → Log Processor → Loki

Collection Agent
  → traces → Tempo
  → metrics → Metrics Backend (Mimir / Grafana Cloud)

K8s cluster
  → kube-state-metrics → Collection Agent → Metrics Backend

Cloud provider
  → Cloud metrics agent → Metrics Backend
```

### What to Monitor with This Stack
- **Service health** — Request rate, error rate, latency (p50/p95/p99) per service via OTel metrics.
- **Distributed traces** — Full request path across services. Identify slow spans, failed calls, cascading timeouts.
- **Logs** — Structured logs with trace correlation. Jump from error log to full trace.
- **K8s resources** — Pod CPU/memory via kube-state-metrics. Node health. HPA scaling events.

### Observability vs Monitoring
- **Monitoring** — Predefined dashboards and alerts for known failure modes. "Is the CPU above 80%?" "Is the error rate above 5%?" You define what to watch in advance. Good for known-unknowns.
- **Observability** — Ability to ask arbitrary questions about system behavior using telemetry data (traces, logs, metrics). "Why was this specific request slow?" "What changed between yesterday and today?" Lets you debug unknown-unknowns — problems you did not predict.
- **Three pillars** — Metrics (what is happening — rates, counts, durations), Logs (why it happened — structured event records), Traces (where it happened — request path across services). Correlated together: trace ID in logs links to the distributed trace, metrics show the aggregate picture.
- **Best approach** — Have both: monitoring dashboards for known patterns (RED/USE methods), plus full observability via OpenTelemetry traces and structured logs for debugging novel issues. Monitoring catches known problems automatically; observability lets you investigate new ones.

## Sorulursa

> [!faq]- "Why Grafana stack instead of Datadog or New Relic?"
> Cost and control. Grafana stack is open-source at the core — Tempo, Loki, Mimir are all free to self-host. You can use Grafana Cloud for a managed experience but could move to self-hosted if needed. Commercial APM tools charge per host per month — with many services and multiple environments, that adds up fast. Grafana stack also integrates better with Kubernetes and OTel natively.

> [!faq]- "How do you correlate logs, traces, and metrics?"
> OTel trace IDs. Every request gets a trace ID that flows through all services. Logs include the trace ID as a structured field. In Grafana, you can click a metric spike, see the traces that contributed to it, click a trace span, and see the logs from that service at that time. All three signals connected by the same trace ID.

> [!faq]- "What's the difference between Tempo and Jaeger?"
> Both store distributed traces. Jaeger uses Elasticsearch or Cassandra for storage — good but expensive at scale. Tempo uses object storage (S3, Azure Blob) — much cheaper for high-volume trace data. Tempo is also designed to work natively with Grafana, so the querying experience is better integrated.

> [!faq]- "How do you handle log volume at scale?"
> Loki indexes labels only, not full text — so storage grows much slower than Elasticsearch. Log shippers add labels (namespace, pod, service) and log processors transform/enrich logs before they reach Loki. Set retention per label — production logs kept longer, debug logs shorter. For high-volume services, sample — keep all error logs, sample a percentage of info logs.
