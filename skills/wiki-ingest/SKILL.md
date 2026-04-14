---
name: wiki-ingest
description: "Ingest sources into the Obsidian wiki vault. Reads a source, extracts entities and concepts, creates or updates wiki pages, cross-references, and logs the operation. Supports files, URLs, and batch mode. Triggers on: ingest, process this source, add this to the wiki, read and file this, batch ingest, ingest all of these, ingest this url."
allowed-tools: Read Write Edit Glob Grep Bash WebFetch
---

# wiki-ingest: Source Ingestion

Read the source. Write the wiki. Cross-reference everything. A single source typically touches 8-15 wiki pages.

Every new wiki page MUST have these five frontmatter fields: `type`, `title`, `created` (today's date), `updated` (today's date), `tags`. Both `created` and `updated` are required on creation.

Every wikilink target MUST exactly match the destination page's `title` frontmatter field. Never link by filename slug, abbreviation, or paraphrase: `[[Context Window Management]]` works, `[[context-window-management]]` or `[[CWM]]` does not. Inconsistent link text breaks cross-references and orphans pages.

**Syntax standard**: Write all Obsidian Markdown using proper Obsidian Flavored Markdown. Wikilinks as `[[Note Name]]`, callouts as `> [!type] Title`, embeds as `![[file]]`, properties as YAML frontmatter. If the kepano/obsidian-skills plugin is installed, prefer its canonical obsidian-markdown skill for Obsidian syntax reference. Otherwise, follow the guidance in this skill.

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

## URL Ingestion

Trigger: user passes a URL starting with `https://`.

Steps:

1. **Fetch** the page using WebFetch.
2. **Clean** (optional): if `defuddle` is available (`which defuddle 2>/dev/null`), run `defuddle [url]` to strip ads, nav, and clutter. Typically saves 40-60% tokens. Fall back to raw WebFetch output if not installed.
3. **Derive slug** from the URL path (last segment, lowercased, spaces→hyphens, strip query strings).
4. **Save** to `.raw/articles/[slug]-[YYYY-MM-DD].md` with a frontmatter header:
   ```markdown
   ---
   source_url: [url]
   fetched: [YYYY-MM-DD]
   ---
   ```
5. Proceed with **Single Source Ingest** starting at step 2 (file is now in `.raw/`).

---

## Image / Vision Ingestion

