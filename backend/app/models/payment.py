from __future__ import annotations

import uuid

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="SET NULL"), nullable=True)
    sale_id = Column(UUID(as_uuid=True), ForeignKey("sales.id", ondelete="SET NULL"), nullable=True)
    supplier_invoice_id = Column(UUID(as_uuid=True), ForeignKey("supplier_invoices.id", ondelete="SET NULL"), nullable=True)
    method = Column(String, nullable=False)
    pg_provider = Column(String, nullable=True)
    pg_reference = Column(String, nullable=True)
    amount = Column(Numeric(14, 2), nullable=False)
    fees = Column(Numeric(12, 2), nullable=False, default=0)
    currency_code = Column(String(3), nullable=False, default="INR")
    status = Column(String, nullable=False, default="initiated")
    settled_at = Column(DateTime(timezone=True), nullable=True)
    idempotency_key = Column(String, nullable=True)
    metadata = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("tenant_id", "idempotency_key", name="uniq_payment_idem"),)
