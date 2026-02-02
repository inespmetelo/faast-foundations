"""Pytest configuration file"""
import pandas as pd
import pytest
from . import FIXTURES_DIR

# Input fixtures

@pytest.fixture(scope="session")
def sample_life_expectancy_input() -> pd.DataFrame:
    """Load the sample raw input fixture (PT + ES)"""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_raw_sample.tsv", sep="\t")


# Expected output fixtures

@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Load the expected cleaned output for PT"""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_expected_pt.csv")

@pytest.fixture(scope="session")
def es_life_expectancy_expected() -> pd.DataFrame:
    """Load the expected cleaned output for ES"""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_expected_es.csv")
