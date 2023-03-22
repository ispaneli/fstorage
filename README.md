<p align="center">
  <a href="https://pypi.org/project/fstorage">
    <img src="https://raw.githubusercontent.com/ispaneli/fstorage/master/docs/img/logo.png" alt="FStorage">
  </a>
</p>
<p align="center">
  <em>Fstorage, Secure file storage, SYNC/ASYNC clients, easy to learn, fast to code.</em>
</p>
<p align="center">
  <a href="https://pypi.org/project/fstorage" target="_blank">
    <img src="https://img.shields.io/pypi/v/fstorage?color=%2334D058&label=pypi%20package" alt="Package version">
  </a>
  <a href="https://pypi.org/project/fstorage" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fstorage.svg?color=%2334D058" alt="Supported Python versions">
  </a>
  <a href="https://pypi.org/project/fstorage" target="_blank">
    <img src="https://static.pepy.tech/personalized-badge/fstorage?period=total&units=none&left_color=grey&right_color=brightgreen&left_text=Downloads" alt="Total downloads">
  </a>
</p>

---

**Source Code**:
<a href="https://github.com/ispaneli/fstorage" target="_blank">
  https://github.com/ispaneli/fstorage
</a>

---

**FStorage** is a simple asynchronous secure file storage for microservices.

It is implemented on the **<a href="https://pypi.org/project/fastapi/" class="external-link" target="_blank">FastAPI</a>** web framework.

To run the file storage, you need:
* **<a href="https://www.postgresql.org/" class="external-link" target="_blank">PostgreSQL</a>**

**WARNING**: With the usual installation of `pip install fstorage`, the requirements are not installed (for more info, see [How to install](#how-to-install-with-requirements))!

---

## How to install with requirements

To deploy the FStorage on the **server**:

```bash
pip install 'fstorage[server]'
```

To use **synchronous client**:

```bash
pip install 'fstorage[sync_client]'
```

To use **asynchronous client**:

```bash
pip install 'fstorage[async_client]'
```

---

## How to deploy storage

Configure virtual environment variables in terminal:

```bash
export POSTGRESQL_URL="postgresql+asyncpg://<db_username>:<db_password>@<db_host>:<db_port>/<db_name>"
export STORAGE_PATH="/Users/<local_username>/.fstorage/storage"
```

Configure **logging.ini**:

```ini
[loggers]
keys=root

[handlers]
keys=logfile, logconsole

[formatters]
keys=logformatter

[logger_root]
level=INFO
handlers=logfile, logconsole

[formatter_logformatter]
format=[%(asctime)s.%(msecs)03d] %(levelname)s [%(thread)d] - %(message)s

[handler_logfile]
class=handlers.RotatingFileHandler
level=INFO
args=('/Users/<local_username>/.fstorage/logfile.log', 'a')
formatter=logformatter

[handler_logconsole]
class=handlers.logging.StreamHandler
level=INFO
args=()
formatter=logformatter
```

Run this code:

```python
import os

from fstorage.server import storage_run


if __name__ == '__main__':
    storage_run(
        storage_path=os.getenv('STORAGE_PATH'),
        log_config_path="logging.ini",
        
        db_async_url=os.getenv('POSTGRESQL_URL'),
        db_echo=True,
        db_future=True,
        db_drop_all=False,

        host='127.0.0.1',
        port=8_000,
        reload=False,
        workers_num=1
    )
```

---

## How to use synchronous client

```python
from fstorage.client.synch.client import SyncClient


if __name__ == '__main__':
    client = SyncClient("http://127.0.0.1:8000")

    upload_response: dict = client.upload(open("example.file", 'rb'))
    print(upload_response)
    # {'id': "<file_id>"}

    get_response: dict = client.get(upload_response['id'])
    print(get_response)
    # {'filename': "example.file", 'bytes': '<data_as_bytes>'}

    client.delete(upload_response['id'])

    try:
        client.get(upload_response['id'])
    except FileExistsError as error:
        print(error)
        # "The file with this ID doesn't exist."

    try:
        client.delete(upload_response['id'])
    except FileExistsError as error:
        print(error)
        # "The file with this ID doesn't exist."
```

---

## How to use asynchronous client

```python
import asyncio

from fstorage.client.asynch.client import AsyncClient


async def example():
    client = AsyncClient("http://127.0.0.1:8000")

    upload_response: dict = await client.upload(open("example.file", 'rb'))
    print(upload_response)
    # {'id': "<file_id>"}

    get_response: dict = await client.get(upload_response['id'])
    print(get_response)
    # {'filename': "example.file", 'bytes': '<data_as_bytes>'}

    await client.delete(upload_response['id'])

    try:
        await client.get(upload_response['id'])
    except FileExistsError as error:
        print(error)
        # "The file with this ID doesn't exist."

    try:
        await client.delete(upload_response['id'])
    except FileExistsError as error:
        print(error)
        # "The file with this ID doesn't exist."


if __name__ == '__main__':
    asyncio.run(example())
```

---

## License

This project is licensed under the terms of the [MIT license](https://github.com/ispaneli/fstorage/blob/master/LICENSE).