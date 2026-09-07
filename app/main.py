from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.api.routes import router
from core.config import get_settings
from core.logging import configure_logging

configure_logging()
s = get_settings()
app = FastAPI(title=s.app_name)
app.include_router(router, prefix='/api')

@app.get('/')
async def voice_demo():
    return FileResponse(Path(__file__).parent / 'api' / 'voice_demo.html')
