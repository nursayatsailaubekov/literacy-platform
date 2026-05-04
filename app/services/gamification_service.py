"""Gamification service with business logic."""
from sqlalchemy.orm import Session
from app.repositories.gamification_repository import BadgeRepository, ChildBadgeRepository
from app.repositories.child_repository import ChildRepository
from app.repositories.notification_repository import NotificationRepository
from app.schemas.gamification import BadgeCreate, BadgeResponse, ChildBadgeResponse


class GamificationService:
    """Service for gamification operations."""

    @staticmethod
    def create_badge(db: Session, badge_data: BadgeCreate) -> BadgeResponse:
        """Create a new badge."""
        badge = BadgeRepository.create(db, badge_data)
        return BadgeResponse.model_validate(badge)

    @staticmethod
    def get_all_badges(db: Session) -> list[BadgeResponse]:
        """Get all available badges."""
        badges = BadgeRepository.get_all(db)
        return [BadgeResponse.model_validate(badge) for badge in badges]

    @staticmethod
    def get_child_badges(db: Session, child_id: int) -> list[ChildBadgeResponse]:
        """Get all badges earned by a child."""
        child_badges = ChildBadgeRepository.get_by_child(db, child_id)
        return [ChildBadgeResponse.model_validate(cb) for cb in child_badges]

    @staticmethod
    def check_and_award_badges(db: Session, child_id: int) -> list[ChildBadgeResponse]:
        """Check if child qualifies for any badges and award them."""
        child = ChildRepository.get_by_id(db, child_id)
        if not child:
            return []

        all_badges = BadgeRepository.get_all(db)
        awarded_badges = []

        for badge in all_badges:
            already_awarded = ChildBadgeRepository.check_awarded(db, child_id, badge.id)
            if already_awarded:
                continue

            if GamificationService._check_badge_criteria(child, badge):
                child_badge = ChildBadgeRepository.award_badge(db, child_id, badge.id)
                awarded_badges.append(child_badge)

                NotificationRepository.create(
                    db=db,
                    child_id=child_id,
                    type="badge_earned",
                    title="New Badge Earned!",
                    message=f"Congratulations! You've earned the '{badge.name}' badge!",
                )

        if child.xp >= 100 * child.level:
            new_level = child.level + 1
            ChildRepository.update_level(db, child, new_level)

            NotificationRepository.create(
                db=db,
                child_id=child_id,
                type="level_up",
                title="Level Up!",
                message=f"Amazing! You've reached level {new_level}!",
            )

        return [ChildBadgeResponse.model_validate(cb) for cb in awarded_badges]

    @staticmethod
    def _check_badge_criteria(child, badge) -> bool:
        """Check if a child meets the criteria for a badge."""
        if badge.criteria_type == "xp":
            return child.xp >= badge.criteria_value
        elif badge.criteria_type == "streak":
            return child.streak_count >= badge.criteria_value
        elif badge.criteria_type == "level":
            return child.level >= badge.criteria_value
        return False
