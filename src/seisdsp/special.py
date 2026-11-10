"""Специальные сигналы: приближения обобщённых функций."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike


def rect_delta(t: ArrayLike, eps: float) -> np.ndarray:
    """Прямоугольное приближение дельта-функции Дирака.

    Прямоугольник ширины ``eps`` и высоты ``1 / eps``: площадь равна
    единице при любом ``eps``, а при ``eps -> 0`` он «стягивается»
    в идеальный импульс.

    Parameters
    ----------
    t : array_like
        Точки, в которых вычисляется приближение (обычно сдвиги
        относительно центра импульса).
    eps : float
        Ширина прямоугольника, строго положительная.

    Returns
    -------
    ndarray
        ``1 / eps`` при ``|t| <= eps / 2`` (края включены), ``0`` вне.

    Raises
    ------
    ValueError
        Если ``eps <= 0``.
    """
    if eps <= 0:
        raise ValueError("eps должно быть положительным")
    t = np.asarray(t, dtype=float)
    return np.where(np.abs(t) <= eps / 2, 1.0 / eps, 0.0)
