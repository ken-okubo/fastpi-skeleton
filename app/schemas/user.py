from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import DateTimeUTC


class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"


class Role(str, Enum):
    user = "user"
    admin = "admin"


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: Optional[str] = Field(None, max_length=150)
    roles: list[Role] = Field(default=[Role.user])

    model_config = {
        "populate_by_name": True,
    }


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=150)
    status: Optional[UserStatus] = None

    model_config = {
        "populate_by_name": True,
    }


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: Optional[str] = None
    status: UserStatus
    roles: list[str] = Field(..., alias="roles")
    created_at: DateTimeUTC = Field(..., alias="createdAt")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
    }

    @classmethod
    def from_user(cls, user) -> "UserResponse":
        return cls(
            id=user.id,
            email=user.email,
            name=user.name,
            status=user.status,
            roles=list(user.role_names),
            created_at=user.created_at,
        )


class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int
    skip: int
    limit: int
