"""Curriculum schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any


class UnitCreate(BaseModel):
    """Schema for creating a unit."""
    title: str
    description: Optional[str] = None
    order_index: int
    is_published: bool = False


class UnitUpdate(BaseModel):
    """Schema for updating a unit."""
    title: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[int] = None
    is_published: Optional[bool] = None


class UnitResponse(BaseModel):
    """Schema for unit response."""
    id: int
    title: str
    description: Optional[str]
    order_index: int
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LessonCreate(BaseModel):
    """Schema for creating a lesson."""
    unit_id: int
    title: str
    description: Optional[str] = None
    order_index: int
    is_published: bool = False


class LessonUpdate(BaseModel):
    """Schema for updating a lesson."""
    title: Optional[str] = None
    description: Optional[str] = None
    order_index: Optional[int] = None
    is_published: Optional[bool] = None


class LessonResponse(BaseModel):
    """Schema for lesson response."""
    id: int
    unit_id: int
    title: str
    description: Optional[str]
    order_index: int
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ExerciseCreate(BaseModel):
    """Schema for creating an exercise."""
    lesson_id: int
    type: str
    question: str
    content: dict[str, Any]
    correct_answer: dict[str, Any]
    order_index: int
    xp_value: int = 10


class ExerciseUpdate(BaseModel):
    """Schema for updating an exercise."""
    type: Optional[str] = None
    question: Optional[str] = None
    content: Optional[dict[str, Any]] = None
    correct_answer: Optional[dict[str, Any]] = None
    order_index: Optional[int] = None
    xp_value: Optional[int] = None


class ExerciseResponse(BaseModel):
    """Schema for exercise response (without correct answer)."""
    id: int
    lesson_id: int
    type: str
    question: str
    content: dict[str, Any]
    order_index: int
    xp_value: int
    created_at: datetime

    class Config:
        from_attributes = True
