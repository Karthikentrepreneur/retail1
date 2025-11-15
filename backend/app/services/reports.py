from __future__ import annotations

import uuid

from app.schemas import reports as report_schema


async def run_report(tenant_id: uuid.UUID, payload: report_schema.ReportRequest) -> report_schema.ReportResponse:
    # Placeholder: use analytics warehouse or live query.
    data = [{"metric": "sales_total", "value": 0}]
    return report_schema.ReportResponse(data=data, generated_at="now")


async def get_snapshot(tenant_id: uuid.UUID, report_key: str) -> report_schema.SnapshotResponse:
    return report_schema.SnapshotResponse(download_url=f"https://storage.googleapis.com/pos-reports/{tenant_id}/{report_key}.pdf")
