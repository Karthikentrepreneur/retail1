from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException, Request, status

from app.schemas import sales as sales_schema
from app.services import sales as sales_service

router = APIRouter()


@router.post("/sales", response_model=sales_schema.SaleOut)
async def create_sale(request: Request, payload: sales_schema.SaleCreate):
    tenant_id = uuid.UUID(request.state.tenant_id)
    sale = await sales_service.create_sale(tenant_id, payload)
    return sales_schema.SaleOut(
        id=str(sale.id),
        invoice_number=sale.invoice_number,
        store_id=str(sale.store_id),
        subtotal=float(sale.subtotal),
        tax_total=float(sale.tax_total),
        grand_total=float(sale.grand_total),
        status=sale.status,
    )


@router.get("/sales/{sale_id}", response_model=sales_schema.SaleOut)
async def get_sale(request: Request, sale_id: uuid.UUID):
    tenant_id = uuid.UUID(request.state.tenant_id)
    sale = await sales_service.get_sale(tenant_id, sale_id)
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return sales_schema.SaleOut(
        id=str(sale.id),
        invoice_number=sale.invoice_number,
        store_id=str(sale.store_id),
        subtotal=float(sale.subtotal),
        tax_total=float(sale.tax_total),
        grand_total=float(sale.grand_total),
        status=sale.status,
    )
