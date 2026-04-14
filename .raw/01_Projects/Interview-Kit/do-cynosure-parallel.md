---
tags:
  - interview-kit
  - interview-kit/devops
up: [[do-volvo]]
---

*[[00-dashboard|Home]] > [[11-pillar-devops|DevOps]] > [[do-volvo|VOLVO CARS]] > CYNOSURE — Parallelization*

# CYNOSURE — Parallelization

> [!warning] **Soru:** "How did you optimize build times?"

At Volvo, we had multiple build targets — QNX ARM, Linux x86, Android Automotive. Cynosure was Volvo's internal build and product tracking system. I wrote `notify-on-messagebus.py` that posted ProductCreated and ActivityCreated events to Cynosure's message bus at `core.messagebus.cynosure.volvocars.biz`, and queried Cynosure's StateDB to resolve SHA1 hashes to product instance IDs. The first version of my orchestration script ran all targets one after another. A full build took over 40 minutes. Developers were pushing changes and waiting nearly an hour for verification feedback.

Understanding build pipeline performance under real resource constraints turned out to be the actual challenge. I tried the obvious fix: run all builds in parallel. It worked for about a day, then we started getting OOM kills. Some targets — especially the QNX ones — needed a lot of memory during the linking phase. Running all of them at the same time on the same machine crashed the build server.

I also wrote `build-vbfs.py` for building VBF (Vehicle Boot File) images for ARM-based QNX targets, integrating with the CS Tools manifest. Module change detection was handled by `detect-changed-modules.py` which compared manifest versions to identify what needed rebuilding.

The fix was smarter batching. I grouped targets by resource requirements: the lighter ones (Linux x86, some small utility builds) ran in parallel first, then the heavy ones (QNX ARM with its large linking step) ran after. Each target still ran in its own Docker container with the toolchain pre-installed, so they were isolated. Total build time went from 40+ minutes down to about 15 minutes.

I bring this up under DevOps because build time directly affects developer feedback loops — a 40-minute build means developers context-switch, a 15-minute build means they wait and stay focused.

## Sorulursa

> [!faq]- "Why not just get bigger build servers?"
> We tried. But the heavy targets needed 16GB+ of RAM each during linking. Running 5 of them in parallel would need 80GB+ just for linking. The build servers we had couldn't handle that, and getting bigger machines approved takes months in a large organization. Batching was the practical solution.

> [!faq]- "How did you determine the resource requirements?"
> I ran each target individually and monitored memory and CPU usage with `top` and `docker stats`. Some targets peaked at 2GB, others at 16GB. I wrote the peak values into the manifest file next to each target and the orchestration script used those to decide the batch groups.

> [!faq]- "Why Docker containers per target?"
> Each target needed a different cross-compilation toolchain. Without containers, you'd have to install all toolchains on the same machine and manage conflicts. With containers, each target had its own image with the exact toolchain version pre-installed. Also made it reproducible — same container, same result, regardless of which build server picked it up. We used a custom Docker image hosted in Volvo's Artifactory (cs-docker-lts.ara-artifactory.volvocars.biz) that included CS Tools, the CSP SDK, and the HP Toolkit. Ansible playbooks handled test execution on emulators — `start_csp_emulators.sh` would spin up CSP emulators, and Ansible orchestrated the test campaigns against them.

> [!faq]- "Technical: Cross-compilation for embedded targets"
> Cross-compilation means building software on one platform (x86 Linux) to run on another (ARM QNX). Each target needs its own toolchain: compiler, linker, libraries. QNX uses its own POSIX-like OS with a microkernel architecture — the QNX Neutrino RTOS. Android Automotive (AAOS) uses the Android NDK for native code. The Cynosure build system abstracted these differences, but you still needed to understand the target: QNX has different threading primitives, AAOS has different filesystem layouts, and the linker flags are completely different. Mistakes show up as cryptic linker errors, not compile errors.

> [!faq]- "How did you monitor build resource usage?"
> Docker stats for real-time container metrics (CPU, memory, disk I/O) and `top` inside the container for process-level detail. The linking phase was the memory spike — the linker loads all object files into memory to resolve symbols. For QNX ARM targets with large codebases, this could peak at 16GB+. I logged peak memory for each target and used that to set the batch groups. We also set `--memory` limits on Docker containers so a runaway build would get OOMKilled rather than taking down the host and killing other builds.

> [!faq]- "If you had to replace Cynosure and ZUUL with mainstream tools, what would you use?"
> For ZUUL (CI orchestration), I'd use **GitHub Actions** or **GitLab CI** with reusable workflows. ZUUL's strength is its gating pipeline — changes can't merge until they pass verification together with other queued changes. GitHub Actions doesn't have this natively, but you can approximate it with merge queues and required status checks. For Cynosure (product tracking and message bus), I'd use a combination of **JFrog Artifactory** for artifact management and **Kafka** for build event streaming. Cynosure's StateDB could be replaced with a simple PostgreSQL database tracking product instances and their metadata. The custom message bus could be replaced with Kafka topics for build events. The key advantage of Cynosure was that everything was integrated in one system — replacing it means gluing 3-4 tools together.

> [!faq]- "Could you use distributed builds instead of batching?"
> Tools like distcc or Icecream can distribute compilation across machines, but linking is still single-machine — you can't distribute the linker. Since our bottleneck was linking, not compilation, distributed builds wouldn't have helped much. The batching approach was the right trade-off for our situation.

---

*[[00-dashboard|Home]] > [[11-pillar-devops|DevOps]] > [[do-volvo|VOLVO CARS]]*
