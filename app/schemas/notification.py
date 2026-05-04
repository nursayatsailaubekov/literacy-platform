"""Notification schemas."""
from pydantic import BaseModel
from datetime import datetime


class NotificationResponse(BaseModel):
    """Schema for notification response."""
    id: int
    child_id: int
    type: str
    title: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
