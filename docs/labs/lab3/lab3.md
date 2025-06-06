## Лабораторная работа: Интеграция парсера данных с FastAPI и использование очередей Celery в Docker

## Цель

Научиться упаковывать FastAPI приложения в Docker, создавать связь между основным приложением и сервисом парсинга данных, а также реализовать асинхронное выполнение задач с использо


ванием очередей Celery и Redis.

## Архитектура проекта
Проект состоит из следующих компонентов:

Основное FastAPI приложение (hackathon)

Сервис парсера (parser)

База данных PostgreSQL

Redis для хранения очередей задач

Celery для обработки асинхронных задач


## Подзадача 1: Упаковка сервисов в Docker

### Hackathon
```python
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Parser
```python4
FROM python:3.9

WORKDIR /parser

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
```

## Docker Compose для оркестрации сервисов
```python4
version: "3.8"

services:
  db:
    image: postgres:14
    container_name: hackathon_postgres
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: hackathon_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    container_name: redis
    restart: always
    ports:
      - "6379:6379"

  hackathon:
    build:
      context: ./hackathon
      dockerfile: Dockerfile
    container_name: hackathon_app
    depends_on:
      - db
      - redis
    env_file:
      - ./hackathon/.env
    ports:
      - "8000:8000"
    volumes:
      - ./hackathon:/app
    command: ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

  parser:
    build:
      context: ./parser
      dockerfile: Dockerfile
    container_name: parser_app
    depends_on:
      - db
    env_file:
      - ./parser/task2/.env
    ports:
      - "9000:9000"
    volumes:
      - ./parser:/parser
    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]

  celery_worker:
    build:
      context: ./hackathon
      dockerfile: Dockerfile
    container_name: celery_worker
    depends_on:
      - redis
      - hackathon
    command: ["celery", "-A", "celery_worker", "worker", "--loglevel=info"]
    volumes:
      - ./hackathon:/app
    environment:
      - CELERY_BROKER=redis://redis:6379/0
      - CELERY_BACKEND=redis://redis:6379/0

volumes:
  postgres_data:
```

## Подзадача 2: Реализация API парсера

```python4
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from celery_worker import parse_url_tasks, celery_app

router = APIRouter()

class URLRequest(BaseModel):
    url: str

@router.post("/parse-url")
def parse_by_url(request: URLRequest):
    try:
        task = parse_url_tasks.delay(request.url)
        return {"task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/task-status/{task_id}")
def get_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.ready():
        return {"status": "completed", "result": task_result.result}
    return {"status": "pending"}
```


Парсим данные по URL
Она подается в очередь
![Снимок экрана 2025-05-25 в 17.10.26.png](..%2F..%2F..%2F..%2F..%2F..%2Fvar%2Ffolders%2Fr5%2F69n9xh3s6wngqm8s3z5qmwlh0000gn%2FT%2FTemporaryItems%2FNSIRD_screencaptureui_ztK9E7%2F%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-05-25%20%D0%B2%2017.10.26.png)


После по task_id получем ответ
![Снимок экрана 2025-05-25 в 17.11.28.png](..%2F..%2F..%2F..%2F..%2F..%2Fvar%2Ffolders%2Fr5%2F69n9xh3s6wngqm8s3z5qmwlh0000gn%2FT%2FTemporaryItems%2FNSIRD_screencaptureui_G40KXW%2F%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-05-25%20%D0%B2%2017.11.28.png)