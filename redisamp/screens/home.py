import asyncio
from textual.app import ComposeResult

from textual import log, on, work
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Footer, Input, ListView, Header
from textual.worker import Worker
from redisamp import redis

from redisamp.widgets.keys_list import KeysList
from redisamp.widgets.key_view import KeyView

KEYS_LIST_ID = "keys-list"
KEY_VIEW_ID = "key-view"
KEYS_FILTER_ID = "keys-filter"

KEYS_LIST_SELECTOR = f"#{KEYS_LIST_ID}"
KEY_VIEW_SELECTOR = f"#{KEY_VIEW_ID}"
KEYS_FILTER_SELECTOR = f"#{KEYS_FILTER_ID}"


class HomeScreen(Screen):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("slash", f"focus('{KEYS_FILTER_ID}')", "Filter"),
    ]

    class KeysFilterChanged(Message):
        def __init__(self, filter_expression: str = '*') -> None:
            self.filter_expression = filter_expression
            super().__init__()
    
    @on(KeysFilterChanged)
    async def fetch_keys(self, message: KeysFilterChanged) -> None:
        worker: Worker = self.scan_keys(message.filter_expression)
        while worker.is_running:
            await asyncio.sleep(0.05)
        
        if worker.is_finished:
            keys_list: KeysList = self.query_one(KEYS_LIST_SELECTOR)
            keys_list.set_keys(worker.result)

    @work(exclusive=True)
    async def scan_keys(self, filter: str = "*", count: int = 1000) -> list[str]:
        keys = await redis.scan(match=filter, count=count)
        log(f"{len(keys[1])} keys matched the filter '{filter}'")

        return keys[1]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Vertical():
            keys_filter = Input(id=KEYS_FILTER_ID, placeholder="*")
            keys_filter.border_title = "Keys Filter"
            yield keys_filter
            with Horizontal():
                yield KeysList(id=KEYS_LIST_ID)
                yield KeyView(id=KEY_VIEW_ID)
            yield Footer()        

        self.post_message(self.KeysFilterChanged())

    @on(Input.Changed, KEYS_FILTER_SELECTOR)
    def key_filter_changed(self, message: Input.Changed) -> None:
        self.post_message(self.KeysFilterChanged(message.value))

    def on_mount(self):
        self.query_one("#keys-list").focus()

    @on(ListView.Highlighted, KEYS_LIST_SELECTOR)
    def key_selected(self, highlighted: ListView.Highlighted):
        if not highlighted.item:
            return

        keys_list: KeysList = highlighted.list_view

        if keys_list.index is not None:
            key = keys_list.keys[keys_list.index]

            key_view: KeyView = self.query_one(KeyView)
            key_view.key_type = key.type
            key_view.key = key.name
