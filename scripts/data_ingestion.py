import pandas as pd
from pathlib import Path

# Path to raw data folder
DATA_FOLDER = Path("data/raw")

# Get all CSV files
csv_files = sorted(DATA_FOLDER.glob("*.csv"))

print("=" * 80)
print(f"TOTAL CSV FILES FOUND : {len(csv_files)}")
print("=" * 80)

for file in csv_files:

    print("\n" + "=" * 80)
    print(f"FILE : {file.name}")
    print("=" * 80)

    try:
        df = pd.read_csv(file)

        print("\nShape")
        print(df.shape)

        print("\nData Types")
        print(df.dtypes)

        print("\nFirst 5 Rows")
        print(df.head())

        print("\nMissing Values")
        print(df.isnull().sum())

        print("\nDuplicate Rows")
        print(df.duplicated().sum())

        print("\nColumns")
        print(list(df.columns))

    except Exception as e:
        print(f"Error reading {file.name}")
        print(e)

print("\nData Ingestion Completed Successfully.")