# Казино и Гуси — Лаба 4

Консольная симуляция казино с игроками, гусями и денежными потоками. Проект сделан в формате Python-пакета (`src/` layout), с пользовательскими коллекциями и псевдослучайной моделью (seed).

## Возможности

### Предметная модель

* `Player`: `balance`, `sanity`, `alive`, методы `can_act()`, `rest()`, `die()`, `apply_sanity()`
* `Goose` + наследники:

  * `WarGoose` — атака игроков
  * `HonkGoose` — «крик» (дебафф по sanity)
* `Chip` — value object, поддерживает `__add__`

### Пользовательские исключения

* `CustomError` — базовый класс
* `NotFoundError` — элемент не найден в коллекции
* `OutOfRangeError` — индекс вне диапазона
* `WrongTypeError` — неверный тип элемента
* `StepZeroError` — шаг среза = 0

### Пользовательские коллекции (требования лабы)

* Списковая коллекция (`PlayerCollection`, `GooseCollection`):

  * `__len__`, `__iter__`, `__getitem__` (индексы и срезы), `__setitem__`, `__delitem__`
  * добавление/удаление элементов, `append()`, `remove()`
* Словарная коллекция балансов (`Balance`):

  * `name -> balance`
  * логирование изменений через `__setitem__`
  * используется для отслеживания балансов игроков и гусей

### Симуляция

* `run_simulation(steps=..., seed=...)` — детерминированный прогон с seed
* **Случайные события:**

  * **Рулетка** — ставки на `0/00/red/black` с выплатами
  * **Слоты** — денежные выплаты + изменение sanity
  * **Крик HonkGoose** — дебафф sanity + взимание 5% баланса (макс $50)
  * **Атака WarGoose** — кража денег у игроков, может убить
* **Обязательные события:**

  * Проверка игроков с sanity=0 (пропускают ход или восстанавливаются)
  * Russian Roulette при 2+ банкротах (победитель получает $5000, проигравший умирает)
  * Банкротство казино (при отрицательном bankroll)
* Логи каждого шага в консоль (через loguru)
* Финальная статистика (изменения балансов, sanity, смерти игроков)

### Конфигурация (Pydantic Settings)

* Все ключевые константы лежат в `settings.py`
* Поддержка переменных окружения с префиксом `CASINO_`

## Примеры

```bash
# детерминированный прогон (100 шагов, seed=42)
uv run python main.py
```

> **Примечание:** Параметры `steps` и `seed` задаются в `main.py`

Пример переменных окружения (PowerShell):

```powershell
$env:CASINO_SLOT_SPIN_COST=20
$env:CASINO_SANITY_SKIP_TURN_CHANCE=0.8
uv run python main.py
```

## Установка и запуск (uv)

```bash
uv sync
uv run python main.py
```

## Структура проекта

```
.
├── src/
│   └── casino_lab4/
│       ├── domain/
│       │   ├── player.py
│       │   ├── goose.py
│       │   └── chip.py
│       ├── collections/
│       │   ├── players.py
│       │   ├── geese.py
│       │   └── balances.py
│       ├── simulation/
│       │   ├── casino.py
│       │   ├── events.py
│       │   ├── event_types.py
│       │   ├── runner.py
│       │   ├── setup.py
│       │   ├── stats.py
│       │   ├── selectors.py
│       │   └── randomization.py
│       ├── core/
│       │   └── errors.py
│       ├── utils/
│       │   ├── logging.py
│       │   └── misc.py
│       └── settings.py
├── tests/
│   ├── domain/
│   ├── collections/
│   └── simulation/
├── main.py
├── pyproject.toml
└── uv.lock
```

## Тесты

```bash
uv run pytest
```

Покрытие в консоли (с подсветкой пропусков):

```bash
uv run pytest --cov=src/casino_lab4 --cov-report=term-missing
```

HTML отчёт:

```bash
uv run pytest --cov=src/casino_lab4 --cov-report=html
```

Текущее покрытие: **96%** (119 тестов)

## Код-стайл и типы

* **pre-commit**: `pre-commit run --all-files` (запускает mypy, ruff, yaml/toml checks)
* **ruff**: `uv run ruff check` (автофикс: `uv run ruff check --fix`)
* **mypy**: `uv run mypy src` (проверка типов)
