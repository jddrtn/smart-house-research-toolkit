"""Explore the published dataset catalogue without downloading any data.

The years identify dataset releases, not the dates of individual observations.
These helpers report catalogue metadata; they do not inspect local files.
"""

from smarthouse.data import available_sources, available_years, has_source


def main() -> None:
    """Print available releases and inspect sources in the latest release."""
    dataset_years = available_years()
    print("Available dataset release years:", dataset_years)

    # Use a year from the catalogue rather than assuming the current year exists.
    dataset_year = dataset_years[-1]
    print(f"\nSources available in {dataset_year}:")
    for source in available_sources(dataset_year):
        print(f"- {source}")

    # Check a source by its catalogue name before choosing a release to explore.
    weatherlink_available = has_source(dataset_year, "weather_link")
    print(f"\nWeatherLink available in {dataset_year}: {weatherlink_available}")


if __name__ == "__main__":
    main()
