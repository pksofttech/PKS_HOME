from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional
from datetime import datetime, timedelta, timezone

from ..stdio import *

INIT_DATABASE = 1


class System_User_Type(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_type: str
    permission_allowed: str = Field(default="")
    system_users: List["System_User"] = Relationship(back_populates="system_user_type")


class System_User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    name: str = Field(unique=True)
    password: str
    createDate: datetime = Field(default=time_now(0), nullable=False)
    create_by: str
    # last_login_Date = Column(DateTime)
    status: str
    pictureUrl: str = Field(default="/static/image/logo.png")
    remark: str = Field(default="")
    system_user_type_id: int = Field(foreign_key="system_user_type.id", nullable=False)
    system_user_type: Optional[System_User_Type] = Relationship(back_populates="system_users")


class Log(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    time: Optional[datetime]
    log_type: Optional[str] = Field(default="info")
    msg: str
    log_owner: int = Field(default=None, foreign_key="system_user.id")
