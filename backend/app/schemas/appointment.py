from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class AppointmentBase(BaseModel):
    counselor_id: str
    scheduled_time: datetime
    duration_minutes: int = Field(..., ge=15, le=120)


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    scheduled_time: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=15, le=120)


class AppointmentResponse(AppointmentBase):
    id: str
    user_id: str
    status: str  # PENDING, CONFIRMED, COMPLETED, CANCELLED
    meeting_link: Optional[str] = None
    price: Decimal
    payment_status: str  # UNPAID, PAID, REFUNDED
    created_at: datetime
    updated_at: datetime
    counselor: dict  # Basic counselor info

    class Config:
        from_attributes = True


class AgoraTokenResponse(BaseModel):
    token: str
    channel_name: str
    uid: int
