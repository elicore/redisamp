from textual.screen import ModalScreen
from redisamp.db import db, SearchIndex
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Collapsible
from textual.app import ComposeResult
from textual.widgets import Label

class SearchIndexScreen(ModalScreen):
    BINDINGS = [
        ("escape", "app.switch_mode('home')", "Back"),
        ("q", "quit", "Quit"),
        ]

    # list redis search indexes
    def list_indexes(self) -> list[str]:
        return db.sync.execute_command("FT._LIST")
    
    def get_index(self, index_name: str) -> dict:
        return db.sync.ft(index_name).info()

    def compose(self) -> ComposeResult:
        yield Label("Search Indexes")
        with Horizontal():
            with VerticalScroll():
                for index in self.list_indexes():
                    si = SearchIndex(self.get_index(index))
                    if si:
                        with Collapsible(title=index, id=index):
                            yield Label(f"Name: {si.name}")
                            yield Label(f"Type: {si.key_type}")
                            yield Label(f"Prefixes: {si.prefixes}")
                            yield Label(f"Num Docs: {si.num_docs}")
                            yield Label(f"Indexing: {si.is_indexing}")
                            yield Label(f"Indexing Progress: {si.indexing_progress*100:.2f}%")  # formatted as percentage
                            yield Label(f"Size: {si.size_mb} MB")
