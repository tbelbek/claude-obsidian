---
name: wiki-ingest
description: "Ingest sources into the Obsidian wiki vault. Reads a source, extracts entities and concepts, creates or updates wiki pages, cross-references, and logs the operation. Supports files, URLs, and batch mode. Triggers on: ingest, process this source, add this to the wiki, read and file this, batch ingest, ingest all of these, ingest this url."
---

# wiki-ingest: Source Ingestion

Read the source. Write the wiki. Cross-reference everything. A single source typically touches 8-15 wiki pages.

**Syntax standard**: Write all Obsidian Markdown using proper Obsidian Flavored Markdown. Wikilinks as `[[Note Name]]`, callouts as `> [!type] Title`, embeds as `![[file]]`, properties as YAML frontmatter. If the kepano/obsidian-skills plugin is installed, prefer its canonical obsidian-markdown skill for Obsidian syntax reference. Otherwise, follow the guidance in this skill.

**Provenance rule**: Any document Claude writes **into `.raw/`** (a fetched
article, a defuddled page, an image description, a saved research note) MUST
include `ai-generated` in its frontmatter `tags:` list. This marks the doc as
Claude-authored so the **Triage Gate** can hold it for review instead of letting
it flow straight into the wiki — `ai-generated` files default to `pending`
(decision `skip`) until a human signs off. (This rule is about `.raw/` source
docs, not the `wiki/` pages ingest produces.)

---

## Transport (v1.7+)

Before mutating any vault file, consult `.vault-meta/transport.json` (auto-created by `bash scripts/detect-transport.sh`). Use the `preferred` transport per the fallback chain:

- **cli** — `obsidian-cli write "$VAULT" "$NOTE" < content.md` (or `append`, `property:set`); see [`skills/wiki-cli/SKILL.md`](../wiki-cli/SKILL.md)
- **mcp-obsidian** / **mcpvault** — `mcp__obsidian-vault__write_note` and friends; see [`skills/wiki/references/mcp-setup.md`](../wiki/references/mcp-setup.md)
- **filesystem** — Claude's `Write`/`Edit` tools with absolute vault-rooted paths (final floor; always works)

Full decision tree: [`wiki/references/transport-fallback.md`](../../wiki/references/transport-fallback.md).

---

## Mode awareness (v1.8+)

Before creating any new wiki page, consult the vault's methodology mode via `python3 scripts/wiki-mode.py route <type> "<name>"`. The router returns the vault-relative path where the page should be filed.

```bash
SRC_PATH=$(python3 scripts/wiki-mode.py route source "Karpathy 2025 LLM Wiki essay")
# generic:      wiki/sources/Karpathy-2025-LLM-Wiki-essay.md
# lyt:          wiki/notes/Karpathy-2025-LLM-Wiki-essay.md  (also update relevant MOC)
# para:         wiki/resources/incoming/Karpathy-2025-LLM-Wiki-essay.md
# zettelkasten: wiki/20260517123456-Karpathy-2025-LLM-Wiki-essay.md

ENT_PATH=$(python3 scripts/wiki-mode.py route entity "Andrej Karpathy")
CON_PATH=$(python3 scripts/wiki-mode.py route concept "Compounding Vault Pattern")
```

If `.vault-meta/mode.json` is absent, the router returns mode=generic paths (identical to v1.7 behavior). No special-casing needed in this skill.

Mode-specific follow-up:
- **LYT**: after filing the atomic note, update the relevant MOC (`wiki/mocs/<topic>-moc.md`) to link the new note. If no MOC exists for the topic, create one using `skills/wiki-mode/templates/lyt/moc-template.md`.
- **Zettelkasten**: filename already includes the timestamp ID. Populate the `id:` frontmatter field to match.
- **PARA**: new ingests land in `wiki/resources/incoming/` by default. Do NOT auto-guess the topic; leave in incoming/ for user review.

## Concurrency (v1.7+)

**Multi-writer is safe in v1.7.** The latent corruption bug from v1.6 — where two parallel sub-agents writing to the same page could silently trample each other — is closed by per-file advisory locking. Every wiki page write MUST be preceded by `wiki-lock acquire <path>`.

