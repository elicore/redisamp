import typer
from textual.app import App

from redisamp.db import db
from redisamp.screens import HomeScreen, ConnectionScreen, SearchScreen


class Redisamp(App):
    CSS_PATH = "main.tcss"
    SCREENS = {
        "connections": ConnectionScreen(),
        "home": HomeScreen(),
        "search": SearchScreen(),
    }

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("c", "push_screen('connections')", "Connections"),
        ("s", "push_screen('search')", "Search"),
        # ("slash", "focus('keys-filter')", "Filter"),
    ]

    def on_mount(self) -> None:
        self.push_screen("home")


app = Redisamp()


def run_app(uri: str = typer.Option("redis://localhost", help="Redis connection URI")):
    db.init(uri)
    if db.online:
        app.run()

def main():
    typer.run(run_app)

if __name__ == "__main__":
    main()
