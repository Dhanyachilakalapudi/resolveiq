from fastapi import FastAPI

from .database import Base, engine
from . import models

from .routes.exceptions import router as exceptions_router
from .routes.resolution import router as resolution_router
from .routes.workflow import router as workflow_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="ResolveIQ API",
    description="AI-assisted exception resolution workbench",
    version="1.0.0"
)


app.include_router(exceptions_router)
app.include_router(resolution_router)
app.include_router(workflow_router)


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
