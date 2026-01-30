from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from src.config import get_settings
from src.api.mural_client import MuralClient
import logging

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")
logger = logging.getLogger(__name__)

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, code: str = None, error: str = None):
    settings = get_settings()
    access_token = None
    
    if error:
        logger.error(f"OAuth Error: {error}")
    
    if code:
        try:
            token_data = MuralClient.exchange_auth_code(
                settings.MURAL_CLIENT_ID,
                settings.MURAL_CLIENT_SECRET,
                settings.MURAL_REDIRECT_URI,
                code
            )
            access_token = token_data.get("access_token")
        except Exception as e:
            logger.error(f"Failed to exchange code: {e}")
            error = "Failed to authenticate with Mural"

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "access_token": access_token,
        "error": error
    })

@router.get("/login")
async def login():
    settings = get_settings()
    if not settings.MURAL_CLIENT_ID:
        raise HTTPException(status_code=500, detail="MURAL_CLIENT_ID not configured")
    
    return RedirectResponse(
        f"https://app.mural.co/api/public/v1/authorization/oauth2/?client_id={settings.MURAL_CLIENT_ID}&redirect_uri={settings.MURAL_REDIRECT_URI}&response_type=code&scope=murals:read murals:write rooms:read rooms:write"
    )
