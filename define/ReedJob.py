from datetime import datetime

from pydantic import BaseModel

from apscheduler.job import Job

import abc

class ReedJob(BaseModel, metaclass=abc.ABCMeta):
    id: str
    job_name: str | None
    type: str
    sys_args: list | None
    busi_args: dict | None
    next_run_time: datetime | None
    status: str | None

    @staticmethod
    @abc.abstractmethod
    def from_job(job: Job):
        ...

    @staticmethod
    @abc.abstractmethod
    def get_type() -> str:
        ...
