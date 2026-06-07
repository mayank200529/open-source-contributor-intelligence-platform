import pandas as pd
import os

repos_df = pd.read_csv("data/raw/repositories.csv")

repos_df["health_score"] = (
    repos_df["stars"] * 5
    + repos_df["forks"] * 3
    + repos_df["open_issues"] * 1
)

repos_df = repos_df.sort_values(
    by="health_score",
    ascending=False
)

os.makedirs("data/processed", exist_ok=True)

repos_df.to_csv(
    "data/processed/repository_health.csv",
    index=False
)

print("Repository Health Dataset Created")
print(
    repos_df[
        ["name", "stars", "forks", "health_score"]
    ].head()
)