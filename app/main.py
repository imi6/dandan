"""Main FastAPI application"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from app.config import settings
from app.api import video, danmaku, match, websocket, settings as settings_api
from app.core.exceptions import setup_exception_handlers

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Create upload directory if not exists
os.makedirs(settings.upload_dir, exist_ok=True)

# Setup exception handlers
setup_exception_handlers(app)

# Include routers
app.include_router(video.router, prefix="/api/video", tags=["video"])
app.include_router(danmaku.router, prefix="/api/danmaku", tags=["danmaku"])
app.include_router(match.router, prefix="/api/match", tags=["match"])
app.include_router(settings_api.router, prefix="/api/settings", tags=["settings"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])


@app.get("/")
async def root(request: Request):
    """Root endpoint - serve HTML page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/splash")
async def splash_page(request: Request):
    """Splash screen"""
    return templates.TemplateResponse("splash.html", {"request": request})


@app.get("/settings")
async def settings_page(request: Request):
    """Settings page"""
    return templates.TemplateResponse("settings.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )