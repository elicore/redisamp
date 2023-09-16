from textual.screen import ModalScreen
from redisamp.db import db
from textual.containers import Horizontal
from textual.app import ComposeResult
from textual.widgets import Label, Placeholder

class SearchScreen(ModalScreen):
    BINDINGS = [("escape", "app.switch_mode('home')", "Back")]

    # list redis search indexes
    def list_indexes(self) -> list[str]:
        return db.sync.execute_command("FT._LIST")

    def compose(self) -> ComposeResult:
        with Horizontal():
            for index in self.list_indexes():
                yield Label(index)
        yield Placeholder("TODO")
