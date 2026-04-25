from fastapi import APIRouter
from pydantic import BaseModel
from app.services.query_service import QueryService
from app.schemas.internal import BotResponse
from app.core.logging_config import logger

router = APIRouter()

class QueryRequest(BaseModel):
    message: str

@router.post("/query", response_model=BotResponse)
async def query(request: QueryRequest):
    """
    Core API endpoint for Pune Family Concierge.
    Accepts a user message and returns a structured response with intent and data.
    """
    logger.info(f"API Request: {request.message}")
    response = QueryService.process_query(request.message)
    logger.info(f"API Response: {response.intent}")
    return response
