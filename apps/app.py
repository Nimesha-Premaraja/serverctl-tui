from datetime import datetime

from dashboard import update_dashboard
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import Digits, Footer, Header, Label, ProgressBar, Static


class MetricCard(Static):
    """A stat card showing a labeled gauge with a headline value."""

    def __init__(self, title: str, card_id: str) -> None:
        super().__init__(id=card_id, classes="metric-card")
        self._title = title

    def compose(self) -> ComposeResult:
        yield Label(self._title, classes="metric-title")
        yield Digits("0.0", id=f"{self.id}-value", classes="metric-value")
        yield ProgressBar(
            total=100,
            show_eta=False,
            show_percentage=False,
            id=f"{self.id}-bar",
        )
        yield Static("", id=f"{self.id}-detail", classes="metric-detail")


class LinuxDashboard(App):
    """Real-time Linux system dashboard built with Textual and psutil."""

    TITLE = "ServerCtl"
    SUB_TITLE = "System Monitor"

    CSS_PATH = "app.tcss"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("d", "toggle_dark", "Theme"),
    ]

    refresh_interval: reactive[float] = reactive(2.0)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Vertical(id="dashboard"):
            with Horizontal(id="stats"):
                yield MetricCard("CPU", "cpu")
                yield MetricCard("MEMORY", "memory")
                yield MetricCard("DISK", "disk")

            with Horizontal(id="panels"):
                with Vertical(id="system-panel", classes="panel"):
                    yield Label("SYSTEM", classes="panel-title")
                    yield Static(id="system-info", classes="panel-body")

                with Vertical(id="network-panel", classes="panel"):
                    yield Label("NETWORK", classes="panel-title")
                    yield Static(id="network-info", classes="panel-body")

            with Horizontal(id="status-bar"):
                yield Static("● LIVE", id="status-indicator")
                yield Static("", id="status-updated")
                yield Static(
                    "R Refresh   D Theme   Q Quit",
                    id="status-hints",
                )

        yield Footer()

    def on_mount(self) -> None:
        update_dashboard(self)
        self.set_interval(self.refresh_interval, lambda: update_dashboard(self))

    def action_refresh(self) -> None:
        update_dashboard(self)

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-light" if self.theme == "textual-dark" else "textual-dark"
        )

    def mark_updated(self) -> None:
        stamp = datetime.now().strftime("%H:%M:%S")
        self.query_one("#status-updated", Static).update(f"Updated {stamp}")

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
