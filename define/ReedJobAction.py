from pydantic import BaseModel
from utils.EnderUtil import TimeUtil

class ReedJobAction(BaseModel):
    action: str  # add, miss, execute, remove, execute_detail
    timestamp: str = TimeUtil.now()
    app_id: str
    job_id: str  # a uuid
    job_name: str | None
    callback_url: str | None
    request_header: dict | None
    request_params: dict | None
    response_code: int | None
    response_header: dict | None
    response_content: bytes | None
    exceptions: str | None
