# 🛡️ Авторизация в проекте

## Описание

Система авторизации реализована через FastAPI с использованием токенов JWT.  
Пользователь проходит аутентификацию по логину и паролю, после чего получает токен доступа для дальнейшей работы с защищёнными маршрутами.

---

## 📩 Процесс авторизации

### 1. Регистрация пользователя

**Метод:** `POST`  
**URL:** `/auth/register`

**Тело запроса (JSON):**

```json
{
  "username": "user1",
  "email": "user1@example.com",
  "password": "securepassword123"
}
```
### 2. Вход пользователя
**Метод:** `POST`  
**URL:** `/auth/login`

**Тело запроса (JSON):**
```json
{
  "username": "user1",
  "password": "securepassword123"
}
```


Ответ (JSON):
```json
{
  "access_token": "<token>",
  "token_type": "bearer"
}

```
![Описание изображения](images/1.png)
### 3. Получение информации о текущем пользователе

**Метод:** `GET`  
**URL:** `/auth/me`

**Тело запроса (JSON):**
```json
{
  "Authorization": "Bearer <token>"
}
```

Ответ (JSON):
```json
{
  "id": 1,
  "username": "user1",
  "email": "user1@example.com",
  "balance": 0.0
}
```

### 4. Получение списка всех пользователей


**Метод:** `GET`  
**URL:** `/auth/`

```json
{
  "Authorization": "Bearer <token>"
}
```
Ответ (JSON):
```json
[
  {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com",
    "balance": 0.0
  },
  {
    "id": 2,
    "username": "user2",
    "email": "user2@example.com",
    "balance": 0.0
  }
]

```

### 5. Смена пароля

**Метод:** `POST`  
**URL:** `/auth/change_password`

```json
{
  "old_password": "oldpass123",
  "new_password": "newpass456"
}

```
Ответ (JSON):
```json
{
  "message": "Пароль успешно изменен"
}
```


## 📊  CRUD

В данной секции описан процесс работы с CRUD-операциями для бюджета. Все операции взаимодействуют с моделями `Budget`, `Category`, и `User`.

---

### 1. Создание бюджета

**Метод:** `POST`  
**URL:** `/budget`  
**Тело запроса (JSON):**

```json
{
  "user_id": 1,
  "category_id": 2,
  "amount": 5000.0,
  "start_date": "2025-01-01",
  "end_date": "2025-12-31"
}
```

### 2. Получение списка бюджетов

**Метод:** `GET`  
**URL:** `/budget_list`  
**Тело запроса (JSON):**

```json
[
  {
    "id": 1,
    "amount": 5000.0,
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "user": {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com"
    },
    "category": {
      "id": 2,
      "name": "Food",
      "type": "Expense"
    }
  }]
```

### 3. Получение бюджета по ID

**Метод:** `GET`  
**URL:** `/budget/{budget_id}`
**Тело запроса (JSON):**
```json
{
  "id": 1,
  "amount": 5000.0,
  "start_date": "2025-01-01",
  "end_date": "2025-12-31",
  "user": {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com"
  },
  "category": {
    "id": 2,
    "name": "Food",
    "type": "Expense"
  }
}
```

### 4. Обновление бюджета

**Метод:** PUT  
**URL:** `/budget/{budget_id}`
**Тело запроса (JSON):**
``` json
{
  "amount": 5500.0,
  "start_date": "2025-02-01",
  "end_date": "2025-12-31"
}
```

### 5. Удаление бюджета

**Метод:** DELETE  
**URL:** `/budget/{budget_id}`
**ТПараметры URL:**

budget_id: ID бюджета, который нужно удалить.

ОТВЕТ
``` json
{
  "status": "OK"
}
```