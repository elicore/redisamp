import dataclasses
from textual import log
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Checkbox


@dataclasses.dataclass
class RedisConnection:
    hostname: str
    port: int
    username: str
    password: str

    tls: bool  # use TLS to connect
    insecure: bool  # skip TLS cert validation
    cert_file: str
    key_file: str

    db: int  # db number

    socket: str

    @property
    def uri(self) -> str:
        pass

    @uri.setter
    def set_uri(self, uri: str):
        pass


class ConnectionScreen(ModalScreen):
    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        with Vertical(id="connections"):
            with Horizontal():
                yield Label("Hostname:")
                yield Input(id="hostname_input")
            with Horizontal():
                yield Label("Port:")
                yield Input(id="port_input", placeholder="6379")
            with Horizontal():
                yield Label("Username:")
                yield Input(id="username_input")
            with Horizontal():
                yield Label("Password:")
                yield Input(id="password_input")
            with Horizontal():
                yield Label("Use TLS:")
                yield Checkbox(id="tls_checkbox")
            with Horizontal():
                yield Label("Validate certificate:")
                yield Checkbox(id="insecure_checkbox")

    def on_unmount(self) -> None:
        # TODO if the connection changed, recreate the connection and refresh
        log.debug("Connection screen unmounting...")
