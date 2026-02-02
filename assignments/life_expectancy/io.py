"""IO functions for life expectancy assignment"""

from pathlib import Path
import pandas as pd

def load_raw_data(path: Path) -> pd.DataFrame:
    """Load raw EU life expectancy TSV file."""
    return pd.read_csv(path, sep="\t")


def save_clean_data(df: pd.DataFrame, path: Path) -> None:
    """Save cleaned DataFrame to CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
