import pandas as pd

# Load correct dataset
trends = pd.read_csv("output/reports/trends.csv")

# clean & sort
trends = trends.sort_values("year")

# growth calculation
trends["growth"] = trends["total_patents"].pct_change()

avg_growth = trends["growth"].mean()
last_value = trends["total_patents"].iloc[-1]

# prediction
future = []

for i in range(1, 4):
    future.append({
        "year": int(trends["year"].max() + i),
        "predicted_patents": int(last_value * (1 + avg_growth) ** i)
    })

pred_df = pd.DataFrame(future)

print("\n PATENT FORECAST")
print(pred_df)

pred_df.to_csv("output/reports/predictions.csv", index=False)