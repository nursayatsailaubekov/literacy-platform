"""Child profile schemas."""
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from app.schemas.learning import ExerciseResultResponse, LessonCompletionResponse


class ChildCreate(BaseModel):
    """Schema for creating a child profile."""
    name: str
    age: int
    avatar: Optional[str] = "default_avatar.png"


class ChildUpdate(BaseModel):
    """Schema for updating a child profile."""
    name: Optional[str] = None
    age: Optional[int] = None
    avatar: Optional[str] = None


class ChildResponse(BaseModel):
    """Schema for child response."""
    id: int
    parent_id: int
    name: str
    age: int
    avatar: str
    level: int
    xp: int
    streak_count: int
    last_activity_date: Optional[date]
    created_at: datetime

    class Config:
        from_attributes = True


class ChildProgress(BaseModel):
    """Schema for child's full progress."""
    child_id: int
    name: str
    level: int
    xp: int
    streak_count: int
    total_exercises_completed: int
    total_lessons_completed: int
    total_badges_earned: int
    exercise_results: list[ExerciseResultResponse]
    lesson_completions: list[LessonCompletionResponse]
    accuracy_rate: float

    class Config:
        from_attributes = True