"""Gamification schemas."""
from pydantic import BaseModel
from datetime import datetime


class BadgeCreate(BaseModel):
    """Schema for creating a badge."""
    name: str
    description: str
    icon: str
    criteria_type: str
    criteria_value: int


class BadgeResponse(BaseModel):
    """Schema for badge response."""
    id: int
    name: str
    description: str
    icon: str
    criteria_type: str
    criteria_value: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChildBadgeResponse(BaseModel):
    """Schema for child badge response."""
    id: int
    child_id: int
    badge: BadgeResponse
    earned_at: datetime

    class Config:
        from_attributes = True

class LeaderboardEntry(BaseModel):
    """Schema for leaderboard entry."""
    rank: int
    child_id: int
    name: str
    age: int
    level: int
    xp: int
    streak_count: int

    class Config:
        from_attributes = True