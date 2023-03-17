class ReedJobExecuteEvent:
    EVENT_JOB_EXECUTE_DETAIL = 2 ** 32
    def __init__(self, code, app_id, job_id, job_name, callback_url, header, busi_params, response, exception):
        self.code = code
        self.app_id = app_id
        self.job_id = job_id
        self.job_name = job_name
        self.callback_url = callback_url
        self.header = header
        self.busi_params = busi_params
        self.response = response
        self.exception = exception

