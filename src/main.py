from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.routers import api, web

app = FastAPI(title="Mural Generator")

# Include routers
app.include_router(api.router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
