"""Load WeatherLink data from the DigiTech Smart House Data Pack."""

from pathlib import Path

import pandas as pd

WEATHERLINK_ENCODING = "cp1252"
WEATHERLINK_HEADER_ROWS = 5


def load_weatherlink(file_path: str | Path) -> pd.DataFrame:
    """Load observations from a WeatherLink CSV export.

    WeatherLink files in the DigiTech Smart House Data Pack contain five
    metadata rows before the actual CSV header. They are also encoded using
    Windows-1252 rather than UTF-8.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"WeatherLink file not found: {path}")

    try:
        data = pd.read_csv(
            path,
            encoding=WEATHERLINK_ENCODING,
            skiprows=WEATHERLINK_HEADER_ROWS,
        )
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as exc:
        raise ValueError(
            "The file does not appear to be a supported WeatherLink export."
        ) from exc

    if "Date & Time" not in data.columns:
        raise ValueError(
            "The file does not appear to be a supported WeatherLink export."
        )

    return data