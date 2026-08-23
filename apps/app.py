from dashboard import update_dashboard
from textual.app import App, ComposeResult
from textual.containers import Grid, Horizontal, Vertical
from textual.widgets import Footer, Header, Label, Static


class LinuxDashboard(App):
    """Real-time Linux system dashboard using Textual and psutil."""

    TITLE = "Linux Server Dashboard"

    CSS_PATH = "app.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Vertical(id="dashboard"):
            with Horizontal(id="stats"):
                yield Static(id="cpu", classes="stat")
                yield Static(id="memory", classes="stat")
                yield Static(id="disk", classes="stat")

            with Horizontal(id="system"):
                with Vertical(classes="panel"):
                    yield Label("SYSTEM", classes="panel-title")
                    yield Static(id="system-info")

                with Vertical(classes="panel"):
                    yield Label("NETWORK", classes="panel-title")
                    yield Static(id="network-info")

            yield Static("Press R to refresh • Press Q to quit", id="footer-info")

        yield Footer()

    def on_mount(self) -> None:
        update_dashboard(self)
        self.set_interval(2, lambda: update_dashboard(self))

    def action_refresh(self) -> None:
        update_dashboard(self)

    @staticmethod
    def bytes_to_gb(value: int) -> float:
        return value / (1024 ** 3)

    @staticmethod
    def bytes_to_mb(value: int) -> float:
        return value / (1024 ** 2)

    @staticmethod
    def format_uptime(seconds: float) -> str:
        days, seconds = divmod(int(seconds), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, _ = divmod(seconds, 60)

        return f"{days}d {hours}h {minutes}m"


if __name__ == "__main__":
    LinuxDashboard().run()
