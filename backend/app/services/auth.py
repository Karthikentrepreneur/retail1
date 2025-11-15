from __future__ import annotations

import datetime as dt
import uuid

from fastapi import HTTPException, status
from sqlalchemy import select

from app.core.security import create_access_token, verify_password
from app.db.session import get_async_session
from app.models import Store, Tenant, User, UserRole

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

_refresh_store: dict[str, dict[str, str]] = {}


async def authenticate_user(username: str, password: str):
    async with get_async_session() as session:
        stmt = select(User, Tenant).join(Tenant, User.tenant_id == Tenant.id).where((User.email == username) | (User.phone == username))
        result = await session.execute(stmt)
        row = result.first()
        if not row:
            return None, None, None
        user: User = row[0]
        tenant: Tenant = row[1]
        if not user.password_hash or not verify_password(password, user.password_hash):
            return None, None, None
        role_stmt = select(UserRole, Store).join(Store, UserRole.store_id == Store.id, isouter=True).where(UserRole.user_id == user.id)
        roles = await session.execute(role_stmt)
        store_scope = [str(role.store_id) for role, _ in roles if role.store_id]
        return user, tenant, store_scope


def issue_access_token(user: User, tenant_id: uuid.UUID, store_scope: list[str] | None) -> str:
    roles = []
    for role in user.roles if hasattr(user, "roles") else []:
        roles.append(role.role)
    return create_access_token(str(user.id), str(tenant_id), store_scope[0] if store_scope else None, roles)


async def issue_refresh_token(user: User, tenant_id: uuid.UUID) -> str:
    refresh_token = uuid.uuid4().hex
    _refresh_store.setdefault(str(user.id), {})[str(tenant_id)] = refresh_token
    return refresh_token


async def refresh_tokens(refresh_token: str) -> tuple[str, str, float]:
    for user_id, tenant_map in _refresh_store.items():
        for tenant_id, stored_token in tenant_map.items():
            if stored_token == refresh_token:
                new_access = create_access_token(user_id, tenant_id, None, [], expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                new_refresh = uuid.uuid4().hex
                _refresh_store[user_id][tenant_id] = new_refresh
                return new_access, new_refresh, float(dt.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds())
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


async def verify_otp(user_id: str, code: str) -> bool:
    # placeholder: integrate with OTP provider
    return code == "000000"

