# Flibusta local server

- [Запуск тестового сервера](#запуск-тестового-сервера)

## Run test server

Create Python virtual environment:

```bash
python -m venv test
cd test
```

Activate the virtual environment:

```bash
source bin/activate
```

Clone the repository:

```bash
git clone https://github.com/crowmurk/flilib
cd flilib
```

Upgrade `pip`:

```bash
pip install --upgrade pip
```

Install dependencies:  to install python `pygraphviz` package [graphviz](https://www.archlinux.org/packages/extra/x86_64/graphviz/) may be required (more about at [graphviz.org](http://www.graphviz.org/)). Normally `pygraphviz` package is not required (see below). If there are any problems, then the package can be removed from `requrements.txt`

Install requirements:

```bash
pip install -r requirements.txt
```

Create project database:

```bash
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

Execute for graphical representation of database models (this is the reason we use `graphviz`)

```bash
./manage.py graph_models inpx library --pygraphviz -g -o db_visualized.png
```

Deacivate the Python virtual environment:

```bash
deactivate
```

## Запуск тестового сервера

Создаем виртуальное окружение Python:

```bash
python -m venv test
cd test
```

Активируем виртуальное окружение:

```bash
source bin/activate
```

Клонируем репозиторий:

```bash
git clone https://github.com/crowmurk/flilib
cd flilib
```

Обновляем `pip`:

```bash
pip install --upgrade pip
```

Устанавливаем зависимости: Для установки модуля `pygraphviz` может потребоваться [graphviz](https://www.archlinux.org/packages/extra/x86_64/graphviz/) (подробней на [graphviz.org](http://www.graphviz.org/)). Для нормальной работы он не нужен (см. ниже), если возникнут проблемы, его можно удалить из `requrements.txt`

```bash
pip install -r requirements.txt
```

Создаем БД:

```bash
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

Для графического представления моделей БД (для чего и нужен `graphviz`) выполнить:

```bash
./manage.py graph_models inpx library --pygraphviz -g -o db_visualized.png
```

Деактивируем виртуальное окружение Python:

```bash
deactivate
```
