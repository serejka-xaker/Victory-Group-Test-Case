# Victory-Group-Test-Case

API сервиса для сокращения ссылок со статистикой.

## Технологический стек
- **Python 3.12**
- **FastAPI** 
- **PostgreSQL** + **SQLAlchemy 2.0**
- **Docker Compose**
- **Pytest**

## Запуск

### 1. Подготовка
Клонируйте репозиторий и создайте файл `.env`:
```bash
git clone https://github.com/serejka-xaker/Victory-Group-Test-Case.git 
cd Victory-Group-Test-Case
cp .env.example .env
```
### 2. Запуск через Docker
```bash
POSTGRES_USER=Имя_пользователя_базы_данных
POSTGRES_PASSWORD=Пароль_пользователя_базы_данных
POSTGRES_DB=Название_базы_данных
DB_ECHO=True или False для отображения в логах операций с базой данных в реальном времени
```
Все данные без кавычек
### 3. Запуск через Docker
```bash
docker compose up -d --build
```
После этого API будет доступно по адресу: http://localhost:8000
Swagger документация будет доступна по адресу: http://localhost:8000/docs

### 4. Запуск тестов
```bash
docker compose run --rm app pytest tests/test_api.py
```

## Проверка работоспособности

### Windows
### 1. Создание короткой ссылки
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/shorten" -Method Post -ContentType "application/json" -Body '{"full_url": "https://www.google.com/"}'
```
### 2. Переход по ссылке
```Browser
Необходимо в браузере открыть ссылку http://localhost:8000/{ID который выдал API}
```
И сразу произойдет редирект на длинную ссылку
### 3. Проверка статистики переходов
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/stats/{ID который выдал API}" -Method Get
```

### Linux
### 1. Создание короткой ссылки
```bash
curl -X POST "http://localhost:8000/shorten" \
     -H "Content-Type: application/json" \
     -d '{"full_url": "https://www.google.com/"}'
```
### 2. Переход по ссылке
```Browser
Необходимо в браузере открыть ссылку http://localhost:8000/{ID который выдал API}
```
И сразу произойдет редирект на длинную ссылку
### 3. Проверка статистики переходов
```powershell
curl -X GET "http://localhost:8000/stats/{ID который выдал API}" 
```
### Пример проверки работоспособности

<img width="1460" height="535" alt="image" src="https://github.com/user-attachments/assets/1d9adfe0-6e76-4815-b4f2-ff291e77d6bc" />


