from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class InventoryTransferRequest(BaseModel):
    source_warehouse_id: str
    destination_warehouse_id: str
    items: list[dict[str, Any]]
    reference: str | None = None


class InventoryBalance(BaseModel):
    warehouse_id: str
    product_variant_id: str
    product_batch_id: str | None
    qty_on_hand: float
    qty_reserved: float


class StockLedgerEntry(BaseModel):
    id: int
    txn_type: str
    quantity: float
    direction: int
    running_balance: float
    txn_time: str
    reference: str | None = None
