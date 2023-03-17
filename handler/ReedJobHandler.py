import logging
# import aioredis as redis
import redis
from requests import Response, ConnectTimeout, ReadTimeout, RequestException
from apscheduler.events import JobEvent, EVENT_JOB_ADDED, EVENT_JOB_MISSED, EVENT_JOB_REMOVED
from event.ReedJobEvent import ReedJobExecuteEvent

from define.ReedJobAction import ReedJobAction
from utils.ReedSchedulerUtil import ReedSchedulerUtil

redis_config = {
    "host": ReedSchedulerUtil.get_os_env("REDIS_HOST"),
    "port": 6379,
    "password": ReedSchedulerUtil.get_os_env("REDIS_PASSWORD"),
    "db": 14
}

pool = redis.ConnectionPool(host=redis_config["host"], port=redis_config["port"], password=redis_config["password"],
                   db=redis_config["db"], decode_responses=True)

redis_conn = redis.Redis(connection_pool=pool)

class ReedJobHandler:
    """
        redis struct: list key format: app_id-job_id-history
    """
    def job_added(self, event: EVENT_JOB_ADDED):
        # logging.info(f"event.code:{event.code}, event.job_id:{event.job_id}, event.jobstore:{event.jobstore}")
        job_history_key = event.job_id+"-history"
        app_id, job_id = ReedSchedulerUtil.apart_job_id(event.job_id)
        reed_job_action = ReedJobAction(action="add", app_id=app_id, job_id=job_id)
        redis_conn.lpush(job_history_key, reed_job_action.json())

    def job_missed(self, event: EVENT_JOB_MISSED):
        job_history_key = event.job_id + "-history"
        app_id, job_id = ReedSchedulerUtil.apart_job_id(event.job_id)
        reed_job_action = ReedJobAction(action="miss", app_id=app_id, job_id=job_id)
        redis_conn.lpush(job_history_key, reed_job_action.json())

    def job_remove(self, event: EVENT_JOB_REMOVED):
        job_history_key = event.job_id + "-history"
        app_id, job_id = ReedSchedulerUtil.apart_job_id(event.job_id)
        reed_job_action = ReedJobAction(action="remove", app_id=app_id, job_id=job_id)
        redis_conn.lpush(job_history_key, reed_job_action.json())


    def job_execute(self, event: EVENT_JOB_REMOVED):
        job_history_key = event.job_id + "-history"
        app_id, job_id = ReedSchedulerUtil.apart_job_id(event.job_id)
        reed_job_action = ReedJobAction(action="execute", app_id=app_id, job_id=job_id)
        redis_conn.lpush(job_history_key, reed_job_action.json())


    def job_execute_detail(self, event: ReedJobExecuteEvent):
        app_id = event.app_id
        job_id = event.job_id
        job_name = event.job_name
        callback_url = event.callback_url
        header = event.header
        busi_params = event.busi_params
        response = event.response
        exception = event.exception
        job_history_key = app_id + "-" + job_id + "-history"
        if response is not None:
            reed_job_action = ReedJobAction(action="execute_detail", app_id=app_id, job_id=job_id, job_name=job_name,
                                            callback_url=callback_url, request_header=header,
                                            request_params=busi_params,
                                            response_code=response.status_code, response_header=response.headers,
                                            response_content=response.content, exceptions=exception)
        elif exception is not None:
            response = exception.response
            request = exception.request
            logging.debug(f"reqeust={request}, response={response}")
            reed_job_action = ReedJobAction(action="execute_detail", app_id=app_id, job_id=job_id, job_name=job_name,
                                            callback_url=callback_url, request_header=header,
                                            request_params=busi_params,
                                            response_code=response.status_code, response_header=response.headers,
                                            response_content=response.content, exceptions=exception)
        else:
            reed_job_action = ReedJobAction(action="execute_detail", app_id=app_id, job_id=job_id, job_name=job_name,
                                            callback_url=callback_url, request_header=header,
                                            request_params=busi_params,
                                            response_code=None, response_header=None,
                                            response_content=None, exceptions=exception)
        redis_conn.lpush(job_history_key, reed_job_action.json())




    # async def job_execute_old(self, app_id: str, uuid: str, job_name: str, callback_url: str, header: dict,
    #                       busi_params: dict, response: Response, exception: RequestException):
    #     job_history_key = app_id + "-" + uuid + "-history"
    #     if response:
    #         reed_job_action = ReedJobAction(action="execute", app_id=app_id, job_id=uuid, job_name=job_name,
    #                                     callback_url=callback_url, request_header=header, request_params=busi_params,
    #                                     response_code=response.status_code, response_header=response.headers,
    #                                     response_content=response.content, exception=exception)
    #     elif exception:
    #         response = exception.response
    #         request = exception.request
    #         logging.debug(f"reqeust={request}, response={response}")
    #         reed_job_action = ReedJobAction(action="execute", app_id=app_id, job_id=uuid, job_name=job_name,
    #                                         callback_url=callback_url, request_header=header,
    #                                         request_params=busi_params,
    #                                         response_code=response.status_code, response_header=response.headers,
    #                                         response_content=response.content, exception=exception)
    #     else:
    #         reed_job_action = ReedJobAction(action="execute", app_id=app_id, job_id=uuid, job_name=job_name,
    #                                         callback_url=callback_url, request_header=header,
    #                                         request_params=busi_params,
    #                                         response_code=None, response_header=None,
    #                                         response_content=None, exception=exception)
    #     await redis_conn.lpush(job_history_key, reed_job_action.json())

handler = ReedJobHandler()
