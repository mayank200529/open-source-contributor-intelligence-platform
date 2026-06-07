import os
import pandas as pd

prs_df = pd.read_csv("data/raw/pull_requests.csv")

total_prs = len(prs_df)
open_prs = len(prs_df[prs_df["state"] == "open"])
closed_prs = len(prs_df[prs_df["state"] == "closed"])

closure_rate = (closed_prs / total_prs) * 100 if total_prs > 0 else 0

pr_summary = pd.DataFrame({
    "metric": [
        "Total PRs",
        "Open PRs",
        "Closed PRs",
        "PR Closure Rate"
    ],
    "value": [
        total_prs,
        open_prs,
        closed_prs,
        round(closure_rate, 2)
    ]
})

os.makedirs("data/processed", exist_ok=True)

pr_summary.to_csv(
    "data/processed/pr_analytics.csv",
    index=False
)

print("PR analytics dataset created.")
print(pr_summary)