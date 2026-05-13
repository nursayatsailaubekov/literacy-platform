"""Child profile service with business logic."""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.child_repository import ChildRepository
from app.schemas.child import ChildCreate, ChildUpdate, ChildResponse
from app.models.child import Child


class ChildService:
    """Service for child profile operations."""

    @staticmethod
    def create_child(db: Session, parent_id: int, child_data: ChildCreate) -> ChildResponse:
        """Create a new child profile."""
        if child_data.age < 2 or child_data.age > 12:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Child age must be between 2 and 12",
            )
        
        child = ChildRepository.create(db, parent_id, child_data)
        return ChildResponse.model_validate(child)

    @staticmethod
    def get_children(db: Session, parent_id: int) -> list[ChildResponse]:
        """Get all children for a parent."""
        children = ChildRepository.get_by_parent(db, parent_id)
        return [ChildResponse.model_validate(child) for child in children]

    @staticmethod
    def get_child(db: Session, child_id: int, parent_id: int) -> ChildResponse:
        """Get a specific child, ensuring ownership."""
        child = ChildRepository.get_by_id(db, child_id)
        if not child:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Child not found",
            )
        if child.parent_id != parent_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this child",
            )
        return ChildResponse.model_validate(child)

    @staticmethod
    def update_child(db: Session, child_id: int, parent_id: int, child_data: ChildUpdate) -> ChildResponse:
        """Update a child profile."""
        child = ChildRepository.get_by_id(db, child_id)
        if not child:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Child not found",
            )
        if child.parent_id != parent_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this child",
            )

        if child_data.age and (child_data.age < 2 or child_data.age > 12):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Child age must be between 2 and 12",
            )

        updated_child = ChildRepository.update(db, child, child_data)
        return ChildResponse.model_validate(updated_child)

    @staticmethod
    def delete_child(db: Session, child_id: int, parent_id: int) -> None:
        """Delete a child profile."""
        child = ChildRepository.get_by_id(db, child_id)
        if not child:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Child not found",
            )
        if child.parent_id != parent_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this child",
            )
        ChildRepository.delete(db, child)

    @staticmethod
    def verify_child_ownership(db: Session, child_id: int, parent_id: int) -> Child:
        """Verify that a parent owns a specific child."""
        child = ChildRepository.get_by_id(db, child_id)
        if not child:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Child not found",
            )
        if child.parent_id != parent_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this child",
            )
        return child
