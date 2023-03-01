import logging

from fastapi import APIRouter, Form, Request
from scheduler.SchedulerManager import scheduler
from apscheduler.triggers.interval import IntervalTrigger

from utils.EnderUtil import StringUtil, TimeUtil
from utils.ReedSchedulerUtil import ReedSchedulerUtil

from define.ReedSchedulerErrorCode import ReedSchedulerErrorCode
from define.ReedResult import ReedResult
from define.ReedIntervalJob import ReedIntervalJob

interval = APIRouter()

BUSI_PARAMS = ["seconds", "callback_url", "fingerprint", "job_name", "start_time", "end_time"]

@interval.post("/{app_id}/job", tags=["创建interval类型的job"])
async def create_job(app_id: str, request: Request, seconds: int = Form(0), callback_url: str = Form(None),
                     fingerprint: str = Form(None), job_name: str = Form(None), start_time: str = Form(None),
                     end_time: str = Form(None)):
    if StringUtil.isEmpty(app_id):
        logging.warning(f"parameter error: app_id is empty!")
        result = ReedResult.get(ReedSchedulerErrorCode.APPID_EMPTY, app_id)
        return result
    if not ReedSchedulerUtil.is_validate_app_id(app_id):
        logging.warning(f"parameter error: app_id is invalidate!")
        result = ReedResult.get(ReedSchedulerErrorCode.APPID_INVALIDATE, app_id)
        return result
    if type(seconds) is not int:
        logging.warning(f"parameter error: interval seconds is not a integer")
        result = ReedResult.get(ReedSchedulerErrorCode.SECONDS_TYPE_ERROR, seconds)
        return result
    if seconds == 0:
        logging.warning(f"parameter error: interval seconds is 0")
        result = ReedResult.get(ReedSchedulerErrorCode.SECONDS_IS_ZERO, seconds)
        return result
    if StringUtil.isEmpty(callback_url):
        logging.warning(f"parameter error: callback_url is empty!")
        result = ReedResult.get(ReedSchedulerErrorCode.CALLBACK_URL_EMPTY, callback_url)
        return result
    if not StringUtil.isHttpUrl(callback_url):
        logging.warning(f"parameter error: callback_url is not a url!")
        result = ReedResult.get(ReedSchedulerErrorCode.CALLBACK_URL_INVALIDATE, callback_url)
        return result

    if start_time and not TimeUtil.is_validate_datetime(start_time):
        logging.warning(f"parameter error: start_time is invalidate!")
        result = ReedResult.get(ReedSchedulerErrorCode.START_TIME_INVALIDATE, start_time)
        return result
    if end_time and not TimeUtil.is_validate_datetime(end_time):
        logging.warning(f"parameter error: end_time is invalidate!")
        result = ReedResult.get(ReedSchedulerErrorCode.END_TIME_INVALIDATE, end_time)
        return result

    if start_time and end_time:
        start_time = TimeUtil.get_datetime(start_time)
        end_time = TimeUtil.get_datetime(end_time)
        if start_time >= end_time:
            logging.warning(f"parameter error: end_time should later than start_time!")
            result = ReedResult.get(ReedSchedulerErrorCode.START_TIME_LATER_THAN_END_TIME, {"start_time": start_time,
                                                                                            "end_time": end_time})
            return result

    params = await request.form()
    logging.debug(f"business parameters: {params}")
    params = dict(filter(lambda item: item[0] not in BUSI_PARAMS, params.items()))
    logging.debug(f"after filter business parameters: {params}")
    logging.debug(f"parameters: app_id={app_id}, job_name={job_name}, seconds={seconds}, callback_url={callback_url}, fingerprint={fingerprint}, custom_params:{params}")
    headers = {"fingerprint": fingerprint}
    # _uuid = StringUtil.uuid(app_id)
    _uuid = StringUtil.uuid()
    _id = app_id+"-"+_uuid
    interval_trigger = IntervalTrigger(seconds=seconds, start_date=start_time, end_date=end_time)
    scheduler.add_job(ReedSchedulerUtil.post, trigger=interval_trigger, args=[app_id, _uuid, job_name, callback_url, headers.__str__()],
                      id=_id, name=job_name, kwargs=params, replace_existing=True, max_instances=1, misfire_grace_time=1)
    result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS, _uuid)
    return result


@interval.get("/{app_id}/jobs", tags=["获取app_id下所有的interval类型的job"])
async def get_interval_jobs_by_app_id(app_id: str):
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
            if type(job.trigger) is IntervalTrigger:
                job_list.append(ReedIntervalJob.from_job(job))
    result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS, job_list)
    return result


@interval.get("/{app_id}/job/{job_id}", tags=["在app_id范围内通过job_id获取interval类型的任务"])
async def get_interval_job_by_job_id_within_app_id(app_id: str, job_id: str):
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
    if job and type(job.trigger) is IntervalTrigger:
        result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS, ReedIntervalJob.from_job(job))
        return result
    else:
        result = ReedResult.get(ReedSchedulerErrorCode.JOB_TYPE_ERROR, type(job.trigger))
        return result





