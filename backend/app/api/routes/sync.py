from __future__ import annotations

import uuid

from fastapi import APIRouter, Request

from app.schemas import sync as sync_schema
from app.services import sync as sync_service

router = APIRouter()


@router.post("/sync/push", response_model=sync_schema.SyncResponse)
async def push_sync(request: Request, payload: sync_schema.SyncPayload):
    tenant_id = uuid.UUID(request.state.tenant_id)
    return await sync_service.push_operations(tenant_id, payload)


@router.get("/sync/pull", response_model=sync_schema.SyncResponse)
async def pull_sync(request: Request, device_id: uuid.UUID, last_sync_token: str | None = None):
    tenant_id = uuid.UUID(request.state.tenant_id)
    return await sync_service.pull_operations(tenant_id, device_id, last_sync_token)


@router.post("/sync/ack")
async def ack_sync(request: Request, payload: sync_schema.SyncAckRequest):
    tenant_id = uuid.UUID(request.state.tenant_id)
    await sync_service.ack_operations(tenant_id, payload)
    return {"status": "ok"}
