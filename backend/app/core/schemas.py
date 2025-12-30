from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    temperature: float = Field(..., ge=0, le=45)
    humidity: float = Field(..., ge=20, le=100)
    wind_speed: float = Field(..., ge=0, le=10)
    sunlight_hours: float = Field(..., ge=0, le=24)
    x_coord: int = Field(..., ge=0)
    y_coord: int = Field(..., ge=0)
    spacing: float = Field(..., ge=0.5, le=5.0)
    shade_percent: float = Field(..., ge=0, le=100)
