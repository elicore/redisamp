from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import LoadingIndicator


class BaseKey(Widget):
    def __init__(self, key: str, *args, **kwargs) -> None:
        self.key = key
        super().__init__(*args, **kwargs)
    
    def compose(self) -> ComposeResult:
        yield LoadingIndicator()