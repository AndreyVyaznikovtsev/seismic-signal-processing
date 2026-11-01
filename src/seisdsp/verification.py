"""Проверки реализаций против аналитических результатов.

Это не замена тестам, а то, что тесты вызывают, а главы учебника
могут показывать читателю. Каждая проверка возвращает словарь
с измеренным и ожидаемым значением, чтобы результат можно было
напечатать в тексте.

Правило проекта: **новая тема приносит сюда хотя бы одну проверку.**
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike

from seisdsp.sequences import circular_convolve, delta, linear_convolve
from seisdsp.special import piecewise_from_jumps

TOL = 1e-10


def _result(name: str, measured: float, expected: float, tol: float = TOL) -> dict:
    return {
        "name": name,
        "measured": float(measured),
        "expected": float(expected),
        "error": float(abs(measured - expected)),
        "ok": bool(abs(measured - expected) <= tol),
    }


def check_convolution_support(n_x: int, n_h: int) -> dict:
    """Длина линейной свёртки равна ``L + M - 1``."""
    y = linear_convolve(np.ones(n_x), np.ones(n_h))
    return _result("длина линейной свёртки", y.size, n_x + n_h - 1, tol=0)


def check_delta_is_identity(length: int = 16) -> dict:
    """Свёртка с дельтой не меняет сигнал, а со сдвинутой — сдвигает."""
    rng = np.random.default_rng(0)
    x = rng.standard_normal(length)
    y = linear_convolve(x, delta(0, 1))
    return _result("свёртка с дельтой", np.max(np.abs(y - x)), 0.0)


def check_parseval(x: ArrayLike) -> dict:
    """Равенство Парсеваля: ``sum|x|^2 == (1/N) sum|X|^2``."""
    x = np.asarray(x, dtype=float)
    X = np.fft.fft(x)
    lhs = float(np.sum(np.abs(x) ** 2))
    rhs = float(np.sum(np.abs(X) ** 2) / x.size)
    return _result("равенство Парсеваля", lhs, rhs, tol=1e-8 * max(1.0, lhs))


def check_dft_of_delta(length: int = 32) -> dict:
    """ДПФ дельты в нуле — константа, равная единице во всех отсчётах."""
    X = np.fft.fft(delta(0, length))
    return _result("ДПФ дельты", np.max(np.abs(X - 1.0)), 0.0, tol=1e-12)


def check_circular_equals_linear(n_x: int = 8, n_h: int = 5) -> dict:
    """Циклическая свёртка после дополнения нулями совпадает с линейной.

    Дополнять надо до ``L + M - 1`` — иначе хвост завернётся на начало.
    """
    rng = np.random.default_rng(1)
    x = rng.standard_normal(n_x)
    h = rng.standard_normal(n_h)

    n_full = n_x + n_h - 1
    xp = np.concatenate([x, np.zeros(n_full - n_x)])
    hp = np.concatenate([h, np.zeros(n_full - n_h)])

    diff = np.max(np.abs(circular_convolve(xp, hp) - linear_convolve(x, h)))
    return _result("циклическая против линейной", diff, 0.0, tol=1e-10)


def check_piecewise_from_jumps() -> dict:
    """Кусочно-постоянная функция через скачки совпадает с прямой разметкой."""
    t = np.linspace(-2.0, 5.0, 350)
    bp = [-1.0, 0.5, 2.0, 3.5]
    vals = [1.0, 3.0, -1.0, 2.5, 0.0]
    y_jumps = piecewise_from_jumps(t, bp, vals)
    conds = [
        t < bp[0],
        (t >= bp[0]) & (t < bp[1]),
        (t >= bp[1]) & (t < bp[2]),
        (t >= bp[2]) & (t < bp[3]),
        t >= bp[3],
    ]
    y_direct = np.select(conds, vals)
    diff = float(np.max(np.abs(y_jumps - y_direct)))
    return _result("кусочно-постоянная через ступеньки", diff, 0.0, tol=1e-12)


ALL_CHECKS = (
    lambda: check_convolution_support(7, 4),
    lambda: check_delta_is_identity(),
    lambda: check_parseval(np.random.default_rng(2).standard_normal(64)),
    lambda: check_dft_of_delta(),
    lambda: check_circular_equals_linear(),
    lambda: check_piecewise_from_jumps(),
)


def run_all() -> list[dict]:
    """Прогнать все проверки и вернуть список результатов."""
    return [check() for check in ALL_CHECKS]
