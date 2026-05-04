"""Child repository for database operations."""
from sqlalchemy.orm import Session
from typing import Optional
from app.models.child import Child
from app.schemas.child import ChildCreate, ChildUpdate


class ChildRepository:
    """Repository for Child model operations."""

    @staticmethod
    def create(db: Session, parent_id: int, child_data: ChildCreate) -> Child:
        """Create a new child profile."""
        child = Child(
            parent_id=parent_id,
            **child_data.model_dump()
        )
        db.add(child)
        db.commit()
        db.refresh(child)
        return child

    @staticmethod
    def get_by_id(db: Session, child_id: int) -> Optional[Child]:
        """Get child by ID."""
        return db.query(Child).filter(Child.id == child_id).first()

    @staticmethod
    def get_by_parent(db: Session, parent_id: int) -> list[Child]:
        """Get all children for a parent."""
        return db.query(Child).filter(Child.parent_id == parent_id).all()

    @staticmethod
    def update(db: Session, child: Child, child_data: ChildUpdate) -> Child:
        """Update a child profile."""
        update_data = child_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(child, field, value)
        db.commit()
        db.refresh(child)
        return child

    @staticmethod
    def delete(db: Session, child: Child) -> None:
        """Delete a child profile."""
        db.delete(child)
        db.commit()

    @staticmethod
    def update_xp(db: Session, child: Child, xp_to_add: int) -> Child:
        """Add XP to a child."""
        child.xp += xp_to_add
        db.commit()
        db.refresh(child)
        return child

    @staticmethod
    def update_streak(db: Session, child: Child, streak_count: int) -> Child:
        """Update child's streak count."""
        child.streak_count = streak_count
        db.commit()
        db.refresh(child)
        return child

    @staticmethod
    def update_level(db: Session, child: Child, level: int) -> Child:
        """Update child's level."""
        child.level = level
        db.commit()
        db.refresh(child)
        return child
