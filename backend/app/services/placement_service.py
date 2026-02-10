import uuid
from pathlib import Path

from app.services.optimization_service import greedy_tower_placement, generate_placement_image

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def optimize_tower_placement(
    farm_length: float = 20.0,
    farm_width: float = 20.0,
    min_spacing: float = 2.5,
    max_towers: int = 15,
):
    # Use the greedy placer that respects spacing and max_towers
    positions = greedy_tower_placement(
        farm_length=farm_length,
        farm_width=farm_width,
        min_spacing=min_spacing,
        max_towers=max_towers,
    )

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    image_filename = f"optimized_tower_layout_{uuid.uuid4().hex}.png"
    image_path = DATA_DIR / image_filename

    # Generate visualization
    generate_placement_image(
        positions=positions,
        farm_width=farm_width,
        farm_length=farm_length,
        min_spacing=min_spacing,
        output_path=str(image_path),
    )

    image_url = "/static/" + image_filename

    return {
        "total_towers": len(positions),
        "tower_positions": positions,
        "image_file": str(image_path),
        "image_url": image_url,
    }
