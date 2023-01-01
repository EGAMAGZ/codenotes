from textual.app import App, ComposeResult
from textual.widgets import Label, Header, Footer


class CodenotesApp(App):
    BINDINGS = [("d", "toggle_dark", "Toogle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Welcome to Codenotes!")
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


if __name__ == "__main__":
    app = CodenotesApp()
    app.run()
