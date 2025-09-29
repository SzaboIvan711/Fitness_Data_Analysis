import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
from src.utils import df 
from tabulate import tabulate 

import os, platform, subprocess
from pathlib import Path 

def run(df: pd.DataFrame, out_dir: Path, show: bool=False, open_after: bool = False):
 # Convert base output path to Path and ensure subfolders exist
 out_dir = Path(out_dir)
 img_dir = out_dir / "img"     # images will be saved here
 tab_dir = out_dir / "tab"     # tabular exports (csv/md) will be saved here
 img_dir.mkdir(parents=True, exist_ok=True)   # make sure image folder exists
 tab_dir.mkdir(parents=True, exist_ok=True)   # make sure table folder exists 

 # Filter dataset: keep sessions with duration between 0.5 and 1.5 hours
 df_fixed = df[
     (df["Session_Duration (hours)"].between(0.5, 1.5))
 ]

 # Aggregate: average workout frequency by Age and Gender
 df_avg = df_fixed.groupby(["Age", "Gender"])["Workout_Frequency (days/week)"].mean().reset_index()

 # Plot: regression of workout frequency vs age, colored by gender
 g = sns.lmplot(
     data=df_avg,
     x="Age",
     y="Workout_Frequency (days/week)",
     hue="Gender",
     col="Gender",
     ci=95, 
     palette="Set1"
 )
 g.fig.suptitle("Correlation_Age_Gender_and_Frequency")  # figure title

 # Save image (PNG) to out/img
 img_path = img_dir/"Correlation_Age_Gender_and_Frequency.png"
 g.savefig(img_path, dpi=300, bbox_inches="tight")
 plt.tight_layout()  # improve layout after plotting/saving

 # Save aggregated table to CSV in out/tab
 csv_path = tab_dir/"Correlation_Age_Gender_and_Frequency.csv"
 df_avg.to_csv(csv_path, index=False)
 try:
  # Optional: also save Markdown table (if supported in the environment)
  md_path = tab_dir/"Correlation_Age_Gender_and_Frequency.md"
  df_avg.to_markdown(md_path, index=False)
 except Exception:
  md_path = None   # ignore markdown export errors silently

 # Display behavior:
 if show:
        plt.show(block=True)   # show this figure and block until the window is closed
 else: 
  plt.close(g.fig)             # close when not showing interactively

 # Optionally open the saved image with the default system viewer
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
 return {"figs": [g.fig], "image": img_path, "table_csv": csv_path}  # return artifacts for pipeline integration

if __name__ == "__main__":
 # Standalone execution: try to import prepared DATA, else read from fallback path
 try: 
  from src.utils import df as DATA
 except Exception: 
  DATA = pd.read_csv("data/clean_set.csv")
 # Run step with showing enabled; do not auto-open after save
 run(DATA, Path("out"), show=True, open_after=False)
 plt.show()
