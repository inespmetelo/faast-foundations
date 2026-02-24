"""Tests for the data_loader module"""
# pylint: disable=redefined-outer-name  # pytest fixtures redefine names intentionally

import json
from pathlib import Path

import pandas as pd
import pytest

from life_expectancy.data_loader import (
    DataLoader,
    TSVDataLoader,
    CSVDataLoader,
    JSONDataLoader,
    DataLoaderFactory,
)


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'city': ['New York', 'London', 'Paris']
    })


@pytest.fixture
def temp_tsv_file(sample_dataframe, tmp_path):
    """Create a temporary TSV file."""
    file_path = tmp_path / "test_data.tsv"
    sample_dataframe.to_csv(file_path, sep='\t', index=False)
    return file_path


@pytest.fixture
def temp_csv_file(sample_dataframe, tmp_path):
    """Create a temporary CSV file."""
    file_path = tmp_path / "test_data.csv"
    sample_dataframe.to_csv(file_path, index=False)
    return file_path


@pytest.fixture
def temp_json_file(sample_dataframe, tmp_path):
    """Create a temporary JSON file."""
    file_path = tmp_path / "test_data.json"
    data = sample_dataframe.to_dict(orient='records')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return file_path


class TestTSVDataLoader:
    """Tests for TSVDataLoader strategy."""

    def test_load_tsv(self, temp_tsv_file, sample_dataframe):
        """Test loading data from TSV file."""
        loader = TSVDataLoader()
        result = loader.load(temp_tsv_file)

        pd.testing.assert_frame_equal(result, sample_dataframe)

    def test_isinstance_dataloader(self):
        """Test that TSVDataLoader is an instance of DataLoader."""
        loader = TSVDataLoader()
        assert isinstance(loader, DataLoader)


class TestCSVDataLoader:
    """Tests for CSVDataLoader strategy."""

    def test_load_csv(self, temp_csv_file, sample_dataframe):
        """Test loading data from CSV file."""
        loader = CSVDataLoader()
        result = loader.load(temp_csv_file)

        pd.testing.assert_frame_equal(result, sample_dataframe)

    def test_isinstance_dataloader(self):
        """Test that CSVDataLoader is an instance of DataLoader."""
        loader = CSVDataLoader()
        assert isinstance(loader, DataLoader)


class TestJSONDataLoader:
    """Tests for JSONDataLoader strategy."""

    def test_load_json(self, temp_json_file, sample_dataframe):
        """Test loading data from JSON file."""
        loader = JSONDataLoader()
        result = loader.load(temp_json_file)

        # Reset index and compare
        pd.testing.assert_frame_equal(
            result.reset_index(drop=True),
            sample_dataframe.reset_index(drop=True)
        )

    def test_isinstance_dataloader(self):
        """Test that JSONDataLoader is an instance of DataLoader."""
        loader = JSONDataLoader()
        assert isinstance(loader, DataLoader)


class TestDataLoaderFactory:
    """Tests for DataLoaderFactory."""

    def test_get_tsv_loader(self):
        """Test factory returns TSVDataLoader for .tsv files."""
        loader = DataLoaderFactory.get_loader("data.tsv")
        assert isinstance(loader, TSVDataLoader)

    def test_get_csv_loader(self):
        """Test factory returns CSVDataLoader for .csv files."""
        loader = DataLoaderFactory.get_loader("data.csv")
        assert isinstance(loader, CSVDataLoader)

    def test_get_json_loader(self):
        """Test factory returns JSONDataLoader for .json files."""
        loader = DataLoaderFactory.get_loader("data.json")
        assert isinstance(loader, JSONDataLoader)

    def test_get_loader_with_path_object(self):
        """Test factory works with Path objects."""
        loader = DataLoaderFactory.get_loader(Path("data.csv"))
        assert isinstance(loader, CSVDataLoader)

    def test_get_loader_case_insensitive(self):
        """Test factory handles uppercase extensions."""
        loader = DataLoaderFactory.get_loader("data.CSV")
        assert isinstance(loader, CSVDataLoader)

    def test_unsupported_format_raises_error(self):
        """Test that unsupported file format raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported file format"):
            DataLoaderFactory.get_loader("data.xml")

    def test_register_new_loader(self):
        """Test registering a custom loader."""
        class XMLDataLoader(DataLoader):  # pylint: disable=too-few-public-methods
            """Test XML data loader."""
            def load(self, source):
                return pd.DataFrame()

        DataLoaderFactory.register_loader('.xml', XMLDataLoader)
        loader = DataLoaderFactory.get_loader("data.xml")
        assert isinstance(loader, XMLDataLoader)

    def test_register_invalid_loader_raises_error(self):
        """Test that registering a non-DataLoader class raises TypeError."""
        class NotALoader:  # pylint: disable=too-few-public-methods
            """Not a valid loader."""

        with pytest.raises(TypeError, match="must be a subclass of DataLoader"):
            DataLoaderFactory.register_loader('.txt', NotALoader)

    def test_factory_load_tsv_integration(self, temp_tsv_file, sample_dataframe):
        """Integration test: factory + loader for TSV."""
        loader = DataLoaderFactory.get_loader(temp_tsv_file)
        result = loader.load(temp_tsv_file)
        pd.testing.assert_frame_equal(result, sample_dataframe)

    def test_factory_load_csv_integration(self, temp_csv_file, sample_dataframe):
        """Integration test: factory + loader for CSV."""
        loader = DataLoaderFactory.get_loader(temp_csv_file)
        result = loader.load(temp_csv_file)
        pd.testing.assert_frame_equal(result, sample_dataframe)

    def test_factory_load_json_integration(self, temp_json_file, sample_dataframe):
        """Integration test: factory + loader for JSON."""
        loader = DataLoaderFactory.get_loader(temp_json_file)
        result = loader.load(temp_json_file)
        pd.testing.assert_frame_equal(
            result.reset_index(drop=True),
            sample_dataframe.reset_index(drop=True)
        )
