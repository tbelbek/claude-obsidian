---
tags:
  - education-kit
---

# Kubernetes — Education Kit

## Key Concepts

### What Kubernetes Is
Kubernetes (K8s) is a container orchestration platform that manages containerized applications across a cluster of machines. It handles scheduling (which container runs where), scaling (add more instances when traffic increases), self-healing (restart crashed containers), rolling updates (deploy without downtime), service discovery (containers find each other by DNS name), and load balancing. Best for: running many microservices in production with high availability and automated operations.

### Core Architecture
- **Pod** — Smallest deployable unit. One or more containers sharing network and storage. In practice, one container per pod for most services.
- **Deployment** — Declares desired pod state (image, replicas, config). K8s continuously reconciles actual state with desired state. Handles scaling and rolling updates.
- **ReplicaSet** — Ensures a specified number of pod replicas are running. Created automatically by Deployments — you rarely interact with it directly.
- **DaemonSet** — Runs exactly one pod per node. Used for node-level agents that need to run everywhere (time sync, metrics collection, log shipping).
- **StatefulSet** — Like Deployment but for stateful workloads. Pods get stable network identity and persistent storage. Each pod has a predictable name (pod-0, pod-1, pod-2).
- **CronJob** — Scheduled job that runs on a cron schedule. Creates a Job resource at each scheduled time.
- **Job** — Runs a pod to completion, then stops. For batch processing, not long-running services. Retries on failure.
- **ScaledJob** — KEDA-based job scaling. Creates Jobs based on external metrics (queue depth, event count).
- **Service** — Stable network endpoint for a set of pods. Types: ClusterIP (internal), NodePort (external via node port), LoadBalancer (cloud load balancer).
- **Ingress** — HTTP/HTTPS routing from outside the cluster to services inside. Rules map hostnames and paths to backend services. Ingress controllers (Nginx, Contour/Envoy, Traefik) implement the actual routing.
- **Node** — A machine (VM or physical) running pods. Kubelet manages pods on each node. Scheduler assigns pods to nodes based on resource requests.

### Docker vs Kubernetes
- **Different jobs** — Docker builds images and runs containers on one machine. Kubernetes runs containers across a cluster of machines and handles everything Docker cannot: scheduling across nodes, auto-scaling, self-healing, rolling updates, service discovery, load balancing.
- **K8s does not build images** — You build with Docker (or Kaniko/BuildKit), push to a registry, K8s pulls from the registry.
- **Container runtime** — K8s uses containerd or CRI-O, not Docker daemon. Docker images work fine — they are OCI-standard. Docker was removed as a K8s runtime in v1.24 because K8s only needs the runtime, not Docker's extra features (CLI, build, compose).
- **When you need K8s** — Multiple services, multiple instances, need auto-scaling, zero-downtime deployments, health-based routing.
- **When Docker alone is enough** — Local development, single-server apps, Docker Compose for small stacks.

### Health Probes
Health probes are HTTP/TCP/command checks that Kubernetes runs periodically to determine if a container is alive, ready for traffic, or still starting up. Without probes, K8s has no way to know if your app is working — it just assumes it is.

- **Startup probe** — Runs during initialization only. Gives slow-starting services time to load caches or run migrations. Once it passes, it stops and liveness/readiness take over. Without it, liveness may kill pods before they finish starting, causing infinite CrashLoopBackOff.
- **Readiness probe** — "Can this pod receive traffic?" If it fails, pod is removed from service endpoints but NOT killed. Critical during rolling updates — new pod does not get traffic until it is ready.
- **Liveness probe** — "Is this pod stuck?" If it fails, K8s kills and restarts the pod. Should only check if the process is hung, NOT if external dependencies are down (otherwise one DB blip kills all pods).
- **Probe types** — HTTP GET (hit `/health` endpoint), TCP socket (check port is open), exec (run a command in container).
- **Tuning** — `initialDelaySeconds` (wait before first check), `periodSeconds` (how often), `failureThreshold` (how many fails before action), `timeoutSeconds` (how long to wait for response). Set based on actual service behavior — never copy-paste defaults.
- **Common mistake** — Not having a startup probe causing liveness to kill the pod during startup leading to infinite CrashLoopBackOff. Another: liveness checking database health causing one DB blip to restart all pods simultaneously.

**Custom health check patterns:**
- **OutOfMemoryCheck** — Monitors heap memory usage. Marks the pod as unhealthy before the OS OOM killer triggers, giving K8s time to schedule a replacement gracefully.
- **InitialDataLoadedCheck** — Verifies that static reference data (config, lookup tables, feature flags) has been loaded before the service accepts traffic.
- **InitializedCheck** — For gateway services, waits until all downstream schemas or configurations are loaded before marking as ready.
- **DatabaseCheck** — Verifies database connectivity. Used as a readiness check — if the database is unreachable, the pod stops receiving new traffic but does not restart.

### Resource Management
Resource management in K8s means defining how much CPU and memory each container gets — requests (guaranteed minimum) and limits (hard maximum). Get it wrong: too low = OOMKill and throttling, too high = wasted cluster capacity, no limits = one pod can starve others.

