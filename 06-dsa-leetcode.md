# DSA and LeetCode — by section (12-year architect)

**Primary hire bar is architecture** ([00](00-levels.md), [07](07-enterprise.md)).  
Use this when a panel still codes, or to map **patterns → your track**. Official: [leetcode.com](https://leetcode.com/problemset/).

**Rule:** time + space, then one **production failure**.

Live: `/interview/06-dsa-leetcode.html` · GitHub: this file in [architecture-interview-qa](https://github.com/fogonmars/architecture-interview-qa).

---

## Quick map — which DSA for which interview file

| Interview section | Notebook | DSA focus | Also |
|---|---|---|---|
| [01 Database](01-database.md) | `/dbnotes/` | Intervals, heap, union-find, BFS (topo), binary search | [08 SQL](08-sql-coding.md) **first** |
| [02 Frontend](02-frontend.md) | `/frontend/` | Strings, stacks, trees (DOM), debounce/throttle, LRU | Event loop verbal |
| [03 Backend](03-backend.md) | `/backend/` | LRU, rate limiter, producers, graphs (deps), concurrency | Idempotency talk |
| [04 AWS/Azure](04-aws-azure.md) | DB 36 · BE 35 · FE 39 | Light — design > code | Job map drills |
| [05 Angular](05-angular.md) | FE 26 | Same as frontend + Rx mental model | |
| [09 AI](09-ai.md) | `/ai/` | Rare code; maybe tokenize/window / top-k | Gold eval, RAG design |
| [10 Mobile](10-mobile.md) | FE 40 | Same as FE + offline queue talk | |
| [11 Specialist](11-specialist.md) | FE 41–46 | Graphs (WebRTC mesh), geometry lite | Design not LC |

**Architect default:** ~20 mediums cold from sections below that match **your JD**, plus SQL if data/backend.

---

## Shared core (everyone who codes)

Do these once; reuse across tracks.

| # | Problem | Maps to |
|---|---|---|
| 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | Hash index analog |
| 2 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Parsers / templates |
| 3 | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Leave overlap → still SQL |
| 4 | [LRU Cache](https://leetcode.com/problems/lru-cache/) | Redis/Caffeine — SoR still DB |
| 5 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Connected components |
| 6 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | Deploy/migration DAG |
| 7 | [Binary Search](https://leetcode.com/problems/binary-search/) | Template |
| 8 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Sliding window |

---

## Database / data architect — DSA + SQL

**Prefer [08 SQL](08-sql-coding.md) over new hards.**

| Pattern | Problems | Enterprise sentence |
|---|---|---|
| Intervals | Merge / Insert / Non-overlapping Intervals | Exclusion constraint in Postgres |
| Heap / Top-K | [Top K Frequent](https://leetcode.com/problems/top-k-frequent-elements/), [Kth Largest](https://leetcode.com/problems/kth-largest-element-in-an-array/) | “Then I’d use a warehouse for heavy Top-K” |
| Union-find | [Redundant Connection](https://leetcode.com/problems/redundant-connection/), connected components | Partition membership |
| BFS shortest | [Network Delay Time](https://leetcode.com/problems/network-delay-time/) | p99 path / timeout budget |
| Design | [Time Based KV](https://leetcode.com/problems/time-based-key-value-store/) | Bi-temporal lite — real answer is DB |

---

## Frontend / Angular — DSA + JS drills

| Pattern | Problems / drills | Enterprise sentence |
|---|---|---|
| Stack / string | Valid Parentheses, Decode String | Template / rich text |
| Trees | Level order, LCA, serialize | Component tree / comments |
| Sliding window | Longest substring, min window | Search UX |
| Design | [Encode TinyURL](https://leetcode.com/problems/encode-and-decode-tinyurl/) | Hash + collision |
| **JS (non-LC)** | Debounce, throttle, `Promise.allSettled`, deep clone, event-loop order | CWV / BFF fan-out |
| **Angular** | RxJS switchMap vs mergeMap verbal | Cancel stale HTTP |

---

## Backend — DSA + concurrency

| Pattern | Problems | Enterprise sentence |
|---|---|---|
| LRU | LRU Cache | Then Redis; SoR = DB |
| Design | [Hit Counter](https://leetcode.com/problems/design-hit-counter/), [Logger Rate Limiter](https://leetcode.com/problems/logger-rate-limiter/) | Then Redis sliding window |
| Graphs | Course Schedule I/II | Liquibase / service deps |
| Producer-consumer | Whiteboard bounded queue | Bulkhead / worker pool |
| Concurrency | [Print in Order](https://leetcode.com/problems/print-in-order/) | Happens-before; DB deadlock same idea |

---

## AI architect — rarely LeetCode

If they force code: sliding window (context), top-k (retrieve), tokenize counts.  
**Real screen:** RAG design, ACL, eval, refuse ([09](09-ai.md), `/ai/`).

---

## Mobile — same as FE +

Offline outbox idempotency (verbal), interval merge for sync conflicts, rate limiter for API. Chapter [10](10-mobile.md).

---

## AWS / Azure / enterprise

Almost no DSA. Drill [04](04-aws-azure.md) + [07](07-enterprise.md) job maps.

---

## Specialist (WebRTC, Electron, WebGL, AR, email, federation)

Design questions > LC. Optional: graph connectivity (mesh), geometry (interval/AABB verbal). See [11](11-specialist.md).

---

## Full pattern list (if JD is DSA-heavy)

Use classic sets: arrays/window → stack/list → trees/heap → graph → DP (only if hard screen) → binary search. Prefer [NeetCode roadmap order](https://neetcode.io/) but **stop** after ~20 cold solves and return to [07](07-enterprise.md).

| Skip unless hard screen | Edit Distance, hard DP |
|---|---|

---

## Two-week warm-up (architect who must code)

| Days | Focus |
|---|---|
| 1–4 | Shared core 1–8 + your track table |
| 5–8 | Blind re-solve + [08 SQL](08-sql-coding.md) if DB/BE |
| 9–14 | [07](07-enterprise.md) daily + flashcards for JD |

Then stop grinding. Win on SoR, dual-write, residual risk.
