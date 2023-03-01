from datetime import datetime, tzinfo

from apscheduler.job import Job

from define.ReedJob import ReedJob
from utils.ReedSchedulerUtil import ReedSchedulerUtil

class ReedDatetimeJob(ReedJob):
    # 运行时间
    run_time: datetime | str | None
    # 时区
    timezone: str | None

    @staticmethod
    def from_job(job: Job):
        reed_datetime_job = ReedDatetimeJob(id=ReedSchedulerUtil.get_uuid(job.id), name=job.name, type=ReedDatetimeJob.get_type(), sys_args=job.args,
                        busi_args=job.kwargs, run_time=job.trigger.run_date,
                        timezone=job.trigger.run_date.tzinfo.zone,
                        status = "running" if job.next_run_time else "paused")
        return reed_datetime_job

    @staticmethod
    def get_type() -> str:
        return "date"



