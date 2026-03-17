from typing import List, Optional
from pydantic import BaseModel, Field

class WhatsAppText(BaseModel):
    body: str

class WhatsAppMessage(BaseModel):
    from_: str = Field(..., alias="from")
    id: str
    timestamp: str
    text: Optional[WhatsAppText] = None
    type: str

class WhatsAppContact(BaseModel):
    profile: dict
    wa_id: str

class WhatsAppMetadata(BaseModel):
    display_phone_number: str
    phone_number_id: str

class WhatsAppValue(BaseModel):
    messaging_product: str
    metadata: WhatsAppMetadata
    contacts: Optional[List[WhatsAppContact]] = None
    messages: Optional[List[WhatsAppMessage]] = None

class WhatsAppChange(BaseModel):
    value: WhatsAppValue
    field: str

class WhatsAppEntry(BaseModel):
    id: str
    changes: List[WhatsAppChange]

class WhatsAppWebhookPayload(BaseModel):
    object: str
    entry: List[WhatsAppEntry]
