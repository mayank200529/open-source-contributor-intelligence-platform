import os
import pandas as pd

prs_df = pd.read_csv("data/raw/pull_requests.csv")
commits_df = pd.read_csv("data/raw/commits.csv")

USERNAME = "mayank200529"

total_prs = len(prs_df)
open_prs = len(prs_df[prs_df["state"] == "open"])
closed_prs = len(prs_df[prs_df["state"] == "closed"])
total_commits = len(commits_df)

activity_score = (
    total_commits * 0.4
    + total_prs * 0.4
    + closed_prs * 0.2
)

ranking_df = pd.DataFrame({
    "contributor": [USERNAME],
    "total_commits": [total_commits],
    "total_prs": [total_prs],
    "open_prs": [open_prs],
    "closed_prs": [closed_prs],
    "activity_score": [round(activity_score, 2)],
    "rank": [1]
})

os.makedirs("data/processed", exist_ok=True)

ranking_df.to_csv(
    "data/processed/contributor_ranking.csv",
    index=False
)

print("Contributor ranking dataset created.")
print(ranking_df)