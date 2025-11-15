from __future__ import annotations

import uuid

from sqlalchemy import select

from app.db.session import get_async_session
from app.models import InventoryBalance, StockLedger
from app.schemas import inventory as inventory_schema


async def get_stock_balances(tenant_id: uuid.UUID, warehouse_id: uuid.UUID | None = None) -> list[InventoryBalance]:
    async with get_async_session(str(tenant_id)) as session:
        stmt = select(InventoryBalance)
        if warehouse_id:
            stmt = stmt.where(InventoryBalance.warehouse_id == warehouse_id)
        result = await session.execute(stmt)
        return list(result.scalars())


async def record_transfer(tenant_id: uuid.UUID, payload: inventory_schema.InventoryTransferRequest) -> None:
    async with get_async_session(str(tenant_id)) as session:
        # Placeholder: implement stock deduction/addition and ledger entries
        pass


async def list_stock_ledger(tenant_id: uuid.UUID, warehouse_id: uuid.UUID, product_variant_id: uuid.UUID) -> list[StockLedger]:
    async with get_async_session(str(tenant_id)) as session:
        stmt = (
            select(StockLedger)
            .where(StockLedger.warehouse_id == warehouse_id, StockLedger.product_variant_id == product_variant_id)
            .order_by(StockLedger.txn_time.desc())
        )
        result = await session.execute(stmt)
        return list(result.scalars())
