# 100 Backend Interview Questions (with answers)

Architect + Java / Go / Node handbook. Steal the **question**, not Netflix’s stack.
Each answer is 2–6 sentences. Failure modes sit in the last sentence when they
earn the space. Deeper chapters: [backend notebook](https://notepads-6389e.web.app/backend/)
and scenario drills in [29](../backend/29-interview/README.md) and
[34](../backend/34-java-go-working-architecture/README.md).

**Topics:** [Runtimes](#runtimes) · [HTTP contracts](#http-contracts) ·
[Shapes & DDD](#shapes--ddd) · [Deployables & edge](#deployables--edge) ·
[Data access](#data-access) · [Messaging](#messaging) ·
[Sagas & idempotency](#sagas--idempotency) · [Redis](#redis) · [Identity](#identity) ·
[Resilience](#resilience) · [Observe, k8s, realtime](#observe-k8s-realtime) ·
[Tenancy, compliance, BaaS](#tenancy-compliance-baas)

---

## Runtimes

**1. When do you pick Java vs Go vs Node for a new API?**
Map **workload, estate, and who pages** — not a conference ranking. Java (or Kotlin on the JVM) wins thick domain and an existing JVM ops/hiring pool. Go wins ingest, proxies, and many connections with small RAM. Node wins BFF/GraphQL glue when the same people own the SPA. Freeze the system of record first; do not add a third language on a hiring freeze.

**2. How does the same hexagonal use-case look in Java, Go, and Node?**
Inbound HTTP is an adapter (Spring controller, `net/http` handler, Fastify/Nest). Domain `ApproveLeave` talks only to ports: repo, clock, events. Outbound adapters implement SQL and outbox. If the domain imports `HttpServletRequest`, `gin.Context`, or `Express.Request`, you do not have a domain.

**3. What is the JVM’s default danger in production?**
Heap, GC pauses, and **thread-pool / connection-pool exhaustion**. RSS is larger than `-Xmx`; size the heap to the cgroup. Virtual threads (21+) make blocking JDBC acceptable again only if the **DB pool** is still bounded. Failure: one playbook that treats a GC death like a Node loop stall.

**4. What is Go’s default danger?**
Forgetting `context` cancel and spawning **unbounded goroutines**. Leaks show as goroutine count and blocked mutex/net in pprof, not as a GC graph. Small binaries do not excuse missing timeouts. Failure: a rewrite-to-Go during a Sev-1 because “Go is faster.”

**5. What is Node’s default danger?**
The **event loop** plus a small `libuv` threadpool. Sync CPU, giant JSON parse, or blocking fs on the request path stalls **everyone**. TypeScript erases at runtime — validate at the edge. Failure: zipping 200MB PDFs or scoring claims on the loop and calling it a backend.

**6. Threads vs goroutines vs the event loop — what is actually different?**
A JVM thread (platform or virtual) is a concurrent unit that can block; you pay with pools and heap. A goroutine is cheap multiplexed concurrency; you still must bound and cancel. Node is **one loop per process** (cluster for cores): IO is multiplexed, CPU is not. Same SLO; different levers: dump/GC vs pprof vs loop delay.

**7. Why don’t virtual threads mean more database connections?**
Loom multiplexes waiting in the JVM; Postgres still has `max_connections` and Hikari still has a size. One virtual thread per request that each holds a connection still saturates the pool. Size pools to the database, not to fashion. Failure: “unlimited virtual threads” with a pool of 200 against a 100-connection primary.

**8. How do you diagnose p99 explosion across three runtimes?**
Classify **runtime physics** before the language war. JVM: GC pause and heap. Node: event-loop delay. Go: goroutine count and blocked syscalls. Mitigate first (rollback, shed load); bound later. Failure: one runbook for all three, or proposing a rewrite at T+20 minutes.

**9. When is polyglot honest?**
When bounded contexts are **separately deployable** and you fund N on-call skillsets: Java SoR, Node BFF, Go ingest is a normal estate. It is dishonest when three languages share one process and one memory. Contracts (OpenAPI, protobuf, AsyncAPI) are the interop — never a shared Hibernate session across a network hop.

**10. Is Nest “enterprise Node” the way Spring is enterprise Java?**
Nest is a **structure** (modules, DI) that looks like Spring. It does not give you JVM maturity, JTA, or the same hiring pool. Use it when the Node team needs rails, not because the folder layout looks bank-ready. Failure: picking Nest to win an ARB while the SoR still lives in Express handlers.

**11. Why is Node usually the wrong ledger?**
Money needs bounded pools, mature transactions, and an ops culture that already pages a JVM or Go binary. The event loop plus CPU adjacent to settlement is a stall waiting to happen. Node as BFF in front of a Java/Go SoR is the honest split. Failure: Express inventing claims amounts.

**12. Why not rewrite working Java payroll in Go for a blog post?**
Profile first — the bottleneck is usually the DB, N+1, or missing indexes. A rewrite adds a language, an on-call, and a dual-run you may never finish. Keep hexagonal ports so a **worker** can move later without moving the ledger. Failure: Go as fashion while payroll still dual-writes.

**13. What must you still have on a single-process service?**
Timeouts on outbound calls, transactions, structured logs, Postgres backups, and a runbook for disk-full and OOM. Single-host is **rung 1**, not amateur hour. Failure: skipping timeouts because “we will never scale.”

**14. How do you place a BFF vs the SoR by language?**
SoR writes usually stay Java or Go. The BFF is often Node because the FE org pages it — Java or Go BFF is equally valid. The BFF holds the browser session and aggregates; it does not own payroll. Failure: three languages in one repo with no ownership.

**15. What does “runtimes are peers” mean in an interview?**
Patterns — hexagonal, outbox, timeouts, idempotency — are identical; skins differ. Interviewers want **placement** (estate, physics, who pages), not “enterprise = Spring.” Name residual risk for the choice you made. Failure: ranking frameworks before naming the system of record.

---

## HTTP contracts

**16. REST vs gRPC vs GraphQL — how do you choose?**
If a human or UI **waits**, you need a sync contract. REST + OpenAPI is the default for CRUD, cacheable HTTP, browsers, and partners. gRPC (or Connect) wins low-latency internal typed RPC and streams. GraphQL wins many clients and sparse fields **if** you budget complexity and per-field authz. If the fact already happened, that is messaging — not another RPC.

**17. What is an honest enterprise REST default?**
Richardson level 2: resources, verbs, status codes, plus OpenAPI and **Idempotency-Key** on money POSTs. HATEOAS is rare for SPA backends; do not fail an ARB for missing `Link` headers. Version by additive JSON first. Failure: HTTP as a SOAP tunnel (one POST to rule them all) celebrated as REST.

**18. Which HTTP methods are idempotent, and why does POST need extra work?**
GET/HEAD are safe; PUT/DELETE are idempotent by spec. PATCH is not inherently idempotent — use `If-Match` or you double-apply. POST is not idempotent unless you **make** it so with a key or natural unique. Gateways that blindly retry POST double-pay.

**19. How should you version a public HTTP API?**
Prefer additive, optional fields. URL `/v1` is for rare breaking public partners, not a lifestyle of `/v3`. Header versioning needs documentation. Give consumers you do not compile with a **sunset window**, not a Friday field delete.

**20. What is gRPC actually for, besides “faster REST”?**
Protobuf contracts, generated stubs, HTTP/2, and **deadlines as cancel**. Unary for RPC CRUD; server-stream for feeds; bidi when both talk. Browsers are not native — use gRPC-Web or Connect. Failure: infinite server stream, client gone, thread/goroutine lives forever.

**21. Why does every gRPC call need a deadline?**
No deadline is a leak: the callee keeps working after the caller left. Propagate remaining time so a 10s query does not start with 20ms left. Map gRPC codes to HTTP at the edge; do not leak raw codes to a SPA. Failure: load-balancing HTTP/2 poorly and blaming protobuf.

**22. When does GraphQL become an N+1 and authz hole?**
One round trip for the SPA is the win; resolvers that hit the DB per field are the loss. Authz must be **per field**, not a single JWT at the gateway. Persist queries and complexity limits in enterprise. Failure: GraphQL as a public dump of the schema with no budget.

**23. GraphQL gateway vs BFF aggregation — same job?**
Both shape a client graph. A BFF can aggregate REST without a schema war. Federation is an **org** contract across teams, not a shortcut around field authz. Failure: stitching three SoRs in resolvers and calling it the domain model.

**24. Why aren’t Kafka topics named after REST verbs?**
Events are **facts that already committed** (`ClaimOpened`), not `UpdateClaimCommand` as a synchronous bus. RPC is for a waiting caller; the log is a projection feed. The ledger stays in the DB. Failure: topic-per-table and compacting money away.

---

## Shapes & DDD

**25. What is layered (N-tier) architecture, and when is it honest?**
Controller → application service → (domain) → repository → DB. Honest for CRUD, a small team, one database, and Spring/JPA gravity. Rot is fat controllers and 800-line transaction scripts that leak `EntityManager` / Prisma to HTTP. Layered is wrong when the web layer **is** the domain.

**26. What is hexagonal architecture (ports and adapters)?**
The application exposes **ports** (use-cases in, repository/events out). Adapters implement HTTP, SQL, Kafka. You can fake Postgres in tests and swap REST for a queue consumer without rewriting policy. Dependencies point **toward** domain, not toward Spring, Gin, or Express.

**27. Hexagonal vs Clean/Onion — is the fight worth an ARB?**
Same arrow rule: entities/use-cases in the middle, frameworks at the edge. Clean is a diagram brand; hexagonal is the same idea with different slides. Fight whether domain imports the web framework, not the slide title. Presenter hierarchies for JSON APIs are usually theatre.

**28. Where do HTTP middleware and authz belong?**
Middleware is a **pipeline of adapters**: CORS, request-id, authn, timeouts. Authorization that needs the aggregate belongs in the **use-case**, not only in a gateway claim. Java filters, Go `http.Handler` wraps, and Express middleware are skins of the same pipeline.

**29. Vertical slices vs technical layers?**
Package by feature (`leave`, `payroll`) each with its adapters, or global `controllers/` / `services/` / `repos/`. Vertical slices match bounded contexts and make extraction possible. Technical layers scale copy-paste across the whole app. Prefer slices once more than one team touches the monolith.

**30. What is a DDD bounded context?**
A **linguistic and model boundary**: “Customer” in billing is not “Customer” in support. Inside, one ubiquitous language and one model; outside, explicit translation. It is the candidate for a module or, later, a service with its own database. Failure: one giant Enterprise Customer entity shared by every team.

**31. Bounded context vs deployable vs database — which split first?**
Start with a **module** boundary (packages, `internal/`, lint). Extract a process when you have an independent **release train** and an independent **data** boundary. Newman: if you cannot extract a database (or a schema with no cross joins), you cannot extract a service. Failure: Helm charts around one schema.

**32. What is an aggregate, and why does it matter for transactions?**
A cluster of entities with a consistency boundary and a root you load and save together. One use-case, one commit, one aggregate unless the outbox row lives in the **same** SoR. Do not `@Transactional` a controller that calls three remote services. Failure: locking the whole company in one “Unit of Work.”

**33. What is an anti-corruption layer (ACL)?**
A translation layer so your model does not ingest COBOL/SOAP field names and nulls. New JSON FNOL talks to your types; the adapter talks to CICS. Dual-run checksums until the old SoR can retire. Failure: big-bang rewrite of 400 SOAP operations.

---

## Deployables & edge

**34. Modular monolith vs microservices — how do you choose?**
Microservices are an **org and data** architecture, not a Spring Cloud feature. Stay a modular monolith (ArchUnit / Go `internal` / package exports) until writes and release trains actually split. Eight engineers and one payroll DBA do not need Netflix. Failure: service per table.

**35. What is a distributed monolith?**
Many processes, still one database (or a shared entity JAR that locks every release). You pay latency, versioning, and tracing without independent deploys. Shared DB + many Helm charts is the classic. Extract data first, or stay one binary.

**36. What does a minimum viable microservice look like?**
One bounded context, one SoR, one team that pages, contracts (OpenAPI/protobuf/AsyncAPI), timeouts, outbox, idempotency. Different runtime is allowed (Go ingest vs Java policy) when that split is real. Failure: `UserService` that only CRUDs users.

**37. What is the honest enterprise hybrid?**
A core SoR modular monolith (often Java), a BFF (often Node), workers/ingest (often Go), and packaged systems behind an ACL. That is three or four deployables with reasons — not fifty entity services. A Node BFF plus a Java core is already two processes without a mesh of tables.

**38. API gateway vs BFF vs domain — who owns what?**
Gateway = edge: TLS, WAF, authn **shape**, routing, quota. BFF = payload shape for **one client family**. Domain = SoR and business rules. Do not merge them on a slide. Failure: eight Kong plugins of `if manager then` discounts.

**39. Why must the SPA not call twelve microservice URLs?**
That **is** the BFF’s job: cookie session in, aggregate with timeouts, tokens not in JavaScript. Mobile is another client — another BFF or a dedicated API, not the web cookie jar. Failure: Bearer in `localStorage`; SOAP from the browser.

**40. Can the BFF be the system of record for money?**
No. The BFF is confidential-client glue: OIDC code + PKCE, httpOnly session, on-behalf-of or service identity to the core. Java/Go keep writes. Failure: inventing leave balances in Express because the SPA needed one round trip.

**41. What is a normal single-VM deploy (rung 1)?**
One Spring Boot JAR **or** one Go binary, Postgres, **nginx** (TLS reverse proxy) to localhost `:8080`, **systemd** (or Compose: app + Postgres + optional Redis). CI copies the artifact, `systemctl restart`, health check; previous binary on disk is rollback. Do not expose Tomcat/Go to the internet.

**42. What does nginx do even on one box?**
TLS, gzip/brotli for static, `proxy_pass`, timeouts, `client_max_body_size`, WebSocket `Upgrade` if you have sockets. The app stays on loopback. nginx retries plus app retries are a storm — pick one hop to retry idempotent GETs. Failure: hoping systemd without a health check is a deploy strategy.

**43. When do you leave a single VM?**
After you profiled: disk/CPU maxed, need rolling deploys, or compliance wants AZ isolation. Next rung is **replicas of the same binary** behind a load balancer — still not fourteen microservices. Sticky sessions without Redis are a trap. Docker Compose of one app + Postgres is still rung 1, not Kubernetes.

**44. What is the scale ladder you should not skip?**
One service → replicas of the same binary → split BFF from SoR → Redis as cache/session/rate-limit → queue plus workers → split a bounded context **with its own DB**. Skip rungs and you buy a distributed monolith. Firebase BaaS is a **parallel** rung-1 for prototypes, not a bank ledger.

**45. Service mesh vs API gateway — same box?**
Mesh (sidecars) is mTLS, retries, timeouts, L7 metrics **between** services. Gateway is partner/public API management and the SPA’s first hop. A mesh retry of a non-idempotent POST is a double charge. Failure: installing Istio and calling it an API strategy.

---

## Data access

**46. ORM vs SQL — JPA vs sqlc?**
Mapping columns to objects is **not** the architecture; the aggregate boundary is. JPA/Hibernate is productive and hides SQL until N+1 and lazy serialization explode. sqlc/jOOQ/pgx make the query **visible**. HTTP JSON ≠ table row — map in the adapter; version the DTO; expand/contract the table.

**47. Why is Hibernate lazy plus a JSON serializer a Sev-1?**
The serializer touches lazy associations and fires N+1 queries on the request thread. GORM auto-preload is the same sin in Go. Fetch plans, DTO queries, or explicit SQL fix it. Failure: binding HTTP JSON onto a JPA entity (mass assignment and schema leak).

**48. How do Java and Go transactions compare?**
Same business rule: one use-case, one commit. Java: `@Transactional` (Required default, readOnly hint, timeout, `@Version`). Go: pass `*sql.Tx` from the use-case; `context.WithTimeout`; `WHERE version=$n`. Outbox is a second `INSERT` in the **same** commit. Saga is **not** a Java annotation.

**49. Optimistic vs pessimistic locking?**
Optimistic: version column, conflict retries the use-case — default for user-facing edits. Pessimistic: `SELECT FOR UPDATE` when lost update is unacceptable and contention is short. Do not hold either lock while calling HTTP or Kafka. Failure: serializable isolation as a substitute for a missing unique constraint on payments.

**50. Why not hold a transaction open across HTTP?**
The row lock and pool slot live as long as the remote call. Downstream slowness becomes pool death and cascading 504s. Commit locally, then talk; use outbox for the fact. Failure: `@Transactional` on a controller that fans out to three services.

**51. Replica routing after a write?**
Writes and read-your-writes go to **primary**. Stale-ok lists may use a replica. `@Transactional(readOnly=true)` is a hint, not magic replica routing — you still configure it. Failure: serving empty success because the replica lagged.

**52. What is CQRS in this estate?**
A **read model** (search, list, GraphQL view) projected from committed facts — not a religion that splits every table on day one. The vector index for RAG is the same idea: rebuild from files; OLTP threads stay the conversation SoR. Failure: Pinecone as chat history.

---

## Messaging

**53. Kafka vs SQS vs RabbitMQ — how do you choose?**
Ask if this is a **job**, a **journal**, or a **notification**. SQS (or Rabbit work queues) = competing consumers, one worker per message. Kafka = append-only log, independent consumer groups, replay. Rabbit also does classic routing/EIP; it is not a database. Kafka is not a queue until you pretend one group is a queue; SQS is not a log — you cannot rewind for a new analytics service.

**54. When is Kafka the honest broker?**
Event journal, CQRS projections, high volume, order **per key** (partition). Consumers are idempotent; facts come from **outbox**. Failure: twelve topics named after REST verbs; using compaction as the money ledger; dual-write DB then `kafka.send`.

**55. When is SQS the honest broker?**
AWS work items, account isolation, operational simplicity, visibility timeout vs process time. Fan-out needs SNS in front; strict order needs FIFO and its limits. Failure: expecting Kafka replay semantics from a queue.

**56. When is RabbitMQ the honest broker?**
Work queues, routing keys, classic EIP, moderate volume. Watch memory alarms and “retention as SoR.” NATS core is fast pub/sub and **not** durable unless JetStream. Failure: Rabbit as the system of record for payments.

**57. Queue vs log vs pub/sub in one sentence each?**
Queue: each message is processed by **one** worker. Log: many groups independently replay. Pub/sub: fan-out, often no long replay (Redis pub/sub, some buses). Pick physics before logo. Failure: “event-driven” with no delivery story.

**58. What EIP must you name in an ARB?**
Competing consumers, poison messages, **DLQ**, idempotent consumer, claim check for fat payloads, correlation id. Retry without idempotency is a double send. No DLQ is an on-call career. Alert on DLQ depth; do not infinite-retry money.

**59. At-least-once vs at-most-once vs exactly-once?**
At-least-once is the default mental model — duplicates after retry/rebalance; **design for them**. At-most-once loses messages on crash — almost never OK for money. Broker “exactly-once” does not erase dual-write or non-idempotent side effects. Language of the consumer is irrelevant.

**60. Inbox plus outbox on consume — what is the sequence?**
Start tx; insert inbox `message_id` (conflict = skip); apply business change; insert outbox; commit; relay publishes. This is Richardson’s boring pair in any language. Failure: Redis SETNX as the only ledger of “we processed this payment.”

---

## Sagas & idempotency

**61. Dual-write vs transactional outbox?**
Dual-write: `COMMIT` the order then `publish` — a crash between them is a lie. Outbox: event row in the **same** DB transaction as the SoR change; CDC or a poller relays to Kafka. Consumers de-dupe. Dual-write is the original sin; Java/Go/Node all commit it the same way.

**62. Saga vs two-phase commit (2PC)?**
A saga is **local transactions plus compensations** (or forward repair) across systems you do not XA. 2PC/XA across app DB and Kafka (or three products) is operationally hostile: locks, coordinator availability, vendor support. Do not 2PC the broker. Compensation is a **new fact** (refund), not magic undo.

**63. When do you not need a saga?**
One aggregate, one database, one transaction — just commit. Sagas for “update email in two tables in the same service” is theatre. Need a saga when order, pay, and stock are **three SoRs** and the user can still see partial progress.

**64. Choreography vs orchestration?**
Choreography: each service listens, acts, emits the next fact — simple for few obvious events, spaghetti when nobody can draw the process. Orchestration: a process manager (Temporal/Camunda/Step Functions) tracks state — visible workflows and human tasks; rot if it owns everyone’s data. Pick from **visibility vs coupling**, not from a vendor booth.

**65. Why is compensation not `rollback()`?**
Stock may have shipped; the card processor already captured. Refunds and reverse-reserves are new business events with their own idempotency. Timeouts create **pending** states, not “paid because 504.” Failure: marking paid on client timeout.

**66. How do you make a money POST idempotent?**
Client sends `Idempotency-Key` (or you use `payment_id`). Store the key in the **same transaction** as the insert; duplicates return the first result. PUT/DELETE already are; POST is not. Double-click pay without a key is a Sev-1. Go or Java for that API; keep PAN in the processor.

**67. How do processor webhooks stay safe?**
At-least-once delivery: **inbox** on event id, verify signatures, state machine for captured/failed/refunded. Do not trust unsigned bodies. Refunds are a saga, not a silent UPDATE. Failure: retrying the original POST without a key because the webhook was late.

**68. Why not XA between Postgres and Kafka?**
The coordinator and lock duration become your availability story. Outbox plus idempotent consumers give **practical** consistency. “Exactly-once” in the broker does not replace that pair. Failure: `INSERT` then `kafka.send` in a try/finally you believe is atomic.

---

## Redis

**69. What roles can Redis play — and which must it never play?**
Name the role in the ADR: **cache**, **session**, **rate limit**, **lock** (SET NX PX), **pub/sub** fan-out, sometimes a light queue. It is **never** the system of record for money or leave balance. Key schema `{bounded}:{agg}:{id}:v{n}`. Java: Lettuce/Redisson; Go: go-redis; stampede: Caffeine L1 or `singleflight`.

**70. Cache-aside vs Redis as SoR?**
Read: get cache; on miss load SoR; set TTL. Write: update SoR then DEL (or version the key). Product chooses fail-open to SoR (slower) vs 503. Inventing a leave balance when Redis is down is forbidden. Failure: Redis as the ledger because it is fast.

**71. Session store: fail-open or fail-closed?**
Usually **fail-closed**: 503 login rather than ghost admin sessions. Signed-cookie fallback only if you designed it. Spring Session / Go Redis store are skins. Sticky Tomcat sessions without Redis break rung-2 replicas.

**72. Rate limit fail-open vs fail-closed?**
Fail-open = availability, risk of abuse. Fail-closed = protect origin, risk of locking out everyone when Redis dies. **Pick** in the ADR; do not discover it in an incident. INCR+TTL or token bucket are implementations, not architecture.

**73. Why isn’t Redis pub/sub your event journal?**
It is fan-out for a WebSocket gateway, not durable replay. If you must not lose, use Kafka (or a queue) via outbox. Lists/Streams as a queue are possible; Rabbit/SQS if you need ops maturity. Failure: “we’ll add Kafka” with no SoR fact.

**74. Distributed locks on the ledger?**
Short SET NX PX for a **job** (don’t run two PDF workers). Do not lock money across seconds of HTTP. The unique constraint and idempotency key are the real locks. Failure: Redisson lock around a SOAP call.

---

## Identity

**75. OIDC / IdP vs homemade JWT — default for humans?**
Integrate an IdP (Entra, Okta, Keycloak, Cognito, Auth0, Firebase Auth) for people. Confidential BFF: authorization code + PKCE, session cookie, RP-initiated logout. Resource servers validate JWKS: `iss`, `aud`, `exp`, `nbf`, signature. Custom JWT only for short, `aud`-bound **service** tokens you can revoke.

**76. Why does each API need its own audience?**
One JWT for “the whole estate” is a lateral-movement gift. Token exchange: Entra JWT → BFF session → outgoing JWT `aud=leave-api` with reduced claims. Downstream must not accept the SPA’s token if it was never meant for that `aud`. Map groups/roles in the resource, not only at Kong.

**77. When is minting your own JWT acceptable?**
Short-lived RS256 (prefer) service tokens after mTLS or workload identity; Firebase **custom** tokens from a **server** Admin SDK. Opaque hashed API keys for partners. Not OK: 24h HS256 in env; `alg=none`; client SDK minting admin; a bank avoiding Keycloak by rolling crypto in a controller.

**78. Why is HS256 in a controller a fail in a bank?**
You just became an amateur IdP: key rotation, revocation, session, MFA, audit. Prefer Entra (even when compute is AWS). Never JWT in a query string; never HS256 secret in the SPA; never trust attacker `kid` JWKS without pinning `iss`. Keep custom claims small — no PII dumps in tokens (they leak in logs).

**79. JWKS down — what is an honest fallback?**
Cached JWKS with max-stale, or **fail login**. Skipping signature verify is forbidden. IdP integration is default; homemade JWT is the exception you can explain. Failure: Firebase custom tokens minted in the browser.

**80. AuthN at the edge vs AuthZ in the use-case?**
Gateway/BFF authenticate (who). Domain authorizes (may this manager approve **this** leave). Security rules in Firestore are a gateway, not HR policy. CSRF if cookies; CORS allowlist; parameterized SQL. Same working set on a single VM as in the cluster.

---

## Resilience

**81. Resilience4j vs gobreaker vs opossum — peers?**
Yes: circuit breaker + extras on Java, Go, and Node. Hystrix is retired; the **idea** remains. Mesh retries do not replace **app** deadlines. The product owns whether a fallback may be stale. Failure: `@Retryable` until it works.

**82. How do you budget timeouts?**
User SLO first; inbound deadline; each outbound timeout **much smaller**; leftover budget for the caller. Invert the anti-pattern (client 30s, gateway 60s, DB none). Timeouts exist on HTTP, DB statement/pool checkout, Redis, and queue visibility. Stopping wait does not stop remote work — pair with idempotency.

**83. When may you retry?**
Only **idempotent** calls, with jitter and a cap. GET is usually safe; POST charge is not unless keyed. Nested timeout plus retry without a deadline is a Saturday Sev-1. Failure: infinite retry; gateway and app both retrying the same POST.

**84. What does a circuit breaker actually do?**
After an error threshold it **fails fast** instead of waiting on a dead dependency, then probes half-open. Combine with timeouts; CB without timeouts still holds pools. Java: Resilience4j; Go: `if err` plus gobreaker; same SLO. Failure: CB that never opens because you retry forever first.

**85. What is a bulkhead?**
Isolate pools so SOAP weather cannot steal checkout connections (separate thread/connection/semaphore per dependency). Noisy-neighbor tenancy is the same idea: interactive vs batch pools. Java Hikari per datasource; Go separate `http.Client`; Node separate agents. One pool of 20 for all tenants is a bulkhead fail.

**86. What is an honest fallback vs a forbidden one?**
Redis cache down → read SoR (slower) or 503 — never invent balance. Holidays API 503 → BFF still renders the page minus that widget. Payments 504 → pending/compensate — never “Paid.” Email down → outbox queued, leave insert stays committed. Feature flags (`SEARCH_OFF`) are architecture.

**87. Load shedding and degraded mode?**
When you cannot keep the SLO, refuse non-critical work (reports, search) so checkout lives. Degraded flags are explicit. Chaos is how you prove the timeout exists. Failure: waiting forever because the dashboard is green.

**88. Deadline propagation across Java, Go, and Node?**
Remaining TTL travels: gRPC deadline, `context.WithTimeout`, `AbortController` / fetch signal. Downstream must not start a 10s query with 20ms left. Spring MVC, `http.Server`, and Fastify timeouts are inbound skins. Failure: Promise.race as a substitute for `statement_timeout`.

---

## Observe, k8s, realtime

**89. What does OpenTelemetry give you that logs alone do not?**
A **trace** across BFF → core → DB/queue with consistent context, plus metrics and (optionally) correlated logs. Java: Micrometer Tracing / OTel; Go: OTel; same collector story on AWS or Azure. Use it to find the hop that ate the SLO, not to replace runbooks. Failure: three languages, three incompatible request-id headers.

**90. Liveness vs readiness vs startup probes?**
**Liveness** = process alive (cheap, local). **Readiness** = can take traffic (dependencies). **Startup** = JVM warming so kubelet does not kill you during boot. Do not point liveness at a deep Postgres check. Failure: cluster restart storms during a DB blip because `/live` was `/ready`.

**91. How should Node and Go expose probes?**
Go: `/healthz` live, `/readyz` = DB ping (readiness only). Node: do not block `/health` on a stalled loop without a strategy (separate lightweight path). Same rule as Java Actuator split. Size JVM `-Xmx` to the cgroup; Node/Go still need memory limits.

**92. WebSocket/SSE vs Web Push — which is “realtime”?**
Open tab: WebSocket or SSE with fan-out, backpressure, auth on the socket (not JWT in the query string). Closed laptop overnight: **Web Push / FCM**, not a socket. Calling sockets “push” confuses the ARB. Go is strong for many connections; Node is fine at modest fan-out; Java often wants a dedicated layer.

**93. Where does Redis sit in a socket fan-out?**
Pub/sub between gateway instances so a message on node A reaches the connection on node B. That is not durable history. Persist the inbox in Postgres; push notify when the tab is closed. Failure: Lambda WebSockets as the leave ledger.

---

## Tenancy, compliance, BaaS

**94. How do you isolate multi-tenant SaaS (SMB pool vs bank whales)?**
**Hybrid:** shared pool + RLS + quotas for 2k small tenants; **silo database** for whales and India residency. Tenant from the **token**, not a spoofable `X-Tenant-Id`. Split pools interactive vs batch. Java/Go/Node all need bounded pools per class of work. Failure: N DSN × 10 connections in one pod.

**95. What belongs in PCI / PII logs, and what never does?**
PAN and secrets **never** in app logs, traces, or RUM. Shrink PCI to the vault/processor; tokenize. PII is a **data class** with retention, encryption in transit/rest, and residency (DPDP/GDPR = lawful basis + where bytes live, not a Spring annotation). Audit is **append-only** who did what for seven years. Failure: US RUM on IN PII without a DPA; vector DB as SoR for medical chat.

**96. Why isn’t Firebase (BaaS) a bank ledger?**
Firebase is a **product bundle**: Hosting, Auth, Firestore/RTDB, Functions, FCM, Storage. Honest for prototypes, mobile-first, internal tools, and CDN hosting. Firestore is a document SoR for chatty presence — not payroll, double-entry, or reporting joins. Security rules ≠ domain AuthZ. Hybrid: Hosting + Entra or Firebase Auth + Java/Go API on a VM/Cloud Run; FCM from a worker. Failure: leave ledger in Firestore “because realtime.”

**97. Admin SDK vs client SDK?**
Admin SDK (Node common; Java and Go exist) is a **privileged** adapter — treat it like a DB password. Client SDK must not mint god tokens. Custom tokens come from **your** authenticated server. Failure: putting domain loops in 15-minute Cloud Functions and calling it core banking.

**98. How do you strangler a SOAP/COBOL estate for a JSON journey?**
Path/operation strangler, ACL, Node BFF hides SOAP, Java wraps COBOL; dual-run checksum; **one writer**. Never rewrite 400 operations. Iframe/façade beats rewrite fiction. Failure: dual-write settlement to old and new.

**99. AWS vs Azure for the same Java/Go API — what actually changes?**
Map **jobs**, not logos: identity, private data plane, queue, SoR, OTel. AWS: ECS/EKS, RDS, IAM/Secrets Manager, SQS. Azure: Container Apps/AKS, Flexible PG, Managed Identity/Key Vault, Service Bus. Workforce **Entra on both**. No Lambda as ledger. Failure: dual-write RDS and Cosmos “for HA”; access keys in Git.

**100. What does a strong 90-second backend answer sound like?**
Freeze SoR, who pages, and failure first. Ship one Java or Go binary behind nginx until numbers and trains demand more. Redis is cache/session/rate-limit — not money. BFF shapes the browser; IdP for humans; outbox not dual-write; timeouts, CB, honest fallbacks; microservices last. Weak answers rank Spring vs Go and “add Kafka.”
)
