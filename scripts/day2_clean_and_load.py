from pathlib import Path
import sqlite3

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DB_PATH = BASE_DIR / "bluestock_mf.db"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_nav_history() -> pd.DataFrame:
    file_path = RAW_DIR / "02_nav_history.csv"
    df = pd.read_csv(file_path)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

    df = df.drop_duplicates()
    df = df.dropna(subset=["amfi_code", "date"])
    df = df.sort_values(["amfi_code", "date"])

    df["nav"] = df.groupby("amfi_code")["nav"].ffill()

    df = df[df["nav"] > 0]

    output = PROCESSED_DIR / "02_nav_history_cleaned.csv"
    df.to_csv(output, index=False)

    print(f"NAV cleaned: {df.shape}")
    return df


def clean_investor_transactions() -> pd.DataFrame:
    file_path = RAW_DIR / "08_investor_transactions.csv"
    df = pd.read_csv(file_path)

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"], errors="coerce"
    )

    df["transaction_type"] = (
        df["transaction_type"]
        .astype(str)
        .str.strip()
        .str.title()
        .replace(
            {
                "Sip": "SIP",
                "Lumpsum": "Lumpsum",
                "Redemption": "Redemption",
            }
        )
    )

    valid_types = {"SIP", "Lumpsum", "Redemption"}
    df = df[df["transaction_type"].isin(valid_types)]

    df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="coerce")
    df = df[df["amount_inr"] > 0]

    df["kyc_status"] = df["kyc_status"].astype(str).str.strip().str.title()
    valid_kyc = {"Verified", "Pending", "Rejected"}
    df = df[df["kyc_status"].isin(valid_kyc)]

    df = df.drop_duplicates()
    df = df.dropna(subset=["investor_id", "transaction_date", "amfi_code"])

    output = PROCESSED_DIR / "08_investor_transactions_cleaned.csv"
    df.to_csv(output, index=False)

    print(f"Transactions cleaned: {df.shape}")
    return df


def clean_scheme_performance() -> pd.DataFrame:
    file_path = RAW_DIR / "07_scheme_performance.csv"
    df = pd.read_csv(file_path)

    numeric_columns = [
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "max_drawdown_pct",
        "aum_crore",
        "expense_ratio_pct",
        "morningstar_rating",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    if "expense_ratio_pct" in df.columns:
        df["expense_ratio_anomaly"] = ~df["expense_ratio_pct"].between(
            0.1, 2.5, inclusive="both"
        )

    df = df.drop_duplicates()
    df = df.dropna(subset=["amfi_code", "scheme_name"])

    output = PROCESSED_DIR / "07_scheme_performance_cleaned.csv"
    df.to_csv(output, index=False)

    print(f"Performance cleaned: {df.shape}")
    return df


def copy_other_csvs() -> None:
    for source in RAW_DIR.glob("*.csv"):
        if source.name.startswith(("02_", "07_", "08_")):
            continue

        target = PROCESSED_DIR / source.name
        pd.read_csv(source).to_csv(target, index=False)


def load_to_sqlite(
    nav: pd.DataFrame,
    transactions: pd.DataFrame,
    performance: pd.DataFrame,
) -> None:
    fund_master = pd.read_csv(RAW_DIR / "01_fund_master.csv")
    aum = pd.read_csv(RAW_DIR / "03_aum_by_fund_house.csv")

    connection = sqlite3.connect(DB_PATH)

    try:
        fund_master.to_sql(
            "dim_fund", connection, if_exists="replace", index=False
        )
        nav.to_sql("fact_nav", connection, if_exists="replace", index=False)
        transactions.to_sql(
            "fact_transactions",
            connection,
            if_exists="replace",
            index=False,
        )
        performance.to_sql(
            "fact_performance",
            connection,
            if_exists="replace",
            index=False,
        )
        aum.to_sql("fact_aum", connection, if_exists="replace", index=False)

        print("\nSQLite tables loaded:")
        for table in [
            "dim_fund",
            "fact_nav",
            "fact_transactions",
            "fact_performance",
            "fact_aum",
        ]:
            count = pd.read_sql_query(
                f"SELECT COUNT(*) AS row_count FROM {table}",
                connection,
            )["row_count"].iloc[0]

            print(f"{table}: {count}")
    finally:
        connection.close()


def main() -> None:
    nav = clean_nav_history()
    transactions = clean_investor_transactions()
    performance = clean_scheme_performance()

    copy_other_csvs()
    load_to_sqlite(nav, transactions, performance)

    print("\nDay 2 cleaning and SQLite loading completed successfully.")


if __name__ == "__main__":
    main()