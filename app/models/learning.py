"""Learning progress models."""
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class ExerciseResult(Base):
    """Record of a child's exercise attempt."""

    __tablename__ = "exercise_results"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    submitted_answer = Column(JSON, nullable=False)
    xp_earned = Column(Integer, default=0)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    child = relationship("Child", back_populates="exercise_results")
    exercise = relationship("Exercise", back_populates="results")


class LessonCompletion(Base):
    """Record of a child completing a lesson."""

    __tablename__ = "lesson_completions"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    score = Column(Integer, nullable=False)  # Percentage or points
    xp_earned = Column(Integer, default=0)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    child = relationship("Child", back_populates="lesson_completions")
    lesson = relationship("Lesson", back_populates="completions")
