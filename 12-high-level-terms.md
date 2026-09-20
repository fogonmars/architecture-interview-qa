# High-level terms — all tracks (plain English index)

**Start here if jargon feels dense.** Each notebook has a full page; this is the map.

| Track | Live page | What it covers |
|---|---|---|
| **Database** | [/dbnotes/HIGH_LEVEL_TERMS.html](https://notepads-6389e.web.app/dbnotes/HIGH_LEVEL_TERMS.html) | SoR, OLTP/OLAP/search/cache/stream, HA/DR, CDC, outbox |
| **Frontend** | [/frontend/HIGH_LEVEL_TERMS.html](https://notepads-6389e.web.app/frontend/HIGH_LEVEL_TERMS.html) | CSR/SSR, BFF, MFE, CWV, push vs socket |
| **Backend / microservices** | [/backend/HIGH_LEVEL_TERMS.html](https://notepads-6389e.web.app/backend/HIGH_LEVEL_TERMS.html) | Monolith vs services, saga, outbox, gateway, resilience |
| **Cloud** | [/interview/12-cloud-terms.html](https://notepads-6389e.web.app/interview/12-cloud-terms.html) | Same job on AWS vs Azure vs GCP |
| **AI** | [/ai/HIGH_LEVEL_TERMS.html](https://notepads-6389e.web.app/ai/HIGH_LEVEL_TERMS.html) | LLM, RAG, embeddings, agents, eval |

**Practical vs bubble (stories, not just words):**

- https://notepads-6389e.web.app/dbnotes/PRACTICAL_VS_BUBBLE.html  
- https://notepads-6389e.web.app/frontend/PRACTICAL_VS_BUBBLE.html  
- https://notepads-6389e.web.app/backend/PRACTICAL_VS_BUBBLE.html  
- https://notepads-6389e.web.app/ai/PRACTICAL_VS_BUBBLE.html  

## One shared sentence for every track

> Name the **system of record**, name every **helper copy (projection)**, and refuse to put money or identity only in a cache, log, search index, or model.

## Mini cheat — words that appear everywhere

| Word | Plain English |
|---|---|
| **SoR** | Source of truth that wins conflicts |
| **Projection** | Rebuildable helper copy |
| **BFF** | Backend shaped for the UI |
| **Idempotent** | Retry safely without double effect |
| **Outbox** | Event saved with the DB row in one commit |
| **AuthN / AuthZ** | Who you are / what you may do |

**Next:** pick your track’s HIGH_LEVEL_TERMS page, then [07 enterprise real apps](07-enterprise.md).
