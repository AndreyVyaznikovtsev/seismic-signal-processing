"""Операторы курса: матрицы разностного оператора."""

from __future__ import annotations

import numpy as np

_BOUNDARIES = ("zero", "periodic", "valid")


def difference_matrix(n: int, boundary: str) -> np.ndarray:
    """Матрица разностного оператора ``y[n] = x[n] - x[n-1]``.

    Parameters
    ----------
    n : int
        Длина входной последовательности, ``n >= 2``.
    boundary : {"zero", "periodic", "valid"}
        Краевое условие: нулевое продолжение (``x[-1] = 0``),
        периодическое (``x[-1] = x[n-1]``) или усечённый выход
        (только отсчёты ``1, ..., n-1``).

    Returns
    -------
    numpy.ndarray
        Матрица формы ``(n, n)`` для ``"zero"`` и ``"periodic"``
        и ``(n - 1, n)`` для ``"valid"``.

    Raises
    ------
    ValueError
        Если ``boundary`` не из допустимых или ``n`` не целое, меньшее 2.

    Examples
    --------
    >>> difference_matrix(3, "valid")
    array([[-1.,  1.,  0.],
           [ 0., -1.,  1.]])
    """
    if boundary not in _BOUNDARIES:
        raise ValueError(
            f"boundary должен быть одним из {_BOUNDARIES}, получено {boundary!r}"
        )
    if not isinstance(n, int | np.integer) or n < 2:
        raise ValueError(f"n должно быть целым и не меньше 2, получено {n!r}")

    a = np.eye(n) - np.eye(n, k=-1)
    if boundary == "periodic":
        a[0, n - 1] = -1.0
    elif boundary == "valid":
        a = a[1:, :]
    return a
