from __future__ import annotations

import uuid

from sqlalchemy import select

from app.db.session import get_async_session
from app.models import Product, ProductVariant
from app.schemas import product as product_schema


async def create_product(tenant_id: uuid.UUID, payload: product_schema.ProductCreate) -> Product:
    async with get_async_session(str(tenant_id)) as session:
        product = Product(
            tenant_id=tenant_id,
            sku=payload.sku,
            barcode=payload.barcode,
            name=payload.name,
            description=payload.description,
            hsn_code=payload.hsn_code,
            tax_group=payload.tax_group,
            base_unit=payload.base_unit,
            attrs=payload.attrs,
        )
        session.add(product)
        await session.flush()
        return product


async def create_variant(tenant_id: uuid.UUID, product_id: uuid.UUID, payload: product_schema.ProductVariantCreate) -> ProductVariant:
    async with get_async_session(str(tenant_id)) as session:
        variant = ProductVariant(
            tenant_id=tenant_id,
            product_id=product_id,
            variant_code=payload.variant_code,
            attributes=payload.attributes,
            sku=payload.sku,
            barcode=payload.barcode,
            price_mrp=payload.price_mrp,
            price_sale=payload.price_sale,
            price_purchase=payload.price_purchase,
            min_stock=payload.min_stock,
            max_stock=payload.max_stock,
        )
        session.add(variant)
        await session.flush()
        return variant


async def list_products(tenant_id: uuid.UUID) -> list[Product]:
    async with get_async_session(str(tenant_id)) as session:
        stmt = select(Product).where(Product.tenant_id == tenant_id)
        result = await session.execute(stmt)
        return list(result.scalars())
