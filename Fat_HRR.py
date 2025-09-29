import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
from src.utils import df 
from tabulate import tabulate 

import os, platform, subprocess
from pathlib import Path 

def run(df: pd.DataFrame, out_dir: Path, show: bool=False, open_after: bool = False):
 # Normalize base output path and ensure subfolders for images/tables exist
 out_dir = Path(out_dir)
 img_dir = out_dir / "img"
 tab_dir = out_dir / "tab"
 img_dir.mkdir(parents=True, exist_ok=True)
 tab_dir.mkdir(parents=True, exist_ok=True) 

 # Filter dataset: keep sessions with duration between 0.5 and 1.5 hours
 df_fixed = df[
     (df["Session_Duration (hours)"].between(0.5, 1.5)) 
 ]

 # Create categorical fat groups from Fat_Percentage (low/mean/high)
 # NOTE: This assigns into a slice of the original DataFrame; pandas may warn about SettingWithCopy.
 df_fixed['Fat_Group'] = pd.cut(df_fixed['Fat_Percentage'], bins=[10, 17, 23, 35], labels=['low', 'mean', 'high'])

 # Aggregate: mean HRR by Age and Fat_Group
 df_avg = df_fixed.groupby(["Age", "Fat_Group"])["HRR"].mean().reset_index()

 # Plot: regression of HRR vs Age; facets by Fat_Group; color by Fat_Group
 g = sns.lmplot(data=df_avg, x="Age", y="HRR", col="Fat_Group", hue="Fat_Group", palette="Set1")
 g.fig.suptitle("Correlation_HHR_and_Fat")   # overall figure title
 plt.tight_layout()                           # reduce overlaps in layout

 # Save image output to out/img
 img_path = img_dir/"Correlation_HHR_and_Fat.png"
 g.savefig(img_path, dpi=300, bbox_inches="tight")

 # Save aggregated table to CSV (and Markdown if available) in out/tab
 csv_path = tab_dir/"Correlation_HHR_and_Fat.csv"
 df_avg.to_csv(csv_path, index=False)
 try:
  md_path = tab_dir/"Correlation_HHR_and_Fat.md"
  df_avg.to_markdown(md_path, index=False)
 except Exception:
  md_path = None 

 # Display behavior: show and block until closed, or close figure when not showing
 if show:
        plt.show(block=True)   # this step's window stays open until you close it
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
   pass

 # Return artifacts for pipeline integration (figure handle and file paths)
 return {"figs": [g.fig], "image": img_path, "table_csv": csv_path}

if __name__ == "__main__":
 # Standalone execution: try loading prepared DATA; otherwise use fallback path
 try: 
  from src.utils import df as DATA
 except Exception: 
  DATA = pd.read_csv("data/clean_gym.csv")
 # Run this step; show interactively; do not auto-open after saving
 run(DATA, Path("out"), show=True, open_after=False)
 plt.show()
