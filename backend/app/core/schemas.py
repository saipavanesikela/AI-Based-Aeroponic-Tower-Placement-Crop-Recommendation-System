from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    temperature: float = Field(..., ge=0, le=45)
    humidity: float = Field(..., ge=20, le=100)
    sunlight_hours: float = Field(..., ge=0, le=24)
    water_ph: float = Field(..., ge=4.5, le=8.0)
    air_quality_index: float = Field(..., ge=0, le=500)
    wind_speed: float = Field(..., ge=0, le=5)
