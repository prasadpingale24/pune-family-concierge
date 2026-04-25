from app.schemas.internal import UserMessage, BotResponse
from app.services.intent_service import IntentDetector
from app.services.response_builder import ResponseBuilder
from app.core.logging_config import logger

class QueryService:
    @staticmethod
    def process_query(message: str, user_id: str = "web_user") -> BotResponse:
        """
        Consolidated method to process a user query.
        Used by both API and Web layers.
        """
        logger.info(f"Processing query from {user_id}: {message}")
        
        # 1. Create internal request object
        user_message = UserMessage(user_id=user_id, message=message)
        
        # 2. Detect Intent
        intent = IntentDetector.detect(user_message)
        logger.info(f"Detected intent: {intent.type}")
        
        # 3. Build Response
        bot_response = ResponseBuilder.build(intent)
        logger.info(f"Generated response for intent: {intent.type}")
        
        return bot_response
