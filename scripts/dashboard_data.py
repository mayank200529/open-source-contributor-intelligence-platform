import os
import pandas as pd

repos_df = pd.read_csv("data/raw/repositories.csv")
prs_df = pd.read_csv("data/raw/pull_requests.csv")

summary = {
    "total_repositories": [len(repos_df)],
    "total_stars": [repos_df["stars"].sum()],
    "total_forks": [repos_df["forks"].sum()],
    "total_prs": [len(prs_df)],
    "open_prs": [len(prs_df[prs_df["state"] == "open"])],
    "closed_prs": [len(prs_df[prs_df["state"] == "closed"])],
    "top_language": [repos_df["language"].mode()[0]],
}

dashboard_df = pd.DataFrame(summary)

os.makedirs("data/processed", exist_ok=True)

dashboard_df.to_csv("data/processed/dashboard_summary.csv", index=False)

print("Dashboard summary dataset created successfully.")
print(dashboard_df)