from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware

from app.core.config import settings
from app.core.logging import configure_logging
from app.api.routes import auth, tenants, products, inventory, sales, payments, gst, reports, sync
from app.api.dependencies import tenant_context


logger = logging.getLogger(__name__)


@asynccontextmanager
def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Starting POS API", extra={"env": settings.environment})
    yield
    logger.info("Shutting down POS API")


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(SessionMiddleware, secret_key=settings.session_secret, max_age=3600),
]

app = FastAPI(
    title="POS SaaS API",
    version="0.1.0",
    lifespan=lifespan,
    middleware=middleware,
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception", extra={"path": request.url.path})
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.middleware("http")
async def tenant_header_middleware(request: Request, call_next):
    tenant_id = request.headers.get("X-Tenant-ID")
    if tenant_id:
        request.state.tenant_id = tenant_id
    response = await call_next(request)
    if tenant_id:
        response.headers["X-Tenant-ID"] = tenant_id
    return response


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tenants.router, prefix="/api", tags=["tenants"], dependencies=[Depends(tenant_context.require_internal)])
app.include_router(products.router, prefix="/api", tags=["products"], dependencies=[Depends(tenant_context.require_tenant)])
app.include_router(inventory.router, prefix="/api", tags=["inventory"], dependencies=[Depends(tenant_context.require_tenant)])
app.include_router(sales.router, prefix="/api", tags=["sales"], dependencies=[Depends(tenant_context.require_store)])
app.include_router(payments.router, prefix="/api", tags=["payments"], dependencies=[Depends(tenant_context.require_tenant)])
app.include_router(gst.router, prefix="/api", tags=["gst"], dependencies=[Depends(tenant_context.require_tenant)])
app.include_router(reports.router, prefix="/api", tags=["reports"], dependencies=[Depends(tenant_context.require_tenant)])
app.include_router(sync.router, prefix="/api", tags=["sync"], dependencies=[Depends(tenant_context.require_device)])


@app.get("/healthz", tags=["health"])
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready", tags=["health"])
async def ready() -> dict[str, str]:
    return {"status": "ready"}

