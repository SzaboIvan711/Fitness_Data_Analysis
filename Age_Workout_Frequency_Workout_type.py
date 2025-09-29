import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
from src.utils import df 
from tabulate import tabulate 

import os, platform, subprocess
from pathlib import Path 

# Step: define the pipeline step; receives a DataFrame and an output base folder
def run(df: pd.DataFrame, out_dir: Path, show: bool=False, open_after: bool = False):
 # Step: normalize output path and prepare subfolders for images and tables
 out_dir = Path(out_dir)
 img_dir = out_dir / "img"
 tab_dir = out_dir / "tab"
 img_dir.mkdir(parents=True, exist_ok=True)
 tab_dir.mkdir(parents=True, exist_ok=True) 

 # Step: filter dataset — keep sessions with duration between 0.5 and 1.5 hours
 df_fixed = df[
     (df["Session_Duration (hours)"].between(0.5, 1.5))
 ]

 # Step: aggregate — average workout frequency by Age and Workout_Type
 df_avg = df_fixed.groupby(["Age", "Workout_Type"])["Workout_Frequency (days/week)"].mean().reset_index()

 # Step: plot — regression of workout frequency vs age, faceted and colored by workout type
 g = sns.lmplot(
     data=df_avg,
     x="Age",
     y="Workout_Frequency (days/week)",
     hue="Workout_Type",
     ci=95, 
     col="Workout_Type",
     palette="Set1"
 )
 g.fig.suptitle("Average_HRR_vs_Age_by_Gender")  # overall figure title for the FacetGrid
 plt.tight_layout()                               # improve spacing to avoid overlaps

 # Step: save image to out/img
 img_path = img_dir/"Average_HRR_vs_Age_by_Gender.png"
 g.savefig(img_path, dpi=300, bbox_inches="tight")

 # Step: export aggregated table to CSV (and Markdown if available) in out/tab
 csv_path = tab_dir/"Average_HRR_vs_Age_by_Gender.csv"
 df_avg.to_csv(csv_path, index=False)
 try:
  md_path = tab_dir/"Average_HRR_vs_Age_by_Gender.md"
  df_avg.to_markdown(md_path, index=False)
 except Exception:
  md_path = None 

 # Step: display logic — show this figure interactively or close it
 if show:
        plt.show(block=True)   # ← this step's window stays open until you close it
 else: 
  plt.close(g.fig)

 # Step: optionally open the saved image with the system's default viewer
 if open_after:
  try:
   if platform.system() == "Windows":
    os.startfile(str(img_path))
   elif platform.system() == "Darwin":
    subprocess.run(["open", str(img_path)])
   else:
    subprocess.run(["xdg-open", str(img_path)])
  except Exception:
   pass

 # Step: return artifacts for the pipeline (figure handle and file paths)
 return {"figs": [g.fig], "image": img_path, "table_csv": csv_path}

# Standalone execution: load data and run this step directly
if __name__ == "__main__":
 try: 
  from src.utils import df as DATA
 except Exception: 
  DATA = pd.read_csv("data/clean_set.csv")
 run(DATA, Path("out"), show=True, open_after=False)
 plt.show()
