---
title: "7 Claude Code Mistakes That Are Costing You Hours"
source: "https://x.com/zodchiii/status/2041107570258018801"
author:
  - "[[@zodchiii]]"
published: 2026-04-06
created: 2026-04-07
description: "You're probably making at least 3 of these right now. Each one has a fix that takes under 2 minutes.The frustrating part is that none of the..."
tags:
  - "clippings"
---
**You're probably making at least 3 of these right now. Each one has a fix that takes under 2 minutes.**

The frustrating part is that none of these mistakes are obvious. Claude Code still gives you output. It still writes code and still feels useful.

You just don't realize how much better it could be until you fix the thing you didn't know was broken.

These are the 7 mistakes I see people make over and over, including myself.

Each one has a specific fix you can apply today 👇

Before we dive in, I share daily notes on AI & vibe coding in my Telegram channel: [https://t.me/zodchixquant](https://t.me/zodchixquant)🧠

![Resim](https://pbs.twimg.com/media/HFN1Ea4aYAAbkOD?format=jpg&name=large)

## 1\. Running everything in one long session

This is the most common mistake and the one that costs the most time.

You start a session, implement a feature, then ask Claude to fix a bug, then write some tests, then review a PR, then refactor something. All in one conversation.

Context fills up, earlier instructions get buried, and Claude starts making mistakes it wouldn't make with a clean window.

A Claude Code session at 90% context usage isn't just slower. It's measurably worse.

The model loses track of what you asked earlier, forgets constraints you set, and starts producing generic output instead of specific solutions.

```plaintext
The pattern that kills quality:

Feature → bug fix → tests → PR review → refactor
All in one session. Context at 95%.
Claude forgot your first 3 instructions.

The pattern that works:

Feature → /clear
Bug fix → /clear
Tests → /clear
PR review → /clear

Each task gets clean context and full attention.
```

**The fix:** Type **/clear** between every distinct task. Takes 1 second. If you take one thing from this entire article, make it this.

![Resim](https://pbs.twimg.com/media/HFN1yleXMAAGrYA?format=jpg&name=large)

## 2\. Writing vague prompts

"Fix the bug" is not a prompt. "Clean up this code" is not a prompt. "Make it better" is definitely not a prompt. Claude Code can work with vague instructions but the output will be vague too.

The difference between a 5-minute task and a 45-minute task is often just the prompt.

```text
Vague (Claude guesses what you want):
"Fix the auth bug"

Specific (Claude knows exactly what to do):
"The login endpoint at /api/auth/login returns 500 
when the email contains a plus sign. The error is in 
src/auth/validate.ts. Fix the regex validation 
and add a test case for emails with plus signs."
```

You don't need to write a novel. You need three things: what's broken, where it is, and what "fixed" looks like. Claude does the rest.

**The fix:** Before you hit enter, ask yourself "could Claude do this in one pass without asking me a follow-up question?" If no, add more detail.

![Resim](https://pbs.twimg.com/media/HFN3AJMWIAAXqAs?format=jpg&name=large)

## 3\. Not giving Claude a feedback loop

This is the mistake that Boris Cherny, the creator of Claude Code, talks about the most.

When you ask Claude to implement something without a way to verify its own work, you're basically asking it to code blindfolded.

The difference is simple: without a feedback loop, Claude writes code and says "done."

With a feedback loop, Claude writes code, runs the tests, sees what failed, fixes it, runs again, and only says "done" when everything passes.

```text
Without feedback loop:

"Implement the shipping calculator"
→ Claude writes code
→ "Done!"
→ You find 3 bugs during review
→ 30 minutes wasted

With feedback loop:

"Implement the shipping calculator. 
Run npm test after making changes. 
Fix any failures before calling it done."
→ Claude writes code
→ Runs tests
→ 2 tests fail
→ Fixes them
→ All tests pass
→ "Done!" (actually done this time)
```

According to Cherny, this one change gives you a 2-3x quality improvement. That's not a small optimization, that's the difference between useful output and output you have to rewrite.

**The fix:** Add "run tests after changes and fix any failures before finishing" to every implementation prompt. Or better yet, put it in your CLAUDE.md so you never have to type it again.

![Resim](https://pbs.twimg.com/media/HFNBv8EbEAE-Y6w?format=png&name=large)

## 4\. Not using CLAUDE.md

Every time you start a Claude Code session, you repeat yourself. "Use TypeScript." "We use Prisma, not raw SQL." "Functional components only." "Run Prettier after editing."

Over and over, every single session.

CLAUDE.md is a file at the root of your project that loads automatically when Claude Code starts. Everything you put in it, Claude reads before you type your first prompt.

You write your rules once and Claude follows them forever.

Without this file you're relying on memory. Yours and Claude's. Both will fail at some point (trust me)

```plaintext
Example CLAUDE.md that saves 5 minutes per session:

# Stack
Next.js 14, TypeScript, Prisma ORM, Tailwind CSS

# Rules
- Functional components with hooks, no class components
- All API responses use {data, error, meta} format
- Error messages should be user-friendly
- All database queries through Prisma, never raw SQL

# After every change
Run \`npm run test\` and fix failures before finishing
Run \`npm run lint\` and fix issues before finishing
```

**The fix:** Create a CLAUDE.md in your project root right now. Start with your stack, your code style rules, and your testing commands. Takes 3 minutes and saves hours over the lifetime of the project.

## 5\. Editing your main branch directly

By default, Claude Code works directly on your current branch. If something goes wrong, your main codebase is affected.

If Claude makes a bad refactor, you're rolling back commits.

If it breaks something subtle, you might not notice until later.

Worktrees solve this completely. Claude creates an isolated copy of your branch, does all its work there, and only merges when you're happy with the result.

If it goes wrong, you delete the worktree and your main branch was never touched.

```plaintext
Risky:
claude "refactor the auth module"
→ Works directly on your branch
→ Something breaks
→ You're reverting commits at 11pm

Safe:
claude -w "refactor-auth"
→ Creates isolated worktree
→ Something breaks
→ Delete worktree, main branch untouched
→ You sleep well
```

**The fix:** Use **claude -w branch-name** for any task that touches more than 2-3 files. Especially refactors, feature implementations, and anything you're not 100% sure about.

![Resim](https://pbs.twimg.com/media/HFNCdFUWIAAzRg5?format=png&name=large)

## 6\. Clicking "yes" on every permission prompt

Claude Code asks permission for everything by default.

"Can I edit this file?" "Can I run this command?" "Can I read this directory?" And most developers just click yes every time without reading what they're approving.

This is slow and also not actually safe. You're not reviewing each action carefully, you're just muscle-memorying through approvals.

Either set up proper scoped permissions so Claude can work without asking, or use auto mode which has an AI safety classifier checking each action.

```plaintext
The slow way:

Claude: "Can I edit auth.ts?" → Yes
Claude: "Can I run npm test?" → Yes
Claude: "Can I read config.js?" → Yes
Claude: "Can I edit auth.ts again?" → Yes
(repeat 47 times per session)

The fast way:

claude --permission-mode auto
→ AI classifier checks each action
→ Blocks risky stuff automatically
→ Lets routine work proceed
→ You actually get things done
```

Or scope it precisely with **\--allowedTools** so Claude has permission for exactly the tools it needs and nothing else.

**The fix:** Either use **--permission-mode auto** for sessions where you trust the environment, or set up **allowedTools** in your **.claude/settings.json** for permanent scoped permissions.

## 7\. Not using parallel sessions for big tasks

Most developers use Claude Code one task at a time. Write a feature, wait for it to finish, review it, then start the next one.

That's fine for small tasks but it's a massive bottleneck for anything bigger.

Claude Code supports multiple sessions running simultaneously, each in its own **worktree**.

You can have one agent implementing a feature, another writing tests, and a third fixing bugs, all at the same time. You just review PRs as they come in.

```plaintext
Sequential (most people):

Feature A: 30 min → review → Feature B: 30 min → review → Feature C: 30 min
Total: 90+ minutes

Parallel (what you should try):

claude -w feature-a --background
claude -w feature-b --background
claude -w feature-c --background
All three run simultaneously → review as PRs arrive
Total: 30 minutes + review time
```

This isn't for every task. Simple one-file changes don't need parallelization. But when you have 3-4 independent features to ship, running them in parallel instead of sequentially is an easy 3x speedup.

**The fix:** Next time you have multiple independent tasks, try spawning them as parallel background sessions with **claude -w branch-name --background** instead of doing them one by one.

## The cheat sheet

## Screenshot-friendly:

![Resim](https://pbs.twimg.com/media/HFNDdH-boAALP1Q?format=jpg&name=large)

## Copy and save:

```text
7 MISTAKES → 7 FIXES

1. One long session           → /clear between tasks
2. Vague prompts              → What, where, and what "done" looks like
3. No feedback loop           → "Run tests, fix failures before finishing"
4. No CLAUDE.md               → Write your rules once, Claude follows forever
5. Working on main branch     → claude -w branch-name
6. Clicking yes 47 times      → --permission-mode auto or --allowedTools
7. One task at a time         → claude -w branch --background (parallel)
```

You don't need to fix all 7 today.

Start with #1 (/clear between tasks) and #3 (feedback loop). Those two alone will make a noticeable difference in your first session.

I share daily notes on AI, finance, and vibe coding in my Telegram channel: [https://t.me/zodchixquant](https://t.me/zodchixquant) 🤖

Thanks for reading!

![Resim](https://pbs.twimg.com/media/HFN35zJaIAADb70?format=jpg&name=large)