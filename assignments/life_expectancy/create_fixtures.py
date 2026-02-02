"""
Script to generate fixtures for life expectancy tests
"""

from pathlib import Path
import pandas as pd
from life_expectancy.cleaning import clean_data

# Directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
FIXTURES_DIR = BASE_DIR / "tests" / "fixtures"
FIXTURES_DIR.mkdir(parents=True, exist_ok=True)

RAW_PATH = DATA_DIR / "eu_life_expectancy_raw.tsv"

# Sample input fixture
df = pd.read_csv(RAW_PATH, sep="\t")

# Extract region from meta column
meta_col = df.columns[0]
regions = df[meta_col].str.split(",", expand=True)[3]
df["region"] = regions

# Take a small sample covering PT and ES
df_sample = df[df["region"].isin(["PT", "ES"])].copy()

# Optional: limit number of rows per country
df_sample = df_sample.groupby("region").head(10)

# Save sample input fixture
sample_path = FIXTURES_DIR / "eu_life_expectancy_raw_sample.tsv"
df_sample.drop(columns=["region"]).to_csv(sample_path, sep="\t", index=False)
print(f"Sample input fixture saved: {sample_path}")

# Generate expected PT output fixture
pt_expected_path = FIXTURES_DIR / "eu_life_expectancy_expected_pt.csv"
clean_data(
    country="PT",
    input_path=sample_path,
    output_path=pt_expected_path
)
print(f"Expected PT fixture saved: {pt_expected_path}")

# Generate expected ES output fixture
es_expected_path = FIXTURES_DIR / "eu_life_expectancy_expected_es.csv"
clean_data(
    country="ES",
    input_path=sample_path,
    output_path=es_expected_path
)
print(f"Expected ES fixture saved: {es_expected_path}")
