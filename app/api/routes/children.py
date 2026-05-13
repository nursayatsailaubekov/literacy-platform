"""Child profile routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.child import ChildCreate, ChildUpdate, ChildResponse, ChildProgress
from app.schemas.learning import ExerciseResultResponse, LessonCompletionResponse
from app.services.child_service import ChildService
from app.repositories.learning_repository import ExerciseResultRepository, LessonCompletionRepository
from app.repositories.gamification_repository import ChildBadgeRepository
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/children", tags=["Children"])

@router.post("", response_model=ChildResponse, status_code=201)
def create_child(
    child_data: ChildCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new child profile."""
    return ChildService.create_child(db, current_user.id, child_data)


@router.get("", response_model=list[ChildResponse])
def get_children(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all children for the current user."""
    return ChildService.get_children(db, current_user.id)


@router.get("/{child_id}", response_model=ChildResponse)
def get_child(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific child."""
    return ChildService.get_child(db, child_id, current_user.id)


@router.put("/{child_id}", response_model=ChildResponse)
def update_child(
    child_id: int,
    child_data: ChildUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a child profile."""
    return ChildService.update_child(db, child_id, current_user.id, child_data)


@router.delete("/{child_id}", status_code=204)
def delete_child(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a child profile."""
    ChildService.delete_child(db, child_id, current_user.id)


@router.get("/{child_id}/progress", response_model=ChildProgress)
def get_child_progress(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get full learning history for a child.
    Includes all exercise results, lesson completions, and statistics.
    """
    # Verify ownership
    child = ChildService.verify_child_ownership(db, child_id, current_user.id)

    # Get all exercise results
    exercise_results = ExerciseResultRepository.get_by_child(db, child_id)

    # Get all lesson completions
    lesson_completions = LessonCompletionRepository.get_by_child(db, child_id)

    # Get badges count
    badges = ChildBadgeRepository.get_by_child(db, child_id)

    # Calculate accuracy rate
    total_exercises = len(exercise_results)
    correct_exercises = sum(1 for r in exercise_results if r.is_correct)
    accuracy_rate = (correct_exercises / total_exercises * 100) if total_exercises > 0 else 0.0

    return ChildProgress(
        child_id=child.id,
        name=child.name,
        level=child.level,
        xp=child.xp,
        streak_count=child.streak_count,
        total_exercises_completed=total_exercises,
        total_lessons_completed=len(lesson_completions),
        total_badges_earned=len(badges),
        exercise_results=[ExerciseResultResponse.model_validate(r) for r in exercise_results],
        lesson_completions=[LessonCompletionResponse.model_validate(c) for c in lesson_completions],
        accuracy_rate=round(accuracy_rate, 2)
    )
