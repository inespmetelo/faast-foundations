"""Data cleaning utilities for EU life expectancy dataset."""

from pathlib import Path
import argparse

import pandas as pd
from life_expectancy.io import load_raw_data, save_clean_data

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

DATA_PATH = DATA_DIR / "eu_life_expectancy_raw.tsv"
OUTPUT_PATH = DATA_DIR / "pt_life_expectancy.csv"

def clean_data(
    country: str = "PT",
    input_path: Path = DATA_PATH,
    output_path: Path = OUTPUT_PATH
) -> pd.DataFrame:

    """
    Loads eu_life_expectancy_raw.tsv, unpivots it to long format, ensures correct data types,
    filters by country, and saves the cleaned data to eu_life_expectancy_cleaned.csv.
    """

    # Load the dataset
    df = load_raw_data(input_path)

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

    # Unpivot to long format: unit, sex, age, region, year, value
    df_long = df_clean.melt(
        id_vars=["unit", "sex", "age", "region"],
        value_vars=year_cols,
        var_name="year",
        value_name="value",
    )

    # Ensure year is an integer
    df_long['year'] = df_long['year'].astype(int)

    # Ensure value is a float, removing Nans
    df_long["value"] = (
        df_long["value"]
        .astype(str)
        .str.strip()
        .str.replace(":", "", regex=False)
        .str.replace(r"[^0-9.\-]", "", regex=True)
        )
    df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")
    df_long = df_long.dropna(subset=['value'])
    df_long['value'] = df_long['value'].astype(float)

    # Filter for the specified country
    df_long = df_long[df_long["region"] == country]

    # Save
    save_clean_data(df_long, output_path)

    return df_long

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

    clean_data(country=args.country, output_path=OUTPUT_PATH, input_path=DATA_PATH)
