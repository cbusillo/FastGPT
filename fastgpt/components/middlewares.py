from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def setup_middlewares(app: FastAPI) -> None:
    # noinspection PyTypeChecker
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )
