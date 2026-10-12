"""Все проверки из seisdsp.verification должны проходить."""

import pytest

from seisdsp import verification


@pytest.mark.parametrize("check", verification.ALL_CHECKS)
def test_check_passes(check):
    result = check()
    assert result["ok"], (
        f"{result['name']}: получено {result['measured']}, "
        f"ожидалось {result['expected']} (ошибка {result['error']:.3e})"
    )


def test_run_all_returns_every_check():
    assert len(verification.run_all()) == len(verification.ALL_CHECKS)
