from __future__ import annotations

import uuid

from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    plan_code = Column(String, nullable=False)
    vertical = Column(String, nullable=False)
    settings = Column(JSON, nullable=False, default=dict)
    data_retention_years = Column(String, nullable=False, default="8")
    legal_hold = Column(Boolean, nullable=False, default=False)
    currency_code = Column(String(3), nullable=False, default="INR")
    country_code = Column(String(2), nullable=False, default="IN")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Store(Base):
    __tablename__ = "stores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    gstin = Column(String, nullable=True)
    timezone = Column(String, nullable=False, default="Asia/Kolkata")
    currency_code = Column(String(3), nullable=False, default="INR")
    address = Column(JSON, nullable=True)
    is_primary = Column(Boolean, nullable=False, default=False)
    status = Column(String, nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class FeatureFlag(Base):
    __tablename__ = "feature_flags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    flag_key = Column(String, nullable=False)
    enabled = Column(Boolean, nullable=False, default=False)
    rollout = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
