---
tags:
  - education-kit
---

# Frontend Frameworks & Modern Web — Education Kit

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| React hooks | useState, useEffect, useRef, useMemo, custom hooks | Virtual DOM | diff tree, batch updates, Fiber for async |
| RSC | render on server, zero JS shipped, async data | Next.js | App Router, RSC, SSR/SSG/ISR, middleware |
| Angular signals | fine-grained reactivity, replaces Zone.js CD | Standalone | no NgModule, self-contained, simpler lazy load |
| Angular DI | hierarchical injector, providedIn root/component | RxJS | Observable streams, switchMap, takeUntil |
| Vue Composition | setup(), ref, reactive, composables for reuse | Pinia | 1KB, no mutations, defineStore, TS-first |
| Blazor | Server=SignalR, WASM=client-side .NET | JS interop | IJSRuntime, [JSImport]/[JSExport] |
| Bundlers | Vite=ESM+esbuild, Webpack=mature+plugins | Styling | Tailwind=utility, CSS-in-JS=scoped+dynamic |
| State mgmt | Redux=enterprise, Zustand=simple, Signals=fine | Rendering | SSR=SEO+fresh, CSR=SPA, SSG=fast, ISR=hybrid |
| CWV | LCP<2.5s, INP<200ms, CLS<0.1 | Code split | dynamic import(), route-based, React.lazy |
| E2E testing | Playwright=multi-browser, Cypress=dev-friendly | Testing Library | test user behavior, getByRole, not implementation |
| Micro-FE | Module Federation, independent deploy, shared shell | Web Components | Custom Elements, Shadow DOM, framework-agnostic |
| a11y/WCAG | semantic HTML, ARIA, keyboard nav, contrast | TS frontend | strict mode, generics, discriminated unions |

---

## 1. React

### React Hooks

**Q: What are React hooks and why were they introduced?**
A: Hooks let you use state and lifecycle features in functional components without classes. Introduced in React 16.8 to solve: (1) reusing stateful logic between components was hard (HOCs and render props created "wrapper hell"), (2) complex components became hard to understand (lifecycle methods mixed unrelated logic), (3) classes confused both people and machines (this binding, optimization difficulties). Rules: call hooks only at the top level (never inside loops/conditions) and only from React functions or custom hooks.

**Q: Explain useState, useEffect, useRef, useMemo, useCallback.**
A: `useState` -- declares reactive state, returns [value, setter]. `useEffect` -- runs side effects after render; dependency array controls when it re-runs (empty = mount only). Return a cleanup function for subscriptions/timers. `useRef` -- mutable container that persists across renders without triggering re-render; commonly used for DOM refs. `useMemo` -- memoizes expensive computed values, recalculates only when deps change. `useCallback` -- memoizes a function reference, useful to prevent child re-renders when passing callbacks as props. Overusing useMemo/useCallback adds complexity -- only use when profiling shows a performance issue.

**Q: What is useReducer and when do you prefer it over useState?**
A: `useReducer(reducer, initialState)` manages complex state transitions via a reducer function (like a mini Redux). Prefer when: state has multiple sub-values that depend on each other, next state depends on previous state, or you want to centralize state logic for testability. Pattern: dispatch an action, reducer produces new state deterministically.

**Q: How do you build custom hooks?**
A: Extract reusable stateful logic into a function prefixed with `use`. Example: `useDebounce(value, delay)` wraps useState + useEffect. Custom hooks compose other hooks. They share logic, not state -- each component calling the hook gets its own state. This replaces HOC/render prop patterns with simpler composition.

### Virtual DOM & Reconciliation

**Q: How does React's virtual DOM work?**
A: React maintains a lightweight in-memory representation of the real DOM. On state change: (1) new virtual DOM tree is created, (2) React diffs it against the previous tree (reconciliation), (3) computes minimal set of real DOM operations, (4) batches and applies them.

**Q: What is React Fiber?**
A: Fiber is React's reconciliation engine (React 16+). It breaks rendering work into units (fibers) that can be paused, prioritized, and resumed. This enables: concurrent rendering, prioritization (user input > background updates), Suspense and transitions.

**Q: What are React keys and why do they matter?**
A: Keys help React identify which items in a list changed, were added, or removed. Without stable keys, React re-renders the entire list. Never use array index as key if list can reorder.

### React Server Components

