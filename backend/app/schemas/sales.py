from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class SaleItem(BaseModel):
    product_variant_id: str
    product_batch_id: str | None = None
    quantity: float
    unit_price: float
    discount_amount: float = 0
    tax_group: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class SaleCreate(BaseModel):
    store_id: str
    warehouse_id: str | None = None
    customer_id: str | None = None
    items: list[SaleItem]
    payments: list[dict[str, Any]]
    discounts: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    source: str = "online"
    offline_temp_id: str | None = None


class SaleOut(BaseModel):
    id: str
    invoice_number: str | None
    store_id: str
    subtotal: float
    tax_total: float
    grand_total: float
    status: str


class SaleReturnRequest(BaseModel):
    sale_id: str
    items: list[SaleItem]
    reason: str | None = None
