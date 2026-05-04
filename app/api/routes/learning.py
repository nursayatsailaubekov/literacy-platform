"""Learning progress routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.learning import ExerciseSubmission, ExerciseResultResponse, LessonCompletionResponse
from app.services.learning_service import LearningService
from app.services.child_service import ChildService
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/learning", tags=["Learning"])


@router.post("/children/{child_id}/exercises", response_model=ExerciseResultResponse)
def submit_exercise(
    child_id: int,
    submission: ExerciseSubmission,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Submit an exercise answer for a child."""
    ChildService.verify_child_ownership(db, child_id, current_user.id)
    return LearningService.submit_exercise(db, child_id, submission)


@router.post("/children/{child_id}/lessons/{lesson_id}/complete", response_model=LessonCompletionResponse)
def complete_lesson(
    child_id: int,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a lesson as complete for a child."""
    ChildService.verify_child_ownership(db, child_id, current_user.id)
    return LearningService.complete_lesson(db, child_id, lesson_id)
