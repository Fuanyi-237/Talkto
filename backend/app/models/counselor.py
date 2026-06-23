from sqlalchemy import Boolean, String, Integer, Numeric, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Counselor(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "counselors"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    credentials: Mapped[str] = mapped_column(String(255), nullable=True)
    years_of_experience: Mapped[int] = mapped_column(Integer, nullable=True)
    biography: Mapped[str] = mapped_column(Text, nullable=True)
    session_pricing: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verification_documents_url: Mapped[str] = mapped_column(String(500), nullable=True)
    average_rating: Mapped[float] = mapped_column(Numeric(3, 2), default=0.0, nullable=False)

    # Relationships
    user = relationship("User", back_populates="counselor_profile")
    appointments = relationship("Appointment", back_populates="counselor", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="counselor", cascade="all, delete-orphan")
    sent_messages = relationship("ChatMessage", foreign_keys="ChatMessage.sender_id", back_populates="sender")
    received_messages = relationship("ChatMessage", foreign_keys="ChatMessage.receiver_id", back_populates="receiver")
    specialties = relationship("CounselorSpecialty", back_populates="counselor", cascade="all, delete-orphan")


class CounselorSpecialty(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "counselor_specialties"

    counselor_id: Mapped[str] = mapped_column(ForeignKey("counselors.id", ondelete="CASCADE"), nullable=False)
    specialty_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relationships
    counselor = relationship("Counselor", back_populates="specialties")
