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
 df_avg = df_fixed.groupby(["smoker", "sex"])["vo2max"].mean().reset_index()

 # Plot: regression of workout frequency vs age, colored by gender
 fig, ax = plt.subplots(figsize=(6,4))
 ax = sns.barplot(
     data=df_avg,
     x="smoker",
     y="vo2max",
     hue="sex",
     palette="Set1"
 )

 ax.set_title("Correlation_smoker_sex_vo2max")   # figure title
 fig.tight_layout()                      # avoid layout overlaps

 # Save image to out/img
 img_path = img_dir/"Correlation_smoker_sex_vo2max.png"
 fig.savefig(img_path, dpi=300, bbox_inches="tight")

 # Save table to CSV in out/tab
 csv_path = tab_dir/"Correlation_smoker_sex_vo2max.csv"
 df_avg.to_csv(csv_path, index=False)
 try:
  # Also export a Markdown table (if tabulate/markdown support is available)
  md_path = tab_dir/"Correlation_smoker_sex_vo2max.md"
  df_avg.to_markdown(md_path, index=False)
 except Exception:
  md_path = None                         # silently ignore if markdown export fails

 # Display logic:
 if show:
        plt.show(block=True)   # ← this step's window stays open until you close it
 else: 
  plt.close(fig)             # close the figure when not showing interactively

# Второй агрегат
 df_avg2 = df_fixed.groupby(["smoker", "sex"])["run_5k_min"].mean().reset_index()

# Построение второго графика
 fig2, ax2 = plt.subplots(figsize=(6,4))
 ax2 = sns.barplot(
     data=df_avg2,
     x="smoker",
     y="run_5k_min",
     hue="sex",
     palette="Set2"
 )

 ax2.set_title("Correlation_smoker_sex_run_5k_min")   # figure title
 fig.tight_layout()                      # avoid layout overlaps

 # Save image to out/img
 img_path = img_dir/"Correlation_smoker_sex_run_5k_min.png"
 fig2.savefig(img_path, dpi=300, bbox_inches="tight")

# Сохранение таблицы
 csv_path2 = tab_dir/"Correlation_smoker_sex_run_5k_min.csv"
 df_avg2.to_csv(csv_path2, index=False)

# Markdown-экспорт
 try:
    md_path2 = tab_dir/"Correlation_smoker_sex_run_5k_min.md"
    df_avg2.to_markdown(md_path2, index=False)
 except Exception:
    md_path2 = None

# Отображение
 if show:
    plt.show(block=True)
 else:
    plt.close(fig)

# 3

 df_avg3 = df_fixed.groupby(["smoker", "sex"])["resting_hr"].mean().reset_index()

 fig3, ax3 = plt.subplots(figsize=(6,4))
 ax3 = sns.barplot(
     data=df_avg3,
     x="smoker",
     y="resting_hr",
     hue="sex",
     palette="deep"
 )

 ax3.set_title("Correlation_smoker_sex_run_resting_hr")   # figure title
 fig.tight_layout()                      # avoid layout overlaps

 # Save image to out/img
 img_path = img_dir/"Correlation_smoker_sex_run_resting_hr.png"
 fig3.savefig(img_path, dpi=300, bbox_inches="tight")


# Сохранение таблицы
 csv_path3 = tab_dir/"Correlation_smoker_sex_resting_hr.csv"
 df_avg3.to_csv(csv_path3, index=False)

# Markdown-экспорт
 try:
    md_path3 = tab_dir/"Correlation_smoker_sex_resting_hr.md"
    df_avg3.to_markdown(md_path3, index=False)
 except Exception:
    md_path3 = None

# Отображение
 if show:
    plt.show(block=True)
 else:
    plt.close(fig)

#4

 df_avg4 = df_fixed.groupby(["smoker", "sex"])["ldl_mg_dL"].mean().reset_index()

