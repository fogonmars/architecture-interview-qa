# Database interview Q&A

Architect drill, not a logo quiz: steal the **question**, not Netflix’s mesh.
The stack in a war story is a constraint; answers are mechanisms plus a failure mode.
If you cannot name a metric after any of them (`EXPLAIN ANALYZE`, lag, slot LSN, restore clock), you memorized a slogan.
**Chapters:** [Internals](../dbnotes/01-architecture/internals.md) · [Transactions](../dbnotes/01-architecture/transactions.md) · [Indexes](../dbnotes/01-architecture/indexes.md) · [Types](../dbnotes/03-database-types/catalog.md) · [Replicas](../dbnotes/04-replication-ha/read-replicas.md) · [Scenarios](../dbnotes/30-interview-and-architecture-scenarios/README.md). **Topics:** [Query path](#query-path-wal-checkpoint-vacuum) · [MVCC](#mvcc-and-isolation) · [Indexes](#explain-indexes-n1-pools) · [Normalization](#normalization) · [Workloads](#oltp-olap-search-cache-stream-graph-ingest) · [Engines](#engines-and-when) · [HA/DR](#replicas-ha-dr) · [Scale/CDC](#partition-shard-cdc-outbox) · [Ops/compliance](#managed-compliance-industry)

---

## Query path, WAL, checkpoint, vacuum

**1. Walk through `SELECT * FROM orders WHERE id = 1` in Postgres.**
Client protocol hits a backend process. Parse builds a tree, rewrite applies views/rules, the planner picks index vs seq scan, the executor walks operators, pages come from `shared_buffers` or disk, MVCC visibility filters tuples, then rows go back on the wire. A primary-key `id` is almost always an index lookup, not a heap scan. `SELECT *` still may fetch TOAST for wide columns you did not need.
**Fail:** drawing “the database” as one box with no parse/plan/visibility.

**2. Parse vs plan vs execute — what actually burns CPU?**
Parse is syntax and names. Plan is cost-based access paths (which index, join order, hashes vs nested loops). Execute is the operators: I/O, CPU, locks, sorts. A cached generic plan that is wrong for this parameter is an execute problem that looks like a “slow database.” Name `pg_stat_statements` and `EXPLAIN (ANALYZE, BUFFERS)` when they ask how you would prove it.

**3. Why write WAL before the heap page?**
Durability is the log (ARIES-style). Crash recovery replays WAL from the last checkpoint; data files are allowed to lag. If you flushed the heap first and died, you could have a page the log never promised. This is why `fsync` on WAL, `synchronous_commit`, and checkpoint timing dominate “is my money still there?” conversations.

**4. What does a checkpoint do?**
It flushes dirty buffers and records a WAL location so recovery starts there instead of at the beginning of time. Too frequent checkpoints spike I/O and stall writers; too rare makes crash recovery and failover long. You tune spread (`checkpoint_completion_target`, max WAL size) against RTO, not against a blog’s “set it to 30 minutes.”

**5. Why does Postgres need VACUUM and InnoDB need purge?**
Postgres keeps old row versions in the heap; vacuum marks them reusable and freezes XIDs. InnoDB keeps old versions in undo and purge reclaims them. If either lags you get bloat, wraparound risk (PG), or history-list length (InnoDB). Autovacuum is not optional hygiene; it is part of the write path’s tax.

**6. What is transaction ID wraparound?**
XIDs are 32-bit. If freeze vacuum does not advance `datfrozenxid`, Postgres will eventually refuse writes to protect MVCC. Monitor `age(datfrozenxid)` per database and table; never “fix” wraparound by turning autovacuum off. A restore drill that only checks “backup succeeded” and never freeze age is incomplete.

**7. What is TOAST and why does `SELECT *` hurt?**
Wide attributes go out-of-line. The planner and executor still have to fetch them if you asked for `*`. Project the columns the API needs; that is cheaper than a cache in front of a fat row. JSONB blobs in the main table make this worse when every list endpoint materializes the document.

**8. Shared buffers vs OS page cache?**
Postgres keeps pages in `shared_buffers`; Linux may cache the same files again. InnoDB’s buffer pool is more aggressive and you size it as the working set. Double-caching is normal on PG; starving `shared_buffers` on a huge instance so “the OS can decide” is a slogan, not a measurement.

**9. Why is `work_mem` dangerous?**
It is per sort/hash **node**, not per instance. `max_connections × nodes × work_mem` OOMs a box that looked fine in `free -h`. Hash joins and sorts that spill to disk are the other failure: you under-set it and p99 explodes. Fix the plan first; then size `work_mem` for the real node count, often behind a pooler.

**10. Why can 10,000 app pods kill a healthy database?**
Each Postgres connection is a backend process: RAM, file descriptors, context switches, `max_connections`. Kubernetes scaled the clients, not the postmaster. Put PgBouncer or RDS Proxy in front; do not raise `max_connections` until the box is a connection farm. Session-mode pooling still will not save you if every pod opens ten idle sessions.

**11. What does `synchronous_commit = off` buy and cost?**
Commits return before WAL is durable on disk. You win latency and can lose the last transactions on crash. Fine for clickstream you can rebuild; not for ledgers, inventory, or PCI cardholder data. Async commit is not a replica, and it is not Multi-AZ.

**12. What is a HOT update?**
If indexed columns do not change and the new version fits on the same heap page, Postgres can skip updating indexes (Heap-Only Tuple). Fat rows, fillfactor 100, and “index every column” kill HOT and turn every update into index maintenance. That shows up as WAL volume, not as a missing cache.

---

## MVCC and isolation

**13. What does MVCC actually do on a read?**
Each statement (or transaction, depending on isolation) sees a snapshot: tuples whose creating XID committed before the snapshot, and that were not deleted by a transaction visible to you. Ordinary `SELECT` does not take row locks. Writers create new versions; readers do not wait — unless you asked `FOR UPDATE` or you are InnoDB locking reads.

**14. Postgres default isolation?**
Read Committed. Each statement takes a new snapshot, so two `SELECT`s in one transaction can see different committed rows. That is the default because it is cheap and matches “I just want the latest committed value.” It is not “safe for money” by itself.

**15. Read Committed vs Repeatable Read vs Serializable?**
RC: new snapshot per statement; you can see committed writes from others between statements. RR in Postgres: one snapshot for the whole transaction; you do not see later commits; write-write conflicts may fail. Serializable (SSI): RR plus predicate-like conflict detection so the history looks serial. Pick the weakest level that preserves the invariant; then retry.

**16. Repeatable Read: Postgres vs InnoDB?**
Postgres RR is snapshot isolation: no gap locks on ordinary reads; write skew is still possible. InnoDB RR uses next-key/gap locks on locking reads and is the MySQL default; phantoms are blocked by locks, not by SSI. Do not translate `REPEATABLE READ` across engines as if it were a standard.

**17. Phantom vs non-repeatable vs write skew?**
Non-repeatable: the same row’s values change between reads. Phantom: the *set* of rows matching a predicate changes. Write skew: two transactions read overlapping state, write disjoint rows, and break an invariant (two doctors both go off-call). SSI is how Postgres serializable catches write skew; RC will not.

**18. How does SSI work, in one breath?**
Serializable Snapshot Isolation watches for rw-conflicts that cannot be ordered. It aborts one transaction instead of holding predicate locks like classic 2PL serializable. Aborts are **normal** under contention. If the app does not retry the **whole** transaction, you “turned on serializable” and still corrupted the invariant.

**19. Why retry serialization failures?**
`40001` / “could not serialize access” is the protocol. Retry with backoff the same business transaction, not a single statement. If retries storm, you have a hot row or an invariant that should be one-row `UPDATE … WHERE qty >= 1` instead of a chatty SSI conversation.

**20. Do readers block writers?**
Not for ordinary MVCC `SELECT`. `SELECT FOR UPDATE` does. Long snapshots **operationally** block vacuum (and, on replicas, recovery), which then blocks writers with bloat or wraparound. That is how a read-only report takes down OLTP without holding a row lock you can see in an app log.

**21. What is idle-in-transaction and why is it an incident?**
The session issued `BEGIN`, then went to HTTP, Kafka, or a breakpoint, while holding a snapshot and possibly locks. Pools fill with “idle in transaction,” vacuum cannot freeze, DDL waits, bloat grows. Set `idle_in_transaction_session_timeout`; fix the app; do not raise `max_connections`.
**Fail:** `max_connections + 200` while CPU is idle.

**22. How should deadlock be handled?**
The engine aborts one transaction. The app retries; lock rows in a consistent order; keep transactions short. Deadlock is a symptom of wide updates, missing indexes on the `WHERE`, or lock upgrade. Raising `lock_timeout` to “let it finish” just lengthens the queue.

**23. ACID C vs CAP C?**
ACID consistency: constraints and invariants hold at commit. CAP consistency: every node shows the same data during a partition (linearizability-ish). You can have a perfectly ACID primary and still have a stale replica. Do not answer “we are consistent” without saying which C.

**24. Two checkouts, last unit of stock — isolation design?**
Atomic `UPDATE … SET qty = qty - 1 WHERE id = $1 AND qty >= 1` and check `rowcount`, or `SERIALIZABLE` plus retry. Read Committed `SELECT` then `UPDATE` loses. Redis `DECR` is not the inventory SoR unless you designed a dual system of record on purpose (you did not).
**Fail:** RC read-modify-write and a unique index on SKU as the “fix.”

---

## EXPLAIN, indexes, N+1, pools

**25. Why is `EXPLAIN` without `ANALYZE` insufficient?**
It is the planner’s guess: estimated rows, not wall time, not buffers, not the misestimate. `EXPLAIN (ANALYZE, BUFFERS)` shows actual rows, I/O, and whether you hashed or nested-looped a million times. The bug is usually a bad estimate (stale stats, correlated columns), not “Postgres is slow.”

**26. When is a B-tree the right index?**
Equality and range on ordered scalars: ids, timestamps, status enums, `(tenant_id, created_at)`. It is the default. It is the wrong default for JSON containment, full-text tokens, or “we might filter any of 40 columns.” Left-most prefix still applies.

**27. Left-prefix rule?**
Index `(a, b, c)` serves `a`, `a+b`, `a+b+c` (and `a` plus range on `b`). It does not serve `b` or `c` alone. A query that filters only `created_at` in a 10k-tenant table wants `(tenant_id, created_at)` if every call has tenant, not a global time index.

**28. What is a covering index?**
Every column the query needs lives in the index (`INCLUDE` in Postgres) so you can index-only scan. It still depends on the visibility map being set — vacuum lag turns “index-only” into heap fetches. Covering is for a **measured** hot path, not for duplicating the table in every index.

**29. Why did my index-only scan still heap-fetch?**
Visibility map bits not all-visible: vacuum has not frozen/set the page. You paid for the index and still random-read the heap. Autovacuum scale factor on a large, slowly updated table is a common cause.

**30. GIN vs B-tree?**
GIN: many keys per row — `JSONB`, arrays, `tsvector`. B-tree: one ordered key, ranges, uniqueness. GIN writes are heavier; do not GIN a uuid. B-tree will not make `@>` on JSON fast.

**31. When is BRIN the right index?**
Physically correlated append-only data: time-series heap that is inserted in time order. Tiny, cheap to maintain. Random heap order (UUID PK, updates that move correlation) makes BRIN a no-op that still costs planner time. Prove correlation; do not “BRIN the fact table” because it is large.

**32. Partial index?**
`CREATE INDEX … WHERE status = 'open'` is small and matches that predicate. Great for sparse hot states. Useless if the app queries `status IN ('open','closed')` or forgets the same `WHERE`. Drop it when the predicate dies.

**33. Why not index every column?**
Write amplification, WAL, disk, slower HOT, more planner choices that go wrong, and indexes nobody uses (`pg_stat_user_indexes`). Each index is a copy you maintain on every `INSERT`/`UPDATE`. Start from `pg_stat_statements`, not from the ERD.

**34. What does sargable mean?**
The predicate can use an index: `col = $1`, `col > $1`, `col LIKE 'foo%'`. `LOWER(col)`, `DATE(ts)`, leading-wildcard `LIKE`, and type mismatches (`varchar` vs `uuid`) are not. Rewrite the query or use an expression index you will actually maintain.

**35. `CREATE INDEX CONCURRENTLY`?**
Avoids a long exclusive lock: two scans, more WAL, can finish `INVALID` if it fails. Default `CREATE INDEX` on a hot 500 GB table is an outage. Liquibase XML `createIndex` may not emit `CONCURRENTLY` — use raw SQL and a follow-up validate.

**36. List 50 orders, each with lines — 51 queries. What is N+1?**
The ORM loaded the parent, then one query per child. Join, `WHERE order_id IN (…)` / select-in-load, or a JSON aggregate. Measure with the same `EXPLAIN` you would use on raw SQL; ORM “includes” that still N+1 at 5k QPS are still N+1.
**Fail:** “that’s just how ActiveRecord is.”

**37. Connection pooling and PgBouncer — why?**
The pool multiplexes many app clients onto few backends. That is how you survive Kubernetes. Put it next to the DB (or RDS Proxy) so you do not open a backend per pod. Pool size is a capacity plan: `backends ≈ cores × (1 + wait_on_io)`, not “equal to replicas in the deployment.”

**38. Transaction pooling vs session pooling?**
Transaction mode returns the server at `COMMIT` — prepared statements, `SET`, temp tables, and advisory locks leak across clients or break. Session mode holds a backend for the client session. Most OLTP wants transaction mode **after** you ban session state. Mixing both in one pooler is how “it works in staging.”

**39. `COUNT(*)` on 80 million rows for a homepage badge?**
Exact count is a sequential visibility walk — OLAP. Use `reltuples`, a counter table, a cached metric, or pre-agg. Sending the same `COUNT(*)` to a replica is the same query with lag.
**Fail:** replica as the “fix” for a full-table count.

**40. Bind parameters vs concatenated SQL?**
Parameters reuse plans and stop injection. String-concatenated email search is both a security finding and a plan-cache disaster (`LIKE '%` + user + `'`). “We sanitize quotes” is not a parser.

---

## Normalization

**41. 1NF?**
Atomic attributes, no repeating groups: not `phone1, phone2, phone3` and not a CSV in a text column you query with `LIKE`. JSONB can be a deliberate exception when the document is not independent facts you join and constrain. 1NF is about predicates and updates, not about “we hate JSON.”

**42. 2NF?**
No non-key attribute depends on only part of a composite key. `(order_id, sku)` as key with `customer_email` on the line depends on `order_id` only — that belongs on `orders`. 2NF violations show up as update anomalies, not as missing indexes.

**43. 3NF vs BCNF?**
3NF: no transitive dependency of non-key on key; it still allows a non-superkey determinant if the dependent is prime. BCNF: every determinant is a superkey. BCNF can lose dependency preservation — you may need the join to enforce an FD. Do not “normalize to BCNF” as a religion on a schema that must enforce FDs in one table.

**44. Classic BCNF example you should be able to write?**
Student, subject, teacher with `teacher → subject`: a teacher teaches one subject, but `(student, subject)` as key leaves `teacher → subject` not a superkey. Decompose to `(teacher, subject)` and `(student, teacher)` (or equivalent). If they cannot draw the FDs, they cannot BCNF.

**45. 4NF in one example?**
Independent multi-valued facts — course has instructors and textbooks — should not be stored as a cross-product in one table. Two tables `(course, instructor)` and `(course, textbook)`. 4NF is rare in interviews; the tell is “we exploded a cartesian and called it a fact table.”

**46. When is denormalization correct?**
A **measured** read path: CQRS projection, point-in-time order snapshots (`sku_name` at purchase), materialized views, with an invalidation or rebuild story. It is wrong as a first schema because “joins are slow.” Joins on keys with indexes are the point of a relational SoR.

**47. Is `sku_name` on `order_line` a 3NF violation?**
If it is the name **at purchase**, it is a historical fact, not a live functional dependency on catalog name. If it is copied so the UI never joins and you overwrite it when marketing renames the SKU, you forged history. Say which one you meant.

**48. Why is EAV a trap?**
Entity-attribute-value has no real types, constraints, or planner stats. Every query is a self-join or a JSON-in-disguise pivot. Prefer real columns, JSONB with constraints you can enforce, or a document store if the aggregate is the unit of load. EAV is how “flexible schema” becomes unqueryable SoR.

**49. Lossless vs dependency-preserving decompose?**
Lossless: join-back equals the original relation. Dependency-preserving: you can still enforce FDs without joining. 3NF synthesis aims at both; BCNF may sacrifice preservation. In an interview, say which invariant you will enforce in the application if the schema cannot.

---

## OLTP, OLAP, search, cache, stream, graph, ingest

**50. OLTP vs OLAP vs warehouse (Snowflake/Redshift)?**
OLTP: row store, millisecond point reads/writes, current truth, small transactions. OLAP/warehouse: columnar scans, minutes-old data OK, `SUM` over terabytes. Checkout does not run on Snowflake; the nightly margin report does not run on the primary. ELT into Redshift/Snowflake/BigQuery from the SoR — do not dual-write the cart to a warehouse.

**51. Search (Elasticsearch/OpenSearch) vs system of record?**
Search is a **near-real-time projection**: relevance, facets, typo tolerance. Rebuild from SoR. Stock-on-hand and payment state stay in OLTP; facets can lag seconds. ES-as-SoR is how you lose the rebuild and then page on heap.

**52. Cache (Redis) vs database?**
Cache is a performance copy with an explicit TTL/invalidation and a stampede plan. The SoR remains the DB (or MemoryDB if you **chose** durable Redis). When Redis dies, the database must survive the thundering herd or you shed load. Sessions-only Redis is a product decision; ledger-in-Redis is an incident.

**53. Stream vs database — why did LinkedIn build Kafka?**
Requirement was activity events consumed independently by feed, search, analytics, and counters, with **replay**. A database is a current snapshot; a log is history many teams can tap without coupling to one schema. Kafka is not a query engine. If you have one consumer and no replay, you wanted a table or a queue.

**54. Graph vs relational — when is Neo4j (or similar) the SoR?**
When **path is the product query** at moderate scale: fraud rings, network inventory, recommendations you can bound. Meta-scale social graph is MySQL + a cache fabric (TAO class), not Neo4j as Facebook SoR. Property graphs (Cypher) ≠ RDF/SPARQL ontologies — do not mix them in the answer.

**55. Ingest / time-series / append-heavy punches?**
Partition by time (or Dynamo/Cassandra partition key that matches the write), idempotency keys, warehouse for reports. One unpartitioned `punches` table plus `LIKE` on name is how attendance systems die. Ingest is not OLTP checkout; do not SERIALIZABLE the firehose.

**56. pgvector vs a dedicated vector DB (ChatGPT-class RAG)?**
Embeddings are a **derived projection** of files/chunks you already store. Start `pgvector` next to the OLTP SoR until scale/latency/ops force an ANN service. Billing, auth, threads, and quotas stay relational. Vector DB as the only copy of customer text is a compliance and rebuild problem.

**57. Feature flags and other “tiny SQL on every request”?**
Redis/etcd plus an SoR for audit. A 50 ms join on the primary for every HTTP request is how you invent a cache after the incident. Flags are not a graph problem and not a warehouse problem.

---

## Engines and when

**58. PostgreSQL vs MySQL/InnoDB — what do you actually pick?**
Both are OLTP row stores. Postgres: rich types, JSONB, GIN, SSI, extensions, MVCC-in-heap. MySQL: operational familiarity in some estates, InnoDB clustered PK, RR+gap locks. Pick the estate skill, the isolation story, and the index types you need — not “PG is more enterprise.” UUIDv4 as InnoDB PK is still a page-split tax.

**59. SQL Server — when is it the honest answer?**
Windows/.NET estate, Always On, columnstore for mixed, existing licenses, T-SQL shop. It is a serious OLTP/warehouse hybrid in Microsoft-heavy companies. “We must use Postgres because interviews” is not an architecture. HA is Availability Groups, not “a read replica we failover manually.”

**60. Oracle vs Postgres for a core?**
Oracle: decades of PL/SQL, RAC stories, vendor lock, cost, staff. Postgres: extensions, cost, cloud defaults. Migration cost is **packages and invariants**, not bytes (SCT inventory, CDC, checksums). “DMS will convert the ERP” is the fail. If RAC was the HA story, name the Postgres operator/Patroni equivalent honestly.

**61. SQLite on the server?**
One writer, local disk, embedded. Fine for small/internal, edge, mobile, tests. Not multi-writer NFS, not a Kubernetes Deployment with three replicas on one file. If you need concurrent writers, you wanted Postgres (or a real multi-writer store).

**62. RDS vs Aurora?**
RDS: managed VM + disk, familiar Postgres/MySQL, you size instances and IOPS. Aurora: disaggregated storage, faster failover, more replicas, compatibility caveats (version lag, extensions). Aurora is not “infinite writes”; the writer is still a writer. Choose on failover RTO, replica count, and extension need — not on the logo.

**63. DynamoDB vs SQL — start from which diagram?**
Dynamo: access patterns first → partition/sort keys → GSIs. SQL: entities and constraints first, then access. Dynamo wins when every query has a known key, writes are huge, and you accept no multi-item SQL. SQL wins unique constraints, ad-hoc, and money invariants. Amazon’s cart at their scale is Dynamo-class **cart** plus relational **order/payment** — not one engine.

**64. Mongo vs Postgres?**
Document aggregate as the unit of load and update → Mongo. Relationships, joins, constraints, reporting in the same SoR → Postgres. “Schema-less” is not a requirement; it is a postponed schema. If you query across documents as if they were tables, you wanted SQL.

**65. Cassandra (or Bigtable-class) when?**
Known partition key for every query, huge write/availability, multi-DC AP. No cross-partition SQL, no cheap unique email. Time-series and inbox-shaped data fit; bank **available balance** does not. Netflix uses it where the access pattern matches — not as a reason for a 50-person SaaS ledger.

**66. Redis — cache, session, or database?**
Usually cache or session. Durable Redis (AOF, MemoryDB) is a choice with a persistence and failover story. Data must fit memory (or you accept eviction). Redis as primary for shopping-cart **at Amazon scale** is the wrong paper; Dynamo is. Redis as primary for a 400 QPS cart can be fine if you accept the durability model.

**67. Elasticsearch vs OpenSearch vs `tsvector`?**
Start with Postgres FTS (`tsvector`/GIN) for admin search. Move to ES/OpenSearch when relevance, facets, and ops are the product. OpenSearch is the AWS-shaped fork; the architecture rule is the same: projection, ILM, shard counts, not SoR. OOM is usually too many shards or aggregations on text.

**68. Kafka vs the database vs a queue?**
Kafka: durable log, replay, many independent consumers, ordering per partition. DB: current state, constraints, queries. Queue (SQS): consume-once work, no fan-out replay. LinkedIn’s problem was the log. Dual-writing payment rows to Kafka from the app is not Kafka’s fault — that is dual-write.

**69. Snowflake vs Redshift vs “just Postgres with a replica”?**
Both warehouses: columnar, separate compute, ELT. Snowflake: separation of storage/compute, multi-cloud sales motion. Redshift: AWS-native, clusters you still operate. A Postgres replica is for **read-your-writes-optional OLTP**, not for 5 TB `SUM`. If the badge on the homepage needs exact `COUNT(*)`, you still do not move checkout to Snowflake.

**70. Cosmos DB — what is the default consistency trap?**
Session: read-your-writes with the session token, not strong global. Partition keys still rule; cross-partition is a bill and a latency. “Cosmos means no decisions” is how you get LWW and surprise RU. Compare to Dynamo on access patterns, not on Azure vs AWS pride.

**71. Aurora Global vs Dynamo Global Tables?**
Aurora Global: typically one writer region, storage replicated, read-local. Dynamo GT: multi-active, last-writer-wins conflicts. Money and stock want a single writer or explicit merge. Multi-region is a latency and RPO product, not a checkbox.

**72. MemoryDB vs ElastiCache?**
MemoryDB: Redis-compatible with a durability story. ElastiCache: typically cache semantics — restore empty is allowed. Pick by whether an empty cache is an incident or a cold start. Neither replaces OLTP constraints.

---

## Replicas, HA, DR

**73. Replica vs HA vs DR — three different jobs?**
Replica: scale **reads**, lag exists, not a writer. HA: automatic failover in-region (Multi-AZ, Patroni), RTO minutes, RPO depends on sync. DR: another region/backup, RPO/RTO you **tested**. Calling an async replica “HA” is how you discover split-brain or data loss in the incident.

**74. RPO vs RTO?**
RPO: how much data you may lose (time or bytes). RTO: how long until you serve again. Multi-AZ sync/quorum can approach RPO 0 in-region; async replica RPO ≈ lag. PITR RPO is the WAL archive delay; RTO is restore + replay + DNS + app. If they cannot name both numbers, they do not have a DR plan.

**75. Multi-AZ vs multi-region?**
Multi-AZ: one region, AZ failure, typically one endpoint, small RPO. Multi-region: region loss, higher RPO unless you paid for sync/global, write-path design (single writer vs conflicts). Users on three continents is not “turn on Multi-AZ.” It is cache, NewSQL, or tenant-split regions.

**76. Physical vs logical replication?**
Physical: WAL bytes, identical cluster, version-coupled. Logical: row events, different indexes/targets, slots, DDL gaps. Logical is for CDC, blue-green, and heterogeneous. Physical is for HA replicas. Slots that are not consumed fill the disk.

**77. Why can queries on a replica get cancelled?**
Recovery conflicts: apply needs to remove tuples your snapshot still sees (vacuum on primary). Cancel the heavy replica query, or delay apply (lag), or do not run long reports on a hot standby you also need for HA. This is Postgres, not “Azure being flaky.”

**78. Point-in-time recovery (PITR)?**
Base backup + WAL archive. You restore to a timestamp or LSN, not “yesterday’s dump.” Test that WAL actually archives; a backup without WAL is crash-only. PITR is not HA — RTO is hours unless you rehearse and automate.

**79. Why restore drills, not backup success emails?**
The unit of DR is **restore**: time, checksum, application boot, IAM, secrets, DNS, who is allowed to promote. Untested backups fail on the day: wrong KMS, empty WAL, slot full, 5 TB and an RTO of 30 minutes. Drill quarterly; write the clock times into the runbook.

**80. Is an async replica RPO 0 disaster recovery?**
No. RPO ≈ replication lag; a crash of the primary can lose unreplicated commits. Sync or quorum storage for RPO 0. Cross-region async as the ledger SoR is a business decision to lose money on region cut.
**Fail:** “we’re Multi-AZ so we cannot lose data” without asking sync vs async.

**81. Split-brain?**
Two primaries accept writes. Fence the old primary (STONITH, cloud disable API, Patroni lock). Application-level “both regions writable” without merge rules is split-brain with extra steps. LWW loses money.

**82. Read-your-writes after you add a replica?**
Checkout POST then GET must hit the **writer**, or wait for LSN, or use session tokens (Aurora/Cosmos). Replica is for paths with a lag SLO. Sticky sessions that still send the confirmation read to a lagging replica are a product bug.

**83. Replication slot disk outage?**
Consumer (logical replica, Debezium) stopped; primary retains WAL. Monitor slot LSN age and disk. Drop dead slots; never “pause CDC” without a disk alarm. This is the 5 TB migration killer.

---

## Partition, shard, CDC, outbox

**84. Partition vs shard?**
Partition: one cluster, planner prunes (time, tenant). Shard: many primaries, app or proxy routing, no cheap cross-shard join. Partition when the table is large but one writer still fits. Shard when writes or working set exceed one primary **after** indexes, pools, and workload split.

**85. Shard key for SaaS?**
Usually `tenant_id`, with a whale plan (dedicated shard, row-level isolation, or refuse the tenant). Hashing `user_id` when every query is by tenant is a self-join tax. Cross-shard unique email needs a global lookup service — say so.

**86. Why is PK = timestamp a hotspot?**
All inserts land on one range, partition, or tablet. Time-ordered UUIDv7/Snowflake IDs still hotspot if you partition only on time and one tenant owns the second. Spread writes; do not “UUID because sharded.”

**87. Cross-shard unique constraint?**
Not cheap. Assignment service, global secondary lookup, or accept duplicates until a sweeper. Unique in SQL is a single-primary feature. Interviewers want you to drop the constraint or name the extra system.

**88. CDC — what is it for?**
Change Data Capture: emit committed row events (logical decoding, binlog, Dynamo streams) for search, cache, warehouse, outbox consumers. It is not a backup. Lag, schema evolution, and deletes (tombstones) are the design. Polling `updated_at` misses gaps; CDC is for volume and correctness.

**89. Outbox vs dual-write vs 2PC?**
Outbox: business row and event row in the **same** database transaction; publisher CDC or poller; consumers idempotent (at-least-once). Dual-write to DB and Kafka from the app loses one side. 2PC/XA: in-doubt transactions hold locks; coordinator is a SPOF — avoid across microservices and mail vendors.
**Fail:** 2PC with five databases; or “we’ll dual-write until the API is ready.”

**90. Scale ladder before you shard?**
Query/index → connection pool → cache → replica (lag OK) → partition → shard or NewSQL. CPU 90% on OLTP is `pg_stat_statements` and `EXPLAIN`, not Cockroach because Netflix. Writes 10× with unchanged reads is not “add replicas.”

---

## Managed, compliance, industry

**91. Managed vs self-host — decision?**
Team skill, extensions (PostGIS, pgvector), version lag, network, backup drills, cost of an operator vs RDS. Managed wins default HA/PITR for most squads. Self-host (CNPG, Patroni, CloudNativePG) when you need extensions, custom WAL, or a K8s estate that already runs operators. Kubernetes Deployment of three Postgres replicas on one PVC is not self-host — it is corruption.

**92. Dynamo vs SQL for a 50-person SaaS cart?**
SQL (Postgres) until access patterns and QPS force KV. Amazon’s paper is **their** scale: always-writable cart in Dynamo-class KV, orders and tax invoices relational. Copying Dynamo Global Tables for 400 QPS is Netflix-mesh energy. Copying one Postgres as Amazon’s only cart is the opposite fail.

**93. RDS Postgres vs Aurora vs “we’ll run Patroni on EKS”?**
RDS: least drama, extension limits. Aurora: failover and replica story, still a writer. Patroni/CNPG: you own fencing, backups, upgrades, and the on-call. HPA on primary CPU is the wrong lever in all three. Liquibase runs as one Job, not in every app pod.

**94. DPDP (India) at data-layer height?**
Classify first (personal vs restricted). Name fiduciary, purpose, residency, DSR (export/erase — including **embeddings** and backups), subprocessors, DPA. Encryption is not a DPIA. Sending KYC video embeddings to a US ANN SaaS because the vendor has SOC 2 is a likely **deny** unless in-region and erasable. SOC 2 is not a DPDP program.

**95. PCI at data-layer height?**
Cardholder data (PAN, track) in scope: minimize, tokenize, do not log, encrypt, isolate CDE, network and access evidence. Store a token or last-four, not PAN, in the OLTP you scale. Async replica of the CDE into a data science VPC is still PCI. `synchronous_commit = off` on authorization is a finding, not a latency win.

**96. Why LinkedIn Kafka instead of a bigger database? (steal the question)**
Many consumers needed the **same history independently**, with replay, without coupling to one OLTP schema. Feed, search, and counts are projections. A bigger Oracle would still be a snapshot plus extract jobs. Fail if Kafka has one consumer and you cannot name replay.

**97. Amazon shopping cart at their scale? (steal the question)**
Always-writable cart: Dynamo-class partitioned KV (Dynamo 2007 paper). Order, payment, tax invoice: relational, strong transactions, idempotency. Fail: one Postgres as the only cart at that QPS **or** Dynamo as the tax invoice SoR.

**98. What do you copy from Zerodha vs Netflix for a 50-person SaaS?**
Zerodha: Postgres + Redis, short path, no zoo, boring HA you can drill. Netflix: cache + HA store + Kafka **after** measured fan-out and multi-region. Fail: Netflix service mesh and Cassandra for balances at 400 QPS because a blog said “web scale.”

**99. Design ChatGPT’s product data layer (not GPUs)?**
Users, orgs, threads, usage, files: OLTP SoR. Rate limits: Redis. Blobs: object storage. RAG: vector **projection** of files, rebuildable. Reject vector DB as billing SoR. Industry: inferred — OpenAI does not publish the chat schema; do not fake an ERD as leaked truth.

**100. First 90 days as DB architect on a brownfield app?**
Measure (`pg_stat_statements`, Performance Insights), connection pool, backup **restore** drill, HA reality vs wiki, schema-as-code, kill idle-in-tx, drop unused indexes, write RPO/RTO, write one scale ladder. Name SoR vs search vs cache vs stream vs warehouse. If you cannot say who is **A** for the engine choice, you are collecting logos.

---

**How to drill:** cover the answer, speak 90 seconds, then the **Fail** line. After any answer they ask *how would you measure that?* — `pg_stat_activity`, `pg_stat_statements`, `EXPLAIN (ANALYZE, BUFFERS)`, replica lag, slot LSN, `age(datfrozenxid)`, last restore drill clock.
