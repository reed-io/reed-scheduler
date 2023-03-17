import logging

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import APIRouter, Form, Request

from define.ReedCronJob import ReedCronJob
from define.ReedDatetimeJob import ReedDatetimeJob
from define.ReedIntervalJob import ReedIntervalJob
from scheduler.SchedulerManager import scheduler

from define.ReedJobAction import ReedJobAction

from define.ReedSchedulerErrorCode import ReedSchedulerErrorCode
from define.ReedResult import ReedResult

from utils.EnderUtil import StringUtil
from utils.ReedSchedulerUtil import ReedSchedulerUtil

console = APIRouter()


@console.get("/{app_id}/jobs", tags=["获取app_id下所有类型的job"])
async def get_jobs_by_app_id(app_id: str):
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
            if type(job.trigger) is CronTrigger:
                job_list.append(ReedCronJob.from_job(job))
            if type(job.trigger) is DateTrigger:
                job_list.append(ReedDatetimeJob.from_job(job))
            if type(job.trigger) is IntervalTrigger:
                job_list.append(ReedIntervalJob.from_job(job))
    result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS, job_list)
    return result


@console.get("/{app_id}/job/{job_id}", tags=["在app_id范围内通过job_id获取任意类型的任务"])
async def get_job_by_job_id_within_app_id(app_id: str, job_id: str):
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
    if job and type(job.trigger) is CronTrigger:
        result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS, ReedCronJob.from_job(job))
        return result
    elif job and type(job.trigger) is DateTrigger:
        result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS, ReedDatetimeJob.from_job(job))
        return result
    elif job and type(job.trigger) is IntervalTrigger:
        result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS, ReedIntervalJob.from_job(job))
        return result
    else:
        result = ReedResult.get(ReedSchedulerErrorCode.JOB_TYPE_ERROR, type(job.trigger))
        return result


@console.put("/{app_id}/job/{job_id}", tags=["暂停或者唤醒指定的任务"])
async def change_job_status_by_job_id_within_app_id(app_id: str, job_id: str, action: str = Form(None)):
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
    if StringUtil.isEmpty(action):
        logging.warning(f"parameter error: action is empty!")
        result = ReedResult.get(ReedSchedulerErrorCode.ACTION_EMPTY, action)
        return result
    if action not in ["pause", "resume"]:
        logging.warning(f"parameter error: action is invalidate, only pause or resume accepted!")
        result = ReedResult.get(ReedSchedulerErrorCode.ACTION_INVALIDATE, action)
        return result

    _job_id = ReedSchedulerUtil.gen_job_id(app_id, job_id)
    job = scheduler.get_job(_job_id)
    if not job:
        logging.warning(f"can not find a job with job_id: {_job_id}")
        result = ReedResult.get(ReedSchedulerErrorCode.JOB_NOT_FOUND, job_id)
        return result
    if action == "pause":
        scheduler.pause_job(_job_id)
    else:
        scheduler.resume_job(_job_id)

    result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS, {"app_id": app_id, "job_id": job_id, "job_name": job.name,
                                                            "before_status": "running" if job.next_run_time else "paused",
                                                            "now_status": "running" if action == "resume" else "paused"})
    return result


@console.delete("/{app_id}/job/{job_id}", tags=["删除指定的任务"])
async def delete_job_by_job_id_within_app_id(app_id: str, job_id: str):
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
    _job_id = ReedSchedulerUtil.gen_job_id(app_id, job_id)
    job = scheduler.get_job(_job_id)
    if not job:
        logging.warning(f"can not find a job with job_id: {_job_id}")
        result = ReedResult.get(ReedSchedulerErrorCode.JOB_NOT_FOUND, job_id)
        return result
    scheduler.remove_job(_job_id)
    result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS)
    return result


@console.get("/{app_id}/job/{job_id}/history", tags=["获取指定任务的历史记录"])
async def get_job_history_by_job_id_within_app_id(app_id: str, job_id: str, request: Request):
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
    redis_conn = request.app.state.redis
    job_history_key = ReedSchedulerUtil.gen_job_history_key(app_id, job_id)
    history_list_length = await redis_conn.llen(job_history_key)
    history = await redis_conn.lrange(job_history_key, 0, history_list_length)
    reed_job_action_list = list()
    for action in history:
        reed_job_action = ReedJobAction.parse_raw(action)
        reed_job_action_list.append(reed_job_action)
    result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS, reed_job_action_list)
    return result

