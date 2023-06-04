from redisamp import redis_sync as redis, redis_bytes
from redisamp.widgets.keys import BaseKey


from textual import log
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static


class StringKey(BaseKey):
    def compose(self) -> ComposeResult:
        try:
            v = redis.get(self.key)
        except UnicodeDecodeError as ude:
            log.debug(ude)
            b = redis_bytes.get(self.key)
            v = b

        yield Container(Static(v))