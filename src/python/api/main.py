from fastapi import FastAPI

from api.routers import assets, exchanges, listings, admin

app = FastAPI(
    title="Asset Manager API",
    description="API for managing financial assets",
    version="0.1.0",
)

app.include_router(assets.router)
app.include_router(exchanges.router)
app.include_router(listings.router)
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
