import re
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegisterPayload(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=100)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()

    @field_validator("full_name", mode="before")
    @classmethod
    def normalize_full_name(cls, value: str) -> str:
        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        # bcrypt supports passwords up to 72 bytes.
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 bytes")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must include at least 1 uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must include at least 1 lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must include at least 1 number")
        return value


class UserLoginPayload(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class RefreshTokenPayload(BaseModel):
    refresh_token: str = Field(min_length=1)
