"""Parent profile routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.child import ChildResponse
from app.repositories.user_repository import UserRepository
from app.repositories.child_repository import ChildRepository
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.parent import UserUpdate

router = APIRouter(prefix="/parents", tags=["Parents"])


@router.get("/{parent_id}", response_model=UserResponse)
def get_parent(
    parent_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get parent profile by ID.
    Parents can only view their own profile unless they are admin.
    """
    if current_user.role.value != "admin" and current_user.id != parent_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own profile"
        )

    parent = UserRepository.get_by_id(db, parent_id)
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent not found"
        )

    return UserResponse.model_validate(parent)


@router.put("/{parent_id}", response_model=UserResponse)
def update_parent(
    parent_id: int,
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update parent profile.
    Parents can only update their own profile.
    """
    if current_user.id != parent_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own profile"
        )

    parent = UserRepository.get_by_id(db, parent_id)
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent not found"
        )

    # Update fields
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(parent, field, value)

    db.commit()
    db.refresh(parent)

    return UserResponse.model_validate(parent)


@router.get("/{parent_id}/children", response_model=list[ChildResponse])
def get_parent_children(
    parent_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get all children linked to a parent.
    Parents can only view their own children unless they are admin.
    """
    if current_user.role.value != "admin" and current_user.id != parent_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own children"
        )

    children = ChildRepository.get_by_parent(db, parent_id)
    return [ChildResponse.model_validate(child) for child in children]
