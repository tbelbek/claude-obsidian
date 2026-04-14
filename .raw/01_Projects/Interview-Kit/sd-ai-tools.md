---
tags:
  - interview-kit
  - interview-kit/software-dev
up: [[sd-combination]]
---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]] > [[sd-combination|COMBINATION AB]] > AI TOOLS*

# AI TOOLS — Cursor + Claude Code

> [!warning] **Soru:** "Do you use AI tools?" / "How do you use AI in development?"

I use Cursor and Claude Code every day. Not as a novelty — as part of my actual development workflow. Using AI tools effectively is an engineering skill in itself — [[ref-ai-tooling#Risks — Where AI Makes Things Worse|knowing when they help and when they make things worse]] matters just as much as knowing the tools exist. Over time I've built specific habits around when to use which tool and, more importantly, when NOT to trust the output.

## My Daily Workflow

**Starting a new feature:**
I write the interface first — the function signatures, the types, the contracts. This is the thinking part and I do it myself. Then I use Cursor to fill in the implementation. It sees the types and the tests I've written, so it usually gets 80% right. I review every line, fix the remaining 20%, and run the tests.

**Writing tests:**
I write the test names and edge cases myself — that's where the domain knowledge lives. Then I let Cursor generate the test bodies. A test like `ShouldRejectOrderWhenStockIsZero` — I name it, Cursor writes the arrange-act-assert. I check the assertions make sense. This is where AI saves the most time for me.

**Refactoring:**
When I need to rename a concept across 15 files, or extract a method and update all callers, I use Claude Code. It reads the whole project, plans the changes, and shows me a diff. I review the diff as I would a PR — does it miss anything? Does it change behavior? Then I approve. For single-file refactoring, Cursor is enough.

**Debugging:**
AI is almost useless for real debugging. A race condition, a data corruption bug, a timing issue — the AI doesn't know your system's runtime behavior. I debug the old-fashioned way: reproduce, isolate, fix. Where AI helps is after I've found the bug — "generate a regression test for this scenario" is a good prompt.

**Code review:**
When reviewing someone else's PR, I sometimes paste a complex method into Cursor and ask "what could go wrong here?" It catches things like missing null checks or resource leaks. But it misses business logic errors because it doesn't understand the domain. It's a second pair of eyes, not a replacement for thinking.

## What I've Learned NOT to Do

**Don't use AI for security code.** Authentication, authorization, input validation, crypto — I write these by hand. AI generates plausible-looking security code that has subtle flaws. A JWT validation that doesn't check expiry. An input sanitizer that misses edge cases. Too risky.

**Don't let AI make architecture decisions.** It can list pros and cons of different approaches, but it doesn't know your team's skills, your infra constraints, or your maintenance budget. Architecture is a people decision, not a code decision.

**Don't skip the review.** AI is confident even when it's wrong. It will generate a function that looks perfect, passes the obvious tests, and has a subtle bug that shows up in production. Every line gets reviewed as if a junior developer wrote it.

**Don't use AI as a crutch.** If I can't explain why the code works, I rewrite it by hand. Blindly accepting AI output makes you dependent and stops your growth as an engineer. I still write code from scratch regularly to stay sharp.

I bring this up under software development because AI tools are changing how code gets written, and having a disciplined workflow around them is becoming as important as knowing the language itself.

## Cursor vs Claude Code — When I Use Which

| Task | Tool | Why |
|------|------|-----|
| Inline code completion | Cursor | Sees current file context, fast |
| Single-file refactoring | Cursor | Composer mode, keeps context |
| Multi-file refactoring | Claude Code | Reads whole project, plans across files |
| Test generation | Cursor | Good at pattern matching from existing tests |
| Architecture exploration | Claude Code | Can grep, read, and summarize across codebase |
| Documentation | Claude Code | Reads code and generates docs in one pass |
| Debugging | Neither | AI doesn't know runtime behavior |
| Security code | Neither | Too risky to trust |

## Sorulursa

> [!faq]- "How do you make sure AI-generated code is safe to merge?"
> Same rules as any code: it needs tests, it needs review, and I need to understand it. My workflow is: write the test first (or at least the test name), let AI generate the implementation, run the test, review the code. If the test passes but I can't explain why the implementation works, I rewrite it. I also never let AI touch security-critical paths — auth, validation, crypto.

> [!faq]- "How much faster are you with these tools?"
> Depends on the task. Boilerplate and tests: 3-4x faster. Complex features: maybe 20% — AI handles the boring parts so I focus on the hard parts. Debugging and architecture: no speed gain, sometimes slower because I have to verify AI suggestions. Average across a week: roughly 30-40% productivity boost.

> [!faq]- "Cursor vs GitHub Copilot — why Cursor?"
> Copilot does inline completion — predicts the next line. Cursor does that plus full-file understanding, multi-file Composer mode, and a chat interface for code exploration. For simple autocomplete they're similar. For refactoring, understanding unfamiliar code, and making changes across files, Cursor is much better. Claude Code fills a different niche — it's a CLI agent for project-wide tasks, not an editor plugin.

> [!faq]- "What's your biggest concern with AI tools in development?"
> Engineers who stop thinking. If you accept every suggestion without understanding it, you're building a codebase nobody understands. When that code breaks at 2 AM, the AI won't be on call — you will. The tool should make you faster, not dumber. I make a point of writing some code from scratch every week, reading documentation instead of asking AI, and understanding the "why" behind patterns, not just copy-pasting the "what."

> [!faq]- "How do you handle AI in a team context?"
> We agreed on rules: AI-generated code gets the same review as human code — no shortcuts. Tests are required, same as always. If someone submits AI-generated code they can't explain, it gets sent back. We also share useful prompts and patterns — if I find a good way to use Cursor for test generation, I share it with the team. The goal is raising the floor, not creating dependency.

> [!faq]- "Technical: How does the context window affect code quality?"
> The more context the AI has, the better the output. Cursor sends the current file plus related files (imports, types). Claude Code can read the entire project. This is why Cursor is better for single-file work and Claude Code is better for cross-project tasks. The practical limit: if your project is huge and the AI can only see part of it, it will generate code that conflicts with parts it can't see. For large codebases, I give Claude Code specific directories to focus on rather than the whole repo.

---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]] > [[sd-combination|COMBINATION AB]]*
