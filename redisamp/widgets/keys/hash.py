from redisamp.db import db
from redisamp.widgets.keys import BaseKey


from rich.table import Table
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static


class HashKey(BaseKey):
    def compose(self) -> ComposeResult:
        redis = db.sync
        h = redis.hgetall(self.key)
        table = Table(show_header=False, expand=True, show_lines=True)
        table.add_column("Key", style="cyan bold")
        table.add_column("Value", style="bright_white")
        [table.add_row(k, v) for k, v in h.items()]
        yield Container(Static(table))