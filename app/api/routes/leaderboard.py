"""Leaderboard routes."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.db.database import get_db
from app.models.child import Child
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.gamification import LeaderboardEntry

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("", response_model=list[LeaderboardEntry])
def get_leaderboard(
    age_group: Optional[int] = Query(None, description="Filter by age (e.g., 5 for 5-year-olds)"),
    limit: int = Query(10, ge=1, le=100, description="Number of entries to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get XP leaderboard.
    Can be filtered by age group.
    Returns top performers sorted by XP.
    """
    query = db.query(Child)

    # Filter by age if specified
    if age_group is not None:
        query = query.filter(Child.age == age_group)

    # Order by XP descending
    children = query.order_by(Child.xp.desc()).limit(limit).all()

    # Build leaderboard with ranks
    leaderboard = []
    for rank, child in enumerate(children, start=1):
        leaderboard.append(
            LeaderboardEntry(
                rank=rank,
                child_id=child.id,
                name=child.name,
                age=child.age,
                level=child.level,
                xp=child.xp,
                streak_count=child.streak_count
            )
        )

    return leaderboard


@router.get("/child/{child_id}", response_model=dict)
def get_child_rank(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get a specific child's rank in the global leaderboard.
    """
    child = db.query(Child).filter(Child.id == child_id).first()
    if not child:
        return {"error": "Child not found"}

    # Count how many children have more XP
    rank = db.query(func.count(Child.id)).filter(Child.xp > child.xp).scalar() + 1

    # Total children count
    total = db.query(func.count(Child.id)).scalar()

    return {
        "child_id": child.id,
        "name": child.name,
        "rank": rank,
        "total_children": total,
        "xp": child.xp,
        "percentile": round((1 - (rank / total)) * 100, 2) if total > 0 else 0
    }