```bash
# Acquire — blocks (returns 75 EX_TEMPFAIL) if another writer holds the lock
if bash scripts/wiki-lock.sh acquire wiki/concepts/Foo.md; then
  # ... do the write via the §Transport-selected method ...
  bash scripts/wiki-lock.sh release wiki/concepts/Foo.md
else
  # rc=75: another writer is in flight. Retry once after 2s; if still held,
  # log to wiki/log.md and skip this page rather than overwrite.
  sleep 2
  bash scripts/wiki-lock.sh acquire wiki/concepts/Foo.md && {
    # write …
    bash scripts/wiki-lock.sh release wiki/concepts/Foo.md
  } || echo "skipped wiki/concepts/Foo.md (locked); logged to wiki/log.md"
fi
```

Properties:
- **Per-file granularity.** Locks key on `sha1(<vault-relative-path>)`; concurrent writes to DIFFERENT pages run in parallel.
- **Age-based staleness.** Default `STALE_AFTER_SEC=60`. A crashed holder unblocks in ≤60 seconds without manual intervention. See `scripts/wiki-lock.sh` header for the full semantics.
- **Cross-process release.** Release is `rm -f` (no PID match required). Skill authors are trusted to release locks they acquire; cross-skill release is allowed by design (a janitor running `wiki-lock clear-stale --max-age 0` is the canonical recovery path).
- **The PostToolUse hook now defers `git add` if any locks are currently held**, so the auto-commit doesn't fire mid-ingest and produce torn commits. See `hooks/hooks.json`.

`wiki-lock` is unconditional in v1.7+ — there is no feature gate, no fallback. Skills that don't acquire locks are racing against any other writer. The script is in core, not opt-in.

Sub-agent rule from v1.6 — *"Sub-agents MUST NOT call `scripts/allocate-address.sh`"* — is preserved (orchestrator still backfills addresses to keep the counter monotonic). The NEW rule is: *sub-agents MAY now write pages, but MUST acquire locks first.* See `agents/wiki-ingest.md`.

---

## Delta Tracking

Before ingesting any file, check `.raw/.manifest.json` to avoid re-processing unchanged sources.

```bash
# Check if manifest exists
[ -f .raw/.manifest.json ] && echo "exists" || echo "no manifest yet"
```

**Manifest format** (create if missing):
```json
{
  "sources": {
    ".raw/articles/article-slug-2026-04-08.md": {
      "hash": "abc123",
      "ingested_at": "2026-04-08",
      "pages_created": ["wiki/sources/article-slug.md", "wiki/entities/Person.md"],
      "pages_updated": ["wiki/index.md"]
    }
  }
}
```

**Before ingesting a file:**
1. Compute a hash: `md5sum [file] | cut -d' ' -f1` (or `sha256sum` on Linux).
2. Check if the path exists in `.manifest.json` with the same hash.
3. If hash matches, skip. Report: "Already ingested (unchanged). Use `force` to re-ingest."
4. If missing or hash differs, proceed with ingest.

**After ingesting a file:**
1. Record `{hash, ingested_at, pages_created, pages_updated}` in `.manifest.json`.
2. Write the updated manifest back.

Skip delta checking if the user says "force ingest" or "re-ingest".

---

## Triage Gate

Before a **batch ingest** (and optionally before a single ingest), run the
deterministic triage classifier so auto-generated session logs never get fanned
into the knowledge graph. Blindly ingesting an inbox full of `checkpoint-*` /
`conversation-review-*` logs is the classic "bulk-dump into RAG" failure mode:
it pollutes entity/concept pages and the hot cache with low-signal content.

```bash
python3 scripts/triage.py apply      # classify .raw/, write the `triage` ledger (manifest only)
python3 scripts/triage.py tag        # ALSO stamp triage/<class> into each file's frontmatter
python3 scripts/triage.py stats      # ingest / archive / skip counts
python3 scripts/triage.py ingestable # one path per line, decision == ingest
```

Use `apply` for an invisible manifest-only ledger, or `tag` when you want the
triage state **visible and filterable in Obsidian** as a frontmatter tag. `tag`
is path-preserving — it adds one `triage/<class>` tag and nothing else; it never
moves, renames, or deletes a file.

`triage.py` classifies every `.raw/` file and records the verdict in
`.raw/.manifest.json` under a top-level **`triage`** key — a logical-tag ledger
(each entry also carries `ai_generated: true|false`). Source files stay immutable
(the verdict lives in the manifest, never written into the source). Classification
precedence, highest first:

| Precedence | Tag | Matches | `decision` | What ingest does |
|-----------|-----|---------|-----------|------------------|
| 1 (override) | per override | frontmatter `triage: …` | as stated | Honors the explicit human call |
| 2 | `triage/log` | `checkpoint-*`, `conversation-review-*` | `archive` | **Skip** — never ingest, never add to `sources` |
| 3 | `triage/pending` | `ai-generated` frontmatter tag | `skip` | **Hold for review** — Claude authored it; awaits human sign-off |
| 4 (default) | `triage/reference` | human-dropped articles / project notes | `ingest` | Process normally |

