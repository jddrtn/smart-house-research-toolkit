"""Inspect CSV schemas in the local DigiTech Smart House Data Pack."""

from pathlib import Path

import pandas as pd


DATA_DIRECTORY = Path("data/raw")


def inspect_csv(file_path: Path) -> None:
    """Print basic structural information without loading the full dataset."""

    # Files in the Data Pack originate from several sensor platforms.
    # They therefore differ in both text encoding and where the actual
    # tabular header begins.
    encodings = ("utf-8", "cp1252")

    # Some exports, particularly WeatherLink files, can contain descriptive
    # metadata before the CSV table. Trying a small number of skipped rows
    # lets this inspection utility discover those schemas without building
    # source-specific assumptions into the exploratory script.
    possible_skiprows = range(0, 6)

    sample = None
    successful_encoding = None
    successful_skiprows = None
    last_error = None

    for encoding in encodings:
        for skiprows in possible_skiprows:
            try:
                # Only a few records are required to identify the schema.
                # Avoiding a full read keeps inspection fast even for large
                # sensor exports.
                sample = pd.read_csv(
                    file_path,
                    nrows=5,
                    encoding=encoding,
                    skiprows=skiprows,
                )

                successful_encoding = encoding
                successful_skiprows = skiprows
                break

            except (UnicodeDecodeError, pd.errors.ParserError) as exc:
                # Encoding and header placement vary between source systems.
                # Record the error and try the next plausible combination.
                last_error = exc

        if sample is not None:
            break

    if sample is None:
        print("\n" + "=" * 80)
        print(f"FAILED: {file_path}")
        print(f"Reason: {last_error}")
        return

    print("\n" + "=" * 80)
    print(file_path)
    print(f"Encoding: {successful_encoding}")
    print(f"Skipped rows: {successful_skiprows}")
    print(f"Columns ({len(sample.columns)}):")

    for column in sample.columns:
        print(f"  - {column}")

    if not sample.empty:
        print("\nFirst row:")
        print(sample.iloc[0].to_dict())


def main() -> None:
    """Inspect every CSV found in the raw Smart House dataset."""

    csv_files = sorted(DATA_DIRECTORY.rglob("*.csv"))

    print(f"Found {len(csv_files)} CSV files.")

    for file_path in csv_files:
        inspect_csv(file_path)


if __name__ == "__main__":
    main()