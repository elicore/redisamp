from typing import Generator
from dataclasses import dataclass

from redis import Redis as RedisSync
from redis.asyncio import Redis


@dataclass
class RedisDB:
    redis: Redis = None
    sync: RedisSync = None
    bytes: Redis = None

    def __init__(self, uri: str = "redis://localhost"):
        self.init(uri)
    
    def init(self, uri: str = "redis://localhost"):
        self.redis = Redis.from_url(uri, decode_responses=True)
        self.sync = RedisSync.from_url(uri, decode_responses=True)
        self.bytes = Redis.from_url(uri)

    @property
    def online(self) -> bool:
        try:
            self.sync.ping()
            return True
        except Exception:
            return False

db = RedisDB()

TYPE_NAMES = {
    "ReJSON-RL": "JSON",
    "hash": "Hash",
    "string": "String",
    "list": "List",
    "set": "Set",
    "zset": "ZSet",
    "stream": "Stream",
    "graphdata": "Graph",
    "TSDB-TYPE": "TS",
    "MBbloom--": "Bloom",
}

@dataclass
class RedisKey:
    name: str
    type: str
    ttl: int = -1


def redis_keys(pattern: str = "*", count: int = 100, batch_size: int = 10) -> Generator[RedisKey, None, None]:
    redis = db.sync
    # create an async generator that yields keys in batches
    cursor = "0"
    fetched_count = 0
    while cursor != 0 and fetched_count < count:
        cursor, keys = redis.scan(cursor=cursor, match=pattern, count=batch_size)
        fetched_count += len(keys)
        p = redis.pipeline()
        for k in keys:
            p.type(k)
            p.ttl(k)
        res = p.execute()

        for i, key in enumerate(keys):
            j = i*2
            _type = res[j]
            ttl = max(res[j + 1],  -1)

            yield RedisKey(name=key, type=_type, ttl=ttl)
