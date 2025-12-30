from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.predict import router as predict_router
from app.api.placement import router as placement_router
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title="Aeroponic Tower Placement System",
    description="Crop suitability prediction and placement optimization",
    version="1.0"
)

# ---------------- CORS CONFIG ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- ROUTES ----------------
app.include_router(predict_router)
app.include_router(placement_router)
app.mount(
    "/static",
    StaticFiles(directory="app/data"),
    name="static"
)


@app.get("/")
def root():
    return {"message": "Aeroponic Tower Placement Backend is running"}