Trigger: user passes an image file path (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`, `.avif`).

Steps:

1. **Read** the image file using the Read tool. Claude can process images natively.
2. **Describe** the image contents: extract all text (OCR), identify key concepts, entities, diagrams, and data visible in the image.
3. **Save** the description to `.raw/images/[slug]-[YYYY-MM-DD].md`:
   ```markdown
   ---
   source_type: image
   original_file: [original path]
   fetched: YYYY-MM-DD
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

### Core principle: compounding over duplication

The wiki is a persistent, compounding artifact. Every ingest must **prefer extending existing pages over creating new ones**. When a new source mentions an entity, concept, or theme that already has a page, extend that page with the new information and add the source to its `sources:` frontmatter list. Only create a new page when no existing page covers the subject.

A good ingest leaves the wiki denser, not wider.

### Steps

1. **Read** the source completely. Do not skim.
2. **Discuss** key takeaways with the user. Ask: "What should I emphasize? How granular?" Skip this step when running non-interactively (batch mode, headless trials, scheduled jobs, or when the user says "just ingest it").
3. **Survey existing coverage.** Read `wiki/hot.md` and `wiki/index.md`. For every entity and concept mentioned in the source, check whether a page already exists (scan index, then `glob wiki/entities/` and `wiki/concepts/`). Produce a mental map: `{entity/concept → exists? → page path}`. This survey is mandatory before any writes.
4. **Create** source summary in `wiki/sources/`. Use the full frontmatter schema from `skills/wiki/references/frontmatter.md` — universal fields plus source-specific (`source_type`, `author`, `date_published`, `url`, `confidence`, `key_claims`). The source summary must link to every entity and concept page this source touches (existing or to-be-created).
5. **Extend or create entity pages** for every person, org, product, and repo mentioned. One page per entity, never duplicates.
   - If the entity page **exists**: add a new `## From [[Source Title]]` section with the new information; append the source to the page's `sources:` frontmatter list; bump `updated`.
   - If it **does not exist**: create it with the canonical entity frontmatter (including `entity_type`, `role`, `first_mentioned`).
6. **Extend or create concept pages** for significant ideas and frameworks. Capture BOTH levels:
   (a) one umbrella concept per source named after the source's main subject or framework (e.g. "Claude Code Best Practices");
   (b) one concept per major capability area that groups related sub-topics (e.g. "Context Window Management" grouping "Clear Command", "Feedback Loop").
   The reader should be able to find the umbrella concept for any major theme in the source. Apply the same extend-over-create rule from step 5: existing concepts get new sections and the source added, not duplicate pages.
7. **Update sub-indexes** (`wiki/entities/_index.md`, `wiki/concepts/_index.md`, `wiki/sources/_index.md`) with new or renamed entries. If the vault uses `wiki/domains/`, update the relevant domain page too — otherwise tags on each page provide domain structure.
8. **Update** `wiki/overview.md` if the big picture changed.
9. **Update** `wiki/index.md`. Add entries for all new pages.
10. **Update** `wiki/hot.md` with this ingest's context.
11. **Append** to `wiki/log.md` (new entries at the TOP):
    ```markdown
    ## [YYYY-MM-DD] ingest | Source Title
    - Source: `.raw/articles/filename.md`
    - Summary: [[Source Title]]
    - Pages created: [[Page 1]], [[Page 2]]
    - Pages updated: [[Page 3]], [[Page 4]]
    - Key insight: One sentence on what is new.
    ```
12. **Check for contradictions.** If new info conflicts with existing pages, add `> [!contradiction]` callouts on both pages (see Contradictions section).
13. **Verify cross-linking.** Every page created or updated in this ingest must have at least one inbound wikilink from another page. Source summary links out to entities and concepts; entity and concept pages link back to the source summary and to each other where related. Pages with zero inbound links are malformed — fix before finishing.

---

## Batch Ingest

Trigger: user drops multiple files or says "ingest all of these."

Steps:

1. List all files to process. Confirm with user before starting.
2. Process each source following the single ingest flow. Defer cross-referencing between sources until step 3.
3. After all sources: do a cross-reference pass. Look for connections between the newly ingested sources.
4. Update index, hot cache, and log once at the end (not per-source).
5. Report: "Processed N sources. Created X pages, updated Y pages. Here are the key connections I found."

Batch ingest is less interactive. For 30+ sources, expect significant processing time. Check in with the user after every 10 sources.

---

## Context Window Discipline

Token budget matters. Distinguish **read budget** from **write/touch budget**:

- **Reads** (fully read 3–5 pages per ingest). Start with `wiki/hot.md`, then `wiki/index.md`, then the handful of pages directly relevant to this source. Use Grep to scan more pages without fully reading them.
- **Touches** (write or small-patch 8–15 pages per ingest). Source summary + several entity/concept pages + sub-indexes + log + hot cache. Touches do not require full re-reads — Edit on specific sections, Write only for new pages.
- Use PATCH / surgical Edit for existing pages. Never re-read an entire file just to update one field.
- Keep wiki pages short. 100–300 lines max. If a page grows beyond 300 lines, split it.
- If a page feels like it needs a full re-read before editing, your mental model of it is stale — Grep for the specific section first.

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

- Do not modify anything in `.raw/`. These are immutable source documents.
- Do not create duplicate pages. Always check the index and search before creating.
- Do not skip the log entry. Every ingest must be recorded.
- Do not skip the hot cache update. It is what keeps future sessions fast.
