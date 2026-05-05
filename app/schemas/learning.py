"""Learning progress schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Any, Generic, TypeVar, List


class ExerciseSubmission(BaseModel):
    """Schema for submitting an exercise answer."""
    exercise_id: int
    submitted_answer: dict[str, Any]


class ExerciseResultResponse(BaseModel):
    """Schema for exercise result response."""
    id: int
    child_id: int
    exercise_id: int
    is_correct: bool
    xp_earned: int
    completed_at: datetime

    class Config:
        from_attributes = True


class LessonCompletionResponse(BaseModel):
    """Schema for lesson completion response."""
    id: int
    child_id: int
    lesson_id: int
    score: int
    xp_earned: int
    completed_at: datetime

    class Config:
        from_attributes = True


T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int