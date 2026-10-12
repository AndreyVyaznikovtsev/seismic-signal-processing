# Обработка сейсмических сигналов

Открытый учебник и библиотека примеров по цифровой обработке сигналов
с приложением к сейсмическим данным.

Проект собирается силами студентов курса как настоящий open source:
задачи живут в [issues](../../issues), изменения приходят через pull request,
каждый PR проходит ревью и CI.

**Сайт:** публикуется автоматически из ветки `main`.

## Быстрый старт

```bash
git clone https://github.com/AndreyVyaznikovtsev/seismic-signal-processing.git
cd seismic-signal-processing
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pre-commit install

make test     # тесты
make site     # собрать сайт в _book/
```

Quarto ставится отдельно: <https://quarto.org/docs/get-started/>

## Структура

| Каталог | Что внутри |
|---|---|
| `chapters/` | главы учебника (`.qmd`) — теория, выводы, формулы |
| `notebooks/` | практические разборы (`.qmd` с исполняемым кодом) |
| `src/seisdsp/` | библиотека: реализации алгоритмов |
| `src/seisdsp/verification.py` | проверки реализаций против аналитики |
| `tests/` | pytest |
| `data/` | данные (**в git не хранятся**, см. `data/README.md`) |
| `docs/` | документы процесса: онбординг, гайды по тексту и рисункам |

Текст и код разнесены намеренно: главы не содержат численных методов,
а вызывают `seisdsp`. Благодаря этому правки в разные главы почти
не конфликтуют между собой, а код приходится переиспользовать,
а не копировать из раздела в раздел.

## Как поучаствовать

Начните с [docs/onboarding.md](docs/onboarding.md), затем
[CONTRIBUTING.md](CONTRIBUTING.md).

## Лицензии

- код (`src/`, `tests/`) — MIT, см. [LICENSE](LICENSE)
- тексты и рисунки (`chapters/`, `notebooks/`, `docs/`) — CC BY 4.0,
  см. [LICENSE-CONTENT](LICENSE-CONTENT)
