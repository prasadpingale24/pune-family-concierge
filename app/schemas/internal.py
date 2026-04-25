from typing import Any, Dict, Optional
from pydantic import BaseModel

class UserMessage(BaseModel):
    user_id: str
    message: str

class BotResponse(BaseModel):
    reply: str
    intent: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
