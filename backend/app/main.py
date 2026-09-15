from fastapi import FastAPI
from backend.app.api.routes import health

app = FastAPI(title="ShrinkToken Pro")

app.include_router(health.router)
# app.include_router(optimize.router, prefix="/api/v1")
# app.include_router(validate.router, prefix="/api/v1")
# app.include_router(cost.router, prefix="/api/v1")
