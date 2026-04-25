from fastapi import FastAPI
from app.api.v1.api import api_router
from app.web.router import router as web_router
from app.core.config import settings
from app.core.logging_config import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Web Application & API for Pune Family Concierge",
    version="2.0.0"
)

# Include Routers
app.include_router(web_router, tags=["web"])
app.include_router(api_router, prefix=settings.API_V1_STR)

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
