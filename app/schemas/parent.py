from pydantic import BaseModel, EmailStr
from typing import Optional

class UserUpdate(BaseModel):
    """Schema for updating parent profile."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None