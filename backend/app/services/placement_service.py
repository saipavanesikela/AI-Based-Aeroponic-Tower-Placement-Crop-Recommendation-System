import matplotlib
matplotlib.use("Agg")  # IMPORTANT for FastAPI

import matplotlib.pyplot as plt
import math
import os

DATA_DIR = "app/data"
IMAGE_PATH = os.path.join(DATA_DIR, "optimized_tower_layout.png")

def optimize_tower_placement(
    farm_length=20,
    farm_width=20,
    min_spacing=2.5,
    max_towers=15
):
    positions = []

    rows = int(farm_length // min_spacing)
    cols = int(farm_width // min_spacing)

    for i in range(rows):
        for j in range(cols):
            if len(positions) >= max_towers:
                break

            x = round((j + 0.5) * min_spacing, 2)
            y = round((i + 0.5) * min_spacing, 2)

            # Ensure inside boundary
            if x <= farm_width and y <= farm_length:
                positions.append([x, y])

        if len(positions) >= max_towers:
            break

    # ------------------ VISUALIZATION ------------------
    os.makedirs(DATA_DIR, exist_ok=True)

    plt.figure(figsize=(6, 6))
    x_vals = [p[0] for p in positions]
    y_vals = [p[1] for p in positions]

    plt.scatter(x_vals, y_vals, c="green", s=120)
    plt.xlim(0, farm_width)
    plt.ylim(0, farm_length)
    plt.xlabel("Farm Width (m)")
    plt.ylabel("Farm Length (m)")
    plt.title("Optimized Aeroponic Tower Placement")
    plt.grid(True)

    plt.savefig(IMAGE_PATH)
    plt.close()

    # Provide a URL that frontend can request. We mount app/data at /static
    image_url = "/static/" + os.path.basename(IMAGE_PATH)

    return {
        "total_towers": len(positions),
        "tower_positions": positions,
        "image_file": IMAGE_PATH,
        "image_url": image_url
    }
