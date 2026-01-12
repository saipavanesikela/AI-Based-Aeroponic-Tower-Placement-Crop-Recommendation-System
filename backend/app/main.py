from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Routers
from app.api.predict import router as predict_router
from app.api.placement import router as placement_router
from app.api.environment import router as environment_router

app = FastAPI(title="Aeroponic Optimization API")

# CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(predict_router)
app.include_router(placement_router)
app.include_router(environment_router)

# Serve generated images and other static data (absolute path for reliability)
STATIC_DIR = Path(__file__).resolve().parent / "data"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
def root():
    return {"message": "Aeroponic Optimization API is running"}
