import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
from tabulate import tabulate 
import os, platform, subprocess
from pathlib import Path 

def run(df: pd.DataFrame, out_dir: Path, show: bool=False, open_after: bool = False):
 # Normalize output base and ensure subfolders for images/tables exist
 out_dir = Path(out_dir)
 img_dir = out_dir / "img"   # images will be saved here
 tab_dir = out_dir / "tab"   # tables (CSV/MD) will be saved here
 img_dir.mkdir(parents=True, exist_ok=True)
 tab_dir.mkdir(parents=True, exist_ok=True)

 # Filter dataset: keep sessions with duration between 0.5 and 1.5 hours
 df_fixed = df[
     (df["Session_Duration (hours)"].between(0.5, 1.5))
 ]

 # Aggregate: mean HRR by Age and Gender (rounded to 2 decimals)
 df_avg = (df_fixed.
           groupby(["Age", "Gender"])["HRR"]
           .mean()
           .reset_index()
           .round(2)
          )

 # Plot: regression HRR vs Age, faceted and colored by Gender
 g = sns.lmplot(data=df_avg, x="Age", y="HRR", col="Gender", hue="Gender", palette="Set1")
 g.fig.suptitle("Correlation_HRR_and_Age_by_Gender")  # overall figure title

 # Save image (PNG) to out/img
 img_path = img_dir/"Correlation_HRR_and_Age_by_Gender.png"
 g.savefig(img_path, dpi=300, bbox_inches="tight")

 # Save aggregated table to CSV (and Markdown if available) in out/tab
 csv_path = tab_dir/"Correlation_HRR_and_Age_by_Gender.csv"
 df_avg.to_csv(csv_path, index=False)
 try:
  md_path = tab_dir/"Correlation_HRR_and_Age_by_Gender.md"
  df_avg.to_markdown(md_path, index=False)
 except Exception:
  md_path = None  # silently ignore if Markdown export is unavailable

 # Display behavior: show interactively (blocking) or close the figure
 if show:
        plt.show(block=True)   # ← this step's window stays open until you close it
 else: 
  plt.close(g.fig)

 # Optionally open the saved image with the system's default viewer
 if open_after:
  try:
   if platform.system() == "Windows":
    os.startfile(str(img_path))
   elif platform.system() == "Darwin":
    subprocess.run(["open", str(img_path)])
   else:
    subprocess.run(["xdg-open", str(img_path)])
  except Exception:
   pass  # ignore failures to auto-open
 return {"figs": [g.fig], "image": img_path, "table_csv": csv_path}  # return artifacts for pipeline use

if __name__ == "__main__":
 # Standalone execution: try importing prepared DATA; otherwise read from a fallback path
 try: 
  from src.utils import df as DATA
 except Exception: 
  DATA = pd.read_csv("data/clean_gym.csv")
 # Run this step; show the plot interactively; do not auto-open after save
 run(DATA, Path("out"), show=True, open_after=False)
 plt.show()
