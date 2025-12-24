# Казино и Гуси — Лаба 4

Консольная симуляция казино с игроками, гусями и денежными потоками. Проект сделан в формате Python-пакета (`src/` layout), с пользовательскими коллекциями и псевдослучайной моделью (seed).

- [Казино и Гуси — Лаба 4](#казино-и-гуси--лаба-4)
  - [Возможности](#возможности)
    - [Предметная модель](#предметная-модель)
    - [Пользовательские исключения](#пользовательские-исключения)
    - [Пользовательские коллекции (требования лабы)](#пользовательские-коллекции-требования-лабы)
    - [Симуляция](#симуляция)
    - [Конфигурация (Pydantic Settings)](#конфигурация-pydantic-settings)
  - [Примеры](#примеры)
    - [Доступные настройки](#доступные-настройки)
  - [Установка и запуск (uv)](#установка-и-запуск-uv)
  - [Структура проекта](#структура-проекта)
  - [Тесты](#тесты)
  - [Код-стайл и типы](#код-стайл-и-типы)

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
* Поддержка `.env` файла (автоматически загружается pydantic-settings)

## Примеры

```bash
# детерминированный прогон (100 шагов, seed=42)
uv run python main.py
```

> **Примечание:** Параметры `steps` и `seed` задаются в `main.py`

**Конфигурация через `.env` файл**

Создай файл `.env` в корне проекта:

```bash
# .env
CASINO_SIMULATION_STEPS=200
CASINO_SIMULATION_SEED=777
CASINO_USE_SEED=true

CASINO_SLOT_SPIN_COST=30
CASINO_PLAYER_START_CASH_MIN=500
CASINO_PLAYER_START_CASH_MAX=5000

CASINO_HONK_FEAR_FEE_PCT=0.10
CASINO_RUSSIAN_ROULETTE_PRIZE=10000
```


### Доступные настройки



| Переменная                           | Тип   | По умолчанию | Описание                                   |
| ------------------------------------ | ----- | ------------ | ------------------------------------------ |
| `CASINO_SIMULATION_STEPS`            | int   | 100          | Количество шагов симуляции                 |
| `CASINO_SIMULATION_SEED`             | int   | 42           | Seed для рандома                           |
| `CASINO_USE_SEED`                    | bool  | true         | Использовать ли seed                       |
| `CASINO_SLOT_SPIN_COST`              | int   | 20           | Стоимость спина в слотах                   |
| `CASINO_PLAYER_START_CASH_MIN`       | int   | 200          | Минимальный стартовый баланс игрока        |
| `CASINO_PLAYER_START_CASH_MAX`       | int   | 2000         | Максимальный стартовый баланс игрока       |
| `CASINO_HONK_SANITY_DEBUFF`          | int   | 10           | Дебафф sanity от крика HonkGoose           |
| `CASINO_HONK_FEAR_FEE_PCT`           | float | 0.05         | Процент баланса, крадущийся HonkGoose (5%) |
| `CASINO_HONK_FEAR_FEE_MAX`           | float | 50.0         | Максимальная сумма кражи HonkGoose         |
| `CASINO_RUSSIAN_ROULETTE_PRIZE`      | float | 5000.0       | Выигрыш в Russian Roulette                 |
| `CASINO_WARGOOSE_ATTACK_VICTIMS_MIN` | int   | 1            | Минимум жертв атаки WarGoose               |
| `CASINO_WARGOOSE_ATTACK_VICTIMS_MAX` | int   | 3            | Максимум жертв атаки WarGoose              |
| `CASINO_WARGOOSE_STEAL_PCT_MIN`      | float | 0.30         | Минимальный % кражи WarGoose               |
| `CASINO_WARGOOSE_STEAL_PCT_MAX`      | float | 0.50         | Максимальный % кражи WarGoose              |

> Все настройки имеют префикс `CASINO_` и **не** чувствительны к регистру.
> Если что табличку (и table of contents) делал через extension `Markdown All in One`.

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
