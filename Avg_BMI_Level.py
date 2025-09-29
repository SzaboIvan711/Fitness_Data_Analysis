import pandas as pd                     # data manipulation
import matplotlib.pyplot as plt         # plotting (Matplotlib)
import seaborn as sns                   # statistical visualizations (Seaborn)
from src.utils import df                # project utility (import kept as-is, may be unused here)
from tabulate import tabulate           # table formatting (kept as-is)

import os, platform, subprocess         # OS helpers for opening files
from pathlib import Path                # path handling

def run(df: pd.DataFrame, out_dir: Path, show: bool=False, open_after: bool = False):
 # Prepare output directories (base -> img/ for figures, tab/ for tables)
 out_dir = Path(out_dir)
 img_dir = out_dir / "img"
 tab_dir = out_dir / "tab"
 img_dir.mkdir(parents=True, exist_ok=True)   # ensure image folder exists
 tab_dir.mkdir(parents=True, exist_ok=True)   # ensure table folder exists 

 # Filter dataset: keep sessions with exactly 1.0 hour duration
 df_fixed = df[df["Session_Duration (hours)"] == 1.0]

 # Aggregate: mean Avg_BPM by Experience_Level
 df_avg = df_fixed.groupby("Experience_Level")["Avg_BPM"].mean().reset_index()

 # Plot: bar chart of Avg_BPM per Experience_Level
 fig, ax = plt.subplots(figsize=(6,4))
 ax = sns.barplot(data=df_avg, x="Experience_Level", y="Avg_BPM", hue="Experience_Level", palette="Paired")
 ax.set_title("Correlation_Avg_BPM_and_Level")
 fig.tight_layout()

 # Save figure to out/img
 img_path = img_dir/"Correlation_Avg_BPM_and_Level.png"
 fig.savefig(img_path, dpi=300, bbox_inches="tight")

 # Save aggregated table to CSV in out/tab
 csv_path = tab_dir/"Correlation_Avg_BPM_and_Level.csv"
 df_avg.to_csv(csv_path, index=False)
 try:
  # Optionally save Markdown table (if environment supports to_markdown)
  md_path = tab_dir/"Correlation_Avg_BPM_and_Level.md"
  df_avg.to_markdown(md_path, index=False)
 except Exception:
  md_path = None  # ignore markdown export errors

 # Display behavior: show this plot (blocking) or close it
 if show:
        plt.show(block=True)   # this step's window stays open until you close it
 else: 
  plt.close(fig)

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
 return {"figs": [fig], "image": img_path, "table_csv": csv_path}  # return artifacts for pipeline integration

if __name__ == "__main__":
 # Standalone run: try importing prepared DATA, else read from fallback path
 try: 
  from src.utils import df as DATA
 except Exception: 
  DATA = pd.read_csv("data/clean_set.csv")  # fallback path kept as-is
 # Execute step and show the plot
 run(DATA, Path("out"), show=True, open_after=False)
 plt.show()
