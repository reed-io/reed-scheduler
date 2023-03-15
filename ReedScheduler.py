import logging
import traceback
import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from starlette.exceptions import HTTPException

from define.ReedResult import ReedResult
from define.BaseErrorCode import BaseErrorCode as ErrorCode

from scheduler.SchedulerManager import scheduler

from controller.test_scheduler import test as test_router
from controller.interval_controller import interval as interval_router
from controller.datetime_controller import datetime as datetime_router
from controller.cron_controller import cron as cron_router
from controller.console_controller import console as console_router

from fastapi.middleware.cors import CORSMiddleware

ReedScheduler = FastAPI(title="ReedScheduler")
ReedScheduler.include_router(console_router, prefix="/console")
# ReedScheduler.include_router(test_router, prefix="/test")
ReedScheduler.include_router(interval_router, prefix="/interval")
ReedScheduler.include_router(datetime_router, prefix="/datetime")
ReedScheduler.include_router(cron_router, prefix="/cron")



"""
logging模块常用format格式说明
%(levelno)s: 打印日志级别的数值
%(levelname)s: 打印日志级别名称
%(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s: 打印当前执行程序名，python如：login.py
%(funcName)s: 打印日志的当前函数
%(lineno)d: 打印日志的当前行号,在第几行打印的日志
%(asctime)s: 打印日志的时间
%(thread)d: 打印线程ID
%(threadName)s: 打印线程名称 
%(process)d: 打印进程ID
%(message)s: 打印日志信息
"""
logging_format = "%(asctime)s [%(thread)d %(threadName)s] {%(filename)s - line:%(lineno)d - %(funcName)s} <%(levelname)s> %(message)s"
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": logging_format
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": logging_format
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout"
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "DEBUG",
        },
        "uvicorn.error": {
            "level": "DEBUG",
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": "DEBUG",
            "propagate": False,
        }
    }
}

origins = [
    "http://localhost",
    "http://localhost:8080",
    "*"
]

ReedScheduler.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def redis_management(ReedCalendar: FastAPI):
    @ReedCalendar.on_event("startup")
    async def init_redis():
        # start scheduler
        scheduler.start()


    @ReedCalendar.on_event("shutdown")
    async def close_redis():
        ...


redis_management(ReedScheduler)


@ReedScheduler.get("/")
async def index():
    return ReedResult.get(ErrorCode.SUCCESS, "ReedCalendar Service is running")


@ReedScheduler.exception_handler(HTTPException)
async def fastapi_http_exception_handler(request: Request, exc: HTTPException):
    logging.error(
        f"HTTPException\nURL:{request.url}\tMethod:{request.method}\n\tHeaders:{request.headers}\n{traceback.format_exc()}")
    result = ReedResult.get(ErrorCode.UNKNOWN_ERROR,
                            {"http_status_code": str(exc.status_code), "detail": str(exc.detail)})
    return JSONResponse(
        status_code=exc.status_code,
        content=eval(result.standard_format())
    )


@ReedScheduler.exception_handler(RequestValidationError)
async def fastapi_request_validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(
        f"RequestValidationError\nURL:{request.url}\tMethod:{request.method}\n\tHeaders:{request.headers}\n{traceback.format_exc()}")
    result = ReedResult.get(ErrorCode.REQUEST_VALIDATION_ERROR,
                            {"tips": exc.errors(), "body": str(exc.body)}).standard_format()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=eval(result)
    )


@ReedScheduler.exception_handler(Exception)
async def fastapi_exception_handler(request: Request, exc: Exception):
    logging.error(
        f"Exception\nURL:{request.url}\tMethod:{request.method}\n\tHeaders:{request.headers}\n{traceback.format_exc()}")
    result = ReedResult.get(ErrorCode.UNKNOWN_ERROR,
                            {"tips": exc.__repr__(), "traceback": traceback.format_exc()}).standard_format()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=eval(result)
    )


if __name__ == "__main__":
    uvicorn.run("ReedScheduler:ReedScheduler", host="0.0.0.0", port=5000, log_config=logging_config)


