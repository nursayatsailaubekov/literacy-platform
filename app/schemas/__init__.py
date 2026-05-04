"""Pydantic schemas for request/response validation."""
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.schemas.child import ChildCreate, ChildUpdate, ChildResponse
from app.schemas.curriculum import (
    UnitCreate,
    UnitUpdate,
    UnitResponse,
    LessonCreate,
    LessonUpdate,
    LessonResponse,
    ExerciseCreate,
    ExerciseUpdate,
    ExerciseResponse,
)
from app.schemas.learning import ExerciseSubmission, ExerciseResultResponse, LessonCompletionResponse
from app.schemas.gamification import BadgeCreate, BadgeResponse, ChildBadgeResponse
from app.schemas.notification import NotificationResponse

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "TokenResponse",
    "ChildCreate",
    "ChildUpdate",
    "ChildResponse",
    "UnitCreate",
    "UnitUpdate",
    "UnitResponse",
    "LessonCreate",
    "LessonUpdate",
    "LessonResponse",
    "ExerciseCreate",
    "ExerciseUpdate",
    "ExerciseResponse",
    "ExerciseSubmission",
    "ExerciseResultResponse",
    "LessonCompletionResponse",
    "BadgeCreate",
    "BadgeResponse",
    "ChildBadgeResponse",
    "NotificationResponse",
]
