from textual import log, work
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Label, ListItem, ListView, Placeholder

from redisamp.keys import TYPE_NAMES, RedisKey
from redisamp import redis


class KeyItem(ListItem):
    def __init__(self, redis_key: RedisKey, ttl: int = -1, *args, **kwargs):
        self.redis_key = redis_key
        self.ttl = f"{ttl}s" if ttl > 0 else "∞"
        super().__init__(*args, **kwargs)
    
    def compose(self) -> ComposeResult:
        _type = self.redis_key.type
        _key = self.redis_key.name
        icon = TYPE_NAMES.get(_type, "?")

        with Horizontal():
            with Horizontal(classes="type-container"):
                yield Label(icon, classes=f"type {_type}")
            yield Label(_key, classes="key-name")
            yield Placeholder(self.ttl, classes="ttl")


class KeysList(ListView):
    keys: list[RedisKey] = reactive(list())

    @work(exclusive=True)
    async def set_keys(self, keys: list):
        if not keys:
            self.border_title = "No Keys"
            return
        
        p = redis.pipeline()
        for k in keys:
            p.type(k)
            p.ttl(k)
        res = await p.execute()

        self.keys.clear()
        if len(self) > 0:
            self.clear()
    
        for i in range(len(keys)):
            k = keys[i]
            j = i*2
            _type = res[j]
            ttl = res[j + 1] if res[j + 1] > 0 else -1

            redis_key = RedisKey(name=k, type=_type)
            self.keys.append(redis_key)
            self.append(KeyItem(redis_key, ttl=ttl))
        
        self.border_title = f"{len(self.keys)} Keys"

        log(f"Refreshed list with {len(self.keys)} keys.")
