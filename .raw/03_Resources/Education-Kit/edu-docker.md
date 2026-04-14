---
tags:
  - education-kit
---

# Docker — Education Kit

## Key Concepts

### What Docker Is
Docker packages applications and their dependencies into lightweight, portable containers that run consistently across any environment — dev laptop, CI server, production cluster. A container is an isolated process with its own filesystem, network, and resource limits, running on a shared OS kernel (not a VM). Best for: eliminating 'works on my machine' problems, standardizing builds, and creating small deployable units that Kubernetes can orchestrate.

### Multi-Stage Builds

Think of it like moving houses. You need a big truck and a full crew to pack everything up (that is your SDK image with compilers and build tools). But once you are at the new place, you do not need the truck anymore — you just need your furniture.

Multi-stage builds work the same way. First stage: big image with everything needed to compile your code. Second stage: tiny image that only runs the finished app. You copy just the compiled output over — not the compilers, not the source code, not the build junk.

**The win:** Your production image drops from 800MB to 80MB. That means faster deploys, cheaper storage, and way less attack surface for security.

**The catch:** Debugging gets harder since there is no shell in the slim image. And if you mess up the COPY, you accidentally bloat the image again.

- **Why** — SDK image (~800MB) is needed to compile. Runtime image (~80MB) is enough to run. Multi-stage copies only the published output to the slim image.
- **Pattern** — Stage 1: `FROM sdk AS build` — restore, build, publish. Stage 2: `FROM runtime` — copy from build stage.
- **Result** — Smaller images, smaller attack surface, faster pulls, faster starts.

### Layer Caching
- **How it works** — Each Dockerfile instruction creates a layer. Docker caches layers and reuses them if inputs have not changed. Cache invalidates from the first changed layer downward.
- **Common mistake** — `COPY . .` early in the Dockerfile copies everything, so any source change invalidates the cache for all subsequent layers including dependency restore.
- **Fix** — Copy project files first (*.csproj / package.json), run restore, then copy source. Dependencies cached unless actually changed.

### Build Context
- **What it is** — The set of files Docker sends to the daemon for building. Everything in the directory unless excluded.
- **.dockerignore** — Excludes files from the build context. Must include `.git`, `node_modules`, `bin/obj`. Without it, builds are slow and images may contain unnecessary files.

### Image Management
- **Tagging** — Commit SHA + build number for development. Semantic version for releases. Never use `latest` in production — essential for tracing any running container back to the exact commit.
- **Retention policies** — Keep last N images per branch, keep all tagged releases, purge old dev images. Without cleanup, registry storage grows unchecked.
- **Base image pinning** — Pin specific versions (not `latest`) for reproducible builds. Pin exact digest for production (e.g., `aspnet:9.0@sha256:abc123` instead of `aspnet:9.0`).

### Docker-in-Docker vs Kaniko
- **DinD** — Runs Docker daemon inside a container. Works but requires privileged mode (security risk).
- **Kaniko** — Builds images without a Docker daemon. Runs unprivileged. Preferred for CI on Kubernetes.
- **BuildKit** — Docker's modern build engine. Supports cache mounts, better parallelism, improved layer caching.

### Docker vs Kubernetes — How They Relate
- **Docker** — Builds and runs containers. One host, one or more containers. You write a Dockerfile, build an image, run a container. Docker handles: image building, container lifecycle, networking between containers on the same host, volume management.
- **Kubernetes** — Orchestrates containers across multiple hosts. You describe desired state (how many replicas, health checks, resource limits), K8s makes it happen. K8s handles: scheduling pods to nodes, scaling, rolling updates, service discovery, load balancing, self-healing (restart crashed pods).
- **Docker without K8s** — Works for development, single-server apps, Docker Compose setups. You manage everything manually: scaling, failover, deployment.
- **K8s without Docker** — K8s can use containerd or CRI-O as container runtimes. Docker was removed as a K8s runtime in v1.24 (images still work — Docker images are OCI-compliant).
- **How they work together** — Docker builds the image (Dockerfile then image then registry). K8s pulls the image and runs it as pods. Docker is the build tool, K8s is the orchestration tool.

### Dockerfile Deep Dive — What Interviewers Ask

**Instruction order matters:**
- Each instruction creates a layer. Docker caches layers top-down — first changed instruction invalidates everything below.
- Put things that change rarely (base image, system packages) at the top. Things that change often (source code) at the bottom.
- `COPY package.json . && RUN npm install` before `COPY . .` — dependencies cached unless package.json changes.

