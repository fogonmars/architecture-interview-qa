# 80 AWS ↔ Azure Interview Questions (with answers)

Same job, two clouds. Every answer maps **AWS ↔ Azure**; **GCP** is named when it is the honest peer. Steal the **question**, not a re:Invent or Build slide. Deep chapters: [dbnotes 36](../dbnotes/36-aws-azure-data-platforms/README.md) · [backend 35](../backend/35-aws-azure-workloads/README.md) · [frontend 39](../frontend/39-aws-azure-frontend/README.md). GCP data peers also live in [dbnotes 06](../dbnotes/06-cloud/aws-azure-gcp.md) and [dbnotes 19](../dbnotes/19-cloud-managed-databases/README.md).

**Topics:** [Well-Architected](#well-architected) · [Landing zone & network](#landing-zone--network) · [Identity & keys](#identity--keys) · [Relational](#relational) · [NoSQL, cache, search](#nosql-cache-search) · [Lake & warehouse](#lake--warehouse) · [Messaging](#messaging) · [Compute](#compute) · [API & edge](#api--edge) · [Frontend hosts & auth](#frontend-hosts--auth) · [Observe & IaC](#observe--iac) · [India, cost, HA/DR](#india-cost-hadr)

---
**Notebooks:** [DB 36](../dbnotes/36-aws-azure-data-platforms/README.md) · [BE 35](../backend/35-aws-azure-workloads/README.md) · [FE 39](../frontend/39-aws-azure-frontend/README.md) · **DSA:** design > code ([06](06-dsa-leetcode.md))


## Well-Architected

**1. What are the Well-Architected pillars on AWS vs Azure?**
AWS Well-Architected and Azure Well-Architected / CAF both ask the same six: operational excellence, security, reliability, performance (efficiency), cost optimization, and sustainability. The architect translation is runbooks and IaC, identity and private data, Multi-AZ plus RPO/RTO, p99 and right-size, unit cost and idle, region and waste. GCP’s Well-Architected / Architecture Framework is the peer with the same pillars, not a third product catalog. Steal the **questions** in the pillar, not the PDF logo.

**2. Can a team “do Well-Architected” with a public RDS or Azure SQL endpoint?**
No. A six-person squad that decks Well-Architected but leaves Postgres on a public `5432` has failed **security** regardless of a slide. Shared responsibility on data: the cloud owns the DC and managed HA plumbing; you still own reconnect, idempotency, the pooler, CMK policy, and a restore you have **run**. Managed failover is still minutes and in-flight transactions are unknown.

**3. What is shared responsibility for runtime (compute) on AWS vs Azure?**
The cloud owns metal and the managed Kubernetes **control plane** (EKS / AKS; GCP peer is GKE). You own node pools, probes, pod identity, and NetworkPolicy. On PaaS (Beanstalk / App Runner vs App Service; GCP Cloud Run) you still own the app, config, authz, and timeouts. On Lambda vs Azure Functions (GCP Cloud Functions / Cloud Run jobs) you own cold start, connection pools, timeout, and the identity of the function.

---

## Landing zone & network

**4. What is a landing zone on AWS vs Azure?**
AWS: Organizations, OUs, Control Tower, accounts as environments. Azure: management groups, subscriptions, Cloud Adoption Framework landing zone. That is where the database actually lives — policy, network, keys, and audit — not a later ticket. GCP’s peer is folders, projects, and a landing-zone / org-policy setup. Do not invent a “prod VPC” that skips the org.

**5. How do you map landing-zone network jobs AWS ↔ Azure?**
VPC + subnets + security groups + NACLs + Transit Gateway vs VNet + subnets + NSGs + Azure Firewall + Virtual WAN. Edge is NLB/ALB, API Gateway, CloudFront vs Load Balancer / Application Gateway / Front Door and APIM. Hybrid is Direct Connect + TGW vs ExpressRoute + Virtual WAN; GCP’s peer is Cloud Interconnect + VPC. DNS is Route 53 vs Azure DNS (plus Private DNS zones).

**6. VPC vs VNet — are they the same idea?**
Yes as **isolation boundary**: CIDR, subnets, route tables, and a private data plane. AWS security groups are stateful L4; NACLs are subnet-stateless. Azure NSGs are the usual L4 control; Azure Firewall is the centralized egress/filter. GCP’s peer is VPC (global by default, unlike AWS regional VPCs). Java or Go on a VM is still honest: EC2 + ALB + systemd **or** Azure VM + App Gateway / nginx — Kubernetes is not mandatory.

**7. PrivateLink vs Private Endpoint?**
AWS **PrivateLink** / VPC endpoints bring RDS, Aurora, Dynamo, S3, OpenSearch (and much of the control plane) onto a private IP in your VPC. Azure **Private Endpoint** does the same for Flexible Server, Azure SQL, Cosmos, Blob, and AI Search. GCP’s peer is **Private Service Connect**. Public `5432` “temporarily” is **your** finding; turn private access on before the first SoR row.

**8. When do you still need NAT if you have PrivateLink / Private Endpoint?**
NAT Gateway is for **internet** egress (package mirrors, third-party APIs, some SaaS). PrivateLink/Private Endpoint removes NAT **to the PaaS** you already consume. GCP Cloud NAT is the peer tax. Architects who leave every subnet 0.0.0.0/0 → NAT “because Lambda needs the internet” pay GB forever.

**9. What is the DNS pairing for private data planes?**
AWS: Route 53 private hosted zones plus the PrivateLink hostname the SDK already uses. Azure: Azure DNS + **Private DNS zones** so the Flexible Server / Blob FQDN resolves to the private IP. If DNS still returns the public VIP, you did not finish Private Endpoint. Do not split-brain public and private names for the same SoR.

**10. Config/SCPs vs Azure Policy?**
AWS Config + Service Control Policies constrain accounts; Azure Policy (and templates / former Blueprints) constrain subscriptions and resource types. GCP org policies are the peer. Use them to ban public IPs on databases, require CMK, and deny “sandbox keys in prod.” Policy is not a substitute for engine audit (`pgaudit` / SQL Audit) on the data plane.

**11. Control-plane audit: CloudTrail vs Activity Log?**
CloudTrail is the AWS API audit; Azure Activity Log plus Azure Monitor is the peer. Data-plane audit is still the engine plus CloudWatch vs diagnostic settings. GCP Cloud Audit Logs is the third peer. Page the log you can actually query in an incident, not three unowned trails.

---

## Identity & keys

**12. IAM vs Entra ID + Managed Identity?**
AWS **IAM** (roles on instance/task/pod, Identity Center for humans) is the AWS identity fabric. Azure is **Entra ID** for humans plus **Managed Identity** (system or user-assigned) on compute, with Azure RBAC. GCP’s peer is Cloud IAM + attached service accounts. App role ≠ DBA; no shared `admin` connection string.

**13. How does an app authenticate to SQL on AWS vs Azure?**
Prefer **IAM DB authentication** (RDS/Aurora token) or a rotated secret in **Secrets Manager**. On Azure prefer **Managed Identity + Entra auth** to Azure SQL / Flexible Server when enabled, else Key Vault secret rotation. GCP: Cloud SQL IAM / Auth Proxy. Never: access keys in Git; `sa` in App Settings as the architecture.

**14. IRSA vs Azure Workload Identity?**
EKS **IRSA** (IAM Roles for Service Accounts) and AKS **Workload Identity** / federated credentials beat long-lived keys in Kubernetes Secrets. GCP Workload Identity is the peer. Spring Cloud AWS / Azure Identity and the default credential chains in Go and Node should consume that role, not an `AKIA` pasted into a ConfigMap.

**15. Entra on AWS — is that a smell?**
**Entra for workforce on AWS is normal** (SSO into Identity Center or SAML). **Cognito on Azure is rare** — do not invent it. Customer CIAM is Cognito user pools vs Entra External ID / B2C; GCP Identity Platform / Firebase Auth is the usual third. Do not smash employees and customers into one pool “for simplicity.”

**16. KMS vs Key Vault?**
AWS **KMS** customer-managed keys (CMK) wrap RDS/S3/EBS encryption. Azure **Key Vault** keys (or managed HSM) wrap Azure SQL / Flexible / Blob. GCP Cloud KMS / CMEK is the peer. Separate **prod and sandbox** keys. Who can **disable** the key is a Sev-1: the cloud will encrypt, you still own blast radius and rotation policy.

**17. Secrets Manager vs Key Vault for connection strings?**
Secrets Manager + RDS rotation Lambda vs Key Vault rotation (and App Configuration for flags). SSM Parameter Store is the cheap AWS sibling; Azure App Configuration is flags, not the SoR password. Rotation is mandatory; a static secret in Git is a breach even if KMS encrypted the disk.

**18. Human DBA path: bastion vs Entra?**
AWS: IAM Identity Center + SSM Session Manager / bastion; AD if you still run SQL Server the old way. Azure: Entra ID + Azure AD authentication for Azure SQL / Flexible when enabled. Do not leave a jump box with a shared Unix password as the “landing zone.”

---

## Relational

**19. RDS vs Azure Database Flexible Server?**
**RDS** PostgreSQL/MySQL/Maria/SQL Server/Oracle is “you size the instance and disk, they patch and backup.” Azure **Flexible Server** is the current Postgres/MySQL analog (Single Server is legacy). GCP **Cloud SQL** is the peer; **AlloyDB** sits nearer Aurora for PG. You still choose version, `max_connections`, HA SKU, and a parameter/config story — extensions are **whitelisted**, not “apt-get on the box.”

**20. Aurora vs Azure SQL Hyperscale — same product?**
No. **Aurora** (MySQL/PostgreSQL-compatible) is distributed storage (six copies across AZs) with compute detached; replicas share the volume. Azure SQL **Hyperscale** is a **SQL Server storage-scale** story, not Aurora and **not** Postgres. Aurora is not 100% PG (extensions, slots, GUCs). GCP **AlloyDB** is the usual Aurora-shaped PG peer; **Spanner** is a different family (externally consistent global SQL, not PG dialect).

**21. Azure SQL Database vs Managed Instance vs RDS SQL Server?**
**Azure SQL DB** is the PaaS database (single DB / elastic pool / Hyperscale). **Managed Instance** is the lift for Agent, linked servers, and near-full SQL Server. RDS SQL Server is the AWS managed instance-shaped offer; SQL Server on EC2/VM when you need the exact box. License and Hybrid Benefit are the interview, not the logo.

**22. When do you pick Azure SQL MI over RDS SQL Server?**
When the estate is already Entra, the app uses SQL Agent/CLR-ish surface, and the RFP froze Azure. RDS SQL Server is honest on an AWS estate. Do not dual-run both as “HA.” GCP has Cloud SQL for SQL Server but **Azure still has SQL Server gravity**.

**23. Aurora Serverless v2 vs Azure SQL serverless / Flexible burst?**
Both are for **spiky** OLTP with a min capacity you forgot to lower. Aurora Serverless v2 ACUs vs Azure SQL serverless / Flexible burst SKUs. GCP has no perfect twin (Cloud SQL Enterprise Plus / AlloyDB autoscale is “close”). Watch **min ACU left at max** — serverless is not free idle.

**24. Aurora Global vs Azure SQL failover groups?**
Both are usually **async** second-region replicas, not zero RPO and not serializable global SQL. Cosmos multi-region is a **different family** — do not call failover groups “Cosmos.” GCP Spanner multi-region is the rare “global SQL with a consistency story you pay for.” Promote/failover is a **drill**, not a SKU checkbox.

**25. What still belongs to you on managed Postgres?**
Reconnect, idempotency, pooler, parameter groups vs Azure server parameters, major-version plan, and a restore you have run. Multi-AZ / zone-redundant is HA in **one region**. PITR windows exist on both; **off-account copy** of backups is still your residency sentence.

---

## NoSQL, cache, search

**26. DynamoDB vs Cosmos DB?**
Known partition key, huge scale: **DynamoDB** (+ optional DAX) vs **Cosmos** (Core/SQL API or Table API). GCP peers: **Firestore** (document) and **Bigtable** (wide-column), not one logo. Dynamo Global Tables ≈ last-writer-wins; Cosmos **session** is the default — neither is a bank ledger unless you designed the invariant. Hot partition = throttle (Dynamo) or 429 (Cosmos).

**27. DocumentDB vs Cosmos Mongo API vs Atlas?**
AWS **DocumentDB** is Mongo-**compatible**, not MongoDB Atlas — compatibility gaps show up in prod. Azure Cosmos **Mongo** API is the Azure-shaped twin and is still a **different product** from Core SQL API. Do not bill “one Cosmos, five APIs” as one mental model. If you need real Mongo, say Atlas and own the estate exception.

**28. Keyspaces vs Cosmos Cassandra API?**
AWS **Keyspaces** (CQL) vs Cosmos **Cassandra** API. GCP Bigtable is **not** CQL Cassandra even if people wave “wide-column.” Partition/row-key design still rules. Do not pick CQL because a blog said “Cassandra is web scale” when your access pattern is SQL joins.

**29. Why not Cosmos APIs as “multi-model one bill”?**
The APIs are **different products** with one RU bill. Graph (Gremlin), Mongo, Cassandra, and Core SQL do not share indexes or query planners as a free lunch. AWS does not honestly offer “one multi-model engine”; pick Dynamo **or** DocumentDB **or** Neptune. GCP similarly splits Firestore / Bigtable / Spanner Graph.

**30. ElastiCache vs Azure Cache for Redis?**
**ElastiCache** Redis/Valkey vs **Azure Cache for Redis** (SKU **is** the HA story: Basic is not Multi-AZ). GCP **Memorystore** is the peer. Memcached exists on ElastiCache; do not invent it on Azure. Cache is not money SoR — even MemoryDB / Enterprise persistence is **durable cache**, not the ledger.

**31. MemoryDB vs Azure Cache Enterprise?**
**MemoryDB** is Redis-compatible with a durable multi-AZ transaction log. Azure Enterprise SKU / persistence is the nearest Azure sentence. Still **not** the leave-balance SoR. Use when you already decided Redis is the working set and you need failover without “oops AOF.”

**32. OpenSearch Service vs Azure AI Search?**
Lucene-shaped search: **OpenSearch Service** vs **Azure AI Search** (formerly Cognitive Search). GCP: Elastic on GCP or Vertex AI Search, not a perfect OpenSearch twin. kNN / RAG is OpenSearch kNN or Aurora `pgvector` vs AI Search vectors or Flexible PG + `pgvector`. Search is a **projection** of SoR — OpenSearch as inventory is an interview fail.

**33. Neptune vs Cosmos Gremlin?**
Property graph: **Neptune** (Gremlin/openCypher + SPARQL) vs Cosmos **Gremlin** API. GCP: Spanner Graph or Neo4j Aura on marketplace — no Neptune twin. Graph is not a reason to skip a relational SoR for leave balances.

---

## Lake & warehouse

**34. S3 vs Blob vs ADLS Gen2?**
Object lake: **S3** vs **Blob** / **ADLS Gen2** (hierarchical namespace for analytics). GCP **GCS** is the peer. Iceberg/Hudi/Delta on S3 vs Delta/Iceberg on ADLS. Files for PDFs on the app path are S3 or Blob; the lake is not the checkout SoR.

**35. Athena vs Synapse serverless / Fabric?**
SQL on files: **Athena** vs Synapse serverless SQL / Fabric. GCP **BigQuery** external tables / BigLake is the peer. **Checkout does not query Athena/Synapse.** Nightly/hourly export is the honest path. Scan tax (S3 list / ADLS scan) is a FinOps line, not a rounding error.

**36. Redshift vs Synapse dedicated / Fabric warehouse?**
MPP warehouse: **Redshift** vs **Synapse dedicated** or Fabric warehouse. GCP **BigQuery** is serverless warehouse (slots), not Redshift nodes. OLTP vs OLAP still applies: warehouse is a projection. Pick from **identity + data gravity**, not a blog TPC.

**37. Glue vs Azure Data Factory? Lake Formation vs Purview?**
ETL/ELT: **Glue** / EMR / dbt vs **Data Factory**, Synapse pipelines, Databricks. Catalog/governance: Glue Data Catalog + **Lake Formation** / DataZone vs **Purview** / Fabric OneLake catalog. GCP: Dataflow / Dataproc + Dataplex. **Catalog ≠ ledger.** Spark: EMR/Glue/Databricks-on-AWS vs Databricks/Synapse Spark/Fabric; GCP Dataproc.

**38. Why is “Athena on the submit path” an anti-pattern?**
You put an OLAP scan SLO on an OLTP user action. Same failure as Synapse serverless in the HTTP request or BigQuery DML as checkout. Use RDS/Aurora or Flexible/Azure SQL (or Cloud SQL) for the write; warehouse is downstream.

---

## Messaging

**39. MSK and Kinesis vs Event Hubs?**
Log/replay: **MSK** (Kafka) and **Kinesis** vs **Event Hubs** (Kafka protocol option). GCP **Pub/Sub** (and Managed Kafka) is the peer. Use when you need replay and consumer groups, not a REST resource per event. Event Hubs Capture / Firehose is how the lake is fed — not how the SoR commits.

**40. SQS vs Storage queues vs Service Bus?**
Work queue: **SQS** (standard/FIFO) vs **Storage queues** or **Service Bus** (sessions ≈ FIFO group). GCP Pub/Sub or Cloud Tasks is the usual peer. Outbox still applies; the queue is not the ledger. FIFO/session is a **grouping** story, not “exactly-once magic.”

**41. SNS vs Service Bus topics vs Event Grid?**
Fan-out: **SNS** vs Service Bus topics / **Event Grid**. Event routing/bus: **EventBridge** vs Event Grid + Event Hubs. GCP Eventarc / Pub/Sub is the peer. **EventBridge ≠ SoR.** Do not put business invariants only in a bus rule.

**42. How do you map CDC into the lake or bus?**
AWS **DMS** (incl. Serverless), Dynamo Streams. Azure **ADF**, SQL CDC, Cosmos change feed, or Debezium on Kafka (MSK or Event Hubs Kafka). GCP Datastream is the peer. Heterogeneous migrate: DMS + SCT vs Azure DMS / ADF vs GCP Database Migration Service. CDC is a projection pipeline, not dual-write HA.

**43. Step Functions vs Logic Apps / Durable Functions?**
Orchestration: **Step Functions** vs **Logic Apps**, **Durable Functions**, or Container Apps jobs. GCP Workflows is the peer. Human + long saga can be Step Functions callbacks or Logic Apps / Temporal you run. Do not encode the domain as a 400-state JSON machine; outbox + workers stay the default.

---

## Compute

**44. Lambda vs Azure Functions?**
Glue, webhooks, timers: **Lambda** vs **Azure Functions** (GCP Cloud Functions / Cloud Run). Not the ledger. Cold start, timeout, and **IAM of the function** are yours. Lambda per REST resource is a YAML distributed monolith; same smell as one Function app per HTTP verb.

**45. Why do Lambda/Functions kill RDS — and what is RDS Proxy?**
**Lambda/Functions × default pool = RDS death** (thousands of short connections). AWS **RDS Proxy** multiplexes to RDS/Aurora. Azure: Flexible Server **PgBouncer** / pooling options, Azure SQL connection constraints, Cosmos **gateway**. GCP: Auth Proxy / AlloyDB pooler. Or **do not** FaaS the writer — put the API on ECS/Container Apps with a sized pool.

**46. ECS/Fargate vs Azure Container Apps?**
Docker without a mesh tax: **ECS** (often Fargate) vs **Container Apps**. GCP **Cloud Run** is the peer. This is the default rung for a Java/Go leave API until a platform team can page Kubernetes. Windows/.NET gravity still pulls App Service / AKS Windows pools; Linux Spring/Go is happy on both.

**47. EKS vs AKS — when is Kubernetes mandatory?**
**EKS** vs **AKS** (GCP **GKE**) when a **platform team exists** to own node pools, upgrades, and NetworkPolicy. “EKS because AWS, AKS because Azure, no platform team” is buying a second job. GitOps (Flux/Argo) is the same on both. Pod identity is IRSA vs Workload Identity, not keys in Secrets.

**48. EC2 vs Azure VM vs the PaaS rungs?**
One VM: **EC2** + systemd vs **Azure VM** + systemd (GCP Compute Engine). Ops-light HTTP: Elastic Beanstalk / App Runner vs **App Service**. Batch: AWS Batch / ECS jobs vs Azure Batch / Container Apps jobs. Honest rung-1 is still a VM; do not skip to EKS for a single process.

**49. What is the leave-API compute map on each cloud?**
AWS: ECS Fargate or EKS; ALB; RDS/Aurora via PrivateLink; Secrets Manager; SQS worker; CloudWatch + OTel; Cognito or Entra for humans. Azure: Container Apps or AKS; App Gateway/Front Door; Flexible PG via Private Endpoint; Key Vault + Managed Identity; Service Bus worker; App Insights + OTel; Entra. Both: timeouts, outbox, no Lambda as the ledger, no dual-write.

---

## API & edge

**50. API Gateway vs APIM?**
Public HTTP API: **API Gateway** (REST/HTTP/WebSocket) vs **APIM**. JWT at the edge: Cognito/JWT authorizer vs Entra / validate-jwt policy. GCP **API Gateway** / Apigee is the peer. TLS, quota, and authn **shape** live here; **domain stays in Java/Go**. APIM business rules as the core is a gateway-as-monolith failure.

**51. ALB/NLB vs Application Gateway / Azure Load Balancer?**
L4/L7 inside the region: **NLB/ALB** vs **Load Balancer / Application Gateway**. Front Door is Azure’s global HTTP edge (see CloudFront). WAF: AWS WAF vs Azure WAF; DDoS: Shield Standard/Advanced vs DDoS Protection. GCP Cloud Load Balancing / Cloud Armor is the peer. Public ALB **to RDS** is a finding.

**52. CloudFront vs Azure Front Door?**
CDN/POP + TLS at the edge: **CloudFront** vs **Front Door** (prefer Front Door over classic Azure CDN). GCP Cloud CDN / Cloudflare remain peers in many RFPs. CSR origin is S3 vs Blob; SSR origin is ECS vs App Service/Container Apps **behind** the same CDN for hashed chunks. Cache-Control is still **yours** in CI.

**53. OAC vs anonymous Blob — why does it matter?**
**Origin Access Control** (CloudFront → S3) beats a public bucket. Front Door → Blob should use Microsoft-managed or your identity — no anonymous container “for convenience.” Public S3 static website as “the CDN” is theft, no WAF, and a weak HTTP/3 story.

**54. SPA fallback: where must it not apply?**
CloudFront custom error **403/404 → `/index.html`** only on the **app** behavior. Azure: Front Door rewrite / SWA navigation fallback. **Never** on `/api` — that serves SPA HTML as JSON. Invalidation is `/*` or `/index.html` vs purge `/` and `index.html`. Hashed assets immutable; `index.html` no-cache.

**55. Signed CloudFront URLs vs Blob SAS?**
Paid/private downloads: CloudFront **signed URL/cookie** vs Blob **SAS** (short TTL, least privilege). A 1-year SAS in JavaScript is a permanent leak. Do not put a JWT on the query string (CDN logs + DPDP). GCP signed GCS URLs are the peer.

**56. AppSync vs Azure GraphQL?**
Managed GraphQL: **AppSync** is the AWS-shaped product. Azure is APIM + **your** GraphQL (or API Center) — there is no AppSync twin. BFF still shapes screens; the gateway is not the domain. WebSocket/SSE: ALB/CloudFront behaviors vs App Gateway/Front Door idle timeouts — **not** Lambda long-poll as a socket server.

---

## Frontend hosts & auth

**57. Amplify Hosting vs Azure Static Web Apps?**
Git-linked SPA/SSR: **Amplify Hosting** vs **Azure Static Web Apps (SWA)**. Amplify wins on AWS account + Amplify SSR + branches; watch build minutes and env secrets. SWA wins on Entra-gated previews and Azure gravity; watch API glue vs a real BFF and region. **Firebase Hosting** is neither and still valid for SPA. Do not run Amplify **and** Front Door **and** Vercel as three cache brains.

**58. CSR origin map: S3+CloudFront vs Blob+Front Door?**
Hashed `dist/` to **S3** (block public; OAI/OAC) vs **Blob** + Front Door. HTML no-cache, assets immutable, SPA fallback not on `/api`. Preview: Amplify PR or extra CloudFront path vs **SWA PR environments**. Rendering strategy still comes from the frontend notebook — cloud is estate gravity, not CSR vs SSR.

**59. SSR/BFF origin: Amplify vs App Service vs containers?**
Node/Java SSR: **ECS/Fargate**, EKS, Beanstalk, App Runner vs **App Service**, **Container Apps**, AKS. Git-push SSR: Amplify Hosting (Next) vs SWA + API or App Service from GitHub. Edge rewrite: CloudFront Functions / **Lambda@Edge** vs Front Door rules engine. Lambda@Edge as a BFF: cold start, region, cost, 1 MB limits — do not.

**60. Cognito vs Entra External ID / B2C?**
Customer CIAM: **Cognito** user pools + Hosted UI vs **Entra External ID / B2C**. Workforce: Cognito **can**, but **Entra even on AWS** is common; Azure is Entra ID. GCP Identity Platform / Firebase Auth is the peer. **B2C ≠ workforce tenant.** Cognito quotas/email/Hosted UI CSS are product; Entra Conditional Access is policy. Frontend: **no JWT in localStorage**, no token on the query string.

**61. ALB OIDC vs Easy Auth — can you stack them with a React JWT?**
ALB OIDC authenticate vs App Proxy / **Easy Auth** on App Service. Token to API: BFF cookie default; check Cognito JWT `aud` vs Entra JWT and **OBO** for Graph/SQL. **Easy Auth + also JWT in React** is two session stories. Cookie to BFF: `Secure` `HttpOnly` `SameSite`; CloudFront/Front Door must **forward** the cookie or a cache key that ignores cookies will serve the wrong user HTML.

**62. CloudFront response headers vs Front Door rules?**
CSP, `nosniff`, HSTS, CORS for fonts: CloudFront **response headers policy** vs Front Door rules. Compress gzip/brotli at the edge; do not gzip woff2. WAF rules must not break SPA POST / auth. Sticky HTML personalization is cached at **BFF/cookie**, not a 1-year CloudFront HTML for “Welcome, Digoman.”

---

## Observe & IaC

**63. CloudWatch vs Azure Monitor / Application Insights?**
Metrics/logs: **CloudWatch** vs **Azure Monitor** + Log Analytics. APM/traces: X-Ray or OTel → AMP/X-Ray vs **Application Insights** + OTel. GCP Cloud Monitoring / Cloud Trace is the peer. Prefer **OpenTelemetry** in the app so you are not married to either SDK. CloudWatch **and** App Insights **and** Datadog with no owner is three bills and no SLO.

**64. RUM and synthetics for the SPA?**
CloudWatch RUM (or Datadog/Sentry you already buy) vs **Application Insights** JS. Synthetics: CloudWatch Synthetics vs App Insights availability tests. Core Web Vitals are owned by the **template**, not the CDN. App Insights + three other RUMs is INP death. Source maps go to Sentry/Datadog — **not** a public S3/Blob.

**65. Feature flags: AppConfig vs Azure App Configuration?**
AWS **AppConfig** (and SSM) vs **Azure App Configuration** + Feature Manager. Same laws: flags are not a second SoR; kill switches need an owner. Do not hide residency or authz in a flag that defaults open.

**66. CDK vs Bicep?**
AWS **CloudFormation** / **CDK** vs Azure **Bicep** / ARM. **Terraform** and Pulumi are honest on **both** (and GCP). Pipeline: CodePipeline or GitHub Actions **OIDC** vs Azure DevOps or GitHub Actions OIDC. Registry: **ECR** vs **ACR** (GCP Artifact Registry). OIDC → IAM role / federated credential; no `AKIA` in Jenkins. Accounts-as-env vs subscriptions-as-env.

**67. Why OIDC from GitHub instead of long-lived cloud keys?**
GitHub Actions assumes an IAM role or Azure federated credential for the length of the job. Same pattern on GCP Workload Identity Federation. Long-lived access keys in CI are how prod leaks. Env promotion is still a **human** gate; OIDC is identity, not “push is prod.”

---

## India, cost, HA/DR

**68. What are the India regions you should name?**
AWS: **`ap-south-1` Mumbai**, **`ap-south-2` Hyderabad**. Azure: **Central India**, **South India**, **West India**. GCP’s India regions (e.g. `asia-south1` Mumbai) are the peer when the RFP is GCP. **Pair the DR region in writing.** DPDP/RBI: name snapshot subprocessors; S3 CRR / Blob GRS is a **legal** sentence, not a checkbox.

**69. Multi-AZ vs region DR?**
**Multi-AZ / zone-redundant SKU = HA in one region**, not region loss. Aurora Global / SQL failover groups = usually **async** second region, not zero RPO. Dynamo Global Tables / Cosmos multi-region = item store with an honest consistency (LWW vs session vs strong **and pay RU+RTT**). Geo-redundant backup means you can **restore** elsewhere — not automatic cutover you never drilled. “Multi-AZ in Mumbai is enough for RBI if the paper says region” is a fail.

**70. Why is NAT Gateway a FinOps Sev-2?**
NAT Gateway **GB processed** (AWS and Azure NAT / Firewall SNAT) dwarfs idle compute on chatty microservices. PrivateLink / Private Endpoint to PaaS avoids NAT where you can. Data egress API → internet vs **cloud-to-cloud** is how multi-cloud bills appear. Reserved Instances / Savings Plans / Azure Reservations are for **steady** SoR compute, not random Lambda.

**71. What unit cost should you quote, not “RDS is expensive”?**
**$ / 1k checkouts** (or per leave submit), including NAT, backup PITR window, provisioned Cosmos RU idle, Aurora volume that never shrinks, Athena/Synapse scan. People are still the largest line if you “save RDS” onto Kubernetes Postgres with no DBA — same on AKS. Idle Multi-AZ **dev** should be stopped/snapshotted.

**72. Encryption and residency — KMS/Key Vault in one sentence?**
In transit: force TLS to the engine. At rest: KMS CMK vs Key Vault; separate prod keys. In use: Nitro Enclaves / Azure Confidential is a **programme**, not a leave-balance checkbox. Residency is **region**; GRS/CRR copies are another geography you must name.

**73. Why never dual-write RDS and Cosmos (or Aurora and Cosmos) for HA?**
Two engines, **two consistency models**, two failure domains — you invented a distributed transaction you cannot test. Same crime as “Aurora in AWS and Cosmos in Azure for HA” or dual-writing AWS and Azure for the **same fact**. Pick **one** system of record; projections (search, cache, warehouse, bus) are downstream. Multi-cloud DR as a logical replica/backup copy is a **programme** with worse RPO/RTO than intra-cloud Multi-AZ — not a checkbox.

**74. Document the HA vs DR SKU words so you cannot bluff.**
Multi-AZ / zone redundant ≠ region loss. Aurora Global / failover group ≠ zero RTT. Dynamo Global Tables ≠ SQL invariants. Cosmos session ≠ strong. GRS backup ≠ failover drill. If the interviewer says “we are multi-region,” answer with **RPO, RTO, consistency, and the last restore date**.

**75. What is the honest HR-leave SoR on each cloud?**
AWS: Aurora PostgreSQL or RDS PG, PrivateLink, IAM auth or Secrets Manager, S3 for PDFs, ElastiCache if measured, OpenSearch only if a search SLO, Athena/Glue for finance export **not** on submit. Azure: Flexible PostgreSQL or Azure SQL (skill), Private Endpoint, Managed Identity, Blob, Azure Cache if measured, AI Search if needed, Synapse/Fabric nightly. Rejected on both: Cosmos/Dynamo “because cloud-native,” public endpoint, ElastiCache as balance SoR.

**76. Name five anti-patterns that fail interviews on both clouds.**
Dual-write RDS+Cosmos for HA; DocumentDB = Atlas; OpenSearch as inventory; Athena on checkout; one KMS key for all envs; GRS as “we failed over”; Lake Formation/Purview as SoR; Lambda per REST resource; Step Functions as the domain; access keys in Git; public ALB to RDS; APIM as core; three APM products with no owner. Frontend twins: CloudFront 404→index on `/api`; SAS with 1-year expiry; Lambda@Edge as BFF.

**77. Mesh, Windows, and “zero trust-ish” — map without collecting logos.**
Service mesh: App Mesh is often replaced by **Istio/Linkerd** on EKS; Istio on AKS is the honest Azure peer (OSM is history). Zero-trust-ish: Verified Access / mesh mTLS vs Entra + Private Link + mesh. Windows/.NET → App Service / AKS Windows; Linux Spring/Go → both. Do not copy a Build slide into a six-person squad.

**78. Hybrid migrate: DMS vs Azure Migrate / Data Box?**
Heterogeneous: **DMS** + SCT vs **Azure DMS** / ADF. On-prem bulk: Snowball / DataSync vs Azure Migrate / Data Box. Backup vault: AWS Backup vs Azure Backup / Recovery Services. GCP Transfer / Database Migration Service is the peer. Homogeneous PG→PG is often native replica, not a logo.

**79. Timestream vs Azure Data Explorer — when do they matter?**
Time series: **Timestream** (or PG+Timescale on RDS) vs **Azure Data Explorer (Kusto)** / Metrics. GCP: Bigtable or Timescale on Cloud SQL. QLDB vs SQL ledger are **niche** — not a reason to skip a real SoR. Most leave systems never need either.

**80. Give the 90-second estate answer (AWS ↔ Azure).**
Freeze SoR as Postgres-shaped on the estate you already page — RDS/Aurora or Flexible/Azure SQL (GCP: Cloud SQL/AlloyDB). PrivateLink or Private Endpoint. IAM / Managed Identity, not keys in Git. Map jobs: compute, queue, identity, secrets, API, observe — Fargate/Container Apps until a platform team can page EKS/AKS. CSR: S3+CloudFront or Blob+Front Door; HTML no-cache; SPA fallback not on `/api`. Auth: Entra or Cognito via BFF cookies. Warehouse and search are projections. Multi-AZ is HA; region is DR. Dynamo/Cosmos only with known keys and an honest consistency. **I will not dual-write RDS and Cosmos, or AWS and Azure, for the same fact.**

---

**Counts:** **80** questions, **80** answers (numbered **1–80**). Format: `**N. Question?**` + 2–6 sentence answers. Sources: dbnotes/36, backend/35, frontend/39 (GCP named as peer where it is the twin).
