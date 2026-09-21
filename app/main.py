from pathlib import Path

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
from starlette.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="HaHaHan's FastAPI Backend")
api_router = APIRouter(prefix="/api")
public_directory = Path(__file__).resolve().parents[2] / "webui-lab"


class HtmlCssOnlyStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope: dict) -> PlainTextResponse:
        if path and not path.endswith((".html", ".css")):
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


app.include_router(api_router)


@app.get("/", include_in_schema=False)
def serve_index() -> FileResponse:
    return FileResponse(public_directory / "index.html")


app.mount(
    "/",
    HtmlCssOnlyStaticFiles(directory=public_directory, html=True),
    name="public",
)
