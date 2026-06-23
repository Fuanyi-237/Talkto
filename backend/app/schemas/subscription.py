from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SubscriptionBase(BaseModel):
    plan_tier: str  # FREE, PREMIUM


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionResponse(SubscriptionBase):
    id: str
    user_id: str
    start_date: datetime
    end_date: Optional[datetime] = None
    status: str  # ACTIVE, CANCELLED, EXPIRED
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CheckoutRequest(BaseModel):
    plan_tier: str  # FREE, PREMIUM
    payment_method: str  # stripe, momo, orange
