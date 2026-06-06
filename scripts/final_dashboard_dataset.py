import os
import pandas as pd

repos_df = pd.read_csv("data/raw/repositories.csv")
prs_df = pd.read_csv("data/raw/pull_requests.csv")
commits_df = pd.read_csv("data/raw/commits.csv")

total_repos = len(repos_df)
total_prs = len(prs_df)
total_commits = len(commits_df)
open_prs = len(prs_df[prs_df["state"] == "open"])
closed_prs = len(prs_df[prs_df["state"] == "closed"])

productivity_score = (total_prs * 0.5) + (total_commits * 0.3) + (total_repos * 0.2)

summary = pd.DataFrame({
    "metric": [
        "Total Repositories",
        "Total Pull Requests",
        "Open Pull Requests",
        "Closed Pull Requests",
        "Total Commits",
        "Productivity Score"
    ],
    "value": [
        total_repos,
        total_prs,
        open_prs,
        closed_prs,
        total_commits,
        round(productivity_score, 2)
    ]
})

os.makedirs("data/processed", exist_ok=True)

summary.to_csv("data/processed/final_dashboard_summary.csv", index=False)

print("Final dashboard dataset created successfully.")
print(summary)