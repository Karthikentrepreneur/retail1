from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TenantCreate(BaseModel):
    name: str
    plan_code: str
    vertical: str
    currency_code: str = Field(default="INR", min_length=3, max_length=3)
    country_code: str = Field(default="IN", min_length=2, max_length=2)
    settings: dict[str, Any] = Field(default_factory=dict)


class TenantOut(BaseModel):
    id: str
    name: str
    plan_code: str
    vertical: str
    currency_code: str
    country_code: str


class StoreCreate(BaseModel):
    name: str
    gstin: str | None = None
    timezone: str = "Asia/Kolkata"
    currency_code: str = "INR"
    address: dict[str, Any] | None = None


class StoreOut(StoreCreate):
    id: str
    tenant_id: str
    status: str


class FeatureFlagUpdate(BaseModel):
    flag_key: str
    enabled: bool
    rollout: dict[str, Any] = Field(default_factory=dict)
