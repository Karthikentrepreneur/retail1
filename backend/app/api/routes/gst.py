from __future__ import annotations

import uuid

from fastapi import APIRouter, Request

from app.schemas import gst as gst_schema
from app.services import gst as gst_service

router = APIRouter()


@router.post("/gst/einvoice", response_model=gst_schema.GSTInvoiceResponse)
async def create_einvoice(request: Request, payload: gst_schema.GSTInvoiceRequest):
    tenant_id = uuid.UUID(request.state.tenant_id)
    doc = await gst_service.generate_einvoice(tenant_id, payload)
    return gst_schema.GSTInvoiceResponse(status=doc.status, irn=doc.irn, ack_no=doc.ack_no, qr_data=doc.qr_data)


@router.get("/gst/returns/export", response_model=gst_schema.GSTExportResponse)
async def export_returns(request: Request, period: str, store_id: uuid.UUID | None = None):
    tenant_id = uuid.UUID(request.state.tenant_id)
    download_url = await gst_service.export_gst(tenant_id, gst_schema.GSTExportRequest(period=period, store_id=str(store_id) if store_id else None))
    return gst_schema.GSTExportResponse(download_url=download_url, generated_at="now")


@router.post("/gst/ewaybill", response_model=gst_schema.GSTInvoiceResponse)
async def create_ewaybill(request: Request, payload: gst_schema.EWayBillRequest):
    tenant_id = uuid.UUID(request.state.tenant_id)
    doc = await gst_service.request_ewaybill(tenant_id, payload)
    return gst_schema.GSTInvoiceResponse(status=doc.status, irn=doc.irn, ack_no=doc.ack_no, qr_data=doc.qr_data)
