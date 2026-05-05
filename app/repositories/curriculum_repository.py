"""Curriculum repository for database operations."""
import math
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from app.models.curriculum import Unit, Lesson, Exercise
from app.schemas.curriculum import (
    UnitCreate,
    UnitUpdate,
    LessonCreate,
    LessonUpdate,
    ExerciseCreate,
    ExerciseUpdate,
)


class UnitRepository:
    """Repository for Unit model operations."""

    @staticmethod
    def create(db: Session, unit_data: UnitCreate) -> Unit:
        """Create a new unit."""
        unit = Unit(**unit_data.model_dump())
        db.add(unit)
        db.commit()
        db.refresh(unit)
        return unit

    @staticmethod
    def get_by_id(db: Session, unit_id: int) -> Optional[Unit]:
        """Get unit by ID."""
        return db.query(Unit).filter(Unit.id == unit_id).first()

    @staticmethod
    def get_all(db: Session, published_only: bool = False) -> list[Unit]:
        """Get all units."""
        query = db.query(Unit).order_by(Unit.order_index)
        if published_only:
            query = query.filter(Unit.is_published == True)
        return query.all()

    @staticmethod
    def update(db: Session, unit: Unit, unit_data: UnitUpdate) -> Unit:
        """Update a unit."""
        update_data = unit_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(unit, field, value)
        db.commit()
        db.refresh(unit)
        return unit

    @staticmethod
    def delete(db: Session, unit: Unit) -> None:
        """Delete a unit."""
        db.delete(unit)
        db.commit()


class LessonRepository:
    """Repository for Lesson model operations."""

    @staticmethod
    def create(db: Session, lesson_data: LessonCreate) -> Lesson:
        """Create a new lesson."""
        lesson = Lesson(**lesson_data.model_dump())
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson

    @staticmethod
    def get_by_id(db: Session, lesson_id: int) -> Optional[Lesson]:
        """Get lesson by ID with eager loading of exercises."""
        return (
            db.query(Lesson)
            .options(joinedload(Lesson.exercises))
            .filter(Lesson.id == lesson_id)
            .first()
        )

    @staticmethod
    def get_by_unit(db: Session, unit_id: int, published_only: bool = False) -> list[Lesson]:
        """Get all lessons for a unit with eager loading."""
        query = (
            db.query(Lesson)
            .options(joinedload(Lesson.exercises))
            .filter(Lesson.unit_id == unit_id)
            .order_by(Lesson.order_index)
        )
        if published_only:
            query = query.filter(Lesson.is_published == True)
        return query.all()

    @staticmethod
    def update(db: Session, lesson: Lesson, lesson_data: LessonUpdate) -> Lesson:
        """Update a lesson."""
        update_data = lesson_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(lesson, field, value)
        db.commit()
        db.refresh(lesson)
        return lesson

    @staticmethod
    def delete(db: Session, lesson: Lesson) -> None:
        """Delete a lesson."""
        db.delete(lesson)
        db.commit()
    
    @staticmethod
    def get_by_order(db: Session, unit_id: int, order_index: int):
        return (
            db.query(Lesson)
            .filter(
                Lesson.unit_id == unit_id,
                Lesson.order_index == order_index 
            )
            .first()
        )
    
    @staticmethod
    def get_by_unit_paginated(
        db: Session, 
        unit_id: int, 
        page: int = 1, 
        page_size: int = 10, 
        published_only: bool = False
    ) -> tuple[list[Lesson], int]:
        """Get lessons for a unit with eager loading and pagination metadata."""
        query = db.query(Lesson).filter(Lesson.unit_id == unit_id)
        
        if published_only:
            query = query.filter(Lesson.is_published == True)
            
        total = query.count()
        
        offset = (page - 1) * page_size
        items = (
            query.options(joinedload(Lesson.exercises)) 
            .order_by(Lesson.order_index)
            .offset(offset)
            .limit(page_size)
            .all()
        )
        
        return items, total


class ExerciseRepository:
    """Repository for Exercise model operations."""

    @staticmethod
    def create(db: Session, exercise_data: ExerciseCreate) -> Exercise:
        """Create a new exercise."""
        exercise = Exercise(**exercise_data.model_dump())
        db.add(exercise)
        db.commit()
        db.refresh(exercise)
        return exercise

    @staticmethod
    def get_by_id(db: Session, exercise_id: int) -> Optional[Exercise]:
        """Get exercise by ID."""
        return db.query(Exercise).filter(Exercise.id == exercise_id).first()

    @staticmethod
    def get_by_lesson(db: Session, lesson_id: int) -> list[Exercise]:
        """Get all exercises for a lesson."""
        return db.query(Exercise).filter(Exercise.lesson_id == lesson_id).order_by(Exercise.order_index).all()

    @staticmethod
    def update(db: Session, exercise: Exercise, exercise_data: ExerciseUpdate) -> Exercise:
        """Update an exercise."""
        update_data = exercise_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(exercise, field, value)
        db.commit()
        db.refresh(exercise)
        return exercise

    @staticmethod
    def delete(db: Session, exercise: Exercise) -> None:
        """Delete an exercise."""
        db.delete(exercise)
        db.commit()
