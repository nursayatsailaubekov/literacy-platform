"""Seed the database with initial data for testing."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.db.database import Base
from app.models import *
from app.repositories.user_repository import UserRepository
from app.repositories.curriculum_repository import UnitRepository, LessonRepository, ExerciseRepository
from app.repositories.gamification_repository import BadgeRepository
from app.core.security import hash_password
from app.schemas.curriculum import UnitCreate, LessonCreate, ExerciseCreate
from app.schemas.gamification import BadgeCreate


def create_admin_user(db: Session):
    """Create an admin user."""
    existing = UserRepository.get_by_email(db, "admin@literacy.com")
    if existing:
        print("Admin user already exists")
        return existing

    admin = UserRepository.create(
        db=db,
        email="admin@literacy.com",
        hashed_password=hash_password("Admin123!"),
        full_name="Admin User",
        role="admin"
    )
    print(f"Created admin user: admin@literacy.com / Admin123!")
    return admin


def create_sample_parent(db: Session):
    """Create a sample parent user."""
    existing = UserRepository.get_by_email(db, "parent@example.com")
    if existing:
        print("Sample parent already exists")
        return existing

    parent = UserRepository.create(
        db=db,
        email="parent@example.com",
        hashed_password=hash_password("Parent123!"),
        full_name="Sample Parent",
    )
    print(f"Created sample parent: parent@example.com / Parent123!")
    return parent


def create_curriculum(db: Session):
    """Create sample curriculum."""
    unit_data = UnitCreate(
        title="Letters & Sounds",
        description="Learn the alphabet and phonics",
        order_index=1,
        is_published=True
    )
    unit = UnitRepository.create(db, unit_data)
    print(f"Created unit: {unit.title}")

    lesson_data = LessonCreate(
        unit_id=unit.id,
        title="Letter A",
        description="Learn the letter A and its sound",
        order_index=1,
        is_published=True
    )
    lesson = LessonRepository.create(db, lesson_data)
    print(f"Created lesson: {lesson.title}")

    exercises = [
        ExerciseCreate(
            lesson_id=lesson.id,
            type="multiple_choice",
            question="Which letter makes the 'ah' sound?",
            content={
                "options": ["A", "B", "C"],
                "instruction": "Choose the correct letter"
            },
            correct_answer={"answer": "A"},
            order_index=1,
            xp_value=10
        ),
        ExerciseCreate(
            lesson_id=lesson.id,
            type="fill_blank",
            question="A is for ___",
            content={
                "options": ["Apple", "Banana", "Cat"],
                "instruction": "Complete the sentence"
            },
            correct_answer={"answer": "Apple"},
            order_index=2,
            xp_value=10
        )
    ]

    for ex_data in exercises:
        exercise = ExerciseRepository.create(db, ex_data)
        print(f"Created exercise: {exercise.question}")

    return unit


def create_badges(db: Session):
    """Create sample badges."""
    badges = [
        BadgeCreate(
            name="First Steps",
            description="Earn your first 50 XP",
            icon="🌟",
            criteria_type="xp",
            criteria_value=50
        ),
        BadgeCreate(
            name="Rising Star",
            description="Reach 100 XP",
            icon="⭐",
            criteria_type="xp",
            criteria_value=100
        ),
        BadgeCreate(
            name="Streak Master",
            description="Maintain a 7-day learning streak",
            icon="🔥",
            criteria_type="streak",
            criteria_value=7
        ),
        BadgeCreate(
            name="Level Up!",
            description="Reach level 5",
            icon="🏆",
            criteria_type="level",
            criteria_value=5
        )
    ]

    for badge_data in badges:
        badge = BadgeRepository.create(db, badge_data)
        print(f"Created badge: {badge.name}")


def main():
    """Run all seed functions."""
    print("Seeding database...")

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        create_admin_user(db)
        create_sample_parent(db)
        create_curriculum(db)
        create_badges(db)
        print("\nDatabase seeded successfully!")
        print("\nLogin credentials:")
        print("Admin: admin@literacy.com / Admin123!")
        print("Parent: parent@example.com / Parent123!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
