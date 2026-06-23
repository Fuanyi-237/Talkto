from sqlalchemy import String, ForeignKey, DateTime, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Appointment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "appointments"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    counselor_id: Mapped[str] = mapped_column(ForeignKey("counselors.id", ondelete="CASCADE"), nullable=False)
    scheduled_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # PENDING, CONFIRMED, COMPLETED, CANCELLED
    meeting_link: Mapped[str] = mapped_column(String(500), nullable=True)  # Agora or internal reference
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    payment_status: Mapped[str] = mapped_column(String(20), nullable=False)  # UNPAID, PAID, REFUNDED

    # Relationships
    user = relationship("User", back_populates="appointments")
    counselor = relationship("Counselor", back_populates="appointments")
    chat_messages = relationship("ChatMessage", back_populates="appointment", cascade="all, delete-orphan")
