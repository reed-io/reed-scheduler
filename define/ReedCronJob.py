from datetime import datetime, tzinfo

from apscheduler.job import Job

from define.ReedJob import ReedJob
from utils.ReedSchedulerUtil import ReedSchedulerUtil

class ReedCronJob(ReedJob):
    # 年  4-digit year
    year: int | str | None
    #  month (1-12)
    month: int | str | None
    #  day of month (1-31)
    day: int | str | None
    #  ISO week (1-53)
    week: int | str | None
    #  number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
    day_of_week: int | str | None
    #  hour (0-23)
    hour: int | str | None
    #  minute (0-59)
    minute: int | str | None
    #  second(0 - 59)
    second: int | str | None
    # 最早开始时间 earliest possible date/time to trigger on (inclusive)
    start_time: datetime | str | None
    # 最晚执行时间  latest possible date/time to trigger on (inclusive)
    end_time: datetime | str | None
    # 时区
    timezone: str | None
    # 任务触发的时间差
    jitter: int | None

    @staticmethod
    def from_job(job: Job):
        reed_cron_job = ReedCronJob(id=ReedSchedulerUtil.get_uuid(job.id), name=job.name, type=ReedCronJob.get_type(), sys_args=job.args,
                        busi_args=job.kwargs, year=job.trigger.fields[0].expressions[0].__str__(), month=job.trigger.fields[1].expressions[0].__str__(), day=job.trigger.fields[2].expressions[0].__str__(),
                        week=job.trigger.fields[3].expressions[0].__str__(), day_of_week=job.trigger.fields[4].expressions[0].__str__(), hour=job.trigger.fields[5].expressions[0].__str__(),
                        minute=job.trigger.fields[6].expressions[0].__str__(), second=job.trigger.fields[7].expressions[0].__str__(),
                        start_time=job.trigger.start_date, end_time=job.trigger.end_date,
                        timezone=job.trigger.timezone.zone, jitter=job.trigger.jitter,
                        status = "running" if job.next_run_time else "paused")
        return reed_cron_job

    @staticmethod
    def get_type() -> str:
        return "cron"
