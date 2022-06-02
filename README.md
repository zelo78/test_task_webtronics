# Тестовое задание *Social network* (simple REST API)

Решение тестового задания компании [Webtronics](https://webtronics.ru/) с использованием **Django**, **Django REST framework**, **PostgreSQL**, **Docker**, **Docker-compose**.

Само задание приведено ниже.

## Установка

1. Клонировать проект в пустую папку:
```shell
git clone https://github.com/zelo78/test_task_webtronics.git .
```

2. Копировать файл `start.env` как `.env` (Он должен находится в корне проекта, рядом с `README.md`)
```shell
cp start.env .env
```

3. Создать и запустить контейнер (при запуске контейнера будут созданы и применены миграции):
```shell
docker-compose up -d --build
```

4. Создать суперпользователя:
```shell
docker exec -it zapp python manage.py createsuperuser --username USER
```

5. В целях тестирования, базу данных можно наполнить данными (пользователи и их посты)
```shell
docker exec -it zapp python manage.py populatebase
```

6. Остановить контейнер
```shell
docker-compose down
```

## Запуск
```shell
docker-compose up
``` 

## Реализованные интерфейсы

### Командная строка

- [x] `python manage.py manage.py populatebase <count: int>`

  - Наполнение базы данных случайными Пользователями и Сообщениями в целях тестирования, общее число Сообщений будет не меньше `count`
  - У Сообщений будет случайный текст, случайная дата создания, несколько лайков и дизлайков

### Реализованные API

- [x] `POST /api/post/create/`
  - создание Сообщения
  - доступно только авторизованному Пользователю (он становится автором Сообщения)
  
- [x] `GET /api/post/`
  - получение списка Сообщений (с пагинацией)
  - доступно для всех
  - возможна фильтрация по Пользователю (автору Сообщения)

- [x] `GET /api/post/<id: int>/`
  - получение конкретного Сообщения
  - доступно для всех
  - администраторы и автор Сообщения видят не просто количество лайков и дизлайков, но и список поставивших отметки like и unlike

- [x] `PATCH /api/post/<id: int>/`
  - частичное обновление Сообщения
  - доступно только его автору и администраторам

- [x] `DELETE /api/post/<id: int>/`
  - удаление Сообщения
  - доступно только его автору и администраторам

- [x] `PATCH /api/post/<id: int>/like/`
  - пометить Сообщение как "понравившееся" (like)
  - доступно только авторизованному пользователю
  - автор метки сохраняется в БД и эта информация доступна автору Сообщения
  - метки "понравилось" и "не понравилось" являются взаимоисключающими, установка одной удаляет другую

- [x] `PATCH /api/post/<id: int>/unlike/`
  - пометить Сообщение как "непонравившееся" (unlike)
  - доступно только авторизованному пользователю
  - автор метки сохраняется в БД и эта информация доступна автору Сообщения
  - метки "понравилось" и "не понравилось" являются взаимоисключающими, установка одной удаляет другую

- [x] `POST /api/token/`
  - получение токена JWT авторизации

- [X] `POST /api/users/`
  - создание нового Пользователя

- [x] `GET /api/users/`
  - получение списка Пользователей
  - доступно только авторизованным пользователям

- [x] `GET /api/users/<id: int>/`
  - получение информации по конкретному пользователю
  - доступно только авторизованным пользователям

- [x] `PATCH /api/users/<id: int>/`
  - частичное обновление Пользователя
  - только для Администраторов или самого себя

- [x] `DELETE /api/users/<id: int>/`
  - удаление Пользователя
  - доступно только Администраторам

### Реализованные URL

- [x] <http://0.0.0.0:8000/admin/>
  - интерфейс администрирования

### Swagger/OpenAPI 2.0 specifications

- [x] <http://0.0.0.0:8000/swagger/> 
  - A swagger-ui view of your API specification 
- [x] <http://0.0.0.0:8000/swagger.json> 
  - A JSON view of your API specification 
- [x] <http://0.0.0.0:8000/swagger.yaml> 
  - A YAML view of your API specification
- [x] <http://0.0.0.0:8000/redoc/> 
  - A ReDoc view of your API specification 

### Авторизация

#### Авторизация с помощью *BasicAuthentication* 
```shell
curl \
  -X GET \
  -H "Content-Type: application/json" \
  -u USER:PASSWORD \
  http://0.0.0.0:8000/api/post/
```

#### Авторизация с помощью *JWT*

- создаём токен авторизации
```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "USER", "password": "PASSWORD"}' \
  http://0.0.0.0:8000/api/token/
```

- получаем ответ вида
> {"refresh":"ey...I0","access":"ey...lQ"}

- авторизуемся с помощью токена:
```shell
curl \
  -X GET \
  -H "Authorization: Bearer ey...lQ" \
  http://0.0.0.0:8000/api/post/
```

## Линтеры

Исходный код проверен линтерами `black` и `flake8`

## Примеры запросов 

В примерах запросов использована BasicAuthentication (ключ `-u USER:PASSWORD`).
Эти же запросы можно выполнить с использованием JWT авторизации (ключ `-H "Authorization: Bearer <token>"`)

1. Получение списка Сообщений
```shell
curl -X GET "http://127.0.0.1:8000/api/posts/"
```

Получаем список Сообщений

2. Получение списка Сообщений, с фильтрацией
```shell
curl -X GET "http://127.0.0.1:8000/api/posts/?author=1"
```

Получаем список Сообщений указанного Пользователя

3. Создание Сообщения
```shell
curl -X POST  \
  -H  "Content-Type: application/json" \
  -d '{"title": "Заголовок", "text": "Сообщение"}' \
  -u USER:PASSWORD \
 "http://127.0.0.1:8000/api/posts/"
```

Получаем созданное Сообщение

4. Получение конкретного Сообщения
```shell
curl -X GET "http://127.0.0.1:8000/api/posts/10/"
```

Получаем данные о Сообщении

5. Получение данных о своём Сообщении 
```shell
curl -X GET \
  -u USER:PASSWORD \
  "http://127.0.0.1:8000/api/posts/10/"
```

Получаем данные о Сообщении, включая списки тех, кто поставил отметку like / unlike

6. Обновление Сообщения
```shell
curl -X PATCH \
  -H  "Content-Type: application/json" \
  -d '{"title": "Новый Заголовок"}' \
  -u USER:PASSWORD \
  "http://127.0.0.1:8000/api/posts/10/"
```

Получаем обновлённое Сообщение

7. Удаление Сообщения
```shell
curl -X DELETE \
  -u USER:PASSWORD \
  "http://127.0.0.1:8000/api/posts/10/"
```

8. Постановка отметки like (или unlike) на чужое Сообщение
```shell
curl -X PATCH \
  -u USER:PASSWORD \
  "http://127.0.0.1:8000/api/posts/20/like/"
```
```shell
curl -X PATCH \
  -u USER:PASSWORD \
  "http://127.0.0.1:8000/api/posts/20/unlike/"
```

Получаем стандартные данные об обновлённом Сообщении

9. Создание нового Пользователя
```shell
curl -X POST \
  -H  "Content-Type: application/json" \
  -d '{"username": "New_username", "password": "PASSWORD"}' \
  "http://127.0.0.1:8000/api/users/"
```

Получаем данные о новом пользователе (кроме пароля)

10. Получение списка Пользователей
```shell
curl -X GET \
  -u USER:PASSWORD \
  "http://127.0.0.1:8000/api/users/"
```

Получаем список Пользователей (требуется авторизация)

11. Получение данных о конкретном Пользователе
```shell
curl -X GET \
  -u USER:PASSWORD \
  "http://127.0.0.1:8000/api/users/10/"
```

Получаем данные о Пользователе (требуется авторизация)

12. Обновление данных о Пользователе
```shell
curl -X PATCH \
  -H  "Content-Type: application/json" \
  -d '{"first_name": "Новое имя"}' \
  -u USER:PASSWORD \
  "http://127.0.0.1:8000/api/users/53/"
```

Получаем обновлённые данные о Пользователе

13. Удаляем Пользователя
```shell
  curl -X DELETE \
  -u USER:PASSWORD \
  "http://127.0.0.1:8000/api/users/10/"
```

Требуется авторизация, только Администраторы имеют права

## Тестовое задание **Социальная сеть**

Тестовое задание компании [Webtronics](https://webtronics.ru/).

Целью этого задания является создания простого REST API. Вы должны использовать Django и Django REST framework.

### Базовые модели

- Пользователь
- Сообщение (всегда создаётся Пользователем)

### Базовые возможности

- регистрация Пользователя
- авторизация Пользователя
- создания Сообщения
- пометить Сообщение как "понравившееся" (like)
- пометить Сообщение как "непонравившееся" (unlike)

Для Пользователей и Постов кандидаты могут определять аттрибуты наиболее подходящим на их взгляд образом.

### Требования

- аутентификация по токену (JWT предпочтителен)
- использование Django с дополнительными модулями, базами данных и т.п.

### Опционально (что будет плюсом)

- использование <https://clearbit.com/platform/enrichment> для получения дополнительной информации о Пользователях
- использование <https://hunter.io/> для подтверждения существования адреса электронной почты при регистрации 

### Время на реализацию

1 рабочий день

### Дополнительные требования

Результат должен быть выложен на [GitHub](https://github.com/), с документацией по тому, как можно развернуть проект и протестировать его.

## Использованные библиотеки

- [Django](https://www.djangoproject.com/) v. 4.0.5
- [Django REST framework](https://www.django-rest-framework.org/) v. 3.13.1
- [django-filter](https://django-filter.readthedocs.io/en/stable/) v. 21.1 - allows users to filter down a queryset based on a model’s fields, displaying the form to let them do this
- [Psycopg](https://www.psycopg.org/docs/) v. 2.9.3 - PostgreSQL database adapter for Python
- [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/) v. 1.20.0 - Yet another Swagger generator. Generate real Swagger/OpenAPI 2.0 specifications from a Django Rest Framework API
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) v. 5.2.0 - Simple JWT provides a JSON Web Token authentication backend for the Django REST Framework
- [python-dotenv](https://pypi.org/project/python-dotenv/) v. 0.20.0 - Reads key-value pairs from a `.env` file and can set them as environment variables
- [black](https://black.readthedocs.io/en/stable/) v. 22.3.0 - The uncompromising code formatter
- [flake8](https://flake8.pycqa.org/en/latest/index.html) v. 4.0.1 - Your Tool For Style Guide Enforcement
- [factory_boy](https://factoryboy.readthedocs.io/en/stable/) v 3.2.1 - Fixtures replacement tool, it aims to replace static, hard to maintain fixtures with easy-to-use factories for complex objects.
