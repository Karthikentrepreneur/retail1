from __future__ import annotations

import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import auth as auth_schema
from app.services import auth as auth_service

router = APIRouter()


@router.post("/login", response_model=auth_schema.TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> auth_schema.TokenResponse:
    user, tenant, store_scope = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = auth_service.issue_access_token(user, tenant.id, store_scope)
    refresh_token = await auth_service.issue_refresh_token(user, tenant.id)
    return auth_schema.TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=dt.timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds(),
    )


@router.post("/refresh", response_model=auth_schema.TokenResponse)
async def refresh(request: auth_schema.RefreshRequest) -> auth_schema.TokenResponse:
    new_access, new_refresh, expires = await auth_service.refresh_tokens(request.refresh_token)
    return auth_schema.TokenResponse(access_token=new_access, refresh_token=new_refresh, token_type="bearer", expires_in=expires)


@router.post("/mfa/verify", response_model=auth_schema.MFAResponse)
async def mfa_verify(payload: auth_schema.MFARequest) -> auth_schema.MFAResponse:
    verified = await auth_service.verify_otp(payload.user_id, payload.code)
    if not verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
    return auth_schema.MFAResponse(success=True)
