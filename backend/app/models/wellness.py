from sqlalchemy import String, ForeignKey, Integer, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class MoodLog(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "mood_logs"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    mood_score: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-10
    stress_level: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-10
    energy_level: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-10
    sleep_quality: Mapped[str] = mapped_column(String(50), nullable=True)
    note: Mapped[str] = mapped_column(Text, nullable=True)
    log_date: Mapped[Date] = mapped_column(Date, nullable=False)

    # Relationships
    user = relationship("User", back_populates="mood_logs")


class JournalEntry(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "journal_entries"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[str] = mapped_column(String(500), nullable=True)  # comma separated emotions
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)

    # Relationships
    user = relationship("User", back_populates="journal_entries")
