from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ReportRequest(BaseModel):
    report_key: str
    filters: dict[str, Any]


class ReportResponse(BaseModel):
    data: list[dict[str, Any]]
    generated_at: str


class SnapshotResponse(BaseModel):
    download_url: str
    expires_at: str | None = None
