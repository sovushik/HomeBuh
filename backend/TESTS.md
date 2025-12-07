# Запуск тестов backend

Тесты написаны с использованием pytest и TestClient для тестирования FastAPI эндпоинтов.

## Требования

Убедитесь, что установлены зависимости:
```bash
pip install -r requirements.txt
```

## Запуск тестов

Из директории `backend`:

```bash
# Запустить все тесты
pytest test_main.py -v

# Запустить тесты с покрытием
pytest test_main.py --cov=. --cov-report=html

# Запустить конкретный класс тестов
pytest test_main.py::TestCategories -v

# Запустить конкретный тест
pytest test_main.py::TestCategories::test_create_category -v
```

## Структура тестов

Тесты организованы по классам для каждого основного модуля:
- `TestHealth` — проверка здоровья сервиса
- `TestCategories` — CRUD категорий и подкатегорий
- `TestAccounts` — управление счетами
- `TestTransactions` — создание и отслеживание транзакций
- `TestBudgets` — управление бюджетами
- `TestPlannedItems` — планируемые доходы/расходы
- `TestTransfer` — переводы между счетами (включая validation)
- `TestAIChat` — AI-отчеты

## Интеграция с CI

Тесты автоматически запускаются в GitHub Actions workflow при каждом push в main.
