import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os 
from pathlib import Path

# folder next to this script (absolute base for outputs)
BASE_DIR = Path(__file__).resolve().parent
out_dir = BASE_DIR / "out" / "img"
out_dir.mkdir(parents=True, exist_ok=True)
file_path = out_dir / "histograms.png"   # absolute path used when opening the file

# load data (CSV relative to current working directory)
df = pd.read_csv('data/clean_set.csv')

# Select numeric columns only
numeric_cols = df.select_dtypes(include=np.number).columns

# Grid settings
n_cols = 3                                # number of subplots per row
n_rows = int(np.ceil(len(numeric_cols) / n_cols))

fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
axes = axes.flatten()

# Plot each numeric column
for i, col in enumerate(numeric_cols):
    sns.histplot(data=df, x=col, kde=True, ax=axes[i], color="steelblue")
    axes[i].set_title(col)
    axes[i].set_xlabel(col)
    axes[i].set_ylabel("Count")
    axes[i].grid(True)

# Remove empty subplots if there are fewer columns than grid cells
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.savefig("out/img/histograms.png", dpi=300, bbox_inches="tight")  # save using a path relative to CWD
plt.close()

# open the saved image with the system's default viewer (Windows)
# NOTE: 'file_path' points to BASE_DIR/out/img/histograms.png, which should match the save path if CWD == BASE_DIR
os.startfile(str(file_path))
