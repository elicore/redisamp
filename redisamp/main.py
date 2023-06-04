import typer
from redis import Redis
from textual.app import App
from .screens import HomeScreen, ConnectionScreen


class Redisamp(App):
    CSS_PATH = "main.css"
    SCREENS = {
        "connections": ConnectionScreen(),
        "home": HomeScreen()
    }

    def on_mount(self) -> None:
        self.push_screen("home")


app = Redisamp()


def run_app(uri: str = typer.Option("redis://localhost", help="Redis connection URI")):
    from redisamp import redis, redis_bytes
    redis = Redis.from_url(uri, decode_responses=True)
    redis_bytes = Redis.from_url(uri)
    app.run()

def main():
    typer.run(run_app)

if __name__ == "__main__":
    main()
