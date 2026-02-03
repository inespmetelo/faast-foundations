"""Data cleaning utilities for EU life expectancy dataset."""

from pathlib import Path
import argparse
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

DATA_PATH = DATA_DIR / "eu_life_expectancy_raw.tsv"
OUTPUT_PATH = DATA_DIR / "pt_life_expectancy.csv"

def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the raw EU life expectancy dataset."""
    return pd.read_csv(path, sep="\t")

def clean_data(df: pd.DataFrame, country: str = "PT") -> pd.DataFrame:
    """
    Clean the EU life expectancy dataset:
    - unpivot to long format
    - ensure correct data types
    - filter by country
    """
    # Identifier columns
    meta_col = df.columns[0]  # "unit,sex,age,geo\\time"
    meta = df[meta_col].str.split(",", expand=True)
    meta.columns = ["unit", "sex", "age", "region"]

    # Year columns
    year_df = df.drop(columns=[meta_col])
    year_df.columns = [c.strip() for c in year_df.columns]
    year_cols = list(year_df.columns)

    # Combine meta columns with year columns
    df_clean = pd.concat([meta, year_df], axis=1)

    # Unpivot to long format
    df_long = df_clean.melt(
        id_vars=["unit", "sex", "age", "region"],
        value_vars=year_cols,
        var_name="year",
        value_name="value",
    )

    # Ensure year is integer
    df_long["year"] = df_long["year"].astype(int)

    # Clean and convert values
    df_long["value"] = (
        df_long["value"]
        .astype(str)
        .str.strip()
        .str.replace(":", "", regex=False)
        .str.replace(r"[^0-9.\-]", "", regex=True)
    )
    df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")
    df_long = df_long.dropna(subset=["value"])
    df_long["value"] = df_long["value"].astype(float)

    # Filter by country
    df_long = df_long[df_long["region"] == country]

    return df_long

def save_data(df: pd.DataFrame, path: Path = OUTPUT_PATH) -> None:
    """Save the cleaned dataset to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

def main(country: str = "PT") -> pd.DataFrame:
    """Run the full data cleaning pipeline and return cleaned data."""
    raw_data = load_data()
    cleaned_data = clean_data(raw_data, country=country)
    save_data(cleaned_data)
    return cleaned_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean EU life expectancy data"
    )
    parser.add_argument(
        "--country",
        default="PT",
        help="Country code to filter (default: PT)",
    )
    args = parser.parse_args()

    main(country=args.country)
