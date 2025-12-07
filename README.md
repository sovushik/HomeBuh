# HomeBuh — Домашняя бухгалтерия

Полнофункциональное веб-приложение для управления личными финансами: расходы, доходы, категории и подкатегории, прикрепление файлов к операциям, планирование будущих поступлений и расходов, управление счетами (карта, банк, вклад) с возможностью переводов между ними. Встроена система AI-отчётов — создавайте отчёты по запросу с автоматической генерацией графиков.

Это современное приложение с рабочим backend (FastAPI), интерактивным frontend (React + Vite) в формате PWA, полным набором unit тестов и CI/CD pipeline на GitHub Actions.

**Ключевые возможности в версии 0.1.0:**

### Backend (API)
- **CRUD операции:**
  - Категории и подкатегории расходов/доходов
  - Счёта (карта, банк, вклад и т.д.)
  - Транзакции с привязкой к счётам и категориям
  - Бюджеты по категориям и месяцам
  - Планируемые расходы/доходы

- **Расширенный функционал:**
  - Загрузка и хранение файлов (чеки, квитанции, документы)
  - Переводы между счетами с автоматической валидацией (проверка баланса, разные счета)
  - AI-powered отчеты: генерация диаграмм (bar, line, pie) по запросу пользователя
  - Интеграция с OpenAI для естественного анализа финансов (опционально)

- **Валидация и качество:**
  - Pydantic схемы для всех эндпоинтов
  - Автоматическая документация OpenAPI (Swagger UI)
  - Unit тесты (pytest): 60+ тестов для всех операций

### Frontend (UI)
- **Компонентная архитектура:**
  - Отдельные страницы для категорий, бюджетов, счётов, переводов и AI-отчётов
  - Навигация по вкладкам для удобства
  - Таблицы, формы, селекты с реальными данными
  - Обработка ошибок и статус-сообщения

- **PWA:**
  - Манифест для установки на устройства
  - Service worker заготовка для офлайн-функционала
  - Адаптивный дизайн

- **UX:**
  - Информативная главная страница с описанием функций
  - Валидация форм (проверка пустых полей, положительных сумм и т.д.)
  - Отображение сгенерированных AI-отчётов с графиками в реальном времени

### DevOps
- **GitHub Actions CI:**
  - Тестирование Python 3.10, 3.11
  - Сборка и проверка frontend (Node 18, 20)
  - Автоматический запуск pytest при каждом push

- **Документация:**
  - `README.md` — полное описание и инструкции
  - `CHANGELOG.md` — версионирование и история изменений
  - `LICENSE` — MIT лицензия
  - `backend/TESTS.md` — инструкции по запуску тестов

---

## Архитектура проекта

```
HomeBuh/
├── backend/                      # FastAPI сервер
│   ├── main.py                  # API эндпоинты
│   ├── models.py                # SQLModel модели (Category, Account, Transaction и т.д.)
│   ├── schemas.py               # Pydantic валидация (Request/Response)
│   ├── db.py                    # Инициализация БД
│   ├── utils.py                 # Утилиты (генерация графиков)
│   ├── test_main.py             # Unit тесты (pytest)
│   ├── requirements.txt          # Python зависимости
│   ├── uploads/                 # Загруженные файлы
│   └── reports/                 # Сгенерированные отчёты
│
├── frontend/                    # React + Vite приложение
│   ├── src/
│   │   ├── pages/              # Компоненты страниц
│   │   │   ├── Categories.jsx
│   │   │   ├── Budgets.jsx
│   │   │   ├── Accounts.jsx
│   │   │   ├── Transfers.jsx
│   │   │   └── Reports.jsx
│   │   ├── App.jsx             # Главное приложение с навигацией
│   │   ├── main.jsx            # React entry point
│   │   └── service-worker.js   # PWA service worker
│   ├── index.html              # HTML template
│   ├── manifest.json           # PWA манифест
│   └── package.json            # Node зависимости
│
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI workflow
│
├── README.md                    # Это описание
├── CHANGELOG.md                 # История изменений и версии
├── LICENSE                      # MIT лицензия
└── .gitignore
```

---

## Быстрый старт (локально)

### Backend

```bash
# Переходим в папку backend
cd backend

# Создаём виртуальное окружение
python3 -m venv venv

# Активируем виртуальное окружение
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Запускаем сервер (reload для разработки)
uvicorn main:app --reload --port 8000
```

Проверка здоровья сервера:
```bash
curl http://localhost:8000/api/health
# Ожидаемо: {"status":"ok"}
```

Swagger UI (документация API):
```
http://localhost:8000/docs
```

### Frontend

В отдельном терминале:

```bash
# Переходим в папку frontend
cd frontend

# Устанавливаем зависимости
npm install

# Запускаем dev сервер
npm run dev
```

Приложение откроется на адресе, который выведет Vite (обычно `http://localhost:5173`).

### Тестирование backend

