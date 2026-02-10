"""Create fixture files for life_expectancy tests."""

from .cleaning import DATA_DIR,BASE_DIR, load_data, clean_data

RAW_DATA_PATH = DATA_DIR/ "eu_life_expectancy_raw.tsv"
FIXTURES_DIR = BASE_DIR / "tests/fixtures"
SAMPLE_INPUT_PATH = FIXTURES_DIR / "eu_life_expectancy_raw_sample.tsv"
EXPECTED_PT_PATH = FIXTURES_DIR / "eu_life_expectancy_expected_pt.csv"
EXPECTED_ES_PATH = FIXTURES_DIR / "eu_life_expectancy_expected_es.csv"

# Load raw data
df_raw = load_data(RAW_DATA_PATH)

# Create a sample fixture
sample_df = df_raw[df_raw[df_raw.columns[0]].str.contains("PT|ES")].head(10)
sample_df.to_csv(SAMPLE_INPUT_PATH, sep="\t", index=False)

# Generate expected PT and ES outputs
pt_df = clean_data(sample_df, country="PT")
pt_df.to_csv(EXPECTED_PT_PATH, index=False)

es_df = clean_data(sample_df, country="ES")
es_df.to_csv(EXPECTED_ES_PATH, index=False)
