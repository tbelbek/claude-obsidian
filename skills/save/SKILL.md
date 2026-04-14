---
name: save
description: >
  Save the current conversation, answer, or insight into the Obsidian wiki vault as a
  structured note. Analyzes the chat, determines the right note type, creates frontmatter,
  files it in the correct wiki folder, and updates index, log, and hot cache.
  Triggers on: "save this", "save that answer", "/save", "file this",
  "save to wiki", "save this session", "file this conversation", "keep this",
  "save this analysis", "add this to the wiki".
allowed-tools: Read Write Edit Glob Grep
---

# save: File Conversations Into the Wiki

Good answers and insights shouldn't disappear into chat history. This skill takes what was just discussed and files it as a permanent wiki page.

The wiki compounds. Save often.

---

## Note Type Decision

Determine the best type from the conversation content:

Types match the canonical schema (`skills/wiki/references/frontmatter.md`). Folder = `type` (never diverge).

| Type | Folder | Use when |
|------|--------|---------|
| question | wiki/questions/ | Multi-step analysis, comparison, or answer to a specific question (whether synthesized in-chat or prompted) |
| concept | wiki/concepts/ | Explaining or defining an idea, pattern, or framework |
| source | wiki/sources/ | Summary of external material discussed in the session |
| comparison | wiki/comparisons/ | Side-by-side analysis of two or more things |
| meta | wiki/meta/ | Decisions, session summaries, dashboards, lint reports |

If the user specifies a type, use that. If not, pick the best fit. When in doubt, use `question`. Long-form synthesis answers are still `type: question` — "synthesis" is a style, not a type.

---

## Save Workflow

1. **Scan** the current conversation. Identify the most valuable content to preserve.
2. **Ask** (if not already named): "What should I call this note?" Keep the name short and descriptive.
3. **Determine** note type using the table above.
4. **Extract** all relevant content from the conversation. Rewrite it in declarative present tense (not "the user asked" but the actual content itself).
5. **Create** the note in the correct folder with full frontmatter.
6. **Collect links**: identify any wiki pages mentioned in the conversation. Add them to `related` in frontmatter.
7. **Update** `wiki/index.md`. Add the new entry at the top of the relevant section.
8. **Append** to `wiki/log.md`. New entry at the TOP:
   ```
   ## [YYYY-MM-DD] save | Note Title
   - Type: [note type]
   - Location: wiki/[folder]/Note Title.md
   - From: conversation on [brief topic description]
   - Key insight: [one sentence — what is new or why this is worth keeping]
   ```
9. **Update** `wiki/hot.md` to reflect the new addition.
10. **Confirm**: "Saved as [[Note Title]] in wiki/[folder]/."

---

## Frontmatter Template

Minimum universal fields (match `skills/wiki/references/frontmatter.md`):

```yaml
---
type: <question|concept|source|comparison|meta>
title: "Note Title"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - <relevant-tag>
status: developing
related:
  - "[[Any Wiki Page Mentioned]]"
sources:
  - ".raw/articles/source-if-applicable.md"
---
```

Note: `sources` holds path strings, not wikilinks. Files under `.raw/` are not linkable via `[[...]]`.

For `type: question`, add the question-specific fields from the canonical schema (`question`, `answer_quality: draft|solid|definitive`).

For meta pages, add `meta_type: decision|session|dashboard|lint-report` plus any type-specific fields (e.g. `decision_date` for decisions).

---

## Writing Style

- Declarative, present tense. Write the knowledge, not the conversation.
- Not: "The user asked about X and Claude explained..."
- Yes: "X works by doing Y. The key insight is Z."
- Include all relevant context. Future sessions should be able to read this page cold.
- Link every mentioned concept, entity, or wiki page with wikilinks.
- Cite sources where applicable: `(Source: [[Page]])`.

---

## What to Save vs. Skip

Save:
- Non-obvious insights or synthesis
- Decisions with rationale
- Analyses that took significant effort
- Comparisons that are likely to be referenced again
- Research findings

Skip:
- Mechanical Q&A (lookup questions with obvious answers)
- Setup steps already documented elsewhere
- Temporary debugging sessions with no lasting insight
- Anything already in the wiki

If it's already in the wiki, update the existing page instead of creating a duplicate.
