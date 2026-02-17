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
    # algorithm selection and tuning
    method: str = Field("ga", description="Placement algorithm: 'hex', 'sa', or 'ga'")
    ga_pop_size: int = Field(60, ge=2, le=200, description="GA population size")
    ga_generations: int = Field(200, ge=1, le=5000, description="GA generations")
    ga_time_limit: float = Field(2.0, ge=0.1, le=60.0, description="GA time limit in seconds")
    sa_time_limit: float = Field(2.0, ge=0.1, le=60.0, description="Simulated annealing time limit in seconds")
    sa_max_iters: int = Field(5000, ge=1, le=200000, description="Simulated annealing max iterations")

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
            max_towers=request.max_towers,
            method=request.method,
            ga_pop_size=request.ga_pop_size,
            ga_generations=request.ga_generations,
            ga_time_limit=request.ga_time_limit,
            sa_time_limit=request.sa_time_limit,
            sa_max_iters=request.sa_max_iters,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Placement optimization failed: {str(e)}")
