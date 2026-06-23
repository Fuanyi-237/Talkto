from sqlalchemy import String, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Review(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "reviews"

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    counselor_id: Mapped[str] = mapped_column(ForeignKey("counselors.id", ondelete="CASCADE"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5
    comment: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="reviews")
    counselor = relationship("Counselor", back_populates="reviews")
