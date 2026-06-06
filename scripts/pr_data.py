import requests
import pandas as pd

USERNAME = "mayank200529"

url = f"https://api.github.com/search/issues?q=author:{USERNAME}+type:pr"

response = requests.get(url)

data = response.json()

prs = []

for item in data.get("items", []):
    prs.append({
        "title": item["title"],
        "state": item["state"],
        "created_at": item["created_at"],
        "updated_at": item["updated_at"],
        "url": item["html_url"]
    })

df = pd.DataFrame(prs)

print(df.head())
print("Total PRs:", len(df))

df.to_csv("data/raw/pull_requests.csv", index=False)