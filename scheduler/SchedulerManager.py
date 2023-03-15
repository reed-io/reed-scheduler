from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor



redis_config = {
    "host": "redis host",
    "port": 6379,
    "password": "redis password",
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
        'coalesce': False,
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

