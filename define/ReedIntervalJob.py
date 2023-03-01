from datetime import datetime
from utils.ReedSchedulerUtil import ReedSchedulerUtil

from apscheduler.job import Job

from define.ReedJob import ReedJob

class ReedIntervalJob(ReedJob):
    # 触发间隔
    interval_seconds: int
    # 最早开始时间
    start_time: datetime | str | None
    # 最晚执行时间
    end_time: datetime | str | None
    # 时区
    timezone: str | None
    # 任务触发的时间差
    jitter: int | None
    # 下次触发时间 tuple(query_time, next_schedule_time)
    next_fire_time: tuple | None


    @staticmethod
    def from_job(job: Job):
        reed_interval_job = ReedIntervalJob(id=ReedSchedulerUtil.get_uuid(job.id), job_name=job.name, type=ReedIntervalJob.get_type(), sys_args=job.args,
                        busi_args=job.kwargs, interval_seconds=job.trigger.interval.seconds,
                        start_time=job.trigger.start_date, end_time=job.trigger.end_date,
                        timezone=job.trigger.timezone.zone, jitter=job.trigger.jitter, next_run_time=job.next_run_time,
                        next_fire_time=(datetime.now(), job.next_run_time),
                        status="running" if job.next_run_time else "paused")
        return reed_interval_job

    @staticmethod
    def get_type() -> str:
        return "interval"
