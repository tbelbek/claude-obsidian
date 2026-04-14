---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Gerrit — Quick Reference

> [!info] How I've used it: Maintained the Gerrit instance at Volvo. Managed project configs, access control, labels, submit rules. Wrote the Python trigger daemon connecting stream-events to ZUUL CI. Handled silent SSH drops, duplicate builds, multi-repo changes.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Change-Based Workflow\|change workflow]] | patchset-based review, not branch-based like GitHub | [[#Labels & Review\|labels & review]] | Code-Review +2, Verified +1, custom labels |
| [[#Triggers & Events\|triggers]] | stream-events → Python daemon → ZUUL CI pipeline | [[#Access Control\|access control]] | project.config, group-based permissions |
| [[#Topic-Based Submissions\|topic submissions]] | multi-repo atomic merges via topic | [[#If I Had to Choose Today\|vs GitHub]] | GitHub for OSS/microservices, Gerrit for monorepo+compliance |

## HOW WE USED IT

At Volvo, I owned the Gerrit infrastructure — not just as a user but as the person who maintained the instance, managed project configs (`project.config` in `refs/meta/config`), and wrote the trigger daemon that connected Gerrit to the build system.

**What I maintained:**
- Project configurations for multiple repos — access control rules per repository (who can push, review, submit), label definitions (Verified -1/+1, Code-Review -2/+2), submit rules requiring both labels before merge
- Service accounts for the CI system with minimal permissions — label access only, no submit rights
- Release branch protection — blocked direct pushes, required full review flow

**What I built:**
- A Python daemon that connected to Gerrit's stream-events SSH interface, listened for `patchset-created` events, kicked off the ZUUL verification pipeline, and posted `Verified +1/-1` back via REST API with build log links
- Heartbeat mechanism (30-second ping) to detect silent SSH disconnects, with automatic reconnect and catch-up query for missed events
- Deduplication logic on change ID + patchset number to filter out internal Gerrit operations (auto-rebases) — cut the build queue by 30%
- `update_manifest.py` that queried the ZUUL REST API for successful builds and updated module versions automatically
- `handle-api-review-mr.py` that bridged Gerrit and GitLab — creating merge requests for API changes via GitLab API v4
- Topic-based submission configuration for multi-repo changes in automotive embedded

**Why Gerrit over GitHub:** Volvo uses Gerrit because it's the same tool Google uses for Android development. The change-based workflow (amend + push vs new commits) keeps a linear history which matters for embedded software traceability. The label system integrates tightly with CI — you can block submission until both human review and automated verification pass.

---

## Key Concepts

### What Gerrit Is
Gerrit is a web-based code review tool and Git hosting platform, widely used in large-scale software projects (Android, Chromium, Volvo). Unlike GitHub's branch-and-PR model, Gerrit uses a change-based workflow — each commit is a reviewable 'change' with patchsets (revisions). Best for: projects requiring strict review gatekeeping, fine-grained access control per branch/path, and integration with CI systems like ZUUL or Jenkins.

### Change-Based Workflow
- **Change** — A single unit of review. Unlike GitHub PRs (branch-based), Gerrit uses a change-based model where you amend and push to the same change.
- **Patchset** — Each push to a change creates a new patchset (revision). Reviewers review per-patchset.
- **Refs** — Gerrit stores patchsets as special Git refs: `refs/changes/XX/YYYY/Z`. Pipelines fetch these to build the exact code under review.

### Labels & Review
- **Code-Review** — Human review label. Typically -2 to +2. -2 blocks submission.
- **Verified** — CI result label. +1 (build passed) or -1 (build failed). Posted by the CI service account via REST API.
- **Submit rules** — Define what labels are required before a change can be merged. Example: Code-Review +2 AND Verified +1.

### Triggers & Events
- **stream-events** — Long-lived SSH connection emitting JSON events in real time. Events: `patchset-created`, `change-merged`, `comment-added`.
- **Webhooks** — Alternative to stream-events. Requires HTTP endpoint. Less real-time.
- **Heartbeat** — I added a 30-second heartbeat to detect silent SSH disconnects.
- **Dead-letter log** — Missed events during connection gaps. On reconnect, query REST API for unverified changes and re-queue.

### Access Control
- **project.config** — Per-repository access rules. Who can push, review, submit.
- **Service accounts** — CI bots with minimal permissions (label access only, no submit rights).
- **Release branches** — Block direct pushes, require full review flow.

### Topic-Based Submissions
- **Topics** — Group related changes across multiple repos. Submit them together.
- **Use case** — Platform API change + client update need to land simultaneously. Without topics, independent verification fails.

### If I Had to Choose Today
- **Instead of Gerrit** — I'd consider GitHub with required reviews and status checks. GitHub's PR model is more familiar to most developers, and GitHub Actions provides native CI integration. Gerrit's advantage is the granular label system and the amend-based workflow which keeps history cleaner, but the learning curve is steep. For embedded/automotive where linear history and strict gating matter, Gerrit is still the better fit.

## Sorulursa

> [!faq]- "How do you train developers who come from GitHub/GitLab?"
> The biggest adjustment is the amend-based workflow. In GitHub you add commits; in Gerrit you amend and force-push the same change. I created a cheat sheet: `git commit --amend` instead of `git commit`, `git review` instead of `git push`. Most developers get comfortable in a week. The harder part is the review culture — Gerrit's label system is more granular than GitHub's approve/reject.

> [!faq]- "How do you handle Gerrit at scale?"
> Cache configuration is critical — Gerrit caches Git objects, diff results, and account data. With many developers, cache misses cause slow page loads. We tuned cache sizes based on actual usage patterns. Also important: replication — Gerrit can replicate to read-only mirrors for CI systems, reducing load on the primary.

> [!faq]- "How did you handle Gerrit upgrades and maintenance?"
> Gerrit upgrades require downtime — the instance needs to be stopped, the database migrated, and restarted. We scheduled upgrades during weekends and announced them a week in advance. The trigger daemon detected the downtime via the heartbeat and queued events for reprocessing on reconnect. We also kept a rollback plan: previous Gerrit WAR file and database backup, tested restore procedure. Never had to use it, but it was documented.

> [!faq]- "Gerrit vs GitHub/GitLab — what's different practically?"
> Gerrit's change model: you amend and push to the same change, instead of adding commits to a PR branch. Review happens per-patchset, and the Verified/Code-Review labels are more granular than GitHub's approve/request-changes. Gerrit is also tightly integrated with CI — the `patchset-created` event + REST API for posting labels is a first-class workflow. The downside: the UX is worse than GitHub, the learning curve is steeper, and most developers coming from GitHub/GitLab need time to adjust to the amend-based workflow.

---

*[[00-dashboard]]*
