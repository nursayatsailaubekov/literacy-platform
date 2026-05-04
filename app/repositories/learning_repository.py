"""Learning progress repository for database operations."""
from sqlalchemy.orm import Session
from typing import Optional
from app.models.learning import ExerciseResult, LessonCompletion


class ExerciseResultRepository:
    """Repository for ExerciseResult model operations."""

    @staticmethod
    def create(
        db: Session,
        child_id: int,
        exercise_id: int,
        is_correct: bool,
        submitted_answer: dict,
        xp_earned: int,
    ) -> ExerciseResult:
        """Create a new exercise result."""
        result = ExerciseResult(
            child_id=child_id,
            exercise_id=exercise_id,
            is_correct=is_correct,
            submitted_answer=submitted_answer,
            xp_earned=xp_earned,
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        return result

    @staticmethod
    def get_by_child(db: Session, child_id: int) -> list[ExerciseResult]:
        """Get all exercise results for a child."""
        return db.query(ExerciseResult).filter(ExerciseResult.child_id == child_id).all()

    @staticmethod
    def get_by_exercise(db: Session, exercise_id: int) -> list[ExerciseResult]:
        """Get all results for an exercise."""
        return db.query(ExerciseResult).filter(ExerciseResult.exercise_id == exercise_id).all()


class LessonCompletionRepository:
    """Repository for LessonCompletion model operations."""

    @staticmethod
    def create(
        db: Session,
        child_id: int,
        lesson_id: int,
        score: int,
        xp_earned: int,
    ) -> LessonCompletion:
        """Create a new lesson completion."""
        completion = LessonCompletion(
            child_id=child_id,
            lesson_id=lesson_id,
            score=score,
            xp_earned=xp_earned,
        )
        db.add(completion)
        db.commit()
        db.refresh(completion)
        return completion

    @staticmethod
    def get_by_child(db: Session, child_id: int) -> list[LessonCompletion]:
        """Get all lesson completions for a child."""
        return db.query(LessonCompletion).filter(LessonCompletion.child_id == child_id).all()

    @staticmethod
    def get_by_lesson(db: Session, lesson_id: int) -> list[LessonCompletion]:
        """Get all completions for a lesson."""
        return db.query(LessonCompletion).filter(LessonCompletion.lesson_id == lesson_id).all()

    @staticmethod
    def check_completed(db: Session, child_id: int, lesson_id: int) -> Optional[LessonCompletion]:
        """Check if a child has completed a specific lesson."""
        return (
            db.query(LessonCompletion)
            .filter(LessonCompletion.child_id == child_id, LessonCompletion.lesson_id == lesson_id)
            .first()
        )
