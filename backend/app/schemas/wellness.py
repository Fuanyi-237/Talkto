from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class MoodLogBase(BaseModel):
    mood_score: int = Field(..., ge=1, le=10)
    stress_level: int = Field(..., ge=1, le=10)
    energy_level: int = Field(..., ge=1, le=10)
    sleep_quality: Optional[str] = None
    note: Optional[str] = None
    log_date: date


class MoodLogCreate(MoodLogBase):
    pass


class MoodLogResponse(MoodLogBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JournalEntryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    tags: Optional[str] = None  # comma separated emotions
    image_url: Optional[str] = None


class JournalEntryCreate(JournalEntryBase):
    pass


class JournalEntryResponse(JournalEntryBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
