# Pipeline.py
from pathlib import Path
import argparse                       # command-line argument parsing
import pandas as pd                   # data loading/manipulation
import matplotlib.pyplot as plt       # plotting (some steps may open figures)

# Import step modules (each exposes a `run(df, out_dir, show=...)` function)
import  Correlation_Stress, Correlation_Sleep, Correlation_Alcohol, Correlation_Smoking, Basic_PhysiologicalConnections

# Registry of pipeline steps: keys are CLI names, values are callables to execute
STEPS = {
    "Correlation_Stress": Correlation_Stress.run,
    "Correlation_Sleep": Correlation_Sleep.run,
    "Correlation_Alcohol": Correlation_Alcohol.run,
    "Correlation_Smoking": Correlation_Smoking.run,
    "Basic_PhysiologicalConnections": Basic_PhysiologicalConnections.run

}

def main():
    p = argparse.ArgumentParser()  # build CLI parser
    p.add_argument("--data", default="data/set.csv")  # path to the input CSV dataset
    p.add_argument("--out",  default="out")   # base output folder; steps themselves write to out/img and out/tab
    p.add_argument("--steps", default="all")  # "all" or a comma-separated list of step keys e.g. "hrr_age_gender,Avg_BMI_Level"
    p.add_argument("--show", action="store_true",
                   help="show windows SEQUENTIALLY (each step blocks until you close it)")  # translated help text
    args = p.parse_args()  # parse arguments from the command line

    df = pd.read_csv(args.data)  # load the dataset once and reuse across steps
    out_dir = Path(args.out); out_dir.mkdir(parents=True, exist_ok=True)  # ensure base output directory exists

    # Resolve which steps to run based on --steps
    steps_to_run = list(STEPS.keys()) if args.steps == "all" \
        else [s.strip() for s in args.steps.split(",") if s.strip()]

    # Execute each selected step in order
    for name in steps_to_run:
        print(f">>> Running: {name}")  # progress log
        res = STEPS[name](df=df, out_dir=out_dir, show=args.show)  # run step; may return dict of artifacts
        if isinstance(res, dict):
            # Print returned artifact paths (e.g., figures, images, tables) for quick inspection
            for k, v in res.items():
                if v: print(f"    {k}: {v}")
        # Close any figures left open by the step (useful when --show is False)
        import matplotlib.pyplot as plt
        plt.close('all')

if __name__ == "__main__":  # script entry point
    main()
