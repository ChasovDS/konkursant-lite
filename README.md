

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/ChasovDS/konkursant-lite.git
    cd konkursant-lite
    ```

2. Установите необходимые зависимости:

    ```bash
    pip install -r requirements.txt
    ```

## Запуск

Чтобы запустить приложение, выполните следующую команду из каталога проекта:

```bash
uvicorn src.main:app --reload
