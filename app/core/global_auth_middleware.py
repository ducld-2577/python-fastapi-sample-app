from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.auth_exception_config import is_auth_exempt_path
from app.core.security import decode_access_token
from app.db.session import AsyncSessionLocal
from app.repositories.user import UserRepository


async def global_auth_middleware(request: Request, call_next):
    path = request.url.path

    if request.method == "OPTIONS" or is_auth_exempt_path(path):
        return await call_next(request)

    authorization = request.headers.get("Authorization", "")
    if not authorization.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Missing or invalid Authorization header"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.replace("Bearer ", "", 1).strip()
    if not token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Missing access token"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = decode_access_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise ValueError("sub not found")
        user_id = int(sub)
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Could not validate credentials"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    async with AsyncSessionLocal() as db:
        user_repo = UserRepository(db)
        user = await user_repo.get(user_id)

    if not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "User not found"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "User account is inactive"},
        )

    request.state.current_user = user
    request.state.user_id = user.id
    request.state.user_role = user.role.value

    return await call_next(request)
