from fastapi import FastAPI
from app.api.webhook import router as webhook_router
from app.core.config import settings
from app.core.logging_config import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend for Pune Family Concierge Bot - Phase 1",
    version="1.0.0"
)

# Include Routers
app.include_router(webhook_router, prefix=settings.API_V1_STR, tags=["webhook"])

@app.get("/")
async def root():
    return {"message": "Welcome to Pune Family Concierge Bot API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Pune Family Concierge Bot...")
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_ENV == "dev",
    )