**Q: What are React Server Components (RSC)?**
A: Components that render exclusively on the server. They never ship JavaScript to the client. Benefits: (1) direct access to backend resources without API layer, (2) zero bundle size impact, (3) automatic code splitting. RSC can be async. They cannot use hooks, event handlers, or browser APIs. Client Components (marked with `"use client"`) handle interactivity.

**Q: How do Server Components differ from SSR?**
A: SSR renders the full component tree to HTML on the server, then hydrates on the client (all component code ships to client). RSC renders only server components on server -- their code never reaches the client. RSC and SSR are complementary.

### Next.js

**Q: Explain the Next.js App Router architecture.**
A: App Router (Next.js 13+) uses file-system routing with `app/` directory. Key concepts: layouts, loading.js (Suspense boundaries), error.js (error boundaries), page.js (route UI). All components are Server Components by default.

**Q: How does caching work in Next.js App Router?**
A: Multiple cache layers: Request Memoization, Data Cache, Full Route Cache, Router Cache. Control via `fetch()` options: `cache: 'force-cache'` (SSG), `cache: 'no-store'` (SSR), `next: { revalidate: 60 }` (ISR).

**Q: What is Next.js middleware?**
A: Code that runs before a request is completed, at the edge. Use cases: authentication, redirects, A/B testing, geolocation-based routing.

---

## 2. Angular

### Angular Signals

**Q: What are Angular Signals and why do they matter?**
A: Signals are a reactive primitive introduced in Angular 16. A signal wraps a value and notifies consumers when it changes. Computed signals auto-track dependencies. Effects run side effects on change. Signals enable fine-grained, targeted updates -- only components that read a changed signal re-render.

**Q: How do Signals compare to RxJS Observables?**
A: Signals are synchronous, always have a current value, auto-track dependencies. Observables are asynchronous streams. Bridge: `toSignal()` and `toObservable()`. Use Signals for UI state, keep RxJS for HTTP/WebSocket/complex async flows.

**Q: How does signal-based change detection differ from Zone.js?**
A: Zone.js patches all async APIs and triggers full tree dirty-checking. With Signals, Angular knows exactly which signals changed and which components read them.

### Standalone Components

**Q: What are standalone components and why use them?**
A: Standalone components (Angular 14+) set `standalone: true` and import dependencies directly instead of relying on NgModule. Benefits: eliminates boilerplate, simplifies lazy loading, clearer dependency graph.

### Dependency Injection

**Q: How does Angular's DI system work?**
A: Hierarchical injector tree. `providedIn: 'root'` creates a singleton. Component-level providers create isolated instances per component subtree.

### RxJS Essentials

**Q: What RxJS operators should a senior developer know?**
A: Transformation: `map`, `switchMap`, `mergeMap`, `concatMap`. Filtering: `filter`, `distinctUntilChanged`, `debounceTime`, `takeUntil`. Combination: `combineLatest`, `forkJoin`. Error: `catchError`, `retry`. Utility: `tap`, `shareReplay`.

**Q: How do you prevent memory leaks with RxJS in Angular?**
A: `takeUntil(destroy$)` pattern, `async` pipe in templates, `takeUntilDestroyed()` in Angular 16+, `take(1)` for one-shot operations.

---

## 3. Vue

### Vue Composition API

**Q: What is the Composition API?**
A: Composition API (Vue 3) organizes code by logical concern instead of option type. Key primitives: `ref()`, `reactive()`, `computed()`, `watch()`/`watchEffect()`.

**Q: What are composables in Vue?**
A: Functions that encapsulate reusable stateful logic using Composition API (like React custom hooks). Convention: prefix with `use`.

**Q: Explain Vue's reactivity system.**
A: Vue 3 uses JavaScript Proxy. When you access a reactive property, Vue tracks it as a dependency. When you modify it, Vue triggers effects. `ref()` wraps a value, `reactive()` wraps an object.

### Pinia

**Q: Why did Pinia replace Vuex?**
A: No mutations, full TypeScript support, flat stores, ~1KB size, Composition API-friendly, devtools support.

---

## 4. Blazor

### Blazor Server vs WebAssembly

**Q: Key differences?**
A: **Server**: UI on server, browser gets thin JS client via SignalR. Fast initial load but requires persistent connection. **WASM**: entire .NET runtime in browser. Works offline but large initial download. .NET 8 allows mixing both per-component.

### Blazor JS Interop

