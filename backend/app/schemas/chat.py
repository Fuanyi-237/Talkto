from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatMessageBase(BaseModel):
    receiver_id: str
    content: str
    media_url: Optional[str] = None
    appointment_id: Optional[str] = None


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageResponse(BaseModel):
    id: str
    sender_id: str
    receiver_id: str
    content: str
    media_url: Optional[str] = None
    appointment_id: Optional[str] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MediaUploadResponse(BaseModel):
    media_url: str
