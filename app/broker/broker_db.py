import socket

import redis
from redis.backoff import ExponentialBackoff
from redis.exceptions import ConnectionError, TimeoutError
from redis.retry import Retry

from app.core.config import settings

host = settings.REDIS_HOST
password = settings.REDIS_PASSWORD
port = settings.REDIS_PORT

retry = Retry(ExponentialBackoff(), 6)

Broker = redis.StrictRedis(
    host=host,
    password=password,
    port=port,
    db=0,
    retry=retry,
    retry_on_error=[ConnectionError, TimeoutError, socket.timeout],
    decode_responses=True,
    health_check_interval=5,
)
