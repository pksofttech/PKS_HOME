import json
import logging
import random
from typing import AsyncIterator
from typing import AsyncGenerator
from .utility import get_password_hash
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import aliased

from ..stdio import *
import urllib
import logging
import logging.handlers

from fastapi import Depends
from sqlmodel import SQLModel, delete, func, insert, text, update
from .models import *

# from app.core import models

from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.core import config


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///sqlacm.db"
# ? connect_args={"check_same_thread": False} For Sqlite เท่านั้น
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

data_base_ip = "localhost"
data_base_name = "dpark_vms"
data_base_password = "dls@1234"

print("Connect DataBase")
_password = urllib.parse.quote_plus(data_base_password)
# SQLALCHEMY_DATABASE_URL = f"mssql+pymssql://sa:{_password}@{data_base_ip}/{data_base_name}?charset=utf8"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=0)

# For postgres DB
postgres_server = "localhost"
postgres_database = "database"
_password = urllib.parse.quote_plus("#bunpotnumnak24")
# SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://root:{_password}@{postgres_server}/{postgres_database}"
# async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

# ? MAIN LIB+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

_async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with _async_session_maker() as session:
        yield session


async def set_databases(init=None):
    print_success("********************************************************")
    print_success(f"Init_db config Time {time_now()}")

    if init:
        print_warning("Clear database for initialization")
        async with async_engine.begin() as conn:
            pass

            await conn.run_sync(SQLModel.metadata.drop_all)

            await conn.run_sync(SQLModel.metadata.create_all)

        async with _async_session_maker() as db:
            for l in ["USER_02", "USER_01", "OPERATOR", "ADMIN", "ROOT"]:
                _system_user_type = System_User_Type(user_type=l)
                if l == "ROOT":
                    _system_user_type.permission_allowed = "system_config,management_system_user,station_config"
                db.add(_system_user_type)
            await db.commit()

            sql = select(System_User_Type.id).where(System_User_Type.user_type == "ROOT")
            _system_user_type_root: System_User_Type = (await db.execute(sql)).one_or_none()
            # print(_system_user_type_root.id)
            print_warning("DataBase is missing root user")
            print_warning("SystemUser root not found init_db() create new root")
            _password = get_password_hash("12341234")
            _root = System_User(
                name="root",
                username="root",
                password=_password,
                system_user_type_id=_system_user_type_root.id,
                create_by="init_db",
                status="Enable",
                pictureUrl="/static/data_base/image/default/system.png",
            )
            db.add(_root)
            await db.commit()

    print_success("********************* Success Set Data For Test ************************")


async def init_db():
    if INIT_DATABASE:
        await set_databases(True)
    async with _async_session_maker() as db:
        pass
