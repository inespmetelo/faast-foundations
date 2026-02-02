"""Tests for the cleaning module"""
import pandas as pd
from life_expectancy.cleaning import clean_data
from . import FIXTURES_DIR


def test_clean_data_pt(
    pt_life_expectancy_expected,
    tmp_path
):
    """Test clean_data() for PT using fixture input and expected output"""
    tmp_out = tmp_path / "pt_life_expectancy.csv"

    result_df = clean_data(
        country="PT",
        input_path=FIXTURES_DIR / "eu_life_expectancy_raw_sample.tsv",
        output_path=tmp_out
    )

    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True),
        pt_life_expectancy_expected.reset_index(drop=True)
    )


def test_clean_data_es(
    es_life_expectancy_expected,
    tmp_path
):
    """Test clean_data() for ES using fixture input and expected output"""
    tmp_out = tmp_path / "es_life_expectancy.csv"

    result_df = clean_data(
        country="ES",
        input_path=FIXTURES_DIR / "eu_life_expectancy_raw_sample.tsv",
        output_path=tmp_out
    )

    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True),
        es_life_expectancy_expected.reset_index(drop=True)
    )
