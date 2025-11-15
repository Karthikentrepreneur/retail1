from __future__ import annotations

import datetime as dt
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: float


class RefreshRequest(BaseModel):
    refresh_token: str


class MFARequest(BaseModel):
    user_id: str
    code: str


class MFAResponse(BaseModel):
    success: bool
    challenge_id: Optional[str] = None
    expires_at: Optional[dt.datetime] = None


class UserOut(BaseModel):
    id: str
    email: EmailStr | None
    phone: str | None
    roles: list[str]
    store_scopes: list[str]


class LoginAudit(BaseModel):
    tenant_id: str
    user_id: str
    device_id: str | None = None
    success: bool
    ip_address: str | None = None
    user_agent: str | None = None
    timestamp: dt.datetime = Field(default_factory=dt.datetime.utcnow)
