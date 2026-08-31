from pathlib import Path

import pytest

from smarthouse.data import load_weatherlink


@pytest.fixture
def weatherlink_csv(tmp_path: Path) -> Path:
    """Create a minimal WeatherLink export matching the real file structure."""
    file_path = tmp_path / "weatherlink.csv"

    # The fixture reproduces WeatherLink's metadata preamble so the test
    # verifies our parser without redistributing the original dataset.
    content = (
        '"DigiTech Smart House"\n'
        '"1/1/25 00:00 : 1 Year"\n'
        '"","DigiTech Smart House"\n'
        '"","AirLink"\n'
        '"",""\n'
        '"Date & Time","AQI","PM 2.5 - ug/m²"\n'
        '"1/1/25 00:00","1,16","1,8"\n'
    )

    file_path.write_text(content, encoding="cp1252")

    return file_path


def test_load_weatherlink_skips_metadata(weatherlink_csv: Path):
    """The WeatherLink metadata preamble should not become dataframe rows."""
    data = load_weatherlink(weatherlink_csv)

    assert list(data.columns) == [
        "Date & Time",
        "AQI",
        "PM 2.5 - ug/m²",
    ]
    assert len(data) == 1


def test_load_weatherlink_rejects_non_weatherlink_file(tmp_path: Path):
    """Files without the expected WeatherLink header should fail clearly."""
    file_path = tmp_path / "invalid.csv"
    file_path.write_text("name,value\nTemperature,20\n", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="supported WeatherLink export",
    ):
        load_weatherlink(file_path)


def test_load_weatherlink_rejects_missing_file(tmp_path: Path):
    """Missing dataset files should produce an informative error."""
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError, match="WeatherLink file not found"):
        load_weatherlink(missing_file)