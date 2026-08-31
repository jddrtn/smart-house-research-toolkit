"""
WeatherLink quickstart example.

Demonstrates how to load a locally downloaded WeatherLink CSV export
(from the DigiTech Smart House Data Pack) using the toolkit's
`load_weatherlink` loader, and how to perform basic inspection of the
resulting DataFrame.

This script only demonstrates existing loader behaviour -- t does not
add timestamp parsing, decimal-comma conversion, missing-data handling,
resampling, or any analysis. You must download the DigiTech Smart House
Data Pack from Kaggle yourself and place the CSV under `data/raw/`;
no dataset files are included in this repository.
"""

from smarthouse.data import load_weatherlink

# Replace this with the path to your own locally downloaded WeatherLink
# CSV export. The dataset itself is never committed to this repository.
WEATHERLINK_CSV_PATH = "data/raw/path/to/weatherlink.csv"


def main() -> None:
    # load_weatherlink already handles WeatherLink's export quirks:
    # the metadata rows preceding the real header, and the cp1252
    # encoding WeatherLink uses. Timestamps and numeric formatting are
    # not normalised yet -- that is separate, ongoing toolkit work.
    data = load_weatherlink(WEATHERLINK_CSV_PATH)

    # Preview the first few observations to see the raw shape of the data.
    print("First 5 rows:")
    print(data.head())

    # List available columns -- useful before writing any analysis code.
    print("\nAvailable columns:")
    print(data.columns)

    # Check overall size: how many observations and measurements.
    print("\nShape (rows, columns):")
    print(data.shape)

    # dtypes, non-null counts, and memory usage in one summary.
    print("\nDataFrame info:")
    data.info()


if __name__ == "__main__":
    main()