**Key instructions:**
- `FROM` — Base image. Use specific tags, not `latest`. Pin digest for reproducibility in production.
- `RUN` — Executes command in a new layer. Combine with `&&` to reduce layers: `RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*`
- `COPY` vs `ADD` — `COPY` is simple copy. `ADD` can extract tars and fetch URLs — use `COPY` unless you specifically need extraction. `ADD` is harder to reason about.
- `WORKDIR` — Sets working directory. Better than `RUN cd /app` because it persists across instructions.
- `EXPOSE` — Documentation only. Does not actually open the port. The port is opened by the application and mapped at runtime.
- `ENV` vs `ARG` — `ENV` persists into the running container. `ARG` is build-time only. Use `ARG` for build parameters (version numbers), `ENV` for runtime config.
- `ENTRYPOINT` vs `CMD` — `ENTRYPOINT` sets the executable. `CMD` provides default arguments. Together: `ENTRYPOINT ["dotnet"]` + `CMD ["MyApp.dll"]`. In practice, just use `ENTRYPOINT ["dotnet", "MyApp.dll"]` for clarity.
- `USER` — Run as non-root. Security best practice. `RUN adduser --disabled-password appuser` then `USER appuser`. Never run production containers as root.
- `HEALTHCHECK` — In-container health check. K8s has its own probes, so this is mainly for Docker Compose or standalone containers.

**Multi-stage build pattern (.NET):**
```
Stage 1 (build):
  FROM sdk:9.0 AS build
  COPY *.csproj → restore (cached if deps unchanged)
  COPY . → build → publish

Stage 2 (runtime):
  FROM aspnet:9.0
  COPY --from=build /app/publish .
  ENTRYPOINT ["dotnet", "MyApp.dll"]
```
Result: ~80MB image instead of ~800MB.

**Common Dockerfile mistakes:**
- `COPY . .` before `RUN restore` — invalidates dependency cache on every code change
- Using `latest` tag — build breaks when base image updates unexpectedly
- Running as root — security risk, K8s Pod Security Standards may reject it
- Not using `.dockerignore` — `.git`, `node_modules`, `bin/obj` end up in build context, slowing build
- Too many layers — each `RUN` creates a layer. Combine related commands with `&&`
- Secrets in `ENV` or `ARG` — visible in image history (`docker history`). Use build secrets (`--secret`) or runtime injection
- Not cleaning up in the same layer — `RUN apt install && ... && rm -rf /var/lib/apt/lists/*` in one command. If you `rm` in a separate `RUN`, the data is still in the previous layer

**Image size optimization:**
- Multi-stage builds (biggest win — SDK vs runtime image)
- Alpine or distroless base images (smaller but may lack debugging tools)
- `.dockerignore` (smaller build context = faster builds)
- Combine RUN commands (fewer layers)
- Remove temp files in the same layer they are created

## Sorulursa

> [!faq]- "How do you decide what goes in the Dockerfile vs what stays outside?"
> Build-time dependencies go in the Dockerfile. Runtime configuration goes in environment variables or config files mounted at deploy time. Secrets never go in the image — they are injected at runtime via a secrets manager or Kubernetes secrets. The image should be the same across all environments — only the config changes.

> [!faq]- "How do you handle Docker image security?"
> Scan images with Trivy before pushing to the registry. Use minimal base images (alpine or distroless where possible). Pin base image versions — do not use `latest`. Set up retention policies so old vulnerable images get cleaned up. And never run as root in production — set `USER` in the Dockerfile.

> [!faq]- "What's the difference between Docker and Kubernetes?"
> Docker builds and runs containers on a single host. Kubernetes orchestrates containers across many hosts — scheduling, scaling, health checking, rolling updates, service discovery. Docker is the build tool, K8s is the orchestration tool. You can use Docker without K8s (development, simple deployments) but not K8s without a container runtime (containerd, CRI-O — Docker itself was removed as a K8s runtime in v1.24, though Docker-built images still work).

> [!faq]- "Walk me through a multi-stage Dockerfile"
> Stage 1: start from the SDK image (big, has compiler), copy project files, restore dependencies (cached layer), copy source code, build and publish. Stage 2: start from the runtime image (small, no compiler), copy the published output from stage 1. Result: production image has only the runtime and your app — no SDK, no source code, no build artifacts. This takes .NET images from ~800MB to ~80MB.

> [!faq]- "ENTRYPOINT vs CMD — when do you use which?"
> ENTRYPOINT sets the executable that always runs. CMD provides default arguments that can be overridden at runtime. Together: ENTRYPOINT defines what runs, CMD defines with what arguments. In practice for microservices, just use ENTRYPOINT with the full command — simpler, no ambiguity.

> [!faq]- "How do you handle Docker builds in CI on Kubernetes?"
> Docker-in-Docker (DinD) requires privileged mode — security risk. Kaniko builds images without a Docker daemon, runs unprivileged. If using self-hosted K8s runners, Kaniko is the way to go. BuildKit is another option — Docker's modern build engine with better caching and parallelism.
