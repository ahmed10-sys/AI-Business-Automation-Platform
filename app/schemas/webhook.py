from pydantic import BaseModel, Field, ConfigDict
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

class WhatsAppMedia(BaseModel):
    id: str
    mime_type: str
    sha256: str

class WhatsAppImage(WhatsAppMedia):
    caption: Optional[str] = None

class WhatsAppDocument(WhatsAppMedia):
    caption: Optional[str] = None
    filename: Optional[str] = None

class WhatsAppAudio(WhatsAppMedia):
    pass

class WhatsAppVideo(WhatsAppMedia):
    caption: Optional[str] = None

class WhatsAppVoice(WhatsAppMedia):
    pass

class Message(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_: str = Field(alias="from")
    id: str
    timestamp: str
    type: str
    text: Optional[TextMessageContent] = None
    image: Optional[WhatsAppImage] = None
    document: Optional[WhatsAppDocument] = None
    audio: Optional[WhatsAppAudio] = None
    video: Optional[WhatsAppVideo] = None
    voice: Optional[WhatsAppVoice] = None
    location: Optional[Dict[str, Any]] = None
    contacts: Optional[List[Dict[str, Any]]] = None
    interactive: Optional[Dict[str, Any]] = None
    button: Optional[Dict[str, Any]] = None
    context: Optional[Dict[str, Any]] = None
    errors: Optional[List[Dict[str, Any]]] = None

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
