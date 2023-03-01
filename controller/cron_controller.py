import logging

from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, Form, Request

from define.ReedCronJob import ReedCronJob
from scheduler.SchedulerManager import scheduler

from utils.EnderUtil import StringUtil, TimeUtil
from utils.ReedSchedulerUtil import ReedSchedulerUtil

from define.ReedSchedulerErrorCode import ReedSchedulerErrorCode
from define.ReedResult import ReedResult

cron = APIRouter()

DEFAULT_CRON_VALUE = "*"
DAY_OF_WEEK_STRINGS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
BUSI_PARAMS = ['callback_url', 'fingerprint', 'job_name', 'year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second', 'start_time', 'end_time']

@cron.post("/{app_id}/job", tags=["创建cron类型的job"])
async def create_job(app_id: str, request: Request, callback_url: str = Form(None), fingerprint: str = Form(None),
                     job_name: str = Form(None), year: int | str = Form(DEFAULT_CRON_VALUE), month: int | str = Form(DEFAULT_CRON_VALUE),
                     day: int | str = Form(DEFAULT_CRON_VALUE), week: int | str = Form(DEFAULT_CRON_VALUE), day_of_week: int | str = Form(DEFAULT_CRON_VALUE),
                     hour: int | str = Form(DEFAULT_CRON_VALUE), minute: int | str = Form(DEFAULT_CRON_VALUE), second: int | str = Form(DEFAULT_CRON_VALUE),
                     start_time: str = Form(None), end_time: str = Form(None)):
    if StringUtil.isEmpty(app_id):
        logging.warning(f"parameter error: app_id is empty!")
        result = ReedResult.get(ReedSchedulerErrorCode.APPID_EMPTY, app_id)
        return result
    if not ReedSchedulerUtil.is_validate_app_id(app_id):
        logging.warning(f"parameter error: app_id is invalidate!")
        result = ReedResult.get(ReedSchedulerErrorCode.APPID_INVALIDATE, app_id)
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

    if year == month == day == week == day_of_week == hour == minute == second == DEFAULT_CRON_VALUE:
        logging.warning(f"parameter error: year, month, day, week, day_of_week, hour, minute, second are all default value!")
        result = ReedResult.get(ReedSchedulerErrorCode.ALL_CRON_BIT_DEFAULT, {'year': year, 'month': month, 'day': day,
                                                                              'week': week, 'day_of_week': day_of_week,
                                                                              'hour': hour, 'minute': minute, 'second': second})
        return result
    if year != DEFAULT_CRON_VALUE and not 1900 <= year <= 9999:
        logging.warning(f"parameter error: year is invalidate! should be * or integer between 1900 and 9999")
        result = ReedResult.get(ReedSchedulerErrorCode.YEAR_INVALIDATE, year)
        return result
    if month != DEFAULT_CRON_VALUE and not 1 <= month <= 12:
        logging.warning(f"parameter error: year is invalidate! should be * or between 1 and 12")
        result = ReedResult.get(ReedSchedulerErrorCode.MONTH_INVALIDATE, month)
        return result
    if day != DEFAULT_CRON_VALUE and not 1 <= day <= 31:
        logging.warning(f"parameter error: day is invalidate! should be * or between 1 and 31")
        result = ReedResult.get(ReedSchedulerErrorCode.DAY_INVALIDATE, day)
        return result
    if week != DEFAULT_CRON_VALUE and not 1 <= week <= 53:
        logging.warning(f"parameter error: week is invalidate! should be * or between 1 and 53")
        result = ReedResult.get(ReedSchedulerErrorCode.WEEK_INVALIDATE, week)
        return result
    if day_of_week != DEFAULT_CRON_VALUE and not 0 <= day_of_week <= 6 and day_of_week not in DAY_OF_WEEK_STRINGS:
        logging.warning(f"parameter error: day_of_week is invalidate! should be * or between 0 and 6 or [mon,tue,wed,thu,fri,sat,sun]")
        result = ReedResult.get(ReedSchedulerErrorCode.DAY_OF_WEEK_INVALIDATE, day_of_week)
        return result
    if hour != DEFAULT_CRON_VALUE and not 0 <= hour <= 23:
        logging.warning(f"parameter error: hour is invalidate! should be * or between 0 and 23")
        result = ReedResult.get(ReedSchedulerErrorCode.HOUR_INVALIDATE, hour)
        return result
    if minute != DEFAULT_CRON_VALUE and not 0 <= minute <= 59:
        logging.warning(f"parameter error: minute is invalidate! should be * or between 0 and 59")
        result = ReedResult.get(ReedSchedulerErrorCode.MINUTE_INVALIDATE, minute)
        return result
    if second != DEFAULT_CRON_VALUE and not 0 <= second <= 59:
        logging.warning(f"parameter error: second is invalidate! should be * or between 0 and 59")
        result = ReedResult.get(ReedSchedulerErrorCode.SECOND_INVALIDATE, second)
        return result

    params = await request.form()
    logging.debug(f"business parameters: {params}")
    params = dict(filter(lambda item: item[0] not in BUSI_PARAMS, params.items()))
    logging.debug(f"after filter business parameters: {params}")
    logging.debug(f"parameters: app_id={app_id}, name={job_name}, callback_url={callback_url}, fingerprint={fingerprint}, "
                  f"year={year}, month={month}, day={day}, week={week}, day_of_week={day_of_week}, hour={hour}, "
                  f"minute={minute}, second={second}, start_time={start_time}, end_time={end_time} custom_params:{params}")
    headers = {"fingerprint": fingerprint}
    # _uuid = StringUtil.uuid(app_id)
    _uuid = StringUtil.uuid()
    _id = app_id+"-"+_uuid
    cron_trigger = CronTrigger(year=year, month=month, day=day, week=week, day_of_week=day_of_week, hour=hour,
                               minute=minute, second=second, start_date=start_time, end_date=end_time)
    scheduler.add_job(ReedSchedulerUtil.post, trigger=cron_trigger, args=[app_id, _uuid, job_name, callback_url, headers.__str__()],
                      id=_id, name=job_name, kwargs=params, replace_existing=True, max_instances=1, misfire_grace_time=1)
    result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS, _uuid)
    return result


@cron.get("/{app_id}/jobs", tags=["获取app_id下所有的cron类型的job"])
async def get_cron_jobs_by_app_id(app_id: str):
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
    result = ReedResult.get(ReedSchedulerErrorCode.SUCCESS, job_list)
    return result


@cron.get("/{app_id}/job/{job_id}", tags=["在app_id范围内通过job_id获取cron类型的任务"])
async def get_cron_job_by_job_id_within_app_id(app_id: str, job_id: str):
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
    else:
        result = ReedResult.get(ReedSchedulerErrorCode.JOB_TYPE_ERROR, type(job.trigger))
        return result


