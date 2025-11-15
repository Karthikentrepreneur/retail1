from __future__ import annotations

import uuid

from fastapi import APIRouter, Request

from app.schemas import reports as report_schema
from app.services import reports as report_service

router = APIRouter()


@router.post("/reports/run", response_model=report_schema.ReportResponse)
async def run_report(request: Request, payload: report_schema.ReportRequest):
    tenant_id = uuid.UUID(request.state.tenant_id)
    return await report_service.run_report(tenant_id, payload)


@router.get("/reports/{report_key}", response_model=report_schema.SnapshotResponse)
async def get_report_snapshot(request: Request, report_key: str):
    tenant_id = uuid.UUID(request.state.tenant_id)
    return await report_service.get_snapshot(tenant_id, report_key)
