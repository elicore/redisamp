from textual import log, work
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Label, ListItem, ListView, Placeholder

from redisamp.db import TYPE_NAMES, RedisKey, redis_keys


class KeyItem(ListItem):
    def __init__(self, redis_key: RedisKey, *args, **kwargs):
        self.redis_key = redis_key
        ttl = redis_key.ttl
        self.ttl = f"{ttl}s" if ttl > 0 else "∞"
        self.icon = TYPE_NAMES.get(redis_key.type, "?")
        super().__init__(*args, **kwargs)
    
    def compose(self) -> ComposeResult:
        with Horizontal():
            with Horizontal(classes="type-container"):
                yield Label(self.icon, classes=f"type {self.redis_key.type}")
            yield Label(self.redis_key.name, classes="key-name")
            yield Placeholder(self.ttl, classes="ttl")


class KeysList(ListView):
    keys: list[RedisKey] = reactive(list())

    def compose(self) -> ComposeResult:
        if not self.keys:
            self.border_title = "No Keys"
            return
        yield from super().compose()
        
    async def clear(self):
        await super().clear()
        self.keys.clear()

    @work(exclusive=True)
    async def update_keys(self, filter: str = "*", count=1000):
        async for key in redis_keys(filter, count):
            self.keys.append(key)
            await self.append(KeyItem(key))
            self.border_title = f"{len(self.keys)} Keys"      
        
        log(f"Refreshed list with {len(self.keys)} keys.")