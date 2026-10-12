"""Тесты базовых операций над последовательностями."""

import numpy as np
import pytest

from seisdsp.sequences import circular_convolve, delta, linear_convolve, unit_step


def test_delta_position():
    assert np.array_equal(delta(1, 4), [0.0, 1.0, 0.0, 0.0])


def test_delta_outside_range_is_zero():
    assert np.all(delta(10, 4) == 0.0)


def test_delta_rejects_bad_length():
    with pytest.raises(ValueError):
        delta(0, 0)


def test_unit_step():
    assert np.array_equal(unit_step(5, n0=2), [0.0, 0.0, 1.0, 1.0, 1.0])


@pytest.mark.parametrize(("n_x", "n_h"), [(1, 1), (7, 4), (3, 9), (16, 16)])
def test_convolution_support_length(n_x, n_h):
    y = linear_convolve(np.ones(n_x), np.ones(n_h))
    assert y.size == n_x + n_h - 1


def test_convolution_matches_numpy():
    rng = np.random.default_rng(42)
    x, h = rng.standard_normal(9), rng.standard_normal(5)
    np.testing.assert_allclose(linear_convolve(x, h), np.convolve(x, h), atol=1e-12)


def test_convolution_is_commutative():
    rng = np.random.default_rng(7)
    x, h = rng.standard_normal(6), rng.standard_normal(4)
    np.testing.assert_allclose(linear_convolve(x, h), linear_convolve(h, x), atol=1e-12)


def test_circular_convolve_wraps_around():
    # сдвиг на 5 в кольце Z_8, применённый к дельте в 5, даёт дельту в 2
    x = delta(5, 8)
    np.testing.assert_allclose(circular_convolve(x, x), delta(2, 8), atol=1e-12)


def test_circular_convolve_requires_equal_lengths():
    with pytest.raises(ValueError):
        circular_convolve(np.ones(4), np.ones(5))


def test_inputs_are_not_mutated():
    x, h = np.ones(4), np.ones(3)
    x_copy, h_copy = x.copy(), h.copy()
    linear_convolve(x, h)
    assert np.array_equal(x, x_copy) and np.array_equal(h, h_copy)
