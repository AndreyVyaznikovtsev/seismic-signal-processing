"""Тесты матрицы разностного оператора."""

import numpy as np
import pytest

from seisdsp.operators import difference_matrix


def test_shapes():
    assert difference_matrix(4, "zero").shape == (4, 4)
    assert difference_matrix(4, "periodic").shape == (4, 4)
    assert difference_matrix(4, "valid").shape == (3, 4)


def test_diagonals_zero():
    a = difference_matrix(4, "zero")
    assert np.all(np.diag(a) == 1)
    assert np.all(np.diag(a, -1) == -1)
    assert a[0, 3] == 0


def test_corner_periodic():
    a = difference_matrix(4, "periodic")
    assert np.all(np.diag(a) == 1)
    assert np.all(np.diag(a, -1) == -1)
    assert a[0, 3] == -1


def test_values_valid():
    a = difference_matrix(4, "valid")
    assert np.array_equal(a[0], [-1, 1, 0, 0])
    assert np.array_equal(a[2], [0, 0, -1, 1])


def test_determinants():
    assert np.isclose(np.linalg.det(difference_matrix(4, "zero")), 1.0)
    assert np.isclose(np.linalg.det(difference_matrix(4, "periodic")), 0.0)


@pytest.mark.parametrize("boundary", ["periodic", "valid"])
def test_constant_in_kernel(boundary):
    a = difference_matrix(4, boundary)
    assert np.allclose(a @ np.ones(4), 0.0)


def test_bad_boundary():
    with pytest.raises(ValueError, match="periodic"):
        difference_matrix(4, "reflect")


@pytest.mark.parametrize("n", [1, 0, -3, 2.5, "4"])
def test_bad_n(n):
    with pytest.raises(ValueError):
        difference_matrix(n, "zero")
