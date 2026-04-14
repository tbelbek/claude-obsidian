---
tags:
  - education-kit
---

# Grafana & Prometheus — Education Kit

## Key Concepts

### Prometheus
- **Pull-based model** — Prometheus scrapes metrics endpoints (`/metrics`) on your services at regular intervals. You don't push metrics, Prometheus pulls them.
- **PromQL** — Query language for Prometheus. Examples: `rate(http_requests_total[5m])` for request rate, `histogram_quantile(0.95, ...)` for p95 latency.
- **Exporters** — Adapters that expose metrics from systems that don't natively support Prometheus format (databases, message brokers, etc.).
- **Alertmanager** — Separate component for routing alerts. Supports Slack, email, PagerDuty.

### Grafana
- **Dashboards** — Visual panels showing metrics over time. Each panel is a PromQL query rendered as a graph, gauge, table, or heatmap.
- **Data sources** — Grafana connects to Prometheus, InfluxDB, Elasticsearch, Loki, etc. Prometheus is the most common primary data source.
- **Alerting** — Grafana can define alert rules on dashboard panels, useful for failure rate thresholds and anomaly detection.
- **Variables** — Dashboard variables for filtering (by service, environment, namespace). One dashboard serves all services.

### What to Monitor

#### RED Method (per service)
- **Rate** — Request rate per second
- **Errors** — Error rate / error percentage
- **Duration** — Request latency (p50, p95, p99)

#### USE Method (per resource)
- **Utilization** — CPU/memory usage percentage
- **Saturation** — Queue depth, thread pool usage
- **Errors** — OOM kills, disk errors, connection failures

#### DORA Metrics (pipeline)
- Deployment frequency, lead time, change failure rate, MTTR
- Monthly trend dashboards help drive data-driven decisions about pipeline investments

---

## Common Questions

**"How do you decide what to monitor?"**
Start with RED method for each service (Rate, Errors, Duration) and USE method for infrastructure (Utilization, Saturation, Errors). These 6 metrics tell you 80% of what you need to know. Add DORA metrics for pipeline health. Avoid monitoring everything — too many dashboards means nobody looks at any of them.

**"How do you handle alert fatigue?"**
Per-build alerting often fails — teams ignore it within a week. Switch to rate-based: alert only if failure rate exceeds a threshold (e.g., 20%) in a rolling hour window. Production deployment failures page on-call immediately. Everything else goes to a channel the team checks during standups.

**"Prometheus vs InfluxDB vs Datadog?"**
Prometheus is free, pull-based, and great for Kubernetes (service discovery). InfluxDB is push-based, better for high-cardinality time-series. Datadog is SaaS — less maintenance but expensive. Choose based on budget, infrastructure, and integration needs.