```bash
cd backend

# Запустить все тесты
pytest test_main.py -v

# Запустить с покрытием
pytest test_main.py --cov=. --cov-report=html

# Запустить конкретный тест
pytest test_main.py::TestTransfer::test_successful_transfer -v
```

Дополнительно см. `backend/TESTS.md` для подробных инструкций.

---

## API Endpoints (основные)

### Категории
- `POST /api/categories` — создать категорию/подкатегорию
- `GET /api/categories` — список всех категорий

### Счёта
- `POST /api/accounts` — создать счёт
- `GET /api/accounts` — список всех счётов

### Транзакции
- `POST /api/transactions` — создать транзакцию
- `GET /api/transactions` — список транзакций

### Бюджеты
- `POST /api/budgets` — создать бюджет (месяц + категория)
- `GET /api/budgets` — список бюджетов

### Планируемые операции
- `POST /api/planned` — создать планируемый расход/доход
- `GET /api/planned` — список планов

### Переводы между счётами
- `POST /api/transfer` — выполнить перевод денег между счётами
  ```json
  {
    "from_account_id": 1,
    "to_account_id": 2,
    "amount": 100.0,
    "currency": "USD"
  }
  ```

### Загрузка файлов
- `POST /api/upload` — загрузить файл
- `GET /api/uploads/{name}` — скачать загруженный файл

### AI-отчёты
- `POST /api/ai/chat` — создать отчёт по запросу
  ```json
  {
    "prompt": "Сделай отчет по расходам за 2025-12 по категориям, построй круговую диаграмму"
  }
  ```

Полная документация доступна в Swagger UI (`/docs`).

---

## Конфигурация и интеграция

### OpenAI для AI-отчётов (опционально)

Если хотите использовать OpenAI для анализа финансов, установите переменную окружения перед запуском backend:

```bash
export OPENAI_API_KEY="sk-..."
uvicorn main:app --reload --port 8000
```

Без ключа система работает в режиме fallback — генерирует простые диаграммы из данных БД.

### Environment переменные

Создайте файл `.env` в папке `backend` (опционально):

```
OPENAI_API_KEY=sk-...
```

---

## CI/CD

GitHub Actions автоматически:
- Проверяет синтаксис Python и Node
- Запускает pytest для всех тестов
- Собирает frontend (`npm run build`)
- Выполняет lint проверки

Смотрите `.github/workflows/ci.yml` для деталей.

---

## Развитие и приоритеты

### Краткосрочно (версия 0.2.0)
- [ ] Аутентификация и multi-user модель (JWT)
- [ ] Улучшить PWA: офлайн-кеш, background sync
- [ ] Интерактивные графики (Chart.js / Recharts вместо matplotlib)
- [ ] Фильтры и поиск в списках

### Среднесрочно (версия 0.3.0)
- [ ] Интеграция с банковскими API
- [ ] Экспорт отчётов (PDF, Excel)
- [ ] Уведомления при превышении бюджета
- [ ] Статистика и аналитика на главной странице

### Долгосрочно
- [ ] Мобильное приложение (React Native)
- [ ] Синхронизация между устройствами
- [ ] Расширенные AI-отчёты и прогнозирование

---

## Технический стек

**Backend:**
- FastAPI — современный веб-фреймворк на Python
- SQLModel — ORM с Pydantic интеграцией
- SQLite — встроенная БД для локального развития
- Matplotlib — генерация графиков
- Pytest — тестирование

**Frontend:**
- React 18 — UI библиотека
- Vite — быстрая сборка и dev сервер
- PWA — возможность установить как приложение

**DevOps:**
- GitHub Actions — CI/CD
- Docker-ready (можно добавить Dockerfile для продакшена)

---

## Лицензия

Проект выпущен под лицензией MIT. Смотрите файл `LICENSE`.

---

## Вклад и поддержка

Проект активно развивается. Если у вас есть идеи, сообщайте через Issues на GitHub.

Для локальной разработки:
1. Форкируйте репозиторий
2. Создайте ветку для вашей фичи (`git checkout -b feature/my-feature`)
3. Коммитьте изменения (`git commit -m "Add my feature"`)
4. Пушьте в ветку (`git push origin feature/my-feature`)
5. Откройте Pull Request

---

## Контакты и информация

**Репозиторий:** https://github.com/sovushik/HomeBuh  
**Версия:** 0.1.0  
**Дата релиза:** 2025-12-07  
**Статус:** Активная разработка

Спасибо за внимание к проекту!
Проект: простая домашняя бухгалтерия с backend (FastAPI) и frontend (React + Vite) в PWA-обёртке.

Запуск backend:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Запуск frontend (dev):

```bash
cd frontend
npm install
npm run dev
```

AI-отчёты: если хотите интегрировать с OpenAI, установите `OPENAI_API_KEY` в окружение перед запуском backend.

GitHub: создайте репозиторий и выполните `git push origin main` (инструкции ниже).
# HomeBuh