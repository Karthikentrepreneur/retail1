from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ProductAttribute(BaseModel):
    key: str
    value: Any


class ProductCreate(BaseModel):
    sku: str
    barcode: str | None = None
    name: str
    description: str | None = None
    hsn_code: str | None = None
    tax_group: str
    base_unit: str
    attrs: dict[str, Any] = Field(default_factory=dict)


class ProductVariantCreate(BaseModel):
    variant_code: str
    attributes: dict[str, Any]
    sku: str | None = None
    barcode: str | None = None
    price_mrp: float | None = None
    price_sale: float | None = None
    price_purchase: float | None = None
    min_stock: float | None = None
    max_stock: float | None = None


class ProductOut(ProductCreate):
    id: str
    tenant_id: str


class ProductVariantOut(ProductVariantCreate):
    id: str
    product_id: str
    tenant_id: str


class PriceListCreate(BaseModel):
    name: str
    currency_code: str = "INR"
    type: str
    is_default: bool = False


class PriceListItemCreate(BaseModel):
    product_variant_id: str
    price: float
    effective_from: str
    effective_to: str | None = None


class PriceListOut(PriceListCreate):
    id: str
    tenant_id: str

