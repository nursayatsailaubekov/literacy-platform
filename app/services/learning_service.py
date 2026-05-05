"""Learning service with business logic."""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date
from app.repositories.learning_repository import ExerciseResultRepository, LessonCompletionRepository
from app.repositories.curriculum_repository import ExerciseRepository, LessonRepository
from app.repositories.child_repository import ChildRepository
from app.schemas.learning import ExerciseSubmission, ExerciseResultResponse, LessonCompletionResponse
from app.services.gamification_service import GamificationService
from app.core.config import settings


class LearningService:
    """Service for learning operations."""

    @staticmethod
    def submit_exercise(db: Session, child_id: int, submission: ExerciseSubmission) -> ExerciseResultResponse:
        """Submit an exercise answer and check correctness."""
        exercise = ExerciseRepository.get_by_id(db, submission.exercise_id)
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exercise not found",
            )

        is_correct = LearningService._check_answer(
            submission.submitted_answer,
            exercise.correct_answer,
        )

        xp_earned = exercise.xp_value if is_correct else 0

        result = ExerciseResultRepository.create(
            db=db,
            child_id=child_id,
            exercise_id=submission.exercise_id,
            is_correct=is_correct,
            submitted_answer=submission.submitted_answer,
            xp_earned=xp_earned,
        )

        if is_correct and xp_earned > 0:
            child = ChildRepository.get_by_id(db, child_id)
            ChildRepository.update_xp(db, child, xp_earned)
            LearningService._update_streak(db, child)
            GamificationService.check_and_award_badges(db, child_id)

        return ExerciseResultResponse.model_validate(result)

    @staticmethod
    def complete_lesson(db: Session, child_id: int, lesson_id: int) -> LessonCompletionResponse:
        """Mark a lesson as complete and award XP."""
        lesson = LessonRepository.get_by_id(db, lesson_id)
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found",
            )

        if lesson.order > 1:
            previous_lesson = LessonRepository.get_by_order(
                db, 
                unit_id=lesson.unit_id, 
                order=lesson.order - 1
            )
            if previous_lesson:
                is_prev_completed = LessonCompletionRepository.check_completed(
                    db, child_id, previous_lesson.id
                )
                if not is_prev_completed:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Please complete Lesson {lesson.order - 1} first",
                    )    

        already_completed = LessonCompletionRepository.check_completed(db, child_id, lesson_id)
        if already_completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Lesson already completed",
            )

        exercises = ExerciseRepository.get_by_lesson(db, lesson_id)
        child_results = ExerciseResultRepository.get_by_child(db, child_id)

        exercise_ids = {ex.id for ex in exercises}
        completed_exercise_ids = {
            res.exercise_id for res in child_results if res.exercise_id in exercise_ids
        }

        if len(completed_exercise_ids) < len(exercise_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not all exercises completed",
            )

        correct_count = sum(
            1 for res in child_results
            if res.exercise_id in exercise_ids and res.is_correct
        )
        score = int((correct_count / len(exercises)) * 100) if exercises else 0

        xp_earned = settings.XP_PER_LESSON

        completion = LessonCompletionRepository.create(
            db=db,
            child_id=child_id,
            lesson_id=lesson_id,
            score=score,
            xp_earned=xp_earned,
        )

        child = ChildRepository.get_by_id(db, child_id)
        ChildRepository.update_xp(db, child, xp_earned)
        GamificationService.check_and_award_badges(db, child_id)

        return LessonCompletionResponse.model_validate(completion)

    @staticmethod
    def _check_answer(submitted: dict, correct: dict) -> bool:
        """Compare submitted answer with correct answer."""
        return submitted == correct

    @staticmethod
    def _update_streak(db: Session, child) -> None:
        """Update child's learning streak."""
        today = date.today()

        if child.last_activity_date == today:
            return

        if child.last_activity_date and (today - child.last_activity_date).days == 1:
            ChildRepository.update_streak(db, child, child.streak_count + 1)
        elif child.last_activity_date and (today - child.last_activity_date).days > 1:
            ChildRepository.update_streak(db, child, 1)
        else:
            ChildRepository.update_streak(db, child, 1)

        child.last_activity_date = today
        db.commit()
