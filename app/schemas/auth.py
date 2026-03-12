from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import DateTimeUTC


class Token(BaseModel):
    access_token: str = Field(..., alias="accessToken")
    refresh_token: str = Field(..., alias="refreshToken")
    token_type: str = Field(default="bearer", alias="tokenType")

    model_config = {
        "populate_by_name": True,
    }


class TokenPayload(BaseModel):
    sub: str
    exp: datetime
    type: str  # "access" or "refresh"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., alias="refreshToken")

    model_config = {
        "populate_by_name": True,
    }


class PasswordChange(BaseModel):
    current_password: str = Field(..., alias="currentPassword")
    new_password: str = Field(..., min_length=8, alias="newPassword")

    model_config = {
        "populate_by_name": True,
    }
