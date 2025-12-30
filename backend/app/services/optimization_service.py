import math
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_IMAGE = BASE_DIR / "data" / "optimized_tower_layout.png"

def greedy_tower_placement(
    farm_length: float,
    farm_width: float,
    min_spacing: float,
    max_towers: int
):
    """
    Greedy algorithm to place aeroponic towers
    and generate visualization automatically.
    """

    # Automatic grid calculation
    grid_cols = int(farm_length // min_spacing)
    grid_rows = int(farm_width // min_spacing)

    cell_x = farm_length / grid_cols
    cell_y = farm_width / grid_rows

    placed_towers = []

    for i in range(grid_cols):
        for j in range(grid_rows):
            if len(placed_towers) >= max_towers:
                break

            x = (i + 0.5) * cell_x
            y = (j + 0.5) * cell_y

            valid = True
            for px, py in placed_towers:
                if math.sqrt((x - px)**2 + (y - py)**2) < min_spacing:
                    valid = False
                    break

            if valid:
                placed_towers.append((x, y))

    # ---------------- SAVE CSV ----------------
    df = pd.DataFrame(placed_towers, columns=["x_meter", "y_meter"])
    csv_path = DATA_DIR / "optimized_tower_positions_auto_grid.csv"
    df.to_csv(csv_path, index=False)

    # ---------------- GENERATE IMAGE ----------------
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor("#f4f9f4")

    # Farm boundary
    ax.add_patch(
        plt.Rectangle(
            (0, 0),
            farm_length,
            farm_width,
            edgecolor="darkgreen",
            facecolor="none",
            linewidth=3
        )
    )

    # Towers
    for i, (x, y) in enumerate(placed_towers):
        ax.add_patch(
            plt.Circle(
                (x, y),
                0.6,
                edgecolor="darkgreen",
                facecolor="#66bb6a",
                linewidth=2
            )
        )
        ax.text(x, y, str(i + 1), ha="center", va="center", fontsize=8)

    ax.set_xlim(0, farm_length)
    ax.set_ylim(0, farm_width)
    ax.set_aspect("equal")
    ax.grid(True, linestyle="--", alpha=0.4)

    ax.set_title("Optimized Aeroponic Tower Placement")
    ax.set_xlabel("Farm Length (m)")
    ax.set_ylabel("Farm Width (m)")

    plt.savefig(OUTPUT_IMAGE, dpi=300, bbox_inches="tight")
    plt.close()

    return {
        "total_towers": len(placed_towers),
        "csv_file": str(csv_path),
        "image_file": str(OUTPUT_IMAGE),
        "tower_positions": placed_towers
    }
