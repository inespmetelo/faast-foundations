"""Unit tests for life_expectancy public functions"""

from pathlib import Path
from unittest.mock import patch
import pandas as pd

from life_expectancy.cleaning import load_data, clean_data, save_data, main


# load data UNIT TEST
@patch("pandas.read_csv")
def test_load_data(mock_read_csv, sample_life_expectancy_input):
    """Unit test for load_data() using mock (no file reading)"""

    mock_read_csv.return_value = sample_life_expectancy_input
    fake_path = Path("fake.tsv")

    df = load_data(fake_path)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    mock_read_csv.assert_called_once_with(fake_path, sep='\t')


# Clean data UNIT TEST
def test_clean_data_unit(sample_life_expectancy_input):
    """Unit test for clean_data()"""

    result = clean_data(sample_life_expectancy_input, country="PT")

    assert isinstance(result, pd.DataFrame)
    assert "year" in result.columns
    assert "value" in result.columns
    assert (result["region"] == "PT").all()


# Save data UNIT TEST
@patch("pandas.DataFrame.to_csv")
def test_save_data_mocked(mock_to_csv):
    """Unit test for save_data() using mock (no file writing)"""

    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    fake_path = Path("fake.csv")

    save_data(df, fake_path)

    mock_to_csv.assert_called_once()


# main UNIT TEST
@patch("life_expectancy.cleaning.save_data")
@patch("life_expectancy.cleaning.clean_data")
@patch("life_expectancy.cleaning.load_data")
def test_main(mock_load, mock_clean, mock_save):
    """Unit test for main() with full mocking"""

    fake_df = pd.DataFrame({"x": [1]})

    mock_load.return_value = fake_df
    mock_clean.return_value = fake_df

    main(country="PT")

    mock_load.assert_called_once()
    mock_clean.assert_called_once()
    mock_save.assert_called_once()
