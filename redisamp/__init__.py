from redis.asyncio import Redis
from redis import Redis as RedysSync

__version__ = '0.0.1'

redis = Redis(decode_responses=True)
redis_sync = RedysSync(decode_responses=True)
redis_bytes = Redis()