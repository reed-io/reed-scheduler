import requests
from requests import ConnectTimeout, ReadTimeout
from utils.EnderUtil import TimeUtil

url = "http://www.baidu.com"
header = None
busi_params = None
app_id = "ender"
uuid = "asdfa-sdf-sd-f-sd"
job_name = "name"
timeout = (1.5, 3)
try:
    response = requests.post(url=url, headers=header, data=busi_params, timeout=timeout)
    print(
        f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} with header:{header}, data:{busi_params}")
    print(
        f"app_id:{app_id} uuid:{uuid} job_name:{job_name} responsed status_code={response.status_code}, headers={response.headers}, content={response.content}")
except ConnectTimeout as e1:
    print(e1.with_traceback())
    print(
        f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} connection time out within {timeout[0]}")
except ReadTimeout as e2:
    print(e2.with_traceback())
    print(
        f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} response read time out within {timeout[1]}")
finally:
    print(
        f"app_id:{app_id} uuid:{uuid} job_name:{job_name} post {url} header={header}, body={busi_params}, timeout={timeout} finished at {TimeUtil.now()}")
    print("-----", response, e1, e2)