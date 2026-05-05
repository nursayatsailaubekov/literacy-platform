"""Curriculum routes (admin and public)."""
import math
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.learning import PaginatedResponse
from app.repositories.curriculum_repository import UnitRepository, LessonRepository, ExerciseRepository
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
    LessonResponse
)
from app.api.dependencies import require_admin, get_current_user
from app.models.user import User

router = APIRouter(prefix="/curriculum", tags=["Curriculum"])


@router.post("/units", response_model=UnitResponse, status_code=201)
def create_unit(
    unit_data: UnitCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new unit (admin only)."""
    return UnitRepository.create(db, unit_data)


@router.get("/units", response_model=list[UnitResponse])
def get_units(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all published units."""
    published_only = current_user.role.value != "admin"
    return UnitRepository.get_all(db, published_only=published_only)


@router.get("/units/{unit_id}", response_model=UnitResponse)
def get_unit(
    unit_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific unit."""
    return UnitRepository.get_by_id(db, unit_id)


@router.put("/units/{unit_id}", response_model=UnitResponse)
def update_unit(
    unit_id: int,
    unit_data: UnitUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update a unit (admin only)."""
    unit = UnitRepository.get_by_id(db, unit_id)
    return UnitRepository.update(db, unit, unit_data)


@router.delete("/units/{unit_id}", status_code=204)
def delete_unit(
    unit_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete a unit (admin only)."""
    unit = UnitRepository.get_by_id(db, unit_id)
    UnitRepository.delete(db, unit)


@router.post("/lessons", response_model=LessonResponse, status_code=201)
def create_lesson(
    lesson_data: LessonCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new lesson (admin only)."""
    return LessonRepository.create(db, lesson_data)

@router.get("/units/{unit_id}/lessons", response_model=PaginatedResponse[LessonResponse])
def get_lessons(
    unit_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    published_only = current_user.role.value != "admin"
    
    items, total = LessonRepository.get_by_unit_paginated(
        db, unit_id, page, page_size, published_only
    )
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size) if total > 0 else 0
    }


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
def get_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific lesson."""
    return LessonRepository.get_by_id(db, lesson_id)


@router.put("/lessons/{lesson_id}", response_model=LessonResponse)
def update_lesson(
    lesson_id: int,
    lesson_data: LessonUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update a lesson (admin only)."""
    lesson = LessonRepository.get_by_id(db, lesson_id)
    return LessonRepository.update(db, lesson, lesson_data)


@router.delete("/lessons/{lesson_id}", status_code=204)
def delete_lesson(
    lesson_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete a lesson (admin only)."""
    lesson = LessonRepository.get_by_id(db, lesson_id)
    LessonRepository.delete(db, lesson)


@router.post("/exercises", response_model=ExerciseResponse, status_code=201)
def create_exercise(
    exercise_data: ExerciseCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new exercise (admin only)."""
    return ExerciseRepository.create(db, exercise_data)


@router.get("/lessons/{lesson_id}/exercises", response_model=list[ExerciseResponse])
def get_exercises(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all exercises for a lesson."""
    return ExerciseRepository.get_by_lesson(db, lesson_id)


@router.put("/exercises/{exercise_id}", response_model=ExerciseResponse)
def update_exercise(
    exercise_id: int,
    exercise_data: ExerciseUpdate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update an exercise (admin only)."""
    exercise = ExerciseRepository.get_by_id(db, exercise_id)
    return ExerciseRepository.update(db, exercise, exercise_data)


@router.delete("/exercises/{exercise_id}", status_code=204)
def delete_exercise(
    exercise_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete an exercise (admin only)."""
    exercise = ExerciseRepository.get_by_id(db, exercise_id)
    ExerciseRepository.delete(db, exercise)
