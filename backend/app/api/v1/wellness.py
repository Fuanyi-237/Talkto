from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date, datetime
from typing import Optional

from app.core.deps import get_db, get_current_active_user
from app.schemas.wellness import (
    MoodLogCreate,
    MoodLogResponse,
    JournalEntryCreate,
    JournalEntryResponse,
)
from app.models.user import User
from app.models.wellness import MoodLog, JournalEntry

router = APIRouter()


@router.get("/moods", response_model=list[MoodLogResponse])
async def get_mood_history(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(30, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(MoodLog).where(MoodLog.user_id == current_user.id)
    
    if start_date:
        query = query.where(MoodLog.log_date >= start_date)
    if end_date:
        query = query.where(MoodLog.log_date <= end_date)
    
    query = query.order_by(MoodLog.log_date.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    mood_logs = result.scalars().all()
    
    return mood_logs


@router.post("/moods", response_model=MoodLogResponse, status_code=201)
async def log_mood(
    mood_data: MoodLogCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    mood_log = MoodLog(
        user_id=current_user.id,
        mood_score=mood_data.mood_score,
        stress_level=mood_data.stress_level,
        energy_level=mood_data.energy_level,
        sleep_quality=mood_data.sleep_quality,
        note=mood_data.note,
        log_date=mood_data.log_date,
    )
    
    db.add(mood_log)
    await db.commit()
    await db.refresh(mood_log)
    
    return mood_log


@router.get("/journals", response_model=list[JournalEntryResponse])
async def get_journal_entries(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    tag: Optional[str] = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(JournalEntry).where(JournalEntry.user_id == current_user.id)
    
    if tag:
        query = query.where(JournalEntry.tags.contains(tag))
    
    query = query.order_by(JournalEntry.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    entries = result.scalars().all()
    
    return entries


@router.post("/journals", response_model=JournalEntryResponse, status_code=201)
async def create_journal_entry(
    entry_data: JournalEntryCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    entry = JournalEntry(
        user_id=current_user.id,
        title=entry_data.title,
        content=entry_data.content,
        tags=entry_data.tags,
        image_url=entry_data.image_url,
    )
    
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    
    return entry
