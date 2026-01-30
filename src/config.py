import os
from functools import lru_cache

class Settings:
    MURAL_CLIENT_ID: str = os.getenv("MURAL_CLIENT_ID", "")
    MURAL_CLIENT_SECRET: str = os.getenv("MURAL_CLIENT_SECRET", "")
    MURAL_REDIRECT_URI: str = os.getenv("MURAL_REDIRECT_URI", "http://localhost:8000/")
    
@lru_cache()
def get_settings():
    return Settings()
