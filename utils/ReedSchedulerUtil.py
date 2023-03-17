import re, logging, os
from requests import ConnectTimeout, ReadTimeout, Response, HTTPError
import requests

# from handler.ReedJobHandler import ReedJobHandler
from utils.EnderUtil import TimeUtil
from event.ReedJobEvent import ReedJobExecuteEvent

APP_ID_PATTERN = re.compile("^[A-Za-z0-9]{5,16}$")  # 数字或字母，长度在5~16之间
# reed_job_handler = ReedJobHandler()

from scheduler.SchedulerManager import scheduler

class ReedSchedulerUtil:
    @staticmethod
    def get_os_env(key: str) -> str:
        return os.getenv(key)

    @staticmethod
    def gen_job_id(app_id: str, uuid: str) -> str:
        return app_id + "-" + uuid


    @staticmethod
    def get_uuid(job_id: str) -> str:
        return "-".join(job_id.split("-")[1:])

    @staticmethod
    def apart_job_id(job_id: str):
        lst = job_id.split("-")
        assert len(lst) > 0
        app_id = lst[0]
        uuid = "-".join(job_id.split("-")[1:])
        return app_id, uuid


    @staticmethod
    def gen_job_history_key(app_id: str, job_id: str) -> str:
        return app_id + "-" + job_id + "-history"


    @staticmethod
    def is_validate_app_id(app_id: str) -> bool:
        return re.match(APP_ID_PATTERN, app_id) != None

    @staticmethod
    def post(app_id, uuid, job_name, url, header, timeout=(1.5, 3), **busi_params):
        try:
            header = eval(header)
            response = requests.post(url=url, headers=header, data=busi_params, timeout=timeout)
            logging.debug(
                f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} with header:{header}, data:{busi_params}")
            logging.debug(
                f"app_id:{app_id} uuid:{uuid} job_name:{job_name} responsed status_code={response.status_code}, headers={response.headers}, content={response.content}")
        except ConnectTimeout as e1:
            print(e1.with_traceback())
            logging.error(
                f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} connection time out within {timeout[0]}")
            # await reed_job_handler.job_execute(app_id, uuid, job_name, url, header, busi_params, None, e1)
            event = ReedJobExecuteEvent(ReedJobExecuteEvent.EVENT_JOB_EXECUTE_DETAIL, app_id, uuid, job_name, url, header, busi_params, None, e1)
            scheduler._dispatch_event(event)
        except ReadTimeout as e2:
            print(e2.with_traceback())
            logging.error(
                f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} response read time out within {timeout[1]}")
            # await reed_job_handler.job_execute(app_id, uuid, job_name, url, header, busi_params, None, e2)
            event = ReedJobExecuteEvent(ReedJobExecuteEvent.EVENT_JOB_EXECUTE_DETAIL, app_id, uuid, job_name, url, header,
                                        busi_params, None, e2)
            scheduler._dispatch_event(event)
        except HTTPError as e3:
            print(e3.with_traceback())
            logging.error(
                f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} get a http error {e3.__str__()}")
            # await reed_job_handler.job_execute(app_id, uuid, job_name, url, header, busi_params, None, e2)
            event = ReedJobExecuteEvent(ReedJobExecuteEvent.EVENT_JOB_EXECUTE_DETAIL, app_id, uuid, job_name, url, header,
                                        busi_params, None, e3)
            scheduler._dispatch_event(event)
        else:
            # await reed_job_handler.job_execute(app_id, uuid, job_name, url, header, busi_params, response, None)
            event = ReedJobExecuteEvent(ReedJobExecuteEvent.EVENT_JOB_EXECUTE_DETAIL, app_id, uuid, job_name, url, header,
                                        busi_params, response, None)
            scheduler._dispatch_event(event)
        finally:
            logging.info(
                f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} header={header}, body={busi_params}, timeout={timeout} finished at {TimeUtil.now()}")





# print(ReedSchedulerUtil.gen_job_id("ender", "12312"))
# print(ReedSchedulerUtil.get_uuid("ender-dcee2a97-c23f-11ed-b61e-5c80b6092062"))
# print(ReedSchedulerUtil.is_validate_app_id("end1"))