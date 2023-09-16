from textual.app import App, ComposeResult
from textual.widgets import Label, ListItem, ListView, Header
import time

num_items = 10000
start_time: float

class ListViewExample(App):
    # CSS_PATH = "list_view.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        global start_time
        start_time = time.time()
        yield Header()
        with ListView():
            for i in range(num_items):
                yield ListItem(Label(f"{i}"))
        
        total_time = time.time() - start_time

        yield Label(f"yielded {num_items} items in {total_time} seconds.")
    
    def on_mount(self):
        total_time = time.time() - start_time
        app.screen.title = f"Up after {total_time} seconds."



app = ListViewExample()
# app.run()