from typing import List, Tuple
import math


def optimize_tower_placement(
    farm_length: float,
    farm_width: float,
    min_spacing: float,
    max_towers: int
) -> List[Tuple[float, float]]:
    """
    Optimized hexagonal (offset) placement of aeroponic towers
    """

    if farm_length <= 0 or farm_width <= 0:
        raise ValueError("Invalid farm dimensions")

    if min_spacing <= 0:
        raise ValueError("Minimum spacing must be positive")

    towers = []

    # Vertical spacing for hex grid
    vertical_spacing = min_spacing * math.sqrt(3) / 2

    row = 0
    y = min_spacing / 2

    while y <= farm_width - min_spacing / 2:
        # Offset every alternate row
        x_offset = (min_spacing / 2) if row % 2 == 1 else 0
        x = min_spacing / 2 + x_offset

        while x <= farm_length - min_spacing / 2:
            candidate = (round(x, 2), round(y, 2))

            # Enforce minimum distance
            if all(math.dist(candidate, t) >= min_spacing for t in towers):
                towers.append(candidate)

                if len(towers) >= max_towers:
                    return towers

            x += min_spacing

        y += vertical_spacing
        row += 1

    return towers
