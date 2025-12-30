import pandas as pd
import math

# ----------------------------------
# FARM CONFIGURATION
# ----------------------------------
FARM_LENGTH = 20.0   # meters
FARM_WIDTH = 20.0    # meters
MIN_SPACING = 2.5    # meters (tower spacing)
MAX_TOWERS = 15

# ----------------------------------
# AUTOMATIC GRID CALCULATION
# ----------------------------------
GRID_COLS = int(FARM_LENGTH // MIN_SPACING)
GRID_ROWS = int(FARM_WIDTH // MIN_SPACING)

CELL_LENGTH = FARM_LENGTH / GRID_COLS
CELL_WIDTH = FARM_WIDTH / GRID_ROWS

print(f"Auto Grid Size: {GRID_COLS} x {GRID_ROWS}")
print(f"Cell Size: {CELL_LENGTH:.2f}m x {CELL_WIDTH:.2f}m")

# ----------------------------------
# LOAD DATA
# ----------------------------------
df = pd.read_csv("aeroponic_crop_placement_dataset.csv")

# Sort by best yield first
df_sorted = df.sort_values(by="yield_score", ascending=False)

selected_positions = []

# ----------------------------------
# DISTANCE CHECK FUNCTION
# ----------------------------------
def is_valid_position(x, y, placed):
    for px, py in placed:
        dist = math.sqrt((x - px)**2 + (y - py)**2)
        if dist < MIN_SPACING:
            return False
    return True

# ----------------------------------
# GREEDY PLACEMENT
# ----------------------------------
for _, row in df_sorted.iterrows():
    if len(selected_positions) >= MAX_TOWERS:
        break

    # Convert grid index → real-world meters
    real_x = row["x_coord"] * CELL_LENGTH
    real_y = row["y_coord"] * CELL_WIDTH

    # Ensure inside farm boundary
    if real_x > FARM_LENGTH or real_y > FARM_WIDTH:
        continue

    if is_valid_position(real_x, real_y, selected_positions):
        selected_positions.append((real_x, real_y))

# ----------------------------------
# SAVE RESULT
# ----------------------------------
placement_df = pd.DataFrame(
    selected_positions,
    columns=["x_meter", "y_meter"]
)

placement_df.to_csv(
    "optimized_tower_positions_auto_grid.csv",
    index=False
)

print("\nFinal Tower Count:", len(selected_positions))
print(placement_df)
