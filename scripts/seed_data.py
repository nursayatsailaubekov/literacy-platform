"""Seed the database with comprehensive initial data for testing."""
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
        print("✓ Admin user already exists")
        return existing

    admin = UserRepository.create(
        db=db,
        email="admin@literacy.com",
        hashed_password=hash_password("Admin123!"),
        full_name="Admin User",
        role="admin"
    )
    print(f"✓ Created admin: admin@literacy.com / Admin123!")
    return admin


def create_sample_parent(db: Session):
    """Create a sample parent user."""
    existing = UserRepository.get_by_email(db, "parent@example.com")
    if existing:
        print("✓ Sample parent already exists")
        return existing

    parent = UserRepository.create(
        db=db,
        email="parent@example.com",
        hashed_password=hash_password("Parent123!"),
        full_name="Sample Parent",
    )
    print(f"✓ Created parent: parent@example.com / Parent123!")
    return parent


def create_comprehensive_curriculum(db: Session):
    """Create comprehensive curriculum with multiple units, lessons, and exercises."""

    # UNIT 1: Letters & Sounds
    unit1 = UnitRepository.create(db, UnitCreate(
        title="Letters & Sounds",
        description="Learn the alphabet and phonics",
        order_index=1,
        is_published=True
    ))
    print(f"✓ Created unit: {unit1.title}")

    # Lessons for Unit 1
    lessons_unit1 = [
        ("Letter A", "Learn the letter A and its sound", 1),
        ("Letter B", "Learn the letter B and its sound", 2),
        ("Letter C", "Learn the letter C and its sound", 3),
        ("Letter D", "Learn the letter D and its sound", 4),
        ("Letter E", "Learn the letter E and its sound", 5),
    ]

    for title, desc, order in lessons_unit1:
        lesson = LessonRepository.create(db, LessonCreate(
            unit_id=unit1.id,
            title=title,
            description=desc,
            order_index=order,
            is_published=True
        ))
        print(f"  ✓ Created lesson: {lesson.title}")

        # Add exercises for each lesson
        letter = title.split()[-1]  # Extract letter
        exercises = [
            ExerciseCreate(
                lesson_id=lesson.id,
                type="multiple_choice",
                question=f"Which letter makes the '{letter.lower()}' sound?",
                content={
                    "options": [letter, "Z", "X"],
                    "instruction": "Choose the correct letter"
                },
                correct_answer={"answer": letter},
                order_index=1,
                xp_value=10
            ),
            ExerciseCreate(
                lesson_id=lesson.id,
                type="fill_blank",
                question=f"{letter} is for ___",
                content={
                    "options": [f"{letter}pple" if letter == "A" else f"{letter}all", "Cat", "Dog"],
                    "instruction": "Complete the word"
                },
                correct_answer={"answer": f"{letter}pple" if letter == "A" else f"{letter}all"},
                order_index=2,
                xp_value=15
            ),
            ExerciseCreate(
                lesson_id=lesson.id,
                type="matching",
                question=f"Match the letter {letter} with its sound",
                content={
                    "pairs": [[letter, f"{letter.lower()}-sound"], ["Z", "z-sound"]],
                    "instruction": "Draw lines to match"
                },
                correct_answer={"matches": {letter: f"{letter.lower()}-sound"}},
                order_index=3,
                xp_value=20
            )
        ]

        for ex_data in exercises:
            exercise = ExerciseRepository.create(db, ex_data)

    # UNIT 2: Simple Words
    unit2 = UnitRepository.create(db, UnitCreate(
        title="Simple Words",
        description="Build your first words",
        order_index=2,
        is_published=True
    ))
    print(f"✓ Created unit: {unit2.title}")

    lessons_unit2 = [
        ("CAT Family", "Learn words like cat, bat, rat", 1),
        ("DOG Family", "Learn words like dog, log, fog", 2),
        ("PIG Family", "Learn words like pig, big, dig", 3),
    ]

    for title, desc, order in lessons_unit2:
        lesson = LessonRepository.create(db, LessonCreate(
            unit_id=unit2.id,
            title=title,
            description=desc,
            order_index=order,
            is_published=True
        ))
        print(f"  ✓ Created lesson: {lesson.title}")

        # Exercises
        family = title.split()[0].lower()
        exercises = [
            ExerciseCreate(
                lesson_id=lesson.id,
                type="multiple_choice",
                question=f"Which word rhymes with {family}?",
                content={
                    "options": [f"b{family[1:]}", "house", "tree"],
                    "instruction": "Choose the rhyming word"
                },
                correct_answer={"answer": f"b{family[1:]}"},
                order_index=1,
                xp_value=10
            ),
            ExerciseCreate(
                lesson_id=lesson.id,
                type="fill_blank",
                question=f"The ___ says meow" if family == "cat" else f"The ___ barks",
                content={
                    "options": [family, "bird", "fish"],
                    "instruction": "Fill in the blank"
                },
                correct_answer={"answer": family},
                order_index=2,
                xp_value=15
            )
        ]

        for ex_data in exercises:
            ExerciseRepository.create(db, ex_data)

    # UNIT 3: Reading Comprehension
    unit3 = UnitRepository.create(db, UnitCreate(
        title="Reading Comprehension",
        description="Understand short sentences and stories",
        order_index=3,
        is_published=True
    ))
    print(f"✓ Created unit: {unit3.title}")

    lessons_unit3 = [
        ("Simple Sentences", "Read and understand simple sentences", 1),
        ("Short Stories", "Read short 2-3 sentence stories", 2),
        ("Questions & Answers", "Answer questions about what you read", 3),
    ]

    for title, desc, order in lessons_unit3:
        lesson = LessonRepository.create(db, LessonCreate(
            unit_id=unit3.id,
            title=title,
            description=desc,
            order_index=order,
            is_published=True
        ))
        print(f"  ✓ Created lesson: {lesson.title}")

        exercises = [
            ExerciseCreate(
                lesson_id=lesson.id,
                type="multiple_choice",
                question="The cat sat on the mat. Where is the cat?",
                content={
                    "options": ["On the mat", "Under the bed", "In the tree"],
                    "instruction": "Choose the correct answer"
                },
                correct_answer={"answer": "On the mat"},
                order_index=1,
                xp_value=20
            ),
            ExerciseCreate(
                lesson_id=lesson.id,
                type="true_false",
                question="Tom has a red ball. Is Tom's ball blue?",
                content={
                    "options": ["True", "False"],
                    "instruction": "Choose true or false"
                },
                correct_answer={"answer": "False"},
                order_index=2,
                xp_value=15
            )
        ]

        for ex_data in exercises:
            ExerciseRepository.create(db, ex_data)

    # UNIT 4: Numbers & Counting
    unit4 = UnitRepository.create(db, UnitCreate(
        title="Numbers & Counting",
        description="Learn numbers 1-20 and basic counting",
        order_index=4,
        is_published=True
    ))
    print(f"✓ Created unit: {unit4.title}")

    lessons_unit4 = [
        ("Numbers 1-5", "Count from 1 to 5", 1),
        ("Numbers 6-10", "Count from 6 to 10", 2),
        ("Numbers 11-20", "Count from 11 to 20", 3),
    ]

    for title, desc, order in lessons_unit4:
        lesson = LessonRepository.create(db, LessonCreate(
            unit_id=unit4.id,
            title=title,
            description=desc,
            order_index=order,
            is_published=True
        ))
        print(f"  ✓ Created lesson: {lesson.title}")

        exercises = [
            ExerciseCreate(
                lesson_id=lesson.id,
                type="multiple_choice",
                question="What number comes after 5?" if order == 1 else "What number comes after 10?",
                content={
                    "options": ["6", "4", "8"] if order == 1 else ["11", "9", "12"],
                    "instruction": "Choose the correct number"
                },
                correct_answer={"answer": "6" if order == 1 else "11"},
                order_index=1,
                xp_value=10
            )
        ]

        for ex_data in exercises:
            ExerciseRepository.create(db, ex_data)

    # UNIT 5: Colors & Shapes
    unit5 = UnitRepository.create(db, UnitCreate(
        title="Colors & Shapes",
        description="Recognize colors and basic shapes",
        order_index=5,
        is_published=True
    ))
    print(f"✓ Created unit: {unit5.title}")

    lessons_unit5 = [
        ("Primary Colors", "Learn red, blue, and yellow", 1),
        ("Basic Shapes", "Learn circle, square, and triangle", 2),
        ("Mixing Colors", "Understand color combinations", 3),
    ]

    for title, desc, order in lessons_unit5:
        lesson = LessonRepository.create(db, LessonCreate(
            unit_id=unit5.id,
            title=title,
            description=desc,
            order_index=order,
            is_published=True
        ))
        print(f"  ✓ Created lesson: {lesson.title}")

        exercises = [
            ExerciseCreate(
                lesson_id=lesson.id,
                type="multiple_choice",
                question="What color is the sun?",
                content={
                    "options": ["Yellow", "Blue", "Green"],
                    "instruction": "Choose the correct color"
                },
                correct_answer={"answer": "Yellow"},
                order_index=1,
                xp_value=10
            )
        ]

        for ex_data in exercises:
            ExerciseRepository.create(db, ex_data)

    return [unit1, unit2, unit3, unit4, unit5]


