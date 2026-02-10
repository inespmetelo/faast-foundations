"Extracts the unique regions from the raw life expectancy data and prints them."""

from pathlib import Path
import pandas as pd

DATA_PATH = Path("life_expectancy/data/eu_life_expectancy_raw.tsv")

df = pd.read_csv(DATA_PATH, sep="\t")

meta_col = df.columns[0]
regions = (
    df[meta_col]
    .str.split(",", expand=True)
    .iloc[:, -1]   # region column
    .unique()
)

regions = sorted(regions)

print("Regions:")
for r in regions:
    print(r)
