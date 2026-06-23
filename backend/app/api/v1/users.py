from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.deps import get_db, get_current_active_user
from app.schemas.user import UserResponse, UserUpdate, OnboardingQuestionnaire
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Update user fields
    update_data = user_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user


@router.post("/onboarding")
async def submit_onboarding(
    questionnaire: OnboardingQuestionnaire,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Store onboarding data
    # In a real app, you might want to create a separate Onboarding model
    # For now, we'll just acknowledge receipt
    return {
        "message": "Onboarding questionnaire submitted successfully",
        "data": questionnaire
    }


@router.put("/me/avatar")
async def upload_avatar(
    avatar_url: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    current_user.profile_picture_url = avatar_url
    await db.commit()
    await db.refresh(current_user)
    
    return {"message": "Avatar updated successfully", "avatar_url": avatar_url}
