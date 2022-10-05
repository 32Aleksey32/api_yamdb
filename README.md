
# api_yamdb - спринт №4 в Яндекс.Практикум
## Спринт 10 - Проект YaMDb

### Описание

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

### Как запустить проект:

Склонируйте репозиторий и перейдите в него в командной строке:

```
git clone https://github.com/32Aleksey32/api_yamdb
```

```
cd api_yamdb
```

Cоздайте и активируйте виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установите зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполните миграции:

```
python3 manage.py migrate
```

Запустите проект:

```
python3 manage.py runserver
```
### Перечень доступных эндпойнтов:

-   `api/v1/auth/signup/`  (POST): Получить код подтверждения на переданный email (доступно всем).
-   `api/v1/auth/token/` (POST): Получить JWT-токен в обмен на username и confirmation code (доступно всем).

-   `api/v1/categories/`  (GET, POST): Получить список всех категорий (доступно всем); Создать категорию (доступно только администратору).
-   `api/v1/categories/{slug}`  (DELETE): Удалить категорию (доступно только администратору).

-   `api/v1/genres/`  (GET, POST): Получить список всех жанров (доступно всем); Создать жанр (доступно только администратору).
-   `api/v1/genres/{slug}`  (DELETE): Удалить жанр (доступно только администратору).

-   `api/v1/titles/`  (GET, POST): Получить список всех произведений и связанных объектов (доступно всем); Добавить новое произведение (доступно только администратору).
-   `api/v1/titles/{title_id}`  (GET, PATCH, DELETE): Информация о произведении (доступно всем); Обновить информацию о произведении / удалить произведение (доступно только администратору).

-   `api/v1/titles/{title_id}/reviews/`  (GET, POST): Получить список всех отзывов (доступно всем); Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение (доступно только аутентифицированным пользователям).
-   `api/v1/titles/{title_id}/reviews/{review_id}`  (GET, PATCH, DELETE): Получить отзыв по id для указанного произведения (доступно всем); Частично обновить отзыв по id / удалить отзыв (доступно автору отзыва, модератору или администратору).

-   `api/v1/titles/{title_id}/reviews/{review_id}/comments/`  (GET, POST): Получить список всех комментариев к отзыву по id (доступно всем); Добавить новый комментарий к отзыву (доступно только аутентифицированным пользователям).
-   `api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}`  (GET, PATCH, DELETE): Получить комментарий к отзыву по id (доступно всем); Частично обновить / удалить комментарий к отзыву по id (доступно автору комментария, модератору или администратору).

-   `api/v1/users/`  (GET, POST): Получить список всех пользователей; Добавить пользователя (доступно только администратору).
-   `api/v1/users/{username}`  (GET, PATCH, DELETE): Получить пользователя по username; Изменить данные пользователя; Удалить пользователя (доступно только администратору).
-   `api/v1/users/me`  (GET, PATCH): Получить / Изменить данные своей учетной записи (доступно авторизованному пользователю).

### Пример запроса-ответа API:

Запрос:
```
GET /api/v1/titles/
```
Пример ответа:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
### Авторы:
* [32Aleksey32](https://github.com/32Aleksey32)
* [LatentBlondinkO](https://github.com/LatentBlondinkO)
* [vnovoselov](https://github.com/vnovoselov)
