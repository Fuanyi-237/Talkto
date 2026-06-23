from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Subscription(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "subscriptions"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_tier: Mapped[str] = mapped_column(String(20), nullable=False)  # FREE, PREMIUM
    start_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # ACTIVE, CANCELLED, EXPIRED

    # Relationships
    user = relationship("User", back_populates="subscriptions")
