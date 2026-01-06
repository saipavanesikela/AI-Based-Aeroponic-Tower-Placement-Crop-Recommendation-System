import os
import math
import logging
import uuid
from typing import List, Tuple

import matplotlib
matplotlib.use("Agg")  # IMPORTANT: non-GUI backend

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

# Setup logger
logger = logging.getLogger("aeroponic.optimization")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# ---------------------------------------------
# GREEDY PLACEMENT ALGORITHM
# ---------------------------------------------
def greedy_tower_placement(
    farm_length: float,
    farm_width: float,
    min_spacing: float,
    max_towers: int
) -> List[Tuple[float, float]]:
    """
    Places towers using a greedy grid-based approach while respecting minimum spacing and farm boundaries.

    Args:
        farm_length (float): Length of the farm in meters.
        farm_width (float): Width of the farm in meters.
        min_spacing (float): Minimum spacing between towers in meters.
        max_towers (int): Maximum number of towers to place.

    Returns:
        List[Tuple[float, float]]: List of (x, y) positions for each tower.
    """
    logger.info(f"Starting greedy placement: length={farm_length}, width={farm_width}, spacing={min_spacing}, max_towers={max_towers}")
    positions = []
    step = min_spacing
    try:
        y = step / 2
        while y <= farm_length - step / 2:
            x = step / 2
            while x <= farm_width - step / 2:
                if len(positions) >= max_towers:
                    logger.info(f"Max towers placed: {len(positions)}")
                    return positions
                valid = True
                for px, py in positions:
                    dist = math.dist((x, y), (px, py))
                    if dist < min_spacing:
                        valid = False
                        break
                if valid:
                    positions.append((round(x, 2), round(y, 2)))
                x += step
            y += step
        logger.info(f"Total towers placed: {len(positions)}")
        return positions
    except Exception as e:
        logger.error(f"Error in greedy_tower_placement: {e}")
        raise

# ---------------------------------------------
# VISUALIZATION (PREMIUM STYLE)
# ---------------------------------------------
def generate_placement_image(
    positions: List[Tuple[float, float]],
    farm_width: float,
    farm_length: float,
    min_spacing: float,
    output_path: str
) -> None:
    """
    Generates and saves a visualization image of the tower placement.

    Args:
        positions (List[Tuple[float, float]]): List of (x, y) tower positions.
        farm_width (float): Width of the farm in meters.
        farm_length (float): Length of the farm in meters.
        min_spacing (float): Minimum spacing between towers in meters.
        output_path (str): Path to save the generated image.
    """
    try:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_facecolor("#f9fafb")

        # Farm boundary
        farm = Rectangle(
            (0, 0),
            farm_width,
            farm_length,
            linewidth=2,
            edgecolor="#1f2937",
            facecolor="none"
        )
        ax.add_patch(farm)

        # Towers
        for i, (x, y) in enumerate(positions):
            # Tower body
            tower = Circle(
                (x, y),
                radius=0.3,
                color="#2563eb",
                zorder=3
            )
            ax.add_patch(tower)

            # Spacing radius
            spacing = Circle(
                (x, y),
                radius=min_spacing / 2,
                color="#60a5fa",
                alpha=0.15,
                zorder=2
            )
            ax.add_patch(spacing)

            # Label
            ax.text(
                x,
                y + 0.4,
                f"T{i+1}",
                ha="center",
                fontsize=9,
                color="#111827"
            )

        # Axes & grid
        ax.set_xlim(0, farm_width)
        ax.set_ylim(0, farm_length)
        ax.set_xticks(range(0, int(farm_width) + 1, 2))
        ax.set_yticks(range(0, int(farm_length) + 1, 2))
        ax.grid(color="#e5e7eb", linestyle="--", linewidth=0.6)

        ax.set_xlabel("Width (meters)")
        ax.set_ylabel("Length (meters)")
        ax.set_title(
            "Optimized Aeroponic Tower Placement",
            fontsize=14,
            fontweight="bold",
            pad=12
        )
        plt.tight_layout()
        plt.savefig(output_path, dpi=200)
        plt.close()
        logger.info(f"Placement image saved to {output_path}")
    except Exception as e:
        logger.error(f"Error generating placement image: {e}")
        raise

# ---------------------------------------------
# MAIN SERVICE FUNCTION
# ---------------------------------------------
def optimize_tower_placement(
    farm_length: float,
    farm_width: float,
    min_spacing: float,
    max_towers: int
) -> dict:
    """
    Main service function called by API. Optimizes tower placement and generates a placement image.

    Args:
        farm_length (float): Length of the farm in meters.
        farm_width (float): Width of the farm in meters.
        min_spacing (float): Minimum spacing between towers in meters.
        max_towers (int): Maximum number of towers to place.

    Returns:
        dict: Dictionary with total_towers, tower_positions, and image_path.
    """
    try:
        positions = greedy_tower_placement(
            farm_length=farm_length,
            farm_width=farm_width,
            min_spacing=min_spacing,
            max_towers=max_towers
        )
        # Ensure output directory exists
        output_dir = "app/data"
        os.makedirs(output_dir, exist_ok=True)
        image_filename = f"optimized_tower_layout_{uuid.uuid4().hex}.png"
        image_path = os.path.join(output_dir, image_filename)
        generate_placement_image(
            positions=positions,
            farm_width=farm_width,
            farm_length=farm_length,
            min_spacing=min_spacing,
            output_path=image_path
        )
        logger.info(f"Placement optimization successful. Towers: {len(positions)}")
        return {
            "total_towers": len(positions),
            "tower_positions": positions,
            "image_path": image_path
        }
    except Exception as e:
        logger.error(f"Error in optimize_tower_placement: {e}")
        raise
