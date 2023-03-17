import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .app_params import APP_PARAMS
from .storage import STORAGE_ROUTER


FSTORAGE_APP = FastAPI(title="FStorage service")
FSTORAGE_APP.include_router(STORAGE_ROUTER)
FSTORAGE_APP.add_middleware(
    CORSMiddleware,
    allow_origins=("*", ),
    allow_credentials=True,
    allow_methods=("*", ),
    allow_headers=("*", ),
    expose_headers=("*", )
)


@FSTORAGE_APP.on_event("startup")
async def on_startup() -> None:
    """
    A function that runs after the Application is started.

    :return: None
    """
    APP_PARAMS.create_orm_engine()
    await APP_PARAMS.init_database()
    APP_PARAMS.init_storage()


def storage_run(**kwargs) -> None:
    """
    Run FStorage-server using user-params.

    :return: None
    """
    for param_name, param_value in kwargs.items():
        setattr(APP_PARAMS, param_name, param_value)

    uvicorn.run(
        'fstorage.server.app:FSTORAGE_APP',
        host=APP_PARAMS.host,
        port=APP_PARAMS.port,
        log_config=APP_PARAMS.log_config_path,
        reload=APP_PARAMS.reload,
        workers=APP_PARAMS.workers_num
    )
