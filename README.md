# HomeBuh — Домашняя бухгалтерия

Домашнее веб-приложение для учёта личных финансов: расходы, доходы, бюджеты по категориям и подкатегориям, прикрепление файлов к операциям, планирование будущих поступлений и расходов, управление счетами (карта, банк, вклад) и промежуточные переводы между ними. Проект включает серверную часть (FastAPI) и клиент (React + Vite) с PWA-заготовкой.

Это минимальная, но расширяемая заготовка — цель ускорить дальнейшую разработку и интеграцию AI-отчётов.

**Ключевые возможности в текущей версии**
- CRUD для категорий и подкатегорий.
- Управление счетами (`Account`) и транзакциями (`Transaction`).
- Возможность прикреплять файлы (чеки, квитанции) к транзакциям.
- Бюджеты по категории/месяцу (`Budget`).
- Планируемые операции (`PlannedItem`) — расходы/доходы с датой.
- Генерация простых отчётов с PNG-диаграммой и заглушкой для AI-обработки (`/api/report`).
- Минимальный frontend (React) с PWA-манифестом и простым service-worker.

**Архитектура**
- Backend: `backend/` — FastAPI + SQLModel (SQLite), загрузка файлов, генерация графиков (matplotlib).
- Frontend: `frontend/` — Vite + React, PWA-манифест и service-worker-заготовка.

Файловая структура (основное):

- `backend/` — сервер
	- `main.py` — точки доступа API
	- `models.py` — модели данных (SQLModel)
	- `db.py` — инициализация базы
	- `uploads/` — загруженные файлы (локально)
	- `reports/` — сгенерированные отчёты
- `frontend/` — клиентская часть (Vite + React)
- `CHANGELOG.md` — история изменений
- `README.md` — это описание

## Быстрый старт (локально)

Backend:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Проверка: откройте `http://localhost:8000/api/health` — должно вернуть `{"status":"ok"}`.

Frontend (dev):
```bash
cd frontend
npm install
npm run dev
```

## Конфигурация AI-отчётов
Если хотите, чтобы endpoint `/api/report` пересылал запросы в OpenAI, установите переменную окружения `OPENAI_API_KEY` перед запуском backend. В текущей реализации есть простая заглушка и пример вызова OpenAI REST API — для продакшн-интеграции рекомендуется использовать официальный SDK и настроить шаблоны запросов.

## Развитие и приоритеты
- Добавить аутентификацию (JWT) и multi-user модель.
- Расширить фронтенд интерфейс (CRUD/UX для всех сущностей).
- Расширить PWA: офлайн-кеш, background sync, нотификации.
- Интерактивные графики (Chart.js / Recharts) для отчётов.
- Полноценная интеграция с OpenAI: шаблоны, лимиты, парсинг.

## Вклад в развитие и выпуск на GitHub
Инструкции для быстрого пуша в репозиторий GitHub (если репозиторий ещё не создан):

```bash
cd /workspaces/HomeBuh
git init
git add .
git commit -m "Initial HomeBuh scaffolding: backend + frontend + PWA"
# создайте репозиторий на GitHub (через веб или gh CLI), затем:
git remote add origin git@github.com:<ваш-login>/<repo>.git
git push -u origin main
```

Или используя `gh` (gh CLI создаст репозиторий и отправит коммит):

```bash
gh repo create <repo-name> --public --source=. --push
```

## License
Проект не содержит автоматически применяемого лицензионного файла. Добавьте `LICENSE` по необходимости.

## Ссылки
- См. `CHANGELOG.md` для истории изменений и планов по релизам.

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