import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------
# FARM CONFIGURATION
# ----------------------------------
FARM_LENGTH = 20  # meters
FARM_WIDTH = 20   # meters

# NOTE:
# This radius is ONLY for visualization.
# It does NOT affect placement or spacing logic.
TOWER_RADIUS = 0.6

# ----------------------------------
# LOAD OPTIMIZED TOWER POSITIONS
# ----------------------------------
df = pd.read_csv("optimized_tower_positions_auto_grid.csv")

print("Number of towers in CSV:", len(df))

# ----------------------------------
# CREATE PLOT
# ----------------------------------
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_facecolor("#f4f9f4")

# Draw farm boundary
farm_boundary = plt.Rectangle(
    (0, 0),
    FARM_LENGTH,
    FARM_WIDTH,
    edgecolor="darkgreen",
    facecolor="none",
    linewidth=3
)
ax.add_patch(farm_boundary)

# ----------------------------------
# DRAW TOWERS
# ----------------------------------
for i, row in df.iterrows():
    tower = plt.Circle(
        (row["x_meter"], row["y_meter"]),
        TOWER_RADIUS,
        edgecolor="darkgreen",
        facecolor="#66bb6a",
        linewidth=2,
        alpha=0.9
    )
    ax.add_patch(tower)

    # Label each tower (to clearly show count)
    ax.text(
        row["x_meter"],
        row["y_meter"],
        str(i + 1),
        color="black",
        fontsize=8,
        ha="center",
        va="center"
    )

# ----------------------------------
# GRID, AXES & LABELS
# ----------------------------------
ax.set_xticks(range(0, FARM_LENGTH + 1, 2))
ax.set_yticks(range(0, FARM_WIDTH + 1, 2))
ax.grid(True, linestyle="--", alpha=0.4)

ax.set_xlim(0, FARM_LENGTH)
ax.set_ylim(0, FARM_WIDTH)
ax.set_aspect("equal")

ax.set_xlabel("Farm Length (meters)", fontsize=12)
ax.set_ylabel("Farm Width (meters)", fontsize=12)

ax.set_title(
    "Optimized Aeroponic Tower Placement (Automatic Grid)",
    fontsize=16,
    fontweight="bold",
    pad=15
)

# Remove unnecessary borders
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# ----------------------------------
# SAVE & SHOW
# ----------------------------------
plt.savefig(
    "optimized_tower_layout_final.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
