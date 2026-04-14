---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# AI-Assisted Development — Quick Reference

> [!info] How I've used it: Daily workflow with Cursor and Claude Code at Combination. Built specific habits around when each tool helps, when it hurts, and how to keep engineers growing instead of becoming dependent.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#Cursor vs Claude Code — When I Use Which\|Cursor vs Claude Code]] | Cursor=inline edit, Claude Code=multi-file refactor | [[#Workflow Integration — My Rules\|my rules]] | tests first, review everything, no AI for security |
| [[#Benefits — Where AI Actually Helps\|benefits]] | 30-40% productivity boost, boilerplate, test gen | [[#Risks — Where AI Makes Things Worse\|risks]] | hallucinations, dependency, skipping understanding |
| [[#Team Context — How We Handle It\|team context]] | engineers must understand what AI generates | [[#Measuring Impact\|measuring impact]] | velocity, quality, learning — not just speed |

## HOW WE USE IT

I use two tools daily — **Cursor** (AI-powered code editor) and **Claude Code** (CLI-based AI agent). Each serves a different purpose, and knowing which to use when is the real skill. 

**The short version:** I write the thinking parts (interfaces, types, contracts, architecture decisions) myself. AI handles the mechanical parts (boilerplate, test bodies, repetitive patterns). Every line of AI output gets reviewed as if a junior developer wrote it.

---

### What AI-Assisted Development Is

AI-assisted development uses large language models (Cursor, Claude Code, GitHub Copilot) to accelerate coding — generating boilerplate, writing tests, explaining unfamiliar code, refactoring, and debugging. The key is knowing when to trust it and when to verify: AI excels at repetitive patterns and boilerplate, but struggles with domain-specific logic, security-critical code, and novel architecture decisions. Used well, it's a 30-40% productivity boost. Used carelessly, it introduces subtle bugs and erodes understanding.

## Key Concepts

### Benefits — Where AI Actually Helps
- **Boilerplate code** — CRUD endpoints, mapping code, DTOs. Pattern is clear, typing is the bottleneck. AI saves 3-4x time here.
- **Test generation** — I name the test and define edge cases. AI writes the arrange-act-assert body. Good at pattern-matching from existing tests.
- **Refactoring** — Renaming across files, extracting methods, changing signatures. AI sees full context and makes fewer mistakes than find-and-replace.
- **Code understanding** — When new to a part of the codebase, asking AI to explain a method is faster than reading 200 lines of unfamiliar code.
- **Documentation** — Generating API docs, README updates, onboarding guides from existing code.

### Risks — Where AI Makes Things Worse
- **Security code** — Auth, validation, crypto. AI generates plausible-looking code with subtle flaws. A JWT validation that doesn't check expiry. An input sanitizer that misses edge cases. Too risky.
- **Complex business logic** — AI doesn't understand your domain. It generates code that looks correct but violates business rules nobody wrote down.
- **Architecture decisions** — AI can list pros and cons but doesn't know your team's skills, infra constraints, or maintenance budget. Architecture is a people decision.
- **Dependency on AI** — If you can't explain why the code works, you can't debug it at 2 AM. Engineers who only accept AI output stop growing.
- **Confident hallucinations** — AI is confident even when wrong. It will generate a function that passes obvious tests and has a subtle bug that shows up in production.

### Workflow Integration — My Rules
- **Write tests first** — Gives you a safety net for AI-generated code. If the test passes and you understand the implementation, it's good.
- **Review everything** — Every line, as if a junior wrote it. No "AI generated it, it's probably fine."
- **Don't use AI for security paths** — Auth, validation, crypto. Write by hand.
- **Keep learning** — Write code from scratch regularly. Read docs instead of asking AI. Understand the "why" behind patterns.
- **Share patterns in the team** — If I find a good way to use Cursor for test generation, I share it. Raise the floor, don't create dependency.

### Team Context — How We Handle It
- AI-generated code gets the same review as human code. No shortcuts.
- Tests required, same as always.
- If someone submits AI-generated code they can't explain, it gets sent back.
- Shared prompts and patterns — what works for one person helps everyone.

### Cursor vs Claude Code — When I Use Which
- **Cursor** — In-editor. Single-file completion, refactoring, test scaffolding. Sees current file + imports. Fast for focused tasks.
- **Claude Code** — CLI agent. Multi-file changes, architecture exploration, project-wide search, documentation generation. Reads the whole project. Better for tasks that span many files.
- **Neither** — Debugging (AI doesn't know runtime behavior), security code, architecture decisions.

### Measuring Impact
- **Boilerplate/tests:** 3-4x faster
- **Complex features:** ~20% faster (AI handles boring parts)
- **Debugging/architecture:** No speed improvement, sometimes slower
- **Average across a week:** ~30-40% productivity boost, varies by task type

## Sorulursa

> [!faq]- "Are you worried AI will replace developers?"
> No. AI is replacing the boring parts — boilerplate, repetitive patterns, documentation. The hard parts — understanding requirements, making architecture trade-offs, debugging complex systems, working with people — are getting more important, not less. The developers who will struggle are the ones who only knew how to write boilerplate.

> [!faq]- "How do you prevent AI from introducing bugs?"
> Same way you prevent any code from having bugs: tests and review. Write the test first, let AI generate the implementation, run the test, review the code. If you can't explain why it works, rewrite it. The workflow matters more than the tool.

> [!faq]- "How do you handle AI in code reviews?"
> No distinction. AI-generated code gets the same scrutiny as human code. The reviewer doesn't need to know if AI wrote it — they just review the logic, edge cases, and security implications. If the code is good, it's good regardless of source. If it's bad, it's bad.

> [!faq]- "What about AI and intellectual property?"
> We use AI tools that don't train on our code (Cursor with Claude, not Copilot with GitHub training). Generated code is treated as our code — we own it, we're responsible for it, we review it. No different from using Stack Overflow answers — you take responsibility for what you ship.

> [!faq]- "How do you keep the team's skills sharp when using AI?"
> Deliberate practice. I still write code from scratch sometimes — especially for complex algorithms, new patterns, and areas where I want to deepen my understanding. I read documentation instead of asking AI. During code reviews, I explain why I'd write something differently, not just that it's wrong. The goal: AI makes you faster at things you already understand, not a substitute for understanding.

---

*[[00-dashboard]]*
