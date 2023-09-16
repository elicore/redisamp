from textual import log, work
from textual.app import ComposeResult
from textual.widgets import DataTable
from rich.text import Text
from rich.style import Style

from redisamp.db import TYPE_NAMES, RedisKey, redis_keys

class KeysList(DataTable):
    keys: list[RedisKey] = list()

    def compose(self) -> ComposeResult:
        if not self.keys:
            self.border_title = "No Keys"
            return
        yield from super().compose()
        
    def clear(self):
        super().clear()
        self.keys.clear()
    
    def on_mount(self) -> None:
        self.add_columns("name", "ttl")
        super().on_mount()

    @work(exclusive=True, thread=True)
    def update_keys(self, filter: str = "*", count=1000):
        for key in redis_keys(filter, count):
            self.keys.append(key)
            row = [Text(key.name, style="bold", overflow="ellipsis"), Text(f"{key.ttl}", style="dim")]
            label_style = Style(bgcolor="magenta")
            label = Text(TYPE_NAMES.get(key.type, "?"), justify="center", style=label_style)
            self.add_row(*row, key=key.name, label=label)
            self.border_title = f"{len(self.keys)} Keys"      
        
        log(f"Refreshed list with {len(self.keys)} keys.")