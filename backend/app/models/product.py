from __future__ import annotations

import uuid

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    sku = Column(String, nullable=False)
    barcode = Column(String, nullable=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    hsn_code = Column(String, nullable=True)
    tax_group = Column(String, nullable=False)
    base_unit = Column(String, nullable=False)
    attrs = Column(JSON, nullable=False, default=dict)
    is_active = Column(String, nullable=False, default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("tenant_id", "sku", name="uniq_product_sku"),
        UniqueConstraint("tenant_id", "barcode", name="uniq_product_barcode"),
    )


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    variant_code = Column(String, nullable=False)
    attributes = Column(JSON, nullable=False, default=dict)
    sku = Column(String, nullable=True)
    barcode = Column(String, nullable=True)
    price_mrp = Column(Numeric(12, 2), nullable=True)
    price_sale = Column(Numeric(12, 2), nullable=True)
    price_purchase = Column(Numeric(12, 2), nullable=True)
    min_stock = Column(Numeric(12, 3), nullable=True)
    max_stock = Column(Numeric(12, 3), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
