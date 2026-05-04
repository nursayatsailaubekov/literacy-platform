"""Admin routes for monitoring and statistics."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from app.db.database import get_db
from app.models.user import User
from app.models.child import Child
from app.models.learning import ExerciseResult, LessonCompletion
from app.models.curriculum import Unit, Lesson, Exercise
from app.api.dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])


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


@router.get("/stats", response_model=PlatformStats)
def get_platform_stats(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """
    Get platform-wide statistics.
    Admin only.
    """
    # Count totals
    total_users = db.query(func.count(User.id)).scalar()
    total_children = db.query(func.count(Child.id)).scalar()
    total_units = db.query(func.count(Unit.id)).scalar()
    total_lessons = db.query(func.count(Lesson.id)).scalar()
    total_exercises = db.query(func.count(Exercise.id)).scalar()
    total_exercises_completed = db.query(func.count(ExerciseResult.id)).scalar()
    total_lessons_completed = db.query(func.count(LessonCompletion.id)).scalar()

    # Active users (children with activity in last N days)
    seven_days_ago = datetime.utcnow().date() - timedelta(days=7)
    thirty_days_ago = datetime.utcnow().date() - timedelta(days=30)

    active_7_days = db.query(func.count(func.distinct(Child.id))).filter(
        Child.last_activity_date >= seven_days_ago
    ).scalar()

    active_30_days = db.query(func.count(func.distinct(Child.id))).filter(
        Child.last_activity_date >= thirty_days_ago
    ).scalar()

    # Average XP
    avg_xp = db.query(func.avg(Child.xp)).scalar() or 0.0

    # Completion rate (lessons completed / total lessons)
    completion_rate = 0.0
    if total_lessons > 0 and total_children > 0:
        possible_completions = total_lessons * total_children
        completion_rate = (total_lessons_completed / possible_completions * 100) if possible_completions > 0 else 0

    # Accuracy rate (correct exercises / total exercises)
    correct_exercises = db.query(func.count(ExerciseResult.id)).filter(
        ExerciseResult.is_correct == True
    ).scalar()
    accuracy_rate = (correct_exercises / total_exercises_completed * 100) if total_exercises_completed > 0 else 0

    return PlatformStats(
        total_users=total_users,
        total_children=total_children,
        total_units=total_units,
        total_lessons=total_lessons,
        total_exercises=total_exercises,
        total_exercises_completed=total_exercises_completed,
        total_lessons_completed=total_lessons_completed,
        active_users_last_7_days=active_7_days,
        active_users_last_30_days=active_30_days,
        average_xp_per_child=round(avg_xp, 2),
        completion_rate=round(completion_rate, 2),
        accuracy_rate=round(accuracy_rate, 2)
    )


@router.get("/logs", response_model=list[ActivityLog])
def get_activity_logs(
    limit: int = Query(50, ge=1, le=500, description="Number of log entries to return"),
    child_id: Optional[int] = Query(None, description="Filter by child ID"),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """
    Get recent activity logs.
    Admin only.
    Shows exercise completions and lesson completions.
    """
    logs = []

    # Get exercise results
    query = db.query(ExerciseResult).join(Child)
    if child_id:
        query = query.filter(ExerciseResult.child_id == child_id)

    exercise_results = query.order_by(ExerciseResult.completed_at.desc()).limit(limit).all()

    for result in exercise_results:
        logs.append({
            "id": result.id,
            "child_id": result.child_id,
            "child_name": result.child.name,
            "activity_type": "exercise_completed",
            "details": f"Exercise #{result.exercise_id}: {'✓ Correct' if result.is_correct else '✗ Incorrect'} (+{result.xp_earned} XP)",
            "timestamp": result.completed_at
        })

    # Get lesson completions
    query = db.query(LessonCompletion).join(Child)
    if child_id:
        query = query.filter(LessonCompletion.child_id == child_id)

    lesson_completions = query.order_by(LessonCompletion.completed_at.desc()).limit(limit).all()

    for completion in lesson_completions:
        logs.append({
            "id": completion.id,
            "child_id": completion.child_id,
            "child_name": completion.child.name,
            "activity_type": "lesson_completed",
            "details": f"Lesson #{completion.lesson_id}: Score {completion.score}% (+{completion.xp_earned} XP)",
            "timestamp": completion.completed_at
        })

    # Sort by timestamp
    logs.sort(key=lambda x: x["timestamp"], reverse=True)

    return [ActivityLog(**log) for log in logs[:limit]]


@router.get("/users", response_model=list[dict])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """
    Get all users with pagination.
    Admin only.
    """
    users = db.query(User).offset(skip).limit(limit).all()

    result = []
    for user in users:
        children_count = db.query(func.count(Child.id)).filter(Child.parent_id == user.id).scalar()
        result.append({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value,
            "children_count": children_count,
            "created_at": user.created_at
        })

    return result