def create_comprehensive_badges(db: Session):
    """Create comprehensive badge system."""
    badges = [
        # XP Badges
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
            name="Super Learner",
            description="Reach 250 XP",
            icon="🚀",
            criteria_type="xp",
            criteria_value=250
        ),
        BadgeCreate(
            name="Literacy Master",
            description="Reach 500 XP",
            icon="👑",
            criteria_type="xp",
            criteria_value=500
        ),
        BadgeCreate(
            name="Reading Champion",
            description="Reach 1000 XP",
            icon="🏆",
            criteria_type="xp",
            criteria_value=1000
        ),
        # Streak Badges
        BadgeCreate(
            name="3-Day Streak",
            description="Learn for 3 days in a row",
            icon="🔥",
            criteria_type="streak",
            criteria_value=3
        ),
        BadgeCreate(
            name="Week Warrior",
            description="Maintain a 7-day learning streak",
            icon="💪",
            criteria_type="streak",
            criteria_value=7
        ),
        BadgeCreate(
            name="Month Master",
            description="Maintain a 30-day learning streak",
            icon="📅",
            criteria_type="streak",
            criteria_value=30
        ),
        # Level Badges
        BadgeCreate(
            name="Level 3 Achieved",
            description="Reach level 3",
            icon="🥉",
            criteria_type="level",
            criteria_value=3
        ),
        BadgeCreate(
            name="Level 5 Achieved",
            description="Reach level 5",
            icon="🥈",
            criteria_type="level",
            criteria_value=5
        ),
        BadgeCreate(
            name="Level 10 Achieved",
            description="Reach level 10",
            icon="🥇",
            criteria_type="level",
            criteria_value=10
        ),
    ]

    for badge_data in badges:
        badge = BadgeRepository.create(db, badge_data)
        print(f"✓ Created badge: {badge.name}")


def main():
    if db.query(Unit).count() > 0:
        return
    """Run all seed functions."""
    print("=" * 60)
    print("SEEDING DATABASE WITH COMPREHENSIVE DATA")
    print("=" * 60)

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print("\n[1/4] Creating Users...")
        create_admin_user(db)
        create_sample_parent(db)

        print("\n[2/4] Creating Curriculum (5 Units, ~20 Lessons, ~50+ Exercises)...")
        create_comprehensive_curriculum(db)

        print("\n[3/4] Creating Badges (11 Achievements)...")
        create_comprehensive_badges(db)

        print("\n" + "=" * 60)
        print("DATABASE SEEDED SUCCESSFULLY!")
        print("=" * 60)
        print("\n📧 Login Credentials:")
        print("   Admin:  admin@literacy.com / Admin123!")
        print("   Parent: parent@example.com / Parent123!")
        print("\n📚 Curriculum Created:")
        print("   • 5 Units")
        print("   • ~20 Lessons")
        print("   • ~50+ Exercises")
        print("\n🏅 Badges Created:")
        print("   • 5 XP-based badges")
        print("   • 3 Streak-based badges")
        print("   • 3 Level-based badges")
        print("\n🚀 Ready to use!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
