"""Child profile routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.child import ChildCreate, ChildUpdate, ChildResponse
from app.services.child_service import ChildService
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/children", tags=["Children"])


@router.post("", response_model=ChildResponse, status_code=201)
def create_child(
    child_data: ChildCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new child profile."""
    return ChildService.create_child(db, current_user.id, child_data)


@router.get("", response_model=list[ChildResponse])
def get_children(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all children for the current user."""
    return ChildService.get_children(db, current_user.id)


@router.get("/{child_id}", response_model=ChildResponse)
def get_child(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific child."""
    return ChildService.get_child(db, child_id, current_user.id)


@router.put("/{child_id}", response_model=ChildResponse)
def update_child(
    child_id: int,
    child_data: ChildUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a child profile."""
    return ChildService.update_child(db, child_id, current_user.id, child_data)


@router.delete("/{child_id}", status_code=204)
def delete_child(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a child profile."""
    ChildService.delete_child(db, child_id, current_user.id)
