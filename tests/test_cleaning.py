import math

import pandas as pd

from smarthouse.data import convert_decimal_comma


def test_converts_decimal_comma_values():
    """Decimal-comma values in a fully-numeric column become floats."""
    data = pd.DataFrame({"AQI": ["1,16", "2,50"]})

    result = convert_decimal_comma(data)

    assert result["AQI"].tolist() == [1.16, 2.5]
    assert result["AQI"].dtype == float


def test_ordinary_decimal_point_values_still_work():
    """A column already using decimal points is left as numeric floats."""
    data = pd.DataFrame({"Temp": [29.6, 1.16]})

    result = convert_decimal_comma(data)

    assert result["Temp"].tolist() == [29.6, 1.16]


def test_missing_values_remain_missing():
    """NaN values in an otherwise-convertible column stay NaN."""
    data = pd.DataFrame({"AQI": ["1,16", None]})

    result = convert_decimal_comma(data)

    assert result["AQI"].iloc[0] == 1.16
    assert math.isnan(result["AQI"].iloc[1])


def test_non_numeric_columns_are_not_modified():
    """Timestamp and label columns are left completely untouched."""
    data = pd.DataFrame(
        {
            "Date & Time": ["1/1/25 00:00", "1/1/25 00:15"],
            "AQI": ["1,16", "2,50"],
        }
    )

    result = convert_decimal_comma(data)

    assert result["Date & Time"].tolist() == ["1/1/25 00:00", "1/1/25 00:15"]
    assert result["AQI"].tolist() == [1.16, 2.5]


def test_unsupported_or_ambiguous_values_are_handled_safely():
    """A column with one non-matching value is left untouched, not coerced."""
    data = pd.DataFrame({"Notes": ["1,16", "sensor offline"]})

    result = convert_decimal_comma(data)

    # Mixed content means the column doesn't fully match the pattern, so
    # auto-detection leaves it alone rather than guessing.
    assert result["Notes"].tolist() == ["1,16", "sensor offline"]


def test_explicit_columns_convert_matching_values_and_preserve_the_rest():
    """With explicit columns, matching values convert; others are untouched."""
    data = pd.DataFrame({"AQI": ["1,16", "already_flagged"]})

    result = convert_decimal_comma(data, columns=["AQI"])

    assert result["AQI"].tolist() == [1.16, "already_flagged"]


def test_input_dataframe_is_not_modified():
    """The original dataframe passed in is left untouched."""
    data = pd.DataFrame({"AQI": ["1,16", "2,50"]})

    convert_decimal_comma(data)

    assert data["AQI"].tolist() == ["1,16", "2,50"]


def test_unknown_column_raises_key_error():
    """Requesting a column that doesn't exist fails clearly."""
    data = pd.DataFrame({"AQI": ["1,16"]})

    try:
        convert_decimal_comma(data, columns=["Missing"])
        raise AssertionError("Expected KeyError")
    except KeyError:
        pass