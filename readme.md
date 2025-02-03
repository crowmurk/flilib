# Flibusta local server

Каталогизатор архивов библиотеки Flibusta

- [Run test server](#run-test-server)

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
pip install -r ./requirements.txt
```

Создаем папки для хранения логов и БД:

```bash
mkdir flilog
mkdir flidb
```

Создаем БД:

```bash
./flilib/manage.py migrate
```

В файле `flilib/flilib/settings/base.py` изменяем пути к архиву библиотеки и файлу inpx на свои:

```python
LIBRARY_DIR = '/path/to/library'
INPX_FILE = '/path/to/inpx/file'
```

Проверяем inpx файл:

```bash
./flilib/manage.py dbupdate --verify-data
```

Обновляем  БД:

```bash
./flilib/manage.py dbupdate --update-db
```

При возникновении ошибок, можно для очистки БД выполнить:

```bash
./flilib/manage.py dbclear
```

Деактивируем виртуальное окружение Python:

```bash
deactivate
```

Запускаем сервер (прервать работу сервера: `Ctrl-C`):

```bash
./start.sh
```

Заходим в браузере: [localhost:8000](http://localhost:8000)

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
pip install -r ./requirements.txt
```

Create log and database destination folders:

```bash
mkdir flilog
mkdir flidb
```

Create project database:

```bash
./flilib/manage.py migrate
```

Change paths to the library archives and inpx file in `flilib/flilib/settings/base.py`:

```python
LIBRARY_DIR = '/path/to/library'
INPX_FILE = '/path/to/file.inpx'
```

Verify inpx file:

```bash
./flilib/manage.py dbupdate --verify-data
```

Update project database:

```bash
./flilib/manage.py dbupdate --update-db
```

If any errors ocurred, you may clear the database:

```bash
./flilib/manage.py dbclear
```

Deacivate the Python virtual environment:

```bash
deactivate
```

Run test server (to stop the server press `Ctrl-C`):

```bash
./start.sh
```

Open in browser: [localhost:8000](http://localhost:8000)
