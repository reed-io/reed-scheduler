import os
from utils.EnderUtil import TimeUtil

print(os.getenv("REDIS_HOST"))
print(os.environ["REDIS_HOST"])


print(TimeUtil.now())
