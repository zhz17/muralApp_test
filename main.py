from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.routers import api, web

app = FastAPI(title="Mural Generator")

# Mount static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Include routers
app.include_router(web.router)
app.include_router(api.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
