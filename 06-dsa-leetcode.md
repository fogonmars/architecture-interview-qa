# DSA and LeetCode — optional coding screen (architect track)

**This repo’s bar is ~12-year architecture** ([00-levels](00-levels.md), [07-enterprise](07-enterprise.md)).  
Some product/FAANG-shaped panels still run a **45–60 min coding screen** before design. Use this file only for that screen — patterns, not a junior grind.

Official: [leetcode.com](https://leetcode.com/problemset/).

**Architect rule:** time + space, then one **production failure** (“O(n) memory — don’t do this on a 10M-row API without a limit”). You still clear the hire on **SoR, dual-write, residual risk, AWS/Azure job map** — not Edit Distance.

## How much (architect)

| Situation | Target |
|---|---|
| Default architect hire | Re-solve **~20 mediums cold** + [08 SQL](08-sql-coding.md) |
| Product company with hard screen | Patterns 1–5 + LRU + intervals + one graph |
| DSA-heavy JD | Full list; **time-box** — do not skip [07](07-enterprise.md) |

---

## Patterns → LeetCode (warm-up order)

### 1. Arrays / two pointers / sliding window

| # | Problem | Why / enterprise pointer |
|---|---|---|
| 1 | [Two Sum](https://leetcode.com/problems/two-sum/) | Hash map vs nested loop |
| 2 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | One pass |
| 3 | [Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) | Set |
| 4 | [Valid Anagram](https://leetcode.com/problems/valid-anagram/) | Counts |
| 5 | [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Hash of counts |
| 6 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Heap vs bucket |
| 7 | [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Prefix |
| 8 | [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) | Kadane |
| 9 | [3Sum](https://leetcode.com/problems/3sum/) | Sort + two pointers |
| 10 | [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Two pointers |
| 11 | [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Harder screen |
| 12 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Window |
| 13 | [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Window + need map |
| 14 | [Longest Repeating Character Replacement](https://leetcode.com/problems/longest-repeating-character-replacement/) | Window |
| 15 | [Permutation in String](https://leetcode.com/problems/permutation-in-string/) | Window of counts |
| 16 | [Move Zeroes](https://leetcode.com/problems/move-zeroes/) | In-place |
| 17 | [Sort Colors](https://leetcode.com/problems/sort-colors/) | Dutch flag |
| 18 | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | **Leave / calendar overlap** analog — still enforce in SQL |
| 19 | [Insert Interval](https://leetcode.com/problems/insert-interval/) | Same family |
| 20 | [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Greedy |

### 2. Stack / string / linked list

| # | Problem | Why |
|---|---|---|
| 21 | [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Stack |
| 22 | [Min Stack](https://leetcode.com/problems/min-stack/) | Aux stack |
| 23 | [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | Stack |
| 24 | [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Monotonic stack |
| 25 | [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Harder |
| 26 | [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Classic |
| 27 | [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Merge |
| 28 | [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Floyd |
| 29 | [Reorder List](https://leetcode.com/problems/reorder-list/) | Reverse + weave |
| 30 | [Remove Nth Node From End](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Two pointers |
| 31 | [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/) | Carry |
| 32 | [LRU Cache](https://leetcode.com/problems/lru-cache/) | **HashMap + DLL** → then say Redis/Caffeine; SoR still DB |

### 3. Trees / BST / heap

| # | Problem | Why |
|---|---|---|
| 33 | [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/) | Recursion baseline |
| 34 | [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | DFS |
| 35 | [Same Tree](https://leetcode.com/problems/same-tree/) | |
| 36 | [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/) | BFS |
| 37 | [Validate BST](https://leetcode.com/problems/validate-binary-search-tree/) | Bounds |
| 38 | [Kth Smallest in BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | Inorder |
| 39 | [Lowest Common Ancestor of BST](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | |
| 40 | [Lowest Common Ancestor of Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | |
| 41 | [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Hard-adjacent |
| 42 | [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | |
| 43 | [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) | |
| 44 | [Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Heap |
| 45 | [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Two heaps |
| 46 | [Task Scheduler](https://leetcode.com/problems/task-scheduler/) | Greedy |
| 47 | [Design Twitter](https://leetcode.com/problems/design-twitter/) | Lite design in code |

### 4. Graphs / BFS / DFS

| # | Problem | Enterprise pointer |
|---|---|---|
| 48 | [Number of Islands](https://leetcode.com/problems/number-of-islands/) | Grid DFS |
| 49 | [Clone Graph](https://leetcode.com/problems/clone-graph/) | |
| 50 | [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) | Multi-source |
| 51 | [Course Schedule](https://leetcode.com/problems/course-schedule/) | **DAG of deploys / migrations** |
| 52 | [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | Topo order |
| 53 | [Word Ladder](https://leetcode.com/problems/word-ladder/) | BFS |
| 54 | [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Multi-source BFS |
| 55 | [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) | |
| 56 | [Number of Connected Components](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | Union-find |
| 57 | [Redundant Connection](https://leetcode.com/problems/redundant-connection/) | |
| 58 | [Network Delay Time](https://leetcode.com/problems/network-delay-time/) | **p99 path / timeouts** |
| 59 | [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | |

### 5. DP (only if the screen is hard)

| # | Problem | Why |
|---|---|---|
| 60 | [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) | Fib |
| 61 | [House Robber](https://leetcode.com/problems/house-robber/) | |
| 62 | [House Robber II](https://leetcode.com/problems/house-robber-ii/) | |
| 63 | [Coin Change](https://leetcode.com/problems/coin-change/) | |
| 64 | [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | |
| 65 | [Word Break](https://leetcode.com/problems/word-break/) | |
| 66 | [Combination Sum](https://leetcode.com/problems/combination-sum/) | Backtrack |
| 67 | [Unique Paths](https://leetcode.com/problems/unique-paths/) | |
| 68 | [Jump Game](https://leetcode.com/problems/jump-game/) | |
| 69 | [Longest Common Subsequence](https://leetcode.com/problems/longest-common-subsequence/) | |
| 70 | [Edit Distance](https://leetcode.com/problems/edit-distance/) | Skip unless hard screen |
| 71 | [Decode Ways](https://leetcode.com/problems/decode-ways/) | Optional |

### 6. Binary search / bits

| # | Problem | Why |
|---|---|---|
| 72 | [Binary Search](https://leetcode.com/problems/binary-search/) | Template |
| 73 | [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | |
| 74 | [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Search on answer |
| 75 | [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | |
| 76 | [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | |
| 77 | [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) | Bi-temporal lite |
| 78–80 | Bit/count problems | Optional |

### 7. Frontend-flavored (if FE architect screen codes)

Debounce/throttle, `Promise.all` vs `allSettled`, event loop, flatten nested comments, LRU in `Map`, virtual list talk → map to CWV / BFF ([02](02-frontend.md)).

### 8. Backend-flavored (Java / Go)

LRU, rate limiter whiteboard → Redis in prod, hit counter, concurrent map talk, Go `errgroup` cancel → bulkhead ([03](03-backend.md)).

### 9. Concurrency (if they insist)

Happens-before, deadlock lock order (= DB deadlock), [Print in Order](https://leetcode.com/problems/print-in-order/) — then return to **architecture**.

---

## Complexity (say out loud)

| Structure | Get |
|---|---|
| Hash map | Average O(1); worst O(n) |
| Heap | peek O(1), push log n |
| BFS/DFS | O(V+E) |
| DP 2D | O(n·m) |

**Enterprise:** O(n²) over orders in an API is an **N+1/CPU Sev-1**, not “let’s shard.”

---

## Company shape (architect hires)

| Panel | Coding | What actually decides the hire |
|---|---|---|
| Accenture / bank / SI architect (L7 / Manager) | Often light or skipped | SoR, programme, AWS/Azure, residual risk — [07](07-enterprise.md) |
| Product architect | One medium + design | Same + scale ladder |
| FAANG Staff+ | Medium–hard + design | Still fail on dual-write more than DP |

---

## Two-week warm-up (before an architect screen that codes)

| Days | Focus |
|---|---|
| 1–3 | Arrays, hash, intervals 01–20 |
| 4–6 | Stack, LRU, trees 21–47 |
| 7–10 | Graph 48–59 + SQL [08](08-sql-coding.md) |
| 11–14 | Blind re-solve 20 mediums + [07](07-enterprise.md) every day |

Then **stop grinding**. Spend remaining time on real apps, AI practical vs bubble, and cloud job maps.
