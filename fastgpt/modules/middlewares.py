from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def setup_middlewares(app: FastAPI) -> None:
    # noinspection PyTypeChecker
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )