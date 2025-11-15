# Multi-tenancy Controls

- **Tenant Propagation**: Auth service embeds `tenant_id`, optional `store_id`, and roles in JWT. FastAPI dependency extracts payload and sets `request.state.tenant_id`. SQLAlchemy sessions execute `set_config('app.current_tenant', tenant_id, true)` per request.
- **Row Level Security**: All tenant-scoped tables enable RLS. Policies restrict `tenant_id = current_setting('app.current_tenant')::uuid`. Write operations use `WITH CHECK` to prevent cross-tenant inserts.
- **Plan & Feature Flags**: `feature_flags` table and `tenants.settings` JSON store plan entitlements. Service layer checks plan before invoking module features. Frontend obtains plan info via `/tenants/me`.
- **Device Isolation**: `devices` table tracks API keys hashed with bcrypt. Device tokens include tenant + store scopes ensuring offline sync operations remain tenant-bound.
- **Data Retention**: `data_purge_jobs` orchestrate deletions by tenant, respecting `legal_hold` flag. Purge executed via Cloud Run job with audit entry.
