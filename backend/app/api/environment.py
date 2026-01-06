from fastapi import APIRouter, HTTPException
from app.services.weather_service import fetch_environment_by_coords

router = APIRouter(prefix="/environment", tags=["Environment"])

@router.get("/coords")
def get_environment_by_coords(lat: float, lon: float):
    try:
        return fetch_environment_by_coords(lat, lon)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to fetch weather data for this location"
        )
