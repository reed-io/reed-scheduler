from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from utils.EnderUtil import SysUtil

redis_config = {
    "host": SysUtil.get_os_env("REDIS_HOST"),
    "port": 6379,
    "password": SysUtil.get_os_env("REDIS_PASSWORD"),
    "db": 14
}

scheduler_config = {
    "jobstores": {
        'default': RedisJobStore(**redis_config)
    },
    "executors": {
        'default': ThreadPoolExecutor(10)
    },
    "job_defaults": {
        'coalesce': False,  # 不许合并执行
        'max_instances': 1  # 默认最大示例数一律为1
    }
}

# scheduler = AsyncIOScheduler(**scheduler_config)


def create_background_scheduler(scheduler_config):
    return BackgroundScheduler(scheduler_config)

def init_scheduler():
    scheduler.start()

def pause_scheduler():
    scheduler.pause()

def resume_scheduler():
    scheduler.resume()

def wakeup_scheduler():
    scheduler.wakeup()

def shutdown_scheduler():
    scheduler.shutdown()

scheduler = BackgroundScheduler(**scheduler_config)

