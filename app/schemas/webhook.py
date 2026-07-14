from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class WhatsAppMetadata(BaseModel):
    display_phone_number: str
    phone_number_id: str

class Profile(BaseModel):
    name: str

class Contact(BaseModel):
    profile: Profile
    wa_id: str

class TextMessageContent(BaseModel):
    body: str

class Message(BaseModel):
    from_: str = Field(alias="from")
    id: str
    timestamp: str
    type: str
    text: Optional[TextMessageContent] = None
    image: Optional[Dict[str, Any]] = None
    document: Optional[Dict[str, Any]] = None
    audio: Optional[Dict[str, Any]] = None
    video: Optional[Dict[str, Any]] = None
    voice: Optional[Dict[str, Any]] = None
    location: Optional[Dict[str, Any]] = None
    contacts: Optional[List[Dict[str, Any]]] = None
    interactive: Optional[Dict[str, Any]] = None
    button: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    errors: Optional[List[Dict[str, Any]]] = None

    class Config:
        populate_by_name = True

class Conversation(BaseModel):
    id: str
    expiration_timestamp: Optional[str] = None
    origin: Dict[str, Any]

class Pricing(BaseModel):
    billable: bool
    pricing_model: str
    category: str

class Status(BaseModel):
    id: str
    status: str
    timestamp: str
    recipient_id: str
    conversation: Optional[Conversation] = None
    pricing: Optional[Pricing] = None
    errors: Optional[List[Dict[str, Any]]] = None

class ChangeValue(BaseModel):
    messaging_product: str
    metadata: WhatsAppMetadata
    contacts: Optional[List[Contact]] = None
    messages: Optional[List[Message]] = None
    statuses: Optional[List[Status]] = None

class Change(BaseModel):
    value: ChangeValue
    field: str

class Entry(BaseModel):
    id: str
    changes: List[Change]

class WhatsAppWebhookPayload(BaseModel):
    object: str
    entry: List[Entry]
