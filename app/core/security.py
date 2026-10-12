import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, Request, status

from app.repositories import member as member_repo

load_dotenv()

COOKIE_NAME = "access_token"
JWT_ISSUER = "foot-helper"
_ALGORITHM = "HS256"


def _secret() -> str:
    secret = os.getenv("JWT_SECRET_KEY")
    if not secret:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="JWT is not configured")
    return secret


def _expire_seconds() -> int:
    raw = os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "28800")
    try:
        return int(raw)
    except ValueError:
        return 28800


def create_access_token(member_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(member_id),
        "iss": JWT_ISSUER,
        "iat": now,
        "exp": now + timedelta(seconds=_expire_seconds()),
    }
    return jwt.encode(payload, _secret(), algorithm=_ALGORITHM)


def read_token(request: Request) -> str | None:
    header = request.headers.get("authorization")
    if header and header.lower().startswith("bearer "):
        return header.split(" ", 1)[1].strip() or None
    return request.cookies.get(COOKIE_NAME)


def get_current_member(request: Request) -> dict:
    token = read_token(request)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = jwt.decode(
            token,
            _secret(),
            algorithms=[_ALGORITHM],
            issuer=JWT_ISSUER,
            options={"require": ["exp", "sub", "iss"]},
        )
        member_id = int(payload["sub"])
    except (jwt.PyJWTError, TypeError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    member = member_repo.get_verified_member(member_id)
    if member is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return member
