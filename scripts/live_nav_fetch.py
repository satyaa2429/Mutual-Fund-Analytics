import requests
import pandas as pd
import os

# API URL
url = "https://api.mfapi.in/mf/125497"

# Fetch data
response = requests.get(url)

# Check request status
if response.status_code == 200:

    data = response.json()

    print("=" * 70)
    print("Scheme Information")
    print("=" * 70)

    print("Scheme Code :", data["meta"]["scheme_code"])
    print("Scheme Name :", data["meta"]["scheme_name"])
    print("Fund House  :", data["meta"]["fund_house"])

    # Convert NAV history to DataFrame
    nav_df = pd.DataFrame(data["data"])

    # Create folder if not present
    os.makedirs("data/raw", exist_ok=True)

    # Save CSV
    output_path = "data/raw/live_nav_125497.csv"
    nav_df.to_csv(output_path, index=False)

    print("\nCSV Saved Successfully")
    print(output_path)

    print("\nFirst 5 Rows")
    print(nav_df.head())

else:
    print("API Request Failed")
    print("Status Code :", response.status_code)