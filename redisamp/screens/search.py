from textual.screen import ModalScreen
from redisamp.db import db
from textual import log
from textual.containers import Horizontal
from textual.app import ComposeResult
from textual.widgets import Label, Placeholder, Button

class SearchScreen(ModalScreen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    # list redis search indexes
    def list_indexes(self) -> list[str]:
        return db.sync.execute_command("FT._LIST")

    def compose(self) -> ComposeResult:
        with Horizontal():
            for index in self.list_indexes():
                yield Label(index)
        # yield Label("Search")
        yield Placeholder("TODO")
        # yield Button("Search", self.search)
