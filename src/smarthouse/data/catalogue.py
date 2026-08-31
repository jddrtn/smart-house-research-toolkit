"""Dataset availability information for the DigiTech Smart House Data Pack."""

from typing import Final


# Keep dataset availability in one place.
DATA_CATALOGUE: Final[dict[int, set[str]]] = {
    2022: set(),
    2023: {"glaze_alarm"},
    2024: set(),
    2025: set(),
}


def available_years() -> list[int]:
    """Return the years currently supported by the toolkit."""
    return sorted(DATA_CATALOGUE)


def available_sources(year: int) -> list[str]:
    """Return the data sources available for a specific year."""
    if year not in DATA_CATALOGUE:
        raise ValueError(f"Unsupported dataset year: {year}")

    return sorted(DATA_CATALOGUE[year])


def has_source(year: int, source: str) -> bool:
    """Return whether a specific data source is available for a year."""
    if year not in DATA_CATALOGUE:
        return False

    return source in DATA_CATALOGUE[year]