from redisamp.db import db
from redisamp.widgets.keys import BaseKey


from rich.table import Table
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static


class SetKey(BaseKey):
    def compose(self) -> ComposeResult:
        redis = db.sync
        s = redis.smembers(self.key)

        table = Table(show_header=False, expand=True)
        table.add_column("Value", style="bright_white")
        [table.add_row(val) for val in s]
        yield Container(Static(table))