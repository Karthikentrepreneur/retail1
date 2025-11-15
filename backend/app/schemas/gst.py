from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class GSTInvoiceRequest(BaseModel):
    sale_id: str
    force: bool = False


class GSTInvoiceResponse(BaseModel):
    status: str
    irn: str | None = None
    ack_no: str | None = None
    qr_data: str | None = None
    error: str | None = None


class GSTExportRequest(BaseModel):
    period: str
    store_id: str | None = None


class GSTExportResponse(BaseModel):
    download_url: str
    generated_at: str


class EWayBillRequest(BaseModel):
    sale_id: str
    vehicle_details: dict[str, Any]
