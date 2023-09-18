from dataclasses import dataclass

from typing import Generator


@dataclass
class RedisKey:
    name: str
    type: str
    ttl: int = -1


def redis_keys(pattern: str = "*", count: int = 100, batch_size: int = 10) -> Generator[RedisKey, None, None]:
    from redisamp.db import db  # TODO ugly patch to avoid circular import. fix this.

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