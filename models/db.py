import os
import shutil
from pathlib import Path

from pyaml_env import parse_config
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel


_STORAGE_PATH = Path(__file__).parents[1] / ".storage"
_CONFIG_PATH = Path(__file__).parents[1] / "config.yaml"
_CONFIG = parse_config(str(_CONFIG_PATH))

ASYNC_DB_ENGINE = create_async_engine(
    _CONFIG['db']['url'],
    echo=_CONFIG['db']['echo_flag'],
    future=_CONFIG['db']['future_flag']
)


async def init_storage() -> None:
    """
    Database initialization, deletion of old data (if required).

    :return: None
    """
    async with ASYNC_DB_ENGINE.begin() as connection:
        if _CONFIG['db']['drop_all_flag']:
            await connection.run_sync(SQLModel.metadata.drop_all)
            shutil.rmtree(_STORAGE_PATH, ignore_errors=True)

        await connection.run_sync(SQLModel.metadata.create_all)
        os.makedirs(_STORAGE_PATH, exist_ok=True)
