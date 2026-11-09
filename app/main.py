from pathlib import Path
import asyncio
import os
import sys
from contextlib import asynccontextmanager

# W08：Windows 預設 ProactorEventLoop，psycopg async 無法使用 → 改 Selector
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from starlette.exceptions import HTTPException
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from pydantic import BaseModel
from starlette.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from fastapi import HTTPException as FastAPIHTTPException

from app.core.db import close_async_pool, close_sync_pool, init_async_pool, init_sync_pool
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
)
from app.core.logging_config import setup_logging
from app.core.request_logging import RequestLoggingMiddleware
from app.routers.auth import router as auth_router
from app.routers.notes import legacy_router, router as notes_router
from app.routers.objectlist import router as objectlist_router
from app.routers.scan import router as scan_router
from app.routers.subclass import router as subclass_router

load_dotenv()
setup_logging()

# 可選：IIS 子路徑（影響 OpenAPI servers 顯示）；Swagger 已用相對路徑抓 openapi.json
ROOT_PATH = os.getenv("ROOT_PATH", "").rstrip("/")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # W08：啟動時開連線池，關閉時歸還
    init_sync_pool()
    await init_async_pool()
    try:
        yield
    finally:
        close_sync_pool()
        await close_async_pool()


app = FastAPI(
    title="HaHaHan's FastAPI Backend",
    root_path=ROOT_PATH,
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# W10：統一錯誤回應（AppException／HTTPException／未預期）
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(FastAPIHTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

# 後加的 middleware 較外層；請求 log 包住整段處理時間
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["SESSION_SECRET_KEY"],
    same_site="lax",
    https_only=os.getenv("AUTH_COOKIE_SECURE", "true").lower() == "true",
)
api_router = APIRouter(prefix="/api")
public_directory = Path(__file__).resolve().parents[2] / "webui-lab"


@app.get("/api/docs", include_in_schema=False)
def swagger_ui():
    # 相對路徑：在 /s學號/api/docs 下會正確抓到 /s學號/api/openapi.json
    return get_swagger_ui_html(
        openapi_url="openapi.json",
        title=app.title + " - Swagger UI",
    )


@app.get("/api/redoc", include_in_schema=False)
def redoc_ui():
    return get_redoc_html(
        openapi_url="openapi.json",
        title=app.title + " - ReDoc",
    )

# 擴充 StaticFiles：只允許前端需要的靜態資源（html/css/js，以及 js、json 目錄）
class HtmlCssOnlyStaticFiles(StaticFiles):
    allowed_extensions = {".html", ".css", ".js", ".svg", ".png", ".jpg", ".jpeg", ".webp"}
    allowed_directories = {"js", "json", "css", "img"}

    async def get_response(self, path: str, scope: dict) -> PlainTextResponse:
        if path and not Path(path).suffix:
            try:
                return await super().get_response(f"{path}.html", scope)
            except HTTPException:
                return PlainTextResponse("Not Found", status_code=404)
        if path:
            suffix = Path(path).suffix.lower()
            top = path.replace("\\", "/").split("/", 1)[0]
            ok_ext = suffix in self.allowed_extensions
            ok_dir = top in self.allowed_directories
            if not (ok_ext or ok_dir):
                return PlainTextResponse("Not Found", status_code=404)
        return await super().get_response(path, scope)


class Item(BaseModel):
    name: str
    price: float


@api_router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@api_router.get("/version")
def version_check() -> dict[str, str]:
    return {"version": "0.1.0"}


@api_router.post("/items", response_model=Item)
def create_item(item: Item) -> Item:
    return item


app.include_router(api_router) # health / version / items
app.include_router(notes_router, prefix="/api")# → app/routers/notes.py
app.include_router(legacy_router, prefix="/api")
app.include_router(subclass_router, prefix="/api")
app.include_router(objectlist_router, prefix="/api")
app.include_router(scan_router, prefix="/api")
app.include_router(auth_router, prefix="/api")


@app.get("/", include_in_schema=False)
def serve_index() -> FileResponse:
    return FileResponse(public_directory / "index.html")


app.mount(
    "/",
    HtmlCssOnlyStaticFiles(directory=public_directory, html=True),
    name="public",
)
