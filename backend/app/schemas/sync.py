from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SyncPayload(BaseModel):
    device_id: str
    last_sync_token: str | None = None
    operations: list[dict[str, Any]] = Field(default_factory=list)


class SyncResponse(BaseModel):
    next_sync_token: str
    operations: list[dict[str, Any]]
    has_more: bool = False


class SyncAckRequest(BaseModel):
    device_id: str
    operation_ids: list[str]
    status: str
