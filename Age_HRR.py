import pandas as pd                     # data manipulation
import matplotlib.pyplot as plt         # plotting (Matplotlib)
import seaborn as sns                   # statistical plots (Seaborn)
from src.utils import df                # project-specific utility (kept as-is)
from tabulate import tabulate           # pretty tables (not used here but imported)

import os, platform, subprocess         # OS utilities to open files
from pathlib import Path                # filesystem paths (object-oriented)

def run(df: pd.DataFrame, out_dir: Path, show: bool=False, open_after: bool = False):
 # Convert output base to Path and prepare subfolders
 out_dir = Path(out_dir)
 img_dir = out_dir / "img"              # images go here
 tab_dir = out_dir / "tab"              # tables/exports go here
 img_dir.mkdir(parents=True, exist_ok=True)   # ensure image subfolder exists
 tab_dir.mkdir(parents=True, exist_ok=True)   # ensure table subfolder exists 

 # Filter dataset: keep sessions with duration between 0.5 and 1.5 hours
 df_fixed = df[
     (df["Session_Duration (hours)"].between(0.5, 1.5)) 
 ]

 # Aggregate: average HRR by Age
 df_avg = df_fixed.groupby("Age")["HRR"].mean().reset_index()

 # Plot: simple linear-model plot Age vs HRR
 g = sns.lmplot(data=df_avg, x="Age", y="HRR")
 plt.title("Correlation_HRR_and_Age")   # figure title
 plt.tight_layout()                      # avoid layout overlaps

 # Save image to out/img
 img_path = img_dir/"Correlation_HRR_and_Age.png"
 g.savefig(img_path, dpi=300, bbox_inches="tight")

 # Save table to CSV in out/tab
 csv_path = tab_dir/"Correlation_HRR_and_Age.csv"
 df_avg.to_csv(csv_path, index=False)
 try:
  # Also export a Markdown table (if tabulate/markdown support is available)
  md_path = tab_dir/"Correlation_HRR_and_Age.md"
  df_avg.to_markdown(md_path, index=False)
 except Exception:
  md_path = None                         # silently ignore if markdown export fails

 # Display logic:
 if show:
        plt.show(block=True)   # ← this step's window stays open until you close it
 else: 
  plt.close(g.fig)             # close the figure when not showing interactively

 # Optionally open the saved image with the system viewer
 if open_after:
  try:
   if platform.system() == "Windows":
    os.startfile(str(img_path))
   elif platform.system() == "Darwin":
    subprocess.run(["open", str(img_path)])
   else:
    subprocess.run(["xdg-open", str(img_path)])
  except Exception:
   pass                        # ignore failures to auto-open
 return {"figs": [g.fig], "image": img_path, "table_csv": csv_path}  # return artifacts for pipeline

if __name__ == "__main__":
 # Standalone execution: try to import prepared DATA, otherwise read from a fallback path
 try: 
  from src.utils import df as DATA
 except Exception: 
  DATA = pd.read_csv("data/clean_set.csv")  # fallback path (kept as-is)
 # Run the step and show the plot when executed directly
 run(DATA, Path("out"), show=True, open_after=False)
 plt.show()
