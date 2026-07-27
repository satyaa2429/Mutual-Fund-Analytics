import requests
import pandas as pd
import os

# Dictionary of scheme names and AMFI codes
schemes = {
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

# Create output folder
os.makedirs("data/raw", exist_ok=True)

for scheme_name, scheme_code in schemes.items():

    print("=" * 70)
    print(f"Fetching {scheme_name} ({scheme_code})")

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        nav_df = pd.DataFrame(data["data"])

        filename = f"data/raw/{scheme_name}.csv"

        nav_df.to_csv(filename, index=False)

        print(f"Saved -> {filename}")

    else:
        print(f"Failed ({response.status_code})")

print("\nAll NAV files downloaded successfully!")