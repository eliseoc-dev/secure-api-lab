from fastapi import FastAPI

from app.api.users import router as users_router
from app.database.connection import Base, engine
from app.models import User


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


app.include_router(
    users_router
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