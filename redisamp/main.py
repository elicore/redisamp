import typer
from textual.app import App

from redisamp.db import db
from redisamp.screens import HomeScreen, ConnectionScreen, SearchIndexScreen


class Redisamp(App):
    CSS_PATH = "main.tcss"
    MODES = {
        "default": "home",
        "home": "home",
        "connections": ConnectionScreen(),
        "search": SearchIndexScreen(),
    }

    SCREENS = {
        "home": HomeScreen(),
    }

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("c", "switch_mode('connections')", "Connections"),
        ("s", "switch_mode('search')", "Search"),
    ]

    def on_mount(self) -> None:
        self.switch_mode("default")


app = Redisamp()


def run_app(url: str = typer.Option("redis://localhost", help="Redis connection URL", envvar="REDIS_URL")):
    db.init(url)
    if db.online:
        app.run()

# def main():
#     typer.run(run_app)

if __name__ == "__main__":
    typer.run(run_app)
