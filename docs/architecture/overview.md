# POS SaaS Architecture Overview

## Vision and Tenets
- **Multi-tenant retail POS** for Indian SMBs with extensibility for new countries and currencies.
- **Cloud-native**: GCP (Cloud Run, Cloud SQL, MemoryStore, Pub/Sub, Cloud Storage).
- **Security-first**: tenant isolation via Postgres RLS, scoped JWTs, auditable actions.
- **Offline-capable** Android POS with conflict-aware sync.
- **Modular vertical logic** pluggable by feature flags and pricing plans.

## Architecture Summary
### Logical View
1. **Presentation**
   - **Web POS & Admin** (Next.js + Tailwind) as PWA for desktops/tablets.
   - **Mobile POS** (React Native + SQLite) with offline support.
2. **API Layer**
   - **FastAPI services** exposed via `/api` gateway.
   - Modules: auth, tenancy, catalog, inventory, sales, payments, GST, reports, sync.
3. **Domain Services**
   - Service layer orchestrating business rules, caching, async workflows.
   - Vertical-specific adapters implemented via plug-in registry pattern.
4. **Data & Integration**
   - **PostgreSQL (Cloud SQL)** with row-level security per tenant.
   - **Redis (MemoryStore)** for cache, rate limiting, distributed locks.
   - **Pub/Sub + Cloud Tasks** for async jobs (GST filings, settlements, sync replay).
   - **Cloud Storage** for documents (invoices, reports).
   - **Third-party**: Payment Gateway (Razorpay), GSP APIs (e-invoice/ewaybill), OTP SMS.
5. **Observability & Ops**
   - Cloud Logging, Cloud Monitoring dashboards and alerts.
   - OpenTelemetry traces from backend and mobile sync workers.

### Physical / Deployment View
- **Cloud Run services**:
  - `pos-api`: FastAPI monolith with modular routers.
  - `gst-worker`: async worker for GST/e-waybill (Cloud Run Jobs triggered by Pub/Sub).
  - `sync-worker`: handles offline sync reconciliation.
- **Cloud SQL (Postgres)** with private IP, high availability.
- **Redis (MemoryStore)** inside VPC for cache + Celery/async tasks.
- **Pub/Sub topics**: `gst-requests`, `payment-webhooks`, `sync-events`, `audit-log`.
- **Cloud Tasks queues** for scheduled retries (GST, settlements, sync).
- **Cloud Storage buckets**: `pos-docs`, `pos-exports`, `pos-backups`.
- **Cloud Armor** for WAF, rate limiting, IP allowlist for admin endpoints.
- **Secrets** in Secret Manager; Cloud KMS for envelope encryption.

### Deployment Pipeline
1. GitHub Actions per repo: lint → tests → build container → Trivy scan → deploy to Cloud Run via deploy step (staging auto, prod manual).
2. Terraform manages infrastructure per environment (dev/staging/prod) with separate workspaces/projects.
3. Database migrations via Alembic executed during deploy.
4. Feature flags managed via config service table and exposed via LaunchDarkly-like module (internal implementation stored per tenant plan settings).

### Key Design Decisions
- **Row-Level Security** chosen for multi-tenancy to balance isolation and shared schema manageability; all queries include tenant scope, SQLAlchemy session enforces `tenant_id` filter via context.
- **Pub/Sub + Cloud Tasks** selected over Celery to leverage managed GCP services and ensure at-least-once delivery with controlled retries.
- **Domain modules** follow clean architecture: routers → services → repositories → DB. Vertical-specific logic is injected via `feature_registry` (strategy pattern) keyed by tenant vertical.
- **Offline sync** uses operation logs persisted locally and reconciled via deterministic merge rules (server authoritative for stock, taxes, numbering). Conflicts generate review tasks surfaced via admin UI.
- **Accounting-lite** implemented as categorized cashbook with double-entry ledger for integrations/export compatibility while keeping scope manageable.
- **Printing** handled using server-rendered PDFs (WeasyPrint) for A4 invoices and ESC/POS templates for 80mm receipts; triggered via webhooks from POS clients.

### Security & Compliance Highlights
- JWT with tenant+store scopes, short-lived (15 min) access tokens, refresh tokens stored server-side with rotation.
- API keys per device (POS terminal/mobile) stored hashed; offline devices use signed commands.
- Postgres: row-level policies, partitioning for audit logs, column-level encryption for sensitive PII (phone, GSTIN) using pgcrypto.
- Audit log stream to BigQuery for retention beyond 8 years.
- Configurable data retention with purge jobs respecting legal hold flag.

### Observability
- Structured logging via OpenTelemetry.
- Metrics: request latency, cache hit ratio, sync queue depth, GST error rates.
- Traces propagate via W3C trace context; spans for DB queries, external API calls.

### Scalability & Performance
- POS search served by Postgres trigram indexes + Redis cache; <150ms requirement met via preloaded hot data and read replicas if needed.
- Inventory writes batched via transactions; FIFO valuation computed via materialized view refresh.
- Web sockets (Cloud Run WebSocket support) or SSE for payment status updates.

### Disaster Recovery & Backups
- Cloud SQL PITR enabled; daily exports to Cloud Storage.
- Infrastructure code in Terraform, enabling region failover (secondary region warm standby).
- Offline mobile ensures business continuity during outages.

