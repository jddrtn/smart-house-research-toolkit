"""Catalogue metadata for the DigiTech Smart House Data Pack."""

from typing import Final, TypedDict


class YearCatalogue(TypedDict):
    """Describe the high-level data sources published for a dataset year."""

    sources: tuple[str, ...]


# This catalogue records the structure of the published DigiTech Smart House
# Data Pack rather than assuming that every year contains the same sensors.
# More detailed metadata will be added after the source files are inspected.
DATA_CATALOGUE: Final[dict[int, YearCatalogue]] = {
    2022: {
        "sources": (
            "glaze_alarm",
            "invisible_systems",
            "weather_link",
        ),
    },
    2023: {
        "sources": (
            "glaze_alarm",
            "invisible_systems",
            "weather_link",
        ),
    },
    2024: {
        "sources": (
            "invincible_systems",
            "sds",
            "weather_link",
        ),
    },
    2025: {
        "sources": (
            "air_quality",
            "air_source_heat_pump",
            "glaze_alarm",
            "invisible_systems",
            "moisture_sensors",
            "weather_link",
        ),
    },
}


def available_years() -> list[int]:
    """Return the years represented in the Smart House Data Pack."""
    return sorted(DATA_CATALOGUE)


def available_sources(year: int) -> list[str]:
    """Return the published source groups associated with a dataset year."""
    if year not in DATA_CATALOGUE:
        raise ValueError(f"Unsupported dataset year: {year}")

    return sorted(DATA_CATALOGUE[year]["sources"])


def has_source(year: int, source: str) -> bool:
    """Return whether a source group is published for a dataset year."""
    if year not in DATA_CATALOGUE:
        return False

    return source in DATA_CATALOGUE[year]["sources"]