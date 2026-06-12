from app.core.config import get_settings

settings = get_settings()

# Exact paths that bypass global auth middleware.
AUTH_EXEMPT_EXACT_PATHS = {
    "/docs",
    "/redoc",
    "/openapi.json",
}

# Prefix paths that bypass global auth middleware.
AUTH_EXEMPT_PREFIX_PATHS = {
    f"{settings.api_v1_prefix}/health",
    f"{settings.api_v1_prefix}/auth/login",
    f"{settings.api_v1_prefix}/auth/register",
    f"{settings.api_v1_prefix}/auth/refresh",
}


def is_auth_exempt_path(path: str) -> bool:
    if path in AUTH_EXEMPT_EXACT_PATHS:
        return True

    return any(path.startswith(prefix) for prefix in AUTH_EXEMPT_PREFIX_PATHS)
