"""Tests for the cleaning module"""

import pandas as pd

from life_expectancy.cleaning import clean_data


def test_clean_data_pt(
    sample_life_expectancy_input,
    pt_life_expectancy_expected,
):
    """Test clean_data() for PT using fixture input and expected output"""

    result_df = clean_data(
        sample_life_expectancy_input,
        country="PT",
    )

    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True),
        pt_life_expectancy_expected.reset_index(drop=True),
    )


def test_clean_data_es(
    sample_life_expectancy_input,
    es_life_expectancy_expected,
):
    """Test clean_data() for ES using fixture input and expected output"""

    result_df = clean_data(
        sample_life_expectancy_input,
        country="ES",
    )

    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True),
        es_life_expectancy_expected.reset_index(drop=True),
    )
