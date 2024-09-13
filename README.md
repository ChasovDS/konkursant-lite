## Установка

### 1. Клонирование репозитория

Сначала клонируйте репозиторий:

```bash
git clone https://github.com/ChasovDS/konkursant-lite.git
cd konkursant-lite
```

### 2. Создание виртуального окружения

Создайте и активируйте виртуальное окружение:

**Для Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Для macOS и Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка необходимых зависимостей

Установите необходимые зависимости, выполнив следующую команду:

```bash
pip install -r requirements.txt
```

## Запуск

Чтобы запустить приложение, выполните следующую команду из каталога проекта:

```bash
uvicorn src.main:app --reload
```

После этого вы сможете получить доступ к приложению по адресу [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) для просмотра документации API.