- **Requests** — Guaranteed minimum CPU/memory. Scheduler uses this to place pods on nodes. If requests too low, pods get scheduled on overloaded nodes.
- **Limits** — Hard maximum. Pod gets OOMKilled if it exceeds memory limit. CPU is throttled (slower, not killed).
- **QoS classes** — Guaranteed (requests = limits), Burstable (requests < limits), BestEffort (no requests/limits). Guaranteed pods are last to be evicted during node pressure.
- **LimitRange** — Per-namespace defaults. Prevents deploying a pod with no limits — every pod gets at least the default.
- **ResourceQuota** — Per-namespace cap on total CPU/memory. Prevents one team from consuming the cluster.
- **HPA (Horizontal Pod Autoscaler)** — Scales pod count based on metrics. Scales up when CPU > target (e.g., 75%), scales down when load drops. More cost-effective than provisioning for peak 24/7.
- **VPA (Vertical Pod Autoscaler)** — Adjusts requests/limits based on observed usage. Requires pod restarts. Good for right-sizing.
- **Cluster Autoscaler** — Scales nodes. Adds nodes when pods cannot be scheduled, removes underutilized nodes.
- **KEDA (Kubernetes Event-Driven Autoscaling)** — Scales based on external metrics (queue depth, event count, custom metrics). More flexible than HPA — can scale to zero.

### Deployment Strategies
Deployment strategies control how Kubernetes replaces old pods with new ones during an update. The goal: update without downtime, with automatic rollback if something goes wrong.

- **Rolling update** — Default. Creates new pods before killing old ones. Typical config: `maxUnavailable: 0, maxSurge: 1` — new pod starts before old one stops, readiness gates traffic.
- **Blue-green** — Two full environments (blue = current, green = new). Switch traffic at ingress level. Instant rollback. More expensive (double resources).
- **Canary** — Small percentage of traffic to new version. Monitor metrics. Gradually increase if healthy. Requires traffic splitting at ingress or service mesh level.
- **Readiness gates** — New pod does not get traffic until readiness probe passes. Critical for rolling updates.
- **preStop hook** — Sleep a few seconds before container shutdown. Lets in-flight requests finish. Without this, active connections get dropped during rollover.
- **terminationGracePeriodSeconds** — How long K8s waits for graceful shutdown before force-killing. Default 30s. Increase for services processing long-running requests.
- **PodDisruptionBudget (PDB)** — Limits simultaneous pod disruptions during voluntary operations (node drain, cluster upgrade). Ensures minimum pod count during maintenance.

### Networking
- **ClusterIP** — Default service type. Internal-only. Pods within the cluster can reach it by service name (DNS).
- **DNS resolution** — `service-name.namespace.svc.cluster.local`. In practice, just `service-name` works within the same namespace.
- **Network Policies** — Firewall rules at the pod level. Control which pods can talk to which. Default deny with explicit allowlists is the recommended approach.
- **Service Mesh** — Istio, Linkerd add mTLS, traffic management, observability between services. Adds a sidecar to every pod — extra resource consumption. Evaluate complexity vs value for your scale.
- **CNI plugins** — Container Network Interface plugins handle pod networking. Options include Calico, Cilium (eBPF-based, supports advanced L7 policies), Flannel, and cloud-specific CNIs.

### Configuration
- **Kustomize** — Template-free overlays. Base `deployment.yaml` + environment-specific patches. No Helm charts needed for simple cases. Simpler than Helm for application services — no template language to learn, native to kubectl.
- **Helm** — Package manager for K8s. Charts bundle templates + values. Good for complex third-party deployments (Prometheus, Grafana, CNI plugins). Use Helm for cluster components, Kustomize for your own services — different tools for different complexity levels.
- **ConfigMaps** — Non-sensitive configuration. Mounted as files or environment variables. Changes require pod restart unless using dynamic reloading.
- **Secrets** — Sensitive data (credentials, API keys). Encrypted at rest, mounted as volumes or env vars. Best practice: use an external secrets manager (Key Vault, Vault) via CSI driver — secrets never stored in K8s or Git.
- **Namespaces** — Logical isolation. Separate namespace per team or environment. Combined with NetworkPolicies and ResourceQuotas for multi-tenancy.
- **Labels & Selectors** — Key-value pairs on resources. Services use selectors to find their pods. Essential for organizing large numbers of microservices.

### Storage
- **PersistentVolume (PV)** — A piece of storage in the cluster. Provisioned by an admin or dynamically.
- **PersistentVolumeClaim (PVC)** — A request for storage by a pod. Binds to a PV. Used for stateful services (databases, caches).
- **StorageClass** — Defines the type of storage (SSD, HDD, cloud disk). Enables dynamic provisioning.
- **EmptyDir** — Temporary storage that exists only for the pod's lifetime. Used for sharing files between containers in the same pod.

