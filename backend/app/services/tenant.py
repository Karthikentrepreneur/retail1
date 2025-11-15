from __future__ import annotations

import uuid

from sqlalchemy import select

from app.db.session import get_async_session
from app.models import FeatureFlag, Store, Tenant
from app.schemas import tenant as tenant_schema


async def create_tenant(payload: tenant_schema.TenantCreate) -> Tenant:
    async with get_async_session() as session:
        tenant = Tenant(
            name=payload.name,
            plan_code=payload.plan_code,
            vertical=payload.vertical,
            currency_code=payload.currency_code,
            country_code=payload.country_code,
            settings=payload.settings,
        )
        session.add(tenant)
        await session.flush()
        return tenant


async def list_tenants() -> list[Tenant]:
    async with get_async_session() as session:
        result = await session.execute(select(Tenant))
        return list(result.scalars())


async def create_store(tenant_id: uuid.UUID, payload: tenant_schema.StoreCreate) -> Store:
    async with get_async_session(str(tenant_id)) as session:
        store = Store(
            tenant_id=tenant_id,
            name=payload.name,
            gstin=payload.gstin,
            timezone=payload.timezone,
            currency_code=payload.currency_code,
            address=payload.address,
        )
        session.add(store)
        await session.flush()
        return store


async def upsert_feature_flag(tenant_id: uuid.UUID, payload: tenant_schema.FeatureFlagUpdate) -> FeatureFlag:
    async with get_async_session(str(tenant_id)) as session:
        stmt = select(FeatureFlag).where(FeatureFlag.tenant_id == tenant_id, FeatureFlag.flag_key == payload.flag_key)
        result = await session.execute(stmt)
        instance = result.scalar_one_or_none()
        if instance:
            instance.enabled = payload.enabled
            instance.rollout = payload.rollout
        else:
            instance = FeatureFlag(tenant_id=tenant_id, flag_key=payload.flag_key, enabled=payload.enabled, rollout=payload.rollout)
            session.add(instance)
        await session.flush()
        return instance
