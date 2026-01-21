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
    logger.info(f"Starting hexagonal placement: length={farm_length}, width={farm_width}, spacing={min_spacing}, max_towers={max_towers}")
    positions: List[Tuple[float, float]] = []

    if farm_length <= 0 or farm_width <= 0:
        logger.error("Invalid farm dimensions")
        return positions

    if min_spacing <= 0:
        logger.error("Minimum spacing must be positive")
        return positions

    # Vertical spacing for hex grid (rows are offset)
    vertical_spacing = min_spacing * math.sqrt(3) / 2

    row = 0
    # start y at half spacing to keep towers inside boundary
    y = min_spacing / 2.0

    try:
        while y <= farm_width - min_spacing / 2.0:
            # offset every other row
            x_offset = (min_spacing / 2.0) if row % 2 == 1 else 0.0
            x = min_spacing / 2.0 + x_offset

            while x <= farm_length - min_spacing / 2.0:
                candidate = (round(x, 2), round(y, 2))

                # Ensure candidate respects minimum spacing to all placed towers
                if all(math.dist(candidate, t) >= min_spacing for t in positions):
                    positions.append(candidate)
                    if len(positions) >= max_towers:
                        logger.info(f"Max towers placed: {len(positions)}")
                        return positions

                x += min_spacing

            y += vertical_spacing
            row += 1

        logger.info(f"Total towers placed: {len(positions)}")
        return positions
    except Exception as e:
        logger.error(f"Error in greedy_tower_placement (hex): {e}")
        raise

# ---------------------------------------------
# VISUALIZATION (PREMIUM STYLE)
# ---------------------------------------------
def generate_placement_image(
    positions: List[Tuple[float, float]],
    farm_width: float,
    farm_length: float,
    min_spacing: float,
    output_path: str,
    cell_size_m: float = None,
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
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_facecolor("#ffffff")

        # Compute grid dimensions (use provided cell_size_m if given, else min_spacing)
        cell = cell_size_m if (cell_size_m and cell_size_m > 0) else min_spacing
        n_cols = max(1, int(math.ceil(farm_width / cell)))
        n_rows = max(1, int(math.ceil(farm_length / cell)))

        # Map tower positions to grid cells (row, col)
        allowed_cells = set()
        for (x, y) in positions:
            col = int(x // cell)
            row = int(y // cell)
            col = min(max(col, 0), n_cols - 1)
            row = min(max(row, 0), n_rows - 1)
            allowed_cells.add((row, col))

        # Draw grid cells and labels
        for row in range(n_rows):
            for col in range(n_cols):
                cell_x = col * cell
                cell_y = row * cell
                cell_w = cell if (cell_x + cell) <= farm_width else max(0.0, farm_width - cell_x)
                cell_h = cell if (cell_y + cell) <= farm_length else max(0.0, farm_length - cell_y)
                if (row, col) in allowed_cells:
                    face = '#dcfce7'  # light green
                    edge = '#86efac'
                else:
                    face = 'none'
                    edge = '#cbd5e1'
                rect = Rectangle((cell_x, cell_y), cell_w, cell_h, linewidth=1, edgecolor=edge, facecolor=face, alpha=0.9, zorder=1)
                ax.add_patch(rect)

                # Cell label like A1, A2... (rows -> letters)
                if row < 26:
                    row_label = chr(ord('A') + row)
                else:
                    row_label = str(row + 1)
                col_label = str(col + 1)
                ax.text(cell_x + cell_w / 2.0, cell_y + cell_h / 2.0, f"{row_label}{col_label}", ha='center', va='center', fontsize=8, color='#0b3954', zorder=2)

        # Farm boundary
        farm = Rectangle((0, 0), farm_width, farm_length, linewidth=2, edgecolor="#0b3d91", facecolor="none", zorder=3)
        ax.add_patch(farm)

        # Draw tower markers on top
        for i, (x, y) in enumerate(positions):
            tower = Circle((x, y), radius=0.28, color="#0b5cff", zorder=4)
            ax.add_patch(tower)
            ax.text(x, y + 0.45, f"{i+1}", ha="center", fontsize=9, fontweight="bold", color="#021124", zorder=5)

        # Axes & ticks
        ax.set_xlim(0, farm_width)
        ax.set_ylim(0, farm_length)
        ax.set_xlabel("Width (meters)")
        ax.set_ylabel("Length (meters)")
        ax.set_title("Optimized Aeroponic Tower Placement", fontsize=14, fontweight="bold", pad=12)

        # Legend
        from matplotlib.patches import Patch
        legend_handles = [Patch(facecolor='#dcfce7', edgecolor='#86efac', label='Cells eligible for towers'), Patch(facecolor='none', edgecolor='#cbd5e1', label='Grid cells')]
        ax.legend(handles=legend_handles, loc='upper right')

        plt.tight_layout()
        plt.savefig(output_path, dpi=220)
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
    max_towers: int,
    cell_size_m: float = None,
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
            output_path=image_path,
            cell_size_m=cell_size_m,
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
