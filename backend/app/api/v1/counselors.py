from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from app.core.deps import get_db, get_current_active_user
from app.schemas.counselor import (
    CounselorCreate,
    CounselorUpdate,
    CounselorResponse,
    CounselorListResponse,
    ReviewCreate,
    ReviewResponse,
)
from app.models.user import User
from app.models.counselor import Counselor, CounselorSpecialty
from app.models.review import Review

router = APIRouter()


@router.get("", response_model=list[CounselorListResponse])
async def list_counselors(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    specialty: Optional[str] = None,
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(Counselor, User)
        .join(User, Counselor.user_id == User.id)
        .where(Counselor.is_verified == True)
    )
    
    if specialty:
        query = query.join(CounselorSpecialty).where(
            CounselorSpecialty.specialty_name == specialty
        )
    
    if min_rating:
        query = query.where(Counselor.average_rating >= min_rating)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    counselors = result.all()
    
    response = []
    for counselor, user in counselors:
        # Get specialties
        specialties_result = await db.execute(
            select(CounselorSpecialty.specialty_name).where(
                CounselorSpecialty.counselor_id == counselor.id
            )
        )
        specialties = [s[0] for s in specialties_result.fetchall()]
        
        response.append(
            CounselorListResponse(
                id=str(counselor.id),
                full_name=user.full_name,
                profile_picture_url=user.profile_picture_url,
                years_of_experience=counselor.years_of_experience,
                biography=counselor.biography,
                session_pricing=counselor.session_pricing,
                average_rating=float(counselor.average_rating),
                is_verified=counselor.is_verified,
                specialties=specialties,
            )
        )
    
    return response


@router.get("/{counselor_id}", response_model=CounselorResponse)
async def get_counselor(
    counselor_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Counselor, User).join(User, Counselor.user_id == User.id).where(
            Counselor.id == counselor_id
        )
    )
    counselor_user = result.scalar_one_or_none()
    
    if not counselor_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counselor not found"
        )
    
    counselor, user = counselor_user
    
    return CounselorResponse(
        id=str(counselor.id),
        user_id=str(counselor.user_id),
        credentials=counselor.credentials,
        years_of_experience=counselor.years_of_experience,
        biography=counselor.biography,
        session_pricing=counselor.session_pricing,
        is_verified=counselor.is_verified,
        verification_documents_url=counselor.verification_documents_url,
        average_rating=float(counselor.average_rating),
        created_at=counselor.created_at,
        updated_at=counselor.updated_at,
        user={
            "id": str(user.id),
            "full_name": user.full_name,
            "email": user.email,
            "profile_picture_url": user.profile_picture_url,
        }
    )


@router.post("/{counselor_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    counselor_id: str,
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if counselor exists
    counselor_result = await db.execute(
        select(Counselor).where(Counselor.id == counselor_id)
    )
    counselor = counselor_result.scalar_one_or_none()
    
    if not counselor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counselor not found"
        )
    
    # Check if user already reviewed this counselor
    existing_review = await db.execute(
        select(Review).where(
            Review.user_id == current_user.id,
            Review.counselor_id == counselor_id
        )
    )
    if existing_review.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this counselor"
        )
    
    # Create review
    review = Review(
        user_id=current_user.id,
        counselor_id=counselor_id,
        rating=review_data.rating,
        comment=review_data.comment
    )
    
    db.add(review)
    
    # Update counselor average rating
    ratings_result = await db.execute(
        select(func.avg(Review.rating)).where(Review.counselor_id == counselor_id)
    )
    avg_rating = ratings_result.scalar() or 0
    counselor.average_rating = avg_rating
    
    await db.commit()
    await db.refresh(review)
    
    return review


@router.get("/{counselor_id}/reviews", response_model=list[ReviewResponse])
async def get_counselor_reviews(
    counselor_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    # Check if counselor exists
    counselor_result = await db.execute(
        select(Counselor).where(Counselor.id == counselor_id)
    )
    if not counselor_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counselor not found"
        )
    
    result = await db.execute(
        select(Review).where(Review.counselor_id == counselor_id)
        .offset(skip).limit(limit)
    )
    reviews = result.scalars().all()
    
    return reviews


@router.get("/match", response_model=list[CounselorListResponse])
async def get_matched_counselors(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Simple matching algorithm - return verified counselors
    # In production, this would use the onboarding questionnaire data
    query = (
        select(Counselor, User)
        .join(User, Counselor.user_id == User.id)
        .where(Counselor.is_verified == True)
        .limit(10)
    )
    
    result = await db.execute(query)
    counselors = result.all()
    
    response = []
    for counselor, user in counselors:
        specialties_result = await db.execute(
            select(CounselorSpecialty.specialty_name).where(
                CounselorSpecialty.counselor_id == counselor.id
            )
        )
        specialties = [s[0] for s in specialties_result.fetchall()]
        
        response.append(
            CounselorListResponse(
                id=str(counselor.id),
                full_name=user.full_name,
                profile_picture_url=user.profile_picture_url,
                years_of_experience=counselor.years_of_experience,
                biography=counselor.biography,
                session_pricing=counselor.session_pricing,
                average_rating=float(counselor.average_rating),
                is_verified=counselor.is_verified,
                specialties=specialties,
            )
        )
    
    return response
