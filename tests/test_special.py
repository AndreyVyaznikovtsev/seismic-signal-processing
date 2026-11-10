"""Тесты прямоугольного приближения дельта-функции."""

import numpy as np
import pytest

from seisdsp.special import rect_delta


def test_rect_delta_inside_support():
    """Внутри носителя значение равно 1/eps."""
    out = rect_delta(np.linspace(-0.4, 0.4, 5), eps=1.0)
    assert np.allclose(out, 1.0)


def test_rect_delta_outside_support_is_zero():
    """Вне носителя — строго ноль."""
    out = rect_delta(np.array([-2.0, -0.6, 0.6, 2.0]), eps=1.0)
    assert np.all(out == 0.0)


def test_rect_delta_edges_included():
    """Края |t| = eps/2 принадлежат носителю."""
    out = rect_delta(np.array([-0.5, 0.5]), eps=1.0)
    assert np.allclose(out, 1.0)


def test_rect_delta_area_is_one():
    """Площадь равна единице при любом eps."""
    for eps in (1e-1, 1e-2, 1e-3):
        t = np.linspace(-eps / 2, eps / 2, 101)
        assert abs(np.trapezoid(rect_delta(t, eps), t) - 1.0) < 1e-12


def test_rect_delta_negative_eps_raises():
    """eps <= 0 отбрасывается с ValueError."""
    with pytest.raises(ValueError):
        rect_delta(np.array([0.0]), eps=-1.0)
