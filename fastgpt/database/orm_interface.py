# database/orm_interface.py
from tortoise import Tortoise


async def start() -> None:
    await Tortoise.init(
        db_url="postgres://localhost/fastgpt",
        modules={"models": ["fastgpt.database.models"]},
    )
    await Tortoise.generate_schemas()


async def stop() -> None:
    await Tortoise.close_connections()
