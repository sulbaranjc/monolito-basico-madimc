# app/main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.routers.patients import router as patients_router

app = FastAPI(title="MEDIMIC Monolith")
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.state.templates = templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

app.include_router(patients_router)


@app.get("/")
def root():
    return RedirectResponse(url="/patients", status_code=303)


@app.get("/health")
def health():
    return {"status": "ok"}
