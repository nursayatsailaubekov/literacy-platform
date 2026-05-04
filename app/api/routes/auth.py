"""Authentication routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    return AuthService.register(db, user_data)


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login a user."""
    return AuthService.login(db, credentials)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return UserResponse.model_validate(current_user)


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """
    Logout user (client-side token invalidation).
    Note: With JWT, actual logout is handled client-side by deleting the token.
    This endpoint is provided for API consistency and can be used for logging.
    """
    return {
        "message": "Successfully logged out. Please delete your token on the client side.",
        "user_id": current_user.id
    }