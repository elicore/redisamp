from redisamp.db import RedisKey, TYPE_NAMES

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class KeyActionsScreen(ModalScreen):
    """Screen with a dialog to quit."""
    BINDINGS = [
        ("escape", "app.pop_screen()", "Cancel"),
    ]

    def __init__(self, key: RedisKey, *args, **kwargs) -> None:
        self.key = key
        super().__init__(*args, **kwargs)

    @property
    def title(self):
        return f"[{TYPE_NAMES[self.key.type]}] {self.key}"

    def compose(self) -> ComposeResult:
        main = Vertical(id="key-actions")
        main.border_title = self.title
        with main:
            Label(f"Key actions for: {self.key}")#, id="question"),
            with Horizontal():
                yield Label("Extend TTL")
                yield Button("TTL", classes="action-button")
            with Horizontal():
                yield Label("Delete")
                yield Button("Delete", classes="action-button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()