from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Type

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel


def singleton(cls: Type[type]) -> Callable:
    """
    Singleton decorator.

    :param Type[type] cls:
    :return:
    :rtype:
    """
    instances = dict()

    def wrapper(*args, **kwargs):
        if cls not in instances.keys():
            instances[cls] = cls(args, kwargs)

        return instances[cls]

    return wrapper


@singleton
@dataclass
class AppParams:
    """
    Dataclass with application configuration parameters.
    """
    _storage_path: Path = NotImplemented

    db_async_url: str = NotImplemented
    db_echo: bool = True
    db_future: bool = True
    db_drop_all: bool = False
    db_engine: AsyncEngine = NotImplemented

    host: str = "127.0.0.1"
    port: int = 8_000
    reload: bool = False
    workers_num: int = 1

    _log_config_path: str = NotImplemented

    @property
    def storage_path(self) -> Path:
        """
        Getter of `storage_path`-field.

        :return: Value of `storage_path`-field.
        :rtype: str
        """
        return self._storage_path

    @storage_path.setter
    def storage_path(self, new_path: str | Path) -> None:
        """
        Setter of `storage_path`-field.

        :param Union[str, Path] new_path: New value of `storage_path`-field.
        :return: None
        """
        self._storage_path = Path(new_path)

    @property
    def log_config_path(self) -> str:
        """
        Getter of `log_config_path`-field.

        :return: Value of `log_config_path`-field.
        :rtype: str
        """
        return self._log_config_path

    @log_config_path.setter
    def log_config_path(self, new_path: str | Path) -> None:
        """
        Setter of `log_config_path`-field.

        :param Union[str, Path] new_path: New value of `log_config_path`-field.
        :return: None
        """
        self._log_config_path = str(new_path)

    def create_orm_engine(self) -> None:
        """
        Create ORM engine.

        :return: None
        """
        self.db_engine = create_async_engine(
            self.db_async_url,
            echo=self.db_echo,
            future=self.db_future
        )

    async def init_database(self) -> None:
        """
        Database initialization, deletion of old data (if required).

        :return: None
        """
        async with self.db_engine.begin() as connection:
            if self.db_drop_all:
                await connection.run_sync(SQLModel.metadata.drop_all)

            await connection.run_sync(SQLModel.metadata.create_all)

    def init_storage(self) -> None:
        """
        Database initialization, deletion of old data (if required).

        :return: None
        """
        if self.db_drop_all:
            shutil.rmtree(self.storage_path, ignore_errors=True)

        os.makedirs(self.storage_path, exist_ok=True)


APP_PARAMS = AppParams()
