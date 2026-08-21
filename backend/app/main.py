from fastapi import FastAPI

from .database import Base, engine
from . import models


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="ResolveIQ API",
    description="AI-assisted exception resolution workbench",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "ResolveIQ API is running",
        "status": "healthy"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }
