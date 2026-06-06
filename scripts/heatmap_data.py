import pandas as pd
import os

df = pd.read_csv("data/raw/commits.csv")

df["commit_date"] = pd.to_datetime(df["commit_date"])

heatmap = (
    df.groupby(df["commit_date"].dt.date)
    .size()
    .reset_index(name="commit_count")
)

os.makedirs("data/processed", exist_ok=True)

heatmap.to_csv(
    "data/processed/heatmap_data.csv",
    index=False
)

print("Heatmap dataset created.")
print(heatmap.head())