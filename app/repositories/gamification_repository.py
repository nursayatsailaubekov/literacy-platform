"""Gamification repository for database operations."""
from sqlalchemy.orm import Session
from typing import Optional
from app.models.gamification import Badge, ChildBadge
from app.schemas.gamification import BadgeCreate


class BadgeRepository:
    """Repository for Badge model operations."""

    @staticmethod
    def create(db: Session, badge_data: BadgeCreate) -> Badge:
        """Create a new badge."""
        badge = Badge(**badge_data.model_dump())
        db.add(badge)
        db.commit()
        db.refresh(badge)
        return badge

    @staticmethod
    def get_by_id(db: Session, badge_id: int) -> Optional[Badge]:
        """Get badge by ID."""
        return db.query(Badge).filter(Badge.id == badge_id).first()

    @staticmethod
    def get_all(db: Session) -> list[Badge]:
        """Get all badges."""
        return db.query(Badge).all()

    @staticmethod
    def delete(db: Session, badge: Badge) -> None:
        """Delete a badge."""
        db.delete(badge)
        db.commit()


class ChildBadgeRepository:
    """Repository for ChildBadge model operations."""

    @staticmethod
    def award_badge(db: Session, child_id: int, badge_id: int) -> ChildBadge:
        """Award a badge to a child."""
        child_badge = ChildBadge(child_id=child_id, badge_id=badge_id)
        db.add(child_badge)
        db.commit()
        db.refresh(child_badge)
        return child_badge

    @staticmethod
    def get_by_child(db: Session, child_id: int) -> list[ChildBadge]:
        """Get all badges earned by a child."""
        return db.query(ChildBadge).filter(ChildBadge.child_id == child_id).all()

    @staticmethod
    def check_awarded(db: Session, child_id: int, badge_id: int) -> Optional[ChildBadge]:
        """Check if a child has already earned a specific badge."""
        return (
            db.query(ChildBadge)
            .filter(ChildBadge.child_id == child_id, ChildBadge.badge_id == badge_id)
            .first()
        )
