import os

from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, status
from starlette.responses import RedirectResponse, Response

from app.core.security import COOKIE_NAME, create_access_token, get_current_member
from app.repositories import member as member_repo
from app.schemas.member import MemberProfile

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

_oauth = OAuth()
_client_id = os.getenv("GOOGLE_CLIENT_ID")
_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
if _client_id and _client_secret:
    _oauth.register(
        name="google",
        client_id=_client_id,
        client_secret=_client_secret,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )


def _redirect_uri() -> str:
    uri = os.getenv("GOOGLE_REDIRECT_URI", "").strip()
    if not uri:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Google login is not configured")
    return uri


def _cookie_secure() -> bool:
    return os.getenv("AUTH_COOKIE_SECURE", "true").lower() == "true"


def _verified(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() == "true"


@router.get("/google/login")
async def google_login(request: Request):
    if not hasattr(_oauth, "google"):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Google login is not configured")
    return await _oauth.google.authorize_redirect(request, _redirect_uri())


@router.get("/google/callback", include_in_schema=False)
async def google_callback(request: Request):
    if not hasattr(_oauth, "google"):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Google login is not configured")
    try:
        token = await _oauth.google.authorize_access_token(request)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Google login failed")
    user = token.get("userinfo") or {}
    google_sub = user.get("sub")
    email = user.get("email")
    if not google_sub or not email or not _verified(user.get("email_verified")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Google account is not verified")
    saved = member_repo.upsert_google_member(
        google_sub=google_sub,
        email=email,
        name=user.get("name"),
        picture=user.get("picture"),
        email_verified=True,
    )
    destination = os.getenv("AUTH_SUCCESS_REDIRECT_URL", "/")
    response = RedirectResponse(url=destination, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key=COOKIE_NAME,
        value=create_access_token(saved["id"]),
        httponly=True,
        secure=_cookie_secure(),
        samesite="lax",
        max_age=int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "28800")),
        path="/",
    )
    return response


@router.get("/me", response_model=MemberProfile)
def read_current_member(member: dict = Depends(get_current_member)) -> dict:
    return member


@router.post("/logout")
def logout() -> Response:
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(COOKIE_NAME, path="/")
    return response
