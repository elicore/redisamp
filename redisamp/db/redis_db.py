from redis import Redis as RedisSync
from redis.asyncio import Redis


from dataclasses import dataclass


@dataclass
class RedisDB:
    redis: Redis = None
    sync: RedisSync = None
    bytes: Redis = None

    def __init__(self, uri: str = "redis://localhost"):
        self.init(uri)

    def init(self, uri: str = "redis://localhost"):
        # TODO check protocol version compatibility
        self.redis = Redis.from_url(uri, decode_responses=True, protocol=3)
        self.sync = RedisSync.from_url(uri, decode_responses=True, protocol=3)
        self.bytes = Redis.from_url(uri, protocol=3)

    @property
    def online(self) -> bool:
        try:
            self.sync.ping()
            return True
        except Exception:
            return False