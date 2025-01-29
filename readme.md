# Flibusta local server

- [Запуск тестового сервера](#запуск-тестового-сервера)

## Run test server

Create Python virtual environment:

```bash
python -m venv flivenv
```

Activate the virtual environment:

```bash
source ./flivenv/bin/activate
```

Clone the repository:

```bash
git clone https://github.com/crowmurk/flilib
```

Upgrade `pip`:

```bash
pip install --upgrade pip
```

Install requirements:

```bash
pip install -r requirements.txt
```

Create project database:

```bash
mkdir flidb

cd flilib
./manage.py migrate
```

Change paths to the library archives and inpx file in `flilib/settings/base.py`:

```python
LIBRARY_DIR = '/path/to/library'
INPX_FILE = '/path/to/file.inpx'
```

Verify inpx file:

```bash
./manage.py dbupdate --verify-data
```

Update project database:

```bash
./manage.py dbupdate --update-db
```

If any errors ocurred, you may clear the database:

```bash
./manage.py dbclear
```

Run test server (to stop the server press `Ctrl-C`):

```bash
./manage.py runserver
```

Open in browser: [localhost:8000](http://localhost:8000)

Deacivate the Python virtual environment:

```bash
deactivate
```

## Запуск тестового сервера

Создаем виртуальное окружение Python:

```bash
python -m venv flivenv
```

Активируем виртуальное окружение:

```bash
source ./flivenv/bin/activate
```

Клонируем репозиторий:

```bash
git clone https://github.com/crowmurk/flilib
```

Обновляем `pip`:

```bash
pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

Создаем БД:

```bash
mkdir flidb

cd flilib
./manage.py migrate
```

В файле `flilib/settings/base.py` изменяем пути к архиву библиотеки и файлу inpx на свои:

```python
LIBRARY_DIR = '/path/to/library'
INPX_FILE = '/path/to/inpx/file'
```

Проверяем inpx файл:

```bash
./manage.py dbupdate --verify-data
```

Обновляем  БД:

```bash
./manage.py dbupdate --update-db
```

При возникновении ошибок, можно для очистки БД выполнить:

```bash
./manage.py dbclear
```

Запускаем тестовый сервер django (прервать работу сервера: `Ctrl-C`):

```bash
./manage.py runserver
```

Заходим в браузере: [localhost:8000](http://localhost:8000)

Деактивируем виртуальное окружение Python:

```bash
deactivate
```
