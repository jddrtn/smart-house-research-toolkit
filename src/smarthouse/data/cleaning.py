"""Cleaning and normalisation utilities for Smart House source data.

These functions transform values that a loader has already read into a
dataframe. They are kept separate from the source-specific loaders (see
``weatherlink.py``) so that reading raw files and cleaning values remain
easy to test and reason about independently.
"""

import re

import pandas as pd

# Matches an optionally-signed decimal-comma number, e.g. "29,6" or "-1,16".
# Anchored on both ends so values that merely contain a comma (labels,
# combined fields) are never misidentified as numeric.
_DECIMAL_COMMA_PATTERN = re.compile(r"^-?\d+,\d+$")


def _convert_value(value: object) -> object:
    """Convert a single decimal-comma string to a float; otherwise leave it."""
    if not isinstance(value, str):
        return value

    if not _DECIMAL_COMMA_PATTERN.match(value):
        return value

    return float(value.replace(",", "."))


def _column_is_fully_convertible(series: pd.Series) -> bool:
    """Return whether every non-null value in a column matches the pattern."""
    non_null = series.dropna()
    if non_null.empty:
        return False

    return non_null.astype(str).str.match(_DECIMAL_COMMA_PATTERN).all()


def convert_decimal_comma(
    data: pd.DataFrame, columns: list[str] | None = None
) -> pd.DataFrame:
    """Convert decimal-comma numeric values (e.g. ``"29,6"``) to floats.

    Some WeatherLink exports use a comma as the decimal separator, which
    pandas otherwise loads as a plain string column (e.g. ``"29,6"``
    instead of ``29.6``).

    By default, every column is inspected, and only columns whose
    non-null values *all* match a decimal-comma number (optionally
    signed, e.g. ``"-1,16"``) are converted to floats. This keeps
    timestamp, label, and other non-numeric columns untouched.

    Pass ``columns`` to restrict conversion to a known set of measurement
    columns. In that mode, matching values are still converted
    individually; any value that does not match the decimal-comma
    pattern (including values that are already numeric, or genuinely
    unsupported/ambiguous text) is left exactly as it was rather than
    being coerced or dropped, so the column may remain a mixed/object
    dtype if not every value converts cleanly.

    Missing values are always preserved as missing. The input dataframe
    is never modified; a new dataframe is returned.
    """
    result = data.copy()
    target_columns = columns if columns is not None else list(data.columns)

    for column in target_columns:
        if column not in result.columns:
            raise KeyError(f"Column not found in dataframe: {column}")

        series = result[column]

        if columns is None and not _column_is_fully_convertible(series):
            continue

        result[column] = series.map(_convert_value)

    return result