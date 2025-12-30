from fastapi import APIRouter
from app.services.optimization_service import greedy_tower_placement

router = APIRouter(
    prefix="/placement",
    tags=["Tower Placement Optimization"]
)

@router.post("/")
def optimize_placement(
    farm_length: float = 20,
    farm_width: float = 20,
    min_spacing: float = 2.5,
    max_towers: int = 15
):
    """
    Run greedy tower placement and generate visualization.
    """
    return greedy_tower_placement(
        farm_length,
        farm_width,
        min_spacing,
        max_towers
    )
