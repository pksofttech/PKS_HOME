import base64
from http.client import HTTPResponse
from io import BytesIO
import json
import os
import time
from typing import Union
from unittest import result

from fastapi import APIRouter, Cookie, Depends, Request, Header, Response

from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import (
    FileResponse,
    RedirectResponse,
    StreamingResponse,
)
import httpx
from pydantic import BaseModel

# from requests.auth import HTTPDigestAuth, HTTPBasicAuth
from PIL import Image

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, asc, desc
from app.core.database import get_async_session
from app.core.auth import access_cookie_token, allowed_permissions, get_jwt_access, get_user_by_id

from ..stdio import *
from app.core import config
from app.core.models import System_User
from sqlalchemy import select

from app.core import models
from app.routes.websocket import WebSockets


DIR_PATH = config.DIR_PATH

templates = Jinja2Templates(directory="templates")
router = APIRouter(tags=["Public"])


@router.get("/page_404")
async def page_404(url: str = ""):
    _now = time_now()
    print_error(f"page_404 : {url}")
    return templates.TemplateResponse(
        "404.html",
        {"request": {}, "now": _now, "app_title": config.APP_TITLE, "url": url},
    )


@router.get("/")
async def main_path(
    app_mode: str | None = Cookie(default="SYSTEM"),
    db: AsyncSession = Depends(get_async_session),
    # user=Depends(access_cookie_token),
):
    _now = time_now()
    # for check_login user
    # print("request from user", user)
    # Check login user

    return templates.TemplateResponse(
        "login.html",
        {"request": {}, "now": _now, "app_title": config.APP_TITLE},
    )


@router.get("/about")
async def about_path(db: AsyncSession = Depends(get_async_session), user=Depends(access_cookie_token)):
    _now = time_now()
    # for check_login user
    print("request from user", user)
    # Check login user
    return templates.TemplateResponse(
        "about.html",
        {"request": {}, "now": _now, "app_title": config.APP_TITLE},
    )


@router.get("/ping")
async def ping(request: Request):
    _now = time_now()
    _header = request.headers
    for k, v in _header.items():
        print(k, v)
    return f"Time process : {time_now() - _now}"


@router.get("/home")
async def router_home(
    db: AsyncSession = Depends(get_async_session),
    # user=Depends(access_cookie_token),
):
    # if not user:
    #     return RedirectResponse(url="/")
    _now = time_now()
    # print(user)
    # datas = {}

    return templates.TemplateResponse(
        "home.html",
        {
            "request": {},
            # "user": user,
            # "datas": datas,
            "now": _now,
        },
    )


@router.get("/system_config")
async def router_system_config(
    db: Session = Depends(get_async_session),
    user=Depends(access_cookie_token),
):
    if not user:
        return RedirectResponse(url="/")
    print(user)
    if not (await allowed_permissions(db, user["system_user_type_id"], "system_config")):
        # return {"success": False, "msg": "not permission_allowed"}
        return templates.TemplateResponse(
            "403.html",
            {
                "request": {},
                "user": user,
            },
        )
    _now = time_now()
    print(user)
    datas = {}

    return templates.TemplateResponse(
        "system_config.html",
        {
            "request": {},
            "user": user,
            "datas": datas,
            "now": _now,
        },
    )
