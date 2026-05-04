"""Gamification models: Badges and achievements."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Badge(Base):
    """Badge/Achievement definition."""

    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    icon = Column(String, nullable=False)
    criteria_type = Column(String, nullable=False)  # "xp", "streak", "lessons_completed", etc.
    criteria_value = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    child_badges = relationship("ChildBadge", back_populates="badge", cascade="all, delete-orphan")


class ChildBadge(Base):
    """Badge earned by a child."""

    __tablename__ = "child_badges"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id", ondelete="CASCADE"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id", ondelete="CASCADE"), nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    child = relationship("Child", back_populates="badges")
    badge = relationship("Badge", back_populates="child_badges")
