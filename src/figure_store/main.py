"""Aplicación web. Arrancar con: make dev"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from figure_store.config import get_settings

BASE_DIR = Path(__file__).resolve().parent

settings = get_settings()

app = FastAPI(
    title=settings.store_name,
    # La documentación interactiva de la API solo en desarrollo.
    docs_url="/docs" if settings.environment == "dev" else None,
    redoc_url=None,
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")
templates.env.globals["store_name"] = settings.store_name


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    """Para monitoreo: el servidor de hosting consulta esta ruta para saber si la app vive."""
    return {"status": "ok"}