# Построение второго графика
 fig4, ax4 = plt.subplots(figsize=(6,4))
 ax4 = sns.barplot(
     data=df_avg4,
     x="smoker",
     y="ldl_mg_dL",
     hue="sex",
     palette="bright"
 )

 ax3.set_title("Correlation_smoker_sex_run_ldl_mg_dL")   # figure title
 fig.tight_layout()                      # avoid layout overlaps

 # Save image to out/img
 img_path = img_dir/"Correlation_smoker_sex_ldl_mg_dL.png"
 fig3.savefig(img_path, dpi=300, bbox_inches="tight")

# Сохранение таблицы
 csv_path4 = tab_dir/"Correlation_smoker_sex_ldl_mg_dL.csv"
 df_avg4.to_csv(csv_path4, index=False)

# Markdown-экспорт
 try:
    md_path4 = tab_dir/"Correlation_smoker_sex_ldl_mg_dL.md"
    df_avg4.to_markdown(md_path4, index=False)
 except Exception:
    md_path4 = None

# Отображение
 if show:
    plt.show(block=True)
 else:
    plt.close(fig)


#5

 df_avg5 = df_fixed.groupby(["smoker", "sex"])["hdl_mg_dL"].mean().reset_index()

# Построение второго графика
 fig5, ax5 = plt.subplots(figsize=(6,4))
 ax5 = sns.barplot(
     data=df_avg5,
     x="smoker",
     y="hdl_mg_dL",
     hue="sex",
     palette="Set1"
 )

 ax5.set_title("Correlation_smoker_sex_run_hdl_mg_dL")   # figure title
 fig5.tight_layout()                      # avoid layout overlaps

 # Save image to out/img
 img_path = img_dir/"Correlation_smoker_sex_hdl_mg_dL.png"
 fig5.savefig(img_path, dpi=300, bbox_inches="tight")

# Сохранение таблицы
 csv_path5 = tab_dir/"Correlation_smoker_sex_hdl_mg_dL.csv"
 df_avg5.to_csv(csv_path5, index=False)

# Markdown-экспорт
 try:
    md_path5 = tab_dir/"Correlation_smoker_sex_ldl_mg_dL.md"
    df_avg5.to_markdown(md_path5, index=False)
 except Exception:
    md_path5 = None

# Отображение
 if show:
    plt.show(block=True)
 else:
    plt.close(fig)

#6

 df_avg6 = df_fixed.groupby(["smoker", "sex"])["triglycerides_mg_dL"].mean().reset_index()

 # Plot: regression of workout frequency vs age, colored by gender
 fig6, ax6 = plt.subplots(figsize=(6,4))
 ax6 = sns.barplot(
     data=df_avg6,
     x="smoker",
     y="triglycerides_mg_dL",
     hue="sex",
     palette="Set2"
 )

 ax6.set_title("Correlation_smoker_sex_triglycerides_mg_dL")   # figure title
 fig6.tight_layout()                      # avoid layout overlaps

 # Save image to out/img
 img_path = img_dir/"Correlation_smoker_sex_triglycerides_mg_dL.png"
 fig6.savefig(img_path, dpi=300, bbox_inches="tight")

# Сохранение таблицы
 csv_path6 = tab_dir/"Correlation_smoker_sex_triglycerides_mg_dL.csv"
 df_avg6.to_csv(csv_path6, index=False)

# Markdown-экспорт
 try:
    md_path6 = tab_dir/"Correlation_smoker_sex_triglycerides_mg_dL.md"
    df_avg6.to_markdown(md_path6, index=False)
 except Exception:
    md_path6 = None

# Отображение
 if show:
    plt.show(block=True)
 else:
    plt.close(fig)

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
 return {"figs": [fig], "image": img_path, "table_csv": csv_path}  # return artifacts for pipeline

if __name__ == "__main__":
 # Standalone execution: try to import prepared DATA, otherwise read from a fallback path
 try: 
  from src.utils import df as DATA
 except Exception: 
  DATA = pd.read_csv("data/set.csv")  # fallback path (kept as-is)
 # Run the step and show the plot when executed directly
 run(DATA, Path("out"), show=True, open_after=False)
 plt.show()