**Q: How does JavaScript interop work?**
A: Calling JS from .NET: `IJSRuntime.InvokeAsync`. Calling .NET from JS: `DotNetObjectReference` with `[JSInvokable]`. Minimize interop calls.

---

## 5. Build Tools & Styling

### Vite vs Webpack

**Q: Why Vite over Webpack?**
A: Vite uses native ES modules in dev (no bundling), esbuild for pre-bundling. Dev server starts in milliseconds. HMR is instant. Webpack is for legacy projects or when specific plugins are needed.

**Q: What is tree-shaking?**
A: Removes unused code from the final bundle based on ES module static analysis. Requires ES modules (not CommonJS).

### CSS-in-JS vs Tailwind

**Q: Compare CSS-in-JS, Tailwind, and CSS Modules.**
A: CSS Modules: locally scoped class names, zero runtime cost. CSS-in-JS: dynamic styles, but runtime cost. Tailwind: utility-first classes, rapid development, tiny production CSS.

---

## 6. State Management

### Redux vs Zustand vs Signals

**Q: Compare them.**
A: Redux: centralized, predictable, excellent devtools, verbose. Zustand: minimal API, hooks-based, ~1KB. Signals: fine-grained reactivity, framework-native.

**Q: When is global state management overkill?**
A: Most apps over-use global state. Prefer local component state, URL params for navigation state, and server state libraries (TanStack Query) for API data.

---

## 7. Rendering Strategies

### SSR vs CSR vs SSG vs ISR

**Q: Explain each and when to use them.**
A: CSR: JS renders UI in browser. SSR: server renders HTML per request. SSG: HTML at build time. ISR: SSG + background regeneration. Most real apps mix strategies.

**Q: What is streaming SSR?**
A: Sends HTML in chunks as components finish rendering. Browser starts painting immediately.

**Q: What is partial hydration and islands architecture?**
A: Only hydrate interactive components. Static HTML stays as-is. Used by Astro, Fresh.

---

## 8. Performance

### Core Web Vitals

**Q: What are they?**
A: LCP (Largest Contentful Paint) <2.5s. INP (Interaction to Next Paint) <200ms. CLS (Cumulative Layout Shift) <0.1.

### Code Splitting & Lazy Loading

**Q: How does code splitting work?**
A: Split JS bundle into smaller chunks loaded on demand. Route-based, component-based, or library splitting via dynamic `import()`.

---

## 9. Testing

### Playwright vs Cypress

**Q: Compare them.**
A: Playwright: multi-browser, multi-language, multi-tab support, tracing. Cypress: JavaScript only, excellent DX, runs inside the browser. Playwright is the industry default for new projects.

### Testing Library

**Q: What is Testing Library?**
A: Tests components the way users interact with them. Query by role, text, label -- not by class name or test ID. Encourages accessible markup.

---

## 10. Architecture Patterns

### Micro-Frontends

**Q: What are they and when to use them?**
A: Each team owns a vertical slice deployed independently. Implementation: Module Federation, iframes, Web Components, server-side composition. Only when multiple teams need independent deployment cycles.

### Web Components

**Q: What are Web Components?**
A: Browser-native component model: Custom Elements, Shadow DOM, HTML Templates. Use for cross-framework design systems.

### WCAG & Accessibility

**Q: Key WCAG 2.1 principles?**
A: POUR: Perceivable, Operable, Understandable, Robust. Use semantic HTML first, add ARIA only when needed. Automated testing catches ~30% -- manual testing with screen reader + keyboard is essential.

### TypeScript for Frontend

**Q: Important patterns?**
A: Discriminated unions for props, generics for reusable hooks, strict mode, utility types (Partial, Pick, Omit, Record), type guards, satisfies operator.

---

## Common Questions

**"How do you decide between SSR, CSR, SSG, and ISR?"**
Blog/docs: SSG. E-commerce product page: ISR. User dashboard: CSR. SEO-critical with real-time data: SSR with streaming. Most apps mix strategies per route.

**"What would you choose for a new frontend project?"**
Depends on the team. React team: Next.js. .NET team: Blazor. Enterprise Angular: Angular 17+ with signals. For all: TypeScript mandatory, Vite for build tooling, Playwright for E2E.

**"How do you approach frontend performance optimization?"**
Measure first (Lighthouse, DevTools, Core Web Vitals). Code splitting, image optimization, font optimization, bundle analysis, render strategy. Avoid client-side data waterfalls.