### Observability
- **kubectl describe pod** — First thing to check when a pod will not start. Shows events, probe failures, resource issues.
- **kubectl logs** — Container stdout/stderr. `-p` for previous container logs (after crash). `-f` for streaming.
- **kubectl top** — Real-time CPU/memory per pod/node. Requires metrics-server.
- **Events** — `kubectl get events --sort-by=.metadata.creationTimestamp` — recent cluster events. Catches scheduling failures, probe failures, image pull errors that logs do not show.
- **Metrics collection** — Agents (Prometheus, Grafana Alloy) scrape metrics from pods. kube-state-metrics exports K8s object state as Prometheus metrics.
- **Distributed tracing** — OpenTelemetry traces across services. Stored in backends like Tempo or Jaeger.
- **Log aggregation** — Centralized log collection (Loki, Elasticsearch). Correlate logs with trace IDs for full observability.
- **Continuous profiling** — Tools like Pyroscope show CPU and memory flamegraphs per service without manual profiling sessions.

### Security
- **RBAC (Role-Based Access Control)** — Roles define permissions (get, list, create, delete on resources), RoleBindings assign roles to users/service accounts. Scope permissions narrowly — cluster-wide only when necessary, namespace-scoped otherwise.
- **Service Accounts** — Identity for pods. Each pod runs as a service account. Use workload identity federation so pods authenticate to cloud services without stored credentials.
- **Network Policies** — Default deny + explicit allowlists. Standard K8s NetworkPolicy for basic rules, CNI-specific policies (e.g., CiliumNetworkPolicy) for L7 filtering and DNS-aware rules.
- **Pod Security Standards** — Restrict pod capabilities: no privileged containers, no host networking, no root user. Three levels: Privileged, Baseline, Restricted.
- **Image scanning** — Scan images for OS and app-level vulnerabilities before push to registry. Critical vulnerability = build fails, image never reaches the registry.

## Sorulursa

> [!faq]- "How do you debug a pod that won't start?"
> `kubectl describe pod` first — shows events, pull errors, probe failures, resource issues. Then `kubectl logs` for application errors. If the container crashes immediately, `kubectl logs -p` shows previous container logs. For OOMKilled, check resource limits vs actual usage in monitoring. For CrashLoopBackOff, usually a config issue or missing dependency. For ImagePullBackOff, check image name/tag and registry credentials.

> [!faq]- "How do you handle zero-downtime deployments?"
> Rolling update with `maxUnavailable: 0, maxSurge: 1` — new pod starts before old one stops. Readiness probe gates traffic — new pod does not get requests until it is ready. preStop hook sleeps a few seconds to drain in-flight requests. terminationGracePeriodSeconds set high enough for graceful shutdown. PodDisruptionBudget ensures minimum pod count during voluntary disruptions.

> [!faq]- "Kustomize vs Helm — when do you use which?"
> Kustomize for your own services — simple overlays, no templating language to learn, native to kubectl. Helm for third-party software (Prometheus, Grafana, CNI plugins) where the upstream chart handles the complexity. If deployment configs are straightforward, Kustomize is simpler.

> [!faq]- "How do you handle secrets in Kubernetes?"
> Use an external secrets manager (Key Vault, Vault) with CSI Secrets Store driver. Secrets mounted into pods as volumes — the pod reads them as files. No secrets in ConfigMaps, no secrets in environment variables (visible in `kubectl describe`), no secrets in Git. For service-to-service auth, use workload identity so pods authenticate without stored credentials.

> [!faq]- "Can you run Kubernetes without Docker?"
> Yes. K8s dropped Docker as a runtime in v1.24. It uses containerd or CRI-O directly — both are OCI-compliant runtimes. Docker-built images still work because they follow the OCI image spec. The change only affects how K8s starts containers, not how you build them.

> [!faq]- "How do you right-size resource requests/limits?"
> Start by deploying with generous limits and no HPA. Run the service under load for a week. Check monitoring for steady-state CPU/memory and peak usage (GC spikes, batch processing). Set requests = steady-state, limits = peak + 20% headroom. Then enable HPA with a target of 70% CPU. Review quarterly as usage patterns change.

> [!faq]- "Walk me through the request flow in a K8s architecture"
> User request goes through CDN/DNS, then the Ingress Controller (L7 routing, TLS termination), then the K8s Service (ClusterIP), then the Pod (selected by label selector). Inside the pod: application middleware pipeline processes the request, calls databases or other services as needed. Response flows back the same path. If the pod fails readiness, the ingress controller removes it from the rotation. If multiple replicas exist, the ingress controller load-balances across them.

> [!faq]- "Why might you choose an eBPF-based CNI (like Cilium) over iptables-based alternatives?"
> eBPF provides kernel-level packet processing instead of iptables. Faster, more observable, and supports advanced network policies (L7 filtering, DNS-aware rules) that standard K8s NetworkPolicy cannot do. At scale with many services, the observability and policy granularity is worth the slightly more complex setup.

> [!faq]- "Why might you skip a service mesh?"
> A service mesh (Istio, Linkerd) adds a sidecar proxy to every pod — extra containers consuming memory and CPU. If your CNI already gives you network policies and basic observability, and your ingress controller handles routing and rate limiting, the service mesh may add more complexity than value. Reconsider if you need advanced traffic splitting (canary by percentage) or cross-cluster service discovery.
