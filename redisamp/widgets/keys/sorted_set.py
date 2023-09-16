from redisamp.db import db
from redisamp.widgets.keys import BaseKey


from rich.table import Table, box
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static


class SortedSetKey(BaseKey):
    def compose(self) -> ComposeResult:
        redis = db.sync
        # get first 100 values by score
        z = redis.zrange(self.key, 0, 100, withscores=True)

        table = Table(box=box.MINIMAL)
        table.add_column("Member", style="bright_white bold")
        table.add_column("Score", style="white")
        [table.add_row(m, str(s)) for (m, s) in z]
        yield Container(Static(table))