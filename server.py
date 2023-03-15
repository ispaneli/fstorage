import os

from src.fstorage.server import storage_run


if __name__ == '__main__':
    storage_run(
        storage_path="~/.fstorage/storage/",

        db_async_url=os.getenv('POSTGRESQL_URL'),
        db_echo=True,
        db_future=True,
        db_drop_all=False,

        host="127.0.0.1",
        port=8_000,
        reload=False,
        workers_num=1
    )
