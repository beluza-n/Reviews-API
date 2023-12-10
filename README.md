# api_yamdb
api_yamdb
Authors:
* gatart (Teamlead, Auth/Users)
* beluza-n (Categories/Genres/Titles)
* Vladimir-V-K (Review/Comments)

## Описание
Групповой проект ао заданию Яндекс Практикума.    
Проект YaMDb собирает отзывы пользователей на различные произведения.

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/gatart/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Обновить пакетный менеджер pip:

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

## Примеры API запросов

### Получить код подтверждения / Зарегистрироваться
Необходимо отправить POST запрос по пути `/api/v1/auth/signup/`.   
Код подтверждения придёт на почту.  
Запрос к серверу:
```json
{
"email": "user@example.com",
"username": "string"
}
```

Ответ сервера:
```json
{
"email": "string",
"username": "string"
}
```
### Получить токен
Необходимо отправить GET запрос по пути `/api/v1/auth/token/`.  
Запрос к серверу:
```json
{
"username": "string",
"confirmation_code": "string"
}
```
Ответ сервера:
```json
{
"token": "string"
}
```
### Другие запросы
Ознакомиться с другими запросами можно в документации к API по пути
`/redoc/`
