import pandas as pd
import matplotlib.pyplot as plt

FARM_LENGTH = 20
FARM_WIDTH = 20
TOWER_RADIUS = 0.6  # visual only

df = pd.read_csv("app/data/optimized_tower_positions_auto_grid.csv")

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_facecolor("#f4f9f4")

# Farm boundary
ax.add_patch(
    plt.Rectangle(
        (0, 0),
        FARM_LENGTH,
        FARM_WIDTH,
        edgecolor="darkgreen",
        facecolor="none",
        linewidth=3
    )
)

# Towers
for i, row in df.iterrows():
    ax.add_patch(
        plt.Circle(
            (row["x_meter"], row["y_meter"]),
            TOWER_RADIUS,
            edgecolor="darkgreen",
            facecolor="#66bb6a",
            linewidth=2
        )
    )
    ax.text(
        row["x_meter"],
        row["y_meter"],
        str(i + 1),
        ha="center",
        va="center",
        fontsize=8
    )

ax.set_xlim(0, FARM_LENGTH)
ax.set_ylim(0, FARM_WIDTH)
ax.set_aspect("equal")
ax.grid(True, linestyle="--", alpha=0.4)

ax.set_title("Optimized Aeroponic Tower Placement")
ax.set_xlabel("Farm Length (m)")
ax.set_ylabel("Farm Width (m)")

plt.savefig("optimized_tower_layout_final.png", dpi=300)
plt.show()
