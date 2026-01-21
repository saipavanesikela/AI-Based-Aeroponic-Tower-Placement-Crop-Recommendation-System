from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
PATH = BASE / "aeroponic_crop_suitability_dataset.csv"


def convert():
    df = pd.read_csv(PATH)
    if "suitability_percentage" not in df.columns:
        raise RuntimeError("Dataset missing suitability_percentage column; regenerate dataset first")

    def map_pct(pct):
        if pct >= 75:
            return 2
        if pct >= 55:
            return 1
        return 0

    df["suitability_class"] = df["suitability_percentage"].apply(map_pct)

    # Drop old 5-class column if present
    if "suitability_score" in df.columns:
        df = df.drop(columns=["suitability_score"])

    df.to_csv(PATH, index=False)
    print("Converted dataset saved to", PATH)


if __name__ == "__main__":
    convert()
