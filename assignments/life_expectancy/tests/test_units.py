"""Unit tests for the IO and cleaning functions"""

from unittest.mock import patch
from pathlib import Path
import pandas as pd
from life_expectancy.io import load_raw_data, save_clean_data
from life_expectancy.cleaning import clean_data
from. import FIXTURES_DIR


def test_load_raw_data_returns_dataframe():
    """Ensure load_raw_data returns a DataFrame with rows and columns."""
    sample_path = FIXTURES_DIR / "eu_life_expectancy_raw_sample.tsv"
    df = load_raw_data(sample_path)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0  # has rows
    assert df.shape[1] > 0  # has columns


def test_save_clean_data_calls_to_csv():
    """Ensure save_clean_data calls DataFrame.to_csv with correct parameters."""
    df = pd.DataFrame({"a": [1, 2, 3]})
    fake_path = Path("/tmp/fake.csv")

    # Patch to_csv to avoid writing to disk
    with patch.object(pd.DataFrame, "to_csv") as mock_to_csv:
        save_clean_data(df, fake_path)
        mock_to_csv.assert_called_once_with(fake_path, index=False)


def test_clean_data_transforms_and_calls_save(tmp_path):
    """Test clean_data function transforms data and attempts to save."""
    input_path = FIXTURES_DIR / "eu_life_expectancy_raw_sample.tsv"
    output_path = tmp_path / "out.csv"

    # Patch to_csv to prevent writing
    with patch.object(pd.DataFrame, "to_csv") as mock_to_csv:
        result_df = clean_data(
            country="PT",
            input_path=input_path,
            output_path=output_path
        )

        # Assert that save was attempted
        mock_to_csv.assert_called_once()

        # Check transformation: all rows filtered to PT
        assert all(result_df["region"] == "PT")
        # Check columns
        assert "year" in result_df.columns
        assert "value" in result_df.columns
