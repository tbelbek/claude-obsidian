---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Kubernetes — Quick Reference

> [!info] How I've used it: Configure deployments for 60+ microservices at Combination — health probes, resource limits, rolling updates, HPA. Use Kustomize for environment overlays. Custom health checks (OutOfMemoryCheck, InitialDataLoadedCheck).

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Core Architecture\|Pod/Deployment/Service]] | pod=container, deployment=desired state, service=stable endpoint | [[#Core Architecture\|DaemonSet]] | one pod per node (Chrono, Alloy, monitoring agents) |
| [[#Core Architecture\|CronJob/Job]] | scheduled/batch work, not long-running | [[#Health Probes\|startup probe]] | runs during init only, prevents liveness killing slow starters |
| [[#Health Probes\|readiness probe]] | can it take traffic? no=removed from LB, not killed | [[#Health Probes\|liveness probe]] | is it stuck? yes=kill+restart. don't check DB health here |
| [[#Health Probes\|custom checks]] | OutOfMemoryCheck, InitialDataLoaded, InitializedCheck | [[#Resource Management\|requests vs limits]] | requests=guaranteed min, limits=hard max, OOMKill if exceeded |
| [[#Resource Management\|HPA]] | auto-scale pods on CPU/memory, 17 services at Combination | [[#Deployment Strategies\|rolling update]] | maxUnavailable:0 maxSurge:1, zero-downtime |
| [[#Deployment Strategies\|PDB]] | min pods during maintenance, 20+ at Combination | [[#Configuration\|Kustomize vs Helm]] | Kustomize=our services (overlays), Helm=platform (Cilium,Chrony) |
| [[#Networking\|Cilium]] | eBPF CNI, advanced network policies, replaces Azure CNI | [[#Core Architecture\|Contour]] | Envoy-based ingress, HTTPProxy CRDs, L7 routing |
| [[#Configuration\|secrets]] | Key Vault via CSI driver, never in Git/env vars | [[#Resource Management\|KEDA]] | event-driven autoscaling, scale-to-zero, queue-based |
| [[#Docker vs Kubernetes\|Docker vs K8s]] | Docker=build+run containers, K8s=orchestrate at scale | | |

## HOW WE USE IT

At Combination, I own the K8s deployment configs for 60+ microservices on Azure AKS. Here's the actual architecture:

### What Kubernetes Is
Kubernetes (K8s) is a container orchestration platform that manages containerized applications across a cluster of machines. It handles scheduling (which container runs where), scaling (add more instances when traffic increases), self-healing (restart crashed containers), rolling updates (deploy without downtime), service discovery (containers find each other by DNS name), and load balancing. Best for: running many microservices in production with high availability and automated operations.

### Cluster Infrastructure
- **AKS** — Azure Kubernetes Service, provisioned via Terraform (GP-IaC-K8s-AKS, GP-IaC-AKS)
- **Cilium** — CNI (Container Network Interface) for pod networking + network policy enforcement. Replaces Azure CNI. Supports CiliumNetworkPolicy for advanced rules beyond standard K8s NetworkPolicy
- **Chrony** — NTP time synchronization running as DaemonSet on every node. Critical for log correlation and distributed tracing timestamps
- **CloudFlare WARP** — Zero Trust networking for secure cluster access

### Ingress & Traffic
- **Contour** (primary) — Envoy-based ingress controller using HTTPProxy CRDs. Handles L7 routing, TLS termination, rate limiting. Has its own HPA, PDB, and NetworkPolicy
- **Nginx** (secondary) — Fallback ingress controller for compatibility
- **External DNS** — Automatically manages Azure DNS records from K8s Ingress/HTTPProxy resources
- **CloudFlare** — CDN and DNS layer in front of the cluster, managed via CDeploy

### Service Deployment Structure
Every service follows the same pattern:
```
service-name/
  k8s/
    deployment.yaml        — base deployment (image, ports, probes, env vars)
    kustomization.yaml     — Kustomize component (patches + resources)
    _envs/
      development/         — dev overrides (replicas, resource limits)
      global-prod/         — production overrides
      row-prod/            — region-specific prod (multi-tenant)
      cmb-prod/            — customer-specific prod
```
Kustomize uses `kind: Component` with patches — no Helm templating for services, just plain YAML + overlays.

### Workload Types We Run
- **Deployments** — Primary workload (60+ services). Stateless, CPU-based HPA
- **DaemonSets** — Chrony (time sync), Azure ScheduledEvents (node maintenance), Grafana Alloy (metrics collection)
- **CronJobs** — Data import pipelines (5+ scheduled jobs for sports data, casino data ingestion)
- **ScaledJobs** — KEDA-based job scaling for burst workloads
- **No StatefulSets** — Fully stateless architecture. State lives in MongoDB/Redis/Kafka, not in pods

### High Availability
- **HPA** — 17+ services with HorizontalPodAutoscaler. CPU target ~75%. Auto-scales during peak hours, scales down overnight *(we used this to handle traffic spikes without over-provisioning)*
- **PDB** — 20+ PodDisruptionBudgets. Ensures minimum pod count during node drains and AKS maintenance. Critical for ingress controllers and high-traffic services
- **Rolling updates** — `maxUnavailable: 0, maxSurge: 1`. New pod starts before old one stops. Readiness probe gates traffic

### Networking & Security
- **Network Policies** — 20+ standard K8s NetworkPolicies + 15+ CiliumNetworkPolicies. Default deny with allowlists. Rules for Azure infrastructure (172.16.0.0/12, 10.0.0.0/8), health checks, DNS, monitoring
- **Service Accounts** — 20+ across components. ClusterRoleBindings for cross-namespace (ingress, monitoring), RoleBindings for namespace-scoped
- **No service mesh** — Cilium handles network policy and observability. No Istio/Linkerd — complexity vs value trade-off for our scale

### Observability (deployed separately)
- **Grafana Alloy** — DaemonSet + Deployment variants for metrics scraping, trace collection, Azure metrics
- **Mimir** — Time-series metrics database (replaces Prometheus for storage)
- **Tempo** — Distributed tracing backend
- **Loki + Promtail** — Log aggregation (Promtail ships logs, Loki stores)
- **Pyroscope** — Continuous profiling (CPU/memory flamegraphs per service)
- **Lumberjack** — Custom in-house log processor for transformation/enrichment
- **kube-state-metrics** — K8s object metrics (pod status, deployment state)

### Custom Health Checks
Beyond standard K8s probes, our services have custom checks via the GP-Infra-ServiceBase-Framework:
- `OutOfMemoryCheck` — monitors heap pressure before the OOM killer triggers
- `InitialDataLoadedCheck` — verifies static data is loaded before accepting traffic
- `InitializedCheck` — GraphQL gateway waits until all 60+ federated schemas are loaded
- `DatabaseCheck` — MongoDB connectivity check integrated into readiness probe

### What's NOT in Our Setup (and why)
- **No StatefulSets** — All state lives in external data stores (MongoDB, Redis, Kafka). Pods are disposable.
- **No service mesh** — Cilium gives us network policies and basic observability. Istio/Linkerd would add complexity without enough value at our scale.
- **No ArgoCD/Flux** — Deployments are push-based via GitHub Actions, not GitOps pull-based. Works for our workflow.
- **Helm only for platform** — Cluster components (Cilium, Chrony, Contour, monitoring) use Helm. Application services use Kustomize — simpler, no template language.

---

## Key Concepts

### Core Architecture
- **Pod** — Smallest deployable unit. One or more containers sharing network and storage. In practice, one container per pod for most services. ← *our 60+ services each run as single-container pods*
- **Deployment** — Declares desired pod state (image, replicas, config). K8s continuously reconciles actual state with desired state. Handles scaling and rolling updates. ← *primary workload type for all our services*
- **ReplicaSet** — Ensures a specified number of pod replicas are running. Created automatically by Deployments — you rarely interact with it directly.
- **DaemonSet** — Runs exactly one pod per node. Used for node-level agents that need to run everywhere. ← *we run Chrony (NTP time sync), Azure ScheduledEvents (node maintenance detection), and Grafana Alloy (metrics collection) as DaemonSets — every node gets one instance automatically*
- **StatefulSet** — Like Deployment but for stateful workloads. Pods get stable network identity and persistent storage. Each pod has a predictable name (pod-0, pod-1, pod-2). ← *we don't use StatefulSets — all our state lives in MongoDB/Redis/Kafka, pods are disposable*
- **CronJob** — Scheduled job that runs on a cron schedule. Creates a Job resource at each scheduled time. ← *we use CronJobs for data import pipelines — sports data, casino data ingestion running every few hours*
- **Job** — Runs a pod to completion, then stops. For batch processing, not long-running services. Retries on failure. ← *our data ingestion pipelines use Jobs for one-off imports*
- **ScaledJob** — KEDA-based job scaling. Creates Jobs based on external metrics (queue depth, event count). ← *we use this for burst workloads — when a message queue fills up, KEDA creates more Job pods to drain it*
- **Service** — Stable network endpoint for a set of pods. Types: ClusterIP (internal), NodePort (external via node port), LoadBalancer (cloud load balancer). ← *all our services use ClusterIP — internal only, external traffic comes through Ingress*
- **Ingress** — HTTP/HTTPS routing from outside the cluster to services inside. Rules map hostnames and paths to backend services. ← *we use Contour (Envoy-based) with HTTPProxy CRDs instead of standard Ingress resources — more features (rate limiting, header routing, weighted backends)*
- **HTTPProxy** — Contour-specific CRD that replaces standard Ingress. Supports features Ingress doesn't: per-route rate limiting, request/response header manipulation, traffic mirroring, weighted backends. ← *our primary ingress resource type at Combination*
- **Node** — A machine (VM or physical) running pods. Kubelet manages pods on each node. Scheduler assigns pods to nodes based on resource requests.

### Docker vs Kubernetes
- **Different jobs** — Docker builds images and runs containers on one machine. Kubernetes runs containers across a cluster of machines and handles everything Docker can't: scheduling across nodes, auto-scaling, self-healing, rolling updates, service discovery, load balancing.
- **K8s doesn't build images** — You build with Docker (or Kaniko/BuildKit), push to a registry (ACR, Docker Hub), K8s pulls from the registry.
- **Container runtime** — K8s uses containerd or CRI-O, not Docker daemon. Docker images work fine — they're OCI-standard. Docker was removed as a K8s runtime in v1.24 because K8s only needs the runtime, not Docker's extra features (CLI, build, compose).
- **When you need K8s** — Multiple services, multiple instances, need auto-scaling, zero-downtime deployments, health-based routing. *(we use K8s at Combination for 60+ services)*
- **When Docker alone is enough** — Local development, single-server apps, Docker Compose for small stacks. *(we used Docker without K8s at Volvo for build containers)*

### Health Probes
Health probes are HTTP/TCP/command checks that Kubernetes runs periodically to determine if a container is alive, ready for traffic, or still starting up. Without probes, K8s has no way to know if your app is working — it just assumes it is.

- **Startup probe** — Runs during initialization only. Gives slow-starting services time to load caches or run migrations. Once it passes, it stops and liveness/readiness take over. ← *we added this after a service with 45-second cache warmup got stuck in an infinite restart loop — liveness was killing it before it finished starting*
- **Readiness probe** — "Can this pod receive traffic?" If it fails, pod is removed from service endpoints but NOT killed. Critical during rolling updates — new pod doesn't get traffic until it's ready. ← *every service has this — Contour routes traffic only to ready pods*
- **Liveness probe** — "Is this pod stuck?" If it fails, K8s kills and restarts the pod. Should only check if the process is hung, NOT if external dependencies are down (otherwise one DB blip kills all pods). ← *we check the process is responsive, not that MongoDB is up*
- **Probe types** — HTTP GET (hit `/health` endpoint), TCP socket (check port is open), exec (run a command in container). ← *we use HTTP GET hitting ASP.NET Core's `/health` endpoint*
- **Tuning** — `initialDelaySeconds` (wait before first check), `periodSeconds` (how often), `failureThreshold` (how many fails before action), `timeoutSeconds` (how long to wait for response). ← *we set these based on actual service behavior measured in Grafana — never copy-paste defaults*
- **Common mistake** — Not having a startup probe → liveness kills the pod during startup → infinite CrashLoopBackOff. Another: liveness checking database health → one DB blip restarts all pods simultaneously.

**Our custom health checks (GP-Infra-ServiceBase-Framework):**
- `LivenessCheck` — Basic process health. Is the event loop responsive? ← *standard for all services*
- `ReadinessCheck` — Can the service handle requests? Checks internal state. ← *standard for all services*
- `OutOfMemoryCheck` — Monitors .NET heap memory usage. Marks the pod as unhealthy before the Linux OOM killer triggers, giving K8s time to schedule a replacement pod gracefully instead of a sudden kill. ← *we use this on memory-intensive services like GP-Entity-Service*
- `InitialDataLoadedCheck` — Verifies that static reference data (config, lookup tables, feature flags) has been loaded from the database before the service accepts traffic. Without this, the first requests after startup would fail or return incomplete data. ← *we use this on services that preload data into memory at startup*
- `InitializedCheck` — GraphQL gateway-specific. Waits until all 60+ federated schemas are loaded from the SchemaRegistry before marking as ready. If the gateway starts serving queries before all schemas are loaded, some resolvers return errors. ← *GP-GraphQL-Gateway only*
- `DatabaseCheck` — Verifies MongoDB connectivity. Used as a readiness check — if the database is unreachable, the pod stops receiving new traffic but doesn't restart. ← *prevents serving requests that would all fail with connection errors*

### Resource Management
Resource management in K8s means defining how much CPU and memory each container gets — requests (guaranteed minimum) and limits (hard maximum). Get it wrong: too low = OOMKill and throttling, too high = wasted cluster capacity, no limits = one pod can starve others.

- **Requests** — Guaranteed minimum CPU/memory. Scheduler uses this to place pods on nodes. If requests too low, pods get scheduled on overloaded nodes. ← *we set requests based on steady-state Grafana metrics*
- **Limits** — Hard maximum. Pod gets OOMKilled if it exceeds memory limit. CPU is throttled (slower, not killed). ← *we set limits to peak + 20% headroom — too tight causes OOMKill during GC spikes*
- **QoS classes** — Guaranteed (requests = limits), Burstable (requests < limits), BestEffort (no requests/limits). Guaranteed pods are last to be evicted during node pressure. ← *most of our services are Burstable — requests for steady state, limits with headroom*
- **LimitRange** — Per-namespace defaults. Prevents deploying a pod with no limits — every pod gets at least the default.
- **ResourceQuota** — Per-namespace cap on total CPU/memory. Prevents one team from consuming the cluster.
- **HPA (Horizontal Pod Autoscaler)** — Scales pod count based on metrics. Scales up when CPU > target (e.g., 75%), scales down when load drops. ← *17 services have HPA at Combination — auto-scale during peak, scale down overnight. Cheaper than provisioning for peak 24/7*
- **VPA (Vertical Pod Autoscaler)** — Adjusts requests/limits based on observed usage. Requires pod restarts. Good for right-sizing — but we prefer HPA for scaling.
- **Cluster Autoscaler** — Scales nodes. Adds nodes when pods can't be scheduled, removes underutilized nodes. ← *AKS manages this for us — we configure min/max node count*
- **KEDA (Kubernetes Event-Driven Autoscaling)** — Scales based on external metrics (queue depth, event count, custom metrics). More flexible than HPA — can scale to zero. ← *we use KEDA ScaledJobs for burst workloads driven by message queue depth*

### Deployment Strategies
Deployment strategies control how Kubernetes replaces old pods with new ones during an update. The goal: update without downtime, with automatic rollback if something goes wrong.

- **Rolling update** — Default. Creates new pods before killing old ones. ← *our standard: `maxUnavailable: 0, maxSurge: 1` — new pod starts before old one stops, readiness gates traffic*
- **Blue-green** — Two full environments (blue = current, green = new). Switch traffic at ingress level. Instant rollback. More expensive (double resources).
- **Canary** — Small percentage of traffic to new version. Monitor metrics. Gradually increase if healthy. ← *we don't do canary yet — would need Contour traffic splitting or a service mesh*
- **Readiness gates** — New pod doesn't get traffic until readiness probe passes. ← *critical for our rolling updates — prevents routing to pods still loading federated schemas*
- **preStop hook** — Sleep a few seconds before container shutdown. Lets in-flight requests finish. ← *without this, active connections get dropped during rollover — we use 5-second sleep*
- **terminationGracePeriodSeconds** — How long K8s waits for graceful shutdown before force-killing. Default 30s. ← *we increase this for services processing long gRPC streams*
- **PodDisruptionBudget (PDB)** — Limits simultaneous pod disruptions during voluntary operations (node drain, AKS upgrade). ← *20+ PDBs at Combination — ensures ingress controllers and high-traffic services stay available during maintenance*

### Networking
- **ClusterIP** — Default service type. Internal-only. Pods within the cluster can reach it by service name (DNS).
- **DNS resolution** — `service-name.namespace.svc.cluster.local`. In practice, just `service-name` works within the same namespace.
- **Network Policies** — Firewall rules at the pod level. Control which pods can talk to which. Example: CI build pods only reach source repo, artifact registry, and test environments — no outbound internet.
- **Service Mesh** — Istio, Linkerd add mTLS, traffic management, observability between services. *(we don't use a service mesh at Combination — Cilium CNI gives us network policies and basic observability. The complexity of Istio/Linkerd isn't worth it at our scale.)*
- **Cilium** — Advanced CNI with network policy enforcement, observability, and some service mesh features without the full mesh overhead. *(we use Cilium at Combination as our CNI — CiliumNetworkPolicy for advanced rules, default-deny with allowlists)*

### Configuration
- **Kustomize** — Template-free overlays. Base `deployment.yaml` + environment-specific patches in `_envs/development/`, `_envs/global-prod/`. No Helm charts needed for simple cases. *(we used this to manage 60+ services across environments at Combination — one base config, environment-specific patches, no Helm template complexity)*
- **Helm** — Package manager for K8s. Charts bundle templates + values. Good for complex third-party deployments (Prometheus, Grafana, Cilium). We use Helm for cluster components, Kustomize for our services. *(we used Helm to deploy complex third-party charts (Cilium CNI, Chrony time sync) and Kustomize for our own services — different tools for different complexity levels)*
- **ConfigMaps** — Non-sensitive configuration. Mounted as files or environment variables. Changes require pod restart unless using dynamic reloading.
- **Secrets** — Sensitive data (credentials, API keys). Encrypted at rest, mounted as volumes or env vars. At Combination, most secrets come from Azure Key Vault via CSI driver. *(we used this to keep secrets out of Git and environment variables at Combination — pods read secrets as mounted files from Key Vault, no credentials stored in K8s)*
- **Namespaces** — Logical isolation. Separate namespace per team or environment. Combined with NetworkPolicies and ResourceQuotas for multi-tenancy.
- **Labels & Selectors** — Key-value pairs on resources. Services use selectors to find their pods. Essential for organizing 60+ microservices.

### Storage
- **PersistentVolume (PV)** — A piece of storage in the cluster. Provisioned by an admin or dynamically.
- **PersistentVolumeClaim (PVC)** — A request for storage by a pod. Binds to a PV. Used for stateful services (databases, caches).
- **StorageClass** — Defines the type of storage (SSD, HDD, Azure Disk, Azure Files). Enables dynamic provisioning.
- **EmptyDir** — Temporary storage that exists only for the pod's lifetime. Used for sharing files between containers in the same pod (e.g., init container downloads config, main container reads it).

### Observability
- **kubectl describe pod** — First thing to check when a pod won't start. Shows events, probe failures, resource issues. ← *my first debugging step — shows exactly why a pod is Pending, CrashLoopBackOff, or ImagePullBackOff*
- **kubectl logs** — Container stdout/stderr. `-p` for previous container logs (after crash). `-f` for streaming. ← *second step — application errors are here*
- **kubectl top** — Real-time CPU/memory per pod/node. Requires metrics-server. ← *quick check if a pod is resource-constrained*
- **Events** — `kubectl get events --sort-by=.metadata.creationTimestamp` — recent cluster events. ← *catches scheduling failures, probe failures, image pull errors that logs don't show*
- **Grafana Alloy** — Collection agent running as DaemonSet. Scrapes Prometheus metrics from pods, receives OTel traces, collects K8s events. ← *replaces standalone Prometheus scraper + OTel Collector in one agent*
- **Mimir** — Time-series metrics database. Stores what Prometheus collects. ← *we use Mimir instead of Prometheus TSDB for long-term storage and multi-tenancy*
- **Tempo** — Distributed tracing backend. Stores traces collected via OpenTelemetry. ← *every request across 60+ services gets a trace ID — click a slow request in Grafana, see the full span breakdown*
- **Loki** — Log aggregation. Indexes labels only (not full text) — cheaper than Elasticsearch for logs. ← *Promtail ships logs from pods, Lumberjack enriches them, Loki stores them*
- **Pyroscope** — Continuous profiling. CPU and memory flamegraphs per service. ← *shows where CPU/memory is spent without manual profiling sessions*
- **kube-state-metrics** — Exports K8s object state as Prometheus metrics: pod status, deployment replicas, HPA state, node conditions. ← *powers our cluster-level Grafana dashboards*

### Security
- **RBAC (Role-Based Access Control)** — Roles define permissions (get, list, create, delete on resources), RoleBindings assign roles to users/service accounts. ← *20+ ServiceAccounts with scoped permissions — ingress controllers get cluster-wide, application services get namespace-scoped*
- **Service Accounts** — Identity for pods. Each pod runs as a service account. ← *we use Azure Workload Identity — pods authenticate to Azure services (Key Vault, ACR) via service account federation, no stored credentials*
- **Network Policies** — Default deny + explicit allowlists. Standard K8s NetworkPolicy for basic rules, CiliumNetworkPolicy for L7 filtering and DNS-aware rules. ← *20+ NetworkPolicies + 15+ CiliumNetworkPolicies at Combination — pods can only talk to what they need*
- **Pod Security Standards** — Restrict pod capabilities: no privileged containers, no host networking, no root user. Three levels: Privileged, Baseline, Restricted. ← *our services run as non-root users*
- **Image scanning** — Trivy in CI pipeline scans images for OS and app-level vulnerabilities before push to ACR. ← *critical vulnerability = build fails, image never reaches the registry*

## Sorulursa

> [!faq]- "How do you debug a pod that won't start?"
> `kubectl describe pod` first — shows events, pull errors, probe failures, resource issues. Then `kubectl logs` for application errors. If the container crashes immediately, `kubectl logs -p` shows previous container logs. For OOMKilled, check resource limits vs actual usage in Grafana. For CrashLoopBackOff, usually a config issue or missing dependency. For ImagePullBackOff, check image name/tag and registry credentials.

> [!faq]- "How do you handle zero-downtime deployments?"
> Rolling update with `maxUnavailable: 0, maxSurge: 1` — new pod starts before old one stops. Readiness probe gates traffic — new pod doesn't get requests until it's ready. preStop hook sleeps a few seconds to drain in-flight requests. terminationGracePeriodSeconds set high enough for graceful shutdown. PodDisruptionBudget ensures minimum pod count during voluntary disruptions.

> [!faq]- "How do you manage 60+ services in Kubernetes?"
> Kustomize overlays with a consistent structure per service — base deployment in `k8s/`, env-specific patches in `k8s/_envs/`. Labels and namespaces for organization. Resource quotas per namespace. HPA for variable-load services. Shared GitHub Actions workflows for deployment so every service deploys the same way. Grafana dashboards with namespace/service filters for monitoring.

> [!faq]- "Kustomize vs Helm — when do you use which?"
> Kustomize for our own services — simple overlays, no templating language to learn, native to kubectl. Helm for third-party software (Prometheus, Grafana, Cilium, Chrony) where the upstream chart handles the complexity. We don't use Helm for our services because Kustomize is simpler and the deployment configs are straightforward.

> [!faq]- "How do you handle secrets in Kubernetes?"
> Azure Key Vault with CSI Secrets Store driver. Secrets mounted into pods as volumes — the pod reads them as files. No secrets in ConfigMaps, no secrets in environment variables (visible in `kubectl describe`), no secrets in Git. For service-to-service auth, pod identity (Azure Workload Identity) so pods authenticate without stored credentials.

> [!faq]- "Can you run Kubernetes without Docker?"
> Yes. K8s dropped Docker as a runtime in v1.24. It uses containerd or CRI-O directly — both are OCI-compliant runtimes. Docker-built images still work because they follow the OCI image spec. The change only affects how K8s starts containers, not how you build them. We still build with Docker (or Kaniko in CI), push to ACR, and K8s pulls the OCI image.

> [!faq]- "How do you right-size resource requests/limits?"
> Start by deploying with generous limits and no HPA. Run the service under load for a week. Check Grafana for steady-state CPU/memory and peak usage (GC spikes, batch processing). Set requests = steady-state, limits = peak + 20% headroom. Then enable HPA with a target of 70% CPU. Review quarterly as usage patterns change.

> [!faq]- "Walk me through the request flow in your K8s architecture"
> User request → CloudFlare CDN/DNS → Contour Ingress Controller (Envoy-based, L7 routing, TLS termination) → K8s Service (ClusterIP) → Pod (selected by label selector). Inside the pod: ASP.NET Core middleware pipeline → GraphQL resolver or gRPC handler → MongoDB/Kafka/Redis. Response flows back the same path. If the pod fails readiness, Contour removes it from the rotation. If multiple replicas exist, Contour load-balances across them.

> [!faq]- "Why Cilium instead of Azure CNI or Calico?"
> Cilium uses eBPF — kernel-level packet processing instead of iptables. Faster, more observable, and supports advanced network policies (L7 filtering, DNS-aware rules) that standard K8s NetworkPolicy can't do. CiliumNetworkPolicy lets us write rules like "allow this pod to talk to this DNS name" instead of just IP ranges. At our scale (60+ services), the observability and policy granularity is worth the slightly more complex setup.

> [!faq]- "Why no service mesh?"
> We evaluated Istio and decided the complexity wasn't worth it for our use case. Cilium gives us network policies and basic observability. For mTLS, we use Azure Workload Identity instead of mesh-level mTLS. For traffic management, Contour handles routing and rate limiting at the ingress level. A service mesh adds a sidecar to every pod — that's 60+ extra containers consuming memory and CPU. We'd reconsider if we needed advanced traffic splitting (canary by percentage) or cross-cluster service discovery.

> [!faq]- "How do you handle multi-tenant deployments?"
> Environment overlays in Kustomize. Each tenant/region has its own `_envs/` directory (global-prod, row-prod, cmb-prod). Same base deployment, different replicas, resource limits, and environment variables per tenant. Network policies isolate tenants at the namespace level. CloudFlare routes traffic to the correct cluster/namespace based on DNS.

> [!faq]- "What monitoring do you have on the cluster itself?"
> Grafana Alloy (DaemonSet) scrapes node and pod metrics. kube-state-metrics exports K8s object state (pod status, deployment replicas, HPA state). Mimir stores time-series data. Pyroscope does continuous CPU/memory profiling per service. We have dashboards for: cluster resource utilization, pod restart rates, HPA scaling events, node pressure, and PDB violations during maintenance. Alerts fire on: OOMKill rate, pod CrashLoopBackOff, node NotReady, and HPA at max replicas.

---

*[[00-dashboard]]*
