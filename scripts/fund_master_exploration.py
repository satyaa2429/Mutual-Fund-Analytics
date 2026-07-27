import pandas as pd

# Load fund master
df = pd.read_csv("data/raw/01_fund_master.csv")

print("=" * 70)
print("DATASET INFORMATION")
print("=" * 70)

print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())

print("\nUnique Fund Houses:")
print(df["fund_house"].unique())

print("\nUnique Categories:")
print(df["category"].unique())

print("\nUnique Sub Categories:")
print(df["sub_category"].unique())

print("\nUnique Risk Grades:")
print(df["risk_category"].unique())