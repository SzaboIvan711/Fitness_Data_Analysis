import pandas as pd                     # data manipulation
import matplotlib.pyplot as plt         # plotting (Matplotlib)
import seaborn as sns                   # statistical visualizations (Seaborn)
from src.utils import df                # project-specific utility (kept as-is)
from tabulate import tabulate           # pretty tables (not directly used here)

import os, platform, subprocess         # OS helpers for opening files cross-platform
from pathlib import Path                # path handling (object-oriented)

def run(df: pd.DataFrame, out_dir: Path, show: bool=False, open_after: bool = False):
 # Normalize output base and ensure subfolders exist
 out_dir = Path(out_dir)
 img_dir = out_dir / "img"              # images will be saved here
 tab_dir = out_dir / "tab"              # tables/exports will be saved here
 img_dir.mkdir(parents=True, exist_ok=True)   # ensure image directory exists
 tab_dir.mkdir(parents=True, exist_ok=True)   # ensure table directory exists 

 # Filter dataset: keep rows where Weight is between 60 and 80 kg
 df_fixed = df[
     (df["Weight (kg)"].between(60, 80))
 ]
# Step 2: group by workout type and compute the mean
 df_avg = df_fixed.groupby("Workout_Type")["Calories_per_hour"].mean().reset_index()

 # Plot: bar chart of average Calories_per_hour by Workout_Type
 fig, ax = plt.subplots(figsize=(6,4))
 ax = sns.barplot(data=df_avg, x="Workout_Type", y="Calories_per_hour", palette="Set2")
 ax.set_title("Correlation_Duration_Type_and_Calories")  # figure title
 fig.tight_layout()                                      # prevent label overlap

 # Save figure to out/img
 img_path = img_dir/"Correlation_Duration_Type_and_Calories.png"
 fig.savefig(img_path, dpi=300, bbox_inches="tight")

 # Save aggregated table to CSV in out/tab
 csv_path = tab_dir/"Correlation_Duration_Type_and_Calories.csv"
 df_avg.to_csv(csv_path, index=False)
 try:
  # Optionally export as Markdown (if environment supports to_markdown)
  md_path = tab_dir/"Correlation_Duration_Type_and_Calories.md"
  df_avg.to_markdown(md_path, index=False)
 except Exception:
  md_path = None  # silently ignore Markdown export failures

 # Display behavior: show interactively (blocking) or close when not showing
 if show:
        plt.show(block=True)   # ← this step's window stays open until you close it
 else: 
  plt.close(fig)

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
   pass
 return {"figs": [fig], "image": img_path, "table_csv": csv_path}  # return artifacts for pipeline integration

if __name__ == "__main__":
 # Standalone execution: try to import prepared DATA; otherwise read from fallback path
 try: 
  from src.utils import df as DATA
 except Exception: 
  DATA = pd.read_csv("data/clean_set.csv")
 # Run the step; show the plot; do not auto-open after save
 run(DATA, Path("out"), show=True, open_after=False)
 plt.show()
