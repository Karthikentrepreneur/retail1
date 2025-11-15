from __future__ import annotations

import uuid

from sqlalchemy import select

from app.db.session import get_async_session
from app.models import Sale, SaleItem
from app.schemas import sales as sales_schema


async def create_sale(tenant_id: uuid.UUID, payload: sales_schema.SaleCreate) -> Sale:
    async with get_async_session(str(tenant_id)) as session:
        subtotal = sum(item.quantity * item.unit_price for item in payload.items)
        tax_total = subtotal * 0.18  # placeholder
        grand_total = subtotal + tax_total
        sale = Sale(
            tenant_id=tenant_id,
            store_id=uuid.UUID(payload.store_id),
            warehouse_id=uuid.UUID(payload.warehouse_id) if payload.warehouse_id else None,
            customer_id=uuid.UUID(payload.customer_id) if payload.customer_id else None,
            subtotal=subtotal,
            discount_total=0,
            tax_total=tax_total,
            grand_total=grand_total,
            status="pending_payment",
            source=payload.source,
            offline_temp_id=payload.offline_temp_id,
        )
        session.add(sale)
        await session.flush()
        for item in payload.items:
            sale_item = SaleItem(
                sale_id=sale.id,
                product_variant_id=uuid.UUID(item.product_variant_id),
                product_batch_id=uuid.UUID(item.product_batch_id) if item.product_batch_id else None,
                quantity=item.quantity,
                unit_price=item.unit_price,
                discount_amount=item.discount_amount,
                tax_group=item.tax_group,
                tax_amount=item.unit_price * item.quantity * 0.18,
                line_total=item.unit_price * item.quantity,
                attributes=item.metadata,
            )
            session.add(sale_item)
        await session.flush()
        return sale


async def get_sale(tenant_id: uuid.UUID, sale_id: uuid.UUID) -> Sale | None:
    async with get_async_session(str(tenant_id)) as session:
        stmt = select(Sale).where(Sale.id == sale_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
