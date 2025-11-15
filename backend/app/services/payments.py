from __future__ import annotations

import uuid

from sqlalchemy import select

from app.db.session import get_async_session
from app.models import Payment
from app.schemas import payments as payment_schema


async def create_pg_order(tenant_id: uuid.UUID, payload: payment_schema.PGOrderRequest) -> payment_schema.PGOrderResponse:
    order_id = uuid.uuid4().hex
    payment_intent = {"upi": {"link": f"upi://pay?pa=merchant@upi&am={payload.amount}&tn={payload.sale_id}"}}
    return payment_schema.PGOrderResponse(order_id=order_id, payment_intent=payment_intent, qr_code=f"{order_id}-qr")


async def record_payment(tenant_id: uuid.UUID, sale_id: uuid.UUID, method: str, amount: float, status: str, idempotency_key: str | None = None) -> Payment:
    async with get_async_session(str(tenant_id)) as session:
        payment = Payment(
            tenant_id=tenant_id,
            sale_id=sale_id,
            method=method,
            amount=amount,
            status=status,
            idempotency_key=idempotency_key,
        )
        session.add(payment)
        await session.flush()
        return payment


async def handle_webhook(tenant_id: uuid.UUID, payload: payment_schema.PaymentWebhook) -> None:
    # Validate signature, update payment record.
    pass


async def issue_refund(tenant_id: uuid.UUID, payload: payment_schema.RefundRequest) -> Payment:
    async with get_async_session(str(tenant_id)) as session:
        stmt = select(Payment).where(Payment.id == uuid.UUID(payload.payment_id))
        result = await session.execute(stmt)
        payment = result.scalar_one_or_none()
        if not payment:
            raise ValueError("Payment not found")
        payment.status = "refunded"
        await session.flush()
        return payment
