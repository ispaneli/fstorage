from pathlib import Path

import uvicorn
from fastapi import FastAPI
from pyaml_env import parse_config

from models.db import init_storage
from services.storage import STORAGE_ROUTER


STORAGE_APP = FastAPI(title="File Storage Microservice")
STORAGE_APP.include_router(STORAGE_ROUTER)

STORAGE_PATH = Path(__file__).parent / "storage"
CONFIG_PATH = Path(__file__).parent / "config.yaml"


@STORAGE_APP.on_event("startup")
async def on_startup() -> None:
    """
    A function that runs after the Application is started.

    :return: None
    """
    await init_storage()


if __name__ == '__main__':
    CONFIG = parse_config(str(CONFIG_PATH))

    uvicorn.run(
        'main:STORAGE_APP',
        host=CONFIG['web_app']['host'],
        port=int(CONFIG['web_app']['port']),
        log_config=CONFIG['web_app']['config_log_path'],
        reload=CONFIG['web_app']['reload_flag'],
        workers=CONFIG['web_app']['workers_num']
    )

