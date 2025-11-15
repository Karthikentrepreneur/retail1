from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status

from app.core.security import decode_token


class TenantContext:
    def __init__(self) -> None:
        self.scopes = {}

    async def __call__(self, request: Request) -> dict[str, str | list[str] | None]:
        auth_header = request.headers.get("Authorization")
        token = None
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        payload = decode_token(token)
        tenant_id = payload.get("tenant_id")
        if not tenant_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tenant missing in token")
        request.state.tenant_id = tenant_id
        request.state.store_id = payload.get("store_id")
        request.state.roles = payload.get("roles", [])
        return {"tenant_id": tenant_id, "store_id": request.state.store_id, "roles": request.state.roles}

    async def require_tenant(self, ctx: dict = Depends()):
        return ctx

    async def require_store(self, ctx: dict = Depends()):
        if not ctx.get("store_id"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Store scope required")
        return ctx

    async def require_device(self, ctx: dict = Depends()):
        return ctx

    async def require_internal(self, ctx: dict = Depends()):
        roles = ctx.get("roles", [])
        if "owner" not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Owner role required")
        return ctx


tenant_context = TenantContext()
