# 100 Angular Interview Questions (with answers)

Architect + Angular handbook. Questions are grouped by topic and progress from
fundamentals to advanced. Each answer is intentionally concise — follow [angular.dev](https://angular.dev) and the [frontend notebook](https://notepads-6389e.web.app/frontend/) to go deeper.

**Topics:** [Fundamentals](#fundamentals) · [Components](#components) ·
[Templates & data binding](#templates--data-binding) · [Directives](#directives) ·
[Pipes](#pipes) · [Signals & change detection](#signals--change-detection) ·
[Dependency Injection](#dependency-injection) · [Routing](#routing) ·
[Forms](#forms) · [HttpClient & interceptors](#httpclient--interceptors) ·
[RxJS](#rxjs) · [SSR & performance](#ssr--performance) · [Testing](#testing) ·
[Tooling & misc](#tooling--misc)

---

## Fundamentals

**1. What is Angular?**
A TypeScript-based, opinionated framework for building client-side (and SSR) web
apps, featuring components, dependency injection, routing, forms, and RxJS.

**2. Angular vs AngularJS?**
AngularJS (1.x) used `$scope` and two-way binding with digest cycles. Angular
(2+) is a complete rewrite: component-based, TypeScript-first, with a hierarchical
DI system and much better performance.

**3. What is a standalone component?**
A component that declares its own dependencies via `imports` and needs no
`NgModule`. It's the modern default. See `app.component.ts`.

**4. What is an NgModule and is it still needed?**
A container that grouped declarations/providers/imports. With standalone APIs it's
largely optional; still used for some libraries and legacy code.

**5. What is the difference between a component and a directive?**
A component is a directive *with a template*. Directives (attribute/structural)
add behavior to existing elements without their own view.

**6. What are the building blocks of an Angular app?**
Components, templates, directives, pipes, services, dependency injection, and (for
navigation) the router.

**7. What is metadata / a decorator?**
Decorators (`@Component`, `@Injectable`, `@Directive`, `@Pipe`) attach metadata to
a class telling Angular how to use it.

**8. What is `main.ts` / how does bootstrapping work?**
`bootstrapApplication(AppComponent, appConfig)` starts the app with a root
component and application-level providers. See `src/main.ts`.

**9. What is Ahead-of-Time (AOT) compilation?**
Templates are compiled to JS at *build* time (not in the browser), giving smaller
bundles, faster startup, and earlier template error detection. It's the default.

**10. What is tree-shaking?**
Dead-code elimination in the bundler. `providedIn: 'root'` services and standalone
imports are tree-shakable — unused code is dropped from the build.

---

## Components

**11. How do you pass data from parent to child?**
Via inputs: `@Input()` or the signal `input()`. See `child-counter.component.ts`.

**12. How do you emit events from child to parent?**
Via outputs: `@Output() EventEmitter` or the signal `output()`; call `.emit(value)`.

**13. What is `input.required()`?**
A signal input that must be provided by the parent or Angular throws at runtime.

**14. What is an input transform?**
`input(value, { transform })` coerces/normalizes the incoming value (e.g. string→
boolean for attribute presence).

**15. What is `model()`?**
A two-way bindable input+output pair enabling `[(value)]` on a custom component.

**16. What is content projection?**
Rendering parent-supplied markup into `<ng-content>` slots (default or named via
`select`). See `card.component.ts`.

**17. What's the difference between view queries and content queries?**
`viewChild`/`viewChildren` query THIS component's own template;
`contentChild`/`contentChildren` query PROJECTED content.

**18. List the lifecycle hooks in order.**
`ngOnChanges` → `ngOnInit` → `ngDoCheck` → `ngAfterContentInit` →
`ngAfterContentChecked` → `ngAfterViewInit` → `ngAfterViewChecked` → `ngOnDestroy`.

**19. When does `ngOnInit` run vs the constructor?**
Constructor runs at instantiation (DI wiring). `ngOnInit` runs once after the
first `ngOnChanges`, when inputs are set — the right place for init logic.

**20. What is `ViewEncapsulation`?**
How component styles are scoped: `Emulated` (default, attribute-based), `None`
(global), `ShadowDom` (native shadow DOM).

**21. What is `exportAs`?**
Lets a template reference a directive/component instance: `#ref="exportAsName"`.

**22. What are host bindings/listeners?**
`@HostBinding`/`@HostListener` (or the `host` metadata) bind properties/attrs and
subscribe to events on the component's own host element.

**23. What are `hostDirectives`?**
Compose behavior from other directives onto a host without inheritance
(Angular 15.1+).

**24. Why prefer `OnPush`?**
It limits change detection to input reference changes, events, async pipe
emissions, and signal changes — big performance gains.

**25. How do sibling components communicate?**
Through a shared service (signal store or `Subject`), the router, or a common
parent. See `cart-state.service.ts`.

---

## Templates & data binding

**26. What are the types of data binding?**
Interpolation `{{ }}`, property `[prop]`, attribute `[attr.x]`, class `[class.x]`,
style `[style.x]`, event `(event)`, and two-way `[(ngModel)]`.

**27. What is the difference between `[prop]` and `attr.prop`?**
`[prop]` binds a DOM *property*; `[attr.x]` binds an HTML *attribute* (needed for
things without a DOM property, e.g. `colspan`, ARIA).

**28. What is the new control flow syntax?**
Built-in `@if`, `@for` (with required `track`), `@switch`, and `@defer` — replacing
`*ngIf`, `*ngFor`, `*ngSwitch`.

**29. Why is `track` required in `@for`?**
It identifies items so Angular can reuse DOM nodes instead of recreating them —
correctness and performance.

**30. What is `@defer`?**
Deferred/lazy template loading with triggers (`on idle`, `on viewport`, `on
interaction`, etc.) plus `@placeholder`/`@loading`/`@error` blocks.

**31. What is `ng-template`?**
A block of template that isn't rendered until instantiated (used by structural
directives, `@defer`, `ngTemplateOutlet`).

**32. What is `ng-container`?**
A logical grouping element that renders no DOM — handy for structural directives
without adding a wrapper node.

**33. What is `$event`?**
The payload of an event binding — a DOM event for native events, or the emitted
value for a custom `output()`.

**34. What is a template reference variable?**
`#name` gives you a reference to a DOM element, component, or directive within the
template.

**35. What is safe navigation `?.` in templates?**
The elvis operator guards against null/undefined: `user?.name` renders nothing if
`user` is nullish.

---

## Directives

**36. Attribute vs structural directive?**
Attribute changes appearance/behavior of an element (`ngClass`); structural adds/
removes DOM using the `*` syntax (`*ngIf`, `*appUnless`). See `shared/directives`.

**37. How does the `*` desugar?**
`*appUnless="x"` becomes `<ng-template [appUnless]="x">…</ng-template>`.

**38. How do you build a structural directive?**
Inject `TemplateRef` + `ViewContainerRef`, then `createEmbeddedView()` / `clear()`.
See `unless.directive.ts`.

**39. What is the structural directive microsyntax?**
The compact `*dir="expr as var; context"` grammar that maps to template inputs and
context variables.

**40. Name some built-in directives.**
`NgClass`, `NgStyle`, `NgModel`, `RouterLink`, `RouterOutlet`, and (legacy) `NgIf`,
`NgForOf`, `NgSwitch`.

---

## Pipes

**41. What is a pipe?**
A template transform: `{{ value | pipe:arg }}`. See `truncate.pipe.ts`.

**42. Pure vs impure pipe?**
Pure (default) is memoized and re-runs only when the input reference changes;
impure (`pure: false`) runs every change-detection cycle.

**43. What is the `async` pipe?**
Subscribes to an Observable/Promise, renders the latest value, and auto-
unsubscribes on destroy — preventing memory leaks.

**44. Why can filtering/sorting in a pipe be a problem?**
Pure pipes won't react to in-place mutations, and heavy work runs on the render
path; Angular recommends doing it in the component. See `filter-by.pipe.ts`.

**45. Name some built-in pipes.**
`DatePipe`, `CurrencyPipe`, `DecimalPipe`, `PercentPipe`, `JsonPipe`, `SlicePipe`,
`UpperCasePipe`, `KeyValuePipe`, `AsyncPipe`.

---

## Signals & change detection

**46. What is a signal?**
A reactive value container; reading it in a reactive context tracks it, and
updating it notifies consumers. See `signals`.

**47. `signal` vs `computed` vs `effect`?**
`signal()` is writable state; `computed()` is derived, memoized state; `effect()`
runs side-effects when read signals change.

**48. How do you update a signal?**
`sig.set(v)` (replace) or `sig.update(fn)` (derive from current). `computed`s are
read-only.

**49. What is `allowSignalWrites`?**
By default writing to a signal inside an `effect` is disallowed (avoids loops);
pass `{ allowSignalWrites: true }` to opt in. See `core-concepts.component.ts`.

**50. How does change detection work?**
Zone.js patches async APIs and triggers change detection; Angular walks the
component tree checking bindings. `OnPush` prunes that walk. Signals enable more
granular, zoneless-friendly updates.

**51. What is zoneless change detection?**
An experimental mode (`provideExperimentalZonelessChangeDetection`) where signals/
events drive updates without Zone.js.

**52. What is `toSignal` / `toObservable`?**
RxJS interop: consume an Observable as a signal, or turn a signal into an
Observable. See `cart-state.service.ts` and `product-list.component.ts`.

**53. How do signals interact with `OnPush`?**
A signal read in a template marks that view dirty when the signal changes, so
`OnPush` components update without manual `markForCheck()`.

**54. What is `markForCheck()` / `detectChanges()`?**
`ChangeDetectorRef.markForCheck()` schedules a check up the tree (OnPush);
`detectChanges()` runs one synchronously.

**55. What is `trackBy` / `track`?**
Identity function for lists so Angular reuses DOM nodes; `track` is its required
form in the new `@for`.

---

## Dependency Injection

**56. What is dependency injection?**
A pattern where a class receives its dependencies from an injector instead of
creating them, improving testability and reuse. See `guide/di`.

**57. What are the provider recipes?**
`useClass`, `useValue`, `useFactory` (with `deps`), and `useExisting` (alias). See
`dependency-injection.reference.ts`.

**58. What is an `InjectionToken`?**
A runtime-safe, typed key to inject non-class values (config, primitives). See
`app-config.token.ts`.

**59. `inject()` vs constructor injection?**
Both retrieve dependencies. `inject()` works in field initializers and functional
guards/interceptors; constructor injection is the classic form.

**60. What does `providedIn` control?**
Where/how a service is registered: `'root'`, `'platform'`, `'any'`, or a module —
governing singleton scope and tree-shaking.

**61. What are the resolution modifiers?**
`@Optional()`, `@Self()`, `@SkipSelf()`, `@Host()` (and `inject()` options
`optional/self/skipSelf/host`) control where the injector looks.

**62. What is a hierarchical injector?**
Injectors form a tree (root → route → component); lookups bubble up until a
provider is found, enabling scoped overrides.

**63. What is a multi-provider?**
`{ provide: TOKEN, useValue: x, multi: true }` collects many values into an array
under one token (e.g. interceptors, validators).

**64. What are `viewProviders`?**
Providers visible to a component's own view but NOT to projected content.

**65. How do you scope a service to a feature?**
Provide it in a route's `providers` array or a component's `providers` — a new
instance is created per that injector.

---

## Routing

**66. How do you define routes?**
A `Routes` array with `path`/`component` (or `loadComponent`), passed to
`provideRouter`. See `app.routes.ts`.

**67. `loadComponent` vs `loadChildren`?**
`loadComponent` lazy-loads a single standalone component; `loadChildren` lazy-loads
a set of child routes (whole feature) as a chunk.

**68. What are the guard types?**
`CanActivateFn`, `CanActivateChildFn`, `CanDeactivateFn`, `CanMatchFn`, and
resolvers (`ResolveFn`). See `routing.reference.ts`.

**69. `canMatch` vs `canActivate`?**
`canMatch` runs before matching (a failure lets the router try the next route and
can gate lazy loading); `canActivate` runs after matching, before activation.

**70. What is a resolver?**
A `ResolveFn` that pre-fetches data before a route activates; the value lands in
`route.data`. See `product.resolver.ts`.

**71. How do you pass data between routes?**
Route params `:id`, query params `?x=`, fragment `#x`, static `data`, `resolve`,
router `state`, and matrix params.

**72. What is `withComponentInputBinding()`?**
A router feature that binds route params/query/data directly to component inputs of
the same name.

**73. What is a named (auxiliary) outlet?**
A secondary `<router-outlet name="x">` targeted by routes with `outlet: 'x'` and
URLs like `/path(x:route)`.

**74. `pathMatch: 'full'` vs `'prefix'`?**
`'full'` matches only when the entire URL equals `path` (needed for `''`
redirects); `'prefix'` (default) matches when the URL starts with `path`.

**75. How do you preload lazy modules?**
`provideRouter(routes, withPreloading(PreloadAllModules))` or a custom preloading
strategy.

**76. `routerLink` vs `router.navigate()`?**
`routerLink` is declarative (in templates); `navigate`/`navigateByUrl` are
imperative (in code), both accepting `NavigationExtras`.

**77. How do you read route parameters?**
Inject `ActivatedRoute` and read `paramMap`/`queryParamMap`/`data` (as snapshots or
observables), or bind them to inputs.

**78. What is the wildcard route?**
`{ path: '**', component: NotFound }` — matches anything unmatched; must be last.

---

## Forms

**79. Reactive vs template-driven forms?**
Reactive: model defined in the component (`FormGroup`), explicit and testable.
Template-driven: model inferred from the template via `ngModel`. See `forms-demo`.

**80. What are `FormControl`/`FormGroup`/`FormArray`?**
A single field, a keyed group of controls, and a dynamic list of controls,
respectively.

**81. How do you add validation?**
Built-in `Validators` (required, minLength, email…), custom `ValidatorFn`, async
validators, and cross-field group validators. See `forms.reference.ts`.

**82. What is `updateOn`?**
Controls when a control's value/validity updates: `'change'` (default), `'blur'`,
or `'submit'`.

**83. `setValue` vs `patchValue`?**
`setValue` requires the full shape; `patchValue` updates a subset.

**84. What is `getRawValue()`?**
Returns values including DISABLED controls (which `value`/`patchValue` omit).

**85. What are typed forms?**
Angular 14+ forms infer strict types for values/controls, catching shape errors at
compile time (`NonNullableFormBuilder` avoids `null`).

**86. How do you build a custom form control?**
Implement `ControlValueAccessor` (writeValue, registerOnChange, registerOnTouched,
setDisabledState) and register it as an `NG_VALUE_ACCESSOR`.

---

## HttpClient & interceptors

**87. How do you make HTTP requests?**
Inject `HttpClient` and call `get/post/put/patch/delete`, which return Observables.
See `product.service.ts`.

**88. What is an interceptor?**
A function every request/response passes through — for auth, logging, caching,
errors, retries. See `core/interceptors`.

**89. How are functional interceptors registered?**
`provideHttpClient(withInterceptors([a, b]))`; they run in array order.

**90. How do you cache HTTP responses?**
Return a cached response via `of(...)` on a hit to skip the network; store on a
miss with `tap`. See `cache.interceptor.ts` + `cache.service.ts`.

**91. What are the `observe` and `responseType` options?**
`observe`: `'body'`|`'response'`|`'events'`; `responseType`:
`'json'`|`'text'`|`'blob'`|`'arraybuffer'`. See `http.reference.ts`.

**92. What is `HttpContext`?**
A per-request key/value bag (via `HttpContextToken`) to pass metadata to
interceptors (e.g. "skip cache").

**93. How do you test HTTP code?**
`provideHttpClientTesting()` + `HttpTestingController` to assert requests and flush
fake responses. See `product.service.spec.ts`.

---

## RxJS

**94. What is an Observable vs a Promise?**
An Observable is a lazy stream of 0..∞ values over time, cancellable and
composable; a Promise is a single eventual value.

**95. Subject vs BehaviorSubject vs ReplaySubject?**
`Subject` multicasts with no memory; `BehaviorSubject` holds a current value for
new subscribers; `ReplaySubject` replays the last N values. See `rxjs.reference.ts`.

**96. `switchMap` vs `mergeMap` vs `concatMap` vs `exhaustMap`?**
switch = cancel previous (search); merge = parallel; concat = queue in order;
exhaust = ignore new while busy (double-submit guard).

**97. How do you avoid memory leaks with subscriptions?**
Use the `async` pipe, `takeUntilDestroyed()`, or `takeUntil(destroy$)` — or convert
to signals with `toSignal`.

**98. What does `shareReplay` do?**
Multicasts one execution and replays the last value(s) to new subscribers — avoids
duplicate HTTP calls. See `product.service.ts`.

---

## SSR & performance

**99. What is SSR and why use it?**
Server-Side Rendering renders the app to HTML on the server for faster first paint
and SEO; the client then *hydrates* it. See `server.ts`, `app.config.server.ts`.

**100. What is hydration and what is `@defer`/lazy loading good for?**
Hydration reuses server-rendered DOM instead of re-rendering (`provideClientHydration()`).
Lazy loading (`loadComponent`/`loadChildren`) and `@defer` shrink the initial
bundle so the app starts faster.

---

## Testing

*(Bonus — see the [Testing section of the README](README.md#14-testing) and the
`*.spec.ts` / `e2e/*.spec.ts` files.)*

- **Unit tests** (Jasmine + Karma + `TestBed`): isolate a class/service/pipe.
- **Component tests**: render with `ComponentFixture`, simulate clicks/input,
  assert the DOM.
- **HTTP tests**: `HttpTestingController` mocks the backend.
- **E2E tests** (Playwright): drive the real app in a real browser; mock the
  network with `page.route()`.

---

## Tooling & misc

- **Angular CLI**: `ng new`, `ng generate`, `ng serve`, `ng build`, `ng test`.
- **Dev proxy**: `proxy.conf.json` forwards `/api` in development.
- **Prod/SSR proxy**: Express `http-proxy-middleware` in `server.ts`.
- **Build**: AOT + esbuild/Vite-based application builder, budgets, and
  prerendering.

> Study tip: for each question, open the referenced file in this repo and trace
> the real code. Understanding beats memorizing.
