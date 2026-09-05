"""Utilities for inspecting missing values in research datasets."""

import pandas as pd


def summarise_missing_values(data: pd.DataFrame) -> pd.DataFrame:
    """Return missing-value counts and percentages for every input column.

    Percentages are calculated from the number of rows in ``data``. Empty
    dataframes therefore report zero missing values and ``0.0`` percent for
    every column. The input dataframe is never modified.
    """
    missing_counts = data.isna().sum()
    row_count = len(data)
    percentages = (
        missing_counts.div(row_count).mul(100)
        if row_count
        else missing_counts.astype(float)
    )

    return pd.DataFrame(
        {
            "column": data.columns,
            "missing_count": missing_counts.to_numpy(),
            "missing_percentage": percentages.to_numpy(),
        }
    )
