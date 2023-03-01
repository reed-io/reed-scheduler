import logging
# from requests_async import ConnectTimeout, ReadTimeout, Response
# import requests_async as requests
from requests import ConnectTimeout, ReadTimeout, Response
import requests
from utils.EnderUtil import TimeUtil

class NetUtil:

    @staticmethod
    def post(app_id, uuid, job_name, url, header, timeout=(1.5, 3), **busi_params):
        try:
            header = eval(header)
            response = requests.post(url=url, headers=header, data=busi_params, timeout=timeout)
            logging.debug(f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} with header:{header}, data:{busi_params}")
            logging.debug(f"app_id:{app_id} uuid:{uuid} job_name:{job_name} responsed status_code={response.status_code}, headers={response.headers}, content={response.content}")
        except ConnectTimeout as e1:
            print(e1.with_traceback())
            logging.error(f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} connection time out within {timeout[0]}")
        except ReadTimeout as e2:
            print(e2.with_traceback())
            logging.error(f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} response read time out within {timeout[1]}")
        finally:
            logging.info(f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} header={header}, body={busi_params}, timeout={timeout} finished at {TimeUtil.now()}")