import pandas as pd
import os

df = pd.read_csv("data/raw/commits.csv")

df["commit_date"] = pd.to_datetime(df["commit_date"])

df["day"] = df["commit_date"].dt.day_name()
df["month"] = df["commit_date"].dt.month_name()

daily_activity = (
    df.groupby("day")
    .size()
    .reset_index(name="commit_count")
)

monthly_activity = (
    df.groupby("month")
    .size()
    .reset_index(name="commit_count")
)

os.makedirs("data/processed", exist_ok=True)

daily_activity.to_csv(
    "data/processed/daily_activity.csv",
    index=False
)

monthly_activity.to_csv(
    "data/processed/monthly_activity.csv",
    index=False
)

print("Most Active Day:")
print(daily_activity.sort_values(
    "commit_count",
    ascending=False
).head(1))

print("\nMost Active Month:")
print(monthly_activity.sort_values(
    "commit_count",
    ascending=False
).head(1))