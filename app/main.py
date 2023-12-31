# Python > 3.8
# Edit by Pksofttech for user
# ? main for set application
import logging
from urllib import response
from fastapi import FastAPI, Request

from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse, RedirectResponse, HTMLResponse
from pydantic import Json

# from fastapi_mqtt.fastmqtt import FastMQTT
# from fastapi_mqtt.config import MQTTConfig
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .stdio import *

from app.core import auth, database

from fastapi_utils.tasks import repeat_every

app = FastAPI(title="WEB-API", version="22.06.0")

app.mount("/static", StaticFiles(directory="./static"), name="static")
# app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

# Set all CORS enabled origins

# root_logger = logging.getLogger()
# root_logger.setLevel(logging.INFO)
# handler = logging.FileHandler("applog.log", "w", "utf-8")
# handler.setFormatter(logging.Formatter(f"%(levelname)s %(asctime)s  %(name)s %(threadName)s : %(message)s"))
# root_logger.addHandler(handler)
#
# root_logger.info(f"************************************************************")
# root_logger.info(f"Start Msg Logger at time {time_now()}")
# root_logger.info(f"************************************************************")

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://192.168.1.152/",
# ]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await database.init_db()
    print_success(f"Server Start Time : {time_now()}")


@app.on_event("shutdown")
async def shutdown_event():
    print_warning(f"Server shutdown Time : {time_now()}")


@app.on_event("startup")
@repeat_every(seconds=60)
def task_run_repeat_every() -> None:
    _now = time_now()
    if _now.hour == 13 and _now.minute == 15:
        print_success(f"Task run repeat :{time_now()}")


@app.middleware("http")
async def process_time(request: Request, call_next):
    start_time = time_now()
    response = await call_next(request)
    process_time = time_now() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"Process time :{process_time.microseconds} us")

    return response


# ? Setting router path
from app.routes import views, websocket, api_system_user

app.include_router(auth.router)
app.include_router(websocket.router)
app.include_router(views.router)
app.include_router(api_system_user.router)


# @app.exception_handler(HTTPException)
# async def app_exception_handler(request: Request, exception: HTTPException):
#     url_str = str(request.url).split("/")[-1]
#     # print_error(url_str)
#     if request.method == "GET":
#         print_error(exception.detail)
#         if exception.detail == "Not Found":
#             if "." in url_str:
#                 return HTMLResponse(str(exception.detail), status_code=exception.status_code)
#             return RedirectResponse(url=f"/page_404?url={request.url}")
#         return PlainTextResponse(str(exception.detail), status_code=exception.status_code)

#     else:
#         return JSONResponse(str(exception.detail), status_code=exception.status_code)
