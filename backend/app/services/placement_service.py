import uuid
from pathlib import Path

import math
from app.services.optimization_service import greedy_tower_placement, generate_placement_image

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def optimize_tower_placement(
    farm_length: float = 20.0,
    farm_width: float = 20.0,
    min_spacing: float = 2.5,
    max_towers: int = 15,
    cell_size_m: float = None,
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

    # Generate visualization; pass optional cell_size_m for grid drawing
    generate_placement_image(
        positions=positions,
        farm_width=farm_width,
        farm_length=farm_length,
        min_spacing=min_spacing,
        cell_size_m=cell_size_m,
        output_path=str(image_path),
    )

    image_url = "/static/" + image_filename

    # compute grid metadata to return (use provided cell_size_m if given)
    cell = cell_size_m if (cell_size_m and cell_size_m > 0) else min_spacing
    n_cols = max(1, int(math.ceil(farm_width / cell)))
    n_rows = max(1, int(math.ceil(farm_length / cell)))
    eligible = []
    for (x, y) in positions:
        col = int(x // cell)
        row = int(y // cell)
        col = min(max(col, 0), n_cols - 1)
        row = min(max(row, 0), n_rows - 1)
        label = chr(ord('A') + row) if row < 26 else str(row + 1)
        label += str(col + 1)
        if label not in eligible:
            eligible.append(label)

    return {
        "total_towers": len(positions),
        "tower_positions": positions,
        "image_file": str(image_path),
        "image_url": image_url,
        "grid": {
            "cell_size_m": min_spacing,
            "n_rows": n_rows,
            "n_cols": n_cols,
            "eligible_cells": eligible,
        },
    }
