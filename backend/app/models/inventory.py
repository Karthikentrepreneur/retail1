from __future__ import annotations

import uuid

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    address = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InventoryBalance(Base):
    __tablename__ = "inventory_balances"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False)
    product_variant_id = Column(UUID(as_uuid=True), ForeignKey("product_variants.id", ondelete="CASCADE"), nullable=False)
    product_batch_id = Column(UUID(as_uuid=True), ForeignKey("product_batches.id", ondelete="SET NULL"), nullable=True)
    qty_on_hand = Column(Numeric(14, 3), nullable=False, default=0)
    qty_reserved = Column(Numeric(14, 3), nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class StockLedger(Base):
    __tablename__ = "stock_ledgers"

    id = Column(String, primary_key=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    warehouse_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id", ondelete="CASCADE"), nullable=False)
    product_variant_id = Column(UUID(as_uuid=True), ForeignKey("product_variants.id", ondelete="CASCADE"), nullable=False)
    product_batch_id = Column(UUID(as_uuid=True), ForeignKey("product_batches.id", ondelete="SET NULL"), nullable=True)
    txn_type = Column(String, nullable=False)
    txn_reference = Column(UUID(as_uuid=True), nullable=True)
    quantity = Column(Numeric(14, 3), nullable=False)
    direction = Column(String, nullable=False)
    running_balance = Column(Numeric(14, 3), nullable=False)
    txn_time = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
