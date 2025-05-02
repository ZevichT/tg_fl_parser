import asyncio

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Model(DeclarativeBase):
    pass


class OffersORM(Model):
    __tablename__ = 'offers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    discreption: Mapped[str]
    price: Mapped[str]
    url: Mapped[str]


engine = create_async_engine(getenv('DB_URL')) # Вставить свой db_url
session_fabric = async_sessionmaker(engine, expire_on_commit=False)
new_session = session_fabric()
# Создание таблицы. Убрать комментарий
#
# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Model.metadata.create_all)
#
#
# asyncio.run(create_tables())
