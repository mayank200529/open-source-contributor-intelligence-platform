import pandas as pd

repos_df = pd.read_csv("data/raw/repositories.csv")
prs_df = pd.read_csv("data/raw/pull_requests.csv")

total_repos = len(repos_df)
total_stars = repos_df["stars"].sum()
total_forks = repos_df["forks"].sum()
top_language = repos_df["language"].mode()[0]

total_prs = len(prs_df)
open_prs = len(prs_df[prs_df["state"] == "open"])
closed_prs = len(prs_df[prs_df["state"] == "closed"])

productivity_score = (total_prs * 0.5) + (total_repos * 0.3) + (total_stars * 0.2)

print("===== Open Source Analytics KPIs =====")
print(f"Total Repositories: {total_repos}")
print(f"Total Stars: {total_stars}")
print(f"Total Forks: {total_forks}")
print(f"Top Language: {top_language}")
print(f"Total PRs: {total_prs}")
print(f"Open PRs: {open_prs}")
print(f"Closed PRs: {closed_prs}")
print(f"Productivity Score: {round(productivity_score, 2)}")