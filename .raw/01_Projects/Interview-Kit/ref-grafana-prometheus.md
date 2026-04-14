---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Grafana & Prometheus — Quick Reference

> [!info] How I've used it: At KocSistem, built DORA metric dashboards and pipeline health monitoring in Grafana with Prometheus. At Combination, Grafana for service metrics and resource usage. At KocSistem (Senior Dev), built the first monitoring POC that started everything.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Prometheus\|Prometheus]] | pull-based metrics, PromQL, time-series DB | [[#Grafana\|Grafana]] | dashboards, alerting, data source agnostic |
| [[#RED Method (per service)\|RED method]] | Rate, Errors, Duration — per service | [[#USE Method (per resource)\|USE method]] | Utilization, Saturation, Errors — per resource |
| [[#DORA Metrics (pipeline)\|DORA in Grafana]] | 4 metrics, monthly reports, data-driven decisions | [[#What I Monitored\|what I monitored]] | pipeline health, service latency, resource usage |

## HOW WE USED IT

**At KocSistem (Senior Dev)** — I [[ls-initiative|built the first monitoring POC]] on my own time. Prometheus for scraping service metrics, Grafana for dashboards showing latency, memory usage, and error rates. This became the template for every new service and [[ls-growth|led to my promotion]].

**At KocSistem (Manager)** — I [[ref-dora#HOW WE USED IT|built DORA metric dashboards]] tracking deployment frequency, lead time, change failure rate, and MTTR. Reported to leadership monthly. Also set up pipeline health dashboards — build duration trends, failure rates, slowest stages. Rate-based alerting (20% threshold) instead of per-build notifications.

**At Combination** — Grafana dashboards for service metrics, CPU/memory usage per pod, and deployment tracking. Prometheus scrapes metrics endpoints on all services.

---

## Key Concepts

### Prometheus
- **Pull-based model** — Prometheus scrapes metrics endpoints (`/metrics`) on your services at regular intervals. You don't push metrics, Prometheus pulls them.
- **PromQL** — Query language for Prometheus. Examples: `rate(http_requests_total[5m])` for request rate, `histogram_quantile(0.95, ...)` for p95 latency.
- **Exporters** — Adapters that expose metrics from systems that don't natively support Prometheus format (databases, message brokers, etc.).
- **Alertmanager** — Separate component for routing alerts. Supports Slack, email, PagerDuty. We used Slack integration at KocSistem.

### Grafana
- **Dashboards** — Visual panels showing metrics over time. Each panel is a PromQL query rendered as a graph, gauge, table, or heatmap.
- **Data sources** — Grafana connects to Prometheus, InfluxDB, Elasticsearch, Loki, etc. We used Prometheus as the primary data source.
- **Alerting** — Grafana can also define alert rules on dashboard panels. We used this for pipeline failure rate thresholds.
- **Variables** — Dashboard variables for filtering (by service, environment, namespace). One dashboard serves all services.

### What I Monitored

#### RED Method (per service)
- **Rate** — Request rate per second
- **Errors** — Error rate / error percentage
- **Duration** — Request latency (p50, p95, p99)

#### USE Method (per resource)
- **Utilization** — CPU/memory usage percentage
- **Saturation** — Queue depth, thread pool usage
- **Errors** — OOM kills, disk errors, connection failures

#### DORA Metrics (pipeline)
- [[ref-dora#Deployment Frequency|Deployment frequency]], [[ref-dora#Lead Time for Changes|lead time]], [[ref-dora#Change Failure Rate|change failure rate]], [[ref-dora#Mean Time to Restore (MTTR)|MTTR]]

## Sorulursa

> [!faq]- "How did you decide what to monitor?"
> Started with RED method for each service (Rate, Errors, Duration) and USE method for infrastructure (Utilization, Saturation, Errors). These 6 metrics tell you 80% of what you need to know. Added DORA metrics for pipeline health. Avoided monitoring everything — too many dashboards means nobody looks at any of them.

> [!faq]- "How did you handle alert fatigue?"
> Per-build alerting failed — team ignored it within a week. Switched to rate-based: alert only if failure rate exceeds 20% in a rolling hour window. Production deployment failures page on-call immediately. Everything else goes to a Slack channel that the team checks during standups.

> [!faq]- "Prometheus vs InfluxDB vs Datadog?"
> Prometheus is free, pull-based, and great for Kubernetes (service discovery). InfluxDB is push-based, better for high-cardinality time-series. Datadog is SaaS — less maintenance but expensive. At KocSistem we used Prometheus because it's free and integrates well with the K8s ecosystem. At Combination, same reasoning.

---

*[[00-dashboard]]*
