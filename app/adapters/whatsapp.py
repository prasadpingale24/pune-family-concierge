from app.schemas.whatsapp import WhatsAppWebhookPayload
from app.schemas.internal import UserMessage
from app.core.logging_config import logger

class WhatsAppAdapter:
    @staticmethod
    def to_internal(payload: WhatsAppWebhookPayload) -> UserMessage:
        try:
            # Extract first entry, first change, first message
            # WhatsApp Cloud API sends complex nested payloads
            entry = payload.entry[0]
            change = entry.changes[0]
            value = change.value
            
            if not value.messages:
                logger.warning("No messages found in WhatsApp payload")
                raise ValueError("No messages in payload")
                
            message = value.messages[0]
            user_id = message.from_
            
            # Text body can be missing if it's not a text message
            if message.type == "text" and message.text:
                text_body = message.text.body
            else:
                text_body = ""
                logger.info(f"Received non-text message of type: {message.type}")

            return UserMessage(user_id=user_id, message=text_body)
            
        except (IndexError, AttributeError) as e:
            logger.error(f"Error parsing WhatsApp payload: {str(e)}")
            raise ValueError(f"Malformed WhatsApp payload: {str(e)}")
