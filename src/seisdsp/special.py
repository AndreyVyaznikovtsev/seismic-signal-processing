"""Специальные функции и кусочно-постоянные представления."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def piecewise_from_jumps(
    t: ArrayLike,
    breakpoints: ArrayLike,
    values: ArrayLike,
    u0: float = 0.5,
) -> float | NDArray[np.float64]:
    """Кусочно-постоянная функция как сумма функций Хевисайда.

    Собирает функцию по формуле
    ``f(t) = v_0 + sum_{k=1}^N (v_k - v_{k-1}) * u(t - t_k)``,
    где ``t_k`` — точки разрыва, а ``v_k`` — значения на интервалах.

    Parameters
    ----------
    t
        Точка или массив точек, в которых вычисляется функция.
    breakpoints
        Одномерный список или массив из ``N`` строго возрастающих точек разрыва.
    values
        Одномерный список или массив из ``N + 1`` значений функции:
        ``values[0]`` до первой точки разрыва, ``values[k]`` между
        ``breakpoints[k - 1]`` и ``breakpoints[k]``, ``values[-1]`` после последней.
    u0
        Значение функции Хевисайда в нуле (по умолчанию ``0.5``).

    Returns
    -------
    float or NDArray
        Значение функции (скаляр или массив того же размера, что ``t``).

    Raises
    ------
    ValueError
        Если размерности не согласованы или точки разрыва не упорядочены
        строго по возрастанию.

    Examples
    --------
    >>> piecewise_from_jumps(0.5, [0.0, 1.0], [0.0, 2.0, 0.0])
    2.0
    """
    bp = np.asarray(breakpoints, dtype=float)
    vals = np.asarray(values, dtype=float)

    if bp.ndim != 1 or vals.ndim != 1:
        raise ValueError("breakpoints и values должны быть одномерными")
    if vals.size != bp.size + 1:
        raise ValueError(
            f"ожидалось len(values) == len(breakpoints) + 1, "
            f"получено {vals.size} и {bp.size}"
        )
    if bp.size > 1 and not np.all(np.diff(bp) > 0):
        raise ValueError("точки разрыва breakpoints должны строго возрастать")

    t_arr = np.asarray(t, dtype=float)
    result = np.full_like(t_arr, vals[0], dtype=float)

    for k in range(bp.size):
        jump = vals[k + 1] - vals[k]
        result = result + jump * np.heaviside(t_arr - bp[k], u0)

    if np.ndim(t) == 0:
        return float(result)
    return result
