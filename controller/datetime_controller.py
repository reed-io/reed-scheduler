import logging
import pytz
from apscheduler.triggers.date import DateTrigger
from fastapi import APIRouter, Form, Request

from define.ReedDatetimeJob import ReedDatetimeJob
from scheduler.SchedulerManager import scheduler

from utils.EnderUtil import StringUtil, TimeUtil
from utils.ReedSchedulerUtil import ReedSchedulerUtil

from define.ReedSchedulerErrorCode import ReedSchedulerErrorCode
from define.ReedResult import ReedResult

datetime = APIRouter()

BUSI_PARAMS = ["datetime", "callback_url", "fingerprint", "job_name"]
DEFAULT_TIMEZONE = 'Asia/Shanghai'

@datetime.post("/{app_id}/job", tags=["创建datetime类型的job"])
async def create_job(app_id: str, request: Request, datetime: str = Form(None), callback_url: str = Form(None),
                     fingerprint: str = Form(None), job_name: str = Form(None)):
    if StringUtil.isEmpty(app_id):
        logging.warning(f"parameter error: app_id is empty!")
        result = ReedResult.get(ReedSchedulerErrorCode.APPID_EMPTY, app_id)
        return result
    if not ReedSchedulerUtil.is_validate_app_id(app_id):
        logging.warning(f"parameter error: app_id is invalidate!")
        result = ReedResult.get(ReedSchedulerErrorCode.APPID_INVALIDATE, app_id)
        return result
    if StringUtil.isEmpty(datetime):
        logging.warning(f"parameter error: datetime is empty!")
        result = ReedResult.get(ReedSchedulerErrorCode.DATETIME_EMPTY, datetime)
        return result
    if not TimeUtil.is_validate_datetime(datetime):
        logging.warning(f"parameter error: datetime is invalidate!")
        result = ReedResult.get(ReedSchedulerErrorCode.DATETIME_INVALIDATE, datetime)
        return result
    datetime = TimeUtil.get_datetime(datetime)
    if datetime <= TimeUtil.now():
        logging.warning(f"parameter error: datetime is already passed!")
        result = ReedResult.get(ReedSchedulerErrorCode.DATETIME_PASSED, datetime)
        return result
    if StringUtil.isEmpty(callback_url):
        logging.warning(f"parameter error: callback_url is empty!")
        result = ReedResult.get(ReedSchedulerErrorCode.CALLBACK_URL_EMPTY, callback_url)
        return result
    if not StringUtil.isHttpUrl(callback_url):
        logging.warning(f"parameter error: callback_url is not a url!")
        result = ReedResult.get(ReedSchedulerErrorCode.CALLBACK_URL_INVALIDATE, callback_url)
        return result
    params = await request.form()
    logging.debug(f"business parameters: {params}")
    params = dict(filter(lambda item: item[0] not in BUSI_PARAMS, params.items()))
    logging.debug(f"after filter business parameters: {params}")
    logging.debug(f"parameters: app_id={app_id}, job_name={job_name}, datetime={datetime}, callback_url={callback_url}, fingerprint={fingerprint}, custom_params:{params}")
    headers = {"fingerprint": fingerprint}
    # _uuid = StringUtil.uuid(app_id)
    _uuid = StringUtil.uuid()
    # _id = app_id+"-"+_uuid
    _id = ReedSchedulerUtil.gen_job_id(app_id, _uuid)
    datetime_trigger = DateTrigger(run_date=datetime, timezone=pytz.timezone(DEFAULT_TIMEZONE))
    scheduler.add_job(ReedSchedulerUtil.post, trigger=datetime_trigger, args=[app_id, _uuid, job_name, callback_url, headers.__str__()],
                      id=_id, name=job_name, kwargs=params, replace_existing=True, max_instances=1, misfire_grace_time=1)
    result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS, _uuid)
    return result


@datetime.get("/{app_id}/jobs", tags=["获取app_id下所有的datetime类型的job"])
async def get_datetime_jobs_by_app_id(app_id: str):
    if StringUtil.isEmpty(app_id):
        logging.warning(f"parameter error: app_id is empty!")
        result = ReedResult.get(ReedSchedulerErrorCode.APPID_EMPTY, app_id)
        return result
    if not ReedSchedulerUtil.is_validate_app_id(app_id):
        logging.warning(f"parameter error: app_id is invalidate!")
        result = ReedResult.get(ReedSchedulerErrorCode.APPID_INVALIDATE, app_id)
        return result
    all_jobs = scheduler.get_jobs()
    job_list = list()
    for job in all_jobs:
        if job.id.startswith(app_id):
            if type(job.trigger) is DateTrigger:
                job_list.append(ReedDatetimeJob.from_job(job))
    result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS, job_list)
    return result


@datetime.get("/{app_id}/job/{job_id}", tags=["在app_id范围内通过job_id获取datetime类型的任务"])
async def get_datetime_job_by_job_id_within_app_id(app_id: str, job_id: str):
    if StringUtil.isEmpty(app_id):
        logging.warning(f"parameter error: app_id is empty!")
        result = ReedResult.get(ReedSchedulerErrorCode.APPID_EMPTY, app_id)
        return result
    if not ReedSchedulerUtil.is_validate_app_id(app_id):
        logging.warning(f"parameter error: app_id is invalidate!")
        result = ReedResult.get(ReedSchedulerErrorCode.APPID_INVALIDATE, app_id)
        return result
    if StringUtil.isEmpty(job_id):
        logging.warning(f"parameter error: job_id is empty!")
        result = ReedResult.get(ReedSchedulerErrorCode.JOBID_EMPTY, job_id)
        return result
    job = scheduler.get_job(job_id=app_id+"-"+job_id)
    if job and type(job.trigger) is DateTrigger:
        result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS, ReedDatetimeJob.from_job(job))
        return result
    else:
        result = ReedResult.get(ReedSchedulerErrorCode.JOB_TYPE_ERROR, type(job.trigger))
        return result

