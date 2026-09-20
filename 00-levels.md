# Levels: ~12-year architect (this repo’s bar)

**This handbook and interview set are aimed at Technical / Solution / Enterprise Architect depth (~10–15 years, L7 / Manager Architect / EA track).** Steal the **question**, not Netflix’s logo.

Live: https://notepads-6389e.web.app/interview/  
GitHub: https://github.com/fogonmars/architecture-interview-qa

Deep notebooks (architect chapters, not flashcards):

| Track | Live |
|---|---|
| DB | `/dbnotes/` |
| Frontend | `/frontend/` |
| Backend | `/backend/` |
| **AI (separate section)** | `/ai/` |

---

## What a 12-year panel actually grades

| They want | You deliver | Fail |
|---|---|---|
| **Who is SoR** | Named store + conflict winner | “We’ll use Kafka as the ledger” |
| **Failure mode** | What breaks, who pages, residual risk | Happy-path only |
| **Org fit** | Team skill, trains, ARB, when to say **no** | Copy Netflix at 10 QPS |
| **Cloud as job map** | Same job on AWS vs Azure | Logo bingo |
| **AI as component** | RAG/agents with ACL, eval, DSR | Vector DB as customer master |
| **Programme** | RACI, strangler, cost of change | “Microservices by December” |

DSA ([06](06-dsa-leetcode.md)) is **optional warmup** if a product company still runs a screen. Architects lose on **dual-write**, **JWT in localStorage**, and **cosine as law** — not Edit Distance.

---

## Study order (architect, ~6–8 weeks)

1. **Decision muscle** — DB 01 + 34, Backend 01 + 05 + 07, Frontend 01 + 34, AI 01 + [PRACTICAL_VS_BUBBLE](../ai/PRACTICAL_VS_BUBBLE.md) + 18.  
2. **Real work examples** — [07-enterprise](07-enterprise.md) (this file’s sister) + notebooks **industry + reference architectures**.  
3. **Flashcards** — [01](01-database.md)–[05](05-angular.md) + [09-ai](09-ai.md); say **90s + fail**.  
4. **Cloud RFP** — [04](04-aws-azure.md) + DB 36 + BE 35 + FE 39.  
5. **Scenarios** — DB 30, FE 30, BE 29, AI 23 (Req / Arch / Fail / 90s).

---

## Coding vs architecture (do not mix)

| They ask | You | Not |
|---|---|---|
| Design leave / claims / RAG | SoR, tx, projections, eval, residual risk | LeetCode DP |
| Why is this query slow? | `EXPLAIN`, index, bloat | “Let’s shard / mesh” |
| AWS vs Azure for this workload | Job map | Feature checklist |
| Invert a binary tree | Code (if they insist) | “I’d use microservices” |

---

## Real-work answer template (use in every panel)

For **any** product they name (Netflix, Zerodha, ChatGPT, your bank’s claims):

1. **Workload / constraints** (QPS class, money?, SEO?, residency?)  
2. **SoR vs projections** (OLTP / cache / search / stream / warehouse / vector)  
3. **Backend shape** (modular monolith vs few services; Java/Go/Node **where**)  
4. **Frontend shape** (CSR vs SSR; BFF; MFE only if org)  
5. **AI (if any)** — prompt / RAG / tools / classical ML; **never** model as ledger  
6. **What you’d refuse** and **residual risk**

Full worked examples: [07-enterprise.md](07-enterprise.md). Industry steal-the-question: [dbnotes 31](../dbnotes/31-industry-case-studies/README.md) · [backend 30](../backend/30-industry/README.md) · [frontend 31](../frontend/31-industry-case-studies/README.md) · [ai 22](../ai/22-industry-case-studies/README.md).

**Mobile clients:** [frontend 40](../frontend/40-react-native-android-ios/README.md) · [10-mobile](10-mobile.md).

