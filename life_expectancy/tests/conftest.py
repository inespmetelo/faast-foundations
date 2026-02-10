"""Pytest configuration file."""

from pathlib import Path
import pytest
import pandas as pd

# Base paths
PROJECT_DIR = Path(__file__).parents[2]
PACKAGE_DIR = PROJECT_DIR / "life_expectancy"
FIXTURES_DIR = PACKAGE_DIR / "tests" / "fixtures"


@pytest.fixture(scope="session")
def sample_life_expectancy_input() -> pd.DataFrame:
    """Load sample raw EU life expectancy input fixture."""
    return pd.read_csv(
        FIXTURES_DIR / "eu_life_expectancy_raw_sample.tsv",
        sep="\t"
    )


@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Load expected cleaned PT output fixture."""
    return pd.read_csv(
        FIXTURES_DIR / "eu_life_expectancy_expected_pt.csv"
    )


@pytest.fixture(scope="session")
def es_life_expectancy_expected() -> pd.DataFrame:
    """Load expected cleaned ES output fixture."""
    return pd.read_csv(
        FIXTURES_DIR / "eu_life_expectancy_expected_es.csv"
    )
