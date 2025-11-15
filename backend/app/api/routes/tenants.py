from __future__ import annotations

import uuid

from fastapi import APIRouter

from app.schemas import tenant as tenant_schema
from app.services import tenant as tenant_service

router = APIRouter()


@router.post("/tenants", response_model=tenant_schema.TenantOut)
async def create_tenant(payload: tenant_schema.TenantCreate):
    tenant = await tenant_service.create_tenant(payload)
    return tenant_schema.TenantOut(
        id=str(tenant.id),
        name=tenant.name,
        plan_code=tenant.plan_code,
        vertical=tenant.vertical,
        currency_code=tenant.currency_code,
        country_code=tenant.country_code,
    )


@router.get("/tenants", response_model=list[tenant_schema.TenantOut])
async def list_tenants():
    tenants = await tenant_service.list_tenants()
    return [
        tenant_schema.TenantOut(
            id=str(t.id),
            name=t.name,
            plan_code=t.plan_code,
            vertical=t.vertical,
            currency_code=t.currency_code,
            country_code=t.country_code,
        )
        for t in tenants
    ]


@router.post("/tenants/{tenant_id}/stores", response_model=tenant_schema.StoreOut)
async def create_store(tenant_id: uuid.UUID, payload: tenant_schema.StoreCreate):
    store = await tenant_service.create_store(tenant_id, payload)
    return tenant_schema.StoreOut(
        id=str(store.id),
        tenant_id=str(store.tenant_id),
        name=store.name,
        gstin=store.gstin,
        timezone=store.timezone,
        currency_code=store.currency_code,
        address=store.address,
        status=store.status,
    )


@router.put("/tenants/{tenant_id}/feature-flags", response_model=tenant_schema.FeatureFlagUpdate)
async def update_feature_flag(tenant_id: uuid.UUID, payload: tenant_schema.FeatureFlagUpdate):
    flag = await tenant_service.upsert_feature_flag(tenant_id, payload)
    return tenant_schema.FeatureFlagUpdate(flag_key=flag.flag_key, enabled=flag.enabled, rollout=flag.rollout)
