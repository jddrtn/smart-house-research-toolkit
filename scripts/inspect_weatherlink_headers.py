"""Show the raw header lines from WeatherLink CSV exports."""

from pathlib import Path


DATA_DIRECTORY = Path("data/raw")


def main() -> None:
    """Print the beginning of every WeatherLink CSV without parsing it."""

    weatherlink_files = sorted(
        path
        for path in DATA_DIRECTORY.rglob("*.csv")
        if "weather" in str(path).lower()
        or path.name.lower() in {"airlink.csv", "indoor.csv", "outdoor.csv"}
    )

    for file_path in weatherlink_files:
        print("\n" + "=" * 80)
        print(file_path)

        # WeatherLink exports appear to use Windows-1252 rather than UTF-8.
        # Reading the raw text first lets us locate the true CSV header before
        # deciding how the production loader should parse these files.
        with file_path.open(
            "r",
            encoding="cp1252",
            errors="replace",
        ) as file:
            for line_number in range(1, 9):
                line = file.readline()

                if not line:
                    break

                print(f"{line_number}: {line.rstrip()}")


if __name__ == "__main__":
    main()