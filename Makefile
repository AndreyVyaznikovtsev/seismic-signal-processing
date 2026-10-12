.PHONY: help test lint fix site preview clean

help:
	@echo "make test     — прогнать тесты"
	@echo "make lint     — проверить стиль"
	@echo "make fix      — починить стиль автоматически"
	@echo "make site     — собрать сайт в _book/"
	@echo "make preview  — сайт с автообновлением"
	@echo "make clean    — убрать артефакты сборки"

test:
	pytest

lint:
	ruff check .
	ruff format --check .

fix:
	ruff check --fix .
	ruff format .

site:
	quarto render

preview:
	quarto preview

clean:
	rm -rf _book .quarto .pytest_cache .ruff_cache
	find . -name __pycache__ -type d -exec rm -rf {} +
