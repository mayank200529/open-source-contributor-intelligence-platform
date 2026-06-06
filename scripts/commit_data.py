import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("GITHUB_USERNAME", "mayank200529")
TOKEN = os.getenv("GITHUB_TOKEN")

headers = {}
if TOKEN:
    headers["Authorization"] = f"Bearer {TOKEN}"


repos_df = pd.read_csv("data/raw/repositories.csv")

commits = []

for _, repo in repos_df.iterrows():
    full_name = repo["full_name"]
    url = f"https://api.github.com/repos/{full_name}/commits"

    params = {
        "author": USERNAME,
        "per_page": 100
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Skipped {full_name}: {response.status_code}")
        continue

    data = response.json()

    for commit in data:
        commits.append({
            "repo_name": full_name,
            "commit_sha": commit["sha"],
            "author_name": commit["commit"]["author"]["name"],
            "commit_date": commit["commit"]["author"]["date"],
            "message": commit["commit"]["message"]
        })

df = pd.DataFrame(commits)

os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/commits.csv", index=False)

print("Commit data collected successfully.")
print(f"Total commits: {len(df)}")
print(df.head())