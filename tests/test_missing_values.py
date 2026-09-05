import pandas as pd
from pandas.testing import assert_frame_equal

from smarthouse.analysis import summarise_missing_values


def test_summarise_missing_values_reports_counts_and_percentages():
    """Each column should be represented with its missing-value statistics."""
    data = pd.DataFrame(
        {
            "Temperature": [20.0, None, 22.0, None],
            "Humidity": [40.0, 41.0, 42.0, 43.0],
            "PM2.5": [None, 12.0, 13.0, 14.0],
        }
    )

    summary = summarise_missing_values(data)

    expected = pd.DataFrame(
        {
            "column": ["Temperature", "Humidity", "PM2.5"],
            "missing_count": [2, 0, 1],
            "missing_percentage": [50.0, 0.0, 25.0],
        }
    )
    assert_frame_equal(summary, expected)


def test_summarise_missing_values_handles_empty_dataframes_without_mutating_them():
    """Empty inputs retain their columns and report zero missing values."""
    data = pd.DataFrame(columns=["Temperature", "Humidity"])
    original = data.copy(deep=True)

    summary = summarise_missing_values(data)

    expected = pd.DataFrame(
        {
            "column": ["Temperature", "Humidity"],
            "missing_count": [0, 0],
            "missing_percentage": [0.0, 0.0],
        }
    )
    assert_frame_equal(summary, expected)
    assert_frame_equal(data, original)
