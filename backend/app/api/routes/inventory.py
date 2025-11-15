from __future__ import annotations

import uuid

from fastapi import APIRouter, Request

from app.schemas import inventory as inventory_schema
from app.services import inventory as inventory_service

router = APIRouter()


@router.get("/inventory/stock", response_model=list[inventory_schema.InventoryBalance])
async def get_stock(request: Request, warehouse_id: uuid.UUID | None = None):
    tenant_id = uuid.UUID(request.state.tenant_id)
    balances = await inventory_service.get_stock_balances(tenant_id, warehouse_id)
    return [
        inventory_schema.InventoryBalance(
            warehouse_id=str(item.warehouse_id),
            product_variant_id=str(item.product_variant_id),
            product_batch_id=str(item.product_batch_id) if item.product_batch_id else None,
            qty_on_hand=float(item.qty_on_hand),
            qty_reserved=float(item.qty_reserved),
        )
        for item in balances
    ]


@router.post("/inventory/transfers")
async def post_transfer(request: Request, payload: inventory_schema.InventoryTransferRequest):
    tenant_id = uuid.UUID(request.state.tenant_id)
    await inventory_service.record_transfer(tenant_id, payload)
    return {"status": "accepted"}


@router.get("/inventory/movements", response_model=list[inventory_schema.StockLedgerEntry])
async def get_movements(request: Request, warehouse_id: uuid.UUID, product_variant_id: uuid.UUID):
    tenant_id = uuid.UUID(request.state.tenant_id)
    entries = await inventory_service.list_stock_ledger(tenant_id, warehouse_id, product_variant_id)
    return [
        inventory_schema.StockLedgerEntry(
            id=entry.id,
            txn_type=entry.txn_type,
            quantity=float(entry.quantity),
            direction=int(entry.direction),
            running_balance=float(entry.running_balance),
            txn_time=entry.txn_time.isoformat(),
            reference=str(entry.txn_reference) if entry.txn_reference else None,
        )
        for entry in entries
    ]
