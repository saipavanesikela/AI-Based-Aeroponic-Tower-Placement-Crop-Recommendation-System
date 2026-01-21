from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE = Path(__file__).parent
PATH = BASE / "aeroponic_crop_suitability_dataset.csv"
OUT = BASE.parent / "data" / "class_distribution.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

def plot():
    df = pd.read_csv(PATH)
    if "suitability_class" not in df.columns:
        raise RuntimeError("suitability_class not found in dataset; run conversion/generation first")

    counts = df["suitability_class"].value_counts().sort_index()
    sns.set(style="whitegrid")
    plt.figure(figsize=(6,4))
    ax = sns.barplot(x=counts.index, y=counts.values, palette="viridis")
    ax.set_xlabel("Suitability Class (0=Unsuitable,1=Moderate,2=Suitable)")
    ax.set_ylabel("Count")
    ax.set_title("Dataset class distribution")
    for i, v in enumerate(counts.values):
        ax.text(i, v + max(counts.values)*0.01, str(v), ha='center')
    plt.tight_layout()
    plt.savefig(OUT)
    print("Saved distribution plot to", OUT)

if __name__ == "__main__":
    plot()
