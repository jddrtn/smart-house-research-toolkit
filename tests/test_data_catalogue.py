from smarthouse.data import available_sources, available_years, has_source


def test_available_years():
    assert available_years() == [2022, 2023, 2024, 2025]


def test_glaze_alarm_available_in_2023():
    assert has_source(2023, "glaze_alarm")


def test_glaze_alarm_not_available_in_2024():
    assert not has_source(2024, "glaze_alarm")


def test_available_sources_returns_sorted_list():
    assert available_sources(2023) == ["glaze_alarm"]