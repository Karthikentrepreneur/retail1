from __future__ import annotations

import uuid

from fastapi import APIRouter, Request

from app.schemas import product as product_schema
from app.services import product as product_service

router = APIRouter()


@router.post("/products", response_model=product_schema.ProductOut)
async def create_product(request: Request, payload: product_schema.ProductCreate):
    tenant_id = uuid.UUID(request.state.tenant_id)
    product = await product_service.create_product(tenant_id, payload)
    return product_schema.ProductOut(
        id=str(product.id),
        tenant_id=str(product.tenant_id),
        sku=product.sku,
        barcode=product.barcode,
        name=product.name,
        description=product.description,
        hsn_code=product.hsn_code,
        tax_group=product.tax_group,
        base_unit=product.base_unit,
        attrs=product.attrs,
    )


@router.get("/products", response_model=list[product_schema.ProductOut])
async def list_products(request: Request):
    tenant_id = uuid.UUID(request.state.tenant_id)
    products = await product_service.list_products(tenant_id)
    return [
        product_schema.ProductOut(
            id=str(prod.id),
            tenant_id=str(prod.tenant_id),
            sku=prod.sku,
            barcode=prod.barcode,
            name=prod.name,
            description=prod.description,
            hsn_code=prod.hsn_code,
            tax_group=prod.tax_group,
            base_unit=prod.base_unit,
            attrs=prod.attrs,
        )
        for prod in products
    ]


@router.post("/products/{product_id}/variants", response_model=product_schema.ProductVariantOut)
async def create_variant(request: Request, product_id: uuid.UUID, payload: product_schema.ProductVariantCreate):
    tenant_id = uuid.UUID(request.state.tenant_id)
    variant = await product_service.create_variant(tenant_id, product_id, payload)
    return product_schema.ProductVariantOut(
        id=str(variant.id),
        product_id=str(variant.product_id),
        tenant_id=str(variant.tenant_id),
        variant_code=variant.variant_code,
        attributes=variant.attributes,
        sku=variant.sku,
        barcode=variant.barcode,
        price_mrp=float(variant.price_mrp or 0),
        price_sale=float(variant.price_sale or 0),
        price_purchase=float(variant.price_purchase or 0),
        min_stock=float(variant.min_stock or 0),
        max_stock=float(variant.max_stock or 0),
    )
