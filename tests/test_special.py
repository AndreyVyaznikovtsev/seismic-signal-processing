"""Тесты для кусочно-постоянных функций через ступеньки Хевисайда."""

import numpy as np
import pytest

from seisdsp.special import piecewise_from_jumps


def test_piecewise_scalar_and_array():
    bp = [0.0, 2.0]
    vals = [1.0, 3.0, -1.0]
    assert piecewise_from_jumps(-1.0, bp, vals) == 1.0
    assert piecewise_from_jumps(1.0, bp, vals) == 3.0
    assert piecewise_from_jumps(3.0, bp, vals) == -1.0

    t = np.array([-1.0, 1.0, 3.0])
    res = piecewise_from_jumps(t, bp, vals)
    assert isinstance(res, np.ndarray)
    assert res.shape == t.shape
    np.testing.assert_allclose(res, [1.0, 3.0, -1.0])


def test_piecewise_at_breakpoints_uses_u0():
    bp = [1.0]
    vals = [0.0, 2.0]
    assert piecewise_from_jumps(1.0, bp, vals, u0=0.5) == 1.0
    assert piecewise_from_jumps(1.0, bp, vals, u0=0.0) == 0.0
    assert piecewise_from_jumps(1.0, bp, vals, u0=1.0) == 2.0


def test_piecewise_matches_np_select():
    t = np.linspace(-3.0, 6.0, 500)
    bp = [-1.5, 0.0, 2.5, 4.0]
    vals = [0.5, 2.0, -1.5, 3.0, 0.0]

    y_jumps = piecewise_from_jumps(t, bp, vals)
    conds = [
        t < bp[0],
        (t >= bp[0]) & (t < bp[1]),
        (t >= bp[1]) & (t < bp[2]),
        (t >= bp[2]) & (t < bp[3]),
        t >= bp[3],
    ]
    y_select = np.select(conds, vals)
    np.testing.assert_allclose(y_jumps, y_select, atol=1e-12)


@pytest.mark.parametrize(
    ("bp", "vals"),
    [
        ([0.0, 1.0], [1.0, 2.0]),
        ([0.0, 1.0], [1.0, 2.0, 3.0, 4.0]),
        ([1.0, 0.0], [1.0, 2.0, 3.0]),
        ([1.0, 1.0], [1.0, 2.0, 3.0]),
        ([[0.0, 1.0]], [1.0, 2.0, 3.0]),
    ],
)
def test_piecewise_rejects_invalid_inputs(bp, vals):
    with pytest.raises(ValueError):
        piecewise_from_jumps(0.0, bp, vals)


def test_piecewise_does_not_mutate_inputs():
    t = np.array([-1.0, 0.5, 2.0])
    bp = np.array([0.0, 1.0])
    vals = np.array([1.0, 2.0, 0.0])
    t_c, bp_c, vals_c = t.copy(), bp.copy(), vals.copy()

    piecewise_from_jumps(t, bp, vals)

    assert np.array_equal(t, t_c)
    assert np.array_equal(bp, bp_c)
    assert np.array_equal(vals, vals_c)
