

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone <URL вашего репозитория>
    cd <имя_директории>
    ```

2. Установите необходимые зависимости:

    ```bash
    pip install -r requirements.txt
    ```

## Запуск

Чтобы запустить приложение, выполните следующую команду из каталога проекта:

```bash
uvicorn src.main:app --reload
