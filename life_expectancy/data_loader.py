"""Data loader strategies for accessing data in different formats."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type, Union

import pandas as pd


class DataLoader(ABC):  # pylint: disable=too-few-public-methods
    """Abstract base class for data loading strategies."""

    @abstractmethod
    def load(self, source: Union[Path, str]) -> pd.DataFrame:
        """Load data from the given source and return a DataFrame.
        
        Args:
            source: Path to the data file or data source
            
        Returns:
            pd.DataFrame: Loaded data
        """


class TSVDataLoader(DataLoader):  # pylint: disable=too-few-public-methods
    """Strategy for loading data from TSV files."""

    def load(self, source: Union[Path, str]) -> pd.DataFrame:
        """Load data from a TSV file.
        
        Args:
            source: Path to the TSV file
            
        Returns:
            pd.DataFrame: Loaded data
        """
        return pd.read_csv(source, sep="\t")


class CSVDataLoader(DataLoader):  # pylint: disable=too-few-public-methods
    """Strategy for loading data from CSV files."""

    def load(self, source: Union[Path, str]) -> pd.DataFrame:
        """Load data from a CSV file.
        
        Args:
            source: Path to the CSV file
            
        Returns:
            pd.DataFrame: Loaded data
        """
        return pd.read_csv(source)


class JSONDataLoader(DataLoader):  # pylint: disable=too-few-public-methods
    """Strategy for loading data from JSON files."""

    def load(self, source: Union[Path, str]) -> pd.DataFrame:
        """Load data from a JSON file.
        
        Args:
            source: Path to the JSON file
            
        Returns:
            pd.DataFrame: Loaded data
        """
        return pd.read_json(source)


class DataLoaderFactory:
    """Factory for creating appropriate data loader based on file extension."""

    _loaders: dict[str, Type[DataLoader]] = {
        '.tsv': TSVDataLoader,
        '.csv': CSVDataLoader,
        '.json': JSONDataLoader,
    }

    @classmethod
    def get_loader(cls, file_path: Union[Path, str]) -> DataLoader:
        """Get the appropriate data loader based on file extension.

        Args:
            file_path: Path to the data file

        Returns:
            DataLoader: Appropriate data loader instance

        Raises:
            ValueError: If file extension is not supported
        """
        path = Path(file_path)
        extension = path.suffix.lower()

        if extension not in cls._loaders:
            supported = ', '.join(cls._loaders.keys())
            raise ValueError(
                f"Unsupported file format: {extension}. "
                f"Supported formats: {supported}"
            )

        loader_class: Type[DataLoader] = cls._loaders[extension]
        return loader_class()

    @classmethod
    def register_loader(cls, extension: str, loader_class: Type[DataLoader]) -> None:
        """Register a new data loader for a specific file extension.

        Args:
            extension: File extension (e.g., '.xml')
            loader_class: DataLoader class to handle this extension

        Raises:
            TypeError: If loader_class is not a subclass of DataLoader
        """
        if not isinstance(loader_class, type) or not issubclass(loader_class, DataLoader):
            raise TypeError(
                f"loader_class must be a subclass of DataLoader, "
                f"got {loader_class}"
            )
        if not extension.startswith('.'):
            extension = f'.{extension}'
        cls._loaders[extension.lower()] = loader_class
