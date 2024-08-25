# FastAPI Investment App

## Описание

Это приложение для управления криптовалютными инвестициями, разработанное с использованием FastAPI. Оно позволяет пользователям регистрироваться, входить в систему и управлять списком выбранных криптовалют, а также получать информацию о текущих курсах выбранных криптовалют.

## Основные возможности

- Регистрация нового пользователя
- Авторизация с использованием JWT токена
- Добавление криптовалют в список пользователя
- Получение текущих курсов выбранных криптовалют

## Технологии

- **Python 3.8+**
- **FastAPI**: Фреймворк для создания веб-приложений на Python
- **SQLAlchemy**: ORM для работы с базой данных
- **SQLite**: База данных по умолчанию (можно заменить на любую другую)
- **Pydantic**: Валидация данных
- **JWT (JSON Web Tokens)**: Аутентификация и авторизация

## Установка и запуск

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/yourusername/fastapi-investment-app.git
   cd fastapi-investment-app
