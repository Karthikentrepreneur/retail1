from __future__ import annotations

import uuid

from sqlalchemy import select

from app.db.session import get_async_session
from app.models import GSTDocument, Sale
from app.schemas import gst as gst_schema


async def generate_einvoice(tenant_id: uuid.UUID, payload: gst_schema.GSTInvoiceRequest) -> GSTDocument:
    async with get_async_session(str(tenant_id)) as session:
        doc = GSTDocument(
            tenant_id=tenant_id,
            sale_id=uuid.UUID(payload.sale_id),
            doc_type="einvoice",
            status="pending",
        )
        session.add(doc)
        await session.flush()
        # Publish to Pub/Sub in real implementation
        return doc


async def export_gst(tenant_id: uuid.UUID, payload: gst_schema.GSTExportRequest) -> str:
    # Generate export file and return signed URL
    return f"https://storage.googleapis.com/pos-exports/{tenant_id}/{payload.period}.json"


async def request_ewaybill(tenant_id: uuid.UUID, payload: gst_schema.EWayBillRequest) -> GSTDocument:
    async with get_async_session(str(tenant_id)) as session:
        doc = GSTDocument(
            tenant_id=tenant_id,
            sale_id=uuid.UUID(payload.sale_id),
            doc_type="ewaybill",
            status="pending",
            payload={"vehicle": payload.vehicle_details},
        )
        session.add(doc)
        await session.flush()
        return doc
