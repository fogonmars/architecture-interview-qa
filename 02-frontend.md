# 100 Frontend Architecture Interview Questions (with answers)

Architect + **React-primary** handbook. Angular, Vue, and Lit appear as **peers**, not as a second Angular-100. Steal the **question**, not a logo. Drill in 90 seconds, then name the **failure mode**. Deep chapters: [frontend notebook](https://notepads-6389e.web.app/frontend/).

**Topics:** [Rendering](#rendering-csr-ssr-ssg-isr-rsc-hydration) · [Next vs Vite](#next-vs-vite) · [Angular vs React](#angular-vs-react-peers) · [State](#state-redux-query-context-ngrx) · [MFE](#micro-frontends-and-module-federation) · [Headless](#headless-cms-vs-coupled) · [BFF and APIs](#bff-graphql-vs-rest) · [Auth and XSS](#cookies-jwt-csp-xss) · [CWV](#core-web-vitals) · [a11y](#accessibility-wcag) · [Bundlers](#bundlers) · [Hosting](#nginx-cdn-aws-azure) · [Realtime](#sockets-sse-web-push) · [PWA / i18n / tokens / L7](#pwa-i18n-tokens-l7)

---
**Notebook:** [/frontend/](https://notepads-6389e.web.app/frontend/) · **DSA:** [06](06-dsa-leetcode.md) (FE) · **Mobile:** [10](10-mobile.md) · **Specialist:** [11](11-specialist.md)


## Rendering (CSR / SSR / SSG / ISR / RSC / hydration)

**1. What is CSR (client-side rendering)?**
The origin serves a shell HTML plus JS; the browser paints the UI after JavaScript fetches data. Honest for authenticated workspaces (HR, claims adjuster, admin) where crawlers and share cards do not need the first HTML to contain the document. Hosting is a static bucket or nginx — Node is optional and usually a BFF, not a renderer. Failure: a public PDP or paid-ad landing as Vite CSR so crawlers and WhatsApp see an empty `#root`.

**2. What is SSR (server-side rendering)?**
A server runs the view layer on the request (or cache miss) and returns HTML, then the client hydrates. Choose it when the URL is public or shareable **and** the first HTML depends on cookies, geo, or A/B. Uncached SSR that waits on six backends **is** your LCP; cache policy is the architecture, not “we use Next.” Failure: `Cache-Control: public` on HTML that included the user’s name.

**3. What is SSG (static site generation)?**
HTML is produced at **build** time and served from a CDN. Choose it when content is the same for everyone and changes on an editorial cadence: docs, brand, legal, careers. Build time is a product constraint — 10k pages × 50 ms is a painful CI, so paginate or generate paths, not the world. Failure: SSG of “my policies” dashboards or baking today’s FX rate into 80k pages until the next pipeline.

**4. What is ISR (incremental static regeneration)?**
Serve static HTML; after a time window or an on-demand tag/path revalidate, regenerate **that** path. Catalog, news, and help articles fit when stale seconds are a **business** SLA (often 30–300 s plus publish webhooks). Cart, session, and “stock = 1” as HTML truth do not. Failure: an ISR loader that read cookies and cached one user’s page for everyone.

**5. What are React Server Components (RSC)?**
Trees that render on the server and **never ship** to the client as JS, with Client Components as interactive islands. They are a **bundle and data-fetch** strategy, not a replacement for CDN cache, auth, or CWV. Use them where streaming HTML helps LCP on read-heavy public pages. Failure: `'use client'` on the god layout — a SPA with extra steps.

**6. How do you choose a rendering mode?**
Per **journey**, not per repo: is the URL ranked or shared; is HTML user-specific; how often does truth change; what host exists; what JS budget will hydration cost. Marketing SSG, PDP ISR plus a client price island, checkout private/no-store, admin CSR is a normal table. Write that table in an ADR. Failure: “the app is SSR” as a single decision.

**7. What is hydration?**
The browser attaches listeners and React (or Angular) reconciles server HTML with the first client render. Cost is **parse + reconcile**, not a free INP win. SSR that still ships a 1.2 MB SPA did not buy you interaction latency. Islands (Astro, disciplined RSC) hydrate only widgets that need it.

**8. What is a hydration mismatch (React #418)?**
Server HTML and the first client render disagree — clocks, `Math.random()`, geo banners from `window`, invalid HTML, or flags evaluated only in the browser. Checkout can look painted but the first click is dead. Fix: time/locale/flags from the **request** (cookie/header), or a client-only island for truly browser data. Failure: `suppressHydrationWarning` on the tree or `Date.now()` in an SSR header.

**9. What is streaming SSR?**
Send chrome first, then product, then slow reviews so the LCP element can paint before the worst backend. Pair with timeouts and fallback HTML, not an unbounded waterfall in one document. RSC streaming is the same idea with a server/client boundary. Failure: streaming a personalized document into a public cache.

**10. When should you refuse SSR?**
When SEO is zero (intranet, FNOL grids, agent desktops) and you would pay a Node fleet to hydrate PII tables Google must not see. Vite CSR plus a cookie BFF is the honest claims-portal default. SSR a public status page **path** if you later need shareable HTML — that path only.

**11. What is the hybrid production default?**
Route classes mix: SSG marketing, ISR catalog, SSR search or geo HTML with a defendable cache key, CSR/private SSR for account and checkout, CSR admin. “One mode for the monorepo” is how you either wreck SEO or wreck origin CPU. Architects name the **host** (CDN vs Node) next to the mode.

**12. How should cache keys treat geo, A/B, and login?**
Anonymous identical HTML: CDN. Geo: country in the URL or a cache key you can purge — not a cookie plus `public`. Logged-in: default **do not** cache HTML; cache API fragments. A/B in a cookie plus public cache means one bucket wins forever. Preview/draft must never hit the public cache.

**13. Why can’t you bet a PDP on crawlers running JS?**
Crawlers improved; paid social unfurls and many previews **do not** run your SPA. First HTML needs title, copy, `og:*`, and JSON-LD if you claim them. Status codes are an origin job — CSR that always returns 200 with “not found” in the client fails Search Console (soft 404).

**14. ISR vs live inventory?**
ISR is “fresh enough” anonymous HTML. Stock and payable price belong in a short-TTL client or edge call, or you sell air for 60 seconds. On-demand revalidate on price publish is for **catalog copy**, not a substitute for a quote API at checkout.

**15. What is the JS budget relationship to SSR?**
SSR improves TTFB and first HTML; it does not delete parse cost on mid Android. Fat hydration wrecks INP even when lab LCP looked fine. Architects measure field p75 and cut Client Components, not “add another image CDN” while origin TTFB is 1.8 s.

**16. Pages Router vs App Router?**
Pages: per-page data functions, familiar cache-as-props. App Router: RSC, streaming, `fetch` cache/tags — you **must** own the cache story or you origin-render the internet. Migrate by **route benefit**, not a conference rewrite. Failure: cargo-cult App Router on a stable Pages storefront with no tagged cache plan.

---

## Next vs Vite

**17. Next.js vs Vite — how do you decide?**
Next is a **rendering and hosting** decision (SSR/SSG/ISR, Node or a platform that runs it). Vite SPA is CSR artifacts on a CDN plus APIs/BFF. Public catalog/SEO: Next (or Astro/Nuxt). Authenticated console: Vite unless you have a real HTML-at-origin need. Failure: Next on an intranet HR app “because the JD said SSR,” or Vite CSR as the only public PDP.

**18. When is Vite the golden path?**
SEO does not matter, the team already ships SPA, and you do not want a Node farm in the request path. Pair with a BFF for cookies and aggregation. Preview, RUM, DS, and CSP still exist — Vite is not “no architecture.” Angular equivalent is a CLI CSR app, not Universal by default.

**19. When is Next (or Nuxt / Analog) justified?**
You need HTML in the first byte for SEO, Open Graph, or mixed public+session chrome, and someone will **operate** ISR cache, image optimization, and cache keys. Self-hosting Next means you own the ISR store across replicas. Vercel is one host, not the law.

**20. Where does Remix / React Router framework sit?**
Loaders/actions and nested routes are an honest peer when mutations and HTTP (`Cookie`, `Cache-Control`) are first-class (quote, checkout-ish). Next’s ISR product is the well-trodden 500k-PDP path. Fat loaders that call 12 services sequentially are the same TTFB scar as fat `getServerSideProps`.

**21. One Next app or two surfaces?**
A large SEO site plus a huge authenticated console often wants **two** apps: Astro/Next public, Vite console — unless the console is small and the team will own SSR cache keys. Unified DX is not worth coupling rendering classes. Budget one Node farm **or** static+functions well, not both poorly.

**22. Does “React” mean Next?**
No. React is a library; Next/Remix/Vite are runtimes. Estate gravity (K8s vs bucket vs IIS), auth, and team skill pick the runtime. Four metaframeworks across eight vendors with no BFF policy is an EA failure, not diversity.

---

## Angular vs React (peers)

**23. Angular vs React — how do you answer without a holy war?**
Constraints: existing estate, hiring, SSR need, design-system seam, who is here in five years. Architecture is rendering, BFF, tokens, and trains — framework is skill and ecosystem. “React is better” fails the room. “Rewrite 30 Angular apps to win an RFP” fails the programme.

**24. When does Angular win?**
The client already runs Angular 15+, the team is TypeScript/Java-shaped, and they want one opinionated path for HTTP, forms, DI, and scheduled majors. Banks and public sector often standardized here. Do not start Angular “because enterprise” with five people and no Angular leads. AngularJS 1.x is a strangler problem, not this win.

**25. When does React win?**
Greenfield with this job family’s hiring pool, mixed web + later RN, or Next/ISR ecosystem for SEO catalogs. You **must** choose router, server cache, and build — without a golden path you get four fetch styles. Fail: picking React because “it’s faster” with no CWV budget.

**26. Should you dual-run React and Angular on one journey?**
Default **no**. Stay on the estate framework; use React only for a **new** independent product with a hiring plan, or islands behind web components. Price the second toolchain and a five-year dual-run if the client still mandates React. Mixing AngularJS + React 19 without a proxy strangler is how you get two SSO cookies.

**27. Where do Lit / web components fit?**
The **contract** between hosts when Angular and React must coexist: tokens as CSS variables, primitives as custom elements, events versioned. Shadow DOM is not a free a11y pass. Lit is a poor choice as the only app framework for a 200-screen portal if you needed Next/Angular batteries.

**28. Vue as a peer?**
Vue 3 + Pinia + Nuxt is a valid golden path where hiring exists — same rendering and BFF laws. Adding Vue as a third runtime beside React and Angular without a seam is vendor chaos. Pinia is the Vue peer of RTK: client store, not the SKU SoR.

---

## State (Redux, Query, Context, NgRx)

**29. What kinds of state must you name?**
Server/remote (API cache), session (BFF cookie), URL (filters, locale, ids), client UI (modal, stepper), ephemeral form, device prefs, cross-app events. APIs and databases are the SoR — Redux is not a policy store. Skipping the taxonomy is how cart quantity lives in Redux **and** Query **and** Context.

**30. What is TanStack Query for?**
Server state as a **disposable cache**: TTL, keys, retries, invalidation. Keys are architecture (`['policy', id, locale, tenant]`). Default for REST/GraphQL in React when you are not already all-in on RTK Query. Failure: Query as an offline system of record, or mixing `de-DE` into `fr-FR` keys.

**31. When is Redux Toolkit (RTK) justified?**
Complex **client** workflows: quote configurator, multi-step FNOL, undo, cross-widget rules that are not GET caches. Toolkit (slices, Immer, listeners) is the only Redux you should write in 2026. Failure: duplicating `GET /policies` into slices — that is Query.

**32. When is React Context correct?**
Theme, locale, a session **handle** (user id, not the profile document), values that change rarely. Not cart ticks, keystrokes, or websocket storms — every consumer re-renders unless you split contexts with discipline most teams will not maintain. Context as a database is an INP and correctness bug.

**33. What is the store pattern (Redux / NgRx / Pinia)?**
One client container: current value + pure update (reducer) + dispatch of intents; effects/epics/thunks talk to the network **outside** the reducer. UI → dispatch → reducer → UI. Never fetch inside the reducer; never put the JWT or the only copy of a SoR document in the store. Official docs: Redux Toolkit, NgRx, Pinia.

**34. NgRx vs RTK — are they the same idea?**
Yes as **peers**: feature state, actions, pure reducers, effects for side effects, selectors/signals. Angular also has `resource`/http + signals for server cache — do not make NgRx the only HTTP pattern. Same rule: wizard in the store, policies in a cache.

**35. Redux vs TanStack Query for a claims app?**
Query (or RTK Query) for lists and policy/claim documents; RTK or XState for the FNOL wizard and dirty UI; cookie session, not JWT in the store. Cache keys include tenant+locale. Failure: GET payloads in Redux, or Query as the form.

**36. RTK Query vs TanStack Query?**
Pick **one**. RTK Query is honest when you already have RTK for client workflows or OpenAPI codegen into that store. Do not run both. Loaders (RR/Remix/Next) own route-owned fetch; combine with Query when many widgets share one entity.

**37. Why is the URL underrated state?**
Shareable, restorable, SEO-relevant filters, locale prefix, `claimId`, pagination belong in the location. Modal “help open” usually does not. Retail facets in the URL; insurance deep link to claim id yes.

**38. Where do forms live?**
React Hook Form / Angular reactive forms are a **local machine** until submit, then invalidate server cache. Do not put every keystroke in Redux. Retry on checkout/FNOL needs idempotency keys so double-submit is not double pay.

**39. Why no global Redux across MFEs?**
Version hell, silent desync, the hardest coupling layer. Each remote owns its Query cache; shell gets badge counts via versioned events (`add-to-cart.v1`). Optional `BroadcastChannel` for same-origin tabs. Lit shell theme is CSS variables, not React Context in the host.

**40. What about normalization?**
Three widgets showing `claimId` should hit **one** cache entry. Query keys do that. `createEntityAdapter` is for **client** collections you own. Retail identity is often `(country, sku)` or `offerId`, not sku alone. Do not fake an ORM of CMS pages unless you own the mutations.

---

## Micro frontends and module federation

**41. What is a micro frontend?**
A user-facing slice a team can **build, test, and deploy** without waiting on another train, while the user still sees one product. A folder in a monorepo that ships one artifact is modularity, not MFE. Independent deploy means host `N` can run with checkout `N+1` inside a compatibility window.

**42. When should you not use micro frontends?**
One squad, ~8 FE engineers, one product, same cadence forever, no platform owner, or “we might have more teams next year.” MFE pays for **organizational parallelism**. Eight people buy distributed coupling: four webpack configs and a worse LCP. Draw module boundaries so you can split later.

**43. What is module federation?**
A runtime `import()` of a remote entry (Webpack 5 / Rsbuild / Vite plugins). Shared libraries (`react`, `react-dom`, the DS) are **singletons** so you do not ship three Reacts. Remote URL is environment config; fallback UI when the remote 404s. SSR+federation is possible and painful — often keep remotes as CSR islands or use zones.

**44. Module federation vs npm packages?**
Packages are **libraries** (tokens, auth helper, logger) on a lockstep or semver train. Federation (or zones) is **independently deployed routes**. If trains are not independent, refuse MFE. Failure: federating Button atoms, `latest` remotes, double React.

**45. Federation vs Next multi-zones vs iframes?**
Zones: path prefix to another Next app — ops-simple, weaker shared header unless edge includes. Federation: one SPA navigation, runtime compose, Sev-1 if remoteEntry dies. Iframe: isolation for untrusted/legacy; a11y, resize, SEO, Apple Pay pain. Pick **one** compose style in year one.

**46. What must an MFE contract freeze?**
Routes, who owns session, DS major, namespaced events, locale from the shell, one RUM agent, error/timeout slots, published types. Version like an API (`mf-checkout@2`). Contract tests on the federated surface, not only unit tests inside the remote. Without a contract you have a distributed monolith.

**47. How does independent deploy actually work?**
Each remote builds to `/remotes/checkout/{gitsha}/`; the shell reads a **manifest** or flag for the live SHA. Rollback flips the pointer. One mutable `remoteEntry.js` is not independence. CI that still zips host+all remotes as one artifact is a modular monolith with extra failure modes.

**48. What does the shell own?**
HTML document, router chrome, auth session, RUM, shared versions, LCP of chrome, skip links and **one** focus system. Domain squads own remote UX and their BFF DTOs. If platform is “everyone’s 20%,” remotes will pin random React copies.

**49. Shared design system in an MFE estate?**
Tokens on `:root` in the shell; primitives **one** copy (npm or shared singleton). Do not federate the entire MUI bundle. a11y focus order across remotes is the shell’s problem. Four Buttons is not a platform.

**50. Different React majors as a goal?**
That is a tax (invalid hook call, duplicate Context). Same major, or wrap as web components. Vendor stuck on Angular 12 is procurement plus an iframe/exit date — architecture cannot paper it forever.

---

## Headless CMS vs coupled

**51. Headless vs coupled CMS?**
Coupled: WordPress/AEM **paints** public HTML; templates live in the CMS. Headless: CMS/commerce is JSON SoR; **your** React/Next/iOS app is the head. Use headless when many channels share a content model and the web team must ship UI without CMS releases. A 12-page brochure with happy Webflow editors does not need it.

**52. What is headless commerce?**
Cart, price, stock, checkout live in a commerce engine; CMS owns storytelling modules on the PDP; identity owns B2B contracts. Do not put price in the CMS except a campaign override with TTL. PCI: hosted fields/redirects, not homemade card inputs.

**53. When is coupled still right?**
Marketing org that lives in the CMS template model, one brand, no omnichannel JSON consumers. Headless without preview, webhooks, or cache budget ships stale or unpreviewed HTML. Editors who need pixel page-builders will hate structured JSON.

**54. Preview and publish architecture?**
Editors see **unpublished** content on **your** app’s preview URL (draft token, Next preview). Publish webhook revalidates **that slug**, not 80k PDPs. Draft must never hit the public cache. CMS down → last good ISR or static shell.

**55. Two systems of record on a PDP?**
CMS = narrative; PIM/commerce = SKU, price, stock. Front end composes with cache keys that know the difference. ISR member prices is a leak and a lie. Fallback locale chain is an operating rule, not a ternary in a leaf component.

**56. Is every SPA “headless”?**
No. Talking to your own Spring `/api/orders` is API-driven. Call it headless when a **content or commerce platform** is SoR for that slice. MACH/composable is a vendor slogan until you can name SoR, preview, and cache.

---

## BFF, GraphQL vs REST

**57. What is a BFF?**
A backend **for one frontend/channel** that shapes screen DTOs, aggregates chatty APIs, hides tokens, and owns the web session cookie. It is allowed to be UI-ugly. It is **not** the enterprise canonical API or the claims SoR. Next server loaders/RSC talking to internal APIs with a session **are** a BFF — you do not always need a second repo.

**58. BFF vs API gateway?**
Gateway: auth, rate limit, WAF, routing — generic. BFF: this dashboard needs four resources in one paint. Do not confuse them. APIM/API Gateway is not the domain.

**59. When do you skip a BFF?**
One CRUD resource, admin UI, gateway auth enough. Do not put all business rules in Express (monolith in denial). Do not let every squad’s BFF call every domain — that is a distributed monolith; add a domain API.

**60. GraphQL vs REST BFF?**
Start REST aggregates for the worst screens. GraphQL when **N clients + field selection** is real and you will fund DataLoader, complexity limits, and schema ownership. GraphQL is a product with an owner, not a default. Failure: GraphQL as BFF **and** SoR; unbounded queries.

**61. What does BFF orchestration look like in production?**
Parallel reads with `allSettled`, per-upstream timeouts inside the UX/LCP budget, retries only on idempotent GETs, partial `200` with `warnings[]` rather than a spinner forever. Money commands belong in a domain service; the BFF is not the transaction coordinator. Pass Idempotency-Key through for pay/FNOL.

**62. Web BFF vs mobile?**
Different shapes are normal — two BFFs or an explicit `channel`. Mobile is a separate OAuth **public** client; do not reuse the web confidential cookie client. Shared OpenAPI for resources you actually share.

**63. God BFF anti-pattern?**
It stores business SoR, grows every squad’s logic, and becomes the monolith you pretended to split. BFF is an experience adapter: auth, aggregate, strip PII. N+1 GraphQL without DataLoader is the same scar with a prettier query.

---

## Cookies, JWT, CSP, XSS

**64. Cookies vs JWT in localStorage?**
First-party web: OIDC **code on a confidential client** (BFF), `HttpOnly` `Secure` `SameSite` session cookie; JS never sees the refresh token. JWT is a **format**, not a storage strategy. Bearer in the browser is for native or APIs that cannot sit behind your origin. Failure: “JWT in localStorage” as modern.

**65. Why is localStorage for tokens a fail?**
XSS plus one script = persistent theft of access **and** refresh. Memory-only bearer still means XSS-as-user, but you do not persist the keys. Hybrid is normal: cookie to BFF, bearer only BFF→API. Never put tokens on query strings (CDN/WAF logs).

**66. What does CSRF require if you use cookies?**
Cookies ride on some cross-site requests. SameSite Lax/Strict, CSRF token or Fetch Metadata on mutating routes, GET without side effects. Bearer headers are not sent by naive foreign forms — that is why SPAs loved tokens, then stored them for XSS. `SameSite=None` for payment iframes **reopens** CSRF-shaped traffic.

**67. XSS vs HttpOnly — are you done?**
HttpOnly stops `document.cookie` exfil of the session id; XSS can still `fetch` as the user. Defense in depth: CSP, sanitizer, short session, step-up for money. React escaping is not a vaccine: `dangerouslySetInnerHTML`, Markdown, `javascript:` hrefs remain holes.

**68. What is CSP doing for the frontend?**
Content-Security-Policy limits which scripts, frames, and connections may run — reduces XSS blast radius and governs GTM/chat origins. Nonces/hashes beat `'unsafe-inline'` forever. Architects own script governance; every vendor tag in `<head>` is an INP and XSS budget.

**69. How do you handle CMS HTML safely?**
Named sanitizer (strict DOMPurify profile) with an owner; URL allowlists (`https` only); encode JSON in script tags so `</script>` cannot break out. Editor HTML is an XSS feed. ISR caching stored XSS turns the CDN into a worm.

**70. SPA public-client + PKCE vs BFF?**
Authorization code + PKCE if you truly have no first-party server. Implicit flow is dead. Prefer BFF for employee/customer **web** on your origin. MFE remotes must not grow a second login or pass bearer between remotes.

---

## Core Web Vitals

**71. What are Core Web Vitals?**
Field metrics at **p75**, usually mobile: **LCP** (largest paint), **INP** (interaction to next paint), **CLS** (layout shift). Google “good” bands: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 — common language, then tighten for 3G India if that is the market. Lighthouse on a laptop is not CrUX.

**72. What is LCP and how do you debug it?**
When the largest viewport element (hero, H1) finishes painting. Levers: TTFB (CDN/ISR/cached SSR), discover the LCP image in first HTML (`fetchpriority`, preload **that** URL), bytes (AVIF/`srcset`), do not hide it until JS. Name the LCP **element** per template in RUM. Failure: optimizing PNG while SSR cookie-bypass wrecks TTFB.

**73. What is INP?**
Latency from click/tap/key to the **next paint** that reflects it (replaced FID). Burned by long tasks, fat hydration, heavy handlers, third-party on `pointerdown`, 10k-row grids. Network wait is not INP if you paint a spinner immediately; 400 ms of reconcile with no paint **is**. Split JS; keep Client Components small.

**74. What is CLS?**
Unexpected layout shift. Reserve ads, images (width/height or aspect-ratio), fonts (`size-adjust` fallback), cookie banners **in flow** at first paint. Late banners and FOUT that reflow H1 hit LCP **and** CLS. Ads are layout citizens if they are contractual.

**75. Lab vs field?**
Lab (Lighthouse, local 4G profile) is a regression **signal**. Source of truth is RUM/CrUX p75 by template and country. CI budgets on **gzipped** bytes per **route class** (PDP ≠ admin). Kill the A/B banner first in a sale window; then bytes vs TTFB vs third-party.

**76. Who owns CWV?**
Template/squad owns the journey; platform owns RUM, budgets, golden path; product owns third-party tags. White screen with CDN 200 is a JS SLO, not uptime on `index.html`.

**77. Third parties and CWV?**
GTM, chat, A/B often **are** the INP/CLS budget. Consent is a render constraint: do not SSR `_ga` before consent; reserve banner space. Kill switches for remotes and tags belong on the edge/BFF so SSR matches CSR.

---

## Accessibility (WCAG)

**78. What is the a11y bar for enterprise web?**
**WCAG 2.2 Level AA** unless legal named otherwise (A is not enough; AAA is rare) — write it in the ADR. Budget 2.2 in product language: focus not obscured by sticky chrome, no drag-only, target size, help/autofill, and auth that works with password managers. Contrast 4.5:1 for normal text is a **token** problem, not a PDP ticket.

**79. Semantic HTML vs ARIA?**
Native `button`, `a href`, `label`, landmarks, heading order, tables for tabular data. ARIA when native cannot (tabs, combobox) — APG patterns, not `role="button"` on a `div`. If the accessibility tree says “unlabeled button,” the feature is incomplete.

**80. How do you run an a11y programme in 90 days?**
Freeze journeys with Legal; fix DS primitives (button, input, dialog, table); axe + keyboard in CI; screen-reader smoke on those journeys; PDF alternatives; dated evidence pack. Overlay widgets are a finding, not a control. Lawsuits care about **journeys**, not 100% automated score.

**81. MFE and accessibility?**
One focus system, skip links, and `h1` policy in the **shell**. Federated remotes stealing focus fail the product. Shadow DOM remotes still need accessible names. Vendor chat/maps/PDFs are **in** the conformance claim.

**82. Keyboard, SR, zoom?**
Tab order, visible focus, focus traps that restore, `aria-live` polite for toasts (do not steal focus every socket event). Zoom 200%/400% is in scope. Icon-only buttons need names. Placeholders are not labels.

---

## Bundlers

**83. Webpack vs Vite?**
The browser downloads the **prod** graph; HMR is a developer SLO. **Vite** for new CSR SPAs (esbuild dev, Rollup/Rolldown prod). **Webpack 5** when module federation or a loader museum is **this year’s** requirement. Choosing Webpack “because enterprise” with no remotes is tax. Measure prod split, not HMR bragging.

**84. What must a production bundler do?**
Resolve, transpile, tree-shake, **route-level** split, minify, **content-hash** filenames, extract CSS, emit maps for Sentry **not** public. Failure: `app.js` overwritten so users mix old HTML and new JS; `mode: development` in Jenkins; barrel files that pull all of lodash.

**85. Rollup, Rspack, Turbopack as peers?**
Rollup/Vite lib mode for the design system. Rspack/Rsbuild when a Webpack estate is too slow. Turbopack is a Next implementation detail — you own budgets, not a bank bet on a moving default. Angular CLI (esbuild in modern versions) — do not eject for fashion. Next: you own splits, not the bundler logo.

**86. Code splitting rule?**
Split on **journey boundaries** (`lazy` / dynamic import), not a `components/` folder. Vendor-split React if it versions slowly; too many tiny files still hurt INP. MFE: one React singleton, not React per remote. Charts off the PDP critical path.

---

## nginx, CDN, AWS, Azure

**87. What does nginx `try_files` do for an SPA?**
`try_files $uri $uri/ /index.html` so a refresh on `/claims/99` is not 404. Hashed `/assets/` should `try_files $uri =404` with long `immutable` cache; HTML is `no-cache`. **Never** map `/api/` through the SPA fallback — split `location /api/` to the BFF. Apache `FallbackResource`, IIS rewrite, Firebase/Vercel redirects are the same law.

**88. gzip vs brotli?**
Compress **text** (JS, CSS, HTML, SVG, JSON). Brotli often 15–25% smaller JS than gzip; gzip remains the universal fallback; send `Vary: Accept-Encoding`. Fail CI on **transfer** (compressed) kB of the LCP route. Dynamic gzip vs `gzip_static`/`brotli_static` vs CDN compress is ops, not a religion.

**89. What must you never gzip?**
JPEG, PNG, WebP, AVIF, **woff2**, mp4 — already compressed; you waste CPU and can enlarge. Measure budgets on compressed size: 900 KB raw vendor might be 280 gzip / 230 brotli.

**90. S3+CloudFront vs Blob+Front Door?**
Same jobs: hashed `dist/`, HTML no-cache, assets immutable, edge gzip/brotli, WAF, SPA 403/404→`index.html` **on the app behavior only**, not `/api`. OAC/OAI vs public buckets; Front Door identity vs anonymous containers. Cloud is estate gravity, not a rendering strategy. Invalidate HTML/`sw.js` on release, not every hashed object.

**91. SSR on AWS vs Azure?**
HTML from ECS/Fargate/EKS or App Service/Container Apps/AKS behind the **same** CDN for static chunks. Amplify vs Azure Static Web Apps is previews, Entra, and residency — not a different cache physics. Lambda@Edge as a BFF is the wrong size. Cookie must be **forwarded** or personalized SSR will cache the wrong user.

**92. Cognito vs Entra on the frontend?**
Workforce SSO is often Entra even on AWS. Customer CIAM is Cognito user pools or Entra External ID/B2C — **B2C ≠ employee tenant**. Frontend still: BFF cookies, no JWT in localStorage, no token in query strings. Easy Auth **plus** a second JWT in React is two session stories.

---

## Sockets, SSE, Web Push

**93. WebSocket vs SSE vs polling?**
Polling (30–60 s + ETag) for rare badges. **SSE** when server→client only (notifications, tokens of a RAG stream). **WebSocket** when bidirectional (chat, collab). Socket.IO/SignalR add fallback and rooms when the estate needs them. CMS banners are ISR, not a socket.

**94. Why can’t a socket notify a closed tab?**
The connection dies with the page. Closed-tab banners are **Web Push** (VAPID + service worker) or native/SMS/email. Open-tab OS banner is the Notifications API **after a user gesture**. Inbox in the DB is SoR; WS/SSE is a projection — reconnect backfills via REST.

**95. How do you architect claims notifications?**
Producer writes inbox **and** publishes (Redis/Kafka). Gateway authenticates upgrade (cookie or 30 s ticket — **not** JWT in the `wss://` query). Shell owns **one** connection; remotes get events. nginx: `Upgrade` for WS; disable buffering for SSE. Horizontal: Redis adapter, pings vs ALB idle timeout.

**96. RAG/chat UI transport?**
BFF streams **SSE**; model keys stay server-side; citations bound to retrieval ids; abort; no prompt PII in RUM. The model is not the SoR. Browser → OpenAI with a secret is a fail.

---

## PWA, i18n, tokens, L7

**97. PWA vs React Native?**
URL-enough employee/customer web: responsive site; add PWA (HTTPS, manifest, **service worker**) for install/offline/Android push. Store, camera-as-core, background location: RN/native/Flutter — React knowledge is not free Yoga, native modules, and App Store trains. Capacitor wraps a web app; it does not fix a 4 MB INP. Share BFF and **tokens** either way. A manifest without an SW is a bookmark.

**98. i18n and RTL for 12 locales?**
Do not collapse language, locale, country, and brand — `Accept-Language` is not a court. SEO wants locale in the URL (`hreflang`), not cookie-only. Use ICU messages (no concatenated sentences; Arabic plurals are not English+s). RTL is `dir` plus **logical** CSS (`inset-inline`), not `left`/`right` or a theme color. Copy lives in CMS/TMS; legal is country; run a pseudo-locale in CI.

**99. What are design tokens?**
Named primitive → semantic → component values (color, type, space, motion) compiled to CSS variables and theme objects. Figma is not a system; a **versioned package + owners + a11y gates** is. Multi-brand: brand is data, checkout logic does not fork. MUI vs Tailwind is a wrapper ADR; tokens are **A**. Angular gets the same tokens, not a fake React import. Raw hex in feature PRs is drift.

**100. What does L7 / programme leadership own that a senior does not?**
Senior owns **this app’s** rendering, state, and failure modes. L7 owns 2–5 squads + platform: golden path (two paths max per channel class), ARB on blast radius (MFE, auth, second React major), estimates from **journeys and integration** (SSO, CMS, i18n, a11y evidence — not “40 React pages”), presales assumptions, RAID/residual risk, CWV/a11y SLOs, vendor conformance. Staff platform; do not put module federation in the SOW unless independent trains are a stated constraint. Delivery is A for the commercial date; you are A for the numbers inside it.
