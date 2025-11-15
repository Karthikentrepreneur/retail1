from __future__ import annotations

from datetime import datetime

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
    challenge_id: str | None = None
    expires_at: datetime | None = None


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
    timestamp: datetime = Field(default_factory=datetime.utcnow)
