"""Notification routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.repositories.notification_repository import NotificationRepository
from app.schemas.notification import NotificationResponse
from app.services.child_service import ChildService
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/children/{child_id}", response_model=list[NotificationResponse])
def get_notifications(
    child_id: int,
    unread_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get notifications for a child."""
    ChildService.verify_child_ownership(db, child_id, current_user.id)
    notifications = NotificationRepository.get_by_child(db, child_id, unread_only)
    return [NotificationResponse.model_validate(n) for n in notifications]


@router.put("/{notification_id}/read", status_code=204)
def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a notification as read."""
    NotificationRepository.mark_as_read(db, notification_id)


@router.put("/children/{child_id}/read-all", status_code=204)
def mark_all_notifications_read(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark all notifications for a child as read."""
    ChildService.verify_child_ownership(db, child_id, current_user.id)
    NotificationRepository.mark_all_as_read(db, child_id)
