from define.BaseErrorCode import BaseErrorCode
from define.ErrorCode import ErrorCode

class ReedSchedulerErrorCode(BaseErrorCode):
    """
        0x00C0~0x00DF
    """
    APPID_EMPTY = ErrorCode(code=0x00c0, message="path variable {app_id} is empty!")
    SECONDS_TYPE_ERROR = ErrorCode(code=0x00c1, message="form parameter {seconds} can not be recognized as an integer!")
    SECONDS_IS_ZERO = ErrorCode(code=0x00c2, message="form parameter {seconds} is zero, we can not accept that!")
    CALLBACK_URL_EMPTY = ErrorCode(code=0x00c3, message="form parameter {callback_url} is empty!")
    CALLBACK_URL_INVALIDATE = ErrorCode(code=0x00c4, message="form parameter {callback_url} is not a url format, please check!")
    JOBID_EMPTY = ErrorCode(code=0x00c5, message="path variable {job_id} is empty!")
    DATETIME_EMPTY = ErrorCode(code=0x00c6, message="form parameter {datetime} is empty!")
    DATETIME_INVALIDATE = ErrorCode(code=0x00c7, message="form parameter {datetime} is invalidate, only {%Y-%m-%d %H:%M:%S} format accepted!")
    DATETIME_PASSED = ErrorCode(code=0x00c8, message="form parameter {datetime} is already passed, please check!")
    START_TIME_INVALIDATE = ErrorCode(code=0x00c9, message="form parameter {start_time} is invalidate, only {%Y-%m-%d %H:%M:%S} format accepted!")
    END_TIME_INVALIDATE = ErrorCode(code=0x00ca, message="form parameter {end_time} is invalidate, only {%Y-%m-%d %H:%M:%S} format accepted!")
    START_TIME_LATER_THAN_END_TIME = ErrorCode(code=0x00cb, message="form parameter {start_time} maybe later than {end_time}, please check!")
    JOB_TYPE_ERROR = ErrorCode(code=0x00cc, message="job type not match, please contact chenxiwen@cnpc.com.cn")
    ALL_CRON_BIT_DEFAULT = ErrorCode(code=0x00cd, message="form parameter year, month, day, week, day_of_week, hour, minute, second are all default value!")
    YEAR_INVALIDATE = ErrorCode(code=0x00ce, message="form parameter {year} is invalidate! should be * or integer between 1900 and 9999")
    MONTH_INVALIDATE = ErrorCode(code=0x00cf, message="form parameter {month} is invalidate! should be * or integer between 1 and 12")
    DAY_INVALIDATE = ErrorCode(code=0x00d0, message="form parameter {day} is invalidate! should be * or integer between 1 and 31")
    WEEK_INVALIDATE = ErrorCode(code=0x00d1, message="form parameter {week} is invalidate! should be * or integer between 1 and 53")
    DAY_OF_WEEK_INVALIDATE = ErrorCode(code=0x00d2, message="form parameter {day_of_week} is invalidate! should be * or between 0 and 6 or [mon,tue,wed,thu,fri,sat,sun]")
    HOUR_INVALIDATE = ErrorCode(code=0x00d3, message="form parameter {hour} is invalidate! should be * or integer between 0 and 23")
    MINUTE_INVALIDATE = ErrorCode(code=0x00d4, message="form parameter {minute} is invalidate! should be * or integer between 0 and 59")
    SECOND_INVALIDATE = ErrorCode(code=0x00d5, message="form parameter {second} is invalidate! should be * or integer between 0 and 59")
    APPID_INVALIDATE = ErrorCode(code=0x00d6, message="path variable {app_id} is invalidate! only characters and numbers accepted and length should between 5 and 16!")
    ACTION_EMPTY = ErrorCode(code=0x00d7, message="form parameter {action} is empty!")
    ACTION_INVALIDATE = ErrorCode(code=0x00d8, message="form parameter {action} is invalidate, only pause or resume accepted!")
    JOB_NOT_FOUND = ErrorCode(code=0x00d9, message="can not find job by this job_id, please check, or maybe this job is already finished")