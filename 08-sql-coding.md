# SQL for architect panels (~12 years)

At **Technical / Solution / Enterprise Architect** depth, panels still ask: **joins, indexes, isolation, EXPLAIN, and who is SoR.** Write correct SQL fast, then name the **failure**.

## What they expect

| Topic | Architect depth |
|---|---|
| Joins / `GROUP BY` / window functions | Correct; know when a window belongs in OLAP not OLTP |
| Indexes | B-tree vs GIN; covering; when index hurts writes |
| `EXPLAIN (ANALYZE, BUFFERS)` | Prove a plan; don’t guess “shard” |
| Isolation | Read phenomena; `SELECT FOR UPDATE`; leave overlap |
| Transactions | One aggregate; outbox in same tx |
| Pagination | Keyset vs `OFFSET` death |
| Migrations | Expand/contract; online DDL |

## Drill (write by hand)

1. Orders with customer name — inner join, filter status, order by date limit 50.  
2. Top N customers by GMV — `GROUP BY` + `ORDER BY SUM`.  
3. Running balance — window `SUM(...) OVER (PARTITION BY account ORDER BY ts)`.  
4. Overlapping leave — exclusion or range overlap predicate.  
5. Idempotent insert — unique business key + `ON CONFLICT`.  
6. Slow query story — sequential scan on unindexed filter; fix index; re-`EXPLAIN`.

## Enterprise pointers (say after the SQL)

- Money/leave: enforce in **DB constraints**, not only app.  
- Search/`LIKE %x%`: move to FTS/search projection.  
- Report on checkout primary: **OLAP**, not bigger OLTP.  
- “Just add Redis”: name what is cached and how invalidated.

**Next:** [01-database](01-database.md) · [07-enterprise](07-enterprise.md).
