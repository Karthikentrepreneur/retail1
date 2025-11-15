from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException, Request, status

from app.schemas import payments as payment_schema
from app.services import payments as payment_service

router = APIRouter()


@router.post("/pg/order", response_model=payment_schema.PGOrderResponse)
async def create_pg_order(request: Request, payload: payment_schema.PGOrderRequest):
    tenant_id = uuid.UUID(request.state.tenant_id)
    return await payment_service.create_pg_order(tenant_id, payload)


@router.post("/pg/webhook")
async def pg_webhook(request: Request, payload: payment_schema.PaymentWebhook):
    tenant_id = uuid.UUID(request.state.tenant_id)
    await payment_service.handle_webhook(tenant_id, payload)
    return {"status": "accepted"}


@router.post("/refunds")
async def refund(request: Request, payload: payment_schema.RefundRequest):
    tenant_id = uuid.UUID(request.state.tenant_id)
    try:
        payment = await payment_service.issue_refund(tenant_id, payload)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return {"id": str(payment.id), "status": payment.status}
