import pandas as pd
from sklearn.ensemble import RandomForestClassifier

commits = pd.read_csv("data/raw/commits.csv")

activity = (
    commits.groupby("repo_name")
    .size()
    .reset_index(name="commit_count")
)

activity["active_next_month"] = (
    activity["commit_count"] > 5
).astype(int)

X = activity[["commit_count"]]
y = activity["active_next_month"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

activity["prediction"] = model.predict(X)

activity.to_csv(
    "data/processed/retention_predictions.csv",
    index=False
)

print(activity.head())
print("Retention model trained successfully.")