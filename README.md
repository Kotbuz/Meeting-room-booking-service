# Meeting-room-booking-service

Сервис автоматизации бронирования переговорных комнат в коворкинге.

## Описание

Приложение позволяет:

- регистрировать и аутентифицировать пользователей по JWT;
- работать с ролями `admin` и `user`;
- просматривать доступные комнаты и временные слоты;
- создавать, просматривать и отменять бронирования;
- ограничивать доступ к чужим броням и контролировать права администраторов.

## Технологический стек

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Alembic
- JWT (`python-jose`)
- pytest
- Docker / Docker Compose

## Требования

Перед запуском установите:

- Python 3.11+
- Poetry
- Docker и Docker Compose

## Конфигурация окружения

Создайте файл `.env` на основе `.env.example`:

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=meeting_room_booking
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
APP_HOST_PORT=8000
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ADMIN_LOGIN=admin
ADMIN_PASSWORD=admin
```

Важно:

- для локального запуска `POSTGRES_HOST=localhost`;
- для запуска через Docker Compose приложение подключается к контейнеру `db` через `POSTGRES_HOST=db`;
- `ADMIN_LOGIN` и `ADMIN_PASSWORD` используются для bootstrap-администратора при старте приложения.

## Локальный запуск через Poetry

1. Установите зависимости:

```bash
poetry install
```

2. Запустите PostgreSQL в контейнере:

```bash
docker compose up -d db
```

3. Запустите сервер:

```bash
poetry run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

4. Откройте API:

```text
http://127.0.0.1:8000/docs
```

## Запуск через Docker Compose

Соберите и запустите весь стек из одного файла:

```bash
docker compose up --build
```

После запуска:

- приложение будет доступно по адресу `http://127.0.0.1:8000`
- PostgreSQL будет поднят в контейнере `db`
- после старта будет создан административный пользователь из переменных `ADMIN_LOGIN` и `ADMIN_PASSWORD`

## Запуск контейнера через `docker run`

Сначала соберите образ:

```bash
docker build -t meeting-room-booking-service .
```

Затем запустите контейнер, если PostgreSQL уже доступен по адресу, указанному в `.env`:

```bash
docker run --rm -p 8000:8000 --env-file .env meeting-room-booking-service
```

> Для контейнера `POSTGRES_HOST` должен указывать на реально доступный хост с PostgreSQL. Для локального окружения это обычно `localhost` или `host.docker.internal`.

## Основные API-маршруты

### Аутентификация

#### Вход в систему

```bash
curl -X POST "http://127.0.0.1:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin"
```

Ответом будет JWT-токен.

#### Данные текущего пользователя

```bash
curl "http://127.0.0.1:8000/api/auth/me" \
  -H "Authorization: Bearer <access_token>"
```

### Комнаты

```bash
curl "http://127.0.0.1:8000/api/rooms/" \
  -H "Authorization: Bearer <access_token>"
```

Поиск свободных комнат:

```bash
curl "http://127.0.0.1:8000/api/rooms/free?date=2026-08-01&start=09:00:00&end=11:00:00" \
  -H "Authorization: Bearer <access_token>"
```

### Таймслоты

```bash
curl "http://127.0.0.1:8000/api/timeslots/" \
  -H "Authorization: Bearer <access_token>"
```

### Бронирования

Список бронирований текущего пользователя:

```bash
curl "http://127.0.0.1:8000/api/bookings/me" \
  -H "Authorization: Bearer <access_token>"
```

Создание бронирования:

```bash
curl -X POST "http://127.0.0.1:8000/api/bookings/" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "room_id": 1,
    "timeslot_id": 1,
    "date": "2026-08-01"
  }'
```

## Роли и права

- `user`:
  - может просматривать комнаты и таймслоты;
  - может создавать и отменять только свои бронирования.
- `admin`:
  - имеет все права пользователя;
  - может управлять комнатами и таймслотами;
  - может отменять любые бронирования.

## Тестирование

Запуск всех тестов:

```bash
pytest -q
```

Для ускорения локальной проверки можно запускать отдельные группы тестов:

```bash
pytest -q tests/test_auth.py tests/test_user.py
pytest -q tests/test_rooms.py tests/test_timeslots.py tests/test_bookings.py
```

## Примечания по развитию

- приложение использует асинхронные SQLAlchemy-сессии;
- миграции базы данных находятся в каталоге `alembic/`;
- при старте приложения автоматически создаётся административный пользователь из `.env`.

