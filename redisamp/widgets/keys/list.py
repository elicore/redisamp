from redisamp import redis_sync as redis
from redisamp.widgets.keys import BaseKey


from rich.table import Table, box
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static


class ListKey(BaseKey):
    def compose(self) -> ComposeResult:
        # get first 100 values
        _list = redis.lrange(self.key, 0, 101)

        table = Table(box=box.MINIMAL, expand=True)  # show_header=False,
        table.add_column("Index", style="bright_black", max_width=5)
        table.add_column("Value", style="bright_white")
        [table.add_row(str(i), val) for i, val in enumerate(_list)]
        yield Container(Static(table))