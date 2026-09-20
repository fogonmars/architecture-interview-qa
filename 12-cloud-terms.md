# High-level terms — cloud (AWS · Azure · GCP)

Also: [index of all term guides](12-high-level-terms.md).

Cloud is a **job map**: same job, different product names. Steal the job, not the logo.

Sister: [DB 36](../dbnotes/36-aws-azure-data-platforms/README.md) · [BE 35](../backend/35-aws-azure-workloads/README.md) · [FE 39](../frontend/39-aws-azure-frontend/README.md) · [interview 04](04-aws-azure.md).

---

## How to talk in an interview

1. Name the **job** (run a container, store files, queue work, SQL SoR…).  
2. Say the **AWS name** and **Azure name** (GCP as peer).  
3. Say the **failure** (e.g. “S3 is not a ledger”).

---

## Compute — “where does my code run?”

| Job | Plain English | AWS | Azure | GCP |
|---|---|---|---|---|
| Virtual machine | You manage an OS | EC2 | Virtual Machines | Compute Engine |
| Container without full K8s | Run containers managed | ECS / Fargate | Container Apps / ACA | Cloud Run |
| Kubernetes | You operate a cluster API | EKS | AKS | GKE |
| Function / FaaS | Short event-driven code | Lambda | Functions | Cloud Functions |
| App platform | PaaS for web apps | Elastic Beanstalk / Amplify | App Service | App Engine |

**Bubble:** “Everything on Kubernetes.” **Practical:** start at VM/PaaS/containers; K8s when fleet/org needs it.

---

## Data — “where do bytes live?”

| Job | Plain English | AWS | Azure | GCP |
|---|---|---|---|---|
| Managed Postgres/MySQL | SQL SoR without babysitting disks | RDS / Aurora | Flexible Server / Azure SQL | Cloud SQL |
| Huge key-value | Known-key lookups at scale | DynamoDB | Cosmos DB | Bigtable / Firestore |
| Files / objects | PDFs, images, backups | S3 | Blob Storage | Cloud Storage |
| Warehouse | Analytics / OLAP | Redshift | Synapse | BigQuery |
| Search | Relevance index (projection) | OpenSearch | AI Search | Elastic on GCP / Vertex Search |
| Cache | Hot keys | ElastiCache (Redis) | Azure Cache for Redis | Memorystore |
| Queue | Work to do later | SQS | Storage Queues / Service Bus | Pub/Sub (or Cloud Tasks) |
| Log / stream | Replayable events | Kinesis / MSK | Event Hubs | Pub/Sub |

**Never:** object store or queue as the **only** money ledger.

---

## Network & security

| Job | Plain English | AWS | Azure |
|---|---|---|---|
| Private link to PaaS | Traffic stays on private network | PrivateLink | Private Endpoint |
| Identity for apps | No password in code | IAM roles | Entra managed identity |
| Secrets | Store keys | Secrets Manager / SSM | Key Vault |
| WAF / edge | Protect HTTP edge | CloudFront + WAF | Front Door + WAF |
| CDN for static | Cache JS/CSS worldwide | CloudFront | Front Door / CDN |

---

## Frontend hosting (short)

| Job | AWS | Azure |
|---|---|---|
| Static site + CDN | S3 + CloudFront | Blob + Front Door / SWA |
| Git-connected web | Amplify Hosting | Static Web Apps |
| Auth for SPA | Cognito | Entra External ID / B2C |

---

## AI cloud (short)

| Job | AWS | Azure | GCP |
|---|---|---|---|
| Hosted LLM API | Bedrock | Azure OpenAI | Vertex AI |
| Vector + search | OpenSearch kNN / pgvector | AI Search | Vertex AI Search |

Detail: [ai HIGH_LEVEL_TERMS](../ai/HIGH_LEVEL_TERMS.md) · [ai 15](../ai/15-cloud-platforms/README.md).

---

## Well-Architected ideas (any cloud)

| Idea | Plain English |
|---|---|
| **Least privilege** | App gets only the permissions it needs |
| **Multi-AZ** | Survive one data center failing |
| **Backup / PITR** | Point-in-time restore for databases |
| **Cost unit** | Know $/transaction or $/user — not “cloud is fine” |
| **One primary estate** | Don’t run active-active multi-cloud for fashion |

**Interview line:** “Same job, two names. I’d map SQL SoR, objects, queue, identity, then pick AWS or Azure from estate gravity.”
