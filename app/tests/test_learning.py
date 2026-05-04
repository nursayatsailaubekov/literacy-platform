"""Tests for learning service."""
import pytest
from sqlalchemy.orm import Session
from app.services.learning_service import LearningService
from app.repositories.user_repository import UserRepository
from app.repositories.child_repository import ChildRepository
from app.repositories.curriculum_repository import UnitRepository, LessonRepository, ExerciseRepository
from app.schemas.child import ChildCreate
from app.schemas.curriculum import UnitCreate, LessonCreate, ExerciseCreate
from app.schemas.learning import ExerciseSubmission
from app.core.security import hash_password


def test_submit_correct_exercise(db: Session):
    """Test submitting a correct exercise answer."""
    user = UserRepository.create(
        db, "test@example.com", hash_password("password"), "Test User"
    )
    child_data = ChildCreate(name="Test Child", age=5)
    child = ChildRepository.create(db, user.id, child_data)

    unit_data = UnitCreate(title="Unit 1", order_index=1, is_published=True)
    unit = UnitRepository.create(db, unit_data)

    lesson_data = LessonCreate(
        unit_id=unit.id, title="Lesson 1", order_index=1, is_published=True
    )
    lesson = LessonRepository.create(db, lesson_data)

    exercise_data = ExerciseCreate(
        lesson_id=lesson.id,
        type="multiple_choice",
        question="What is 2 + 2?",
        content={"options": ["3", "4", "5"]},
        correct_answer={"answer": "4"},
        order_index=1,
        xp_value=10,
    )
    exercise = ExerciseRepository.create(db, exercise_data)

    submission = ExerciseSubmission(
        exercise_id=exercise.id,
        submitted_answer={"answer": "4"}
    )

    result = LearningService.submit_exercise(db, child.id, submission)

    assert result.is_correct is True
    assert result.xp_earned == 10

    updated_child = ChildRepository.get_by_id(db, child.id)
    assert updated_child.xp == 10


def test_submit_incorrect_exercise(db: Session):
    """Test submitting an incorrect exercise answer."""
    user = UserRepository.create(
        db, "test@example.com", hash_password("password"), "Test User"
    )
    child_data = ChildCreate(name="Test Child", age=5)
    child = ChildRepository.create(db, user.id, child_data)

    unit_data = UnitCreate(title="Unit 1", order_index=1, is_published=True)
    unit = UnitRepository.create(db, unit_data)

    lesson_data = LessonCreate(
        unit_id=unit.id, title="Lesson 1", order_index=1, is_published=True
    )
    lesson = LessonRepository.create(db, lesson_data)

    exercise_data = ExerciseCreate(
        lesson_id=lesson.id,
        type="multiple_choice",
        question="What is 2 + 2?",
        content={"options": ["3", "4", "5"]},
        correct_answer={"answer": "4"},
        order_index=1,
        xp_value=10,
    )
    exercise = ExerciseRepository.create(db, exercise_data)

    submission = ExerciseSubmission(
        exercise_id=exercise.id,
        submitted_answer={"answer": "5"}
    )

    result = LearningService.submit_exercise(db, child.id, submission)

    assert result.is_correct is False
    assert result.xp_earned == 0

    updated_child = ChildRepository.get_by_id(db, child.id)
    assert updated_child.xp == 0
