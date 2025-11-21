from fastapi import FastAPI
from src.python.api.routers import assets

app = FastAPI(
    title="Asset Manager API",
    description="API for managing financial assets",
    version="0.1.0",
)

app.include_router(assets.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
