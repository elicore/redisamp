from textual import log
from textual.screen import Screen


class SettingsScreen(Screen):
    BINDINGS = [("escape,q,ctrl+t", "app.pop_screen", "Back")]

    def on_mount(self):
        terminal: Terminal = Terminal(command="zsh", id="terminal_bash")
        self.mount(terminal)
        terminal.start()

    def on_unmount(self) -> None:
        # TODO if the connection changed, recreate the connection and refresh
        log.debug("Settings screen unmounting...")
