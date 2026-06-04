from redis import Redis
from rq import Queue, SimpleWorker
from ..config import REDIS_HOST, REDIS_PORT

redis_connection = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
)

queue = Queue(connection=redis_connection)


def start_worker():
    worker = SimpleWorker([queue], connection=redis_connection)
    worker.work()
