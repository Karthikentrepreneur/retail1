from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PGOrderRequest(BaseModel):
    sale_id: str
    amount: float
    method: str = "upi"
    metadata: dict[str, Any] = Field(default_factory=dict)


class PGOrderResponse(BaseModel):
    order_id: str
    payment_intent: dict[str, Any]
    qr_code: str | None = None


class PaymentWebhook(BaseModel):
    provider: str
    payload: dict[str, Any]
    signature: str
    idempotency_key: str


class RefundRequest(BaseModel):
    payment_id: str
    amount: float
    reason: str | None = None
