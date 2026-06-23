from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    preferred_language: Optional[str] = None
    profile_picture_url: Optional[str] = None


class UserRegister(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    country: Optional[str] = None
    preferred_language: Optional[str] = None
    profile_picture_url: Optional[str] = None


class UserResponse(UserBase):
    id: str
    is_active: bool
    is_counselor: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OnboardingQuestionnaire(BaseModel):
    primary_concern: str
    preferred_communication: str  # video, voice, chat
    preferred_gender: Optional[str] = None
    budget_range: Optional[str] = None
    previous_therapy: bool = False
    additional_notes: Optional[str] = None
