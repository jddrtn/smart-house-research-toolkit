import pytest

from smarthouse.data import available_sources, available_years, has_source


def test_available_years():
    """The catalogue should expose every annual Smart House release."""
    assert available_years() == [2022, 2023, 2024, 2025]


def test_2022_sources():
    """2022 should expose the source groups present in its published folder."""
    assert available_sources(2022) == [
        "glaze_alarm",
        "invisible_systems",
        "weather_link",
    ]


def test_2023_sources():
    """2023 should expose the three source groups present in its release."""
    assert available_sources(2023) == [
        "glaze_alarm",
        "invisible_systems",
        "weather_link",
    ]


def test_2024_sources():
    """2024 has a different source structure from earlier releases."""
    assert available_sources(2024) == [
        "invincible_systems",
        "sds",
        "weather_link",
    ]


def test_2025_sources():
    """2025 introduces several additional Smart House data sources."""
    assert available_sources(2025) == [
        "air_quality",
        "air_source_heat_pump",
        "glaze_alarm",
        "invisible_systems",
        "moisture_sensors",
        "weather_link",
    ]


def test_has_source():
    """Source checks should respect differences between annual releases."""
    assert has_source(2025, "moisture_sensors")
    assert not has_source(2023, "moisture_sensors")


def test_unknown_year_has_no_source():
    """Unknown years should not report sources as available."""
    assert not has_source(2026, "weather_link")


def test_available_sources_rejects_unknown_year():
    """Requesting a catalogue for an unsupported year should fail clearly."""
    with pytest.raises(ValueError, match="Unsupported dataset year: 2026"):
        available_sources(2026)