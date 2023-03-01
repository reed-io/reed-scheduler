import re, logging
from requests import ConnectTimeout, ReadTimeout, Response
import requests
from utils.EnderUtil import TimeUtil

APP_ID_PATTERN = re.compile("^[A-Za-z0-9]{5,16}$")  # 数字或字母，长度在5~16之间
class ReedSchedulerUtil:
    @staticmethod
    def gen_job_id(app_id: str, uuid: str) -> str:
        return app_id + "-" + uuid


    @staticmethod
    def get_uuid(job_id: str) -> str:
        return "-".join(job_id.split("-")[1:])


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
        except ReadTimeout as e2:
            print(e2.with_traceback())
            logging.error(
                f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} response read time out within {timeout[1]}")
        finally:
            logging.info(
                f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} header={header}, body={busi_params}, timeout={timeout} finished at {TimeUtil.now()}")




# print(ReedSchedulerUtil.gen_job_id("ender", "12312"))
# print(ReedSchedulerUtil.get_uuid("ender-dcee2a97-c23f-11ed-b61e-5c80b6092062"))
# print(ReedSchedulerUtil.is_validate_app_id("end1"))