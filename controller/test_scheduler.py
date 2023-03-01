import logging


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from define.ReedResult import ReedResult
from define.BaseErrorCode import BaseErrorCode

from fastapi import APIRouter, Request


test = APIRouter()


redis_config = {
    "host": "service.persona.net.cn",
    "port": 6379,
    "password": "Shashiyuefu@2021",
    "db": 14
}

mysql_info = dict(
    host="service.persona.net.cn",
    port=33066,
    username="ender",
    password='Passw0rd#12345',
    dbname="calendar",
    encoding="utf8"
)

scheduler_config = {
    "jobstores": {
        'default': RedisJobStore(**redis_config)
    },
    # "jobstores": {
    #     'default': SQLAlchemyJobStore(url="mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8"
    #                                                          % (mysql_info['username'], mysql_info['password'],
    #                                                             mysql_info['host'], mysql_info['port'],
    #                                                            mysql_info['dbname']))
    # },
    "executors": {
        'default': ThreadPoolExecutor(10)
    },
    "job_defaults": {
        'coalesce': False,
    }
}


# scheduler = AsyncIOScheduler(**scheduler_config)
scheduler = BackgroundScheduler(**scheduler_config)
scheduler.start()

def executor(args):
    print("test", args)
    logging.debug("test")

@test.post('/interval/{job_id}', tags=["指定jobId创建一个datetime类型的任务"])
async def interval_create(job_id: str):
    job = scheduler.add_job(executor, "interval", seconds=3, args=["ender"], id=job_id, replace_existing=True)
    result = ReedResult.get(BaseErrorCode.SUCCESS, job.__str__())
    return result


@test.put("/interval/{job_id}", tags=["暂定指定的任务"])
async def interval_pause(job_id: str):
    job = scheduler.get_job(job_id=job_id)
    job.pause()
    logging.info(f"job[{job_id}] paused")
    result = ReedResult.get(BaseErrorCode.SUCCESS, job_id)
    return result



@test.get("/jobs", tags=["获取所有任务"])
async def get_jobs():
    jobs = scheduler.get_jobs()
    logging.debug(jobs)
    for job in jobs:
        logging.debug(job.__getstate__())
        logging.debug(f"job[{job.trigger.start_date}, {job.trigger.end_date}, {job.trigger.timezone}, {job.trigger.interval}, {job.trigger.jitter}]")
        logging.debug(f"job.pendding={job.pending}")
    result = ReedResult.get(BaseErrorCode.SUCCESS, job.__repr__())
    return result


@test.post("/ender", tags=["用于接受调用并打印数据的测试接口"])
async def ender(request: Request):
    logging.debug(f"request:{request}")
    logging.debug(f"headers:{request.headers}")
    logging.debug(f"form:{await request.form()}")
    result = ReedResult.get(BaseErrorCode.SUCCESS)
    return result


