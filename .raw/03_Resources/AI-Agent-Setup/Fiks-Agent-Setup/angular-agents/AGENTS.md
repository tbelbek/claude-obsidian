# Angular UI Development Agents

3-agent system for Angular UI development: Architecture → Development → Testing & CI/CD.

## Quick Start

1. Start with **UI Architect Agent** — design analysis, component specs
2. **Angular Developer Agent** — implement all code (template + style + logic)
3. **CI/CD & Testing Agent** — write tests, configure pipeline, fix builds

## Agent Overview

| Agent | Role | Input | Output | Model |
|-------|------|-------|--------|-------|
| **ui-architect-agent** | Design → architecture spec | Figma/user requirements | Component tree, type defs, routing plan | Sonnet |
| **angular-developer-agent** | Write all Angular code | Component spec | `.ts`, `.html`, `.css` files, services, routes | Sonnet |
| **cicd-testing-agent** | Tests, pipeline, quality | Implemented components | Test files, GH Actions workflows, coverage report | Sonnet |

## Workflow

```
┌─────────────────────────────────────────────────────┐
│                  USER / FIGMA INPUT                  │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
         ┌──────────────────────────┐
         │    UI ARCHITECT AGENT    │
         │  • Component hierarchy   │
         │  • Type definitions      │
         │  • State management plan │
         │  • Tailwind mappings     │
         │  • A11y requirements     │
         └────────────┬─────────────┘
                      │ Component Spec
                      ▼
         ┌──────────────────────────┐
         │  ANGULAR DEVELOPER AGENT │
         │  • HTML templates        │
         │  • CSS / Tailwind        │
         │  • TypeScript logic      │
         │  • Services & state      │
         │  • Routing & lazy load   │
         └────────────┬─────────────┘
                      │ Implemented Code
                      ▼
         ┌──────────────────────────┐
         │  CI/CD & TESTING AGENT   │
         │  • Unit tests            │
         │  • Component tests       │
         │  • E2E tests (Playwright)│
         │  • GitHub Actions CI     │
         │  • Lint, coverage, build │
         └──────────────────────────┘
```

## Orchestration Rules

| Situation | Route To |
|-----------|----------|
| New UI feature / page design | `ui-architect-agent` |
| Implement component from spec | `angular-developer-agent` |
| Modify existing component | `angular-developer-agent` |
| Write / fix tests | `cicd-testing-agent` |
| Build error | `cicd-testing-agent` |
| Pipeline setup / update | `cicd-testing-agent` |
| Architecture question mid-implementation | `ui-architect-agent` |
| Flaky test diagnosis | `cicd-testing-agent` |

## Directory Structure

```
angular-agents/
├── AGENTS.md                        # This file — master reference
├── ui-architect-agent/
│   ├── SOUL.md                      # Identity, principles, rules
│   └── AGENTS.md                    # Workflow, routing, tools
├── angular-developer-agent/
│   ├── SOUL.md                      # Angular patterns, code standards
│   └── AGENTS.md                    # Implementation workflow, CLI commands
└── cicd-testing-agent/
    ├── SOUL.md                      # Testing philosophy, CI/CD patterns
    └── AGENTS.md                    # Test workflow, pipeline templates
```

## Communication Protocol

### Spec Handoff (Architect → Developer)

```markdown
## Component: [Name]
- Type: Standalone | Shared | Layout | Page
- Pattern: Container | Presentational
- Inputs: @Input() list with TypeScript types
- Outputs: @Output() list with event types
- State: local signal | service signal | NgRx
- Children: [sub-component list]
- Tailwind: [key utility classes]
- A11y: [ARIA roles, keyboard behavior]
- Responsive: [breakpoint strategy]
```

### Test Handoff (Developer → Testing)

```markdown
## Ready for Testing: [Component Name]
- Path: src/app/features/feature-name/
- Key behaviors: [list of what to test]
- Edge cases: [null inputs, empty lists, error states]
- User interactions: [form submit, click, keyboard nav]
```

### Quality Verdict (Testing → Team)

```
PASS        → Ready to merge
WARN        → Minor issues noted, can merge
FAIL        → Must fix: [specific issues with file:line references]
```

## Token Optimization

| Task Type | Model | Reason |
|-----------|-------|--------|
| Simple component breakdown | Haiku | Fast, routine |
| Complex architecture (multi-page) | Sonnet | Reasoning needed |
| Simple presentational component | Haiku | Pattern-based |
| Complex stateful component | Sonnet | Signals, async, forms |
| Simple unit tests | Haiku | Follow patterns |
| Complex integration / E2E tests | Sonnet | Setup, assertions |
| Pipeline configuration | Sonnet | YAML, caching, stages |
| Build error fix | Haiku | Targeted fix |

**Message limits:** 15-20 per agent task. Checkpoint if exceeding.

## Angular Stack

- **Angular:** 17+ (standalone components, signals, new control flow)
- **Styling:** Tailwind CSS 3.x
- **State:** Signals (local), Services with signals (shared), NgRx (complex)
- **Forms:** Reactive forms only
- **Testing:** Jest or Karma (unit), Angular Testing Library (component), Playwright (E2E)
- **CI/CD:** GitHub Actions
- **Linting:** ESLint with Angular plugin + Prettier

## Common Patterns

### State Management Decision Tree
```
Local only?                    → signal() in component
Shared between siblings?       → Service with signal()
Complex app-wide + time-travel? → NgRx SignalStore
Async stream (WebSocket, SSE)?  → RxJS Observable
```

### Component Classification
```
Page component      → Lazy loaded via router, fetches data
Container component → Manages state, passes to presentational
Presentational      → Pure @Input/@Output, no side effects
Shared/UI component → Reusable across features (button, card, modal)
Layout component    → Shell, header, sidebar, footer
```

## Version

- Created: 2026-04-02
- Angular: 17+ (signals, standalone, new control flow)
- Tailwind: 3.x
- Node: 20 LTS
