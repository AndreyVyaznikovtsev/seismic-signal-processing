"""Базовые операции над конечными последовательностями.

Модуль намеренно небольшой: он задаёт образец того, как оформляется
реализация в этом проекте. Каждая функция обязана:

* документировать область определения результата;
* не изменять входные массивы;
* иметь проверку в :mod:`seisdsp.verification`.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def delta(n: int, length: int) -> NDArray[np.float64]:
    """Дельта Кронекера как последовательность длины ``length``.

    Parameters
    ----------
    n
        Позиция единицы.
    length
        Длина последовательности.

    Returns
    -------
    NDArray
        Массив длины ``length``, равный единице в позиции ``n`` и нулю иначе.

    Examples
    --------
    >>> delta(1, 4)
    array([0., 1., 0., 0.])
    """
    if length <= 0:
        raise ValueError("length должна быть положительной")
    x = np.zeros(length, dtype=float)
    if 0 <= n < length:
        x[n] = 1.0
    return x


def unit_step(length: int, n0: int = 0) -> NDArray[np.float64]:
    """Единичная ступенька: единица при ``n >= n0``, ноль иначе."""
    if length <= 0:
        raise ValueError("length должна быть положительной")
    n = np.arange(length)
    return (n >= n0).astype(float)


def linear_convolve(x: ArrayLike, h: ArrayLike) -> NDArray[np.float64]:
    """Линейная свёртка двух конечных последовательностей.

    Для носителей длины ``L`` и ``M`` результат имеет длину ``L + M - 1``:
    это прямое следствие границ суммирования
    ``max(0, n - M + 1) <= k <= min(L - 1, n)``.

    Notes
    -----
    Реализация намеренно прямая, без БПФ: она служит эталоном,
    относительно которого проверяются быстрые варианты.
    """
    x = np.asarray(x, dtype=float)
    h = np.asarray(h, dtype=float)
    if x.ndim != 1 or h.ndim != 1:
        raise ValueError("ожидаются одномерные последовательности")

    L, M = x.size, h.size
    y = np.zeros(L + M - 1, dtype=float)
    for n in range(L + M - 1):
        k_lo = max(0, n - M + 1)
        k_hi = min(L - 1, n)
        for k in range(k_lo, k_hi + 1):
            y[n] += x[k] * h[n - k]
    return y


def circular_convolve(x: ArrayLike, h: ArrayLike) -> NDArray[np.float64]:
    """Циклическая свёртка на кольце ``Z_N``.

    Обе последовательности должны иметь одинаковую длину ``N``.
    Индексы берутся по модулю ``N``: за краем записи начинается её начало.
    """
    x = np.asarray(x, dtype=float)
    h = np.asarray(h, dtype=float)
    if x.shape != h.shape:
        raise ValueError("длины должны совпадать")

    N = x.size
    y = np.zeros(N, dtype=float)
    for n in range(N):
        for m in range(N):
            y[n] += x[m] * h[(n - m) % N]
    return y
