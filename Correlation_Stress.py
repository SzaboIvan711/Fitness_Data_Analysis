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
 df_fixed = df
 # Aggregate: average HRR by Age
 df_avg = df_fixed.groupby(["stress_level", "sex"])["vo2max"].mean().reset_index()

 # Plot: regression of workout frequency vs age, colored by gender
 g = sns.lmplot(
     data=df_avg,
     x="stress_level",
     y="vo2max",
     hue="sex",
     col="sex",
     ci=95, 
     palette="Set1"
 )

 g.fig.suptitle("Correlation_stress_level_sex_vo2max")   # figure title
 plt.tight_layout()                      # avoid layout overlaps

 # Save image to out/img
 img_path = img_dir/"Correlation_stress_level_sex_vo2max.png"
 g.savefig(img_path, dpi=300, bbox_inches="tight")

 # Save table to CSV in out/tab
 csv_path = tab_dir/"Correlation_stress_level_sex_vo2max.csv"
 df_avg.to_csv(csv_path, index=False)
 try:
  # Also export a Markdown table (if tabulate/markdown support is available)
  md_path = tab_dir/"Correlation_stress_level_sex_vo2max.md"
  df_avg.to_markdown(md_path, index=False)
 except Exception:
  md_path = None                         # silently ignore if markdown export fails

 # Display logic:
 if show:
        plt.show(block=True)   # ← this step's window stays open until you close it
 else: 
  plt.close(g.fig)             # close the figure when not showing interactively

# Второй агрегат
 df_avg2 = df_fixed.groupby(["stress_level", "sex"])["run_5k_min"].mean().reset_index()

# Построение второго графика
 g2 = sns.lmplot(
    data=df_avg2,
    x="stress_level",
    y="run_5k_min",
    hue="sex",
    col="sex",
    ci=95,
    palette="Set2"
 )

 g2.fig.suptitle("Correlation_stress_level_sex_run_5k_min")
 plt.tight_layout()

# Сохранение второго графика
 img_path2 = img_dir/"Correlation_stress_level_sex_run_5k_mins.png"
 g2.savefig(img_path2, dpi=300, bbox_inches="tight")

# Сохранение таблицы
 csv_path2 = tab_dir/"Correlation_stress_level_sex_run_5k_min.csv"
 df_avg2.to_csv(csv_path2, index=False)

# Markdown-экспорт
 try:
    md_path2 = tab_dir/"Correlation_stress_level_sex_run_5k_min.md"
    df_avg2.to_markdown(md_path2, index=False)
 except Exception:
    md_path2 = None

# Отображение
 if show:
    plt.show(block=True)
 else:
    plt.close(g2.fig)

# 3

 df_avg3 = df_fixed.groupby(["stress_level", "sex"])["resting_hr"].mean().reset_index()

# Построение второго графика
 g3 = sns.lmplot(
    data=df_avg3,
    x="stress_level",
    y="resting_hr",
    hue="sex",
    col="sex",
    ci=95,
    palette="deep"
 )

 g3.fig.suptitle("Correlation_stress_level_sex_resting_hr")
 plt.tight_layout()

# Сохранение второго графика
 img_path3 = img_dir/"Correlation_stress_level_sex_resting_hr.png"
 g3.savefig(img_path3, dpi=300, bbox_inches="tight")

# Сохранение таблицы
 csv_path3 = tab_dir/"Correlation_stress_level_sex_resting_hr.csv"
 df_avg3.to_csv(csv_path3, index=False)

# Markdown-экспорт
 try:
    md_path3 = tab_dir/"Correlation_stress_level_sex_resting_hr.md"
    df_avg3.to_markdown(md_path3, index=False)
 except Exception:
    md_path3 = None

# Отображение
 if show:
    plt.show(block=True)
 else:
    plt.close(g3.fig)

#4

 df_avg4 = df_fixed.groupby(["stress_level", "sex"])["systolic_bp"].mean().reset_index()

# Построение второго графика
 g4 = sns.lmplot(
    data=df_avg4,
    x="stress_level",
    y="systolic_bp",
    hue="sex",
    col="sex",
    ci=95,
    palette="bright"
 )

 g4.fig.suptitle("Correlation_stress_level_sex_systolic_bp")
 plt.tight_layout()

# Сохранение второго графика
 img_path4 = img_dir/"Correlation_stress_level_sex_systolic_bp.png"
 g4.savefig(img_path4, dpi=300, bbox_inches="tight")

# Сохранение таблицы
 csv_path4 = tab_dir/"Correlation_stress_level_sex_systolic_bp.csv"
 df_avg4.to_csv(csv_path4, index=False)

# Markdown-экспорт
 try:
    md_path4 = tab_dir/"Correlation_stress_level_sex_systolic_bp.md"
    df_avg4.to_markdown(md_path4, index=False)
 except Exception:
    md_path4 = None

# Отображение
 if show:
    plt.show(block=True)
 else:
    plt.close(g4.fig)


#5

 df_avg5 = df_fixed.groupby(["stress_level", "sex"])["max_pushups"].mean().reset_index()

 # Plot: regression of workout frequency vs age, colored by gender
 g5 = sns.lmplot(
    data=df_avg5,
    x="stress_level",
    y="max_pushups",
    hue="sex",
    col="sex",
    ci=95,
    palette="Set1"
)

 g5.fig.suptitle("Correlation_stress_level_sex_max_pushups")
 plt.tight_layout()

# Сохранение второго графика
 img_path5 = img_dir/"Correlation_stress_level_sex_max_pushups.png"
 g5.savefig(img_path5, dpi=300, bbox_inches="tight")

# Сохранение таблицы
 csv_path5 = tab_dir/"Correlation_stress_level_sex_max_pushups.csv"
 df_avg5.to_csv(csv_path5, index=False)

# Markdown-экспорт
 try:
    md_path5 = tab_dir/"Correlation_stress_level_sex_max_pushups.md"
    df_avg5.to_markdown(md_path5, index=False)
 except Exception:
    md_path5 = None

# Отображение
 if show:
    plt.show(block=True)
 else:
    plt.close(g5.fig)


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
  DATA = pd.read_csv("data/set.csv")  # fallback path (kept as-is)
 # Run the step and show the plot when executed directly
 run(DATA, Path("out"), show=True, open_after=False)
 plt.show()
