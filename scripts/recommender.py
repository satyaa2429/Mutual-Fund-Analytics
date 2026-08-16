from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"


def recommend_funds(risk_appetite, top_n=3):
    """Recommend top mutual funds based on risk and Sharpe ratio."""

    performance_file = DATA_DIR / "07_scheme_performance_cleaned.csv"

    if not performance_file.exists():
        performance_file = DATA_DIR / "07_scheme_performance.csv"

    df = pd.read_csv(performance_file)

    df["sharpe_ratio"] = pd.to_numeric(
        df["sharpe_ratio"],
        errors="coerce"
    )

    risk_col = (
        "risk_grade"
        if "risk_grade" in df.columns
        else "risk_category"
    )

    risk = risk_appetite.strip().lower()

    if risk not in ["low", "moderate", "high"]:
        raise ValueError(
            "Risk appetite must be Low, Moderate, or High."
        )

    result = df[
        df[risk_col]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq(risk)
    ]

    return (
        result
        .sort_values("sharpe_ratio", ascending=False)
        .head(top_n)
    )


if __name__ == "__main__":
    appetite = input(
        "Enter risk appetite (Low/Moderate/High): "
    )

    print(recommend_funds(appetite).to_string(index=False))