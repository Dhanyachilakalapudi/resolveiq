from fastapi import FastAPI

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
        "status": "healthy"
    }
