import pytest

from pylette import Color


def test_delta_e_is_zero_for_identical_colors() -> None:
    c = Color(rgba=(120, 60, 200, 255), frequency=1.0)
    assert c.delta_e(c) == pytest.approx(0.0, abs=1e-9)


def test_delta_e_is_symmetric_and_positive() -> None:
    a = Color(rgba=(10, 20, 30, 255), frequency=0.5)
    b = Color(rgba=(200, 180, 50, 255), frequency=0.5)
    assert a.delta_e(b) == pytest.approx(b.delta_e(a))
    assert a.delta_e(b) > 0.0
