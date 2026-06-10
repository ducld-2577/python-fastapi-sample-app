import bcrypt
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError
from jose import jwt

from app.core.config import get_settings

settings = get_settings()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(
    user_id: int,
):
    return _create_token(
        user_id=user_id,
        token_type="access",
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )


def decode_access_token(token: str) -> dict:
    return _decode_token(token=token, expected_token_type="access")


def create_refresh_token(user_id: int):
    return _create_token(
        user_id=user_id,
        token_type="refresh",
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
    )


def decode_refresh_token(token: str) -> dict:
    return _decode_token(token=token, expected_token_type="refresh")


def _create_token(user_id: int, token_type: str, expires_delta: timedelta) -> str:
    payload = {
        "sub": str(user_id),
        "type": token_type,
        "exp": datetime.utcnow() + expires_delta,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def _decode_token(token: str, expected_token_type: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        if payload.get("type") != expected_token_type:
            raise JWTError
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
