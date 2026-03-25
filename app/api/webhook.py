from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse
from app.schemas.whatsapp import WhatsAppWebhookPayload
from app.adapters.whatsapp import WhatsAppAdapter
from app.services.intent_service import IntentDetector
from app.services.response_builder import ResponseBuilder
from app.core.logging_config import logger
from app.core.config import settings

router = APIRouter()


@router.get("/whatsapp", response_class=PlainTextResponse)
async def verify_whatsapp_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
):
    """
    Verification endpoint for WhatsApp Cloud API webhook setup.
    """
    logger.info("Received WhatsApp webhook verification request")

    if hub_mode == "subscribe" and hub_verify_token == settings.WHATSAPP_VERIFY_TOKEN:
        logger.info("WhatsApp webhook verification succeeded")
        return hub_challenge

    logger.warning("WhatsApp webhook verification failed")
    raise HTTPException(status_code=403, detail="Verification token mismatch")


@router.post("/whatsapp")
async def whatsapp_webhook(payload: WhatsAppWebhookPayload):
    """
    Endpoint for WhatsApp Cloud API Webhooks.
    """
    logger.info("Received WhatsApp webhook")
    
    try:
        # 1. Adapt external payload to internal schema
        internal_request = WhatsAppAdapter.to_internal(payload)
        logger.info(f"Adapted request from user: {internal_request.user_id}")
        
        # 2. Detect Intent
        intent = IntentDetector.detect(internal_request)
        logger.info(f"Detected intent: {intent.type}")
        
        # 3. Build Response
        bot_response = ResponseBuilder.build(intent)
        logger.info(f"Generated response for user: {internal_request.user_id}")
        
        return bot_response
        
    except ValueError as e:
        logger.error(f"Error processing webhook: {str(e)}")
        # For webhooks, sometimes it's better to return 200 even on some errors 
        # to prevent WhatsApp from retrying indefinitely, but here we raise 400 for bad payloads
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
