import matplotlib
matplotlib.use("Agg")  # headless safe

import matplotlib.pyplot as plt
from pathlib import Path


def visualize_placement(
    towers,
    farm_length,
    farm_width,
    output_path="optimized_tower_layout.png"
):
    """
    Saves a clean placement visualization to disk
    """

    if not towers:
        raise ValueError("No towers to visualize")

    x_vals = [t[0] for t in towers]
    y_vals = [t[1] for t in towers]

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.scatter(x_vals, y_vals, s=120, c="green", edgecolors="black")

    for i, (x, y) in enumerate(towers, start=1):
        ax.text(x, y, str(i), fontsize=9, ha="center", va="center", color="white")

    ax.set_xlim(0, farm_length)
    ax.set_ylim(0, farm_width)

    ax.set_title("Optimized Aeroponic Tower Placement")
    ax.set_xlabel("Farm Length (m)")
    ax.set_ylabel("Farm Width (m)")

    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, linestyle="--", alpha=0.5)

    output_path = Path(output_path)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close(fig)

    return str(output_path)
