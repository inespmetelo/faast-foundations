"""Tests for the cleaning module"""

import pandas as pd
import pytest

from life_expectancy.cleaning import clean_data


@pytest.mark.parametrize(
    "country,expected_fixture",
    [
        ("PT", "pt_life_expectancy_expected"),
        ("ES", "es_life_expectancy_expected"),
    ],
)
def test_clean_data(
    sample_life_expectancy_input,
    country,
    expected_fixture,
    request,
):
    """Test clean_data() for different countries using fixture input and expected output"""

    expected_df = request.getfixturevalue(expected_fixture)

    result_df = clean_data(
        sample_life_expectancy_input,
        country=country,
    )

    pd.testing.assert_frame_equal(
        result_df.reset_index(drop=True),
        expected_df.reset_index(drop=True),
    )
