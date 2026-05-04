"""Gamification routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.gamification import BadgeCreate, BadgeResponse, ChildBadgeResponse
from app.services.gamification_service import GamificationService
from app.services.child_service import ChildService
from app.api.dependencies import require_admin, get_current_user
from app.models.user import User

router = APIRouter(prefix="/gamification", tags=["Gamification"])


@router.post("/badges", response_model=BadgeResponse, status_code=201)
def create_badge(
    badge_data: BadgeCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new badge (admin only)."""
    return GamificationService.create_badge(db, badge_data)


@router.get("/badges", response_model=list[BadgeResponse])
def get_badges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all available badges."""
    return GamificationService.get_all_badges(db)


@router.get("/children/{child_id}/badges", response_model=list[ChildBadgeResponse])
def get_child_badges(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all badges earned by a child."""
    ChildService.verify_child_ownership(db, child_id, current_user.id)
    return GamificationService.get_child_badges(db, child_id)
