---
tags:
  - interview-kit
  - interview-kit/reference
up: "[[00-dashboard]]"
---

*[[00-dashboard]]*

# Frontend Frameworks & Modern Web — Senior Interview Questions

> [!tip] Frontend knowledge for a senior full-stack engineer. Covers React, Angular, Vue, Blazor, tooling, state management, rendering strategies, testing, accessibility, and architecture patterns. Focus: enough depth to show competence, not pretend to be a frontend specialist.

## Quick Scan

| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#React Hooks\|React hooks]] | useState, useEffect, useRef, useMemo, custom hooks | [[#Virtual DOM & Reconciliation\|virtual DOM]] | diff tree, batch updates, Fiber for async |
| [[#React Server Components\|RSC]] | render on server, zero JS shipped, async data | [[#Next.js\|Next.js]] | App Router, RSC, SSR/SSG/ISR, middleware |
| [[#Angular Signals\|Angular signals]] | fine-grained reactivity, replaces Zone.js CD | [[#Standalone Components\|standalone]] | no NgModule, self-contained, simpler lazy load |
| [[#Dependency Injection\|Angular DI]] | hierarchical injector, providedIn root/component | [[#RxJS Essentials\|RxJS]] | Observable streams, switchMap, takeUntil |
| [[#Vue Composition API\|Vue Composition]] | setup(), ref, reactive, composables for reuse | [[#Pinia\|Pinia]] | 1KB, no mutations, defineStore, TS-first |
| [[#Blazor Server vs WebAssembly\|Blazor]] | Server=SignalR, WASM=client-side .NET | [[#Blazor JS Interop\|JS interop]] | IJSRuntime, [JSImport]/[JSExport] |
| [[#Vite vs Webpack\|bundlers]] | Vite=ESM+esbuild, Webpack=mature+plugins | [[#CSS-in-JS vs Tailwind\|styling]] | Tailwind=utility, CSS-in-JS=scoped+dynamic |
| [[#Redux vs Zustand vs Signals\|state mgmt]] | Redux=enterprise, Zustand=simple, Signals=fine | [[#SSR vs CSR vs SSG vs ISR\|rendering]] | SSR=SEO+fresh, CSR=SPA, SSG=fast, ISR=hybrid |
| [[#Core Web Vitals\|CWV]] | LCP<2.5s, INP<200ms, CLS<0.1 | [[#Code Splitting & Lazy Loading\|code split]] | dynamic import(), route-based, React.lazy |
| [[#Playwright vs Cypress\|E2E testing]] | Playwright=multi-browser, Cypress=dev-friendly | [[#Testing Library\|Testing Library]] | test user behavior, getByRole, not implementation |
| [[#Micro-Frontends\|micro-FE]] | Module Federation, independent deploy, shared shell | [[#Web Components\|Web Components]] | Custom Elements, Shadow DOM, framework-agnostic |
| [[#WCAG & Accessibility\|a11y/WCAG]] | semantic HTML, ARIA, keyboard nav, contrast | [[#TypeScript for Frontend\|TS frontend]] | strict mode, generics, discriminated unions |

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
A: React maintains a lightweight in-memory representation of the real DOM. On state change: (1) new virtual DOM tree is created, (2) React diffs it against the previous tree (reconciliation), (3) computes minimal set of real DOM operations, (4) batches and applies them. This is faster than direct DOM manipulation because DOM operations are expensive and batching reduces reflows/repaints.

**Q: What is React Fiber?**
A: Fiber is React's reconciliation engine (React 16+). It breaks rendering work into units (fibers) that can be paused, prioritized, and resumed. This enables: concurrent rendering (don't block the main thread for large updates), prioritization (user input > background updates), Suspense and transitions. Each fiber node represents a component instance and tracks its state, effects, and position in the tree.

**Q: What are React keys and why do they matter?**
A: Keys help React identify which items in a list changed, were added, or removed. Without stable keys, React re-renders the entire list. With keys, it can match old and new elements efficiently. Never use array index as key if list can reorder -- it causes incorrect state association and subtle bugs.

### React Server Components

**Q: What are React Server Components (RSC)?**
A: Components that render exclusively on the server. They never ship JavaScript to the client. Benefits: (1) direct access to backend resources (DB, filesystem) without API layer, (2) zero bundle size impact -- heavy dependencies (markdown parsers, syntax highlighters) stay on the server, (3) automatic code splitting. RSC can be async (use async/await directly). They cannot use hooks, event handlers, or browser APIs. Client Components (marked with `"use client"`) handle interactivity and compose with Server Components.

**Q: How do Server Components differ from SSR?**
A: SSR renders the full component tree to HTML on the server, then hydrates it on the client (all component code ships to client). RSC renders only server components on server -- their code never reaches the client. The client receives a serialized representation (not HTML) that React reconstructs. RSC and SSR are complementary: RSC reduces bundle size, SSR provides fast initial HTML.

### Next.js

**Q: Explain the Next.js App Router architecture.**
A: App Router (Next.js 13+) uses file-system routing with `app/` directory. Key concepts: layouts (shared UI that preserves state across navigations), loading.js (Suspense boundaries), error.js (error boundaries), page.js (route UI). All components are Server Components by default. Uses React Server Components, streaming, and Suspense natively. Replaces `getServerSideProps`/`getStaticProps` with direct async data fetching in Server Components.

**Q: How does caching work in Next.js App Router?**
A: Multiple cache layers: (1) Request Memoization -- deduplicates identical fetch calls within a single render, (2) Data Cache -- persists fetch results across requests (configurable revalidation), (3) Full Route Cache -- caches rendered output of static routes at build time, (4) Router Cache -- client-side cache of visited routes for instant back/forward navigation. You control caching via `fetch()` options: `cache: 'force-cache'` (default SSG), `cache: 'no-store'` (SSR), `next: { revalidate: 60 }` (ISR).

**Q: What is Next.js middleware?**
A: Code that runs before a request is completed. Executes at the edge (not in Node.js). Use cases: authentication checks, redirects, A/B testing, geolocation-based routing, request/response header manipulation. Defined in `middleware.ts` at project root. Runs on every request matching the configured matcher pattern.

---

## 2. Angular

### Angular Signals

**Q: What are Angular Signals and why do they matter?**
A: Signals are a reactive primitive introduced in Angular 16. A signal is a wrapper around a value that notifies consumers when it changes. `signal(0)` creates one, `.set()` / `.update()` modifies it, reading is just `count()`. Computed signals (`computed(() => count() * 2)`) auto-track dependencies. Effects (`effect(() => console.log(count()))`) run side effects on change. Why it matters: Zone.js change detection checks the entire component tree on every async event. Signals enable fine-grained, targeted updates -- only components that read a changed signal re-render. This is a fundamental shift toward better performance and simpler mental model.

**Q: How do Signals compare to RxJS Observables?**
A: Signals are synchronous, always have a current value, and auto-track dependencies. Observables are asynchronous streams, may not have a current value, require explicit subscription/unsubscription, and are more powerful for complex async flows (debounce, retry, combine streams). Bridge: `toSignal()` converts Observable to Signal, `toObservable()` converts Signal to Observable. Guideline: use Signals for synchronous component/UI state, keep RxJS for HTTP calls, WebSocket streams, complex event composition.

**Q: How does signal-based change detection differ from Zone.js?**
A: Zone.js patches all async APIs (setTimeout, Promise, XHR) and triggers change detection on every async event -- Angular then dirty-checks the entire component tree. With Signals, Angular knows exactly which signals changed and which components read them, so it only re-renders affected views. In Angular 17+, you can go fully zoneless (`provideExperimentalZonelessChangeDetection()`) for maximum performance.

### Standalone Components

**Q: What are standalone components and why use them?**
A: Standalone components (Angular 14+) set `standalone: true` in the decorator. They import their dependencies directly (other components, directives, pipes) instead of relying on an NgModule. Benefits: (1) eliminates NgModule boilerplate, (2) simplifies lazy loading (can lazy-load a single component, not an entire module), (3) clearer dependency graph (each component declares exactly what it needs), (4) easier to learn and onboard. In Angular 17+, standalone is the default for new projects.

**Q: How do you migrate from NgModules to standalone?**
A: Angular provides `ng generate @angular/core:standalone` schematic for automated migration. Strategy: (1) start with leaf components (no children), (2) add `standalone: true` and move imports from NgModule into the component's `imports` array, (3) remove component from NgModule declarations, (4) work upward to parent components, (5) eventually remove empty NgModules. Can be done incrementally -- standalone and module-based components coexist.

### Dependency Injection

**Q: How does Angular's DI system work?**
A: Angular has a hierarchical injector tree. When a component requests a dependency, Angular walks up the injector hierarchy until it finds a provider. Levels: (1) `providedIn: 'root'` -- singleton across the entire app (tree-shakeable), (2) module-level -- scoped to that module, (3) component-level (`providers: [...]` in component) -- new instance per component. This enables scoped services: a service provided at component level creates isolated instances per component subtree. The injector resolves dependencies transitively -- if Service A depends on Service B, both are resolved automatically.

**Q: What is the difference between providedIn root vs component-level providers?**
A: `providedIn: 'root'` creates a singleton shared across the entire app -- ideal for global services (auth, HTTP, logging). Component-level providers create a new instance for each component instance -- ideal for stateful services that should be isolated (form state, component-specific data). If you provide at component level, child components also get that instance unless they provide their own override.

### RxJS Essentials

**Q: What RxJS operators should a senior developer know?**
A: **Transformation**: `map`, `switchMap` (cancel previous inner observable -- use for HTTP/search), `mergeMap` (concurrent inner observables -- use for parallel operations), `concatMap` (sequential inner observables -- use for ordered operations). **Filtering**: `filter`, `distinctUntilChanged`, `debounceTime` (wait for pause in emissions -- search input), `take`, `takeUntil` (unsubscribe pattern). **Combination**: `combineLatest`, `forkJoin` (wait for all to complete -- parallel HTTP calls), `withLatestFrom`. **Error**: `catchError`, `retry`, `retryWhen`. **Utility**: `tap` (side effects without modifying stream), `shareReplay` (multicast + cache last N values).

**Q: How do you prevent memory leaks with RxJS in Angular?**
A: (1) `takeUntil(destroy$)` pattern -- create a Subject, emit in ngOnDestroy, use takeUntil on all subscriptions. (2) `async` pipe in templates -- auto-subscribes and unsubscribes. (3) `DestroyRef` + `takeUntilDestroyed()` in Angular 16+ -- cleaner than manual Subject. (4) `take(1)` for one-shot operations. Never subscribe in a component without a cleanup strategy.

---

## 3. Vue

### Vue Composition API

**Q: What is the Composition API and how does it differ from Options API?**
A: Composition API (Vue 3) organizes code by logical concern instead of option type. Options API groups by type (data, methods, computed, watch) -- related logic gets scattered. Composition API uses `setup()` or `<script setup>` to colocate related logic. Key primitives: `ref()` for reactive primitives, `reactive()` for reactive objects, `computed()` for derived values, `watch()`/`watchEffect()` for side effects. `<script setup>` is the recommended syntax -- automatically exposes top-level bindings to template, less boilerplate.

**Q: What are composables in Vue?**
A: Functions that encapsulate and reuse stateful logic using Composition API (equivalent to React custom hooks). Convention: prefix with `use` (e.g., `useFetch`, `useAuth`). A composable returns reactive state and methods. Unlike mixins (Vue 2), composables have explicit inputs/outputs, no naming conflicts, clear data flow, and full TypeScript support. They are the primary code reuse mechanism in Vue 3.

**Q: Explain Vue's reactivity system.**
A: Vue 3 uses JavaScript Proxy (replacing Vue 2's Object.defineProperty). When you access a reactive property, Vue tracks it as a dependency. When you modify it, Vue triggers all effects that depend on it. `ref()` wraps a value in `{ value: ... }` with getter/setter tracking. `reactive()` wraps an object in a Proxy. Limitations: destructuring reactive objects breaks reactivity (use `toRefs()`). The Proxy-based system handles dynamic property addition/deletion (Vue 2 couldn't).

### Pinia

**Q: Why did Pinia replace Vuex?**
A: Pinia is the official state management for Vue 3. Improvements over Vuex: (1) no mutations -- direct state modification allowed, (2) full TypeScript support with inference, (3) no nested modules -- flat store architecture, (4) ~1KB size, (5) Composition API-friendly (stores use `ref`/`computed`), (6) devtools support with time-travel debugging. Define a store with `defineStore('id', () => { ... })` using Composition API syntax. Access stores via `useXxxStore()` in components.

**Q: When should you use Pinia vs local component state vs provide/inject?**
A: Local state (`ref`/`reactive`): component-specific, not shared. Props/emits: parent-child communication. Provide/inject: dependency injection for deep component trees without prop drilling. Pinia: shared state across unrelated components, state that persists across route navigations, complex state logic needing devtools. Rule of thumb: start local, lift to Pinia only when multiple unrelated components need the same state.

---

## 4. Blazor

### Blazor Server vs WebAssembly

**Q: What are the key differences between Blazor Server and Blazor WebAssembly?**
A: **Blazor Server**: UI runs on the server, browser gets a thin JS client. All UI events travel over a SignalR (WebSocket) connection. Pros: fast initial load, thin client, full .NET API access, app code stays on server (security). Cons: requires persistent connection (latency-sensitive), every interaction has network round-trip, doesn't work offline, scales with concurrent connections (server memory per user). **Blazor WASM**: entire .NET runtime + app downloaded to browser, runs on WebAssembly. Pros: runs offline, no server dependency after load, scales like any SPA. Cons: large initial download (several MB), limited .NET API surface, slower startup, code visible to client.

**Q: What is Blazor United / .NET 8 render modes?**
A: .NET 8 introduced unified hosting: a single Blazor app can mix Server and WASM rendering per-component. Render modes: `InteractiveServer` (SignalR), `InteractiveWebAssembly` (WASM), `InteractiveAuto` (starts as Server, switches to WASM after download). `@rendermode` attribute on component usage controls this. Static SSR is also available for non-interactive content. This eliminates the binary Server-vs-WASM choice.

### Blazor Component Lifecycle

**Q: What is the Blazor component lifecycle?**
A: `SetParametersAsync` -- called when parent sets parameters. `OnInitialized`/`OnInitializedAsync` -- called once after first render (data fetching goes here). `OnParametersSet`/`OnParametersSetAsync` -- called after parameters change. `OnAfterRender`/`OnAfterRenderAsync` -- called after DOM update (JS interop goes here, check `firstRender` parameter). `Dispose`/`DisposeAsync` via `IDisposable`/`IAsyncDisposable` -- cleanup timers, event handlers, SignalR connections.

### Blazor JS Interop

**Q: How does JavaScript interop work in Blazor?**
A: **Calling JS from .NET**: inject `IJSRuntime`, call `InvokeAsync<T>("functionName", args)`. The JS function must be in `window` scope or a module. **Calling .NET from JS**: create a `DotNetObjectReference`, pass it to JS, JS calls `invokeMethodAsync('MethodName', args)` -- the .NET method must be `[JSInvokable]`. **In .NET 7+ WASM**: `[JSImport]`/`[JSExport]` attributes for direct interop without IJSRuntime overhead. Best practice: minimize JS interop calls (each is a boundary crossing), batch operations, use JS modules (`IJSObjectReference`) for isolation.

---

## 5. Build Tools & Styling

### Vite vs Webpack

**Q: Why has Vite largely replaced Webpack for new projects?**
A: **Vite**: uses native ES modules in dev (no bundling during development), esbuild for dependency pre-bundling (10-100x faster than JS-based bundlers), Rollup for production builds. Dev server starts in milliseconds regardless of app size. HMR is instant because it only processes the changed module. **Webpack**: bundles everything before dev server starts (slow for large apps), loader-based pipeline, mature plugin ecosystem. Still used in legacy projects and when specific Webpack plugins are required. Webpack 5 added Module Federation (micro-frontends). **For new projects in 2025**: Vite is the default choice for React (via create-vite), Vue, Svelte. Angular moved to esbuild in v17.

**Q: What is tree-shaking and how do bundlers implement it?**
A: Tree-shaking removes unused code from the final bundle. Based on ES module static analysis -- bundler traces import/export chains and eliminates dead code. Requirements: ES modules (not CommonJS), side-effect-free code (mark via `sideEffects: false` in package.json). Example: if you `import { debounce } from 'lodash-es'`, only debounce (and its deps) ships, not the entire lodash library. CommonJS (`require()`) prevents tree-shaking because imports are dynamic.

### CSS-in-JS vs Tailwind

**Q: Compare CSS-in-JS, Tailwind, and CSS Modules.**
A: **CSS Modules**: locally scoped class names via build tool (`.button` becomes `.button_abc123`). No naming conflicts, works with standard CSS, zero runtime cost. **CSS-in-JS** (styled-components, Emotion): write CSS in JavaScript, scoped by default, dynamic styles based on props, colocation with components. Downside: runtime cost (generates styles at runtime), SSR complexity, bundle size. Trend: moving away from runtime CSS-in-JS toward zero-runtime solutions (vanilla-extract, Panda CSS). **Tailwind CSS**: utility-first classes directly in HTML (`class="flex items-center p-4 bg-blue-500"`). Pros: rapid development, consistent design system, tiny production CSS (purges unused classes), no naming decisions. Cons: verbose HTML, learning curve for utility names, custom designs need config. In 2025, Tailwind v4 uses a Rust-based engine (Oxide) for faster builds.

**Q: When would you choose Tailwind vs CSS Modules?**
A: Tailwind: rapid prototyping, design-system consistency, team wants utility-first approach, component-based frameworks (React/Vue/Angular -- utilities stay with component). CSS Modules: team prefers traditional CSS, complex animations, needs full CSS features (media queries written naturally), existing CSS expertise. Both can coexist. For a backend-heavy engineer touching frontend: Tailwind is often easier -- no context switching to separate CSS files, autocomplete with IDE extension.

---

## 6. State Management Patterns

### Redux vs Zustand vs Signals

**Q: Compare Redux, Zustand, and Signals for state management.**
A: **Redux** (+ Redux Toolkit): centralized store, unidirectional flow (dispatch action -> reducer -> new state -> UI updates). Predictable, excellent devtools (time-travel debugging), middleware for async (thunks, sagas). Verbose but standardized. Best for: large teams, complex state logic, enterprise apps. **Zustand**: minimal API, hooks-based, no boilerplate. `create((set) => ({ count: 0, increment: () => set(s => ({ count: s.count + 1 })) }))`. No providers/context needed. ~1KB. Best for: small-to-medium apps, simplicity-first teams. **Signals** (Preact Signals, Angular Signals, Solid): fine-grained reactivity. Value changes propagate only to subscribers. No virtual DOM diffing needed for updates. Best for: performance-critical UIs, framework-native solutions.

**Q: When is global state management overkill?**
A: Most apps over-use global state. Prefer: (1) local component state for UI-specific state (form inputs, toggles, modals), (2) URL/query params for navigation state (filters, pagination), (3) server state libraries (React Query/TanStack Query, SWR) for API data -- they handle caching, revalidation, loading/error states. Global store only for: truly shared UI state (theme, user preferences, shopping cart), state that must survive route changes without refetching.

---

## 7. Rendering Strategies

### SSR vs CSR vs SSG vs ISR

**Q: Explain SSR, CSR, SSG, and ISR. When do you use each?**
A: **CSR (Client-Side Rendering)**: browser downloads minimal HTML + JS bundle, JS renders the UI. Pros: rich interactivity, no server needed after initial load. Cons: slow initial load (blank screen until JS executes), poor SEO (crawlers may not execute JS). Use for: dashboards, admin panels, authenticated apps. **SSR (Server-Side Rendering)**: server renders full HTML per request. Pros: fast first paint, good SEO, dynamic content. Cons: server load per request, TTFB depends on server speed. Use for: e-commerce product pages, content sites needing SEO + fresh data. **SSG (Static Site Generation)**: HTML generated at build time. Pros: fastest delivery (served from CDN), highly cacheable. Cons: stale until next build, rebuild time grows with pages. Use for: blogs, docs, marketing sites. **ISR (Incremental Static Regeneration)**: SSG + background regeneration. Serves stale static page, regenerates in background on a timer or on-demand. Pros: speed of SSG + freshness. Cons: Next.js-specific (though others are adopting). Use for: large catalogs, news sites.

**Q: What is streaming SSR and why does it matter?**
A: Traditional SSR waits for the entire page to render before sending HTML. Streaming SSR sends HTML in chunks as components finish rendering. The browser can start painting immediately, even while later parts of the page are still rendering on the server. React 18+ supports this via `renderToPipeableStream`. Combined with Suspense boundaries, slow components show fallbacks while fast components render immediately. Dramatically improves TTFB and perceived performance for complex pages.

**Q: What is partial hydration and islands architecture?**
A: Full hydration (React default): ship all JS and re-attach event handlers to entire page -- expensive. **Partial hydration**: only hydrate interactive components, leave static HTML as-is. **Islands architecture** (Astro): page is static HTML by default, interactive components are "islands" that hydrate independently. Each island loads its own JS only when needed (on load, on visible, on idle). Result: dramatically less JS shipped. Astro, Fresh (Deno), Eleventy use this pattern.

---

## 8. Performance

### Core Web Vitals

**Q: What are Core Web Vitals and their thresholds?**
A: Google's metrics for user experience. **LCP (Largest Contentful Paint)**: time until the largest visible element renders. Good: <2.5s. Improve: optimize critical rendering path, preload hero images, use CDN, SSR/SSG. **INP (Interaction to Next Paint)**: time from user interaction to next visual update (replaced FID in 2024). Good: <200ms. Improve: break long tasks, use `requestIdleCallback`, defer non-critical work, use web workers for heavy computation. **CLS (Cumulative Layout Shift)**: visual stability -- how much content shifts unexpectedly. Good: <0.1. Improve: set explicit dimensions on images/videos, avoid injecting content above existing content, use `font-display: swap` with font preloading.

**Q: How do you diagnose and fix a slow LCP?**
A: (1) Identify the LCP element (Chrome DevTools > Performance > LCP marker). Common LCP elements: hero image, heading text, video poster. (2) Check: is the resource discoverable early? (preload critical images), is it blocked by render-blocking CSS/JS? (defer non-critical scripts), is the server slow? (optimize TTFB with caching/SSR), is the image too large? (responsive images with srcset, modern formats like WebP/AVIF, lazy-load below-fold images but NOT the LCP image).

### Code Splitting & Lazy Loading

**Q: How does code splitting work?**
A: Split the JS bundle into smaller chunks loaded on demand. Techniques: (1) **Route-based splitting** -- each route is a separate chunk, loaded when navigated to. (2) **Component-based splitting** -- heavy components loaded when needed (`React.lazy(() => import('./HeavyComponent'))`, Angular `loadComponent` in routes, Vue `defineAsyncComponent`). (3) **Library splitting** -- large dependencies in separate chunks. Bundlers (Vite/Webpack) handle this via dynamic `import()` statements. Key: split at natural boundaries (routes, modals, rarely-used features) to keep initial bundle small.

**Q: What is lazy loading and how do you implement it for images?**
A: Defer loading resources until needed. Images: native `loading="lazy"` attribute (browser handles it), or Intersection Observer API for custom behavior. Components: dynamic imports (see above). Routes: lazy route definitions. Important: never lazy-load above-the-fold / LCP content -- it needs to load immediately. Use `loading="eager"` or `fetchpriority="high"` for critical images.

---

## 9. Testing

### Playwright vs Cypress

**Q: Compare Playwright and Cypress for E2E testing.**
A: **Playwright**: multi-browser (Chromium, Firefox, WebKit), multi-language (JS, Python, C#, Java), multi-tab/multi-origin support, built-in auto-waiting, parallel execution, tracing/video/screenshots. Architecture: controls browser via CDP/protocol, runs outside the browser. **Cypress**: JavaScript only, Chromium + Firefox (limited WebKit), runs inside the browser (same-origin limitation), excellent DX with time-travel debugging in GUI, automatic retries. **Key differences**: Playwright handles complex scenarios better (multi-tab, downloads, auth contexts), Cypress has better developer experience for simple cases. For a .NET backend team: Playwright's C# support is a strong advantage. In 2025, Playwright has become the industry default for new projects.

**Q: What are Playwright best practices?**
A: (1) Use user-facing locators: `getByRole`, `getByLabel`, `getByText` -- not CSS selectors or XPath. (2) Use `test.describe` for grouping, `test.beforeEach` for setup. (3) Use Page Object Model for maintainability. (4) Leverage auto-waiting (don't add manual waits). (5) Use `expect(locator).toBeVisible()` assertions. (6) Mock network when testing UI logic, use real backend for integration tests. (7) Use `storageState` for auth (login once, reuse across tests). (8) Run in CI with `--workers=4` for parallelism.

### Testing Library

**Q: What is Testing Library and how does it differ from Enzyme/traditional approaches?**
A: Testing Library (React Testing Library, Angular Testing Library, Vue Testing Library) tests components the way users interact with them. Philosophy: "The more your tests resemble the way your software is used, the more confidence they give you." Query by role (`getByRole('button', { name: 'Submit' })`), text, label -- not by class name, test ID, or component internals. No shallow rendering -- renders the full component tree. Fires real events (`userEvent.click`). Tests behavior, not implementation -- refactoring components doesn't break tests. Encourages accessible markup (querying by role means components must have proper ARIA roles).

---

## 10. Architecture Patterns

### Micro-Frontends

**Q: What are micro-frontends and when should you use them?**
A: Extending microservices to the frontend -- each team owns a vertical slice (frontend + backend) deployed independently. Implementation approaches: (1) **Module Federation** (Webpack 5) -- runtime JS module sharing between independently built apps, (2) **iframe-based** -- strong isolation but poor UX (no shared state, separate scroll), (3) **Web Components** -- custom elements as integration boundary, (4) **Server-side composition** -- Nginx/edge assembles HTML fragments. **When to use**: multiple teams working on large app, need independent deployment cycles, teams use different frameworks. **When NOT to use**: small team, single framework, added complexity outweighs benefits. Shared concerns: routing coordination, shared design system, authentication, performance overhead.

**Q: What are the challenges of micro-frontends?**
A: (1) Shared dependencies -- multiple React versions = bloated bundle; solve with shared scope in Module Federation. (2) CSS conflicts -- namespace or shadow DOM. (3) Routing -- need a shell app that coordinates. (4) Shared state -- event bus or shared store, adds complexity. (5) Testing -- E2E tests must span multiple micro-frontends. (6) Performance -- extra network requests, duplicate framework code. (7) Developer experience -- local development requires running multiple apps. For most teams, a well-structured monolith with clear module boundaries is simpler and sufficient.

### Web Components

**Q: What are Web Components and when would you use them?**
A: Browser-native component model with three specs: (1) **Custom Elements** -- define new HTML tags (`customElements.define('my-button', MyButton)`), (2) **Shadow DOM** -- encapsulated DOM subtree with scoped styles (no CSS leakage in or out), (3) **HTML Templates** -- `<template>` and `<slot>` for declarative structure. Use when: building a design system that must work across React, Angular, Vue, vanilla JS; micro-frontend integration boundary; third-party embeddable widgets. Limitations: no built-in state management, SSR support is limited, React has quirky interop (custom events, property vs attribute). Lit is the most popular library for building Web Components.

### WCAG & Accessibility

**Q: What are the key WCAG 2.1 principles and how do you implement them?**
A: POUR principles: **Perceivable** -- text alternatives for images (alt text), captions for video, sufficient color contrast (4.5:1 for normal text, 3:1 for large). **Operable** -- all functionality available via keyboard (no mouse-only interactions), no keyboard traps, skip-to-content links, focus management on route changes. **Understandable** -- clear language, consistent navigation, error identification with suggestions. **Robust** -- valid HTML, works with assistive technologies. Implementation: use semantic HTML first (`<nav>`, `<main>`, `<button>`, `<h1>`-`<h6>`), add ARIA only when semantic HTML is insufficient (`aria-label`, `aria-live`, `role`). Automated testing catches ~30% of issues (Axe, Lighthouse) -- manual testing with screen reader + keyboard is essential.

**Q: What ARIA attributes should every frontend developer know?**
A: `aria-label` -- text label when visible label is missing. `aria-labelledby` -- references another element as label. `aria-describedby` -- supplementary description. `aria-hidden="true"` -- hide decorative elements from screen readers. `aria-live="polite"` / `"assertive"` -- announce dynamic content changes. `aria-expanded` -- toggleable sections. `role="alert"` -- urgent notifications. `role="dialog"` -- modal dialogs (must trap focus). `aria-required`, `aria-invalid` -- form validation. Rule: prefer native HTML semantics over ARIA. `<button>` is better than `<div role="button">`.

### TypeScript for Frontend

**Q: What TypeScript patterns are important for frontend development?**
A: **Discriminated unions** for component props: `type Props = { mode: 'edit'; onSave: () => void } | { mode: 'view' }` -- TypeScript narrows type based on `mode`. **Generics** for reusable hooks/composables: `function useFetch<T>(url: string): { data: T | null; loading: boolean }`. **Strict mode** (`strict: true`) -- catches null/undefined errors at compile time. **Template literal types** for CSS/routing: `` type Route = `/users/${string}` ``. **Utility types**: `Partial<T>`, `Pick<T, K>`, `Omit<T, K>`, `Record<K, V>` for prop manipulation. **Type guards**: `function isError(x: unknown): x is Error` for runtime narrowing. **Satisfies operator** (TS 4.9): `const config = { ... } satisfies Config` -- validates type without widening.

**Q: How does TypeScript improve React/Angular/Vue development?**
A: **React**: typed props/state (`FC<Props>`), typed hooks (`useState<User>(null)`), typed event handlers (`React.ChangeEvent<HTMLInputElement>`), typed context. **Angular**: DI is fully typed, template type checking (strict mode), typed forms (`FormGroup<{ name: FormControl<string> }>`), typed HTTP responses. **Vue**: `<script setup lang="ts">` with `defineProps<{ title: string }>()`, typed composables, Pinia stores with full inference. TypeScript catches prop mismatches, missing required props, and incorrect event handler signatures at compile time rather than runtime.

---

## Sorulursa (Interview Q&A)

> [!question] "You're a backend engineer -- how comfortable are you with frontend?"
> I'm primarily backend, but I've worked with frontend throughout my career. I understand React component architecture, hooks, and state management. I've built features in Angular (signals, standalone components, RxJS). I know when to use SSR vs CSR vs SSG. I can read and modify frontend code confidently, set up proper testing with Playwright, and optimize Core Web Vitals. I'm not a CSS artist, but I understand the build pipeline, TypeScript patterns, and architectural decisions that matter at a senior level. I can pair effectively with frontend specialists and make informed decisions about frontend architecture.

> [!question] "How do you decide between SSR, CSR, SSG, and ISR?"
> It depends on the content type and freshness requirements. Blog/docs: SSG -- build once, serve from CDN, fastest possible. E-commerce product page: ISR -- pre-render at build, revalidate every 60 seconds for price changes. User dashboard: CSR -- authenticated, dynamic, no SEO needed. SEO-critical pages with real-time data: SSR with streaming. Most real apps mix strategies -- Next.js lets you choose per route. The key insight: don't SSR everything just because you can -- it adds server load. Don't CSR everything -- it hurts SEO and initial load.

> [!question] "What would you choose for a new frontend project and why?"
> Depends on the team and requirements. If the team knows React: Next.js with App Router (RSC, SSR, SSG, ISR built-in, excellent DX). If the team is .NET-heavy: Blazor with .NET 8 render modes (Server + WASM unified). If enterprise Angular shop: Angular 17+ with signals and standalone components. For all: TypeScript mandatory, Vite for build tooling, Tailwind for styling consistency, Playwright for E2E tests. The framework matters less than the team's expertise -- a well-built Angular app outperforms a poorly-built React app.

> [!question] "How do you approach frontend performance optimization?"
> Start with measurement: Lighthouse + Chrome DevTools + real user monitoring (Core Web Vitals). Fix the biggest bottleneck first. Common wins: (1) code splitting -- ship less JS on initial load, (2) image optimization -- WebP/AVIF, responsive srcset, lazy loading below fold, (3) font optimization -- font-display: swap, preload critical fonts, (4) bundle analysis -- find and eliminate large unused dependencies, (5) render strategy -- SSR/SSG for initial paint, hydrate only interactive parts. At architecture level: avoid client-side data waterfalls (fetch data on server), use streaming SSR, implement proper caching headers.

> [!question] "Explain micro-frontends. When would you recommend them?"
> Micro-frontends split a frontend into independently deployable pieces, each owned by a team. Module Federation (Webpack 5) is the most common runtime approach. I'd recommend them only when: (1) multiple teams (5+) need to deploy frontend changes independently, (2) the app is large enough that a single repo creates bottlenecks, (3) teams might use different frameworks. For most organizations, a well-structured monorepo with clear module boundaries gives 80% of the benefits without the complexity. The overhead of micro-frontends (shared dependencies, routing coordination, testing) is significant.
