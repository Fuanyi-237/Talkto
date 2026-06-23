from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime

from app.core.deps import get_db, get_current_active_user
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
    AgoraTokenResponse,
)
from app.models.user import User
from app.models.appointment import Appointment
from app.models.counselor import Counselor

router = APIRouter()


@router.get("", response_model=list[AppointmentResponse])
async def list_appointments(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).where(Appointment.user_id == current_user.id)
        .order_by(Appointment.scheduled_time.desc())
    )
    appointments = result.scalars().all()
    
    response = []
    for appointment in appointments:
        # Get counselor info
        counselor_result = await db.execute(
            select(Counselor, User).join(User, Counselor.user_id == User.id)
            .where(Counselor.id == appointment.counselor_id)
        )
        counselor_data = counselor_result.first()
        
        if counselor_data:
            counselor, user = counselor_data
            counselor_info = {
                "id": str(counselor.id),
                "full_name": user.full_name,
                "profile_picture_url": user.profile_picture_url,
                "session_pricing": float(counselor.session_pricing),
            }
        else:
            counselor_info = {}
        
        response.append(
            AppointmentResponse(
                id=str(appointment.id),
                user_id=str(appointment.user_id),
                counselor_id=str(appointment.counselor_id),
                scheduled_time=appointment.scheduled_time,
                duration_minutes=appointment.duration_minutes,
                status=appointment.status,
                meeting_link=appointment.meeting_link,
                price=float(appointment.price),
                payment_status=appointment.payment_status,
                created_at=appointment.created_at,
                updated_at=appointment.updated_at,
                counselor=counselor_info,
            )
        )
    
    return response


@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment_data: AppointmentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if counselor exists and is verified
    counselor_result = await db.execute(
        select(Counselor).where(Counselor.id == appointment_data.counselor_id)
    )
    counselor = counselor_result.scalar_one_or_none()
    
    if not counselor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counselor not found"
        )
    
    if not counselor.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Counselor is not verified"
        )
    
    # Create appointment
    appointment = Appointment(
        user_id=current_user.id,
        counselor_id=appointment_data.counselor_id,
        scheduled_time=appointment_data.scheduled_time,
        duration_minutes=appointment_data.duration_minutes,
        status="PENDING",
        price=counselor.session_pricing or 0,
        payment_status="UNPAID",
    )
    
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    
    # Get counselor info for response
    user_result = await db.execute(
        select(User).where(User.id == counselor.user_id)
    )
    user = user_result.scalar_one_or_none()
    
    counselor_info = {
        "id": str(counselor.id),
        "full_name": user.full_name if user else "",
        "profile_picture_url": user.profile_picture_url if user else None,
        "session_pricing": float(counselor.session_pricing) if counselor.session_pricing else 0,
    }
    
    return AppointmentResponse(
        id=str(appointment.id),
        user_id=str(appointment.user_id),
        counselor_id=str(appointment.counselor_id),
        scheduled_time=appointment.scheduled_time,
        duration_minutes=appointment.duration_minutes,
        status=appointment.status,
        meeting_link=appointment.meeting_link,
        price=float(appointment.price),
        payment_status=appointment.payment_status,
        created_at=appointment.created_at,
        updated_at=appointment.updated_at,
        counselor=counselor_info,
    )


@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).where(
            Appointment.id == appointment_id,
            Appointment.user_id == current_user.id
        )
    )
    appointment = result.scalar_one_or_none()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Get counselor info
    counselor_result = await db.execute(
        select(Counselor, User).join(User, Counselor.user_id == User.id)
        .where(Counselor.id == appointment.counselor_id)
    )
    counselor_data = counselor_result.first()
    
    if counselor_data:
        counselor, user = counselor_data
        counselor_info = {
            "id": str(counselor.id),
            "full_name": user.full_name,
            "profile_picture_url": user.profile_picture_url,
            "session_pricing": float(counselor.session_pricing),
        }
    else:
        counselor_info = {}
    
    return AppointmentResponse(
        id=str(appointment.id),
        user_id=str(appointment.user_id),
        counselor_id=str(appointment.counselor_id),
        scheduled_time=appointment.scheduled_time,
        duration_minutes=appointment.duration_minutes,
        status=appointment.status,
        meeting_link=appointment.meeting_link,
        price=float(appointment.price),
        payment_status=appointment.payment_status,
        created_at=appointment.created_at,
        updated_at=appointment.updated_at,
        counselor=counselor_info,
    )


@router.put("/{appointment_id}/reschedule", response_model=AppointmentResponse)
async def reschedule_appointment(
    appointment_id: str,
    appointment_update: AppointmentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).where(
            Appointment.id == appointment_id,
            Appointment.user_id == current_user.id
        )
    )
    appointment = result.scalar_one_or_none()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    if appointment.status in ["COMPLETED", "CANCELLED"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot reschedule completed or cancelled appointments"
        )
    
    # Update appointment
    update_data = appointment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(appointment, field, value)
    
    appointment.status = "PENDING"
    
    await db.commit()
    await db.refresh(appointment)
    
    # Get counselor info
    counselor_result = await db.execute(
        select(Counselor, User).join(User, Counselor.user_id == User.id)
        .where(Counselor.id == appointment.counselor_id)
    )
    counselor_data = counselor_result.first()
    
    if counselor_data:
        counselor, user = counselor_data
        counselor_info = {
            "id": str(counselor.id),
            "full_name": user.full_name,
            "profile_picture_url": user.profile_picture_url,
            "session_pricing": float(counselor.session_pricing),
        }
    else:
        counselor_info = {}
    
    return AppointmentResponse(
        id=str(appointment.id),
        user_id=str(appointment.user_id),
        counselor_id=str(appointment.counselor_id),
        scheduled_time=appointment.scheduled_time,
        duration_minutes=appointment.duration_minutes,
        status=appointment.status,
        meeting_link=appointment.meeting_link,
        price=float(appointment.price),
        payment_status=appointment.payment_status,
        created_at=appointment.created_at,
        updated_at=appointment.updated_at,
        counselor=counselor_info,
    )


@router.post("/{appointment_id}/cancel")
async def cancel_appointment(
    appointment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).where(
            Appointment.id == appointment_id,
            Appointment.user_id == current_user.id
        )
    )
    appointment = result.scalar_one_or_none()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    if appointment.status in ["COMPLETED", "CANCELLED"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel completed or already cancelled appointments"
        )
    
    appointment.status = "CANCELLED"
    
    await db.commit()
    
    return {"message": "Appointment cancelled successfully"}


@router.get("/{appointment_id}/token", response_model=AgoraTokenResponse)
async def get_agora_token(
    appointment_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Appointment).where(
            Appointment.id == appointment_id,
            Appointment.user_id == current_user.id
        )
    )
    appointment = result.scalar_one_or_none()
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    if appointment.status != "CONFIRMED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment must be confirmed to get video token"
        )
    
    # In production, generate actual Agora token using agora-token-builder
    # For now, return a placeholder
    return AgoraTokenResponse(
        token="placeholder_agora_token",
        channel_name=f"appointment_{appointment_id}",
        uid=12345,
    )
