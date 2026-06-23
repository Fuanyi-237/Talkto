from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class CounselorBase(BaseModel):
    credentials: Optional[str] = None
    years_of_experience: Optional[int] = None
    biography: Optional[str] = None
    session_pricing: Optional[Decimal] = None


class CounselorCreate(CounselorBase):
    verification_documents_url: Optional[str] = None


class CounselorUpdate(BaseModel):
    credentials: Optional[str] = None
    years_of_experience: Optional[int] = None
    biography: Optional[str] = None
    session_pricing: Optional[Decimal] = None


class CounselorResponse(CounselorBase):
    id: str
    user_id: str
    is_verified: bool
    verification_documents_url: Optional[str] = None
    average_rating: float
    created_at: datetime
    updated_at: datetime
    user: dict  # Basic user info

    class Config:
        from_attributes = True


class CounselorListResponse(BaseModel):
    id: str
    full_name: str
    profile_picture_url: Optional[str] = None
    years_of_experience: Optional[int] = None
    biography: Optional[str] = None
    session_pricing: Optional[Decimal] = None
    average_rating: float
    is_verified: bool
    specialties: list[str] = []

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: str
    user_id: str
    counselor_id: str
    rating: int
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
