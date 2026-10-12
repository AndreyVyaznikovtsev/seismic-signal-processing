# Первые шаги

Цель этой страницы — довести вас до первого влитого pull request
за один вечер. Тема не важна, важен пройденный путь.

## 1. Поставить окружение

```bash
git clone https://github.com/AndreyVyaznikovtsev/seismic-signal-processing.git
cd seismic-signal-processing

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
pip install -e .
pre-commit install
```

Проверка, что всё встало:

```bash
make test
```

Должно быть зелено. Если нет, заведите issue с меткой `help wanted`
и приложите текст ошибки целиком.

Quarto ставится отдельно: <https://quarto.org/docs/get-started/>.
Без него соберутся тесты, но не сайт.

## 2. Взять задачу

Откройте [issues](../../issues) и отфильтруйте по метке
`good first issue`. В выбранной задаче напишите одну строку: «беру».
Так двое не возьмутся за одно и то же.

Для примера дальше разбирается задача №1 — завести `CONTRIBUTORS.md`.

## 3. Сделать ветку от свежего `main`

```bash
git switch main
git pull                 # обязательно
git switch -c docs/1-contributors
```

Строка `git pull` здесь не для красоты. Пока вы занимались прошлой
задачей, в `main` могли влить чужие правки. Ветка, отведённая от
устаревшего состояния, при вливании даст конфликт, и разбирать его
придётся вам. Чем дольше живёт ветка, тем больнее.

Схема имени ветки: `тип/номер-issue-краткое-описание`.

## 4. Поработать

Это главный шаг, и он состоит не из команд git, а из собственно работы:
нужно создать или изменить файлы.

Создаём `CONTRIBUTORS.md` в корне репозитория:

```markdown
# Участники

Спасибо всем, кто пишет этот учебник.

- Иван Петров — [@ipetrov](https://github.com/ipetrov)
```

Упоминаем файл в конце `README.md`:

```markdown
## Участники

Список тех, кто работал над проектом, — в [CONTRIBUTORS.md](CONTRIBUTORS.md).
```

Теперь смотрим, что git видит наши изменения:

```bash
git status
```

```
On branch docs/1-contributors
Changes not staged for commit:
        modified:   README.md
Untracked files:
        CONTRIBUTORS.md
```

Если в выводе пусто — вы ничего не изменили, и коммитить нечего.
Вернитесь и внесите правки.

Отбираем изменения и фиксируем:

```bash
git add CONTRIBUTORS.md README.md
git commit -m "docs: Завести список участников"
```

Хуки `pre-commit` проверят оформление перед коммитом. Если хук что-то
поправил сам, коммит не пройдёт: добавьте изменённые файлы заново
(`git add -A`) и повторите `git commit`.

Коммитов может быть несколько — делайте их небольшими и осмысленными.
Один коммит на «добавил файл», другой на «упомянул в README» — нормально.

Посмотреть, как получилось на сайте:

```bash
quarto preview
```

## 5. Открыть pull request

```bash
git push -u origin docs/1-contributors
gh pr create --fill
```

В описании напишите `Closes #1` — issue закроется сам при вливании.

Дальше пройдитесь по чек-листу из [CONTRIBUTING.md](../CONTRIBUTING.md)
и проставьте метки.

## 6. Пройти ревью

Придут замечания. Это нормально и означает, что ваш PR прочитали.
Отвечайте на каждое: правкой либо аргументом. После правок просто
пушьте в ту же ветку, pull request обновится сам.

Когда CI зелёный и рецензент согласен, мейнтейнер вольёт изменения.

## 7. Прибраться

```bash
git switch main
git pull
git branch -d docs/1-contributors
```

## Частые затруднения

**CI красный, а локально зелено.** Почти всегда забыли добавить файл
в коммит. Проверьте `git status` и `git show --stat HEAD`.

**Конфликт при вливании.** Подтяните `main` в свою ветку:

```bash
git fetch origin
git rebase origin/main
```

Разрешите конфликт в файлах, затем `git add` и `git rebase --continue`.

**Случайно закоммитили данные.** Напишите в issue, не пытайтесь чинить
историю сами: переписывание истории ломает ветки у всех остальных.
