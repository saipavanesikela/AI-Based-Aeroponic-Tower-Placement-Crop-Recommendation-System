from typing import List, Tuple
import math


def is_valid(point, placed, min_dist):
    """Check minimum spacing constraint"""
    for p in placed:
        if math.dist(point, p) < min_dist:
            return False
    return True


def optimize_tower_placement(
    farm_length: float,
    farm_width: float,
    min_spacing: float,
    max_towers: int
) -> List[Tuple[float, float]]:
    """
    Deterministic greedy placement of aeroponic towers
    """

    if farm_length <= 0 or farm_width <= 0:
        raise ValueError("Invalid farm dimensions")

    if min_spacing <= 0:
        raise ValueError("Minimum spacing must be positive")

    placed = []

    x = min_spacing / 2
    while x <= farm_length - min_spacing / 2:
        y = min_spacing / 2
        while y <= farm_width - min_spacing / 2:

            candidate = (round(x, 2), round(y, 2))

            if is_valid(candidate, placed, min_spacing):
                placed.append(candidate)

                if len(placed) >= max_towers:
                    return placed

            y += min_spacing
        x += min_spacing

    return placed
