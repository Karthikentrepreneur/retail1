from __future__ import annotations

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import event

from app.core.config import settings


ASYNC_ENGINE = create_async_engine(settings.database_url, pool_size=10, max_overflow=20, pool_pre_ping=True)
ASYNC_SESSION_FACTORY = async_sessionmaker(bind=ASYNC_ENGINE, class_=AsyncSession, expire_on_commit=False)

SYNC_ENGINE = create_async_engine(settings.sync_database_url.replace("asyncpg", "psycopg"), pool_size=5, max_overflow=10)
SYNC_SESSION_FACTORY = sessionmaker(bind=SYNC_ENGINE.sync_engine, autocommit=False, autoflush=False)


@asynccontextmanager
async def get_async_session(tenant_id: str | None = None):
    async with ASYNC_SESSION_FACTORY() as session:
        if tenant_id:
            await session.execute(f"SELECT set_config('app.current_tenant', '{tenant_id}', true)")
        try:
            yield session
        finally:
            await session.execute("SELECT set_config('app.current_tenant', '', true)")


@asynccontextmanager
def get_sync_session(tenant_id: str | None = None):
    with SYNC_SESSION_FACTORY() as session:  # type: ignore[arg-type]
        if tenant_id:
            session.execute("SELECT set_config('app.current_tenant', :tenant, true)", {"tenant": tenant_id})
        try:
            yield session
        finally:
            session.execute("SELECT set_config('app.current_tenant', '', true)")


@event.listens_for(ASYNC_SESSION_FACTORY, "after_begin")
def enforce_rls(session: AsyncSession, transaction, connection):  # type: ignore[override]
    tenant_id = getattr(session.info.get("context"), "tenant_id", None)
    if tenant_id:
        connection.exec_driver_sql("SELECT set_config('app.current_tenant', %s, true)", (tenant_id,))

