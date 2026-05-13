from pydantic import BaseModel
from datetime import datetime

class PlatformStats(BaseModel):
    """Schema for platform-wide statistics."""
    total_users: int
    total_children: int
    total_units: int
    total_lessons: int
    total_exercises: int
    total_exercises_completed: int
    total_lessons_completed: int
    active_users_last_7_days: int
    active_users_last_30_days: int
    average_xp_per_child: float
    completion_rate: float
    accuracy_rate: float


class ActivityLog(BaseModel):
    """Schema for activity log entry."""
    id: int
    child_id: int
    child_name: str
    activity_type: str
    details: str
    timestamp: datetime

    class Config:
        from_attributes = True