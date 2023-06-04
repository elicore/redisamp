from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Label

from redisamp import redis
from redisamp.widgets.keys import (BaseKey, render_key)


class KeyView(Vertical):
    key: reactive[str] = reactive("")
    key_type: reactive[str] = reactive("")
    ttl: reactive[int] = reactive(-1)
    key_size: reactive[int] = reactive(-1)

    _ttl = Label(classes="ttl")
    _key_size = Label(classes="key-size")

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield self._key_size
            yield self._ttl

    def watch_ttl(self, ttl: int):
        self._ttl.update(f"TTL: {ttl if ttl > 0 else '∞'}")

    def watch_key_size(self, size: int):
        self._key_size.update(f"[b]Size:[/b] {size} bytes")

    async def watch_key(self, key: str):
        try:
            # remove the previous key view
            self.query_one(BaseKey).remove()
        except NoMatches:
            pass

        # get the display values
        key_view = render_key(self.key_type, key)
        self.mount(key_view)

        self.border_title = key

        self.ttl = await redis.ttl(key)
        self.key_size = await redis.memory_usage(key)
