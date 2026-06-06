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


def fetch_user_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"

    params = {
        "per_page": 100,
        "sort": "updated"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    repos_data = response.json()
    repositories = []

    for repo in repos_data:
        repositories.append({
            "repo_id": repo["id"],
            "name": repo["name"],
            "full_name": repo["full_name"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "open_issues": repo["open_issues_count"],
            "language": repo["language"],
            "created_at": repo["created_at"],
            "updated_at": repo["updated_at"],
            "html_url": repo["html_url"]
        })

    return pd.DataFrame(repositories)


if __name__ == "__main__":
    df = fetch_user_repositories(USERNAME)

    os.makedirs("data/raw", exist_ok=True)

    output_path = "data/raw/repositories.csv"
    df.to_csv(output_path, index=False)

    print("Repositories collected successfully.")
    print(f"Username: {USERNAME}")
    print(f"Total repositories: {len(df)}")
    print(df.head())