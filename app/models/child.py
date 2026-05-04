"""Child profile model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app.db.database import Base


class Child(Base):
    """Child profile model."""

    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    avatar = Column(String, default="default_avatar.png")
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    streak_count = Column(Integer, default=0)
    last_activity_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    parent = relationship("User", back_populates="children")
    exercise_results = relationship("ExerciseResult", back_populates="child", cascade="all, delete-orphan")
    lesson_completions = relationship("LessonCompletion", back_populates="child", cascade="all, delete-orphan")
    badges = relationship("ChildBadge", back_populates="child", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="child", cascade="all, delete-orphan")
