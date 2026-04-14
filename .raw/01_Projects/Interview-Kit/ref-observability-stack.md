---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Observability Stack (Tempo, Loki, OpenTelemetry) — Quick Reference

> [!info] How I've used it: At Combination, full Grafana observability stack — Grafana Alloy for metrics/traces ingestion, Promtail for log collection to Loki, OpenTelemetry SDK in every service, custom Lumberjack for log processing. At KocSistem, built [[ref-grafana-prometheus|Prometheus + Grafana]] from scratch.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#OpenTelemetry (OTel)\|OpenTelemetry]] | SDK in every service, auto-instrumentation, W3C trace context | [[#Grafana Tempo (Distributed Tracing)\|Tempo]] | distributed tracing, trace-to-log correlation |
| [[#Grafana Loki (Log Aggregation)\|Loki]] | log aggregation, labels not full-text, cost efficient | [[#Grafana Alloy (Collection Agent)\|Alloy]] | metrics/traces collection agent, replaces Promtail |
| [[#The Full Data Flow\|data flow]] | service→OTel→Alloy→Tempo/Loki→Grafana | [[#What I Monitor with This Stack\|what I monitor]] | latency, errors, saturation, business events |
| [[#Observability vs Monitoring\|observability vs monitoring]] | monitoring=known failures, observability=arbitrary questions | | |

## HOW WE USE IT

Every service at Combination is instrumented with **OpenTelemetry** via the shared `GP.ServiceBase` framework. The `OpenTelemetryConfiguration` class configures OTLP exporters for metrics and traces — services export to **Grafana Alloy** which runs as a DaemonSet on every K8s node.

The monitoring infrastructure lives in `GP-IaC-Monitoring-AKS` with Helm charts for each component:

| Component | Product | Purpose |
|-----------|---------|---------|
| `cmb-alloy` | Grafana Alloy | Metrics scraping + traces collection |
| `cmb-alloy-azure` | Grafana Alloy | Azure metrics + logs collection |
| `cmb-alloy-single` | Grafana Alloy | Kubernetes events collection |
| `cmb-promtail` | Promtail | Log collection → Loki |
| `cmb-lumberjack` | Custom (in-house) | Log processing and transformation |
| `kube-state-metrics` | kube-state-metrics | K8s object metrics (pod status, deployments) |
| `kubelet-stats-metrics` | kubelet-stats-metrics | Pod disk usage as Prometheus metrics |

---

## Key Concepts

### OpenTelemetry (OTel)
- **What** — Vendor-neutral standard for instrumenting applications. Produces traces, metrics, and logs in a common format (OTLP).
- **How we use it** — Every .NET service includes the `GP.ServiceBase` framework which auto-configures OTel with OTLP exporter. Services export to Grafana Alloy via environment variables (`OTEL_EXPORTER_OTLP_ENDPOINT`).
- **Traces** — Each HTTP/gRPC request creates a trace with spans for each operation (database call, external API call, message publish). Traces flow: service → Alloy → Tempo.
- **Metrics** — Request rate, latency histograms, error counters, custom business metrics. Metrics flow: service → Alloy → Grafana Cloud.
- **Auto-instrumentation** — OTel SDK automatically instruments ASP.NET Core, HttpClient, gRPC, MongoDB driver. No manual span creation needed for basic operations.

### Grafana Tempo (Distributed Tracing)
- **What** — Distributed tracing backend by Grafana. Stores and queries traces. Like Jaeger but designed for massive scale with object storage.
- **How it fits** — Services emit traces via OTel → Alloy collects them → Tempo stores them → Grafana visualizes them.
- **Use case** — "This request took 3 seconds — why?" Open the trace in Grafana, see each span: 50ms in the service, 2.8s waiting for a downstream gRPC call, 150ms in MongoDB. Now you know where to optimize.
- **TraceID correlation** — Each request gets a trace ID that flows through all services. Logs include the trace ID so you can jump from a log line to the full trace.

### Grafana Loki (Log Aggregation)
- **What** — Log aggregation system by Grafana. Like Elasticsearch but designed to be cheaper and simpler — indexes labels only, not full text.
- **How we use it** — Promtail runs as a DaemonSet, tails container logs from `/var/log/pods/`, adds labels (namespace, pod, container), and ships to Loki.
- **Lumberjack** — Our custom in-house log processor that transforms and enriches logs before they reach Loki. Handles structured log parsing, field extraction, and log routing.
- **Querying** — LogQL query language in Grafana. Filter by labels: `{namespace="production", app="feed-service"} |= "error"`.
- **Correlation** — Logs include trace IDs from OTel. Click a log line in Grafana → jump to the full trace in Tempo.

### Grafana Alloy (Collection Agent)
- **What** — Grafana's unified collection agent (successor to Grafana Agent). Scrapes Prometheus metrics, receives OTel traces, collects Azure metrics.
- **How we use it** — Multiple Alloy instances per cluster: one for metrics scraping (DaemonSet), one for Azure metrics, one for K8s events. Configured via Helm charts in `GP-IaC-Monitoring-AKS`.
- **Why Alloy instead of raw Prometheus** — Alloy can receive OTel data natively. Prometheus can't receive traces. Alloy replaces both Prometheus scraper and OTel Collector in one agent.

### The Full Data Flow
```
Service (.NET + OTel SDK)
  → metrics + traces → Grafana Alloy (DaemonSet)
  → logs → Promtail → Lumberjack → Loki

Grafana Alloy
  → traces → Tempo
  → metrics → Grafana Cloud (Mimir)

K8s cluster
  → kube-state-metrics → Alloy → Grafana Cloud
  → kubelet-stats → Alloy → Grafana Cloud

Azure
  → Alloy-Azure → Grafana Cloud
```

### What I Monitor with This Stack
- **Service health** — Request rate, error rate, latency (p50/p95/p99) per service via OTel metrics.
- **Distributed traces** — Full request path across 60+ services. Identify slow spans, failed calls, cascading timeouts.
- **Logs** — Structured logs with trace correlation. Jump from error log to full trace.
- **K8s resources** — Pod CPU/memory via kube-state-metrics. Node health. HPA scaling events.
- **MongoDB** — Atlas metrics collected via custom `monitoring-atlas` component.

### Observability vs Monitoring
- **Monitoring** — Predefined dashboards and alerts for known failure modes. "Is the CPU above 80%?" "Is the error rate above 5%?" You define what to watch in advance. Good for known-unknowns.
- **Observability** — Ability to ask arbitrary questions about system behavior using telemetry data (traces, logs, metrics). "Why was this specific request slow?" "What changed between yesterday and today?" Lets you debug unknown-unknowns — problems you didn't predict.
- **Three pillars** — Metrics (what is happening — rates, counts, durations), Logs (why it happened — structured event records), Traces (where it happened — request path across services). Correlated together: trace ID in logs links to the distributed trace, metrics show the aggregate picture.
- **Our approach** — At Combination, we have both: monitoring dashboards in Grafana for known patterns (RED/USE methods), plus full observability via OpenTelemetry traces in Tempo and structured logs in Loki for debugging novel issues. *(the monitoring catches known problems automatically; observability lets us investigate new ones)*

## Sorulursa

> [!faq]- "Why Grafana stack instead of Datadog or New Relic?"
> Cost and control. Grafana stack is open-source at the core — Tempo, Loki, Mimir are all free to self-host. We use Grafana Cloud for the managed experience but could move to self-hosted if needed. Datadog charges per host per month — with 60+ services and multiple environments, that adds up fast. Grafana stack also integrates better with Kubernetes and OTel natively.

> [!faq]- "How do you correlate logs, traces, and metrics?"
> OTel trace IDs. Every request gets a trace ID that flows through all services. Logs include the trace ID as a structured field. In Grafana, you can click a metric spike → see the traces that contributed to it → click a trace span → see the logs from that service at that time. All three signals connected by the same trace ID.

> [!faq]- "What's the difference between Tempo and Jaeger?"
> Both store distributed traces. Jaeger uses Elasticsearch or Cassandra for storage — good but expensive at scale. Tempo uses object storage (S3, Azure Blob) — much cheaper for high-volume trace data. Tempo is also designed to work natively with Grafana, so the querying experience is better integrated. For 60+ services generating millions of traces, Tempo's cost model wins.

> [!faq]- "How do you handle log volume at scale?"
> Loki indexes labels only, not full text — so storage grows much slower than Elasticsearch. Promtail adds labels (namespace, pod, service) and Lumberjack transforms/enriches logs before they reach Loki. We set retention per label — production logs kept 30 days, debug logs 7 days. For high-volume services, we sample — keep all error logs, sample 10% of info logs.

---

*[[00-dashboard]]*
