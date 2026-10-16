from fastapi import FastAPI
from app.middleware import (
    SecurityHeadersMiddleware,
)
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.database.connection import Base, engine
from app.models import User
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse
from app.rate_limit import limiter



Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Secure API Lab",
    description=(
        "Educational API security project."
    ),
    version="0.1.0",
)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

app.add_middleware(
    SecurityHeadersMiddleware
)

app.include_router(
    users_router
)

app.include_router(auth_router)
app.include_router(users_router)

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error."
        },
    )

@app.get("/")
def root():
    return {
        "message": (
            "Secure API Lab is running."
        )
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }