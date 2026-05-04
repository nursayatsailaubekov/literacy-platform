"""Notification repository for database operations."""
from sqlalchemy.orm import Session
from app.models.notification import Notification


class NotificationRepository:
    """Repository for Notification model operations."""

    @staticmethod
    def create(db: Session, child_id: int, type: str, title: str, message: str) -> Notification:
        """Create a new notification."""
        notification = Notification(
            child_id=child_id,
            type=type,
            title=title,
            message=message,
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def get_by_child(db: Session, child_id: int, unread_only: bool = False) -> list[Notification]:
        """Get all notifications for a child."""
        query = db.query(Notification).filter(Notification.child_id == child_id)
        if unread_only:
            query = query.filter(Notification.is_read == False)
        return query.order_by(Notification.created_at.desc()).all()

    @staticmethod
    def mark_as_read(db: Session, notification_id: int) -> None:
        """Mark a notification as read."""
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if notification:
            notification.is_read = True
            db.commit()

    @staticmethod
    def mark_all_as_read(db: Session, child_id: int) -> None:
        """Mark all notifications for a child as read."""
        db.query(Notification).filter(Notification.child_id == child_id).update({"is_read": True})
        db.commit()