**Gate rules:**
1. Ingest **only** files where `decision == "ingest"` (use `triage.py ingestable`).
2. **Never** record an `archive`/`skip` file in the manifest `sources` map — that
   map means "ingested", and a held file there would suppress it from a future
   intentional pass. The `triage` ledger is the only place their state lives.
3. **`ai-generated` ⇒ pending:** anything Claude wrote into `.raw/` is held for
   review, so AI-authored content never auto-flows into the wiki. To ingest one,
   sign off by adding `triage: ingest` to its frontmatter (override wins).
4. Run `triage.py` again after dropping new sources — it is idempotent.

---

## URL Ingestion

Trigger: user passes a URL starting with `https://`.

Steps:

1. **Fetch** the page using WebFetch.
2. **Clean** (optional): if `defuddle` is available (`which defuddle 2>/dev/null`), run `defuddle [url]` to strip ads, nav, and clutter. Typically saves 40-60% tokens. Fall back to raw WebFetch output if not installed.
3. **Derive slug** from the URL path (last segment, lowercased, spaces→hyphens, strip query strings).
4. **Save** to `.raw/articles/[slug]-[YYYY-MM-DD].md` with a frontmatter header (Claude
   authored this `.raw/` doc, so it carries `ai-generated` per the Provenance rule):
   ```markdown
   ---
   source_url: [url]
   fetched: [YYYY-MM-DD]
   tags:
     - ai-generated
   ---
   ```
5. Proceed with **Single Source Ingest** starting at step 2 (file is now in `.raw/`).

---

## Image / Vision Ingestion

