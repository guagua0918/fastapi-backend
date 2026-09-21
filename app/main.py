from pathlib import Path
import os

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from pydantic import BaseModel
from starlette.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from app.core.db import get_connection

load_dotenv()

# 可選：IIS 子路徑（影響 OpenAPI servers 顯示）；Swagger 已用相對路徑抓 openapi.json
ROOT_PATH = os.getenv("ROOT_PATH", "").rstrip("/")

app = FastAPI(
    title="HaHaHan's FastAPI Backend",
    root_path=ROOT_PATH,
    docs_url=None,
    redoc_url=None,
    openapi_url="/api/openapi.json",
)
api_router = APIRouter(prefix="/api")
public_directory = Path(__file__).resolve().parents[2] / "webui-lab"


@app.get("/api/docs", include_in_schema=False)
def swagger_ui():
    # 相對路徑：在 /s115321503/api/docs 下會正確抓到 /s115321503/api/openapi.json
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

# 擴充 StaticFiles：路徑不是 .html／.css 就回 404
class HtmlCssOnlyStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope: dict) -> PlainTextResponse:
        if path and not path.endswith((".html", ".css")):
            return PlainTextResponse("Not Found", status_code=404)
        return await super().get_response(path, scope)


class Item(BaseModel):
    name: str
    price: float


class Note(BaseModel):
    id: int
    title: str
    content: str
    created_at: str


@api_router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@api_router.get("/version")
def version_check() -> dict[str, str]:
    return {"version": "0.1.0"}


@api_router.post("/items", response_model=Item)
def create_item(item: Item) -> Item:
    return item


@api_router.get("/note/{note_id}", response_model=Note)
def get_note(note_id: int) -> Note:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, content, created_at
                FROM notes
                WHERE id = %s
                """,
                (note_id,),
            )
            row = cur.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return Note(
        id=row[0],
        title=row[1],
        content=row[2],
        created_at=row[3].isoformat(),
    )


app.include_router(api_router)


@app.get("/", include_in_schema=False)
def serve_index() -> FileResponse:
    return FileResponse(public_directory / "index.html")


app.mount(
    "/",
    HtmlCssOnlyStaticFiles(directory=public_directory, html=True),
    name="public",
)
