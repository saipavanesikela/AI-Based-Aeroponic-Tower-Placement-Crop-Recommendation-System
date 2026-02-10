from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.placement_service import optimize_tower_placement

router = APIRouter(
    prefix="/placement",
    tags=["Tower Placement"]
)

# -------------------------------
# REQUEST SCHEMA
# -------------------------------
class PlacementRequest(BaseModel):
    farm_length: float = Field(..., gt=0, le=100, description="Farm length in meters (0 < length ≤ 100)")
    farm_width: float = Field(..., gt=0, le=100, description="Farm width in meters (0 < width ≤ 100)")
    min_spacing: float = Field(..., ge=0.5, le=10, description="Minimum spacing between towers (0.5 ≤ spacing ≤ 10)")
    max_towers: int = Field(..., ge=1, le=1000, description="Maximum number of towers (1 ≤ max_towers ≤ 1000)")

# -------------------------------
# API ENDPOINT
# -------------------------------
@router.post("/")
def place_towers(request: PlacementRequest):
    """
    Optimizes aeroponic tower placement based on farm parameters
    """
    try:
        result = optimize_tower_placement(
            farm_length=request.farm_length,
            farm_width=request.farm_width,
            min_spacing=request.min_spacing,
            max_towers=request.max_towers
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Placement optimization failed: {str(e)}")