Trigger: user passes an image file path (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`, `.avif`).

Steps:

1. **Read** the image file using the Read tool. Claude can process images natively.
2. **Describe** the image contents: extract all text (OCR), identify key concepts, entities, diagrams, and data visible in the image.
3. **Save** the description to `.raw/images/[slug]-[YYYY-MM-DD].md` (Claude-authored
   `.raw/` doc → carries `ai-generated` per the Provenance rule):
   ```markdown
   ---
   source_type: image
   original_file: [original path]
   fetched: YYYY-MM-DD
   tags:
     - ai-generated
   ---
   # Image: [slug]

   [Full description of image contents, transcribed text, entities visible, etc.]
   ```
4. Copy the image to `_attachments/images/[slug].[ext]` if it's not already in the vault.
5. Proceed with **Single Source Ingest** on the saved description file.

Use cases: whiteboard photos, screenshots, diagrams, infographics, document scans.

---

## Single Source Ingest

Trigger: user drops a file into `.raw/` or pastes content.

Steps:

1. **Read** the source completely. Do not skim.
2. **Discuss** key takeaways with the user. Ask: "What should I emphasize? How granular?" Skip this if the user says "just ingest it."
3. **Create** source summary in `wiki/sources/`. Use the source frontmatter schema from `references/frontmatter.md`. Assign an address per the **Address Assignment** section below.
4. **Create or update** entity pages for every person, org, product, and repo mentioned. One page per entity. Assign addresses to new entity pages.
5. **Create or update** concept pages for significant ideas and frameworks. Assign addresses to new concept pages.
6. **Update** relevant domain page(s) and their `_index.md` sub-indexes.
7. **Update** `wiki/overview.md` if the big picture changed.
8. **Update** `wiki/index.md`. Add entries for all new pages.
9. **Update** `wiki/hot.md` with this ingest's context.
10. **Append** to `wiki/log.md` (new entries at the TOP):
    ```markdown
    ## [YYYY-MM-DD] ingest | Source Title
    - Source: `.raw/articles/filename.md`
    - Summary: [[Source Title]]
    - Pages created: [[Page 1]], [[Page 2]]
    - Pages updated: [[Page 3]], [[Page 4]]
    - Key insight: One sentence on what is new.
    ```
11. **Check for contradictions.** If new info conflicts with existing pages, add `> [!contradiction]` callouts on both pages.

---

## Batch Ingest

Trigger: user drops multiple files or says "ingest all of these."

Steps:

1. **Run the Triage Gate first** (`python3 scripts/triage.py apply`). Take the
   `ingestable` set as your work-list; report the archive/skip counts so the
   user sees what's being held back. Confirm with user before starting.
2. Process each source following the single ingest flow. Defer cross-referencing between sources until step 3.
3. After all sources: do a cross-reference pass. Look for connections between the newly ingested sources.
4. Update index, hot cache, and log once at the end (not per-source).
5. Report: "Processed N sources. Created X pages, updated Y pages. Here are the key connections I found."

Batch ingest is less interactive. For 30+ sources, expect significant processing time. Check in with the user after every 10 sources.

---

## Context Window Discipline

Token budget matters. Follow these rules during ingest:

- Read `wiki/hot.md` first. If it contains the relevant context, don't re-read full pages.
- Read `wiki/index.md` to find existing pages before creating new ones.
- Read only 3-5 existing pages per ingest. If you need 10+, you are reading too broadly.
- Use PATCH for surgical edits. Never re-read an entire file just to update one field.
- Keep wiki pages short. 100-300 lines max. If a page grows beyond 300 lines, split it.
- Use search (`/search/simple/`) to find specific content without reading full pages.

---

## Contradictions

> [!note] Custom callout dependency
> The `[!contradiction]` callout type used below is a **custom callout** defined in `.obsidian/snippets/vault-colors.css` (auto-installed by `/wiki` scaffold). It renders with reddish-brown styling and an alert-triangle icon when the snippet is enabled. If the snippet is missing, Obsidian falls back to default callout styling, so the page still works without the visual flourish. See [[skills/wiki/references/css-snippets.md]] for the four custom callouts (`contradiction`, `gap`, `key-insight`, `stale`).

When new info contradicts an existing wiki page:

On the existing page, add:
```markdown
> [!contradiction] Conflict with [[New Source]]
> [[Existing Page]] claims X. [[New Source]] says Y.
> Needs resolution. Check dates, context, and primary sources.
```

On the new source summary, reference it:
```markdown
> [!contradiction] Contradicts [[Existing Page]]
> This source says Y, but existing wiki says X. See [[Existing Page]] for details.
```

Do not silently overwrite old claims. Flag and let the user decide.

---

## What Not to Do

- **Source files under `.raw/` are immutable — content and path.** Do not edit the body of files users drop there (articles, transcripts, images), and never move, rename, or delete them. The `.raw/.manifest.json` delta tracker and its `address_map` (DragonScale Mechanism 2) are maintained by `wiki-ingest`. **One narrow, opt-in exception:** `triage.py tag` may add a single `triage/<class>` tag to a file's frontmatter (and only that) so the triage state is visible/filterable in Obsidian — still no path change, no rename, no delete, no body edit. Everything else under `.raw/` is read-only source content.
- Do not create duplicate pages. Always check the index and search before creating.
- Do not skip the log entry. Every ingest must be recorded.
- Do not skip the hot cache update. It is what keeps future sessions fast.

---

## Address Assignment (DragonScale Mechanism 2 MVP)

**Opt-in feature**. DragonScale address assignment runs only if `scripts/allocate-address.sh` is present AND `.vault-meta/` exists. Otherwise, skip this entire section and proceed with ingest normally.

**Feature detection (run at start of every ingest)**:

```bash
if [ -x ./scripts/allocate-address.sh ] && [ -d ./.vault-meta ]; then
  DRAGONSCALE_ADDRESSES=1
else
  DRAGONSCALE_ADDRESSES=0
fi
```

When `DRAGONSCALE_ADDRESSES=0`, pages are created without an `address:` frontmatter field, and `wiki-lint`'s Address Validation section is skipped entirely (missing addresses are not flagged in any severity). This preserves default plugin behavior for vaults that have not adopted DragonScale.

When `DRAGONSCALE_ADDRESSES=1`, proceed with the rest of this section.

---

Every **newly created non-meta wiki page** gets a stable address in its frontmatter:

```yaml
address: c-000042
```

Format: `c-<6-digit-counter>`. The `c-` prefix stands for "creation-order counter." Zero-padded.

Rollout baseline: **2026-04-23** (Phase 2 ship date). Pages with `created:` >= this date are post-rollout and MUST have an address (unless excluded below). Pages with `created:` earlier are legacy-exempt until a deliberate backfill pass assigns `l-NNNNNN` addresses.

### Required tool: `scripts/allocate-address.sh`

Address allocation is delegated to an atomic Bash helper. The helper uses `flock` on `.vault-meta/.address.lock` to prevent read-use-increment races and recovers the counter by scanning existing frontmatter if the counter file is missing.

```bash
ADDR=$(./scripts/allocate-address.sh)
# ADDR is now e.g. "c-000042"; counter is already incremented
```

**CRITICAL**: never use the Write or Edit tool on `.vault-meta/address-counter.txt`. That would fire the PostToolUse hook, which runs `git add wiki/ .raw/` and can accidentally commit unrelated pending wiki changes under a generic message. Counter mutation is **only** permitted through the helper script (Bash tool).

### Helper modes

- `./scripts/allocate-address.sh` — atomically reserves and returns the next address.
- `./scripts/allocate-address.sh --peek` — prints the next value without reserving (safe, read-only).
- `./scripts/allocate-address.sh --rebuild` — recomputes the counter from the highest observed `c-NNNNNN` in existing frontmatter. Never resets to 1 silently if pages already have addresses. Run this if the counter file is suspected corrupt.

### Assignment procedure (per new page)

1. Before writing a new non-meta page, call `./scripts/allocate-address.sh` and capture the output.
2. Include `address: c-XXXXXX` in the page's frontmatter.
3. Record the path-to-address mapping in `.raw/.manifest.json` under a new top-level key `address_map` (see schema below).

### `address_map` in `.raw/.manifest.json`

```json
{
  "sources": { ... },
  "address_map": {
    "wiki/concepts/Example.md": "c-000042",
    "wiki/entities/Another.md": "c-000043"
  }
}
```

On re-ingest of the same source (whether by `--force` or a changed hash), always consult `address_map` first. If the target page path has a prior address, REUSE it. Do not allocate a new one.

On a page rename, the skill must update the `address_map` key (old path -> new path) while preserving the address value.

### Exclusions (do NOT assign an address to)

- Meta files: `_index.md`, `index.md`, `log.md`, `hot.md`, `overview.md`, `dashboard.md`, `dashboard.base`, `Wiki Map.md`, `getting-started.md`.
- Fold pages under `wiki/folds/` (they use their own deterministic `fold_id`).
- Pre-rollout legacy pages (`created:` < 2026-04-23). Legacy pages get `l-NNNNNN` addresses only via a deliberate backfill operation.

### Idempotency rules

- If a page being (re)written already has an `address:` field in its current content, REUSE it. Do not allocate a new one.
- If a source is re-ingested and `address_map` has a mapping for the target path, reuse that mapping.
- If the source has been ingested before AND the target page has no address AND the page `created:` date is post-rollout, allocate an address and record it. This covers the case where an older ingest produced a page before Phase 2 rollout; the rollout cutoff still applies (pages dated pre-2026-04-23 stay legacy).

### Concurrency policy

- **Single-writer only** in Phase 2. Do not run parallel ingests from multiple Claude sessions or sub-agents that assign addresses. The `flock` in the helper prevents counter corruption but does not serialize page writes themselves.
- Sub-agents (codex, general-purpose) that are dispatched for research or review MUST NOT call the allocator. They are read-only in this respect.
- Multi-writer support is a deferred feature.

### Batch ingest

Assign addresses sequentially during single-source-ingest for each source. Do not pre-reserve a block of counter values. The helper is cheap (one lock, one integer read/write).

---

## How to think (10-principle mapping)

When working on this skill, apply the 10-principle loop. See [`skills/think/SKILL.md`](../think/SKILL.md) for the canonical framework.

| # | Principle | Application here |
|---|-----------|-------------------|
| 1 | OBSERVE (ext) | Read the source file completely before extracting anything. No shortcuts on long sources. |
| 2 | OBSERVE (int) | Am I biased toward the source's framing? Where do my disagreements live? Note them as contradiction callouts. |
| 3 | LISTEN | The user's source-selection intent — what made THIS source worth ingesting, and what is the user hoping to extract? |
| 4 | THINK | Which entities deserve pages? Which concepts? What cross-references? What contradictions with existing pages? |
| 5 | CONNECT (lat) | This source's claims vs other sources already in the wiki. Contradictions are the highest-signal finding. |
| 6 | CONNECT (sys) | `wiki-mode.py route` for paths + `wiki-lock.sh` for safety + index/log/hot for consumer visibility. |
| 7 | FEEL | A page that compounds — useful in 6 months, not just today. Skip filler; favor synthesis over transcription. |
| 8 | ACCEPT | Not every claim is wiki-worthy. Editorial judgment is part of ingest, not a bug to remove. |
| 9 | CREATE | Source + entity + concept pages with full frontmatter; cross-references; contradiction callouts where needed. |
| 10 | GROW | Contradictions found mid-ingest are the most valuable wiki signal. File them as questions for follow-up, not silently. |
