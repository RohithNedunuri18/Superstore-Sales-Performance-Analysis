import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
sns.set_theme(style="whitegrid")
pd.set_option("display.width", 100); pd.set_option("display.max_columns", 12)
print("pandas", pd.__version__)

df = pd.read_csv("Sample - Superstore.csv", parse_dates=["Order Date"], encoding="cp1252")

print(df.dtypes.to_string())
print("\nMissing values:", int(df.isna().sum().sum()), "| Duplicates:", int(df.duplicated().sum()))
df = df.drop_duplicates().dropna()
df["Year"], df["Month"] = df["Order Date"].dt.year, df["Order Date"].dt.month
df["Margin %"] = df["Profit"] / df["Sales"] * 100
print(df[["Sales", "Profit", "Discount"]].describe().round(2).to_string())

monthly = df.set_index("Order Date").resample("MS")[["Sales", "Profit"]].sum()
monthly.plot(figsize=(9, 4), marker="o", title="Monthly Sales and Profit")
plt.ylabel("Amount"); plt.tight_layout(); plt.show()
print(monthly.tail(6).round(0).to_string())

season = df.groupby(["Year", "Month"])["Sales"].sum().groupby("Month").mean()
season.plot(kind="bar", figsize=(9, 4), color="#4C78A8", title="Average Sales by Calendar Month")
plt.xlabel("Month"); plt.tight_layout(); plt.show()
print("Peak months:", season.nlargest(3).round(0).to_dict())
print("Slowest months:", season.nsmallest(3).round(0).to_dict())

for col in ["Category", "Segment", "Region"]:
    t = df.groupby(col).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).round(0)
    t["Margin %"] = (t["Profit"] / t["Sales"] * 100).round(1)
    print(t.sort_values("Profit", ascending=False).to_string(), "\n")
df.groupby("Category")["Profit"].sum().sort_values().plot(kind="barh", color="#54A24B", figsize=(7, 3), title="Total Profit by Category")
plt.tight_layout(); plt.show()

bucket = df.groupby("Discount").agg(
    Orders=("Order ID", "nunique"),
    Line_Items=("Sales", "size"),
    Sales=("Sales", "sum"),
    TotalProfit=("Profit", "sum")
)

bucket["Profit Margin %"] = (
    bucket["TotalProfit"] / bucket["Sales"] * 100
).round(2)

print(bucket.round(2).to_string())

print("\nCorrelation Discount vs Margin %:",
      round(df["Discount"].corr(df["Margin %"]), 3))

bucket["Profit Margin %"].plot(
    kind="bar",
    color="#E45756",
    figsize=(7, 3.5),
    title="Profit Margin % by Discount Level"
)

plt.axhline(0, color="black", lw=1)
plt.ylabel("Profit Margin %")
plt.tight_layout()
plt.show()

best = season.idxmax()
loss = bucket[bucket["Profit Margin %"] < 0].index.min()
print(f"1. Sales peak in month {best}; plan inventory and campaigns ahead of Q4.")
print(f"2. Best category by profit: {df.groupby('Category')['Profit'].sum().idxmax()}.")
print(f"3. Discount levels from {loss:.0%} show negative overall profit margins in this dataset.")
df.to_csv("sales_clean.csv", index=False); print("Saved sales_clean.csv")
