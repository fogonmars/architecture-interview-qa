# DSA and LeetCode — optional screen (12-year architect track)

**Primary prep for this repo is architecture** ([00-levels](00-levels.md), [07-enterprise](07-enterprise.md)).  
Some product companies still run a **45–60 min coding screen** before the design panel. This file is that **optional** bar — patterns, not 2000 problems.

Official: [leetcode.com](https://leetcode.com/problemset/).

**Architect rule:** if you code, say **time + space**, then one **enterprise failure** (“O(n) memory — don’t do this on a 10M row API without a limit”). You still win the job on SoR / dual-write / residual risk, not Edit Distance.

## How many problems?

| Track | Target | Cadence |
|---|---|---|
| **12y architect (default)** | Re-solve **~20 mediums cold** + SQL comfort | 2–3/week before a product-company screen |
| Staff/TA mixed panel | Patterns 1–4 + LRU + intervals | Light |
| Only if JD is DSA-heavy | Full list below | Time-box; do not skip [07](07-enterprise.md) |

If the company is **Accenture / Infosys / bank Java**: arrays, strings, HashMap, SQL, collections. If **product / FAANG-shaped**: trees, graphs, DP, concurrency.

---

## Patterns → LeetCode (do in this order)

Links are the public problem pages.

### 1. Arrays / two pointers / sliding window (2y must)

| # | Problem | Why interviews use it |
|---|---|---|
| 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | Hash map vs nested loop |
| 2 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | One pass min |
| 3 | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | Set |
| 4 | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | Count arrays |
| 5 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Hash of counts |
| 6 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Heap vs bucket |
| 7 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Prefix; no division |
| 8 | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Kadane |
| 9 | [3Sum](https://leetcode.com/problems/3sum/) | Sort + two pointers |
| 10 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Two pointers |
| 11 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Senior bar |
| 12 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Sliding window |
| 13 | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Window + need map |
| 14 | [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | Window |
| 15 | [Permutation in String](https://leetcode.com/problems/permutation-in-string/) | Window of counts |
| 16 | [Move Zeroes](https://leetcode.com/problems/move-zeroes/) | In-place |
| 17 | [Sort Colors](https://leetcode.com/problems/sort-colors/) | Dutch flag |
| 18 | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | Sort + sweep — **calendar / leave overlap** analog |
| 19 | [Insert Interval](https://leetcode.com/problems/insert-interval/) | Same family |
| 20 | [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Greedy |

**Enterprise pointer:** leave overlap and “merge meeting rooms” are **interval** problems in disguise. After you code, say you’d still enforce overlap in **SQL unique/exclusion**, not only in JS.

### 2. Stack / string / linked list (2y)

| # | Problem | Why |
|---|---|---|
| 21 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Stack |
| 22 | [Min Stack](https://leetcode.com/problems/min-stack/) | Aux stack |
| 23 | [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | Stack |
| 24 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Monotonic stack |
| 25 | [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Senior |
| 26 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Classic |
| 27 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Merge step of mergesort |
| 28 | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Floyd |
| 29 | [Reorder List](https://leetcode.com/problems/reorder-list/) | Reverse + weave |
| 30 | [Remove Nth Node From End](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Two pointers |
| 31 | [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | Carry |
| 32 | [LRU Cache](https://leetcode.com/problems/lru-cache/) | **HashMap + DLL** — maps to Redis/Caffeine talk |

**Enterprise pointer:** LRU Cache is how you **explain** an in-process cache. Then say: distributed cache is Redis; SoR is still the DB ([01](01-database.md) Redis Q).

### 3. Trees / BST / heap (2y–senior)

| # | Problem | Why |
|---|---|---|
| 33 | [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | Recursion baseline |
| 34 | [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | DFS |
| 35 | [Same Tree](https://leetcode.com/problems/same-tree/) | Recursion |
| 36 | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | BFS queue |
| 37 | [Validate BST](https://leetcode.com/problems/validate-binary-search-tree/) | Bounds |
| 38 | [Kth Smallest in BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | Inorder |
| 39 | [Lowest Common Ancestor of BST](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | Walk |
| 40 | [Lowest Common Ancestor of Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | Recursion |
| 41 | [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Hard-adjacent |
| 42 | [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Senior |
| 43 | [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) | |
| 44 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Heap / quickselect |
| 45 | [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Two heaps |
| 46 | [Task Scheduler](https://leetcode.com/problems/task-scheduler/) | Greedy + count |
| 47 | [Design Twitter](https://leetcode.com/problems/design-twitter/) | **Lite system design in code** |

### 4. Graphs / BFS / DFS (senior bar; 2y if product company)

| # | Problem | Why |
|---|---|---|
| 48 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Grid DFS |
| 49 | [Clone Graph](https://leetcode.com/problems/clone-graph/) | Hash + DFS |
| 50 | [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | Multi-source |
| 51 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | Cycle / Kahn |
| 52 | [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | Topo order |
| 53 | [Word Ladder](https://leetcode.com/problems/word-ladder/) | BFS |
| 54 | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Multi-source BFS |
| 55 | [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) | n-1 edges + connected |
| 56 | [Number of Connected Components](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | Union-find |
| 57 | [Redundant Connection](https://leetcode.com/problems/redundant-connection/) | Union-find |
| 58 | [Network Delay Time](https://leetcode.com/problems/network-delay-time/) | Dijkstra — **timeouts analog** |
| 59 | [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | Bellman / BFS |

**Enterprise pointer:** Course Schedule = **DAG of deploys / liquibase**. Network Delay = **p99 path through services**. After code, one sentence of architecture.

### 5. DP (senior / FAANG; 2y only if JD says DSA strong)

| # | Problem | Why |
|---|---|---|
| 60 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | Fib |
| 61 | [House Robber](https://leetcode.com/problems/house-robber/) | Linear DP |
| 62 | [House Robber II](https://leetcode.com/problems/house-robber-ii/) | Circular |
| 63 | [Coin Change](https://leetcode.com/problems/coin-change/) | Unbounded knapsack |
| 64 | [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | n log n follow-up |
| 65 | [Word Break](https://leetcode.com/problems/word-break/) | |
| 66 | [Combination Sum](https://leetcode.com/problems/combination-sum/) | Backtrack |
| 67 | [Unique Paths](https://leetcode.com/problems/unique-paths/) | Grid DP |
| 68 | [Jump Game](https://leetcode.com/problems/jump-game/) | Greedy/DP |
| 69 | [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | 2D DP |
| 70 | [Edit Distance](https://leetcode.com/problems/edit-distance/) | Hard-adjacent |
| 71 | [Decode Ways](https://leetcode.com/problems/decode-ways/) | |

Skip 70–71 if you are 2 years and the company is a service firm. Do 60–68.

### 6. Binary search / bits / math

| # | Problem | Why |
|---|---|---|
| 72 | [Binary Search](https://leetcode.com/problems/binary-search/) | Template |
| 73 | [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | |
| 74 | [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Search on answer |
| 75 | [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | |
| 76 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | |
| 77 | [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) | **Bi-temporal lite** |
| 78 | [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | |
| 79 | [Counting Bits](https://leetcode.com/problems/counting-bits/) | |
| 80 | [Missing Number](https://leetcode.com/problems/missing-number/) | XOR |

### 7. Frontend-flavored (JS interviews)

Implement **without** a framework. Then map to React.

| Practice | Analog in the job |
|---|---|
| Debounce / throttle a function | Search box INP ([02](02-frontend.md) CWV) |
| `Promise.all` vs `allSettled` | BFF fan-out |
| Deep clone vs structuredClone | Don’t clone the Query cache |
| Event loop: microtask vs macrotask | Why `setTimeout(0)` isn’t a scheduler |
| Flatten nested comments | Tree DFS — same as LC trees |
| LRU in JS `Map` | Client cache; still not SoR |
| [Encode and Decode TinyURL](https://leetcode.com/problems/encode-and-decode-tinyurl/) | Hash + collision — design lite |
| Virtual list (describe) | 10k rows; don’t render 10k DOM |

LeetCode JS: filter tag **JavaScript**. Prefer writing **TypeScript** in the panel if the job is TS.

### 8. Backend-flavored (Java / Go)

| Practice | Analog |
|---|---|
| [LRU Cache](https://leetcode.com/problems/lru-cache/) | Caffeine / LinkedHashMap |
| Producer-consumer with queue (whiteboard) | Bounded worker pool |
| Rate limiter sliding window (code) | Redis INCR analog; then say Redis in prod |
| [Design Hit Counter](https://leetcode.com/problems/design-hit-counter/) | |
| [Logger Rate Limiter](https://leetcode.com/problems/logger-rate-limiter/) | |
| Concurrent hashmap vs ConcurrentHashMap talk | Java senior |
| Context cancel in Go: `errgroup` | Timeouts ([03](03-backend.md)) |

Do **not** invent a thread pool on a LeetCode that is single-threaded. After the code: “In prod this is a bulkhead.”

### 9. Concurrency (Java senior; skip at 2y unless JD is concurrent)

| Topic | Drill |
|---|---|
| Happens-before, volatile vs synchronized | Verbal + tiny code |
| Deadlock: lock order | Same as DB deadlock ([01](01-database.md)) |
| CompletableFuture / goroutines + channel | One kata |
| [Print in Order](https://leetcode.com/problems/print-in-order/) | Barriers |
| [Fizz Buzz Multithreaded](https://leetcode.com/problems/fizz-buzz-multithreaded/) | Optional |

---

## Complexity you must say out loud

| Structure | Get | Extra |
|---|---|---|
| Hash map | Average O(1) | Worst O(n); load factor |
| Heap | peek O(1), push log n | |
| Sorted array + binary search | log n | Must be sorted |
| BFS/DFS graph | O(V+E) | |
| DP 2D | O(n·m) time and often memory | Space-opt |

**Enterprise:** an O(n²) nested loop over orders in an API is an **N+1 or CPU Sev-1**, not a “we’ll shard.”

---

## Company shape (India + global)

| Company shape | DSA | Also |
|---|---|---|
| Service / Accenture L9–L11 (~2–5y) | Easy–medium arrays/strings/SQL | Java collections, Spring verbal |
| Product mid (Razorpay, Zerodha-class bar) | Medium + one design | Postgres, Redis |
| FAANG / hard product | Medium–hard + design | [07](07-enterprise.md) |
| Architect hire | Maybe one medium | SoR, AWS/Azure, programme |

---

## 30-day calendar (2 years)

| Week | Focus | Count |
|---|---|---|
| 1 | Arrays + hash + two pointers | 01–12 |
| 2 | Window + stack + linked list | 13–32 |
| 3 | Trees + heap + intervals | 33–47, 18–20 |
| 4 | Graph **or** DP (pick by JD) + SQL [08](08-sql-coding.md) | 48–59 or 60–68 |

Re-solve **blind**. If you peek, it does not count.

## After you pass the coding screen

Stop grinding new hards. Switch to [07-enterprise.md](07-enterprise.md) and the flashcards for your track. Architect interviews are lost on **dual-write** and **JWT in localStorage**, not on Edit Distance.
